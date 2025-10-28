"""
认证相关 ViewSet
处理用户注册、登录、登出等功能
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ...serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
)


@method_decorator(csrf_exempt, name='dispatch')
class AuthViewSet(viewsets.GenericViewSet):
    """认证相关ViewSet"""
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """用户注册"""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # 生成JWT Token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """用户登录"""
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """用户登出"""
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'detail': '登出成功'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': '登出失败'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """获取当前用户信息"""
        # 自动计算并更新等级
        if request.user.profile:
            request.user.profile.calculate_level()
            request.user.profile.save()
        
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
