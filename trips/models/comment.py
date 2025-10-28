"""
评论模型
"""
import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    """评论模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # 谁发的评论
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')  # 父评论（用于回复）
    content = models.TextField()
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)  # 图片字段
    video = models.FileField(upload_to='comment_videos/', blank=True, null=True)  # 视频字段
    timestamp = models.DateTimeField(auto_now_add=True)
    page = models.CharField(max_length=16, default='trip')  # 区分不同页面
    is_pinned = models.BooleanField(default=False)  # 是否置顶

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # 先保存以获得路径

        # 图片压缩
        if self.image:
            try:
                img_path = self.image.path
                img = Image.open(img_path)

                max_width = 1920  # 从1080提升到1920（2K分辨率）
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

                # 首次压缩为 JPEG 格式，质量提升到 85
                img = img.convert('RGB')  # 避免 PNG 无法保存为 JPEG 报错
                img.save(img_path, format='JPEG', quality=85)

                # 如果压缩后仍 > 3MB，执行二次压缩（阈值从1MB提高到3MB，质量从50提升到70）
                if os.path.getsize(img_path) > 3 * 1024 * 1024:
                    img.save(img_path, format='JPEG', quality=70)

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

    class Meta:
        ordering = ['-is_pinned', '-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"
    
    @property
    def is_top_level(self):
        """判断是否为顶层评论"""
        return self.parent is None
    
    @property
    def author_page(self):
        """获取评论所属的页面（旅行）"""
        return self.page

