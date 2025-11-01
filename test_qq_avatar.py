#!/usr/bin/env python
"""
测试 QQ 头像下载和上传功能
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roamio.settings')
django.setup()

from django.contrib.auth.models import User
from trips.utils.avatar_downloader import set_user_avatar_from_url

print("=" * 60)
print("QQ 头像下载测试")
print("=" * 60)

# 获取用户
user_id = int(input("\n请输入要测试的用户 ID（默认 27）: ") or "27")

try:
    user = User.objects.get(id=user_id)
    print(f"\n✅ 找到用户: {user.username} (ID: {user.id})")
    print(f"当前头像: {user.profile.avatar or '无'}")
except User.DoesNotExist:
    print(f"\n❌ 用户 ID {user_id} 不存在")
    exit(1)

# 测试 QQ 头像 URL（使用一个公开的测试头像）
test_avatar_url = input("\n请输入 QQ 头像 URL（或按回车使用测试 URL）: ").strip()

if not test_avatar_url:
    # 使用一个公开的测试图片
    test_avatar_url = "https://q.qlogo.cn/headimg_dl?dst_uin=10000&spec=100"

print(f"\n开始下载和上传头像...")
print(f"源 URL: {test_avatar_url}")

# 调用函数
success, message = set_user_avatar_from_url(user, test_avatar_url)

print("\n" + "=" * 60)
if success:
    print("✅ 成功!")
    print(f"消息: {message}")
    
    # 重新加载用户数据
    user.refresh_from_db()
    print(f"新头像 URL: {user.profile.avatar}")
    
    # 验证 URL
    if user.profile.avatar and user.profile.avatar.startswith('https://'):
        print("✅ URL 格式正确（HTTPS）")
        
        # 提示测试访问
        print(f"\n请在浏览器中访问以下 URL 测试:")
        print(user.profile.avatar)
    else:
        print("⚠️  URL 格式可能有问题")
else:
    print("❌ 失败!")
    print(f"错误: {message}")
    
print("=" * 60)

