"""
URL路由模块
统一管理所有URL配置
"""
from django.urls import path, include
from ..views import main_menu

# 主URL配置
urlpatterns = [
    path('', main_menu, name='trips_main_menu'),
]

# 引入各子模块的URL
urlpatterns += [
    path('', include('trips.urls.auth_urls')),     # 认证相关
    path('', include('trips.urls.trip_urls')),     # 旅行页面
    path('', include('trips.urls.user_urls')),     # 用户中心
    path('', include('trips.urls.api_urls')),      # API接口
]

