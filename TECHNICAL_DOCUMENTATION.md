# Roamio 技术文档

## 📋 目录

1. [项目概述](#项目概述)
2. [技术架构](#技术架构)
3. [技术栈](#技术栈)
4. [系统架构](#系统架构)
5. [数据库设计](#数据库设计)
6. [API设计](#api设计)
7. [前端架构](#前端架构)
8. [核心功能实现](#核心功能实现)
9. [部署方案](#部署方案)
10. [开发指南](#开发指南)
11. [安全机制](#安全机制)
12. [性能优化](#性能优化)

---

## 项目概述

### 项目简介

Roamio 是一个现代化的旅行规划与社区分享平台，采用前后端分离架构，为用户提供完整的旅行规划、编辑、分享和社区互动功能。

### 核心特性

- **可视化旅行编辑** - 模块化的行程编辑器，支持实时预览
- **社区互动** - 评论、回复、点赞、打卡等社交功能
- **用户等级系统** - 基于公开旅行和评论数的等级进阶
- **智能媒体处理** - 自动压缩图片和视频
- **权限控制** - 细粒度的访问控制和数据隐私保护
- **响应式设计** - 完美适配移动端和PC端

---

## 技术架构

### 架构模式

采用 **前后端分离** 架构：

```
┌─────────────────────────────────────────┐
│             前端 (Vue 3)                 │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │   SPA    │  │ Pinia    │  │ Router ││
│  │  Pages   │  │  Store   │  │  Route ││
│  └──────────┘  └──────────┘  └────────┘│
└─────────────────────────────────────────┘
                    ↓ HTTPS
┌─────────────────────────────────────────┐
│         后端 API (Django REST)           │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │ ViewSets │  │Models   │  │Serial ││
│  │  CRUD    │  │Database │  │   izer││
│  └──────────┘  └──────────┘  └────────┘│
└─────────────────────────────────────────┘
                    ↓ ORM
┌─────────────────────────────────────────┐
│          数据库 (SQLite/PostgreSQL)      │
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │  Users   │  │  Trips   │  │Comments││
│  │ Profiles │  │  Stats   │  │  Media ││
│  └──────────┘  └──────────┘  └────────┘│
└─────────────────────────────────────────┘
```

### 数据流向

```
User Action (前端)
    ↓
API Request (HTTP/HTTPS)
    ↓
ViewSet (权限验证、数据处理)
    ↓
Serializer (数据验证、序列化)
    ↓
Model (ORM操作)
    ↓
Database (持久化存储)
    ↓
Response (JSON数据)
    ↓
Frontend Display (渲染展示)
```

---

## 技术栈

### 后端技术

| 技术 | 版本 | 用途 |
|------|------|------|
| **Django** | 5.0.6 | Web框架 |
| **Django REST Framework** | 3.14.0 | REST API |
| **DRF SimpleJWT** | 5.3.0 | JWT认证 |
| **django-cors-headers** | 4.3.0 | 跨域请求 |
| **django-filter** | 23.5 | 数据过滤 |
| **Pillow** | 10.0.0 | 图片处理 |
| **MoviePy** | 1.0.3 | 视频处理 |
| **uWSGI** | 2.0.23 | WSGI服务器 |

### 前端技术

| 技术 | 版本 | 用途 |
|------|------|------|
| **Vue.js** | 3.x | 前端框架 |
| **Vue Router** | 4.x | 路由管理 |
| **Pinia** | 2.x | 状态管理 |
| **Axios** | - | HTTP请求 |
| **Bootstrap 5** | 5.x | UI框架 |
| **Babel** | - | JS转译 |

### 数据库

- **开发环境**: SQLite 3
- **生产环境**: PostgreSQL (推荐)

### 部署工具

- **Nginx**: 反向代理、静态文件服务
- **uWSGI**: Python应用服务器
- **Supervisor**: 进程管理

---

## 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                    前端层 (Vue 3)                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  View Layer │  │State(Pinia) │  │  Router     │     │
│  │   Page      │  │  Store      │  │  Route      │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│         │                 │                 │           │
│  ┌────────────────────────────────────────────────┐  │
│  │          组件层 (Components)                     │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │  │
│  │  │  Editor  │  │ Comments │  │  NavBar  │      │  │
│  │  └──────────┘  └──────────┘  └──────────┘      │  │
│  └────────────────────────────────────────────────┘  │
│                            │                          │
│  ┌────────────────────────────────────────────────┐  │
│  │          API封装层 (Axios)                     │  │
│  │  HTTP请求 → request.js → API端点               │  │
│  └────────────────────────────────────────────────┘  │
└────────────────────┬──────────────────────────────────┘
                     │ HTTPS/REST API
┌────────────────────┴──────────────────────────────────┐
│                 后端层 (Django)                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  REST API   │  │ ViewSets    │  │  URL Router │     │
│  │  Framework  │  │  CRUD操作   │  │  路由分发   │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│         │                 │                 │           │
│  ┌────────────────────────────────────────────────┐  │
│  │          序列化器层 (Serializers)                │  │
│  │  数据验证 → 序列化 → 反序列化 → 权限控制        │  │
│  └────────────────────────────────────────────────┘  │
│                            │                          │
│  ┌────────────────────────────────────────────────┐  │
│  │          模型层 (Models)                        │  │
│  │  ORM映射 → 数据库操作 → 业务逻辑                │  │
│  └────────────────────────────────────────────────┘  │
└────────────────────┬──────────────────────────────────┘
                     │ ORM Query
┌────────────────────┴──────────────────────────────────┐
│                   数据层                             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Users     │  │    Trips    │  │  Comments   │     │
│  │  Profiles   │  │   SiteStat  │  │  Replies    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐                      │
│  │   Media     │  │  Static     │                      │
│  │  Files      │  │  Files      │                      │
│  └─────────────┘  └─────────────┘                      │
└─────────────────────────────────────────────────────────┘
```

### 后端模块划分

#### 1. 数据模型层 (models/)

```python
trips/models/
├── user_profile.py      # 用户扩展信息
│   ├── UserProfile     # 用户配置文件模型
│   ├── avatar, bio     # 头像、个人简介
│   └── level计算        # 用户等级系统
│
├── trip.py              # 旅行计划模型
│   ├── Trip             # 核心旅行模型
│   ├── slug生成         # 哈希编码唯一标识
│   ├── config (JSON)    # 模块配置
│   └── overview (JSON)  # 内容数据
│
├── comment.py           # 评论模型
│   ├── Comment          # 评论与回复
│   ├── parent外键       # 嵌套回复支持
│   └── media支持        # 图片/视频评论
│
└── site_stat.py         # 网站统计
    ├── SiteStat         # 页面统计数据
    └── views/likes      # 浏览量、点赞数
```

#### 2. API层 (api/)

```python
trips/api/viewsets/
├── user_viewset.py       # 用户管理
│   ├── GET /users/{id}/  # 获取用户信息
│   ├── PATCH /users/{id}/# 更新用户信息
│   └── DELETE /users/{id}/# 删除账号（高级设置）
│
├── trip_plan_viewset.py  # 旅行管理
│   ├── GET /trip-plans/ # 获取列表
│   ├── POST /trip-plans/# 创建旅行
│   ├── PATCH /trip-plans/{slug}/# 更新旅行
│   ├── DELETE /trip-plans/{slug}/# 删除旅行
│   ├── POST /trip-plans/{slug}/clone/# 复制旅行
│   ├── POST /trip-plans/{slug}/add_to_tree/# 添加到旅行树
│   └── retrieve访问控制 # 公开/私有访问控制
│
└── comment_viewset.py    # 评论管理
    ├── GET /comments/?trip={slug}# 获取评论列表
    ├── POST /comments/  # 创建评论（权限：作者可创建顶层）
    ├── GET /comments/{id}/replies/# 获取回复列表
    └── DELETE /comments/{id}/# 删除评论（权限控制）
```

#### 3. 序列化器层 (serializers/)

```python
trips/serializers/
├── user_serializer.py
│   ├── UserSerializer       # 用户基本信息
│   ├── UserProfileSerializer# 用户配置
│   └── RegisterSerializer   # 用户注册
│
├── trip_detail_serializer.py
│   ├── TripCreateSerializer # 创建旅行
│   ├── TripDetailSerializer # 旅行详情
│   ├── TripListSerializer   # 旅行列表
│   └── TripUpdateSerializer # 更新旅行
│
└── comment_serializer.py
    ├── CommentSerializer     # 评论序列化
    ├── CommentCreateSerializer# 创建评论
    └── 权限判断              # can_delete等
```

#### 4. 视图层 (views/)

```python
trips/views/
├── base_views.py      # 基础视图（首页）
├── auth_views.py      # 认证视图
├── user_views.py      # 用户视图
├── trip_views.py      # 旅行视图
└── comment_views.py   # 评论视图
```

#### 5. 工具与管理 (management/)

```python
trips/management/commands/
├── delete_trips_without_slug.py    # 删除无slug旅行（保护旅行树）
└── fix_missing_slugs.py            # 修复slug
```

### 前端模块划分

#### 1. 页面组件 (views/)

```
web/src/views/
├── HomeView.vue              # 首页 - 旅行树展示
├── TripDetailView.vue         # 旅行详情页
│   ├── 内容展示              # highlights, itinerary, budget
│   ├── 评论系统              # CommentSection
│   ├── 背景音乐              # audio player
│   └── 点赞/打卡             # like/checkin
│
├── TripEditorView.vue         # 旅行编辑器
│   ├── 基本信息编辑          # BasicInfoEditor
│   ├── 模块选择              # ModuleSelector
│   ├── 内容编辑              # ContentEditor
│   └── 设置面板              # EditorSidebar
│
├── MyTripsView.vue           # 我的旅行
│   ├── 旅行列表展示          # trip cards
│   ├── 编辑/预览/删除        # actions
│   └── 旅行树管理            # add/remove from tree
│
└── UserCenterView.vue        # 个人中心
    ├── 用户资料              # UserProfileCard
    ├── 统计数据              # UserStats
    └── 高级设置              # AdvancedSettingsModal
```

#### 2. 组件层 (components/)

```
web/src/components/
├── NavBar.vue               # 导航栏（全局）
│   ├── 登录/登出            # auth status
│   ├── 导航链接             # menu items
│   └── 用户头像             # user avatar
│
├── comments/                # 评论组件系统
│   ├── CommentSection.vue  # 评论容器
│   ├── CommentItem.vue     # 单个评论卡片
│   ├── CommentForm.vue     # 评论表单
│   └── ReplySection.vue    # 回复区域
│
└── editor/                  # 编辑器组件
    ├── BasicInfoEditor.vue  # 基本信息编辑
    ├── ModuleSelector.vue  # 模块选择器
    ├── ContentEditor.vue   # 内容编辑器
    └── EditorSidebar.vue   # 编辑侧边栏
```

#### 3. API封装层 (api/)

```javascript
web/src/api/
├── request.js              # HTTP请求基础封装
│   ├── axios实例配置       # baseURL, timeout
│   ├── 请求拦截器          # 添加token
│   ├── 响应拦截器          # 错误处理
│   └── JWT刷新机制        # token refresh
│
├── trip.js                  # 旅行API
│   ├── getTripDetail       # 获取详情
│   ├── createTripPlan      # 创建旅行
│   ├── updateTripPlan      # 更新旅行
│   └── deleteTripPlan      # 删除旅行
│
├── comment.js               # 评论API
│   ├── getComments         # 获取评论列表
│   ├── createComment       # 创建评论
│   ├── deleteComment       # 删除评论
│   └── getReplies          # 获取回复
│
└── user.js                  # 用户API
    ├── getMe                # 获取当前用户
    ├── updateUser           # 更新用户
    └── deleteUser           # 删除账号
```

#### 4. 状态管理 (stores/)

```javascript
web/src/stores/
└── user.js                  # 用户状态管理
    ├── state                # 用户信息、认证状态
    ├── getters              # 计算属性
    └── actions              # 登录、登出、获取用户信息
```

#### 5. 路由配置 (router/)

```javascript
web/src/router/index.js
routes: [
  { path: '/', component: HomeView },
  { path: '/trip/:slug', component: TripDetailView },
  { path: '/editor/:slug?', component: TripEditorView },
  { path: '/my-trips', component: MyTripsView, meta: { requiresAuth: true } },
  { path: '/user-center', component: UserCenterView, meta: { requiresAuth: true } }
]
```

---

## 数据库设计

### 核心数据模型

#### 1. User (Django内置)
```python
# 扩展用户信息
class UserProfile(models.Model):
    user = OneToOneField(User)
    avatar = ImageField()
    bio = TextField()
    tags = CharField()
    level = CharField()  # novice/explorer/wanderer/adventurer/master
    
    # 等级计算基于公开旅行数+评论数
```

#### 2. Trip (旅行计划)
```python
class Trip(models.Model):
    slug = SlugField(unique=True)  # 哈希编码，保证唯一性和隐私
    title = CharField()
    description = TextField()
    icon = CharField()
    author = ForeignKey(User)
    
    # 日期
    start_date = DateField()
    end_date = DateField()
    
    # 状态与可见性
    status = CharField()        # draft/published
    visibility = CharField()    # private/public
    
    # 内容存储（JSON字段）
    config = JSONField()        # 模块配置
    overview = JSONField()      # 内容详情
    
    # 主题
    theme_color = CharField()   # 主题色
    background_music = CharField()  # 背景音乐
    
    # 时间戳
    created_at = DateTimeField()
    updated_at = DateTimeField()
```

#### 3. Comment (评论)
```python
class Comment(models.Model):
    user = ForeignKey(User, related_name='comments')
    parent = ForeignKey('self', null=True)  # 支持嵌套回复
    
    content = TextField()
    image = ImageField()
    video = FileField()
    
    page = CharField()          # 所属页面（旅行slug）
    is_pinned = BooleanField()   # 是否置顶
    
    timestamp = DateTimeField()
    
    class Meta:
        ordering = ['-is_pinned', '-timestamp']
```

#### 4. SiteStat (网站统计)
```python
class SiteStat(models.Model):
    page = CharField()      # 对应旅行slug
    views = IntegerField()   # 浏览量
    likes = IntegerField()   # 点赞数
    checked_in = BooleanField()
```

### 关系图

```
User
  ├─ UserProfile (一对一)
  ├─ Trip (一对多, author)
  ├─ Comment (一对多, user)
  └─ SiteStat (无直接关联)

Trip
  ├─ User (author)
  ├─ SiteStat (通过slug关联)
  └─ Comment (通过page字段关联)

Comment
  ├─ User (评论者)
  ├─ Trip (通过page字段)
  └─ Comment (parent, 嵌套回复)
```

---

## API设计

### RESTful API 规范

#### 基础配置

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```

#### 主要API端点

| 端点 | 方法 | 功能 | 权限 |
|------|------|------|------|
| `/api/v1/auth/register/` | POST | 用户注册 | 公开 |
| `/api/v1/auth/login/` | POST | 用户登录 | 公开 |
| `/api/v1/auth/me/` | GET | 获取当前用户信息 | 认证用户 |
| `/api/v1/users/{id}/` | GET | 获取用户信息 | 只读 |
| `/api/v1/users/{id}/` | PATCH | 更新用户信息 | 本人 |
| `/api/v1/users/{id}/` | DELETE | 删除账号 | 本人 |
| `/api/v1/trip-plans/` | GET | 获取旅行列表 | 只读 |
| `/api/v1/trip-plans/{slug}/` | GET | 获取旅行详情 | 公开或本人 |
| `/api/v1/trip-plans/` | POST | 创建旅行 | 认证用户 |
| `/api/v1/trip-plans/{slug}/` | PATCH | 更新旅行 | 作者 |
| `/api/v1/trip-plans/{slug}/` | DELETE | 删除旅行 | 作者 |
| `/api/v1/comments/` | GET | 获取评论列表 | 只读 |
| `/api/v1/comments/{id}/replies/` | GET | 获取回复 | 只读 |
| `/api/v1/comments/` | POST | 创建评论 | 认证用户 |
| `/api/v1/comments/{id}/` | DELETE | 删除评论 | 本人或管理员 |

### 访问控制逻辑

#### 旅行访问控制
```python
def retrieve(self, request, *args, **kwargs):
    """只有公开的旅行或作者本人可以访问"""
    instance = self.get_object()
    if instance.visibility != 'public' and instance.author != request.user:
        raise NotFound("该旅行计划不可访问")
    return Response(serializer.data)
```

#### 评论创建权限
```python
def perform_create(self, serializer):
    """创建顶层评论需要是旅行作者"""
    parent = serializer.validated_data.get('parent')
    if not parent:  # 顶层评论
        # 检查是否为旅行作者
        trip = Trip.objects.filter(slug=serializer.validated_data['page']).first()
        if trip.author != self.request.user:
            raise PermissionDenied("只有作者可以创建顶层评论")
    serializer.save(user=self.request.user)
```

#### 用户统计
```python
def get_stats(self, obj):
    return {
        'trips_count': obj.trips.count(),                    # 总旅行数
        'public_trips_count': obj.trips.filter(visibility='public').count(),  # 公开旅行数
        'comments_count': obj.comments.count(),             # 评论数
    }
```

---

## 前端架构

### 组件层次

```
App.vue (根组件)
  ├─ NavBar.vue (导航栏)
  ├─ HomeView.vue (首页)
  ├─ TripDetailView.vue (旅行详情)
  │   ├─ ContentEditor.vue (内容显示)
  │   └─ CommentSection.vue (评论区域)
  │       ├─ CommentItem.vue (单个评论)
  │       └─ ReplySection.vue (回复区域)
  ├─ TripEditorView.vue (旅行编辑器)
  │   ├─ BasicInfoEditor.vue
  │   ├─ ModuleSelector.vue
  │   ├─ ContentEditor.vue
  │   └─ EditorSidebar.vue
  ├─ MyTripsView.vue (我的旅行)
  └─ UserCenterView.vue (个人中心)
      ├─ UserProfileCard.vue
      ├─ UserStats.vue
      └─ AdvancedSettingsModal.vue
```

### 状态管理

#### Pinia Store

```javascript
// stores/user.js
export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null,
    isAuthenticated: false,
  }),
  
  actions: {
    async login(credentials) {
      // 登录逻辑
      const tokens = await login(credentials);
      // 存储token
      // 更新userInfo
    },
    
    async fetchUserInfo() {
      // 获取用户信息
      this.userInfo = await getMe();
    }
  }
})
```

### 路由配置

```javascript
const routes = [
  { path: '/', component: HomeView },
  { path: '/trip/:slug', component: TripDetailView },
  { path: '/editor/:slug?', component: TripEditorView },
  { path: '/my-trips', component: MyTripsView, meta: { requiresAuth: true } },
  { path: '/user-center', component: UserCenterView, meta: { requiresAuth: true } },
]
```

---

## 核心功能实现

### 1. 旅行编辑器

#### 模块化设计
- **BasicInfoEditor**: 基本信息（标题、描述、日期）
- **ModuleSelector**: 模块选择（亮点、行程、预算、提示）
- **ContentEditor**: 内容编辑（根据选择的模块动态渲染）
- **EditorSidebar**: 设置面板（状态、可见性、主题色、背景音乐）

#### 数据持久化
```javascript
// 保存草稿
const handleSave = async () => {
  const data = {
    title: tripData.title,
    description: tripData.description,
    config: tripData.config,        // 模块配置
    overview: tripData.overview,    // 详细内容
    status: 'draft'
  };
  await createTripPlan(data);
};
```

### 2. 评论系统

#### 嵌套回复
```python
class Comment(models.Model):
    parent = models.ForeignKey('self', related_name='replies')
    # 顶层评论parent为None
    # 回复时parent指向被回复的评论
```

#### 权限控制
- **创建顶层评论**: 只有旅行作者可以
- **回复**: 所有登录用户可以
- **删除评论**: 评论作者、旅行作者或管理员可以
- **删除回复**: 回复作者、旅行作者或管理员可以

### 3. 用户等级系统

#### 等级计算逻辑
```python
def calculate_level(self):
    trips_count = self.user.trips.filter(visibility='public').count()
    comments_count = self.user.comments.count()
    
    if trips_count >= 10 and comments_count >= 100:
        self.level = 'master'       # 旅行大师
    elif trips_count >= 6 and comments_count >= 50:
        self.level = 'adventurer'   # 冒险家
    elif trips_count >= 3 and comments_count >= 20:
        self.level = 'wanderer'     # 漫游者
    elif trips_count >= 1 and comments_count >= 5:
        self.level = 'explorer'     # 探索者
    else:
        self.level = 'novice'       # 新手
```

**等级要求**:
- 新手: 无要求
- 探索者: ≥1个公开旅行 + ≥5条评论
- 漫游者: ≥3个公开旅行 + ≥20条评论
- 冒险家: ≥6个公开旅行 + ≥50条评论
- 旅行大师: ≥10个公开旅行 + ≥100条评论

### 4. Slug生成

#### 哈希编码
```python
def save(self, *args, **kwargs):
    if not self.slug:
        unique_id = str(uuid.uuid4())
        timestamp = str(timezone.now().timestamp())
        hash_string = f"{self.title}_{unique_id}_{timestamp}"
        
        # MD5哈希，截取12位
        hash_obj = hashlib.md5(hash_string.encode())
        hash_hex = hash_obj.hexdigest()[:12]
        
        self.slug = hash_hex
        # 确保唯一性
```

**优势**:
- 保护隐私：无法从slug推测内容
- 唯一性：结合UUID和时间戳
- 简短：12位十六进制字符串

### 5. 媒体处理

#### 图片压缩
```python
# models/user_profile.py
def save(self, *args, **kwargs):
    if self.avatar:
        img = Image.open(img_path)
        # 裁剪为正方形
        min_side = min(img.width, img.height)
        img = img.crop((left, top, right, bottom))
        
        # 调整为300x300
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        
        # 保存为JPEG
        img.convert('RGB').save(img_path, format='JPEG', quality=90)
```

#### 视频压缩
```python
# 使用MoviePy压缩视频
from moviepy.editor import VideoFileClip

video = VideoFileClip(video_path)
video.write_videofile(output_path, bitrate="1000k")
```

---

## 部署方案

### 生产环境配置

#### uWSGI配置
```ini
[uwsgi]
http = :8000
module = roamio.wsgi:application
master = true
processes = 4
vacuum = true
daemonize = /var/log/uwsgi/uwsgi.log
pidfile = /var/run/uwsgi.pid
```

#### Nginx配置
```nginx
server {
    listen 80;
    server_name app7508.acapp.acwing.com.cn;
    
    # 静态文件
    location /static/ {
        alias /var/www/roamio/staticfiles/;
    }
    
    # Vue构建文件
    location /vue/ {
        alias /var/www/roamio/static/vue/;
    }
    
    # API代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # SPA路由
    location / {
        root /var/www/roamio/static/vue;
        try_files $uri $uri/ /index.html;
    }
}
```

### 部署步骤

```bash
# 1. 克隆代码
git clone https://github.com/ppshuX/roamio.git
cd roamio

# 2. 安装依赖
pip install -r requirements.txt

# 3. 数据库迁移
python manage.py migrate

# 4. 创建超级用户
python manage.py createsuperuser

# 5. 收集静态文件
python manage.py collectstatic --noinput

# 6. 构建前端
cd web
npm install
npm run build
cd ..

# 7. 启动uWSGI
uwsgi --ini scripts/uwsgi.ini --daemonize uwsgi.log

# 8. 重启Nginx
sudo systemctl restart nginx
```

---

## 开发指南

### 本地开发环境

#### 后端启动
```bash
# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 启动开发服务器
python manage.py runserver
```

#### 前端启动
```bash
cd web

# 安装依赖
npm install

# 开发模式（热重载）
npm run serve

# 生产构建
npm run build
```

### 代码规范

#### Python
- 遵循 PEP 8 代码风格
- 使用类型提示（Type Hints）
- 函数和类添加文档字符串

#### JavaScript/Vue
- 使用 ES6+ 语法
- 组件采用 Composition API
- 命名使用 camelCase
- 文件名使用 PascalCase

### 调试技巧

#### Django Debug Toolbar
```python
# settings.py
INSTALLED_APPS = [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
```

#### Vue DevTools
- 安装浏览器扩展: Vue DevTools
- 查看组件状态、Props、Events
- 追踪状态变化

---

## 安全机制

### 1. 认证与授权

#### JWT认证
```python
# settings.py
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}
```

#### 权限控制
```python
class TripPlanViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]
```

### 2. 数据保护

#### 敏感信息过滤
```python
class TripDetailSerializer(serializers.ModelSerializer):
    # 不在公开API中暴露邮箱等敏感信息
    author = UserSerializer(read_only=True)
```

#### CSRF保护
```javascript
// request.js
axios.defaults.xsrfHeaderName = "X-CSRFToken";
```

### 3. 文件上传安全

#### 文件类型验证
```python
# models.py
def validate_image(uploaded_file):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    valid_mime_types = ['image/jpeg', 'image/png', 'image/gif']
    
    if not any(uploaded_file.name.lower().endswith(ext) for ext in valid_extensions):
        raise ValidationError("不支持的图片格式")
```

#### 文件大小限制
```python
# 限制上传文件大小为10MB
MAX_UPLOAD_SIZE = 10 * 1024 * 1024
```

---

## 性能优化

### 1. 数据库优化

#### 使用select_related和prefetch_related
```python
# 减少查询次数
queryset = Comment.objects.select_related('user', 'user__profile').prefetch_related('replies')
```

#### 添加索引
```python
class Trip(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['author', 'status']),
            models.Index(fields=['visibility']),
        ]
```

### 2. 前端优化

#### 懒加载
```javascript
// 路由懒加载
const TripDetailView = () => import('@/views/TripDetailView.vue');

// 图片懒加载
<img v-lazy="imageSrc" />
```

#### 虚拟滚动
```javascript
// 处理大量列表时使用虚拟滚动
import { RecycleScroller } from 'vue-virtual-scroller';
```

### 3. 缓存策略

#### Django缓存
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

#### CDN加速
- 静态文件托管到CDN
- 图片使用WebP格式
- 启用HTTP/2

---

## 附录

### A. API响应格式

```json
{
  "id": 123,
  "title": "厦门三天两晚游",
  "author": {
    "id": 1,
    "username": "testuser",
    "profile": {
      "level": "explorer",
      "avatar": "/media/user_avatars/xxx.jpg"
    }
  },
  "stats": {
    "views": 100,
    "likes": 10
  }
}
```

### B. 错误处理

```json
{
  "detail": "错误消息"
}
// 或
{
  "field_name": ["错误消息1", "错误消息2"]
}
```

### C. 分页格式

```json
{
  "count": 100,
  "next": "http://api.example.com/api/v1/trips/?page=3",
  "previous": "http://api.example.com/api/v1/trips/?page=1",
  "results": [...]
}
```

### D. 常用命令

```bash
# 创建迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 收集静态文件
python manage.py collectstatic

# 运行开发服务器
python manage.py runserver

# 数据库shell
python manage.py dbshell
```

---

## 参考资料

- [Django官方文档](https://docs.djangoproject.com/)
- [Django REST Framework文档](https://www.django-rest-framework.org/)
- [Vue.js官方文档](https://vuejs.org/)
- [Vue Router文档](https://router.vuejs.org/)
- [Pinia文档](https://pinia.vuejs.org/)

---

**文档版本**: v1.0  
**最后更新**: 2024年  
**维护者**: Roamio开发团队
