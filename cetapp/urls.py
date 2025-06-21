from django.urls import path
from . import views

urlpatterns = [
    path('trip/', views.trip_page, name='trip_page'),
    path('trip/add_comment/', views.add_comment, name='add_comment'),
    path('trip/like/', views.like_view, name='like_view'),
    path('trip/checkin/', views.checkin_view, name='checkin_view'),
    path('trip/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
     path('register/', views.register, name='register'),
]

