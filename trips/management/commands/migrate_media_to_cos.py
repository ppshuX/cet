"""
将本地 media 文件迁移到腾讯云 COS
用于一次性迁移所有旧的本地媒体文件到 COS
"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from trips.models import Comment
from trips.utils.tencent_cos import upload_to_cos


class Command(BaseCommand):
    help = '将本地 media 文件迁移到腾讯云 COS 并更新数据库'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='试运行，不实际上传和修改数据库',
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['avatar', 'comment_image', 'comment_video', 'all'],
            default='all',
            help='迁移类型：avatar（头像）、comment_image（评论图片）、comment_video（评论视频）、all（全部）',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        migration_type = options['type']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('=== 试运行模式（不会实际修改数据）==='))
        else:
            self.stdout.write(self.style.WARNING('=== 正式迁移模式 ==='))
        
        self.stdout.write('')
        
        # 统计
        stats = {
            'avatar_total': 0,
            'avatar_success': 0,
            'avatar_skip': 0,
            'avatar_fail': 0,
            'comment_image_total': 0,
            'comment_image_success': 0,
            'comment_image_skip': 0,
            'comment_image_fail': 0,
            'comment_video_total': 0,
            'comment_video_success': 0,
            'comment_video_skip': 0,
            'comment_video_fail': 0,
        }
        
        # 迁移头像
        if migration_type in ['avatar', 'all']:
            self.migrate_avatars(dry_run, stats)
        
        # 迁移评论图片
        if migration_type in ['comment_image', 'all']:
            self.migrate_comment_images(dry_run, stats)
        
        # 迁移评论视频
        if migration_type in ['comment_video', 'all']:
            self.migrate_comment_videos(dry_run, stats)
        
        # 输出统计
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== 迁移完成 ==='))
        self.stdout.write(f"头像：{stats['avatar_success']}/{stats['avatar_total']} 成功，{stats['avatar_skip']} 跳过，{stats['avatar_fail']} 失败")
        self.stdout.write(f"评论图片：{stats['comment_image_success']}/{stats['comment_image_total']} 成功，{stats['comment_image_skip']} 跳过，{stats['comment_image_fail']} 失败")
        self.stdout.write(f"评论视频：{stats['comment_video_success']}/{stats['comment_video_total']} 成功，{stats['comment_video_skip']} 跳过，{stats['comment_video_fail']} 失败")

    def migrate_avatars(self, dry_run, stats):
        """迁移用户头像"""
        self.stdout.write(self.style.HTTP_INFO('\n>>> 开始迁移用户头像'))
        
        # 查找所有有头像的用户
        users = User.objects.filter(profile__avatar__isnull=False).exclude(profile__avatar='')
        stats['avatar_total'] = users.count()
        
        for user in users:
            avatar = user.profile.avatar
            
            # 跳过已经是 COS URL 的
            if avatar.startswith('http://') or avatar.startswith('https://'):
                self.stdout.write(f"  跳过（已是 COS URL）: User {user.id} - {user.username}")
                stats['avatar_skip'] += 1
                continue
            
            # 构建本地文件路径
            local_path = os.path.join(settings.MEDIA_ROOT, avatar)
            
            if not os.path.exists(local_path):
                self.stdout.write(self.style.WARNING(f"  ⚠️  本地文件不存在: {local_path}"))
                stats['avatar_fail'] += 1
                continue
            
            # 构建 COS 路径
            filename = os.path.basename(avatar)
            cos_path = f"media/avatars/migrated_{filename}"
            
            self.stdout.write(f"  迁移: User {user.id} - {user.username}")
            self.stdout.write(f"    本地: {local_path}")
            self.stdout.write(f"    COS: {cos_path}")
            
            if not dry_run:
                try:
                    # 上传到 COS
                    cos_url = upload_to_cos(local_path, cos_path)
                    
                    # 更新数据库
                    user.profile.avatar = cos_url
                    user.profile.save()
                    
                    self.stdout.write(self.style.SUCCESS(f"    ✅ 成功: {cos_url}"))
                    stats['avatar_success'] += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"    ❌ 失败: {e}"))
                    stats['avatar_fail'] += 1
            else:
                stats['avatar_success'] += 1

    def migrate_comment_images(self, dry_run, stats):
        """迁移评论图片"""
        self.stdout.write(self.style.HTTP_INFO('\n>>> 开始迁移评论图片'))
        
        # 查找所有有图片的评论
        comments = Comment.objects.filter(image__isnull=False).exclude(image='')
        stats['comment_image_total'] = comments.count()
        
        for comment in comments:
            image = comment.image
            
            # 跳过已经是 COS URL 的
            if image.startswith('http://') or image.startswith('https://'):
                self.stdout.write(f"  跳过（已是 COS URL）: Comment {comment.id}")
                stats['comment_image_skip'] += 1
                continue
            
            # 构建本地文件路径
            local_path = os.path.join(settings.MEDIA_ROOT, image)
            
            if not os.path.exists(local_path):
                self.stdout.write(self.style.WARNING(f"  ⚠️  本地文件不存在: {local_path}"))
                stats['comment_image_fail'] += 1
                continue
            
            # 构建 COS 路径
            filename = os.path.basename(image)
            cos_path = f"media/comments/images/migrated_{filename}"
            
            self.stdout.write(f"  迁移: Comment {comment.id} by {comment.user.username}")
            self.stdout.write(f"    本地: {local_path}")
            self.stdout.write(f"    COS: {cos_path}")
            
            if not dry_run:
                try:
                    # 上传到 COS
                    cos_url = upload_to_cos(local_path, cos_path)
                    
                    # 更新数据库
                    comment.image = cos_url
                    comment.save()
                    
                    self.stdout.write(self.style.SUCCESS(f"    ✅ 成功: {cos_url}"))
                    stats['comment_image_success'] += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"    ❌ 失败: {e}"))
                    stats['comment_image_fail'] += 1
            else:
                stats['comment_image_success'] += 1

    def migrate_comment_videos(self, dry_run, stats):
        """迁移评论视频"""
        self.stdout.write(self.style.HTTP_INFO('\n>>> 开始迁移评论视频'))
        
        # 查找所有有视频的评论
        comments = Comment.objects.filter(video__isnull=False).exclude(video='')
        stats['comment_video_total'] = comments.count()
        
        for comment in comments:
            video = comment.video
            
            # 跳过已经是 COS URL 的
            if video.startswith('http://') or video.startswith('https://'):
                self.stdout.write(f"  跳过（已是 COS URL）: Comment {comment.id}")
                stats['comment_video_skip'] += 1
                continue
            
            # 构建本地文件路径
            local_path = os.path.join(settings.MEDIA_ROOT, video)
            
            if not os.path.exists(local_path):
                self.stdout.write(self.style.WARNING(f"  ⚠️  本地文件不存在: {local_path}"))
                stats['comment_video_fail'] += 1
                continue
            
            # 构建 COS 路径
            filename = os.path.basename(video)
            cos_path = f"media/comments/videos/migrated_{filename}"
            
            self.stdout.write(f"  迁移: Comment {comment.id} by {comment.user.username}")
            self.stdout.write(f"    本地: {local_path}")
            self.stdout.write(f"    COS: {cos_path}")
            
            if not dry_run:
                try:
                    # 上传到 COS
                    cos_url = upload_to_cos(local_path, cos_path)
                    
                    # 更新数据库
                    comment.video = cos_url
                    comment.save()
                    
                    self.stdout.write(self.style.SUCCESS(f"    ✅ 成功: {cos_url}"))
                    stats['comment_video_success'] += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"    ❌ 失败: {e}"))
                    stats['comment_video_fail'] += 1
            else:
                stats['comment_video_success'] += 1

