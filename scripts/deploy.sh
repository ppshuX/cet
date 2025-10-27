#!/bin/bash

# Roamio 部署脚本
# Usage: ./deploy.sh

set -e

echo "开始部署 Roamio..."

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置变量
PROJECT_DIR="/var/www/roamio"
REPO_URL="<your-git-repo-url>"
DOMAIN="app7508.acapp.acwing.com.cn"
IP="47.121.137.60"
DB_NAME="roamio"
DB_USER="roamio_user"

# 检查是否为root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}请使用sudo运行此脚本${NC}"
    exit 1
fi

echo -e "${GREEN}步骤 1/8: 更新系统${NC}"
apt update && apt upgrade -y

echo -e "${GREEN}步骤 2/8: 安装依赖${NC}"
apt install -y python3 python3-pip python3-venv nginx git postgresql postgresql-contrib

echo -e "${GREEN}步骤 3/8: 配置数据库${NC}"
systemctl start postgresql
systemctl enable postgresql

# 创建数据库和用户
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;" || true
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD 'changeme';" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" || true

echo -e "${GREEN}步骤 4/8: 克隆项目${NC}"
if [ ! -d "$PROJECT_DIR" ]; then
    mkdir -p $PROJECT_DIR
    git clone $REPO_URL $PROJECT_DIR
else
    cd $PROJECT_DIR
    git pull
fi

echo -e "${GREEN}步骤 5/8: 创建虚拟环境${NC}"
cd $PROJECT_DIR
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

echo -e "${GREEN}步骤 6/8: 配置Django${NC}"
# 创建.env文件
cat > .env << EOF
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,$IP
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
EOF

# 修改settings.py
python << PYTHON_SCRIPT
import re

with open('roamio/settings.py', 'r') as f:
    content = f.read()

# 修改DEBUG
content = re.sub(r'^DEBUG = True', 'DEBUG = False', content, flags=re.MULTILINE)

# 添加ALLOWED_HOSTS
if 'ALLOWED_HOSTS' not in content:
    content = content.replace(
        'from pathlib import Path',
        'from pathlib import Path\nimport os\nfrom dotenv import load_dotenv\n\nload_dotenv()'
    )
    
    content += '''
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '$DB_NAME',
        'USER': '$DB_USER',
        'PASSWORD': 'changeme',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
'''

with open('roamio/settings.py', 'w') as f:
    f.write(content)
PYTHON_SCRIPT

echo -e "${GREEN}步骤 7/8: 运行迁移和构建前端${NC}"
python manage.py migrate
python manage.py collectstatic --noinput

cd web
npm install
npm run build
cd ..

echo -e "${GREEN}步骤 8/8: 配置Gunicorn和Nginx${NC}"

# 创建Gunicorn配置
cat > gunicorn_config.py << EOF
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
timeout = 60
max_requests = 1000
EOF

# 创建systemd服务
cat > /etc/systemd/system/roamio.service << EOF
[Unit]
Description=Roamio Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --config $PROJECT_DIR/gunicorn_config.py roamio.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 配置Nginx
cat > /etc/nginx/sites-available/roamio << EOF
server {
    listen 80;
    server_name $DOMAIN $IP;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias $PROJECT_DIR/media/;
        expires 30d;
    }
}
EOF

# 创建软链接
ln -sf /etc/nginx/sites-available/roamio /etc/nginx/sites-enabled/

# 设置权限
chown -R www-data:www-data $PROJECT_DIR/media
chmod -R 755 $PROJECT_DIR/media

# 测试Nginx配置
nginx -t

# 启动服务
systemctl daemon-reload
systemctl enable roamio
systemctl restart roamio
systemctl restart nginx

echo -e "${GREEN}部署完成！${NC}"
echo -e "${YELLOW}请访问: http://$DOMAIN${NC}"
echo -e "${YELLOW}请运行: python manage.py createsuperuser${NC}"

