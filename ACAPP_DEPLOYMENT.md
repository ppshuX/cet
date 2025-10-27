# ACApp平台部署指南

## 服务器信息
- **IP**: 47.121.137.60
- **域名**: https://app7508.acapp.acwing.com.cn/
- **应用ID**: 7508

## 快速开始

### 1. 连接到服务器

```bash
ssh acs@47.121.137.60
```

### 2. 项目结构

```
/home/acs/
  └── roamio/          # 项目根目录
      ├── roamio/      # Django设置
      ├── trips/       # 应用代码
      ├── web/         # Vue前端
      ├── media/       # 用户上传的媒体文件
      ├── staticfiles/ # 静态文件（npm run build后）
      └── db.sqlite3   # 数据库
```

### 3. 首次部署

```bash
# 1. 进入项目目录
cd /home/acs/roamio

# 2. 创建虚拟环境（如果还没有）
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 4. 配置Django
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# 5. 构建前端
cd web
npm install
npm run build
cd ..

# 6. 启动服务
# 使用现有的uwsgi配置，或使用scripts/deploy_acapp.sh
```

### 4. 使用自动化脚本

```bash
chmod +x scripts/deploy_acapp.sh
./scripts/deploy_acapp.sh
```

### 5. 配置uWSGI（推荐）

使用项目根目录下的 `scripts/uwsgi.ini` 配置：

```bash
# 启动uWSGI
cd /home/acs/roamio
source venv/bin/activate
uwsgi --ini scripts/uwsgi.ini --daemonize

# 或者使用systemd服务
sudo systemctl start roamio
sudo systemctl enable roamio
```

### 6. 配置Nginx

ACApp平台已配置好Nginx，通常配置文件在：
```
/etc/nginx/nginx.conf
```

确认配置包含：

```nginx
server {
    listen 443 ssl;
    server_name app7508.acapp.acwing.com.cn;

    # SSL证书（ACApp提供）
    ssl_certificate /etc/nginx/ssl/cert.crt;
    ssl_certificate_key /etc/nginx/ssl/cert.key;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/acs/roamio/staticfiles/;
        expires 30d;
    }

    location /media/ {
        alias /home/acs/roamio/media/;
        expires 30d;
    }
}
```

## 日常更新

### 更新代码

```bash
cd /home/acs/roamio
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
cd web && npm run build && cd ..
systemctl restart roamio
```

## 重要配置说明

### 1. 数据库
- **开发环境**: SQLite (`db.sqlite3`)
- **生产环境**: 可切换到PostgreSQL

切换数据库，修改 `roamio/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'roamio',
        'USER': 'acs',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 2. 静态文件和媒体文件

确保 `roamio/settings.py` 中配置正确：

```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
```

### 3. 安全设置

**生产环境必须修改**:

1. 更改 `SECRET_KEY`:
```python
# roamio/settings.py
SECRET_KEY = os.getenv('SECRET_KEY', 'your-new-secret-key-here')
```

2. 设置 `DEBUG = False`:
```python
DEBUG = False
```

3. 配置ALLOWED_HOSTS（已完成）:
```python
ALLOWED_HOSTS = ['47.121.137.60', 'app7508.acapp.acwing.com.cn', '127.0.0.1', 'localhost']
```

## 常用命令

```bash
# 查看日志
tail -f /home/acs/roamio/uwsgi.log
journalctl -u roamio -f

# 重启服务
systemctl restart roamio
sudo nginx -s reload

# 数据库备份
python manage.py dumpdata > backup.json

# 数据库恢复
python manage.py loaddata backup.json
```

## 故障排查

### 1. 502 Bad Gateway
检查uWSGI是否运行：
```bash
ps aux | grep uwsgi
systemctl status roamio
```

### 2. 静态文件404
重新收集静态文件：
```bash
python manage.py collectstatic --noinput
```

### 3. 媒体文件权限
```bash
chmod -R 755 /home/acs/roamio/media
```

### 4. 端口冲突
检查8000端口占用：
```bash
lsof -i :8000
netstat -tulnp | grep 8000
```

## 性能优化建议

1. **使用PostgreSQL**替代SQLite（生产环境）
2. **启用Redis缓存**（可选）
3. **配置CDN**（如果使用云存储）
4. **使用uWSGI进程池**（已配置）

## 备份策略

```bash
# 创建备份脚本
cat > /home/acs/backup_roamio.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/acs/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# 备份数据库
python manage.py dumpdata > $BACKUP_DIR/db_$DATE.json

# 备份media目录
tar -czf $BACKUP_DIR/media_$DATE.tar.gz media/

# 保留最近7天的备份
find $BACKUP_DIR -name "*.json" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
EOF

chmod +x /home/acs/backup_roamio.sh
```

添加到crontab:
```bash
crontab -e
# 每天凌晨2点备份
0 2 * * * /home/acs/roamio/backup_roamio.sh
```

## 联系支持

如遇到问题，请检查：
1. Nginx错误日志: `/var/log/nginx/error.log`
2. uWSGI日志: `/home/acs/roamio/uwsgi.log`
3. Django日志: 检查 `LOGGING` 配置

