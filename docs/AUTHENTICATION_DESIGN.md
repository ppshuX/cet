# 认证设计说明

## 🎯 设计原则

**统一使用 JWT 认证，避免 CSRF 问题**

## 📊 认证架构

### 1. API 认证（JWT）

```python
# REST Framework 配置
DEFAULT_AUTHENTICATION_CLASSES = [
    'rest_framework_simplejwt.authentication.JWTAuthentication',
]

# ✅ 优点：
# - 无状态认证，服务器无需存储 session
# - 不需要 CSRF token
# - 支持多设备同时登录
# - 易于扩展（微服务架构友好）
```

**使用场景：**
- ✅ Vue 前端登录
- ✅ 移动端 API 调用
- ✅ 所有 REST API 请求

### 2. Django Admin 认证（Session + CSRF）

```python
# CSRF 仅用于 Django Admin
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = [...]
```

**使用场景：**
- ✅ Django Admin 后台（`/admin/`）
- ✅ 表单提交（如果有）

## 🔐 认证流程

### API 登录流程

```javascript
// 1. 前端请求登录
POST /api/v1/auth/login/
{
  "username": "alice",
  "password": "password123"
}

// 2. 后端返回 JWT
{
  "access": "eyJhbGc...",  // Access Token (1天)
  "refresh": "eyJhbGc...", // Refresh Token (7天)
  "user": {...}
}

// 3. 前端存储 token
localStorage.setItem('access_token', data.access)
localStorage.setItem('refresh_token', data.refresh)

// 4. 后续请求携带 token
Authorization: Bearer eyJhbGc...
```

### JWT Token 结构

```python
# Access Token - 短期有效
{
  "token_type": "access",
  "exp": 1234567890,  # 1天后过期
  "jti": "token-id",
  "user_id": 1
}

# Refresh Token - 长期有效
{
  "token_type": "refresh",
  "exp": 1234567890,  # 7天后过期
  "jti": "token-id",
  "user_id": 1
}
```

## 🛡️ 安全特性

### 1. Token 黑名单

```python
# 登出时将 token 加入黑名单
@action(detail=False, methods=['post'])
def logout(self, request):
    refresh_token = request.data.get('refresh')
    if refresh_token:
        token = RefreshToken(refresh_token)
        token.blacklist()  # ✨ 加入黑名单
```

**工作原理：**
- 用户登出 → token 加入 `BlacklistedToken` 表
- 后续请求验证 token 是否在黑名单中
- 在黑名单 → 拒绝访问
- 不在黑名单 → 允许访问

### 2. Token 轮换

```python
SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,    # 刷新时返回新 token
    'BLACKLIST_AFTER_ROTATION': True,  # 旧 token 自动加入黑名单
}
```

**优势：**
- ✅ 每次刷新都生成新 token
- ✅ 旧 token 自动失效
- ✅ 防止 token 被盗用

### 3. 多标签页支持

**问题：** Session 认证在多个标签页中共享 cookie，可能导致 CSRF 冲突

**解决方案：** JWT 认证，每个标签页独立存储 token

```javascript
// 每个标签页独立管理 token
localStorage.getItem('access_token')  // 互不干扰
```

## 📈 对比分析

| 特性 | JWT 认证 ✅ | Session 认证 ❌ |
|------|------------|----------------|
| CSRF 防护 | 不需要 | 需要 |
| 多标签页 | ✅ 支持 | ❌ 可能冲突 |
| 跨域支持 | ✅ 简单 | ❌ 复杂 |
| 扩展性 | ✅ 无状态 | ❌ 需要共享存储 |
| 手机端 | ✅ 原生支持 | ⚠️ 需要 cookie |

## 🚀 未来优化

### 1. 实现 Token 刷新自动化

```javascript
// 前端自动刷新 token
interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      // Access token 过期，使用 refresh token 刷新
      const refresh = localStorage.getItem('refresh_token')
      const { data } = await refreshToken(refresh)
      localStorage.setItem('access_token', data.access)
      // 重试原请求
      return axios.request(error.config)
    }
    return Promise.reject(error)
  }
)
```

### 2. 双因子认证（2FA）

```python
# 发送验证码
send_verification_code(user.phone)

# 验证登录
if validate_code(code):
    # 生成 JWT
    return generate_jwt(user)
```

### 3. OAuth 社交登录

```python
# GitHub 登录
@action(detail=False, methods=['post'])
def github_login(self, request):
    code = request.data.get('code')
    # 交换 access token
    # 获取用户信息
    # 生成 JWT
```

## 📝 总结

**核心原则：**
1. ✅ API 统一使用 JWT 认证
2. ✅ Admin 保留 Session 认证（Django 默认）
3. ✅ 不需要为 API 配置 CSRF
4. ✅ 支持多标签页同时登录

**这样做的好处：**
- 🔒 更安全：无状态认证，token 可撤销
- 🚀 更快速：不需要查询数据库验证 session
- 📱 更兼容：支持 Web、移动端、API
- 🌐 更灵活：易于微服务拆分

