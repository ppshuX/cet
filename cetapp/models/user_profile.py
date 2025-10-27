"""
用户配置文件模型
"""
import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """用户配置文件模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='user_avatars/', blank=True, null=True, 
                              help_text='用户头像，推荐上传正方形图片')
    
    def __str__(self):
        return f"{self.user.username}的配置"
    
    def get_avatar_url(self):
        """获取头像URL，如果没有头像则返回默认头像"""
        if self.avatar:
            return self.avatar.url
        else:
            # 返回默认头像路径
            return '/static/images/default_avatar.png'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # 如果上传了头像，进行压缩处理
        if self.avatar:
            try:
                img_path = self.avatar.path
                img = Image.open(img_path)
                
                # 裁剪为正方形
                min_side = min(img.width, img.height)
                left = (img.width - min_side) // 2
                top = (img.height - min_side) // 2
                right = left + min_side
                bottom = top + min_side
                img = img.crop((left, top, right, bottom))
                
                # 调整大小为200x200像素
                img = img.resize((200, 200), Image.Resampling.LANCZOS)
                
                # 转换为RGB格式并保存
                img = img.convert('RGB')
                img.save(img_path, format='JPEG', quality=85)
                
            except Exception as e:
                print(f"头像处理失败: {e}")


# 自动为新用户创建配置文件
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)

