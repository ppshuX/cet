"""
认证相关序列化器
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, 
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """验证用户名和密码"""
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    '用户名或密码错误',
                    code='authorization'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    '此账号已被停用',
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                '必须提供用户名和密码',
                code='authorization'
            )
        
        attrs['user'] = user
        return attrs


class TokenObtainSerializer(serializers.Serializer):
    """Token获取序列化器"""
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        """返回用户信息"""
        from .user_serializer import UserSerializer
        user = self.context.get('user')
        if user:
            return UserSerializer(user).data
        return None

