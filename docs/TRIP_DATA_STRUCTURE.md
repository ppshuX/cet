# 旅行数据结构说明

## 📊 数据模型对比

### ❌ 旧模型：SiteStat（没有作者信息）

```python
class SiteStat(models.Model):
    """网站统计模型（旧）"""
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    page = models.CharField(max_length=16)  # 如 'trip', 'trip1', 'trip2'
    # ❌ 没有 author 字段
```

**问题：**
- 无法知道这些"旅行"是谁创建的
- 无法查询某个用户的旅行列表
- 无法过滤"我的旅行"

### ✅ 新模型：Trip（有作者信息）

```python
class Trip(models.Model):
    """旅行计划模型（新）"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='🗺️')
    
    # ⭐ 作者字段
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    
    # 日期
    start_date = models.DateField()
    end_date = models.DateField()
    
    # 状态
    status = models.CharField(choices=[('draft', '草稿'), ('published', '已发布')])
    visibility = models.CharField(choices=[('private', '私有'), ('public', '公开')])
```

**优势：**
- ✅ 每个旅行都有明确的作者
- ✅ 可以查询某个用户的所有旅行
- ✅ 支持"我的旅行"功能
- ✅ 支持权限控制（只能编辑自己的旅行）

## 🔄 当前数据库状态

### 旧数据（SiteStat）

```
Total: 5 条记录
1. page=trip,    views=786,  likes=1870  ⚠️ 没有作者
2. page=trip1,   views=351,  likes=2057  ⚠️ 没有作者
3. page=trip2,   views=245,  likes=220   ⚠️ 没有作者
4. page=trip3,   views=421,  likes=558   ⚠️ 没有作者
5. page=trip4,   views=82,   likes=15    ⚠️ 没有作者
```

### 新数据（Trip）

```
Total: 0 条记录
（没有用户创建新的旅行计划）
```

## 🎯 答案

### Q: 旅行树中的旅行，对应的作者分别是哪些？

**A: 当前旅行树显示的数据来自旧模型 `SiteStat`，这些数据没有作者信息。**

**具体说明：**
1. **旅行树**（`TripListView`）调用 `/api/v1/trips/`
2. 这个 API 使用的是 `TripViewSet`
3. `TripViewSet` 实际上查询的是 `SiteStat` 模型
4. `SiteStat` 模型没有 `author` 字段

### 为什么会这样？

你的项目正在从旧系统迁移到新系统：

**旧系统：**
```python
# 简单的页面统计
SiteStat(page='trip', views=786, likes=1870)
```

**新系统：**
```python
# 完整的旅行计划
Trip(
    title='厦门之旅',
    author=User(username='J.Grigg'),  # ⭐ 有作者！
    start_date='2025-07-01',
    visibility='public'
)
```

### 🔧 如何修复？

#### 方案1：给旧数据添加默认作者

```python
# 创建迁移，给所有旧 SiteStat 添加默认作者
# 但这需要手动分配每个"旅行"给某个用户
```

#### 方案2：使用新的 Trip 模型（推荐）

```python
# 让 TripViewSet 使用新的 Trip 模型
class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.filter(visibility='public')  # ✅ 使用新模型
    serializer_class = TripSerializer
```

### 📝 建议

如果你想让"旅行树"显示有作者信息的旅行：

1. **创建一些旅行计划**（在编辑器中）
2. **将 `TripViewSet` 切换到新模型**
3. **旧数据保留作为"示例"或"模板"**

### 当前的实际情况

- ✅ **J.Grigg 的旅行数：0**（因为没有在编辑器创建）
- ✅ **J.Grigg 的评论数：77**
- ✅ **等级：探索者**（0旅行 + 77评论）
- ⚠️ **旅行树显示的 5 个"旅行"没有作者信息**（旧数据）

## 🚀 下一步

如果你想提升等级到**旅行大师**：

1. 使用编辑器创建 **10 个旅行计划**
2. 你已经有 77 条评论
3. 满足条件：**10 个旅行 + 100 条评论** → 大师

**你就将成为旅行大师！**

## 📊 数据模型关系图

```
User (用户)
  ↓
  ├─ trips (一对多) → Trip (有作者) ⭐ 新系统
  └─ comment_set (一对多) → Comment

SiteStat (旧数据，无作者关系)
  └─ ❌ 无法关联到 User
```

