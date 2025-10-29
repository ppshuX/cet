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
    SendVerificationCodeSerializer,
    VerifyCodeSerializer,
    QQLoginSerializer,
    QQBindSerializer,
)
from ...utils.email_service import send_verification_code
from ...utils.rate_limit import check_email_rate_limit, check_ip_rate_limit, get_client_ip
from ...utils.qq_oauth import (
    get_qq_authorize_url,
    generate_state,
    get_qq_user_info_by_code,
)
from ...models import EmailVerificationCode, SocialAccount
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.cache import cache


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
    
    @action(detail=False, methods=['post'])
    def send_verification_code(self, request):
        """
        发送邮箱验证码
        
        频率限制：
        - 同一邮箱：5分钟内最多3次
        - 同一IP：1小时内最多10次
        """
        serializer = SendVerificationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        verification_type = serializer.validated_data['type']
        ip_address = get_client_ip(request)
        
        # 检查邮箱频率限制
        allowed, remaining_seconds, error_msg = check_email_rate_limit(
            email, 
            minutes=5, 
            max_requests=3
        )
        if not allowed:
            return Response({
                'error': error_msg,
                'remaining_seconds': remaining_seconds
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        # 检查IP频率限制
        allowed, remaining_seconds, error_msg = check_ip_rate_limit(
            ip_address,
            hours=1,
            max_requests=10
        )
        if not allowed:
            return Response({
                'error': error_msg,
                'remaining_seconds': remaining_seconds
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        # 对于注册类型，检查邮箱是否已注册
        if verification_type == 'register':
            from django.contrib.auth.models import User
            if User.objects.filter(email=email).exists():
                return Response({
                    'error': '该邮箱已被注册'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # 发送验证码
        success, verification_code, error_msg = send_verification_code(
            email=email,
            verification_type=verification_type,
            user=request.user if request.user.is_authenticated else None,
            ip_address=ip_address,
            expires_in_minutes=10
        )
        
        if success:
            return Response({
                'success': True,
                'message': '验证码已发送到您的邮箱',
                'expires_in': 600  # 10分钟（秒）
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': error_msg or '发送验证码失败，请稍后重试'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def verify_code(self, request):
        """验证邮箱验证码"""
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        verification_type = serializer.validated_data['type']
        
        # 查找有效的验证码
        verification_codes = EmailVerificationCode.objects.filter(
            email=email,
            code=code,
            verification_type=verification_type,
            is_used=False
        ).order_by('-created_at')
        
        # 查找未过期的验证码
        valid_code = None
        for vc in verification_codes:
            if vc.is_valid():
                valid_code = vc
                break
        
        if not valid_code:
            return Response({
                'error': '验证码无效或已过期，请重新获取'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 标记验证码为已使用
        valid_code.mark_as_used()
        
        # 生成临时验证token（用于后续注册/重置密码等操作，有效期5分钟）
        import secrets
        temp_token = secrets.token_urlsafe(32)
        cache.set(
            f'email_verified_token:{temp_token}',
            {
                'email': email,
                'verification_type': verification_type,
                'verified_at': timezone.now().isoformat()
            },
            timeout=300  # 5分钟有效期
        )
        
        return Response({
            'success': True,
            'verified': True,
            'message': '验证成功',
            'email': email,
            'verification_token': temp_token,  # 临时token，用于后续注册
            'expires_in': 300  # 5分钟（秒）
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def qq_login_url(self, request):
        """
        获取QQ登录URL
        
        返回QQ授权登录的URL，前端需要跳转到此URL
        """
        state = generate_state()
        authorize_url, state_generated = get_qq_authorize_url(state)
        
        # 将state存储到缓存（用于后续验证，有效期10分钟）
        cache.set(
            f'qq_oauth_state:{state_generated}',
            True,
            timeout=600
        )
        
        return Response({
            'authorization_url': authorize_url,
            'state': state_generated
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def qq_callback(self, request):
        """
        QQ登录回调处理
        
        处理QQ OAuth回调，如果已绑定则直接登录，如果未绑定则要求绑定邮箱
        """
        serializer = QQLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data['code']
        state = serializer.validated_data['state']
        
        # 验证state（CSRF防护）
        state_valid = cache.get(f'qq_oauth_state:{state}')
        if not state_valid:
            return Response({
                'error': '无效的state参数，请重新登录'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 删除state（一次性使用）
        cache.delete(f'qq_oauth_state:{state}')
        
        # 获取QQ用户信息
        qq_info = get_qq_user_info_by_code(code)
        if not qq_info.get('success'):
            return Response({
                'error': qq_info.get('error_description', 'QQ登录失败，请重试')
            }, status=status.HTTP_400_BAD_REQUEST)
        
        openid = qq_info.get('openid')
        unionid = qq_info.get('unionid', '')
        
        # 查找是否已绑定账号
        try:
            social_account = SocialAccount.objects.get(
                provider='qq',
                uid=openid
            )
            # 已绑定，直接登录
            user = social_account.user
            
            # 生成JWT Token
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'success': True,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data,
                'message': '登录成功'
            }, status=status.HTTP_200_OK)
            
        except SocialAccount.DoesNotExist:
            # 未绑定，返回需要绑定邮箱的信息
            # 临时存储QQ信息（用于后续绑定）
            import secrets
            temp_token = secrets.token_urlsafe(32)
            cache.set(
                f'qq_bind_temp:{openid}',
                qq_info,
                timeout=600  # 10分钟有效期
            )
            
            return Response({
                'success': False,
                'need_bind_email': True,
                'qq_info': {
                    'openid': openid,
                    'unionid': unionid,
                    'nickname': qq_info.get('nickname', ''),
                    'avatar_url': qq_info.get('avatar_url', ''),
                },
                'temp_token': temp_token,
                'message': '首次QQ登录，请绑定邮箱'
            }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def qq_bind(self, request):
        """
        QQ账号绑定（首次QQ登录时绑定邮箱）
        """
        serializer = QQBindSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data['code']
        state = serializer.validated_data['state']
        email = serializer.validated_data.get('email', '').strip().lower()
        verification_token = serializer.validated_data.get('verification_token')
        
        # 验证state
        state_valid = cache.get(f'qq_oauth_state:{state}')
        if not state_valid:
            return Response({
                'error': '无效的state参数'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cache.delete(f'qq_oauth_state:{state}')
        
        # 获取QQ用户信息
        qq_info = get_qq_user_info_by_code(code)
        if not qq_info.get('success'):
            return Response({
                'error': qq_info.get('error_description', '获取QQ信息失败')
            }, status=status.HTTP_400_BAD_REQUEST)
        
        openid = qq_info.get('openid')
        unionid = qq_info.get('unionid', '')
        
        # 检查是否已绑定
        if SocialAccount.objects.filter(provider='qq', uid=openid).exists():
            return Response({
                'error': '该QQ账号已被绑定'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证邮箱和验证token
        if not email or not verification_token:
            return Response({
                'error': '请先验证邮箱'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证邮箱验证token
        cache_key = f'email_verified_token:{verification_token}'
        token_data = cache.get(cache_key)
        
        if not token_data:
            return Response({
                'error': '邮箱验证token无效或已过期'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if token_data.get('email') != email:
            return Response({
                'error': '邮箱验证token与邮箱地址不匹配'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查邮箱是否已注册
        user = None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # 邮箱未注册，创建新账号
            base_username = email.split('@')[0]
            username = base_username
            counter = 1
            
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1
            
            import secrets
            random_password = secrets.token_urlsafe(16)
            user = User.objects.create_user(
                username=username,
                email=email,
                password=random_password
            )
            
            # 标记邮箱已验证
            if hasattr(user, 'profile'):
                user.profile.email_verified = True
                user.profile.email_verified_at = timezone.now()
                user.profile.save()
        
        # 创建QQ绑定
        SocialAccount.objects.create(
            user=user,
            provider='qq',
            uid=openid,
            unionid=unionid if unionid else None,
            nickname=qq_info.get('nickname', ''),
            avatar_url=qq_info.get('avatar_url', '')
        )
        
        # 删除验证token
        cache.delete(cache_key)
        
        # 生成JWT Token
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
            'message': 'QQ绑定成功'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def qq_bind_existing(self, request):
        """为已有账号绑定QQ"""
        serializer = QQLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data['code']
        state = serializer.validated_data['state']
        
        # 验证state
        state_valid = cache.get(f'qq_oauth_state:{state}')
        if not state_valid:
            return Response({
                'error': '无效的state参数'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cache.delete(f'qq_oauth_state:{state}')
        
        # 获取QQ用户信息
        qq_info = get_qq_user_info_by_code(code)
        if not qq_info.get('success'):
            return Response({
                'error': qq_info.get('error_description', '获取QQ信息失败')
            }, status=status.HTTP_400_BAD_REQUEST)
        
        openid = qq_info.get('openid')
        
        # 检查是否已被其他账号绑定
        if SocialAccount.objects.filter(provider='qq', uid=openid).exclude(user=request.user).exists():
            return Response({
                'error': '该QQ账号已被其他账号绑定'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查当前用户是否已绑定QQ
        if SocialAccount.objects.filter(user=request.user, provider='qq').exists():
            return Response({
                'error': '您已绑定QQ账号'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建绑定
        SocialAccount.objects.create(
            user=request.user,
            provider='qq',
            uid=openid,
            unionid=qq_info.get('unionid', ''),
            nickname=qq_info.get('nickname', ''),
            avatar_url=qq_info.get('avatar_url', '')
        )
        
        return Response({
            'success': True,
            'message': 'QQ绑定成功'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def qq_unbind(self, request):
        """解绑QQ账号"""
        try:
            social_account = SocialAccount.objects.get(
                user=request.user,
                provider='qq'
            )
            social_account.delete()
            
            return Response({
                'success': True,
                'message': 'QQ解绑成功'
            }, status=status.HTTP_200_OK)
            
        except SocialAccount.DoesNotExist:
            return Response({
                'error': '您未绑定QQ账号'
            }, status=status.HTTP_400_BAD_REQUEST)
