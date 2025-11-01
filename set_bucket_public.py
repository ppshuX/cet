#!/usr/bin/env python
"""设置存储桶为公有读"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roamio.settings')
django.setup()

from trips.utils.tencent_cos import get_cos_client
from django.conf import settings

print("正在设置存储桶权限...")
print(f"存储桶: {settings.TENCENT_COS_BUCKET}")

try:
    client = get_cos_client()
    
    # 设置为公有读
    response = client.put_bucket_acl(
        Bucket=settings.TENCENT_COS_BUCKET,
        ACL='public-read'
    )
    
    print("✅ 存储桶权限已设置为公有读!")
    
    # 验证
    acl_response = client.get_bucket_acl(Bucket=settings.TENCENT_COS_BUCKET)
    print(f"当前 ACL: {acl_response.get('ACL', 'unknown')}")
    
    print("\n请在浏览器中测试:")
    print("https://romaio-media-1326824138.cos.ap-guangzhou.myqcloud.com/media/comments/images/user27_20251101_162315_a906d46c.ico")
    
except Exception as e:
    print(f"❌ 设置失败: {e}")
    print("\n请在腾讯云控制台手动设置:")
    print("1. 登录 https://console.cloud.tencent.com/cos")
    print("2. 选择存储桶 romaio-media-1326824138")
    print("3. 权限管理 → 存储桶访问权限")
    print("4. 公共权限 → 读权限 → 公有读")

