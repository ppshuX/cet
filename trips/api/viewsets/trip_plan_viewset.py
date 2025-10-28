"""
旅行计划相关 ViewSet
处理旅行计划的 CRUD、克隆、添加到旅行树等功能
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models

from ...models import Trip, SiteStat
from ...serializers import (
    TripCreateSerializer,
    TripDetailSerializer,
    TripListSerializer,
    TripUpdateSerializer,
    SiteStatSerializer,
)


class TripPlanViewSet(viewsets.ModelViewSet):
    """旅行计划ViewSet（用于编辑器）"""
    queryset = Trip.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """根据action选择序列化器"""
        if self.action == 'create':
            return TripCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TripUpdateSerializer
        elif self.action == 'list':
            return TripListSerializer
        return TripDetailSerializer
    
    def get_permissions(self):
        """根据action设置权限"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]
    
    def get_queryset(self):
        """过滤查询集"""
        queryset = Trip.objects.all()
        
        # 如果是my_trips action，只返回当前用户的
        if self.action == 'my_trips':
            if self.request.user.is_authenticated:
                return queryset.filter(author=self.request.user)
            return queryset.none()
        
        # 普通列表：只返回公开的或自己的
        if self.action == 'list':
            if self.request.user.is_authenticated:
                return queryset.filter(
                    models.Q(visibility='public') | models.Q(author=self.request.user)
                )
            return queryset.filter(visibility='public')
        
        return queryset
    
    def perform_create(self, serializer):
        """创建时自动设置作者"""
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        """更新时检查权限"""
        trip = self.get_object()
        if trip.author != self.request.user and not self.request.user.is_superuser:
            raise PermissionError("无权修改他人的旅行计划")
        serializer.save()
    
    def perform_destroy(self, instance):
        """删除时检查权限"""
        if instance.author != self.request.user and not self.request.user.is_superuser:
            raise PermissionError("无权删除他人的旅行计划")
        instance.delete()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_trips(self, request):
        """获取我的旅行列表"""
        queryset = self.get_queryset()
        
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TripListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = TripListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def clone(self, request, slug=None):
        """复制旅行计划"""
        source_trip = self.get_object()
        
        # 创建副本
        new_trip = Trip.objects.create(
            author=request.user,
            title=f"{source_trip.title} (副本)",
            description=source_trip.description,
            icon=source_trip.icon,
            start_date=source_trip.start_date,
            end_date=source_trip.end_date,
            status='draft',
            visibility='private',
            config=source_trip.config.copy() if source_trip.config else {},
            overview=source_trip.overview.copy() if source_trip.overview else {},
            theme_color=source_trip.theme_color,
            background_music=source_trip.background_music,
        )
        
        serializer = TripDetailSerializer(new_trip)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_tree(self, request, slug=None):
        """将旅行计划添加到旅行树（创建SiteStat）"""
        # 检查是否为管理员
        if not request.user.is_superuser:
            return Response({
                'detail': '当前未开放此功能'
            }, status=status.HTTP_403_FORBIDDEN)
        
        trip = self.get_object()
        
        # 检查权限
        if trip.author != request.user and not request.user.is_superuser:
            raise PermissionError("无权将此旅行添加到旅行树")
        
        # 检查是否已存在
        try:
            SiteStat.objects.get(page=trip.slug)
            return Response({
                'detail': '该旅行已存在于旅行树中',
                'slug': trip.slug
            }, status=status.HTTP_200_OK)
        except SiteStat.DoesNotExist:
            # 创建新的SiteStat
            site_stat = SiteStat.objects.create(
                page=trip.slug,
                views=0,
                likes=0,
                checked_in=False
            )
            
            serializer = SiteStatSerializer(site_stat)
            return Response({
                'detail': '旅行已成功添加到旅行树',
                'stat': serializer.data,
                'slug': trip.slug
            }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_from_tree(self, request, slug=None):
        """从旅行树移除旅行计划（删除SiteStat）"""
        # 检查是否为管理员
        if not request.user.is_superuser:
            return Response({
                'detail': '当前未开放此功能'
            }, status=status.HTTP_403_FORBIDDEN)
        
        trip = self.get_object()
        
        # 检查权限
        if trip.author != request.user and not request.user.is_superuser:
            raise PermissionError("无权从旅行树移除此旅行")
        
        # 删除SiteStat
        try:
            site_stat = SiteStat.objects.get(page=trip.slug)
            site_stat.delete()
            return Response({
                'detail': '旅行已成功从旅行树移除',
                'slug': trip.slug
            }, status=status.HTTP_200_OK)
        except SiteStat.DoesNotExist:
            return Response({
                'detail': '该旅行不存在于旅行树中',
                'slug': trip.slug
            }, status=status.HTTP_404_NOT_FOUND)
