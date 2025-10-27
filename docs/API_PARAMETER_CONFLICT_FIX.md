# API 参数冲突修复说明

## 🐛 问题描述

前端访问评论API时出现 404 错误：
```
GET http://localhost:8080/api/v1/comments/?page=trip1
404 (Not Found)
Error: Invalid page.
```

## 🔍 问题原因

**`page` 参数与 DRF 的分页参数冲突！**

Django REST Framework 的 `PageNumberPagination` 使用 `page` 作为分页参数（如 `?page=1`, `?page=2` 表示第几页），所以我们不能同时用 `page` 来过滤评论所属的旅行页面。

## ✅ 解决方案

### 后端修改

创建自定义过滤器类，将查询参数 `trip` 映射到模型字段 `page`：

**文件：`cetapp/api/viewsets.py`**

```python
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import CharFilter

class CommentFilter(FilterSet):
    """评论过滤器 - 使用 'trip' 参数代替 'page' 以避免与分页冲突"""
    trip = CharFilter(field_name='page', lookup_expr='exact')
    
    class Meta:
        model = Comment
        fields = {
            'user': ['exact'],
        }

class CommentViewSet(viewsets.ModelViewSet):
    """评论ViewSet"""
    queryset = Comment.objects.all().order_by('-timestamp')
    filterset_class = CommentFilter  # 使用自定义过滤器
    # ...
```

### 前端修改

将过滤参数从 `page` 改为 `trip`：

**文件：`cetapp/web/src/views/TripDetailView.vue`**

```javascript
// 修改前
const data = await getCommentList({ page: slug })

// 修改后
const data = await getCommentList({ trip: slug })
```

## 📝 API 使用说明

### ✅ 正确用法

```javascript
// 获取 trip1 的评论
GET /api/v1/comments/?trip=trip1

// 获取 trip1 的第2页评论
GET /api/v1/comments/?trip=trip1&page=2

// 按用户过滤
GET /api/v1/comments/?trip=trip1&user=7
```

### ❌ 错误用法（会被分页器拦截）

```javascript
GET /api/v1/comments/?page=trip1  // ❌ page 被分页器占用
```

## 🔑 重要提示

1. **查询参数**：使用 `trip` 来过滤评论所属的旅行页面
2. **模型字段**：Comment 模型的字段名仍然是 `page`（不需要修改数据库）
3. **创建评论**：创建评论时仍然使用 `page` 字段名（FormData.append('page', 'trip1')）
4. **分页参数**：`page=1,2,3...` 仍然用于分页

## ✅ 测试结果

```bash
# 后端测试
curl "http://127.0.0.1:8000/api/v1/comments/?trip=trip1"
# 返回 200 OK，包含43条评论 ✅

# 前端测试
访问 http://localhost:8080/
点击任意旅行卡片查看详情
评论正常显示 ✅
```

## 📚 相关文件

- `cetapp/api/viewsets.py` - 后端过滤器配置
- `cetapp/web/src/api/comment.js` - 前端API封装
- `cetapp/web/src/views/TripDetailView.vue` - 前端使用示例

---

**修复日期**: 2025-10-27  
**影响范围**: 评论API过滤功能  
**兼容性**: 向前兼容，不影响已有功能

