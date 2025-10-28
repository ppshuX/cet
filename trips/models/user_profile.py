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
    
    # ========== 扩展字段 - 旅行者信息 ==========
    # 个人简介
    bio = models.TextField(blank=True, max_length=500, help_text='个人简介')
    
    # 用户标签（如：摄影爱好者、美食达人等）
    tags = models.CharField(
        max_length=200, 
        blank=True,
        help_text='用户标签，逗号分隔'
    )
    
    # 访问统计（可选 - 用于缓存）
    visited_countries = models.CharField(
        max_length=200, 
        blank=True,
        help_text='访问过的国家'
    )
    
    # 用户等级
    LEVEL_CHOICES = [
        ('novice', '新手'),
        ('explorer', '探索者'),
        ('wanderer', '漫游者'),
        ('adventurer', '冒险家'),
        ('master', '旅行大师'),
    ]
    level = models.CharField(
        max_length=20, 
        choices=LEVEL_CHOICES, 
        default='novice',
        help_text='用户等级'
    )
    
    def __str__(self):
        return f"{self.user.username}的配置"
    
    @property
    def get_username(self):
        """获取用户名"""
        return self.user.username
    
    @property
    def get_comments(self):
        """获取该用户的所有评论"""
        return self.user.comment_set.all()
    
    @property
    def get_trips(self):
        """获取该用户的所有旅行计划"""
        return self.user.trips.all()
    
    @property
    def get_public_trips(self):
        """获取公开的旅行计划"""
        return self.user.trips.filter(visibility='public')
    
    def calculate_level(self):
        """根据旅行和评论数量自动计算等级"""
        trips_count = self.user.trips.count()
        comments_count = self.user.comment_set.count()
        
        # 等级计算逻辑（更平衡）
        # 新手 → 探索者：至少1个旅行 OR 5条评论
        # 探索者 → 漫游者：至少5个旅行 OR (3个旅行+20条评论)
        # 漫游者 → 冒险家：至少10个旅行 OR (5个旅行+50条评论)
        # 冒险家 → 旅行大师：至少20个旅行 OR (10个旅行+100条评论)
        
        if trips_count >= 20:
            self.level = 'master'
        elif trips_count >= 10 or (trips_count >= 5 and comments_count >= 50):
            self.level = 'adventurer'
        elif trips_count >= 5 or (trips_count >= 3 and comments_count >= 20):
            self.level = 'wanderer'
        elif trips_count >= 1 or comments_count >= 5:
            self.level = 'explorer'
        else:
            self.level = 'novice'
    
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
                
                # 调整大小为300x300像素（从200提升到300）
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                
                # 转换为RGB格式并保存，质量提升到90
                img = img.convert('RGB')
                img.save(img_path, format='JPEG', quality=90)
                
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

