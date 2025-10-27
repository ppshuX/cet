# 静态文件访问修复说明

## 🐛 问题描述

前端访问默认头像时出现404错误：
```
GET http://localhost:8080/static/images/default_avatar.png 404 (Not Found)
```

## 🔍 问题原因

前端尝试从Vue开发服务器（localhost:8080）访问静态文件，但该文件存在于Django后端（127.0.0.1:8000）。

## ✅ 解决方案

### 方案演进

#### ❌ 错误方案：硬编码后端地址
```javascript
// 这样会导致部署时需要修改所有URL
avatar: () => 'http://127.0.0.1:8000/static/images/default_avatar.png'
```

#### ✅ 正确方案：使用代理 + 环境变量

**核心思想**：
- 开发环境：通过Vue代理访问后端静态文件
- 生产环境：根据部署方式自动适配（同域/跨域）

### 实现细节

#### 1. Vue代理配置（`cetapp/web/vue.config.js`）

```javascript
devServer: {
  port: 8080,
  proxy: {
    // 代理API请求
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    },
    // 代理静态文件 ⭐
    '/static': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    },
    // 代理媒体文件 ⭐
    '/media': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    }
  }
}
```

#### 2. 统一配置管理（`cetapp/web/src/config/api.js`）

```javascript
/**
 * 获取API基础URL
 * - 开发环境：返回空字符串，使用相对路径（通过代理）
 * - 生产环境同域：返回空字符串，使用相对路径
 * - 生产环境跨域：返回配置的完整URL
 */
export const getApiBaseUrl = () => {
  return process.env.VUE_APP_API_BASE_URL || ''
}

/**
 * 获取完整URL
 */
export const getFullUrl = (path) => {
  if (!path) return null
  if (path.startsWith('http')) return path
  
  const baseUrl = getApiBaseUrl()
  return baseUrl ? baseUrl + path : path
}

/**
 * 获取头像URL
 */
export const getAvatarUrl = (avatarUrl) => {
  return getFullUrl(avatarUrl || '/static/images/default_avatar.png')
}
```

#### 3. 使用示例

**Pinia Store** (`cetapp/web/src/stores/user.js`):
```javascript
import { getAvatarUrl } from '@/config/api'

getters: {
  avatar: (state) => getAvatarUrl(state.userInfo?.profile?.avatar_url),
}
```

**Vue组件** (`TripDetailView.vue`):
```vue
<template>
  <img :src="getAvatarUrl(comment.user.profile?.avatar_url)" />
</template>

<script>
import { getAvatarUrl } from '@/config/api'

export default {
  setup() {
    return { getAvatarUrl }
  }
}
</script>
```

## 🌐 不同部署场景

### 场景1：开发环境

**前端**: http://localhost:8080  
**后端**: http://127.0.0.1:8000

**配置**: 无需配置，代理自动处理

**访问路径**:
```
http://localhost:8080/static/images/default_avatar.png
↓ (代理)
http://127.0.0.1:8000/static/images/default_avatar.png
```

---

### 场景2：生产环境 - 同域部署（推荐）

**前端**: https://yourdomain.com/static/vue/  
**后端**: https://yourdomain.com/api/  
**静态文件**: https://yourdomain.com/static/

**配置**: `.env.production.local`
```bash
VUE_APP_API_BASE_URL=
# 留空，使用相对路径
```

**访问路径**:
```
/static/images/default_avatar.png
↓ (相对路径)
https://yourdomain.com/static/images/default_avatar.png
```

---

### 场景3：生产环境 - 跨域部署

**前端**: https://www.yourdomain.com  
**后端**: https://api.yourdomain.com

**配置**: `.env.production.local`
```bash
VUE_APP_API_BASE_URL=https://api.yourdomain.com
```

**访问路径**:
```
/static/images/default_avatar.png
↓ (添加baseUrl)
https://api.yourdomain.com/static/images/default_avatar.png
```

**额外要求**: 
- Django需要配置CORS
- 后端需要允许跨域访问静态文件

## 🎯 最佳实践

### ✅ 推荐做法

1. **使用统一配置函数**
   ```javascript
   import { getAvatarUrl, getFullUrl } from '@/config/api'
   ```

2. **开发环境使用代理**
   - 不硬编码任何URL
   - 所有资源使用相对路径

3. **生产环境优先同域部署**
   - 无需配置环境变量
   - 无需处理CORS
   - 性能更好

### ❌ 避免做法

1. **硬编码后端地址**
   ```javascript
   // ❌ 不要这样做
   avatar: 'http://127.0.0.1:8000/static/...'
   ```

2. **在多处重复逻辑**
   ```javascript
   // ❌ 不要到处写URL处理逻辑
   // ✅ 统一使用 getFullUrl, getAvatarUrl
   ```

3. **忽略环境变量**
   ```javascript
   // ❌ 不要忽略 process.env.VUE_APP_API_BASE_URL
   ```

## 🔧 重启服务以应用更改

修改 `vue.config.js` 后需要重启Vue开发服务器：

```bash
# 停止当前服务 (Ctrl+C)
# 重新启动
cd cetapp/web
npm run serve
```

## ✅ 验证修复

### 1. 检查代理是否生效

访问前端并打开浏览器控制台，应该看到：
```
GET http://localhost:8080/static/images/default_avatar.png 200 (OK)
```

### 2. 检查头像是否显示

- 旅行详情页的评论区用户头像正常显示
- 未登录用户显示默认头像

### 3. 检查媒体文件

- 评论中的图片正常显示
- 评论中的视频正常播放

## 📚 相关文档

- [部署指南](DEPLOYMENT_GUIDE.md) - 详细的生产环境部署说明
- [API参数冲突修复](API_PARAMETER_CONFLICT_FIX.md) - 相关问题修复

---

**修复日期**: 2025-10-27  
**影响范围**: 所有静态资源和媒体文件访问  
**兼容性**: 开发/生产环境自动适配

