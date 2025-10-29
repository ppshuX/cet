# 账号安全改进规划

## 📋 项目概述

### 背景
当前系统存在以下安全隐患：
- 注册和登录缺乏邮箱验证，可能存在恶意注册
- 缺少第三方登录（QQ），用户体验不够完善
- 无法确保账号唯一性和可追溯性

### 目标
1. **增强安全性**：通过邮箱验证确保账号真实性
2. **提升用户体验**：支持QQ快速登录
3. **保障账号唯一性**：同一邮箱/QQ只能绑定一个账号
4. **防止恶意行为**：通过验证机制减少垃圾账号和恶意评论

---

## 🎯 功能需求

### 核心功能

#### 1. 邮箱验证系统
- [x] 注册时邮箱验证（发送验证码）
- [x] 登录时的邮箱验证（可选，根据风险等级）
- [x] 邮箱验证码有效期管理（5-10分钟）
- [x] 验证码发送频率限制（防刷）
- [x] 邮箱唯一性校验

#### 2. QQ登录集成
- [x] QQ OAuth 2.0 接入
- [x] 首次QQ登录自动绑定邮箱
- [x] 已有账号绑定QQ功能
- [x] QQ账号解绑功能
- [x] QQ登录状态保持

#### 3. 账号唯一性保障
- [x] 同一邮箱只能注册一个账号
- [x] 同一QQ只能绑定一个账号
- [x] 邮箱+QQ双重验证机制
- [x] 账号合并策略（处理冲突）

---

## 🏗️ 技术架构设计

### 数据库模型变更

#### 1. User模型扩展

```python
# trips/models/user_profile.py 扩展

class User(AbstractUser):
    """
    扩展Django默认User模型
    """
    # 现有字段保持不变
    # username, email, password, ...
    
    # 新增字段
    email_verified = models.BooleanField(default=False, verbose_name='邮箱已验证')
    email_verified_at = models.DateTimeField(null=True, blank=True, verbose_name='邮箱验证时间')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='手机号')
    is_active = models.BooleanField(default=True)  # 邮箱验证后激活
    
    # 元数据
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        db_table = 'auth_user'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['email_verified']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.email})"
```

#### 2. 第三方登录绑定模型（新建）

```python
# trips/models/social_auth.py (新建文件)

from django.db import models
from django.contrib.auth.models import User

class SocialAccount(models.Model):
    """
    第三方账号绑定表
    支持：QQ、微信、GitHub等
    """
    PROVIDER_CHOICES = [
        ('qq', 'QQ'),
        ('wechat', '微信'),
        ('github', 'GitHub'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='social_accounts',
        verbose_name='用户'
    )
    provider = models.CharField(
        max_length=20, 
        choices=PROVIDER_CHOICES,
        verbose_name='登录提供商'
    )
    uid = models.CharField(
        max_length=100, 
        db_index=True,
        verbose_name='第三方用户ID'
    )
    unionid = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name='UnionID（QQ/微信）'
    )
    nickname = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name='第三方昵称'
    )
    avatar_url = models.URLField(
        blank=True,
        verbose_name='第三方头像URL'
    )
    
    # 绑定时间
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'social_account'
        unique_together = [('provider', 'uid')]  # 同一平台的同一账号只能绑定一次
        indexes = [
            models.Index(fields=['provider', 'uid']),
            models.Index(fields=['user', 'provider']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_provider_display()}"
```

#### 3. 邮箱验证码模型（新建）

```python
# trips/models/email_verification.py (新建文件)

from django.db import models
from django.contrib.auth.models import User
import secrets

class EmailVerificationCode(models.Model):
    """
    邮箱验证码存储
    """
    VERIFICATION_TYPES = [
        ('register', '注册验证'),
        ('login', '登录验证'),
        ('reset_password', '重置密码'),
        ('bind_email', '绑定邮箱'),
    ]
    
    email = models.EmailField(verbose_name='邮箱地址', db_index=True)
    code = models.CharField(max_length=10, verbose_name='验证码')
    verification_type = models.CharField(
        max_length=20, 
        choices=VERIFICATION_TYPES,
        verbose_name='验证类型'
    )
    
    # 状态管理
    is_used = models.BooleanField(default=False, verbose_name='已使用')
    expires_at = models.DateTimeField(verbose_name='过期时间')
    
    # 关联用户（注册时可能还没有用户）
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='verification_codes'
    )
    
    # IP和元数据
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'email_verification_code'
        indexes = [
            models.Index(fields=['email', 'code', 'is_used']),
            models.Index(fields=['expires_at']),
        ]
        # 清理过期验证码（通过定时任务）
    
    @classmethod
    def generate_code(cls, length=6):
        """生成数字验证码"""
        return ''.join([str(secrets.randbelow(10)) for _ in range(length)])
    
    def is_valid(self):
        """检查验证码是否有效"""
        from django.utils import timezone
        return not self.is_used and self.expires_at > timezone.now()
    
    def __str__(self):
        return f"{self.email} - {self.code} ({self.verification_type})"
```

---

## 🔌 API设计

### 1. 邮箱验证相关API

#### 1.1 发送验证码
```
POST /api/v1/auth/send-verification-code/
```

**请求体：**
```json
{
  "email": "user@example.com",
  "type": "register",  // register, login, reset_password
  "recaptcha_token": "..."  // 可选：Google reCAPTCHA token
}
```

**响应：**
```json
{
  "success": true,
  "message": "验证码已发送到您的邮箱",
  "expires_in": 300  // 过期时间（秒）
}
```

**限制：**
- 同一邮箱5分钟内最多3次
- 同一IP 1小时内最多10次
- 验证码有效期：5因子10分钟

#### 1.2 验证邮箱验证码
```
POST /api/v1/auth/verify-email-code/
```

**请求体：**
```json
{
  "email": "user@example.com",
  "code": "123456",
  "type": "register"
}
```

**响应：**
```json
{
  "success": true,
  "verified": true,
  "token": "..."  // 临时token，用于完成注册
}
```

### 2. 注册API（修改）

#### 2.1 用户注册
```
POST /api/v1/auth/register/
```

**请求体：**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "username": "username",
  "verification_token": "...",  // 来自验证码验证的token
  "avatar": "..."  // 可选
}
```

**流程：**
1. 检查邮箱是否已验证（通过verification_token）
2. 检查邮箱是否已注册
3. 创建用户（email_verified=True）
4. 自动登录，返回JWT token

### 3. QQ登录相关API

#### 3.1 获取QQ登录URL
```
GET /api/v1/auth/qq/login-url/
```

**响应：**
```json
{
  "authorization_url": "https://graph.qq.com/oauth2.0/authorize?...",
  "state": "random_state_string"  // 用于CSRF防护
}
```

#### 3.2 QQ登录回调
```
GET /settings/qq/receive_code?code=xxx&state=xxx
```

**注意**：回调地址需要匹配QQ开发者平台配置的实际回调域

**处理流程：**
1. 验证state参数（CSRF防护）
2. 通过code获取access_token
3. 获取QQ用户信息（openid, unionid）
4. 检查是否已绑定账号
   - 已绑定 → 直接登录，返回JWT token
   - 未绑定 → 要求绑定邮箱 → 发送验证码 → 创建账号并绑定
5. 前端处理：
   - 成功：保存JWT token，跳转到首页
   - 需要绑定邮箱：跳转到邮箱绑定页面

#### 3.3 绑定QQ账号（已有账号）
```
POST /api/v1/auth/qq/bind/
```

**请求：**（需要JWT认证）
- Headers: `Authorization: Bearer <token>`

**请求体：**
```json
{
  "qq_code": "...",  // QQ OAuth回调code
  "state": "..."
}
```

#### 3.4 解绑QQ账号
```
DELETE /api/v1/auth/qq/unbind/
```

**请求：**（需要JWT认证）

### 4. 登录API（修改）

#### 4.1 邮箱+密码登录
```
POST /api/v1/auth/login/
```

**请求体：**
```json
{
  "email": "user@example.com",  // 改为email而不是username
  "password": "password",
  "need_verification": false  // 根据风险等级决定
}
```

**流程：**
1. 验证邮箱+密码
2. 风险检测：
   - 新IP地址 → 需要邮箱验证
   - 多次失败 → 需要邮箱验证
   - 新设备 → 可选邮箱验证
3. 返回JWT token

---

## 📧 邮件服务配置

### 方案选择

#### 推荐方案：腾讯企业邮箱 / SendGrid

**腾讯企业邮箱：**
- 优点：国内稳定，免费额度高，QQ登录天然亲和
- 配置：SMTP方式

**SendGrid：**
- 优点：国际化，送达率高，API友好
- 配置：REST API

### Django邮件配置

```python
# roamio/settings.py

# 邮件配置（推荐使用环境变量）
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.exmail.qq.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'Roamio <noreply@roamio.com>')

# 邮件模板路径
EMAIL_TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates', 'emails')
```

### 邮件模板设计

```html
<!-- templates/emails/verification_code.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Roamio 邮箱验证</title>
</head>
<body>
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2>欢迎使用 Roamio！</h2>
        <p>您的验证码是：</p>
        <div style="font-size: 32px; font-weight: bold; color: #667eea; text-align: center; padding: 20px; background: #f5f5f5; border-radius: 8px;">
            {{ code }}
        </div>
        <p style="color: #666;">验证码有效期：10分钟</p>
        <p style="color: #999; font-size: 12px;">如果这不是您的操作，请忽略此邮件。</p>
    </div>
</body>
</html>
```

---

## 🔐 QQ OAuth 2.0 接入

### 申请步骤

1. **访问QQ互联开发者平台**
   - URL: https://connect.qq.com/
   - 注册/登录开发者账号

2. **创建应用**
   - 应用名称：Roamio旅行平台
   - 应用类型：网站应用
   - 回调地址：`https://app7581.acapp.acwing.com.cn/settings/qq/receive_code`

3. **获取凭证**
   - ✅ **App ID**: `102813859`
   - ✅ **App Key**: `OddPvLYXHo69wTYO`
   - ✅ **网站地址**: `https://app7508.acapp.acwing.com.cn/`
   - ✅ **回调域**: `https://app7508.acapp.acwing.com.cn/settings/qq/receive_code`

### OAuth流程

```
1. 用户点击"QQ登录"
   ↓
2. 重定向到QQ授权页面
   ↓
3. 用户授权后，QQ回调到我们的服务器
   ↓
4. 服务器用code换取access_token
   ↓
5. 用access_token获取用户信息（openid, unionid）
   ↓
6. 检查是否已绑定账号
   - 已绑定 → 登录
   - 未绑定 → 要求绑定邮箱 → 创建账号
   ↓
7. 返回JWT token给前端
```

### 环境变量配置

```bash
# .env
QQ_APP_ID=102813859
QQ_APP_KEY=OddPvLYXHo69wTYO
QQ_REDIRECT_URI=https://app7508.acapp.acwing.com.cn/settings/qq/receive_code
QQ_BASE_URL=https://graph.qq.com
```

### 实际发生时信息

**已申请完成 ✅**

- **App ID**: `102813859`
- **App Key**: `OddPvLYXHo69wTYO`
- **网站地址**: `https://app7508.acapp.acwing.com.cn/`
- **回调地址**: `https://app7508.acapp.acwing.com.cn/settings/qq/receive_code`

**注意**：
- 回调地址需要与QQ开发者平台配置完全一致
- 回调地址已统一为：`https://app7508.acapp.acwing.com.cn/settings/qq/receive_code`
- 前后端使用统一域名，避免跨域问题

---

## ⏱️ 实施计划

### 阶段一：基础准备（1-2天）

**Day 1:**
- [x] 申请QQ互联开发者账号和应用 ✅ **已完成**
  - App ID: `102813849`
  - App Key: `42qVzHPOBoEPM5c1`
  - 网站地址: `https://app7508.acapp.acwing.com.cn/`
  - 回调地址: `https://app7508.acapp.acwing.com.cn/settings/qq/receive_code`
- [ ] 配置邮件服务（腾讯企业邮箱/SendGrid）
- [ ] 设计数据库迁移脚本
- [ ] 创建环境变量配置（已提供QQ凭证）

**Day 2:**
- [ ] 编写数据库迁移
- [ ] 创建新的模型（SocialAccount, EmailVerificationCode）
- [ ] 扩展User模型
- [ ] 执行数据库迁移

### 阶段二：邮箱验证功能（3-4天）

**Day 3-4:**
- [ ] 实现邮件发送服务（utils/email.py）
- [ ] 创建邮件模板
- [ ] 实现验证码生成和存储逻辑
- [ ] 实现发送验证码API
- [ ] 实现验证验证码API
- [ ] 添加频率限制中间件

**Day 5-6:**
- [ ] 修改注册API，集成邮箱验证
- [ ] 修改登录API，添加风险检测
- [ ] 前端：注册页面集成邮箱验证
- [ ] 前端：登录页面优化
- [ ] 测试邮箱验证流程

### 阶段三：QQ登录集成（4-5天）

**Day 7-8:**
- [ ] 安装QQ OAuth相关库（requests即可）
- [ ] 实现QQ OAuth工具函数
- [ ] 实现获取QQ登录URL API
- [ ] 实现QQ回调处理API
- [ ] 实现账号绑定逻辑

**Day 9-10:**
- [ ] 前端：QQ登录按钮组件
- [ ] 前端：QQ登录回调处理
- [ ] 实现绑定/解绑QQ Due API
- [ ] 用户中心：显示QQ绑定状态
- [ ] 测试QQ登录完整流程

### 阶段四：联调和优化（2-3天）

**Day 11-12:**
- [ ] 端到端测试
- [ ] 错误处理优化
- [ ] 用户体验优化（loading、错误提示）
- [ ] 安全性测试（SQL注入、XSS等）
- [ ] 性能优化（缓存验证码查询）

**Day 13:**
- [ ] 生产环境部署
- [ ] 监控和日志等待置
- [ ] 文档更新

### 总计时间：13-15天

---

## 🛡️ 安全考虑

### 1. 验证码安全
- ✅ 验证码使用加密存储（或hash）
- ✅ 验证码只能使用一次
- ✅ 设置合理的过期时间
- ✅ IP和邮箱频率限制

### 2. QQ OAuth安全
- ✅ State参数CSRF防护
- ✅ Token安全存储
- ✅ 回调URL白名单验证

### 3. 账号唯一性
- ✅ 数据库唯一索引
- ✅ 应用层双重校验
- ✅ 并发注册处理（数据库锁）

### 4. 数据保护
- ✅ 敏感信息加密存储
- ✅ 日志中不记录密码
- ✅ IP地址脱敏处理

---

## 📊 监控和日志

### 关键指标
1. **注册转化率**：发送验证码 → 成功注册
2. **验证码发送量**：每日/每小时
3. **QQ登录使用率**：QQ登录 vs 邮箱登录
4. **异常登录检测**：新IP、失败次数

### 日志记录
```python
# 记录事件
- 验证码发送
- 验证码验证成功/失败
- QQ登录成功/失败
- 账号绑定/解绑
- 异常IP访问
```

---

## 🧪 测试计划

### 单元测试
- [ ] 验证码生成和验证
- [ ] 邮箱验证逻辑
- [ ] QQ OAuth流程
- [ ] 账号绑定逻辑

### 集成测试
- [ ] 完整注册流程
- [ ] 完整登录流程
- [ ] QQ登录流程
- [ ] 异常情况处理

### 安全测试
- [ ] 验证码暴力破解
- [ ] 频率限制绕过
- [ ] CSRF攻击防护
- [ ] SQL注入测试

---

## 📝 前端改动清单

### 需要修改的页面

1. **注册页面** (`web/src/views/RegisterView.vue`)
   - 添加邮箱验证码输入框
   - 添加"发送验证码"按钮
   - 优化表单验证

2. **登录页面** (`web/src/views/LoginView.vue`)
   - 改为邮箱登录（替代username）
   - 添加QQ登录按钮
   - 添加风险登录时的验证码验证

3. **用户中心** (`web/src/views/UserCenterView.vue`)
   - 显示QQ绑定状态
   - 添加"绑定QQ"按钮
   - 添加"解绑QQ"功能

### 新增组件

- `web/src/components/EmailVerification.vue` - 邮箱验证组件
- `web/src/components/QQLoginButton.vue` - QQ登录按钮

---

## 📚 相关文档

- [QQ互联开发者文档](https://wiki.connect.qq.com/)
- [Django邮件发送](https://docs.djangoproject.com/en/5.0/topics/email/)
- [DRF SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)

---

## ✅ 验收标准

### 功能验收
- [ ] 新用户注册必须通过邮箱验证
- [ ] 可以通过QQ快速登录
- [ ] QQ登录后必须绑定邮箱
- [ ] 同一邮箱/QQ只能绑定一个账号
-/index.html - 验证码发送有频率限制
- [ ] 异常登录会触发二次验证

### 性能验收
- [ ] 验证码发送响应时间 < 2秒
- [ ] QQ登录流程 < 5秒
- [ ] 并发注册/登录支持 > 100 QPS

### 安全验收
- [ ] 验证码无法暴力破解
- [ ] 频率限制有效防刷
- [ ] 无SQL注入/XSS漏洞

---

**文档版本：** v1.0  
**创建日期：** 2024年  
**最后更新：** 2024年

