import os
from PIL import Image

image_dir = "media/comment_images"
max_width = 1080
quality = 70
force_compress_size = 1024 * 1024  # 1MB

for filename in os.listdir(image_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        path = os.path.join(image_dir, filename)
        try:
            img = Image.open(path)
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.LANCZOS)  # ✅ 用 Image.LANCZOS

            img = img.convert('RGB')  # 确保能保存为 JPEG
            img.save(path, format='JPEG', quality=quality)

            # 如果还大于 1MB，再压一遍
            if os.path.getsize(path) > force_compress_size:
                img.save(path, format='JPEG', quality=50)

            print(f"✅ 压缩完成：{filename}")

        except Exception as e:
            print(f"❌ 压缩失败：{filename}，原因：{e}")

