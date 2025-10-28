from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from trips.models import UserProfile, Comment, Trip
from django.db import models


class Command(BaseCommand):
    help = 'Delete all non-admin users and create profiles for admin users'

    def handle(self, *args, **options):
        # Get all admins and normal users
        admin_users = User.objects.filter(models.Q(is_superuser=True) | models.Q(is_staff=True))
        normal_users = User.objects.exclude(models.Q(is_superuser=True) | models.Q(is_staff=True))

        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(f"Admin users: {admin_users.count()}")
        self.stdout.write(f"Normal users (will be deleted): {normal_users.count()}")
        self.stdout.write(f"{'='*60}\n")

        # Create Profile for admins
        self.stdout.write("Processing admin users...")
        for user in admin_users:
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f"[CREATED] Profile for {user.username}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"[OK] User {user.username} already has profile"))

        # Delete normal users and their data
        if normal_users.count() > 0:
            self.stdout.write(f"\nDeleting {normal_users.count()} normal users...")
            for user in normal_users:
                # Delete user's comments
                comments_count = Comment.objects.filter(user=user).count()
                Comment.objects.filter(user=user).delete()
                
                # Delete user's trips
                trips_count = Trip.objects.filter(author=user).count()
                Trip.objects.filter(author=user).delete()
                
                # Delete user
                username = user.username
                user.delete()
                self.stdout.write(f"[DELETED] User: {username} (comments: {comments_count}, trips: {trips_count})")
            
            self.stdout.write(self.style.SUCCESS(f"\nCompleted! Deleted {normal_users.count()} users"))
        else:
            self.stdout.write("\nNo normal users to delete")

        # Final statistics
        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(f"Admin users: {User.objects.filter(models.Q(is_superuser=True) | models.Q(is_staff=True)).count()}")
        self.stdout.write(f"Total users: {User.objects.count()}")
        self.stdout.write(f"{'='*60}\n")

