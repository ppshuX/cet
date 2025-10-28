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
        fields = ['avatar', 'avatar_url', 'bio', 'tags', 'level', 'visited_countries']
    
    def get_avatar_url(self, obj):
        """获取头像URL"""
        return obj.get_avatar_url()


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    profile = UserProfileSerializer(read_only=True)
    stats = serializers.SerializerMethodField()
    is_superuser = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'is_superuser', 'is_staff', 'profile', 'stats']
        read_only_fields = ['id', 'date_joined', 'is_superuser', 'is_staff']
    
    def get_stats(self, obj):
        """获取用户统计信息"""
        return {
            # 总旅行数（包括私有的，用户自己查看）
            'trips_count': obj.trips.count(),
            # 公开的旅行数（对外显示的，只有公开的才算入等级）
            'public_trips_count': obj.trips.filter(visibility='public').count(),
            # 评论数
            'comments_count': obj.comments.count(),  # 使用 'comments' 因为 Comment 模型的 related_name 是 'comments'
        }


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
            'email': {'required': False},
            'username': {'error_messages': {'required': '用户名不能为空'}},
            'password': {'error_messages': {'required': '密码不能为空'}},
            'password2': {'error_messages': {'required': '请确认密码'}}
        }
    
    def validate_username(self, value):
        """验证用户名"""
        if not value or not value.strip():
            raise serializers.ValidationError("用户名不能为空")
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("用户名至少需要3个字符")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("该用户名已被使用，请选择其他用户名")
        return value
    
    def validate_email(self, value):
        """验证邮箱"""
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("该邮箱已被注册")
        return value
    
    def validate(self, attrs):
        """验证两次密码是否一致"""
        password = attrs.get('password')
        password2 = attrs.get('password2')
        
        if password and password2 and password != password2:
            raise serializers.ValidationError({
                "password2": "两次输入的密码不一致"
            })
        
        if password and len(password) < 8:
            raise serializers.ValidationError({
                "password": "密码至少需要8个字符"
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
        if not value or not value.strip():
            raise serializers.ValidationError("用户名不能为空")
        value = value.strip()
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("该用户名已被使用，请选择其他用户名")
        return value


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """更新用户配置序列化器"""
    
    class Meta:
        model = UserProfile
        fields = ['bio', 'tags', 'visited_countries']
    
    def validate_bio(self, value):
        """验证个人简介长度"""
        if value and len(value) > 500:
            raise serializers.ValidationError("个人简介不能超过500字")
        return value
    
    def validate_tags(self, value):
        """验证标签格式"""
        if value:
            tags = [tag.strip() for tag in value.split(',') if tag.strip()]
            # 最多10个标签
            if len(tags) > 10:
                raise serializers.ValidationError("标签数量不能超过10个")
            # 每个标签最多20个字符
            for tag in tags:
                if len(tag) > 20:
                    raise serializers.ValidationError(f"标签'{tag}'长度不能超过20个字符")
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

