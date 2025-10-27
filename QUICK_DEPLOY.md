# 快速部署指南

## 服务器端部署（最终版）

```bash
# 1. 连接到服务器
ssh acs@47.121.137.60

# 2. 进入项目目录
cd /home/acs/roamio

# 3. 更新代码（如果有新版本）
git pull origin master

# 4. 激活虚拟环境
source venv/bin/activate

# 5. 更新依赖（如有新增）
pip install -r requirements.txt

# 6. 运行数据库迁移
python manage.py migrate

# 7. 收集静态文件（确保前端文件在 staticfiles/）
python manage.py collectstatic --noinput

# 8. 如果有新的前端更改，需要重新构建
cd web
npm install
npm run build
cd ..

# 9. 重启服务
systemctl restart roamio
# 或
pkill -f uwsgi
uwsgi --ini scripts/uwsgi.ini --daemonize
```

## 项目结构说明

```
roamio/
├── roamio/           # Django设置（核心）
├── trips/            # Django应用（核心）
├── web/              # Vue源代码（开发用）
├── static/           # 前端构建产物（部署用）
│   └── vue/
│       ├── index.html    # 单页应用入口
│       └── assets/       # JS + CSS + 图片
│           ├── js/       # 压缩后的JS文件
│           ├── css/      # 压缩后的CSS文件
│           └── img/      # 图片资源
├── staticfiles/      # Django收集的静态文件（复制到 static/）
├── media/            # 用户上传的文件
├── db.sqlite3        # 数据库
└── scripts/
    ├── uwsgi.ini     # uWSGI配置
    └── deploy_acapp.sh
```

## 部署状态

### 已完成 ✅
- ✅ 前端已打包到 `static/vue/`
- ✅ 只有一个 `index.html` 入口
- ✅ JS/CSS 已压缩并优化
- ✅ 静态文件已收集到 `staticfiles/`
- ✅ uWSGI 配置已就绪

### 需要执行
1. 在服务器上运行 `python manage.py collectstatic`
2. 启动 uWSGI 服务
3. 配置 Nginx 反向代理

## 前端资源说明

### 当前结构（已优化）
```
static/vue/
├── index.html                    # 唯一HTML文件
├── favicon.ico                   # 网站图标
└── assets/
    ├── js/
    │   ├── chunk-vendors.js      # Vue框架（202KB）
    │   ├── app.js                # 应用代码（50KB）
    │   └── [动态路由].js         # 按需加载
    └── css/
        └── chunk-vendors.css     # 样式文件
```

### 为什么有这么多JS文件？
这是 Vue Router 的**代码分割**优化：
- 每个页面（路由）对应一个JS文件
- 用户访问时才加载对应的JS
- 减少首屏加载时间

### 可以合并吗？
理论上可以，但不推荐：
- ❌ 失去代码分割优势
- ❌ 首屏加载变慢
- ❌ 更新时需要重新下载整个应用

### 当前优化情况
- ✅ 已压缩（gzip）
- ✅ 已合并（chunk-vendors 包含所有依赖）
- ✅ 懒加载（路由级别）
- ✅ 浏览器缓存（文件名带hash）
- ✅ 生产环境已优化

## 性能优化建议

如果还想进一步优化：

1. **启用Gzip压缩**（Nginx配置）
```nginx
gzip on;
gzip_types text/css application/javascript image/svg+xml;
```

2. **CDN加速**（可选）
- 静态资源放到CDN
- 减少服务器压力

3. **PWA（可选）**
- 离线访问
- 提升用户体验

## 总结

**你的项目已经很优化了！**

- ✅ 前端已打包成单页应用
- ✅ 只有一个HTML入口
- ✅ JS/CSS已压缩
- ✅ 静态资源已组织好

**不需要进一步打包，直接部署即可！**

