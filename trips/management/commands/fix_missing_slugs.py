"""
修复没有slug的旅行计划，为它们生成新的slug
"""
from django.core.management.base import BaseCommand
from trips.models import Trip
import hashlib
import uuid
from django.utils import timezone


class Command(BaseCommand):
    help = '为没有slug的旅行计划生成新的slug'

    def handle(self, *args, **options):
        # 查找没有slug或slug为空的旅行
        trips_without_slug = Trip.objects.filter(slug__isnull=True) | Trip.objects.filter(slug='')
        
        count = trips_without_slug.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('所有旅行都有slug'))
            return
        
        self.stdout.write(f'找到 {count} 个没有slug的旅行，开始修复...')
        
        fixed_count = 0
        
        for trip in trips_without_slug:
            # 生成新的slug
            unique_id = str(uuid.uuid4())
            timestamp = str(timezone.now().timestamp())
            hash_string = f"{trip.title}_{unique_id}_{timestamp}"
            
            hash_obj = hashlib.md5(hash_string.encode())
            hash_hex = hash_obj.hexdigest()[:12]
            
            trip.slug = hash_hex
            
            # 确保唯一性
            while Trip.objects.filter(slug=trip.slug).exclude(id=trip.id).exists():
                hash_string = f"{trip.title}_{uuid.uuid4()}_{timestamp}"
                hash_obj = hashlib.md5(hash_string.encode())
                hash_hex = hash_obj.hexdigest()[:12]
                trip.slug = hash_hex
            
            trip.save()
            fixed_count += 1
            self.stdout.write(f'  ✓ 修复: {trip.title} -> slug: {trip.slug}')
        
        self.stdout.write(self.style.SUCCESS(f'成功修复 {fixed_count} 个旅行的slug'))
