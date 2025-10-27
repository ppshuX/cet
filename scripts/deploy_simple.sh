#!/bin/bash
# 简单部署脚本 - Vue作为Django静态文件

set -e
echo "🚀 开始部署..."

# 1. 构建Vue
echo "[1/3] 构建Vue前端..."
cd cetapp/web
npm run build
cd ../..

# 2. 收集静态文件
echo "[2/3] 收集静态文件..."
python manage.py collectstatic --noinput

# 3. 重启Django
echo "[3/3] 重启Django..."
if command -v supervisorctl &> /dev/null; then
    sudo supervisorctl restart cet
else
    pkill -9 uwsgi || true
    sleep 1
    uwsgi --ini scripts/uwsgi.ini --daemonize /tmp/uwsgi.log
fi

echo "✅ 部署完成！"
echo "访问：https://yourdomain.com/app/"

