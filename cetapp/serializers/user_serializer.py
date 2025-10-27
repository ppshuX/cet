"""
用户相关序列化器
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from ..models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """用户配置序列化器"""
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['avatar', 'avatar_url']
    
    def get_avatar_url(self, obj):
        """获取头像URL"""
        return obj.get_avatar_url()


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'profile']
        read_only_fields = ['id', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'},
        label="确认密码"
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': False}
        }
    
    def validate(self, attrs):
        """验证两次密码是否一致"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "两次输入的密码不一致"
            })
        return attrs
    
    def create(self, validated_data):
        """创建用户"""
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    """更新用户信息序列化器"""
    
    class Meta:
        model = User
        fields = ['username', 'email']
    
    def validate_username(self, value):
        """验证用户名唯一性"""
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("该用户名已被使用")
        return value


class AvatarUploadSerializer(serializers.Serializer):
    """头像上传序列化器"""
    avatar = serializers.ImageField(required=True)
    
    def validate_avatar(self, value):
        """验证头像文件"""
        # 验证文件大小（5MB）
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("图片大小不能超过5MB")
        
        # 验证文件类型
        if not value.content_type.startswith('image/'):
            raise serializers.ValidationError("请上传图片文件")
        
        return value

