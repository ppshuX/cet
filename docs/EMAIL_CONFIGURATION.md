# 邮件配置说明

## 📧 邮件发送配置

### 开发环境

默认情况下，开发环境（`DEBUG=True`）会将验证码输出到控制台，方便调试。

要启用真实邮件发送，需要：

#### 方法一：使用 .env 文件（推荐）

1. **创建 `.env` 文件**（在项目根目录）
```env
# 启用真实邮件发送
USE_REAL_EMAIL=1

# SMTP服务器配置
EMAIL_HOST=smtp.exmail.qq.com
EMAIL_PORT=587

# 发件邮箱账号和授权码
# 注意：QQ邮箱需要使用授权码，不是登录密码
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_authorization_code

# 发件人显示名称
DEFAULT_FROM_EMAIL=Roamio <your_email@example.com>
```

2. **重启 Django 服务器**

#### 方法二：使用环境变量（Windows PowerShell）

```powershell
# 在启动Django服务器前设置环境变量
$env:USE_REAL_EMAIL="1"
$env:EMAIL_HOST="smtp.exmail.qq.com"
$env:EMAIL_PORT="587"
$env:EMAIL_HOST_USER="your_email@example.com"
$env:EMAIL_HOST_PASSWORD="your_authorization_code"
$env:DEFAULT_FROM_EMAIL="Roamio <your_email@example.com>"

# 然后启动服务器
python manage.py runserver
```

### 生产环境

生产环境（`DEBUG=False`）会自动使用SMTP发送，需要确保设置了以下环境变量：

```env
EMAIL_HOST=smtp.exmail.qq.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_authorization_code
DEFAULT_FROM_EMAIL=Roamio <your_email@example.com>
```

## 📮 常见邮箱配置

### QQ邮箱 / 腾讯企业邮箱

1. **开启SMTP服务**：
   - QQ邮箱：设置 -> 账户 -> 开启POP3/IMAP/SMTP服务
   - 生成授权码（不是登录密码！）

2. **配置参数**：
```env
EMAIL_HOST=smtp.qq.com          # QQ个人邮箱
# 或
EMAIL_HOST=smtp.exmail.qq.com   # 腾讯企业邮箱
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### Gmail

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
# Gmail需要使用应用专用密码（不是账户密码）
```

### 163邮箱

```env
EMAIL_HOST=smtp.163.com
EMAIL_PORT=465
EMAIL_USE_SSL=True
# 或
EMAIL_PORT=25
EMAIL_USE_TLS=False
```

### Outlook / Hotmail

```env
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

## ⚠️ 重要提示

1. **授权码 vs 密码**：
   - QQ邮箱、Gmail等需要使用授权码或应用专用密码
   - 不是登录密码！

2. **安全性**：
   - `.env` 文件已被 `.gitignore` 忽略，不会提交到Git
   - 生产环境的敏感信息应通过服务器环境变量设置

3. **测试**：
   - 配置完成后，重启服务器
   - 发送验证码测试是否成功

## 🔍 故障排查

如果邮件发送失败，检查：

1. **环境变量是否正确设置**
   ```python
   # 在Django shell中测试
   python manage.py shell
   >>> import os
   >>> print(os.getenv('EMAIL_HOST_USER'))
   >>> print(os.getenv('USE_REAL_EMAIL'))
   ```

2. **SMTP服务器地址和端口是否正确**

3. **授权码是否正确**（不是登录密码）

4. **防火墙是否阻止了SMTP连接**

5. **查看Django日志中的错误信息**

