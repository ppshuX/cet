# 🚀 CET → Roamio 重命名指南

## 📝 概述

本指南将帮助你将项目从 **CET** (英语学习平台) 重命名为 **Roamio** (旅行平台)。

---

## ⚠️ 重要提示

**在执行以下步骤前，请先备份数据库和代码！**

```bash
# 备份数据库
copy db.sqlite3 db.sqlite3.backup

# 提交当前代码
git add .
git commit -m "备份：准备重命名为Roamio"
```

---

## 🔧 手动操作步骤

### 步骤 1: 重命名Django项目目录
```powershell
# 在项目根目录执行
Rename-Item -Path "cet" -NewName "roamio"
```

### 步骤 2: 重命名Django应用目录
```powershell
# 在项目根目录执行
Rename-Item -Path "cetapp" -NewName "trips"
```

### 步骤 3: 更新 manage.py
打开 `manage.py`，修改第9行：
```python
# 原来：
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cet.settings')

# 改为：
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roamio.settings')
```

### 步骤 4: 更新 roamio/settings.py
打开 `roamio/settings.py`，修改以下内容：

1. **第58行** - ROOT_URLCONF：
```python
# 原来：
ROOT_URLCONF = 'cet.urls'

# 改为：
ROOT_URLCONF = 'roamio.urls'
```

2. **第70行** - WSGI_APPLICATION：
```python
# 原来：
WSGI_APPLICATION = 'cet.wsgi.application'

# 改为：
WSGI_APPLICATION = 'roamio.wsgi.application'
```

3. **第45行** - INSTALLED_APPS（将 `cetapp` 改为 `trips`）：
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # 原来：'cetapp',
    'trips',  # ⭐ 修改这里
    
    # DRF相关
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
]
```

### 步骤 5: 更新 roamio/asgi.py
打开 `roamio/asgi.py`，修改第12行：
```python
# 原来：
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cet.settings')

# 改为：
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roamio.settings')
```

### 步骤 6: 更新 roamio/wsgi.py
打开 `roamio/wsgi.py`，修改第12行：
```python
# 原来：
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cet.settings')

# 改为：
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roamio.settings')
```

### 步骤 7: 更新 roamio/urls.py
打开 `roamio/urls.py`，修改import语句：
```python
# 原来：
from cetapp import views

# 改为：
from trips import views
```

修改urlpatterns：
```python
# 原来：
path('trips/', include('cetapp.urls')),
path('api/v1/', include('cetapp.api.urls')),

# 改为：
path('trips/', include('trips.urls')),
path('api/v1/', include('trips.api.urls')),
```

### 步骤 8: 更新 trips/apps.py
打开 `trips/apps.py`，修改：
```python
from django.apps import AppConfig

class TripsConfig(AppConfig):  # ⭐ 原来是 CetappConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trips'  # ⭐ 原来是 'cetapp'
```

### 步骤 9: 更新所有 trips/ 目录下的导入
使用查找替换功能：
- 查找：`from cetapp`
- 替换：`from trips`
- 作用范围：`trips/` 目录

### 步骤 10: 更新 uwsgi 配置
打开 `scripts/uwsgi.ini`，修改：
```ini
# 原来：
module = cet.wsgi

# 改为：
module = roamio.wsgi
```

---

## 🧪 测试步骤

### 1. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. 创建超级用户（如果需要）
```bash
python manage.py createsuperuser
```

### 3. 收集静态文件
```bash
python manage.py collectstatic --noinput
```

### 4. 运行开发服务器
```bash
python manage.py runserver
```

访问 `http://127.0.0.1:8000/` 查看是否正常。

### 5. 测试Vue前端
```bash
cd trips/web
npm run serve
```

访问 `http://localhost:8080/` 查看是否正常。

---

## 📦 更新Vue项目

### 1. 更新 package.json
打开 `trips/web/package.json`，修改：
```json
{
  "name": "roamio-web",
  "version": "1.0.0",
  "description": "Roamio 旅行平台前端",
  ...
}
```

### 2. 更新 vue.config.js
打开 `trips/web/vue.config.js`，修改路径（如果需要）：
```javascript
// 生产构建配置
outputDir: '../static/vue',  // 保持不变，因为trips/static/vue
```

### 3. 更新路由和组件中的标题
打开 `trips/web/src/router/index.js`，修改：
```javascript
router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'Roamio 旅行平台'  // ⭐ 修改默认标题
  ...
})
```

---

## 📝 更新文档

### 1. 更新 README.md
- 将所有 "CET" 替换为 "Roamio"
- 更新项目描述
- 更新项目名称

### 2. 更新其他文档
在 `docs/` 目录下的所有文档中：
- 查找：`cetapp`
- 替换：`trips`

---

## ✅ 验收清单

完成后，请确认以下项目：

- [ ] Django服务器能正常启动
- [ ] Vue前端能正常启动
- [ ] API接口能正常访问（/api/v1/）
- [ ] 登录功能正常
- [ ] 旅行列表页面正常
- [ ] 旅行详情页面正常
- [ ] 评论功能正常
- [ ] 用户中心功能正常
- [ ] Django Admin能正常访问
- [ ] 所有文档已更新

---

## 🎉 完成后

恭喜！你的项目已经成功从 **CET** 重命名为 **Roamio**！

下一步：
1. 提交代码到Git
2. 更新远程仓库
3. 重新部署到服务器

```bash
git add .
git commit -m "重构：将项目从CET重命名为Roamio"
git push origin master
```

---

**祝Roamio旅行平台越来越好！** 🚀✨

