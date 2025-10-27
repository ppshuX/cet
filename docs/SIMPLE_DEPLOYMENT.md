# ⚡ 简单部署指南

## 🎯 方案：Vue作为Django静态文件

**无需修改Nginx配置！** Vue构建后作为Django的静态文件，通过Django提供服务。

---

## 🚀 部署步骤（3步）

### 1. 构建Vue前端

```bash
cd cetapp/web
npm install  # 首次需要安装依赖
npm run build
```

构建产物会输出到 `cetapp/static/vue/` 目录。

### 2. 收集Django静态文件

```bash
cd ../..  # 回到项目根目录
python manage.py collectstatic --noinput
```

### 3. 重启Django服务

```bash
# 如果使用uWSGI
sudo supervisorctl restart cet

# 或者如果使用uwsgi命令
pkill -9 uwsgi
uwsgi --ini scripts/uwsgi.ini --daemonize /tmp/uwsgi.log
```

---

## 🌐 访问地址

部署成功后：

### 旧系统（Django HTML）
```
https://yourdomain.com/cetapp/trip/
https://yourdomain.com/accounts/login/
```

### 新系统（Vue SPA）
```
https://yourdomain.com/app/
```

访问 `/app/` 会加载Vue单页应用，所有静态资源（CSS/JS/图片）通过Django的 `/static/vue/` 提供。

---

## 📂 文件结构

```
cet/
├── cetapp/
│   ├── static/
│   │   └── vue/              # Vue构建产物
│   │       ├── index.html    # Vue应用入口
│   │       ├── assets/       # CSS/JS/图片
│   │       └── ...
│   └── web/
│       └── (Vue源码)
└── static/                   # collectstatic收集后的目录
    └── vue/                  # 生产环境从这里提供
```

---

## 🔧 配置说明

### Vue配置（`cetapp/web/vue.config.js`）

```javascript
{
  // 构建输出到Django的static目录
  outputDir: '../static/vue',
  
  // 静态资源通过Django提供
  publicPath: '/static/vue/'
}
```

### Django视图（`cetapp/views/base_views.py`）

```python
def vue_app(request):
    """提供Vue单页应用"""
    # 读取并返回 cetapp/static/vue/index.html
    return HttpResponse(html_content)
```

### URL路由（`cet/urls.py`）

```python
path('app/', views.vue_app, name='vue-app'),  # Vue应用
path('api/v1/', include('cetapp.api.urls')),  # API接口
```

---

## ✅ 优势

1. **无需修改Nginx** - 使用现有配置即可
2. **部署简单** - 3条命令完成部署
3. **向后兼容** - 老URL继续工作
4. **统一管理** - 所有静态文件通过Django管理

---

## 🔄 更新流程

每次修改Vue代码后：

```bash
# 1. 重新构建
cd cetapp/web
npm run build

# 2. 收集静态文件
cd ../..
python manage.py collectstatic --noinput

# 3. 重启Django
sudo supervisorctl restart cet
```

---

## 📊 开发 vs 生产

### 开发环境

```bash
# 终端1：启动Django
python manage.py runserver

# 终端2：启动Vue开发服务器
cd cetapp/web
npm run serve
```

访问：http://localhost:8080

### 生产环境

```bash
# 构建 + 部署
cd cetapp/web && npm run build
cd ../.. && python manage.py collectstatic --noinput
sudo supervisorctl restart cet
```

访问：https://yourdomain.com/app/

---

## 🆘 常见问题

### Q: 访问 `/app/` 显示404

**A:** 确保已构建Vue应用
```bash
cd cetapp/web
npm run build
ls ../static/vue/index.html  # 检查是否存在
```

### Q: 静态资源404（CSS/JS）

**A:** 运行collectstatic
```bash
python manage.py collectstatic --noinput
```

### Q: 修改Vue代码不生效

**A:** 需要重新构建和收集静态文件
```bash
cd cetapp/web && npm run build
cd ../.. && python manage.py collectstatic --noinput
sudo supervisorctl restart cet
```

### Q: API请求失败

**A:** 检查Django是否正常运行
```bash
ps aux | grep uwsgi
tail -f /tmp/uwsgi.log
curl http://127.0.0.1:8000/api/v1/trips/
```

---

## 📚 相关文档

- [API参数冲突修复](API_PARAMETER_CONFLICT_FIX.md)
- [静态文件访问修复](STATIC_FILES_FIX.md)
- [前端集成指南](FRONTEND_INTEGRATION_COMPLETE.md)

---

**就这么简单！不需要修改Nginx，不需要复杂配置。** ✨

