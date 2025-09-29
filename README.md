# 🌟 旅行交流平台 (Travel Community Platform)

一个基于Django的旅行规划与分享平台，提供旅行记录、路线规划、社区交流等功能。支持图片和视频上传，具备智能压缩功能以优化存储。

## 📋 目录

- [功能特性](#-功能特性)
- [技术架构](#-技术架构)
- [快速开始](#-快速开始)
- [项目结构](#-项目结构)
- [页面功能](#-页面功能)
- [视频压缩功能](#-视频压缩功能)
- [部署指南](#-部署指南)
- [开发指南](#-开发指南)
- [API文档](#-api文档)
- [贡献指南](#-贡献指南)

## ✨ 功能特性

### 🎯 核心功能
- **旅行规划**：创建和管理多个旅行计划
- **社区交流**：用户评论、点赞、互动系统
- **媒体分享**：支持图片和视频上传与展示
- **智能压缩**：自动压缩媒体文件，优化存储空间
- **用户系统**：注册、登录、权限管理

### 🚀 技术亮点
- **响应式设计**：支持PC和移动端访问
- **实时更新**：AJAX实现无刷新交互
- **文件管理**：智能图片和视频压缩
- **模块化设计**：可扩展的页面架构
- **SEO友好**：良好的URL结构和页面标题

### 🎨 用户体验
- **现代UI**：Bootstrap框架，美观易用
- **即时反馈**：实时点赞、评论状态更新
- **媒体预览**：点击放大图片，内置视频播放器
- **背景音乐**：可选的氛围音乐播放

## 🏗️ 技术架构

### 后端技术栈
- **框架**：Django 5.0.6
- **数据库**：SQLite3 (可扩展至PostgreSQL/MySQL)
- **文件处理**：PIL (图片), MoviePy (视频)
- **身份认证**：Django Auth System

### 前端技术栈
- **UI框架**：Bootstrap 5
- **JavaScript**：原生JS + jQuery
- **样式**：CSS3 + 自定义样式
- **交互**：AJAX异步请求

### 媒体处理
- **图片压缩**：PIL自动调整尺寸和质量
- **视频压缩**：MoviePy智能压缩大于5MB的视频
- **文件存储**：本地文件系统 (可扩展至云存储)

## 🚀 快速开始

### 环境要求
- Python 3.8+
- pip
- Git

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd cet
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **数据库初始化**
```bash
python manage.py migrate
```

4. **创建超级用户** (可选)
```bash
python manage.py createsuperuser
```

5. **运行开发服务器**
```bash
python manage.py runserver
```

6. **访问应用**
打开浏览器访问：`http://127.0.0.1:8000`

### 快速体验
- 🏠 **主页**：`/` - 查看所有旅行计划
- 🏖️ **厦门旅行**：`/cetapp/trip/` - 厦门三天两晚游
- 🌊 **三岔河游**：`/cetapp/trip1/` - 一日游计划
- 🏔️ **曲靖之旅**：`/cetapp/trip2/` - 二日游行程
- 🌇 **长沙慢旅行**：`/cetapp/trip4/` - 三天两夜游 (支持视频上传)

## 📂 项目结构

```
cet/
├── 📁 cetapp/                 # 主应用
│   ├── 📁 migrations/         # 数据库迁移文件
│   ├── 📁 templates/          # HTML模板
│   │   └── 📁 cetapp/
│   │       ├── index.html     # 主菜单页面
│   │       ├── trip.html      # 厦门旅行页面
│   │       ├── trip1.html     # 三岔河一日游
│   │       ├── trip2.html     # 曲靖二日游
│   │       ├── trip3.html     # 通用模板页面
│   │       └── trip4.html     # 长沙旅行 (支持视频)
│   ├── models.py              # 数据模型
│   ├── views.py               # 视图函数
│   ├── urls.py                # URL路由
│   ├── forms.py               # 表单定义
│   └── utils.py               # 工具函数
├── 📁 media/                  # 媒体文件存储
│   ├── 📁 comment_images/     # 评论图片
│   └── 📁 comment_videos/     # 评论视频
├── 📁 static/                 # 静态文件
│   ├── 📁 css/                # 样式文件
│   ├── 📁 js/                 # JavaScript文件
│   ├── 📁 images/             # 静态图片
│   └── 📁 music/              # 背景音乐
├── 📁 templates/              # 全局模板
├── 📄 manage.py               # Django管理脚本
├── 📄 add_trip_page.py        # 新页面创建工具
├── 📄 README.md               # 项目说明文档
├── 📄 VIDEO_COMPRESSION_README.md  # 视频压缩说明
└── 📄 requirements.txt        # 依赖列表
```

## 🗺️ 页面功能

### 🏠 主菜单页面 (`/`)
- **旅行计划展示**：藤蔓式布局展示所有旅行计划
- **用户认证**：登录/注册入口
- **励志语录**：动态获取每日励志语录

### 🏖️ 厦门旅行页面 (`/cetapp/trip/`)
- **详细行程**：三天两晚完整旅行计划
- **景点介绍**：植物园、鼓浪屿、八市等
- **美食推荐**：沙茶面、海蛎煎等特色小吃
- **交通指南**：具体路线和时间安排

### 🌊 三岔河一日游 (`/cetapp/trip1/`)
- **自然风光**：龙凤寺、白水塘、紫溪湿地
- **徒步路线**：适合家庭和朋友结伴
- **拍照打卡**：最佳拍摄点推荐

### 🏔️ 曲靖二日游 (`/cetapp/trip2/`)
- **两日行程**：合理安排时间和路线
- **当地特色**：文化景点和自然风光
- **住宿推荐**：性价比高的住宿选择

### 🌇 长沙旅行页面 (`/cetapp/trip4/`) ⭐
- **慢旅行理念**：三天两夜深度体验
- **文化探索**：老街、博物馆、历史遗迹
- **美食之旅**：茶颜悦色、臭豆腐、糖油粑粑
- **视频分享**：支持上传和播放旅行视频
- **智能压缩**：自动压缩大于5MB的视频文件

### 🎨 通用功能 (所有页面)
- **评论系统**：用户可发表文字、图片、视频评论
- **点赞功能**：实时点赞统计和显示
- **浏览统计**：页面访问量统计
- **打卡功能**：旅行打卡记录
- **权限控制**：管理员可管理所有内容

## 🎬 视频压缩功能

### 🎯 功能特点
- **智能触发**：仅对大于5MB的视频进行压缩
- **质量优化**：720p分辨率，500kbps视频比特率
- **大幅压缩**：通常可将50MB视频压缩至3-8MB
- **自动处理**：上传即压缩，无需用户干预

### 📊 压缩效果

| 原始大小 | 压缩后大小 | 压缩率 | 说明 |
|---------|-----------|--------|------|
| 50MB    | 3-8MB     | 85-95% | 大文件显著压缩 |
| 30MB    | 2-5MB     | 85-95% | 中等文件有效压缩 |
| 10MB    | 2-3MB     | 70-85% | 小文件适度压缩 |
| 5MB     | 保持原样   | 0%     | 无需压缩 |

### 🔧 技术实现
- **库依赖**：MoviePy + FFmpeg
- **压缩策略**：分辨率调整 + 比特率控制
- **存储优化**：显著减少GitHub仓库大小
- **用户体验**：保持视频质量的同时加快加载速度

详细说明请参考：[VIDEO_COMPRESSION_README.md](VIDEO_COMPRESSION_README.md)

## 🚀 部署指南

### 开发环境部署

1. **克隆并进入项目**
```bash
git clone <repository-url>
cd cet
```

2. **安装Python依赖**
```bash
pip install django pillow moviepy python-dotenv
```

3. **初始化数据库**
```bash
python manage.py migrate
python manage.py createsuperuser  # 创建管理员账户
```

4. **收集静态文件** (生产环境)
```bash
python manage.py collectstatic
```

5. **运行服务器**
```bash
python manage.py runserver 0.0.0.0:8000
```

### 生产环境部署

#### 使用Nginx + uWSGI

1. **安装uWSGI**
```bash
pip install uwsgi
```

2. **配置uWSGI** (`scripts/uwsgi.ini`)
```ini
[uwsgi]
module = cet.wsgi:application
master = true
processes = 4
socket = /tmp/uwsgi.sock
chmod-socket = 666
vacuum = true
die-on-term = true
```

3. **配置Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /static/ {
        alias /path/to/cet/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/cet/media/;
    }
    
    location / {
        uwsgi_pass unix:/tmp/uwsgi.sock;
        include uwsgi_params;
    }
}
```

4. **启动服务**
```bash
uwsgi --ini scripts/uwsgi.ini
sudo systemctl restart nginx
```

### 环境变量配置

创建 `.env` 文件：
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## 🛠️ 开发指南

### 添加新的旅行页面

#### 方法1：使用自动化脚本 (推荐)
```bash
# 查看当前状态和建议
python add_trip_page.py

# 创建新页面
python add_trip_page.py trip5 "我的新旅行计划"
```

#### 方法2：手动添加

1. **创建视图函数** (`cetapp/views.py`)
```python
def trip5(request):
    return trip_page_generic(request, 'trip5')
```

2. **添加URL路由** (`cetapp/urls.py`)
```python
urlpatterns.extend(add_trip_page_urls('trip5'))
```

3. **创建HTML模板** (`cetapp/templates/cetapp/trip5.html`)
```python
from cetapp.utils import create_trip_page_template
content = create_trip_page_template('trip5', '我的新旅行计划')
# 将content保存为HTML文件
```

### 自定义样式和功能

1. **添加自定义CSS**
```css
/* 在模板中添加 */
<style>
    .custom-class {
        /* 你的样式 */
    }
</style>
```

2. **扩展JavaScript功能**
```javascript
// 添加自定义交互
document.addEventListener('DOMContentLoaded', function() {
    // 你的代码
});
```

3. **修改模型字段**
```python
# 在 cetapp/models.py 中修改
class Comment(models.Model):
    # 添加新字段
    new_field = models.CharField(max_length=100)
```

记得运行迁移：
```bash
python manage.py makemigrations
python manage.py migrate
```

### 代码质量和最佳实践

1. **遵循Django惯例**
   - 使用Django的内置功能
   - 遵循MVT模式
   - 合理使用中间件

2. **安全考虑**
   - 启用CSRF保护
   - 验证用户输入
   - 使用Django的权限系统

3. **性能优化**
   - 合理使用查询集
   - 启用缓存
   - 压缩静态文件

## 📚 API文档

### 评论相关API

#### 添加评论
```http
POST /cetapp/{page_name}/add_comment/
Content-Type: multipart/form-data

{
    "content": "评论内容",
    "image": "图片文件",
    "video": "视频文件"
}
```

#### 删除评论
```http
POST /cetapp/{page_name}/delete_comment/{comment_id}/
X-CSRFToken: [csrf_token]
```

#### 点赞页面
```http
POST /cetapp/{page_name}/like/
X-CSRFToken: [csrf_token]
```

#### 获取统计信息
```http
GET /cetapp/{page_name}/views_likes/

Response:
{
    "views": 123,
    "likes": 45
}
```

### 其他API

#### 获取励志语录
```http
GET /cetapp/get_quote/

Response:
{
    "content": "励志语录内容",
    "author": "作者"
}
```

## 🤝 贡献指南

### 如何参与贡献

1. **Fork项目**到你的GitHub账户
2. **创建功能分支**：`git checkout -b feature/amazing-feature`
3. **提交更改**：`git commit -m 'Add some amazing feature'`
4. **推送分支**：`git push origin feature/amazing-feature`
5. **创建Pull Request**

### 代码规范

1. **Python代码**
   - 遵循PEP 8标准
   - 使用有意义的变量名
   - 添加必要的注释

2. **HTML/CSS**
   - 保持代码整洁
   - 使用语义化标签
   - 遵循响应式设计原则

3. **JavaScript**
   - 使用ES6+语法
   - 避免全局变量污染
   - 添加错误处理

### 提交信息格式
```
类型: 简短描述

详细描述（如需要）

类型包括：
- feat: 新功能
- fix: 修复
- docs: 文档
- style: 格式
- refactor: 重构
- test: 测试
- chore: 构建过程或辅助工具的变动
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👥 作者

- **开发者**: J.Grigg
- **联系方式**: [GitHub](https://github.com/yourusername)

## 🙏 致谢

- Django框架团队
- Bootstrap UI框架
- MoviePy视频处理库
- 所有贡献者和用户

## 📝 更新日志

### v2.0.0 (2025-09-29)
- ✨ 新增视频上传和播放功能
- 🎬 实现智能视频压缩 (5MB阈值)
- 🎨 优化长沙旅行页面UI
- 📱 改进移动端适配

### v1.5.0 (2025-09-20)
- 🚀 重构页面管理系统
- 📄 添加自动化页面创建工具
- 🎯 优化评论和点赞功能
- 📚 完善文档和指南

### v1.0.0 (2025-09-01)
- 🎉 项目初始版本
- 🏠 基础页面和功能
- 👤 用户认证系统
- 💬 评论和互动功能

---

**🌟 如果这个项目对你有帮助，请给它一个Star！**

**🚀 开始你的旅行规划之旅吧！**
