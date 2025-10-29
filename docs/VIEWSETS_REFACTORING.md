# ViewSets 重构说明

## 背景

原始的 `trips/api/viewsets.py` 文件有 605 行代码，包含了 5 个不同的 ViewSet 类，导致文件过长，难以维护。

## 重构方案

将 `viewsets.py` 拆分为多个小文件，按功能模块组织：

```
trips/api/
├── __init__.py
├── viewsets.py.old          # 原文件备份
└── viewsets/                # 新增目录
    ├── __init__.py           # 导出所有 ViewSet
    ├── auth_viewset.py       # 认证相关 (注册、登录、登出)
    ├── user_viewset.py       # 用户相关 (用户信息、头像上传、个人资料)
    ├── comment_viewset.py    # 评论相关 (评论 CRUD、图片上传)
    ├── trip_viewset.py       # 旅行页面相关 (展示、点赞、打卡、评论列表)
    └── trip_plan_viewset.py  # 旅行计划相关 (CRUD、克隆、添加到旅行树)
```

## 各文件说明

### 1. `auth_viewset.py` (95行)
- **功能**: 用户认证
- **ViewSet**: `AuthViewSet`
- **Actions**: `register`, `login`, `logout`, `me`

### 2. `user_viewset.py` (105行)
- **功能**: 用户信息管理
- **ViewSet**: `UserViewSet`
- **Actions**: `upload_avatar`, `update_profile`, `stats`

### 3. `comment_viewset.py` (225行)
- **功能**: 评论管理
- **ViewSet**: `CommentViewSet`
- **FilterSet**: `CommentFilter`
- **Actions**: `add_image` (为评论添加图片)

### 4. `trip_viewset.py` (78行)
- **功能**: 旅行页面展示和互动
- **ViewSet**: `TripViewSet`
- **Actions**: `like`, `checkin`, `stats`, `comments`

### 5. `trip_plan_viewset.py` (186行)
- **功能**: 旅行计划编辑和管理
- **ViewSet**: `TripPlanViewSet`
- **Actions**: `my_trips`, `clone`, `add_to_tree`, `remove_from_tree`

## 导入路径调整

所有 ViewSet 都通过 `trips/api/viewsets/__init__.py` 统一导出：

```python
from .auth_viewset import AuthViewSet
from .user_viewset import UserViewSet
from .comment_viewset import CommentViewSet, CommentFilter
from .trip_viewset import TripViewSet
from .trip_plan_viewset import TripPlanViewSet
```

这样，`trips/api/urls.py` 中的导入无需修改：

```python
from .viewsets import UserViewSet, CommentViewSet, TripViewSet, TripPlanViewSet, AuthViewSet
```

## 相对导入路径

在各个 ViewSet 文件中，使用 `...` (三个点) 来访问上级模块：

```python
from ...models import Comment
from ...serializers import CommentSerializer
```

这是因为文件结构是：
- `trips/models/` - 三级的 parents (from `trips/api/viewsets/`)
- `trips/serializers/` - 三级的 parents (from `trips/api/viewsets/`)

## 优势

1. **更好的代码组织**: 每个文件专注于一个功能模块
2. **更易于维护**: 修改某个功能只需要查看对应文件
3. **更清晰的职责划分**: 每个 ViewSet 的职责更加明确
4. **更易于协作**: 多人开发时减少代码冲突
5. **更符合 Django 最佳实践**: 模块化组织代码

## 后续优化建议

1. 可以考虑进一步拆分 `comment_viewset.py` 和 `trip_plan_viewset.py`，因为它们仍然比较长
2. 可以添加更多的文档字符串
3. 可以考虑使用 mixins 来共享通用逻辑
