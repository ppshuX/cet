import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#评论模型
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 谁发的评论
    content = models.TextField()
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)  # 新增的图片字段
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # 先保存以获得路径

        if self.image:
            try:
                img_path = self.image.path
                img = Image.open(img_path)

                max_width = 1080
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

                # 首次压缩为 JPEG 格式，质量为 70
                img = img.convert('RGB')  # 避免 PNG 无法保存为 JPEG 报错
                img.save(img_path, format='JPEG', quality=70)

                # 如果压缩后仍 > 1MB，执行二次压缩
                if os.path.getsize(img_path) > 1024 * 1024:
                    img.save(img_path, format='JPEG', quality=50)

            except Exception as e:
                print(f"图片压缩失败: {e}")

#网站统计模型
class SiteStat(models.Model):
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    checked_in = models.BooleanField(default=False)
