"""
URL路由模块
统一管理所有URL配置
"""
from django.urls import path, include
from ..views import main_menu

# 主URL配置
urlpatterns = [
    path('', main_menu, name='cetapp_main_menu'),
]

# 引入各子模块的URL
urlpatterns += [
    path('', include('cetapp.urls.auth_urls')),     # 认证相关
    path('', include('cetapp.urls.trip_urls')),     # 旅行页面
    path('', include('cetapp.urls.user_urls')),     # 用户中心
    path('', include('cetapp.urls.api_urls')),      # API接口
]

