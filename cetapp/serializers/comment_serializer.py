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
    
    class Meta:
        model = Comment
        fields = [
            'id', 'user', 'content', 'image', 'video', 
            'page', 'timestamp', 'can_delete'
        ]
        read_only_fields = ['id', 'user', 'timestamp']
    
    def get_can_delete(self, obj):
        """判断当前用户是否可以删除此评论"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.user == request.user or request.user.is_superuser


class CommentCreateSerializer(serializers.ModelSerializer):
    """评论创建序列化器"""
    
    class Meta:
        model = Comment
        fields = ['content', 'image', 'video', 'page']
    
    def validate(self, attrs):
        """验证至少有一项内容"""
        if not any([attrs.get('content'), attrs.get('image'), attrs.get('video')]):
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


class CommentListSerializer(serializers.ModelSerializer):
    """评论列表序列化器（精简版）"""
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'image', 'video', 'timestamp']
    
    def get_user(self, obj):
        """只返回用户的基本信息"""
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'avatar': obj.user.profile.get_avatar_url()
        }

