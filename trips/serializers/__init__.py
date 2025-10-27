"""
序列化器模块
将Django模型转换为JSON格式，用于API响应
"""
from .user_serializer import (
    UserSerializer, 
    UserProfileSerializer, 
    RegisterSerializer,
    UpdateUserSerializer,
    AvatarUploadSerializer,
)
from .comment_serializer import CommentSerializer, CommentCreateSerializer
from .trip_serializer import TripSerializer, SiteStatSerializer
from .auth_serializer import LoginSerializer, TokenObtainSerializer

__all__ = [
    # 用户
    'UserSerializer',
    'UserProfileSerializer',
    'RegisterSerializer',
    'UpdateUserSerializer',
    'AvatarUploadSerializer',
    # 评论
    'CommentSerializer',
    'CommentCreateSerializer',
    # 旅行
    'TripSerializer',
    'SiteStatSerializer',
    # 认证
    'LoginSerializer',
    'TokenObtainSerializer',
]

