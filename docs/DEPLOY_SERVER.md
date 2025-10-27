# 部署到服务器指南

## 服务器信息
- IP: 47.121.137.60
- 域名: https://app7508.acapp.acwing.com.cn/

## 部署步骤

### 1. 准备服务器环境

```bash
# 连接到服务器
ssh <user>@47.121.137.60

# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要的软件
sudo apt install -y python3 python3-pip python3-venv nginx git
sudo apt install -y postgresql postgresql-contrib  # 如果使用PostgreSQL
# 或者
sudo apt install -y mysql-server mysql-client      # 如果使用MySQL
```

### 2. 克隆项目

```bash
cd /path/to/your/projects
git clone <your-repo-url> roamio
cd roamio
```

### 3. 创建虚拟环境并安装依赖

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. 配置Django设置

创建 `.env` 文件：

```bash
cd /path/to/roamio
cat > .env << EOF
DJANGO_SETTINGS_MODULE=roamio.settings
SECRET_KEY=<your-secret-key>
DEBUG=False
ALLOWED_HOSTS=app7508.acapp.acwing.com.cn,47.121.137.60
DATABASE_URL=postgresql://user:password@localhost:5432/roamio
EOF
```

### 5. 配置数据库

```bash
# 如果使用PostgreSQL
sudo -u postgres psql
CREATE DATABASE roamio;
CREATE USER roamio_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE roamio TO roamio_user;
\q

# 如果使用MySQL
sudo mysql
CREATE DATABASE roamio CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'roamio_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON roamio.* TO 'roamio_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 6. 配置Django数据库

编辑 `roamio/settings.py`：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # 或 'mysql'
        'NAME': 'roamio',
        'USER': 'roamio_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['app7508.acapp.acwing.com.cn', '47.121.137.60']
```

### 7. 运行迁移

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 8. 构建前端

```bash
cd web
npm install
npm run build
cd ..
```

### 9. 配置Gunicorn

```bash
pip install gunicorn
```

创建 `gunicorn_config.py`：

```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
timeout = 60
max_requests = 1000
```

### 10. 配置Nginx

```bash
sudo nano /etc/nginx/sites-available/roamio
```

添加配置：

```nginx
server {
    listen 80;
    server_name app7508.acapp.acwing.com.cn 47.121.137.60;

    # 重定向到HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name app7508.acapp.acwing.com.cn;

    ssl_certificate /path/to/your/cert.crt;
    ssl_certificate_key /path/to/your/cert.key;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/roamio/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /path/to/roamio/media/;
        expires 30d;
    }
}
```

创建软链接并重启Nginx：

```bash
sudo ln -s /etc/nginx/sites-available/roamio /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 11. 配置Systemd服务

```bash
sudo nano /etc/systemd/system/roamio.service
```

添加内容：

```ini
[Unit]
Description=Roamio Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/roamio
Environment="PATH=/path/to/roamio/venv/bin"
ExecStart=/path/to/roamio/venv/bin/gunicorn \
    --config /path/to/roamio/gunicorn_config.py \
    roamio.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable roamio
sudo systemctl start roamio
sudo systemctl status roamio
```

### 12. 配置防火墙

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 维护命令

```bash
# 重启应用
sudo systemctl restart roamio

# 查看日志
sudo journalctl -u roamio -f

# 更新代码
cd /path/to/roamio
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
cd web && npm run build && cd ..
sudo systemctl restart roamio
```

## 常见问题

### 1. 媒体文件权限
```bash
sudo chown -R www-data:www-data /path/to/roamio/media
sudo chmod -R 755 /path/to/roamio/media
```

### 2. SSL证书
使用ACApp平台提供的SSL证书，路径通常在 `/etc/nginx/ssl/`

### 3. 静态文件
确保 `STATIC_ROOT` 设置在 `roamio/settings.py` 中：
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

## 开发环境vs生产环境

### 开发环境 (settings.py)
- `DEBUG = True`
- 使用SQLite数据库
- 开发服务器

### 生产环境 (需要创建 production_settings.py)
- `DEBUG = False`
- 使用PostgreSQL/MySQL
- Gunicorn + Nginx
- SSL证书
- 日志记录

