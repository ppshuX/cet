from django.core.management.base import BaseCommand
from django.db import transaction

from trips.models.site_stat import SiteStat
from trips.models.trip import Trip


class Command(BaseCommand):
    help = (
        "Migrate legacy SiteStat records (page='<slug>') to new TripPlan prefix "
        "records (page='tp:<slug>'). Use --mode to control merge strategy."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would change without writing to the database",
        )
        parser.add_argument(
            "--mode",
            choices=["copy", "sum", "max"],
            default="copy",
            help=(
                "How to migrate counts when destination already exists: "
                "copy=overwrite dest with source; sum=add source to dest; max=take the greater value"
            ),
        )
        parser.add_argument(
            "--only",
            nargs="*",
            help="Limit to specified slugs (space separated)",
        )

    def handle(self, *args, **options):
        dry_run: bool = options["dry_run"]
        mode: str = options["mode"]
        only_slugs = set(options["only"] or [])

        trips_qs = Trip.objects.all().only("id", "slug")
        if only_slugs:
            trips_qs = trips_qs.filter(slug__in=only_slugs)

        migrated = 0
        skipped = 0
        created = 0

        @transaction.atomic
        def migrate_one(trip: Trip):
            nonlocal migrated, skipped, created
            slug = trip.slug
            if not slug:
                skipped += 1
                self.stdout.write(self.style.WARNING(f"Trip {trip.id} has no slug, skip"))
                return

            source_page = slug  # legacy page key
            dest_page = f"tp:{slug}"  # new TripPlan-prefixed page key

            try:
                source = SiteStat.objects.get(page=source_page)
            except SiteStat.DoesNotExist:
                # No legacy record; nothing to migrate
                skipped += 1
                self.stdout.write(self.style.WARNING(f"No legacy stat for {source_page}, skip"))
                return

            dest, was_created = SiteStat.objects.get_or_create(page=dest_page)
            if was_created:
                created += 1

            old_views, old_likes, old_comments = dest.views, dest.likes, getattr(dest, "comments_count", 0)
            if mode == "copy":
                new_views = source.views
                new_likes = source.likes
                new_comments = getattr(source, "comments_count", 0)
            elif mode == "sum":
                new_views = old_views + source.views
                new_likes = old_likes + source.likes
                new_comments = old_comments + getattr(source, "comments_count", 0)
            else:  # max
                new_views = max(old_views, source.views)
                new_likes = max(old_likes, source.likes)
                new_comments = max(old_comments, getattr(source, "comments_count", 0))

            if dry_run:
                self.stdout.write(
                    f"[DRY-RUN] {dest_page}: views {old_views}->{new_views}, "
                    f"likes {old_likes}->{new_likes}, comments {old_comments}->{new_comments} "
                    f"(from {source_page})"
                )
                return

            dest.views = new_views
            dest.likes = new_likes
            if hasattr(dest, "comments_count"):
                dest.comments_count = new_comments
                update_fields = ["views", "likes", "comments_count"]
            else:
                update_fields = ["views", "likes"]
            dest.save(update_fields=update_fields)
            migrated += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"Migrated {source_page} -> {dest_page}: views {old_views}->{new_views}, "
                    f"likes {old_likes}->{new_likes}, comments {old_comments}->{new_comments}"
                )
            )

        for trip in trips_qs.iterator():
            migrate_one(trip)

        summary = (
            f"migrated={migrated}, created_dest={created}, skipped={skipped}, dry_run={dry_run}, mode={mode}"
        )
        if dry_run:
            self.stdout.write(self.style.WARNING(summary))
        else:
            self.stdout.write(self.style.SUCCESS(summary))


