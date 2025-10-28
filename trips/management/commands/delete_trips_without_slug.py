"""
删除没有slug的旅行计划
"""
from django.core.management.base import BaseCommand
from trips.models import Trip, SiteStat


class Command(BaseCommand):
    help = '删除所有没有slug的旅行计划（排除已在旅行树上的）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='预览将要删除的旅行（不实际删除）',
        )

    def handle(self, *args, **options):
        # 查找没有slug或slug为空的旅行
        trips_without_slug = Trip.objects.filter(
            slug__isnull=True
        ) | Trip.objects.filter(slug='')
        
        # 获取所有在旅行树上的slug列表
        on_tree_slugs = set(SiteStat.objects.values_list('page', flat=True))
        
        # 过滤掉在旅行树上的旅行
        trips_to_delete = []
        trips_on_tree = []
        
        for trip in trips_without_slug:
            # 检查是否在旅行树上
            if trip.slug in on_tree_slugs or not trip.slug:
                # 检查是否有SiteStat记录
                has_site_stat = SiteStat.objects.filter(page=trip.slug).exists()
                if has_site_stat:
                    trips_on_tree.append(trip)
                else:
                    # 即使没有slug，也检查是否在树上（通过标题匹配）
                    on_tree = SiteStat.objects.filter(page=trip.title).exists()
                    if on_tree:
                        trips_on_tree.append(trip)
                    else:
                        trips_to_delete.append(trip)
            else:
                trips_to_delete.append(trip)
        
        # 显示在旅行树上的旅行（不会被删除）
        if trips_on_tree:
            self.stdout.write(self.style.WARNING(f'\n以下 {len(trips_on_tree)} 个旅行在旅行树上，将被跳过:'))
            for trip in trips_on_tree:
                self.stdout.write(f'  ⚠️ ID: {trip.id}, 标题: {trip.title}')
        
        # 显示将要删除的旅行
        if trips_to_delete:
            count = len(trips_to_delete)
            self.stdout.write(f'\n找到 {count} 个没有slug且不在旅行树上的旅行:')
            
            for trip in trips_to_delete:
                self.stdout.write(f'  - ID: {trip.id}, 标题: {trip.title}, 作者: {trip.author.username}')
            
            if options['dry_run']:
                self.stdout.write(self.style.WARNING('\n这是预览模式，未实际删除'))
                return
            
            # 确认删除
            confirm = input(f'\n确定要删除这 {count} 个旅行吗? (yes/no): ')
            
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING('操作已取消'))
                return
            
            # 删除旅行
            trip_ids = [trip.id for trip in trips_to_delete]
            deleted_count = Trip.objects.filter(id__in=trip_ids).delete()[0]
            
            self.stdout.write(self.style.SUCCESS(f'成功删除 {deleted_count} 个旅行计划'))
        else:
            self.stdout.write(self.style.SUCCESS('没有找到需要删除的旅行（所有没有slug的旅行都在旅行树上）'))
