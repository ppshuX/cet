"""
用户相关 ViewSet
处理用户信息的查询、更新、头像上传等功能
"""
import uuid
import os
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.contrib.auth.models import User

from ...models import Comment
from ...serializers import (
    UserSerializer,
    UserProfileSerializer,
    UpdateUserSerializer,
    UserProfileUpdateSerializer,
    AvatarUploadSerializer,
)


class UserViewSet(viewsets.ReadOnlyModelViewSet,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    """用户ViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def destroy(self, request, *args, **kwargs):
        """删除用户账号（只能删除自己的）"""
        user = self.get_object()
        
        # 权限检查：只能删除自己的账号
        if user != request.user:
            return Response(
                {'detail': '无权删除他人账号'},
                status=403  # HTTP_403_FORBIDDEN
            )
        
        # 调用父类的删除方法
        return super().destroy(request, *args, **kwargs)
    
    def get_serializer_class(self):
        """根据action选择序列化器"""
        if self.action in ['update', 'partial_update']:
            return UpdateUserSerializer
        return UserSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """获取用户详情时自动计算等级"""
        response = super().retrieve(request, *args, **kwargs)
        user = self.get_object()
        # 自动计算并更新等级
        if hasattr(user, 'profile') and user.profile:
            user.profile.calculate_level()
            user.profile.save()
        return response
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def upload_avatar(self, request, pk=None):
        """上传头像"""
        user = self.get_object()
        
        # 权限检查：只能修改自己的头像
        if user != request.user and not request.user.is_superuser:
            return Response(
                {'detail': '无权修改他人头像'},
                status=403  # HTTP_403_FORBIDDEN
            )
        
        serializer = AvatarUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        avatar_file = serializer.validated_data['avatar']
        
        # 生成唯一文件名
        ext = os.path.splitext(avatar_file.name)[-1]
        avatar_file.name = f"{uuid.uuid4().hex}{ext}"
        
        # 保存头像
        profile = user.profile
        
        # 删除旧头像
        if profile.avatar:
            try:
                os.remove(profile.avatar.path)
            except:
                pass
        
        profile.avatar = avatar_file
        profile.save()
        
        return Response({
            'avatar_url': profile.get_avatar_url(),
            'detail': '头像上传成功'
        })
    
    @action(detail=False, methods=['patch', 'put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """更新个人资料（包括 bio, tags, visited_countries）"""
        profile = request.user.profile
        serializer = UserProfileUpdateSerializer(
            profile, 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # 自动计算等级
        profile.calculate_level()
        profile.save()
        
        return Response({
            'detail': '个人资料更新成功',
            'profile': UserProfileSerializer(profile).data
        })
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """获取用户统计信息"""
        user = self.get_object()
        comments_count = Comment.objects.filter(user=user).count()
        
        return Response({
            'comments_count': comments_count,
        })
