# 🌍 Roamio - 智能旅行规划平台

> **一个现代化的旅行规划与社区分享平台，采用前后端分离架构。**

**让每个旅行都成为难忘的回忆** ✈️🏖️🌄

---

## 📚 项目文档

详细的技术文档已整理到 [`docs/`](docs/) 目录：

### 🎯 开发指南
- **[阶段开发计划](docs/PHASE_PLAN.md)** ⭐⭐⭐ - 清晰的5阶段发展路线
- **[产品路线图](docs/PRODUCT_ROADMAP.md)** ⭐⭐ - 详细技术实现方案
- **[旅行页面指南](docs/TRIP_PAGES_GUIDE.md)** ⭐⭐ - 新增旅行页面方法
- **[自定义旅行指南](docs/CUSTOM_TRIP_GUIDE.md)** ⭐ - 个性化配置说明
- **[旅行内容指南](docs/TRIP_CONTENT_GUIDE.md)** ⭐ - 详细配置说明

### 🚀 快速开始
- **[立即部署](DEPLOY_NOW.md)** ⭐ - 一键部署指南
- **[API快速开始](docs/QUICK_START_API.md)** ⭐ - API使用指南
- **[简化部署](docs/SIMPLE_DEPLOYMENT.md)** ⭐ - 简单部署方案
- **[组件使用指南](web/src/components/COMPONENTS_GUIDE.md)** - Vue组件API文档

### 📖 技术文档
- **[项目结构](docs/PROJECT_STRUCTURE.md)** - 项目架构说明
- **[前端项目README](web/README.md)** - Vue项目详细说明
- **[认证系统](docs/AUTH_README.md)** - 用户认证文档
- **[视频压缩](docs/VIDEO_COMPRESSION_README.md)** - 视频压缩实现

---

## 🌟 核心功能

### ✈️ 旅行规划
- **可视化行程编辑器** - 拖拽式行程设计
- **模块化组件** - 自由组合行程模块（进度条、亮点、预算等）
- **智能预算计算** - 实时费用估算
- **行程分享** - 公开或私密分享

### 🤖 AI助手（规划中）
- **智能推荐目的地** - 根据预算和偏好推荐
- **自动生成行程** - AI帮你规划每日安排
- **实时优化建议** - 检测行程问题并给出建议

### 👥 社区互动
- **旅行广场** - 浏览他人的精彩行程
- **评论与点赞** - 与旅行者互动交流
- **打卡分享** - 实际旅行后的照片分享
- **用户关注** - 关注喜欢的旅行达人

### 📱 现代化体验
- **前后端分离** - Vue 3 + Django REST Framework
- **响应式设计** - 完美适配移动端和PC端
- **实时预览** - 编辑行程时即时查看效果
- **RESTful API** - 标准化接口设计

---

## 🛠️ 技术栈

### 后端
- **Django 5.2** - Python Web框架
- **Django REST Framework** - RESTful API
- **djangorestframework-simplejwt** - JWT认证
- **drf-spectacular** - API文档（Swagger/ReDoc）
- **Pillow** - 图片处理
- **moviepy** - 视频压缩

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **Vue Router** - 前端路由
- **Pinia** - 状态管理
- **Axios** - HTTP客户端
- **Bootstrap 5** - UI框架

### 数据库
- **SQLite** (开发环境)
- **PostgreSQL** (生产环境推荐)

### 部署
- **Nginx** - Web服务器
- **uWSGI** - Python应用服务器
- **Docker** (可选)

---

## 🚀 快速开始

### 前置要求
- Python 3.8+
- Node.js 14+
- pip & npm

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/roamio.git
cd roamio
```

### 2. 后端设置

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 创建超级用户
```bash
python manage.py createsuperuser
```

#### 初始化旅行数据（可选）
```bash
python init_trip_data.py
```

#### 运行开发服务器
```bash
python manage.py runserver
```

后端API将运行在 `http://127.0.0.1:8000/`

### 3. 前端设置

#### 安装依赖
```bash
cd web
npm install
```

#### 运行开发服务器
```bash
npm run serve
```

前端应用将运行在 `http://localhost:8080/`

#### 生产构建
```bash
npm run build
```

构建产物会输出到 `trips/static/vue/`

---

## 📂 项目结构

```
roamio/
├── roamio/               # Django项目配置
│   ├── settings.py       # 主配置文件
│   ├── urls.py          # 主URL路由
│   ├── wsgi.py          # WSGI入口
│   └── asgi.py          # ASGI入口
│
├── trips/               # 旅行应用（主应用）⭐
│   ├── models/          # 数据模型
│   │   ├── user_profile.py    # 用户资料
│   │   ├── comment.py         # 评论
│   │   └── site_stat.py       # 统计数据
│   │
│   ├── views/           # 视图函数
│   │   ├── auth_views.py      # 认证相关
│   │   ├── trip_views.py      # 旅行页面
│   │   ├── comment_views.py   # 评论管理
│   │   └── user_views.py      # 用户中心
│   │
│   ├── api/             # RESTful API
│   │   ├── serializers/       # 序列化器
│   │   ├── viewsets.py        # ViewSets
│   │   └── urls.py            # API路由
│   │
│   ├── templates/       # Django模板（向后兼容）
│   │   └── trips/       # 模板目录 ⭐
│   │       ├── index.html
│   │       ├── trip*.html
│   │       └── components/
│   │
│   ├── web/             # Vue前端项目
│   │   ├── src/
│   │   │   ├── views/         # 页面组件
│   │   │   ├── components/    # 可复用组件
│   │   │   ├── router/        # 路由配置
│   │   │   ├── stores/        # Pinia状态管理
│   │   │   ├── api/           # API封装
│   │   │   └── config/        # 配置文件
│   │   ├── public/
│   │   └── package.json
│   │
│   ├── migrations/      # 数据库迁移
│   └── static/          # 静态文件
│
├── media/               # 用户上传文件
│   ├── user_avatars/    # 用户头像
│   ├── comment_images/  # 评论图片
│   └── comment_videos/  # 评论视频
│
├── static/              # 收集的静态文件
├── docs/                # 项目文档
├── scripts/             # 部署脚本
├── manage.py            # Django管理脚本
├── requirements.txt     # Python依赖
└── README.md           # 项目说明
```

---

## 🔌 API接口

### 认证相关
```
POST   /api/v1/auth/register/          注册
POST   /api/v1/auth/login/             登录
POST   /api/v1/auth/logout/            登出
POST   /api/v1/auth/token/refresh/     刷新Token
```

### 旅行相关
```
GET    /api/v1/trips/                  旅行列表
GET    /api/v1/trips/{slug}/           旅行详情
POST   /api/v1/trips/{slug}/like/      点赞
POST   /api/v1/trips/{slug}/checkin/   打卡
```

### 评论相关
```
GET    /api/v1/comments/               评论列表（支持筛选）
POST   /api/v1/comments/               发表评论
DELETE /api/v1/comments/{id}/          删除评论
```

### 用户相关
```
GET    /api/v1/users/                  用户列表
GET    /api/v1/users/{id}/             用户详情
PATCH  /api/v1/users/{id}/             更新用户
```

完整API文档：访问 `/api/docs/`

---

## 🎨 特色功能

### 1. 智能图片压缩
- 用户上传头像自动压缩至200KB以下
- 评论图片自动压缩
- 保持图片质量的同时节省存储

### 2. 视频压缩
- 评论视频自动压缩
- 自动调整分辨率和码率
- 大幅减小视频文件体积

### 3. 配置驱动的内容
- 通过`tripConfig.js`轻松管理旅行内容
- 无需修改代码即可更新行程信息
- 支持模块化组件开关

### 4. 组件化设计
- 可复用的Vue组件
- `TripProgress` - 进度条组件
- `TripStats` - 统计组件
- `TripOverview` - 行程概览组件
- `CommentSection` - 评论区组件

---

## 🔒 安全性

- **JWT认证** - 安全的token认证机制
- **CORS配置** - 跨域请求控制
- **CSRF保护** - 防止跨站请求伪造
- **SQL注入防护** - Django ORM自动防护
- **XSS防护** - Vue自动转义

---

## 📈 性能优化

- **图片压缩** - 自动压缩用户上传的图片
- **视频压缩** - 智能压缩评论视频
- **静态文件CDN** - 支持CDN加速
- **API分页** - 避免一次加载过多数据
- **懒加载** - 路由级别的代码分割

---

## 🚀 部署指南

详细部署步骤请参考：
- **[立即部署](DEPLOY_NOW.md)**
- **[简化部署指南](docs/SIMPLE_DEPLOYMENT.md)**

### 快速部署步骤

1. **准备服务器**
   - Ubuntu 20.04+ / CentOS 7+
   - Python 3.8+
   - Nginx
   - uWSGI

2. **克隆代码**
   ```bash
   git clone https://github.com/yourusername/roamio.git
   cd roamio
   ```

3. **配置环境**
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic
   ```

4. **构建前端**
   ```bash
   cd web
   npm install
   npm run build
   ```

5. **配置Nginx和uWSGI**
   - 参考 `scripts/uwsgi.ini`
   - 配置Nginx反向代理

6. **启动服务**
   ```bash
   uwsgi --ini scripts/uwsgi.ini
   sudo systemctl restart nginx
   ```

---

## 🛠️ 开发指南

### 添加新的旅行页面

参考文档：[旅行页面指南](docs/TRIP_PAGES_GUIDE.md)

### 自定义旅行内容

参考文档：[自定义旅行指南](docs/CUSTOM_TRIP_GUIDE.md)

### 创建新组件

参考文档：[组件使用指南](web/src/components/COMPONENTS_GUIDE.md)

---

## 📊 数据模型

### UserProfile（用户资料）
- 用户头像
- 昵称
- 简介

### Comment（评论）
- 评论内容
- 评论图片
- 评论视频
- 所属旅行页面
- 评论用户

### SiteStat（统计数据）
- 页面浏览量
- 点赞数
- 打卡数
- 评论数

---

## 🤝 贡献指南

欢迎贡献代码、报告Bug、提出建议！

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

---

## 📄 开源协议

本项目采用 MIT 协议开源。

---

## 🙏 鸣谢

- **Django** - 强大的Python Web框架
- **Vue.js** - 渐进式JavaScript框架
- **Bootstrap** - 优秀的CSS框架
- **DRF** - Django REST Framework
- **所有贡献者** - 感谢你们的支持！

---

## 📞 联系方式

- **项目地址**: https://github.com/yourusername/roamio
- **问题反馈**: [Issues](https://github.com/yourusername/roamio/issues)
- **邮箱**: your.email@example.com

---

## 🗺️ 产品路线图

### 当前版本 v1.0 ✅
- ✅ 前后端分离架构
- ✅ 用户认证系统
- ✅ 旅行详情展示
- ✅ 评论互动功能
- ✅ 图片视频压缩
- ✅ **CET到Roamio重命名完成**

### v2.0 - 基础编辑器（规划中）
- [ ] 可视化行程编辑器
- [ ] 模块化组件选择
- [ ] 实时预览
- [ ] 草稿保存

### v3.0 - 模板市场（规划中）
- [ ] 官方模板库
- [ ] 旅行广场
- [ ] 模板复制
- [ ] 筛选搜索

### v4.0 - AI助手（规划中）
- [ ] AI推荐目的地
- [ ] AI生成行程
- [ ] 智能预算计算
- [ ] 实时优化建议

详细规划请参考：[产品路线图](docs/PRODUCT_ROADMAP.md)

---

**让Roamio陪你探索世界的每一个角落！** 🌍✨

**Built with ❤️ by the Roamio Team**
