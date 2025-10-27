"""
API ViewSets
基于DRF的视图集，实现RESTful API
"""
import uuid
import os
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers as drf_serializers
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import CharFilter
from rest_framework.filters import SearchFilter, OrderingFilter

from ..models import Comment, SiteStat
from ..serializers import (
    UserSerializer,
    RegisterSerializer,
    UpdateUserSerializer,
    AvatarUploadSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    TripSerializer,
    SiteStatSerializer,
    LoginSerializer,
)


class AuthViewSet(viewsets.GenericViewSet):
    """认证相关ViewSet"""
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """用户注册"""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # 生成JWT Token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """用户登录"""
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """用户登出"""
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'detail': '登出成功'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': '登出失败'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """获取当前用户信息"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet,
                  mixins.UpdateModelMixin):
    """用户ViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['date_joined', 'username']
    ordering = ['-date_joined']
    
    def get_serializer_class(self):
        """根据action选择序列化器"""
        if self.action in ['update', 'partial_update']:
            return UpdateUserSerializer
        return UserSerializer
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def upload_avatar(self, request, pk=None):
        """上传头像"""
        user = self.get_object()
        
        # 权限检查：只能修改自己的头像
        if user != request.user and not request.user.is_superuser:
            return Response(
                {'detail': '无权修改他人头像'},
                status=status.HTTP_403_FORBIDDEN
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
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """获取用户统计信息"""
        user = self.get_object()
        comments_count = Comment.objects.filter(user=user).count()
        
        return Response({
            'comments_count': comments_count,
        })


class CommentFilter(FilterSet):
    """评论过滤器 - 使用 'trip' 参数代替 'page' 以避免与分页冲突"""
    trip = CharFilter(field_name='page', lookup_expr='exact')
    
    class Meta:
        model = Comment
        fields = {
            'user': ['exact'],
        }


class CommentViewSet(viewsets.ModelViewSet):
    """评论ViewSet"""
    queryset = Comment.objects.all().order_by('-timestamp')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # 使用自定义过滤器类，将 'trip' 参数映射到模型的 'page' 字段
    filterset_class = CommentFilter
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def get_serializer_class(self):
        """根据action选择序列化器"""
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer
    
    def get_permissions(self):
        """根据action设置权限"""
        if self.action == 'create':
            # 只有管理员可以创建评论
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]
    
    def perform_create(self, serializer):
        """创建评论时自动设置用户"""
        # 权限检查：只有管理员可以发表评论
        if not self.request.user.is_superuser:
            raise drf_serializers.ValidationError({
                'detail': '仅管理员可发表评论'
            })
        
        # 处理文件重命名
        image = self.request.FILES.get('image')
        video = self.request.FILES.get('video')
        
        if image:
            ext = os.path.splitext(image.name)[-1]
            image.name = f"{uuid.uuid4().hex}{ext}"
        
        if video:
            ext = os.path.splitext(video.name)[-1]
            video.name = f"{uuid.uuid4().hex}{ext}"
        
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """删除评论"""
        comment = self.get_object()
        
        # 权限检查：只有评论作者或管理员可以删除
        if comment.user != request.user and not request.user.is_superuser:
            return Response(
                {'detail': '无权删除此评论'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TripViewSet(viewsets.ReadOnlyModelViewSet):
    """旅行页面ViewSet"""
    queryset = SiteStat.objects.all()
    serializer_class = TripSerializer
    lookup_field = 'page'
    permission_classes = [AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        """获取旅行详情，并增加浏览量"""
        instance = self.get_object()
        instance.views += 1
        instance.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def like(self, request, page=None):
        """点赞"""
        stat = self.get_object()
        stat.likes += 1
        stat.save()
        return Response({'likes': stat.likes})
    
    @action(detail=True, methods=['post'])
    def checkin(self, request, page=None):
        """打卡"""
        stat = self.get_object()
        stat.checked_in = True
        stat.save()
        return Response({'checked_in': True})
    
    @action(detail=True, methods=['get'])
    def stats(self, request, page=None):
        """获取统计信息"""
        stat = self.get_object()
        serializer = SiteStatSerializer(stat)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, page=None):
        """获取该页面的评论列表"""
        stat = self.get_object()
        comments = Comment.objects.filter(page=stat.page).order_by('-timestamp')
        
        # 分页
        page_obj = self.paginate_queryset(comments)
        if page_obj is not None:
            serializer = CommentSerializer(page_obj, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

