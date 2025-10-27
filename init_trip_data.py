#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
初始化旅行数据
创建所有旅行页面的SiteStat记录
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roamio.settings')
django.setup()

from trips.models import SiteStat

# 要创建的旅行页面
trips = ['trip', 'trip1', 'trip2', 'trip3', 'trip4']

print("开始初始化旅行数据...")

# 先检查并清理重复数据
print("\n检查重复数据...")
for trip_page in trips:
    existing = SiteStat.objects.filter(page=trip_page)
    count = existing.count()
    
    if count > 1:
        print(f"发现 {trip_page} 有 {count} 条重复记录，正在清理...")
        # 保留第一条，删除其他
        first = existing.first()
        existing.exclude(id=first.id).delete()
        print(f"已清理 {trip_page} 的重复记录，保留了 ID={first.id}")

print("\n创建或更新记录...")
for trip_page in trips:
    # 使用 update_or_create 来避免重复
    stat, created = SiteStat.objects.update_or_create(
        page=trip_page,
        defaults={
            'views': 0,
            'likes': 0,
            'checked_in': False
        }
    )
    
    if created:
        print(f"创建了 {trip_page} 的统计记录")
    else:
        print(f"{trip_page} 的统计记录已存在（已重置为初始值）")

print("\n数据初始化完成！")
print(f"总共有 {SiteStat.objects.count()} 条旅行记录")

# 显示所有记录
print("\n当前旅行列表：")
for stat in SiteStat.objects.all().order_by('page'):
    print(f"  - {stat.page}: 浏览 {stat.views} | 点赞 {stat.likes}")

