# 🧩 旅行页面组件使用指南

## 📦 组件列表

### 1. TripProgress - 旅行进度条

**功能**: 显示旅行的进度条，根据开始和结束日期计算当前进度。

**Props**:
- `startDate` (String, 可选): 旅行开始日期 (格式: YYYY-MM-DD)
- `endDate` (String, 可选): 旅行结束日期 (格式: YYYY-MM-DD)

**使用示例**:
```vue
<TripProgress
  start-date="2025-06-22"
  end-date="2025-06-24"
/>
```

**特性**:
- 自动计算旅行进度百分比
- 三种状态：未开始、进行中、已结束
- 绿色渐变进度条
- 显示提示信息

---

### 2. TripStats - 统计数据卡片

**功能**: 显示旅行的浏览量、点赞数，并提供点赞按钮。

**Props**:
- `views` (Number, 默认: 0): 浏览量
- `likes` (Number, 默认: 0): 点赞数

**Events**:
- `@like`: 点击点赞按钮时触发

**使用示例**:
```vue
<TripStats
  :views="trip.stats.views"
  :likes="trip.stats.likes"
  @like="handleLike"
/>
```

**特性**:
- 漂亮的统计卡片样式
- 图标 + 数字展示
- 蓝色渐变点赞按钮
- 点赞中的加载状态

---

### 3. TripOverview - 行程概览

**功能**: 通用的内容展示卡片，使用插槽 (slot) 来自定义内容。

**Props**:
- `title` (String, 默认: "行程概览"): 卡片标题

**Slots**:
- `default`: 卡片内容（支持HTML）

**使用示例**:
```vue
<!-- 行程介绍 -->
<TripOverview title="行程概览">
  <h4>第一天：厦门植物园</h4>
  <p>早上游览厦门植物园...</p>
  
  <h4>第二天：鼓浪屿</h4>
  <p>乘船前往鼓浪屿...</p>
</TripOverview>

<!-- 预算表格 -->
<TripOverview title="预算明细">
  <table>
    <thead>
      <tr>
        <th>项目</th>
        <th>金额</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>交通</td>
        <td>¥500</td>
      </tr>
      <tr>
        <td>住宿</td>
        <td>¥800</td>
      </tr>
    </tbody>
  </table>
</TripOverview>
```

**特性**:
- 白色卡片背景
- 标题带下划线
- 内置样式支持：标题、段落、列表、表格
- 响应式设计

---

### 4. CommentSection - 评论区

**功能**: 完整的评论功能，包括打卡、发布评论、查看评论、删除评论。

**Props**:
- `comments` (Array, 默认: []): 评论列表
- `isAdmin` (Boolean, 默认: false): 是否为管理员
- `hasCheckedIn` (Boolean, 默认: false): 是否已打卡
- `getAvatarUrl` (Function, 必需): 获取头像URL的函数

**Events**:
- `@checkin`: 点击打卡按钮时触发
- `@submit-comment`: 提交评论时触发，参数: `{ content, image, video }`
- `@delete-comment`: 删除评论时触发，参数: `commentId`

**使用示例**:
```vue
<CommentSection
  :comments="comments"
  :is-admin="isAdmin"
  :has-checked-in="trip.stats.checked_in"
  :get-avatar-url="getAvatarUrl"
  @checkin="handleCheckin"
  @submit-comment="handleSubmitComment"
  @delete-comment="handleDeleteComment"
/>
```

**在 setup() 中实现事件处理**:
```javascript
// 打卡
const handleCheckin = async () => {
  try {
    await checkinTrip(route.params.slug)
    await fetchTripDetail() // 刷新数据
    alert('打卡成功！')
  } catch (error) {
    console.error('打卡失败:', error)
  }
}

// 提交评论
const handleSubmitComment = async (commentData) => {
  try {
    const formData = new FormData()
    formData.append('page', route.params.slug)
    if (commentData.content) {
      formData.append('content', commentData.content)
    }
    if (commentData.image) {
      formData.append('image', commentData.image)
    }
    if (commentData.video) {
      formData.append('video', commentData.video)
    }
    
    await createComment(formData)
    await fetchComments() // 刷新评论列表
  } catch (error) {
    console.error('发布评论失败:', error)
  }
}

// 删除评论
const handleDeleteComment = async (commentId) => {
  try {
    await deleteComment(commentId)
    await fetchComments() // 刷新评论列表
  } catch (error) {
    console.error('删除评论失败:', error)
  }
}
```

**特性**:
- 打卡功能（已打卡显示✅）
- 管理员可发布评论（支持图片、视频）
- 评论列表展示（头像、用户名、时间、内容）
- 管理员可删除评论
- 图片点击放大查看
- 视频播放器
- 加载状态动画

---

## 🎯 完整页面示例

**TripDetailView.vue 简化版**:

```vue
<template>
  <div class="trip-detail-container">
    <NavBar />
    
    <div class="container py-5">
      <div v-if="loading" class="text-center">
        <div class="spinner-border text-primary"></div>
      </div>
      
      <div v-else-if="trip">
        <!-- 标题卡片 -->
        <div class="card shadow-lg mb-4">
          <div class="card-body p-5">
            <h1>{{ trip.name }}</h1>
            <p class="text-muted">{{ trip.description }}</p>
            
            <!-- 统计组件 ⭐ -->
            <TripStats
              :views="trip.stats.views"
              :likes="trip.stats.likes"
              @like="handleLike"
            />
          </div>
        </div>
        
        <!-- 进度条组件 ⭐ -->
        <TripProgress
          start-date="2025-06-22"
          end-date="2025-06-24"
        />
        
        <!-- 行程概览组件 ⭐ -->
        <TripOverview title="行程概览">
          <h4>第一天：厦门植物园</h4>
          <p>游览植物园，观赏热带植物...</p>
        </TripOverview>
        
        <!-- 评论组件 ⭐ -->
        <CommentSection
          :comments="comments"
          :is-admin="isAdmin"
          :has-checked-in="trip.stats.checked_in"
          :get-avatar-url="getAvatarUrl"
          @checkin="handleCheckin"
          @submit-comment="handleSubmitComment"
          @delete-comment="handleDeleteComment"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores'
import { getTripDetail, likeTrip, checkinTrip } from '@/api/trip'
import { getCommentList, createComment, deleteComment } from '@/api/comment'
import { getAvatarUrl } from '@/config/api'
import NavBar from '@/components/NavBar.vue'
import TripProgress from '@/components/TripProgress.vue'
import TripStats from '@/components/TripStats.vue'
import TripOverview from '@/components/TripOverview.vue'
import CommentSection from '@/components/CommentSection.vue'

export default {
  name: 'TripDetailView',
  
  components: {
    NavBar,
    TripProgress,
    TripStats,
    TripOverview,
    CommentSection
  },
  
  setup() {
    const route = useRoute()
    const userStore = useUserStore()
    
    const trip = ref(null)
    const comments = ref([])
    const loading = ref(true)
    
    const isAdmin = computed(() => userStore.isAdmin)
    
    // ... 数据获取和事件处理逻辑
    
    return {
      trip,
      comments,
      loading,
      isAdmin,
      handleLike,
      handleCheckin,
      handleSubmitComment,
      handleDeleteComment,
      getAvatarUrl
    }
  }
}
</script>
```

---

## 🎨 样式特点

所有组件都遵循统一的设计语言：

- **白色卡片背景** (#fff)
- **12px 圆角** (border-radius: 12px)
- **柔和阴影** (0 4px 12px rgba(0,0,0,0.05))
- **悬停动画** (transform + box-shadow)
- **响应式设计** (移动端优化)

---

## 📝 注意事项

1. **TripProgress**: 如果不传日期，默认显示50%进度
2. **TripStats**: 点赞按钮点击后会有500ms的禁用状态
3. **TripOverview**: 使用 `:deep()` 为插槽内容提供样式
4. **CommentSection**: 只有管理员能看到发表评论表单

---

## 🚀 扩展性

这些组件都是独立的，可以：
- 在任何页面中使用
- 组合使用或单独使用
- 通过 props 自定义样式
- 通过 slots 自定义内容

---

**创建日期**: 2025-10-27  
**组件数量**: 4个  
**作者**: AI Assistant

