"""
评论相关序列化器
"""
from rest_framework import serializers
from ..models import Comment
from .user_serializer import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    """评论序列化器（列表/详情）"""
    user = UserSerializer(read_only=True)
    can_delete = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    is_top_level = serializers.SerializerMethodField()
    parent_id = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'user', 'parent_id', 'content', 'image', 'video', 
            'page', 'timestamp', 'can_delete', 'is_top_level', 'replies_count'
        ]
        read_only_fields = ['id', 'user', 'timestamp']
    
    def get_image(self, obj):
        """返回完整URL（包含域名）或相对路径"""
        if not obj.image:
            return None
        
        # 获取原始 URL
        image_url = obj.image.url
        
        # 处理 URL 中可能存在的 /media/media/ 重复问题
        image_url = image_url.replace('/media/media/', '/media/')
        
        # 获取 request 对象
        request = self.context.get('request')
        
        if request:
            # 检查 URL 是否已经包含域名
            if image_url.startswith('http://') or image_url.startswith('https://'):
                return image_url
            
            # 如果有 request，手动构建完整 URL
            # 确保以 /media/ 开头
            if image_url.startswith('/media/'):
                full_url = f"{request.scheme}://{request.get_host()}{image_url}"
            else:
                # 如果路径不是以 /media/ 开头，添加它
                if not image_url.startswith('/'):
                    image_url = f"/media/{image_url}"
                full_url = f"{request.scheme}://{request.get_host()}{image_url}"
            
            return full_url
        else:
            # 没有 request 对象，返回相对路径
            return image_url
    
    def get_video(self, obj):
        """返回完整URL（包含域名）或相对路径"""
        if not obj.video:
            return None
        
        # 获取原始 URL
        video_url = obj.video.url
        
        # 处理 URL 中可能存在的 /media/media/ 重复问题
        video_url = video_url.replace('/media/media/', '/media/')
        
        # 获取 request 对象
        request = self.context.get('request')
        
        if request:
            # 检查 URL 是否已经包含域名
            if video_url.startswith('http://') or video_url.startswith('https://'):
                return video_url
            
            # 如果有 request，手动构建完整 URL
            # 确保以 /media/ 开头
            if video_url.startswith('/media/'):
                full_url = f"{request.scheme}://{request.get_host()}{video_url}"
            else:
                # 如果路径不是以 /media/ 开头，添加它
                if not video_url.startswith('/'):
                    video_url = f"/media/{video_url}"
                full_url = f"{request.scheme}://{request.get_host()}{video_url}"
            
            return full_url
        else:
            # 没有 request 对象，返回相对路径
            return video_url
    
    def get_can_delete(self, obj):
        """判断当前用户是否可以删除此评论"""
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            return False
        if not request.user.is_authenticated:
            return False
        
        # 如果是回复（有父评论）
        if obj.parent:
            # 回复只能由回复作者或旅行作者删除
            from ..models import Trip
            try:
                trip = Trip.objects.filter(slug=obj.page).first()
                # 权限：回复作者、旅行作者或管理员
                return (
                    obj.user == request.user or  # 回复作者
                    (trip and trip.user == request.user) or  # 旅行作者
                    request.user.is_superuser  # 管理员
                )
            except Exception:
                # 如果获取Trip失败，回退到原始逻辑
                return obj.user == request.user or request.user.is_superuser
        else:
            # 顶层评论只能由评论作者或管理员删除
            return obj.user == request.user or request.user.is_superuser
    
    def get_is_top_level(self, obj):
        """判断是否为顶层评论"""
        try:
            # 直接检查parent字段
            return obj.parent is None or obj.parent_id is None
        except (AttributeError, Exception):
            return obj.parent is None
    
    def get_parent_id(self, obj):
        """获取父评论ID"""
        return obj.parent_id if obj.parent else None
    
    def get_replies_count(self, obj):
        """获取回复数量（仅对顶层评论有效）"""
        if obj.parent:
            return 0  # 回复本身没有回复数
        return Comment.objects.filter(parent=obj).count()


class CommentCreateSerializer(serializers.ModelSerializer):
    """评论创建序列化器"""
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True)
    content = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = Comment
        fields = ['content', 'image', 'video', 'page', 'parent']
    
    def validate(self, attrs):
        """验证至少有一项内容"""
        content = attrs.get('content', '').strip() if attrs.get('content') else ''
        image = attrs.get('image')
        video = attrs.get('video')
        
        if not content and not image and not video:
            raise serializers.ValidationError(
                "评论内容、图片或视频至少需要提供一项"
            )
        return attrs
    
    def validate_image(self, value):
        """验证图片"""
        if value and value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("图片大小不能超过10MB")
        return value
    
    def validate_video(self, value):
        """验证视频"""
        if value and value.size > 100 * 1024 * 1024:
            raise serializers.ValidationError("视频大小不能超过100MB")
        return value


class CommentUpdateSerializer(serializers.ModelSerializer):
    """评论更新序列化器"""
    
    class Meta:
        model = Comment
        fields = ['content']
    
    def validate_content(self, value):
        """验证内容不为空"""
        if not value or not value.strip():
            raise serializers.ValidationError("评论内容不能为空")
        return value.strip()


class CommentListSerializer(serializers.ModelSerializer):
    """评论列表序列化器（精简版）"""
    user = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'image', 'video', 'timestamp']
    
    def get_image(self, obj):
        """返回完整URL（包含域名）或相对路径"""
        if not obj.image:
            return None
        
        # 获取原始 URL
        image_url = obj.image.url
        
        # 处理 URL 中可能存在的 /media/media/ 重复问题
        image_url = image_url.replace('/media/media/', '/media/')
        
        # 获取 request 对象
        request = self.context.get('request')
        
        if request:
            # 检查 URL 是否已经包含域名
            if image_url.startswith('http://') or image_url.startswith('https://'):
                return image_url
            
            # 如果有 request，手动构建完整 URL
            # 确保以 /media/ 开头
            if image_url.startswith('/media/'):
                full_url = f"{request.scheme}://{request.get_host()}{image_url}"
            else:
                # 如果路径不是以 /media/ 开头，添加它
                if not image_url.startswith('/'):
                    image_url = f"/media/{image_url}"
                full_url = f"{request.scheme}://{request.get_host()}{image_url}"
            
            return full_url
        else:
            # 没有 request 对象，返回相对路径
            return image_url
    
    def get_video(self, obj):
        """返回完整URL（包含域名）或相对路径"""
        if not obj.video:
            return None
        
        # 获取原始 URL
        video_url = obj.video.url
        
        # 处理 URL 中可能存在的 /media/media/ 重复问题
        video_url = video_url.replace('/media/media/', '/media/')
        
        # 获取 request 对象
        request = self.context.get('request')
        
        if request:
            # 检查 URL 是否已经包含域名
            if video_url.startswith('http://') or video_url.startswith('https://'):
                return video_url
            
            # 如果有 request，手动构建完整 URL
            # 确保以 /media/ 开头
            if video_url.startswith('/media/'):
                full_url = f"{request.scheme}://{request.get_host()}{video_url}"
            else:
                # 如果路径不是以 /media/ 开头，添加它
                if not video_url.startswith('/'):
                    video_url = f"/media/{video_url}"
                full_url = f"{request.scheme}://{request.get_host()}{video_url}"
            
            return full_url
        else:
            # 没有 request 对象，返回相对路径
            return video_url
    
    def get_user(self, obj):
        """只返回用户的基本信息"""
        try:
            avatar = obj.user.profile.get_avatar_url()
        except Exception:
            avatar = None
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'avatar': avatar
        }

