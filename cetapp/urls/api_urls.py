"""
API相关URL路由
"""
from django.urls import path
from ..views import get_quote

urlpatterns = [
    path('get_quote/', get_quote, name='get_quote'),
]

