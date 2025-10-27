# 🎨 CET旅行平台 - Vue 3前端

基于Vue 3的现代化单页应用（SPA），与Django REST API后端完美对接。

---

## ⚡ 快速开始

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run serve

# 生产构建
npm run build
```

---

## 📁 项目结构

```
src/
├── api/                    # API接口封装
│   ├── request.js          # Axios配置（请求/响应拦截）
│   ├── auth.js             # 认证API
│   ├── trip.js             # 旅行API
│   ├── comment.js          # 评论API
│   ├── user.js             # 用户API
│   └── index.js            # 统一导出
│
├── stores/                 # Pinia状态管理
│   ├── index.js            # Pinia实例
│   └── user.js             # 用户状态（登录/登出/用户信息）
│
├── views/                  # 页面组件
│   ├── LoginView.vue       # 登录页面
│   ├── TripListView.vue    # 旅行列表页面
│   └── TripDetailView.vue  # 旅行详情页面
│
├── router/                 # 路由配置
│   └── index.js            # 路由定义和守卫
│
├── App.vue                 # 根组件
└── main.js                 # 应用入口
```

---

## 🔧 技术栈

- **Vue 3.2** - 渐进式JavaScript框架
- **Vue Router 4** - 官方路由管理器
- **Pinia 2.1** - 新一代状态管理
- **Axios 1.6** - HTTP客户端
- **Bootstrap 5** - CSS框架

---

## 🌐 API对接

### 开发环境
- 前端: http://localhost:8080
- 后端: http://127.0.0.1:8000
- 代理: 自动通过Vue CLI配置

### API Base URL
```javascript
// 开发环境（自动代理）
/api/v1

// 生产环境
http://your-domain.com/api/v1
```

---

## 📄 页面说明

### 1. 登录页面 (`/login`)
- 用户名/密码登录
- JWT Token管理
- 自动保存登录状态
- 登录后跳转首页

### 2. 旅行列表 (`/`)
- 展示所有旅行计划
- 卡片式布局
- 显示浏览量和点赞数
- 点击查看详情

### 3. 旅行详情 (`/trip/:slug`)
- 旅行完整信息
- 统计数据可视化
- 点赞和打卡功能
- 评论列表
- 发表评论（管理员）
- 图片/视频上传和展示

---

## 🔐 认证机制

### Token管理
```javascript
// 登录后自动保存
localStorage.setItem('access_token', token)
localStorage.setItem('refresh_token', refreshToken)

// 请求时自动携带
headers: { Authorization: `Bearer ${token}` }

// 401自动跳转登录页
```

### 用户状态
```javascript
import { useUserStore } from '@/stores'

const userStore = useUserStore()

// 登录
await userStore.login({ username, password })

// 登出
await userStore.logout()

// 检查登录状态
userStore.isLoggedIn

// 获取用户信息
userStore.userInfo
userStore.username
userStore.avatar
```

---

## 🚀 开发指南

### 添加新页面

1. **创建Vue组件**
```vue
<!-- src/views/NewPage.vue -->
<template>
  <div>New Page</div>
</template>

<script>
export default {
  name: 'NewPage'
}
</script>
```

2. **添加路由**
```javascript
// src/router/index.js
{
  path: '/new',
  name: 'new',
  component: () => import('@/views/NewPage.vue')
}
```

### 调用API

```javascript
import { getTripList } from '@/api/trip'

// 在组件中使用
const fetchData = async () => {
  try {
    const data = await getTripList()
    console.log(data)
  } catch (error) {
    console.error(error)
  }
}
```

### 使用状态管理

```javascript
import { useUserStore } from '@/stores'

export default {
  setup() {
    const userStore = useUserStore()
    
    return {
      username: userStore.username,
      isLoggedIn: userStore.isLoggedIn
    }
  }
}
```

---

## 🎨 样式定制

### Bootstrap自定义
项目使用Bootstrap 5，可以通过以下方式自定义：

1. **使用Bootstrap类**
```vue
<button class="btn btn-primary">按钮</button>
```

2. **自定义样式**
```vue
<style scoped>
.custom-class {
  /* 你的样式 */
}
</style>
```

---

## 🔧 配置说明

### vue.config.js
```javascript
{
  // 开发服务器配置
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',  // 后端地址
        changeOrigin: true
      }
    }
  },
  
  // 生产构建配置
  outputDir: '../static/vue',  // 构建到Django static目录
  publicPath: '/static/vue/'    // 资源路径前缀
}
```

---

## 🐛 调试技巧

### 1. 使用Vue DevTools
安装浏览器扩展以调试Vue应用

### 2. 查看Network请求
打开Chrome DevTools → Network查看API调用

### 3. 查看Console日志
所有错误都会输出到控制台

### 4. 查看Pinia状态
使用Pinia DevTools查看状态变化

---

## 📦 构建部署

### 开发构建
```bash
npm run build
```

构建文件输出到 `../static/vue/`

### Django集成
构建后的文件可以直接被Django服务：

```python
# Django settings.py
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
```

访问: http://your-domain.com/static/vue/index.html

---

## ✅ 功能清单

### 已实现
- [x] 用户登录
- [x] 旅行列表展示
- [x] 旅行详情查看
- [x] 点赞功能
- [x] 打卡功能
- [x] 评论列表
- [x] 发表评论（含图片/视频）
- [x] 删除评论
- [x] Token自动管理
- [x] 401自动跳转
- [x] 响应式布局

### 待实现
- [ ] 用户注册
- [ ] 个人中心
- [ ] 头像上传
- [ ] 评论分页
- [ ] 搜索功能
- [ ] 筛选功能
- [ ] 图片预览
- [ ] Toast提示

---

## 📚 参考资源

- [Vue 3文档](https://vuejs.org/)
- [Pinia文档](https://pinia.vuejs.org/)
- [Vue Router文档](https://router.vuejs.org/)
- [Axios文档](https://axios-http.com/)
- [Bootstrap文档](https://getbootstrap.com/)

---

## 🆘 需要帮助？

1. 查看 [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. 查看 [完整文档](../../docs/)
3. 检查浏览器控制台错误
4. 查看Django日志

---

**Happy Coding! 🚀**
