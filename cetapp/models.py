import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# 用户配置文件模型
class UserProfile(models.Model):
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

#评论模型
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 谁发的评论
    content = models.TextField()
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)  # 新增的图片字段
    video = models.FileField(upload_to='comment_videos/', blank=True, null=True)  # 新增的视频字段
    timestamp = models.DateTimeField(auto_now_add=True)
    page = models.CharField(max_length=16, default='trip')  # 新增字段，区分trip和trip1

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # 先保存以获得路径

        # 图片压缩
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

        # 视频压缩
        if self.video:
            try:
                video_path = self.video.path
                original_size = os.path.getsize(video_path)
                
                # 只有当文件大小超过5MB时才压缩
                if original_size > 5 * 1024 * 1024:
                    print(f"开始压缩视频，原始大小: {original_size / (1024*1024):.2f}MB")
                    
                    # 动态导入moviepy以避免启动时的导入错误
                    try:
                        from moviepy.editor import VideoFileClip
                        
                        # 读取视频
                        clip = VideoFileClip(video_path)
                        
                        # 设置压缩参数
                        max_width = 720  # 最大宽度720p
                        max_height = 720  # 最大高度720p
                        
                        # 如果原视频分辨率过高，则缩放
                        if clip.w > max_width or clip.h > max_height:
                            # 按比例缩放
                            scale_factor = min(max_width / clip.w, max_height / clip.h)
                            new_w = int(clip.w * scale_factor)
                            new_h = int(clip.h * scale_factor)
                            clip = clip.resize((new_w, new_h))
                        
                        # 创建临时压缩文件
                        temp_path = video_path.replace('.mp4', '_compressed.mp4')
                        
                        # 压缩视频 - 使用较低比特率以达到压缩效果
                        clip.write_videofile(
                            temp_path,
                            bitrate="500k",  # 500kbps，大幅降低文件大小
                            audio_bitrate="64k",  # 降低音频比特率
                            preset='fast'  # 使用快速编码预设
                        )
                        
                        # 关闭剪辑对象释放资源
                        clip.close()
                        
                        # 如果压缩成功且文件变小，则替换原文件
                        compressed_size = os.path.getsize(temp_path)
                        if compressed_size < original_size:
                            # 删除原文件并重命名压缩文件
                            os.remove(video_path)
                            os.rename(temp_path, video_path)
                            print(f"视频压缩完成，压缩后大小: {compressed_size / (1024*1024):.2f}MB")
                        else:
                            # 压缩文件更大，删除压缩文件保留原文件
                            os.remove(temp_path)
                            print(f"压缩后文件更大，保留原文件")
                            
                    except ImportError:
                        print("MoviePy未安装，跳过视频压缩")
                        return
                        
            except Exception as e:
                print(f"视频压缩失败: {e}")

#网站统计模型
class SiteStat(models.Model):
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    checked_in = models.BooleanField(default=False)
    page = models.CharField(max_length=16, default='trip')  # 新增字段，区分trip和trip1

    def __str__(self):
        return f"{self.page} 页面统计"


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
