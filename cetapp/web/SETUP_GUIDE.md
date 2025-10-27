# 🚀 前端项目设置指南

## 📦 安装依赖

```bash
cd cetapp/web
npm install
```

这会安装以下依赖：
- **axios**: HTTP请求库
- **pinia**: 状态管理
- **vue-router**: 路由管理
- **bootstrap**: UI框架

## 🎯 启动开发服务器

```bash
npm run serve
```

访问: http://localhost:8080

## 📁 项目结构

```
cetapp/web/
├── public/              # 静态资源
├── src/
│   ├── api/             # ✅ API接口封装
│   │   ├── request.js   # axios配置
│   │   ├── auth.js      # 认证API
│   │   ├── trip.js      # 旅行API
│   │   ├── comment.js   # 评论API
│   │   └── user.js      # 用户API
│   ├── stores/          # ✅ Pinia状态管理
│   │   ├── index.js
│   │   └── user.js      # 用户状态
│   ├── views/           # ✅ 页面组件
│   │   ├── LoginView.vue        # 登录页面
│   │   ├── TripListView.vue     # 旅行列表
│   │   └── TripDetailView.vue   # 旅行详情
│   ├── router/          # ✅ 路由配置
│   ├── App.vue
│   └── main.js
├── vue.config.js        # ✅ Vue配置（代理）
└── package.json
```

## 🔗 后端API连接

### 开发环境
前端自动通过代理连接到后端：
- 前端: http://localhost:8080
- 后端: http://127.0.0.1:8000
- 代理配置在 `vue.config.js`

### 测试API连接

1. 启动Django后端:
```bash
cd ../../  # 回到项目根目录
python manage.py runserver
```

2. 启动Vue前端:
```bash
cd cetapp/web
npm run serve
```

3. 访问 http://localhost:8080，应该能看到旅行列表

## 📝 已实现的功能

### ✅ 用户认证
- 登录页面 `/login`
- Token自动管理
- 自动刷新token
- 登出功能

### ✅ 旅行列表
- 首页展示所有旅行
- 点击查看详情
- 响应式卡片布局

### ✅ 旅行详情
- 旅行信息展示
- 统计数据（浏览/点赞/评论）
- 点赞和打卡功能
- 评论列表
- 发表评论（管理员）
- 删除评论（权限控制）
- 图片/视频上传

## 🎨 自定义配置

### 修改API地址

编辑 `.env.development`:
```env
VUE_APP_API_BASE_URL=http://your-api-url/api/v1
```

### 修改代理设置

编辑 `vue.config.js`:
```javascript
devServer: {
  proxy: {
    '/api': {
      target: 'http://your-backend-url',
      changeOrigin: true
    }
  }
}
```

## 🏗️ 生产构建

```bash
npm run build
```

构建文件会输出到 `../static/vue/`，可以直接被Django服务。

## 📚 下一步开发

### 待实现功能
- [ ] 用户注册页面
- [ ] 个人中心页面
- [ ] 用户头像上传
- [ ] 更多旅行页面路由
- [ ] 搜索和筛选功能
- [ ] 分页功能
- [ ] 图片预览模态框
- [ ] 富文本编辑器

### 推荐的组件库
可以考虑引入UI组件库提升体验：
- **Element Plus**: https://element-plus.org/
- **Ant Design Vue**: https://antdv.com/
- **Naive UI**: https://www.naiveui.com/

## 🐛 常见问题

### 1. API 404错误
检查后端是否启动：`python manage.py runserver`

### 2. CORS跨域错误
确保Django的CORS配置正确，参考 `cet/settings.py`

### 3. Token过期
前端会自动处理401错误并跳转登录页

### 4. 图片/视频上传失败
- 检查文件大小限制
- 检查Django的MEDIA_ROOT配置
- 确保用户有管理员权限

## 💡 开发技巧

### 1. 使用Vue DevTools
安装浏览器扩展以调试Vue应用

### 2. API调试
使用浏览器开发者工具Network面板查看API请求

### 3. 状态管理
使用Pinia DevTools查看状态变化

## 📞 获取帮助

- 📖 查看 `docs/` 目录下的文档
- 🔍 检查浏览器控制台错误
- 📝 查看Django日志

---

**🎉 前端开发环境配置完成！开始愉快的开发吧！**

