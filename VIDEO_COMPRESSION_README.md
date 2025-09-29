# 视频上传与压缩功能说明

## 功能概述

长沙旅行页面现已支持视频上传功能，并具备自动压缩机制，有效减少GitHub存储占用。

## 主要特性

### 1. 双重媒体支持
- **图片上传**：支持常见图片格式（JPG、PNG等）
- **视频上传**：支持常见视频格式（MP4、AVI等）
- **同时上传**：用户可以同时上传图片和视频到同一条评论

### 2. 智能压缩策略

#### 图片压缩
- 自动调整尺寸至最大1080px宽度
- JPEG质量压缩（70%，如仍超1MB则降至50%）
- 确保文件大小控制在合理范围内

#### 视频压缩
- **触发条件**：仅对超过5MB的视频进行压缩
- **分辨率调整**：最大720p分辨率
- **比特率控制**：
  - 视频比特率：500kbps
  - 音频比特率：64kbps
- **编码优化**：使用快速编码预设

### 3. 存储优化
- 压缩前：原始视频可能达到50MB+
- 压缩后：通常能减少到2-8MB，压缩率80-95%
- 显著减少GitHub仓库大小

## 技术实现

### 依赖库
```python
# 必需安装
pip install moviepy
```

### 核心代码位置
- **模型定义**：`cetapp/models.py` - Comment模型
- **压缩逻辑**：在模型的save()方法中实现
- **前端界面**：`cetapp/templates/cetapp/trip4.html`

### 压缩流程
1. 用户上传视频文件
2. 系统检查文件大小是否超过5MB
3. 如需要压缩：
   - 读取视频文件
   - 调整分辨率为720p
   - 设置低比特率重新编码
   - 替换原文件
4. 保存到`media/comment_videos/`目录

## 部署注意事项

### GitHub存储管理
1. **避免大文件提交**：压缩功能确保视频文件大小合理
2. **Git LFS考虑**：对于计划上传大量媒体文件，可考虑启用Git LFS
3. **定期清理**：建议定期检查媒体文件占用空间

### 服务器部署
1. **安装FFmpeg**：MoviePy需要FFmpeg支持
   ```bash
   # Ubuntu/Debian
   sudo apt install ffmpeg
   
   # Windows
   # 下载FFmpeg并配置环境变量
   ```

2. **依赖安装**：
   ```bash
   pip install moviepy
   ```

3. **文件权限**：确保Django有写入media目录的权限

### 性能考虑
- **压缩时间**：压缩大型视频可能需要较长时间
- **CPU使用**：视频压缩是CPU密集型操作
- **异步处理**：生产环境建议使用Celery进行异步压缩

## 使用示例

### 前端上传
```html
<!-- 长沙旅行页面评论表单 -->
<form id="commentForm" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    <textarea name="content" placeholder="写下你的留言..."></textarea>

    <!-- 图片上传 -->
    <input type="file" name="image" accept="image/*">
    
    <!-- 视频上传 -->
    <input type="file" name="video" accept="video/*">
    
    <button type="submit">发表评论</button>
</form>
```

### 前端显示
```html
<!-- 视频播放 -->
{% if comment.video %}
<video controls style="max-width: 100%; max-height: 400px;">
    <source src="{{ comment.video.url }}" type="video/mp4">
    您的浏览器不支持视频播放。
</video>
{% endif %}
```

## 压缩效果预估

| 原始大小 | 压缩后大小 | 压缩率 |
|---------|-----------|--------|
| 50MB    | ~3-8MB   | 85-95% |
| 30MB    | ~2-5MB   | 85-95% |
| 10MB    | ~2-3MB   | 70-85% |
| 5MB     | 不压缩    | 0%     |

## 故障排除

### 常见问题
1. **MoviePy导入失败**：确保使用正确的Python环境安装
2. **FFmpeg未找到**：安装FFmpeg并确保在PATH中
3. **压缩失败**：检查文件格式兼容性

### 调试方法
```python
# 在Django shell中测试
python manage.py shell

from cetapp.models import Comment
comment = Comment.objects.filter(video__isnull=False).first()
if comment:
    print(f"视频大小: {comment.video.size}")
```

## 扩展功能建议

1. **进度显示**：添加压缩进度条
2. **格式转换**：自动转换为Web友好格式（WebM）
3. **缩略图生成**：为视频生成预览缩略图
4. **批量处理**：支持批量上传和压缩

---

总结：视频压缩功能有效解决了GitHub存储占用问题，确保项目仓库保持轻量化，同时提供良好的用户体验。
