#!/usr/bin/env python
"""
COS 配置和权限检查脚本
用于诊断文件上传成功但前端无法显示的问题
"""
import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roamio.settings')
django.setup()

from django.conf import settings
from trips.models import Comment

print("=" * 60)
print("腾讯云 COS 配置检查")
print("=" * 60)

# 1. 检查配置
print("\n1. 环境配置检查:")
print(f"   SECRET_ID: {settings.TENCENT_COS_SECRET_ID[:10]}..." if settings.TENCENT_COS_SECRET_ID else "   SECRET_ID: ❌ 未配置")
print(f"   SECRET_KEY: {settings.TENCENT_COS_SECRET_KEY[:10]}..." if settings.TENCENT_COS_SECRET_KEY else "   SECRET_KEY: ❌ 未配置")
print(f"   BUCKET: {settings.TENCENT_COS_BUCKET}")
print(f"   REGION: {settings.TENCENT_COS_REGION}")

# 2. 检查最新评论
print("\n2. 数据库检查:")
comments_with_images = Comment.objects.filter(image__isnull=False).order_by('-id')[:5]

if comments_with_images:
    print(f"   找到 {comments_with_images.count()} 条带图片的评论")
    for i, comment in enumerate(comments_with_images, 1):
        print(f"\n   评论 #{i}:")
        print(f"   - ID: {comment.id}")
        print(f"   - 用户: {comment.user.username}")
        print(f"   - 图片 URL: {comment.image}")
        
        # 检查 URL 格式
        if comment.image.startswith('https://'):
            print(f"   ✅ URL 格式正确（HTTPS）")
            
            # 检查 bucket 名称
            if settings.TENCENT_COS_BUCKET in comment.image:
                print(f"   ✅ 存储桶名称匹配")
            else:
                print(f"   ❌ 存储桶名称不匹配！")
                print(f"      配置中: {settings.TENCENT_COS_BUCKET}")
                print(f"      URL中: 请检查")
            
            # 检查区域
            if settings.TENCENT_COS_REGION in comment.image:
                print(f"   ✅ 区域代码匹配")
            else:
                print(f"   ⚠️  区域代码可能不匹配")
        else:
            print(f"   ❌ URL 格式错误（应该以 https:// 开头）")
else:
    print("   ❌ 没有找到带图片的评论")

# 3. 测试 COS 连接
print("\n3. COS 连接测试:")
try:
    from trips.utils.tencent_cos import get_cos_client
    client = get_cos_client()
    print("   ✅ COS 客户端创建成功")
    
    # 尝试列出存储桶中的文件
    try:
        response = client.list_objects(
            Bucket=settings.TENCENT_COS_BUCKET,
            Prefix='media/comments/images/',
            MaxKeys=10
        )
        
        if 'Contents' in response:
            file_count = len(response['Contents'])
            print(f"   ✅ 成功列出文件：{file_count} 个")
            
            if file_count > 0:
                print("\n   最近上传的文件:")
                for obj in response['Contents'][:5]:
                    print(f"   - {obj['Key']}")
                    print(f"     大小: {obj['Size']} 字节")
                    print(f"     修改时间: {obj['LastModified']}")
        else:
            print("   ⚠️  存储桶中没有文件")
    except Exception as e:
        print(f"   ❌ 列出文件失败: {e}")
        
except Exception as e:
    print(f"   ❌ COS 客户端创建失败: {e}")

# 4. 生成测试 URL
print("\n4. 生成的 URL 格式:")
test_filename = "user27_20251101_161958_79feed2a.ico"
test_url = f"https://{settings.TENCENT_COS_BUCKET}.cos.{settings.TENCENT_COS_REGION}.myqcloud.com/media/comments/images/{test_filename}"
print(f"   {test_url}")

print("\n" + "=" * 60)
print("检查完成！")
print("=" * 60)
print("\n下一步操作:")
print("1. 复制上面的测试 URL 在浏览器中打开")
print("2. 如果返回 403 Forbidden，需要设置存储桶为「公有读私有写」")
print("3. 如果返回 404 Not Found，检查文件路径是否正确")
print("4. 如果能正常显示，则问题在前端")
print("=" * 60)

