# 用户认证系统说明

## 概述
已将注册和登录界面统一放到cetapp应用中，提供了更好的用户体验和代码组织。

## 新的URL结构

### 独立页面
- **注册页面**: `/cetapp/register/`
- **登录页面**: `/cetapp/login/`
- **登出功能**: `/cetapp/logout/`

### 统一认证页面
- **统一认证页面**: `/cetapp/auth/` (推荐使用)

## 功能特点

### 1. 统一认证页面 (`/cetapp/auth/`)
- 在一个页面中提供登录和注册功能
- 使用标签页切换，用户体验更好
- 响应式设计，支持移动端
- 统一的Bootstrap样式

### 2. 独立页面
- 注册页面：`/cetapp/register/`
- 登录页面：`/cetapp/login/`
- 登出功能：`/cetapp/logout/`
- 保持原有的独立功能

### 3. 中文界面
- 所有表单字段标签都使用中文
- 错误提示信息使用中文
- 用户友好的中文界面

## 文件结构

```
cetapp/
├── templates/
│   └── cetapp/
│       ├── auth.html          # 统一认证页面
│       ├── login.html         # 独立登录页面
│       └── register.html      # 独立注册页面
├── forms.py                   # 自定义表单（中文标签）
├── views.py                   # 包含认证视图函数
└── urls.py                    # 包含认证URL配置
```

## 视图函数

### `auth_view(request)`
- 渲染统一认证页面
- 提供注册和登录表单

### `login_view(request)`
- 处理用户登录
- 登录成功后跳转到 `/cetapp/trip1/`

### `register(request)`
- 处理用户注册
- 注册成功后自动登录并跳转到 `/cetapp/trip1/`

### `logout_view(request)`
- 处理用户登出
- 登出后跳转到 `/cetapp/auth/`

## 表单特点

### CustomLoginForm
- 用户名字段：中文标签"用户名"
- 密码字段：中文标签"密码"
- 中文错误提示信息
- Bootstrap样式

### CustomRegisterForm
- 用户名字段：中文标签"用户名"
- 密码字段：中文标签"密码"
- 确认密码字段：中文标签"确认密码"
- 中文错误提示信息
- Bootstrap样式

## 样式特点

- 使用Bootstrap 5框架
- 响应式设计，适配移动端
- 统一的卡片式布局
- 现代化的UI设计
- 完全中文化的用户界面

## 使用方法

1. **推荐使用统一认证页面**：
   - 访问 `/cetapp/auth/`
   - 在标签页中切换登录/注册

2. **使用独立页面**：
   - 注册：访问 `/cetapp/register/`
   - 登录：访问 `/cetapp/login/`
   - 登出：访问 `/cetapp/logout/`

## 注意事项

- 已移除Django默认的认证URL配置
- 所有认证功能现在都在cetapp应用中
- 登录/注册成功后都会跳转到trip1页面
- 登出后会跳转到统一认证页面
- 保持了原有的表单验证和错误处理
- 所有界面元素都使用中文 