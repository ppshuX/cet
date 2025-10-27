#!/bin/bash

# ACApp平台专用部署脚本
# Usage: ./deploy_acapp.sh

set -e

echo "🚀 开始部署 Roamio 到 ACApp 平台..."

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 配置变量（ACApp平台特有）
APP_ID="7508"
DOMAIN="app7508.acapp.acwing.com.cn"
SERVER_IP="47.121.137.60"
PROJECT_DIR="/home/acs/roamio"

echo -e "${YELLOW}注意：ACApp平台的特殊要求：${NC}"
echo "1. 使用官方提供的SSL证书"
echo "2. 前端通过 /static/ 访问静态资源"
echo "3. 媒体文件通过 /media/ 访问"
echo "4. 使用Gunicorn + Nginx反向代理"

read -p "继续部署? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

echo -e "${GREEN}步骤 1/7: 检查环境${NC}"
cd $PROJECT_DIR || exit 1

echo -e "${GREEN}步骤 2/7: 更新代码${NC}"
git pull origin master

echo -e "${GREEN}步骤 3/7: 激活虚拟环境并安装依赖${NC}"
source venv/bin/activate
pip install -r requirements.txt

echo -e "${GREEN}步骤 4/7: 配置数据库迁移${NC}"
python manage.py migrate

echo -e "${GREEN}步骤 5/7: 收集静态文件${NC}"
python manage.py collectstatic --noinput

echo -e "${GREEN}步骤 6/7: 构建前端${NC}"
cd web
npm install
npm run build
cd ..

echo -e "${GREEN}步骤 7/7: 重启服务${NC}"
systemctl restart roamio
systemctl restart nginx

echo -e "${GREEN}✅ 部署完成！${NC}"
echo -e "${YELLOW}请访问: https://${DOMAIN}${NC}"

