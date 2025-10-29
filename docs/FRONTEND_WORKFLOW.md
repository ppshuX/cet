# 前端工作流程说明

## 🔄 两种开发模式

### 模式 1：开发模式（开发时推荐）

```bash
# 终端1：启动 Django 后端
python manage.py runserver

# 终端2：启动 Vue 前端开发服务器
cd web
npm run serve
```

**工作流程：**
- Vue 开发服务器运行在 `http://localhost:8080`
- Django API 运行在 `http://localhost:8000`
- 开发服务器通过 proxy 代理 API 请求到 8000 端口
- **修改 Vue 代码立即生效（热重载）** ✅
- 不需要手动 build

**优点：**
- ⚡ 修改代码立即看到效果
- 🔥 热重载，无需手动刷新
- 🐛 更好的调试体验

**缺点：**
- 需要运行两个服务器
- 占用两个端口

### 模式 2：生产模式（当前使用的）

```bash
# 步骤1：构建 Vue 应用
cd web
npm run build

# 步骤2：Django 自动服务构建后的文件
python manage.py runserver
```

**工作流程：**
- 构建后的文件放在 `static/vue/` 目录
- Django 在 `http://localhost:8000` 服务所有内容
- 访问 `http://localhost:8000` → Django 返回 Vue 应用
- **修改 Vue 代码后必须重新 build** ⚠️

**优点：**
- 只需要一个服务器
- 更接近生产环境
- 可以测试 Django 的路由和静态文件服务

**缺点：**
- 每次修改都要 build
- 构建需要时间（15-20秒）
- 不会自动热重载

## 📂 文件结构

```
roamio/
├── web/                    # Vue 源代码（开发时修改）
│   ├── src/
│   │   ├── views/
│   │   │   └── UserCenterView.vue  ← 你修改这里
│   │   ├── api/
│   │   └── ...
│   └── package.json
│
└── static/vue/            # 构建后的文件（Django 实际服务）
    ├── index.html
    ├── assets/
    │   ├── js/
    │   │   ├── app.xxx.js       ← 编译后的JS
    │   │   └── ...
    │   └── css/
    │       └── ...
    └── ...
```

## 🔄 完整工作流程

### 开发时：

1. **修改源代码**
   ```bash
   # 修改 web/src/views/UserCenterView.vue
   ```

2. **构建前端**
   ```bash
   cd web
   npm run build
   # 这会将构建产物输出到 ../static/vue/
   ```

3. **重启或刷新**
   - Django 开发服务器会自动检测文件变化
   - 浏览器清除缓存并刷新页面（Ctrl + F5）

### 为什么需要 build？

**简单回答：**
Django 无法直接运行 `.vue` 文件，需要先将它们编译成浏览器能理解的 `.html`、`.js`、`.css`。

**详细解释：**

```javascript
// web/src/views/UserCenterView.vue (源代码)
<template>
  <div>{{ username }}</div>
</template>

<script>
export default {
  data() {
    return { username: 'alice' }
  }
}
</script>
```

↓ build 后变成 ↓

```javascript
// static/vue/assets/js/app.xxx.js (编译后)
function render() {
  return createElement('div', user.username)
}
// ... 浏览器能运行的纯 JavaScript
```

## 🎯 推荐开发流程

### 当前阶段（快速修改）

如果你要频繁修改界面：

```bash
# 打开两个终端

# 终端1：Django（保持不变）
python manage.py runserver

# 终端2：Vue 开发服务器（新开一个）
cd web
npm run serve
```

然后访问：`http://localhost:8080/user/center`

**这样修改代码立即生效，不需要 build！**

### 部署到生产（偶尔）

```bash
# 构建一次
cd web
npm run build

# 然后访问
http://127.0.0.1:8000/user/center
```

## 📊 对比表

| 特性 | 开发模式 (8080) | 生产模式 (8000) |
|------|----------------|----------------|
| 访问地址 | `http://localhost:8080` | `http://127.0.0.1:8000` |
| 热重载 | ✅ 自动 | ❌ 需要手动 |
| 修改生效 | ⚡ 立即 | ⏳ 需要build |
| build | ❌ 不需要 | ✅ 必需 |
| 服务器 | 2个（Django + Vue） | 1个（Django） |
| 调试 | 🐛 更好 | ⚠️ 一般 |

## 🚀 何时使用哪种？

### 使用开发模式（8080）当：
- ✅ 频繁修改界面
- ✅ 需要快速看到效果
- ✅ 调试样式问题
- ✅ 测试新功能

### 使用生产模式（8000）当：
- ✅ 测试完整用户流程
- ✅ 验证 Django 路由
- ✅ 模拟生产环境
- ✅ 性能测试
- ✅ 准备部署

## 💡 总结

**为什么需要 build？**

因为 Django 无法运行 `.vue` 文件，必须：
1. 将 Vue 组件编译成纯 JavaScript
2. 打包所有依赖
3. 输出到静态文件目录
4. Django 服务这些静态文件

**解决方案：**

当前可以使用开发模式快速开发：
```bash
npm run serve  # 在 web/ 目录下
# 然后访问 http://localhost:8080
# 修改代码立即生效，无需build！
```

