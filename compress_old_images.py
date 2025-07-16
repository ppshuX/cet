import os
from PIL import Image

image_dir = "media/comment_images"
max_width = 1080
quality = 70
force_compress_size = 1024 * 1024  # 1MB
min_size = 400 * 1024              # 小于 400KB 的不压

for filename in os.listdir(image_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        path = os.path.join(image_dir, filename)

        try:
            # 小于最小大小的图片不压缩
            if os.path.getsize(path) < min_size:
                print(f"🟡 跳过（文件小于400KB）: {filename}")
                continue

            img = Image.open(path)

            # 如果宽度太大就缩小
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.LANCZOS)

            # 转换为 RGB，避免模式问题
            img = img.convert('RGB')

            # 压缩保存（覆盖原图）
            img.save(path, format='JPEG', quality=quality)

            # 如果还大于 1MB，再压一轮（质量更低）
            if os.path.getsize(path) > force_compress_size:
                img.save(path, format='JPEG', quality=50)

            print(f"✅ 压缩完成并覆盖原图: {filename}")

        except Exception as e:
            print(f"❌ 压缩失败: {filename}，原因：{e}")

