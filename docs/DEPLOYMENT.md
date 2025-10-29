# 云端部署指南

## 快速部署

### 方法一：使用自动化部署脚本（推荐）

在云端服务器上执行：

```bash
cd /home/acs/roamio
bash scripts/deploy.sh
```

### 方法二：手动部署

#### 1. SSH 登录到服务器

```bash
ssh acs@app7508.acapp.acwing.com.cn
```

#### 2. 进入项目目录并拉取代码

```bash
cd /home/acs/roamio
git pull origin master
```

#### 3. 收集静态文件

```bash
python3 manage.py collectstatic --noinput
```

#### 4. 执行数据库迁移（如果需要）

```bash
python3 manage.py migrate --noinput
```

#### 5. 重启 uWSGI 服务

```bash
sudo systemctl restart uwsgi
```

#### 6. 检查服务状态

```bash
sudo systemctl status uwsgi
```

#### 7. 查看日志

```bash
tail -f /home/acs/roamio/uwsgi.log
```

## 验证部署

部署完成后，访问以下地址验证：

- **前端地址**: https://app7508.acapp.acwing.com.cn/
- **API 文档**: https://app7508.acapp.acwing.com.cn/api/schema/swagger-ui/

## 常见问题

### 1. 服务启动失败

检查 uWSGI 配置：

```bash
sudo systemctl status uwsgi
```

查看完整日志：

```bash
cat /home/acs/roamio/uwsgi.log
```

### 2. 静态文件未更新

重新收集静态文件：

```bash
cd /home/acs/roamio
python3 manage.py collectstatic --noinput
sudo systemctl restart uwsgi
```

### 3. 代码更新后没有生效

确保重启了 uWSGI：

```bash
sudo systemctl restart uwsgi
```

查看重启日志：

```bash
sudo systemctl status uwsgi
```

## 服务管理命令

### 查看服务状态

```bash
sudo systemctl status uwsgi
```

### 重启服务

```bash
sudo systemctl restart uwsgi
```

### 停止服务

```bash
sudo systemctl stop uwsgi
```

### 启动服务

```bash
sudo systemctl start uwsgi
```

### 重新加载配置（无需重启）

```bash
sudo systemctl reload uwsgi
```

## 监控和日志

### 查看实时日志

```bash
tail -f /home/acs/roamio/uwsgi.log
```

### 查看最近的错误

```bash
tail -n 100 /home/acs/roamio/uwsgi.log | grep -i error
```

### 查看 Nginx 日志

```bash
sudo tail -f /var/log/nginx/error.log
```

## 性能优化

### 调整 uWSGI 进程数

编辑 `/home/acs/roamio/scripts/uwsgi.ini`：

```ini
processes = 4  # 根据服务器性能调整
threads = 5
```

重启服务：

```bash
sudo systemctl restart uwsgi
```

### 清理旧的静态文件

```bash
cd /home/acs/roamio
rm -rf staticfiles/*
python3 manage.py collectstatic --noinput
```

## 回滚部署

如果需要回滚到之前的版本：

```bash
cd /home/acs/roamio
git log --oneline  # 查看提交历史
git reset --hard <commit-hash>  # 回滚到指定版本
sudo systemctl restart uwsgi
```


