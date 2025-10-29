# 📘 Django 实际邮箱发送配置与调试总结

## 一、项目目标

让 Django 能通过 **QQ 邮箱 SMTP 服务器** 发送真实邮件（例如验证码、注册确认、找回密码等），而不是仅在控制台打印内容。

---

## 二、环境与前提条件

| 项目        | 值                     |
| --------- | --------------------- |
| 系统环境      | Ubuntu 20.04（阿里云 ECS） |
| Python 版本 | 3.8                   |
| Django 版本 | 任意（3.x 或 4.x 均可）      |
| 邮箱服务商     | QQ 邮箱                 |
| 邮件协议      | SMTP（端口 587 / TLS）    |
| 授权码       | QQ 邮箱后台生成             |

---

## 三、操作步骤

### 1️⃣ 创建 `.env` 文件

在项目根目录（与 `manage.py` 同级）执行：

```bash
touch .env
```

内容如下（示例）：

```bash
# ==================== 邮件配置 ====================
USE_REAL_EMAIL=1

# SMTP服务器配置（QQ邮箱）
EMAIL_HOST=smtp.qq.com
EMAIL_PORT=587

# ⚠️ 邮箱账号和授权码（授权码不是密码）
EMAIL_HOST_USER=2064747320@qq.com
EMAIL_HOST_PASSWORD=vjywgfmoemlibheh

# 发件人显示名称
DEFAULT_FROM_EMAIL=Roamio <2064747320@qq.com>

# ==================== QQ OAuth 配置 ====================
QQ_APP_ID=102813859
QQ_APP_KEY=OddPvLYXHo69wTYO
QQ_REDIRECT_URI=https://app7508.acapp.acwing.com.cn/settings/qq/receive_code
```

**注意：** `.env` 文件已添加到 `.gitignore`，不会被提交到 Git 仓库。

---

### 2️⃣ 在 QQ 邮箱获取授权码

1. 登录 [QQ邮箱网页版](https://mail.qq.com/)
2. 打开：**设置 → 账户 → POP3/IMAP/SMTP服务**
3. 启用 "SMTP 服务"
4. 点击 "生成授权码"
5. 验证身份后获得授权码，例如：

   ```
   vjywgfmoemlibheh
   ```
6. 将授权码填入 `.env` 文件中。

**⚠️ 重要提示：**
- 授权码不是登录密码，需要单独生成
- 授权码一旦生成，旧密码会失效
- 妥善保管授权码，不要泄露

---

### 3️⃣ 修改 Django 设置（settings.py）

```python
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ==================== 邮件配置 ====================
# 是否使用真实邮件发送（如果USE_REAL_EMAIL=1，即使是开发环境也会真实发送邮件）
USE_REAL_EMAIL = os.getenv('USE_REAL_EMAIL', '0') == '1'

# 开发环境默认使用控制台后端（验证码会打印到控制台）
# 如果设置了 USE_REAL_EMAIL=1，则使用真实SMTP发送
# 生产环境始终使用SMTP后端
if DEBUG and not USE_REAL_EMAIL:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    print("=" * 50)
    print("[DEV] 开发环境：邮件将输出到控制台")
    print("[提示] 要发送真实邮件，请设置环境变量: USE_REAL_EMAIL=1")
    print("=" * 50)
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.qq.com')  # QQ邮箱SMTP
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')  # 从环境变量读取
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')  # 从环境变量读取
    if USE_REAL_EMAIL and DEBUG:
        print("=" * 50)
        print("[DEV] 使用真实SMTP发送邮件")
        if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
            print("[警告] EMAIL_HOST_USER 或 EMAIL_HOST_PASSWORD 未配置，邮件发送可能失败")
        print("=" * 50)

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'Roamio <noreply@roamio.com>')
```

---

### 4️⃣ 确保安装依赖包

```bash
pip install python-dotenv
```

或者添加到 `requirements.txt`：

```
python-dotenv>=0.19.0
```

然后安装：

```bash
pip install -r requirements.txt
```

---

### 5️⃣ 开放服务器端口（阿里云 ECS）

登录 [阿里云控制台 → 安全组 → 入方向规则]，添加以下配置：

| 授权策略 | 协议类型    | 端口范围    | 授权对象      | 描述     |
| ---- | ------- | ------- | --------- | ------ |
| 允许   | 自定义 TCP | 587/587 | 0.0.0.0/0 | QQ邮箱验证 |

（建议出方向也放行 587）

**操作步骤：**
1. 进入阿里云控制台
2. 找到你的 ECS 实例
3. 点击 "安全组"
4. 配置规则 → 入方向规则 → 添加安全组规则
5. 填写上述表格内容
6. 保存

---

### 6️⃣ 测试端口连通性

安装 telnet：

```bash
sudo apt update
sudo apt install telnet -y
```

测试：

```bash
telnet smtp.qq.com 587
```

**成功输出示例：**

```
Trying 58.251.111.79...
Connected to smtp.qq.com.
Escape character is '^]'.
220 smtp.qq.com Esmtp QQ Mail Server
```

✅ 表示端口畅通。

按 `Ctrl + ]` 然后输入 `quit` 退出 telnet。

**如果连接失败：**
- 检查安全组配置是否正确
- 检查服务器防火墙是否拦截
- 确认服务器能访问外网

---

### 7️⃣ 发送测试邮件

进入 Django Shell：

```bash
python3 manage.py shell
```

运行：

```python
from django.core.mail import send_mail
from django.conf import settings

# 检查配置
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")

# 发送测试邮件
result = send_mail(
    subject='QQ邮箱发信测试',
    message='你好，这是一封来自 Django 的测试邮件！\n\n如果你收到这封邮件，说明配置成功！',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['你的其他邮箱@gmail.com'],  # 替换为你的真实邮箱
    fail_silently=False,
)

print(f"\n发送结果: {result}")
```

**成功输出：**

```
EMAIL_BACKEND: django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST: smtp.qq.com
EMAIL_PORT: 587
EMAIL_HOST_USER: 2064747320@qq.com

发送结果: 1
```

并且你的收件箱能收到邮件，则表示配置成功 ✅。

---

## 四、常见问题与解决方案

| 问题                        | 原因                     | 解决方法                        |
| ------------------------- | ---------------------- | --------------------------- |
| `ConnectionRefusedError`  | 服务器防火墙拦截端口             | 在阿里云安全组开放 587 或 465         |
| `SMTPAuthenticationError` | 授权码错误或 SMTP 未启用        | 确认重新生成 QQ 邮箱授权码             |
| `No Mx Record Found`      | 收件人域名无效（如 example.com） | 使用真实邮箱地址测试                  |
| `TimeoutError`            | 网络不通或 DNS 问题           | 检查服务器是否能 ping 通 smtp.qq.com |
| `.env` 文件未读取          | `python-dotenv` 未安装或路径错误 | 确认 `load_dotenv()` 在 settings.py 开头调用 |
| 邮件发送成功但收不到          | 被标记为垃圾邮件或被拦截           | 检查垃圾邮件文件夹，配置 SPF/DKIM 记录    |

---

## 五、验证结果

最终测试结果：

| 测试项         | 状态     | 说明            |
| ----------- | ------ | ------------- |
| `.env` 配置   | ✅ 正常加载 | 环境变量成功读取        |
| QQ 授权码      | ✅ 有效   | SMTP 认证通过        |
| SMTP 端口 587 | ✅ 通    | telnet 测试成功      |
| 邮件发送        | ✅ 成功   | Django shell 测试通过 |
| Gmail 收件    | ✅ 成功   | 收件箱正常收到邮件      |

---

## 六、进阶优化

### ✅ 添加 HTML 邮件模板

创建邮件模板 `templates/emails/verification_code.html`：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Roamio 验证码</title>
</head>
<body>
    <h2>您的验证码是：{{ code }}</h2>
    <p>有效期：10分钟</p>
</body>
</html>
```

发送 HTML 邮件：

```python
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def send_html_email(subject, template_name, context, to_email):
    html_content = render_to_string(template_name, context)
    text_content = '请使用支持HTML的邮件客户端查看此邮件'
    
    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
```

### ✅ 封装通用邮件发送函数

参见项目中的 `trips/utils/email_service.py`：

```python
from trips.utils import send_verification_code

# 发送验证码
success, code, error_msg = send_verification_code(
    email='user@example.com',
    verification_type='register',
    expires_in_minutes=10
)
```

### ✅ 自定义管理命令

创建 `trips/management/commands/sendtestmail.py`：

```python
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = '发送测试邮件'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='收件人邮箱')

    def handle(self, *args, **options):
        email = options['email']
        
        result = send_mail(
            subject='Roamio 测试邮件',
            message='这是一封测试邮件',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        
        if result:
            self.stdout.write(self.style.SUCCESS(f'邮件已发送到 {email}'))
        else:
            self.stdout.write(self.style.ERROR('邮件发送失败'))
```

使用：

```bash
python manage.py sendtestmail you@example.com
```

### ✅ 配合 Celery 异步发送邮件

安装 Celery：

```bash
pip install celery redis
```

配置异步任务：

```python
# tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_async(subject, message, recipient_list):
    send_mail(subject, message, None, recipient_list)
```

调用：

```python
from .tasks import send_email_async

send_email_async.delay(
    subject='验证码',
    message='您的验证码是123456',
    recipient_list=['user@example.com']
)
```

---

## 七、项目集成示例

### 在 Roamio 项目中的使用

项目已实现完整的邮箱验证码功能：

1. **发送验证码 API**: `POST /api/v1/auth/send_verification_code/`
2. **验证验证码 API**: `POST /api/v1/auth/verify_code/`
3. **注册时验证邮箱**: 注册需要提供 `verification_token`

**完整流程：**

```
用户注册 → 发送验证码 → 验证码存入数据库 → 发送邮件 → 
用户输入验证码 → 验证通过 → 生成临时token → 用户提交注册表单 → 
验证token → 创建用户 → 标记邮箱已验证
```

---

## 八、安全建议

1. **保护授权码**
   - 永远不要将授权码提交到 Git 仓库
   - 使用环境变量管理敏感信息
   - 定期更换授权码

2. **防止邮件滥用**
   - 实现发送频率限制（IP、邮箱）
   - 验证收件人邮箱格式
   - 记录发送日志用于审计

3. **邮件内容安全**
   - 避免在邮件中暴露敏感信息
   - 使用 HTTPS 链接
   - 验证用户操作的真实性

4. **配置 SPF 记录（可选）**
   - 在域名 DNS 中添加 SPF 记录，提高邮件送达率
   - 示例：`v=spf1 include:qq.com ~all`

---

## 九、总结

🎯 **你已掌握：**

* ✅ 环境变量配置（`.env` 文件 + `python-dotenv`）
* ✅ QQ 邮箱 SMTP 授权码获取和使用
* ✅ Django 邮件模块配置原理
* ✅ 服务器安全组端口放行
* ✅ 邮件发送完整验证流程
* ✅ HTML 邮件模板制作
* ✅ 频率限制和安全防护

📦 **最终效果：**

> Django 项目可以在云端通过 QQ 邮箱自动发送真实邮件，实现注册验证、密码重置、通知提醒等功能。

---

## 十、相关文档

- [Django 邮件文档](https://docs.djangoproject.com/en/5.0/topics/email/)
- [QQ 邮箱 SMTP 设置帮助](https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256)
- [项目邮箱验证流程文档](./EMAIL_QQ_LOGIN_FLOW.md)
- [账号安全改进规划](./ACCOUNT_SECURITY_IMPROVEMENT.md)

---

**文档版本：** v1.0  
**创建日期：** 2024年10月  
**最后更新：** 2024年10月

---

💡 **提示：** 此文档已保存到项目中，路径：`docs/DJANGO_EMAIL_SETUP_COMPLETE.md`

