#!/usr/bin/env python
"""
快速配置邮件发送功能
运行此脚本会创建 .env 文件（如果不存在）
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
ENV_FILE = BASE_DIR / '.env'

def create_env_file():
    """创建.env文件"""
    if ENV_FILE.exists():
        print("⚠️  .env 文件已存在！")
        choice = input("是否要覆盖现有配置？(y/N): ")
        if choice.lower() != 'y':
            print("取消操作")
            return
    
    print("\n📧 邮件配置向导")
    print("=" * 50)
    
    use_real = input("\n是否启用真实邮件发送？(Y/n，默认N，仅控制台输出): ").strip().lower()
    use_real_email = '0' if use_real == 'n' else '1'
    
    if use_real_email == '1':
        print("\n请输入SMTP配置：")
        email_host = input("SMTP服务器 (默认: smtp.exmail.qq.com): ").strip() or 'smtp.exmail.qq.com'
        email_port = input("SMTP端口 (默认: 587): ").strip() or '587'
        email_user = input("发件邮箱地址: ").strip()
        email_password = input("邮箱授权码/密码: ").strip()
        default_from = input(f"发件人显示名称 (默认: Roamio <{email_user}>): ").strip() or f'Roamio <{email_user}>'
        
        if not email_user or not email_password:
            print("❌ 邮箱地址和授权码不能为空！")
            return
        
        env_content = f"""# 邮件配置
USE_REAL_EMAIL=1
EMAIL_HOST={email_host}
EMAIL_PORT={email_port}
EMAIL_HOST_USER={email_user}
EMAIL_HOST_PASSWORD={email_password}
DEFAULT_FROM_EMAIL={default_from}

# QQ OAuth 配置（已配置）
QQ_APP_ID=102813859
QQ_APP_KEY=OddPvLYXHo69wTYO
QQ_REDIRECT_URI=https://app7508.acapp.acwing.com.cn/settings/qq/receive_code
"""
    else:
        env_content = """# 邮件配置（开发环境：验证码输出到控制台）
USE_REAL_EMAIL=0

# QQ OAuth 配置（已配置）
QQ_APP_ID=102813859
QQ_APP_KEY=OddPvLYXHo69wTYO
QQ_REDIRECT_URI=https://app7508.acapp.acwing.com.cn/settings/qq/receive_code
"""
    
    ENV_FILE.write_text(env_content, encoding='utf-8')
    print(f"\n✅ .env 文件已创建: {ENV_FILE}")
    print("\n📝 提示：")
    print("   1. 重启Django服务器使配置生效")
    if use_real_email == '1':
        print("   2. 确保邮箱授权码正确（QQ邮箱需要生成授权码，不是登录密码）")
        print("   3. 如发送失败，请查看 docs/EMAIL_CONFIGURATION.md 获取帮助")
    else:
        print("   2. 验证码将显示在Django服务器控制台")
    print("")

if __name__ == '__main__':
    create_env_file()

