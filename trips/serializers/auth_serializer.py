"""
认证相关序列化器
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    username = serializers.CharField(
        required=True,
        error_messages={'required': '请输入用户名'}
    )
    password = serializers.CharField(
        required=True, 
        write_only=True,
        style={'input_type': 'password'},
        error_messages={'required': '请输入密码'}
    )
    
    def validate_username(self, value):
        """验证用户名"""
        if not value or not value.strip():
            raise serializers.ValidationError('用户名不能为空')
        return value.strip()
    
    def validate_password(self, value):
        """验证密码"""
        if not value:
            raise serializers.ValidationError('密码不能为空')
        return value
    
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
                raise serializers.ValidationError({
                    'non_field_errors': ['用户名或密码错误']
                })
            
            if not user.is_active:
                raise serializers.ValidationError({
                    'non_field_errors': ['此账号已被停用，请联系管理员']
                })
        else:
            raise serializers.ValidationError({
                'non_field_errors': ['用户名和密码不能为空']
            })
        
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

