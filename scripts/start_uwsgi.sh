#!/bin/bash
cd /home/acs/roamio

echo "🔧 正在加载环境变量..."
set -a
source /home/acs/roamio/.env
set +a

echo "🚀 启动 uWSGI..."
uwsgi --ini /home/acs/roamio/scripts/uwsgi.ini --daemonize /home/acs/roamio/uwsgi.log

echo "✅ 启动完成，检查环境变量..."
sleep 2
cat /proc/$(pgrep -f uwsgi | head -n 1)/environ | tr '\0' '\n' | grep EMAIL

