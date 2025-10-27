# 🚀 快速开始：前后端分离实战

## ⚡ 快速上手指南

### 第一步：安装依赖

```bash
# 安装后端依赖
pip install -r requirements_api.txt

# 创建数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser
```

### 第二步：启动后端服务

```bash
# 运行Django开发服务器
python manage.py runserver

# 访问API文档
# Swagger文档: http://127.0.0.1:8000/api/docs/
# ReDoc文档:   http://127.0.0.1:8000/api/redoc/
```

### 第三步：测试API

#### 1. 用户注册

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "test1234",
    "password2": "test1234",
    "email": "test@example.com"
  }'
```

响应:
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "date_joined": "2025-10-27T12:00:00",
    "profile": {
      "avatar": null,
      "avatar_url": "/static/images/default_avatar.png"
    }
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 2. 用户登录

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "test1234"
  }'
```

#### 3. 获取旅行列表

```bash
curl http://127.0.0.1:8000/api/v1/trips/
```

响应:
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "slug": "trip",
      "name": "厦门三天两晚游",
      "description": "探索厦门的植物园、鼓浪屿、八市美食",
      "stats": {
        "page": "trip",
        "views": 100,
        "likes": 50,
        "checked_in": false,
        "comments_count": 20
      }
    }
  ]
}
```

#### 4. 点赞旅行

```bash
curl -X POST http://127.0.0.1:8000/api/v1/trips/trip/like/
```

#### 5. 获取评论列表

```bash
curl "http://127.0.0.1:8000/api/v1/comments/?page=trip"
```

#### 6. 创建评论（需要认证且是管理员）

```bash
curl -X POST http://127.0.0.1:8000/api/v1/comments/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "page": "trip",
    "content": "很棒的旅行！"
  }'
```

---

## 🎨 前端项目搭建

### 方案一：Vue 3 + Vite（推荐）

```bash
# 创建Vue项目
npm create vite@latest frontend -- --template vue
cd frontend

# 安装依赖
npm install
npm install vue-router pinia axios
npm install element-plus
npm install @element-plus/icons-vue

# 启动开发服务器
npm run dev
```

#### 项目结构

```
frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── api/                    # API接口封装
│   │   ├── request.js          # axios封装
│   │   ├── auth.js             # 认证API
│   │   ├── trip.js             # 旅行API
│   │   ├── comment.js          # 评论API
│   │   └── user.js             # 用户API
│   ├── assets/                 # 静态资源
│   ├── components/             # 公共组件
│   │   ├── Header.vue
│   │   ├── Footer.vue
│   │   ├── CommentList.vue
│   │   └── CommentItem.vue
│   ├── views/                  # 页面组件
│   │   ├── Home.vue
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   ├── TripList.vue
│   │   ├── TripDetail.vue
│   │   └── UserCenter.vue
│   ├── router/                 # 路由配置
│   │   └── index.js
│   ├── store/                  # 状态管理
│   │   ├── index.js
│   │   └── modules/
│   │       ├── user.js
│   │       └── trip.js
│   ├── utils/                  # 工具函数
│   │   ├── auth.js
│   │   └── storage.js
│   ├── App.vue
│   └── main.js
├── .env.development            # 开发环境配置
├── .env.production             # 生产环境配置
├── package.json
└── vite.config.js
```

#### 关键配置文件

**.env.development**
```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
VITE_APP_TITLE=CET旅行平台
```

**vite.config.js**
```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  }
})
```

**src/api/request.js**
```javascript
import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => response.data,
  error => {
    const message = error.response?.data?.detail || '请求失败'
    ElMessage.error(message)
    
    // 401未授权，跳转登录
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/login'
    }
    
    return Promise.reject(error)
  }
)

export default request
```

**src/api/auth.js**
```javascript
import request from './request'

// 用户注册
export const register = (data) => {
  return request.post('/auth/register/', data)
}

// 用户登录
export const login = (data) => {
  return request.post('/auth/login/', data)
}

// 用户登出
export const logout = () => {
  const refresh = localStorage.getItem('refresh_token')
  return request.post('/auth/logout/', { refresh })
}

// 获取当前用户信息
export const getCurrentUser = () => {
  return request.get('/auth/me/')
}
```

**src/api/trip.js**
```javascript
import request from './request'

// 获取旅行列表
export const getTripList = (params) => {
  return request.get('/trips/', { params })
}

// 获取旅行详情
export const getTripDetail = (slug) => {
  return request.get(`/trips/${slug}/`)
}

// 点赞
export const likeTrip = (slug) => {
  return request.post(`/trips/${slug}/like/`)
}

// 打卡
export const checkinTrip = (slug) => {
  return request.post(`/trips/${slug}/checkin/`)
}

// 获取统计
export const getTripStats = (slug) => {
  return request.get(`/trips/${slug}/stats/`)
}

// 获取评论
export const getTripComments = (slug, params) => {
  return request.get(`/trips/${slug}/comments/`, { params })
}
```

**src/store/modules/user.js**
```javascript
import { defineStore } from 'pinia'
import { login, register, logout, getCurrentUser } from '@/api/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('access_token') || '',
    refreshToken: localStorage.getItem('refresh_token') || '',
    userInfo: null,
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token,
    username: (state) => state.userInfo?.username || '',
    avatar: (state) => state.userInfo?.profile?.avatar_url || '',
  },
  
  actions: {
    // 登录
    async login(credentials) {
      const { access, refresh, user } = await login(credentials)
      this.token = access
      this.refreshToken = refresh
      this.userInfo = user
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
    },
    
    // 注册
    async register(data) {
      const { access, refresh, user } = await register(data)
      this.token = access
      this.refreshToken = refresh
      this.userInfo = user
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
    },
    
    // 登出
    async logout() {
      try {
        await logout()
      } finally {
        this.token = ''
        this.refreshToken = ''
        this.userInfo = null
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      }
    },
    
    // 获取用户信息
    async getUserInfo() {
      if (!this.token) return
      const userInfo = await getCurrentUser()
      this.userInfo = userInfo
    },
  }
})
```

**src/views/Login.vue**
```vue
<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2>用户登录</h2>
      </template>
      
      <el-form
        :model="form"
        :rules="rules"
        ref="formRef"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="用户名"
            size="large"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            size="large"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            style="width: 100%"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
        
        <div class="links">
          <router-link to="/register">还没有账号？立即注册</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const handleLogin = async () => {
  await formRef.value.validate()
  
  loading.value = true
  try {
    await userStore.login(form)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error) {
    console.error('登录失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 400px;
}

.links {
  text-align: center;
  margin-top: 10px;
}

.links a {
  color: #409eff;
  text-decoration: none;
}
</style>
```

---

## 📝 总结

✅ **后端API已配置完成**
- Django REST Framework
- JWT认证
- CORS跨域
- API文档自动生成

✅ **前端项目结构设计完成**
- Vue 3 + Vite
- Pinia状态管理
- Axios HTTP封装
- Element Plus UI

🚀 **下一步:**
1. 按照上述步骤创建前端项目
2. 复制示例代码
3. 开始开发具体页面
4. 联调测试

💡 **提示:**
- API文档地址: http://127.0.0.1:8000/api/docs/
- 前端开发服务器: http://localhost:5173
- 后端API地址: http://127.0.0.1:8000/api/v1/

**🎉 恭喜！前后端分离改造的基础已经完成！**

