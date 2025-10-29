#!/bin/bash

# Roamio 部署脚本
# 用于在云端服务器更新代码并重启服务

set -e  # 遇到错误时退出

echo "🚀 开始部署 Roamio..."

# 1. 进入项目目录
cd /home/acs/roamio

# 2. 备份当前代码
echo "📦 备份当前代码..."
git stash

# 3. 拉取最新代码
echo "📥 从 GitHub 拉取最新代码..."
git pull origin master

# 4. 收集静态文件
echo "📦 收集静态文件..."
python3 manage.py collectstatic --noinput

# 5. 检查数据库迁移（如果需要）
echo "🔄 检查数据库迁移..."
python3 manage.py migrate --noinput

# 6. 重启 uWSGI 服务
echo "🔄 重启 uWSGI 服务..."
sudo systemctl restart uwsgi

# 7. 检查 uWSGI 服务状态
echo "✅ 检查服务状态..."
sudo systemctl status uwsgi --no-pager

echo "✅ 部署完成！"
echo "🌐 访问地址: https://app7508.acapp.acwing.com.cn/"

