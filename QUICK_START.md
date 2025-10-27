# ⚡ 快速开始

## 🎯 核心理念

**Vue打包后作为Django静态文件，无需修改Nginx！**

---

## 🚀 3步部署

### 1. 构建Vue
```bash
cd cetapp/web
npm run build
```

### 2. 收集静态文件
```bash
cd ../..
python manage.py collectstatic --noinput
```

### 3. 重启Django
```bash
sudo supervisorctl restart cet
```

**或者一键执行：**
```bash
chmod +x scripts/deploy_simple.sh
./scripts/deploy_simple.sh
```

---

## 🌐 访问地址

- **旧系统（Django HTML）**: `https://yourdomain.com/cetapp/trip/`
- **新系统（Vue SPA）**: `https://yourdomain.com/app/`
- **API文档**: `https://yourdomain.com/api/docs/`

---

## 📚 文档索引

### 必读
- [简单部署指南](docs/SIMPLE_DEPLOYMENT.md) ⭐ - 详细部署说明

### 参考
- [API快速开始](docs/QUICK_START_API.md) - API使用
- [前端集成指南](docs/FRONTEND_INTEGRATION_COMPLETE.md) - Vue架构

### 问题修复
- [静态文件404](docs/STATIC_FILES_FIX.md)
- [API参数冲突](docs/API_PARAMETER_CONFLICT_FIX.md)
- [注册功能](docs/REGISTRATION_FIX.md)

---

## 🔧 本地开发

```bash
# 终端1：Django后端
python manage.py runserver

# 终端2：Vue前端
cd cetapp/web
npm run serve
```

访问：http://localhost:8080

---

**就这么简单！** ✨

