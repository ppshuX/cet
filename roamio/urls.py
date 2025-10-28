"""
URL configuration for Roamio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include, re_path
from trips import views
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # ==================== RESTful API路由 ⭐（必须在最前面） ====================
    path('api/v1/', include('trips.api.urls')),
    
    # API文档
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='api-schema'), name='api-redoc'),
    
    # Django Admin
    path('admin/', admin.site.urls),
    
    # ==================== 旅行相关路由（保留向后兼容） ====================
    path('trips/', include('trips.urls')),
    path('accounts/login/', views.custom_login, name='login'),
    path('accounts/logout/', views.custom_logout, name='logout'),
    
    # ==================== Vue单页应用 ⭐（必须在最后） ====================
    path('', views.vue_app, name='home'),  # 首页
    # Catch-all：匹配非管理路径和非静态资源路径
    re_path(r'^(?!admin|api|static|media|trips|accounts).*$', views.vue_app),
]

# 静态文件和媒体文件
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
