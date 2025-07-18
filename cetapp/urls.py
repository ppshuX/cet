from django.urls import path
from . import views
from .utils import add_trip_page_urls

urlpatterns = [
    path('', views.main_menu, name='cetapp_main_menu'),
    path('trip/', views.trip_page, name='trip_page'),
    path('trip/add_comment/', views.add_comment, name='add_comment'),
    path('trip/like/', views.like_view, name='like_view'),
    path('trip/checkin/', views.checkin_view, name='checkin_view'),
    path('trip/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('trip/views_likes/', views.trip_views_likes, name='trip_views_likes'),
    path('trip1/', views.trip1, name='trip1'),
    path('trip1/views_likes/', views.trip1_views_likes, name='trip1_views_likes'),
    path('trip1/like/', views.trip1_like_view, name='trip1_like_view'),
    path('trip1/add_comment/', views.trip1_add_comment, name='trip1_add_comment'),
    path('trip1/delete_comment/<int:comment_id>/', views.trip1_delete_comment, name='trip1_delete_comment'),
    path('register/', views.register, name='register'),
    path('trip2/like/', views.trip2_like_view, name='trip2_like_view'),
    path('trip3/like/', views.trip3_like_view, name='trip3_like_view'),
]

# 动态添加 trip2 路由
urlpatterns.extend(add_trip_page_urls('trip2'))
# 动态添加 trip3 路由
urlpatterns.extend(add_trip_page_urls('trip3'))

