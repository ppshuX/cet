"""
邮件发送服务
"""
import os
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from ..models import EmailVerificationCode


def send_verification_email(email, code, verification_type='register', user=None):
    """
    发送邮箱验证码
    
    Args:
        email: 邮箱地址
        code: 验证码
        verification_type: 验证类型 (register, login, reset_password, bind_email)
        user: 用户对象（可选）
    
    Returns:
        bool: 发送是否成功
    """
    try:
        # 根据验证类型选择邮件主题
        subject_map = {
            'register': '欢迎注册 Roamio - 邮箱验证',
            'login': 'Roamio 登录验证',
            'reset_password': 'Roamio 重置密码',
            'bind_email': 'Roamio 绑定邮箱验证',
        }
        subject = subject_map.get(verification_type, 'Roamio 邮箱验证')
        
        # 渲染邮件内容
        context = {
            'code': code,
            'email': email,
            'verification_type': verification_type,
            'expires_in': 10,  # 10分钟有效期
        }
        
        # 尝试使用HTML模板
        try:
            html_message = render_to_string('emails/verification_code.html', context)
        except:
            # 如果模板不存在，使用简单的文本格式
            html_message = f"""
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif;">
                <h2 style="color: #667eea;">欢迎使用 Roamio！</h2>
                <p>您的验证码是：</p>
                <div style="font-size: 32px; font-weight: bold; color: #667eea; text-align: center; padding: 20px; background: #f5f5f5; border-radius: 8px; margin: 20px 0;">
                    {code}
                </div>
                <p style="color: #666;">验证码有效期：10分钟</p>
                <p style="color: #999; font-size: 12px;">如果这不是您的操作，请忽略此邮件。</p>
            </div>
            """
        
        # 文本格式（备用）
        message = f"您的 Roamio 验证码是：{code}，有效期10分钟。如果这不是您的操作，请忽略此邮件。"
        
        # 发送邮件
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            
            # 开发环境额外提示
            if settings.DEBUG:
                print("\n" + "=" * 50)
                print(f"[DEV] 验证码已发送到: {email}")
                print(f"验证码: {code}")
                print(f"类型: {verification_type}")
                print("=" * 50 + "\n")
            
            return True
        except Exception as send_error:
            # 更详细的错误信息
            error_msg = str(send_error)
            print(f"[ERROR] 邮件发送异常: {error_msg}")
            
            # 检查是否是配置问题
            if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
                if not settings.DEBUG:
                    print("[WARNING] EMAIL_HOST_USER 或 EMAIL_HOST_PASSWORD 未配置")
            
            raise  # 重新抛出异常以便上层处理
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"发送验证邮件失败: {e}")
        print(f"详细错误: {error_detail}")
        # 记录到Django日志
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"邮件发送失败: {e}\n{error_detail}")
        return False


def send_verification_code(email, verification_type='register', user=None, ip_address=None, expires_in_minutes=10):
    """
    生成并发送验证码
    
    Args:
        email: 邮箱地址
        verification_type: 验证类型
        user: 用户对象（可选）
        ip_address: IP地址（可选）
        expires_in_minutes: 过期时间（分钟）
    
    Returns:
        tuple: (success: bool, code: EmailVerificationCode or None, error_message: str)
    """
    try:
        # 创建验证码
        verification_code = EmailVerificationCode.create_code(
            email=email,
            verification_type=verification_type,
            user=user,
            ip_address=ip_address,
            expires_in_minutes=expires_in_minutes
        )
        
        # 发送邮件
        success = send_verification_email(
            email=email,
            code=verification_code.code,
            verification_type=verification_type,
            user=user
        )
        
        if success:
            return True, verification_code, None
        else:
            # 如果发送失败，删除验证码记录
            verification_code.delete()
            return False, None, "邮件发送失败，请稍后重试"
            
    except Exception as e:
        error_msg = f"生成验证码失败: {str(e)}"
        print(error_msg)
        return False, None, error_msg

