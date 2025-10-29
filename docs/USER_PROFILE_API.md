# 用户资料 API 使用文档

## 📋 新增字段

在 `UserProfile` 模型中新增的字段：

| 字段 | 类型 | 说明 | 限制 |
|------|------|------|------|
| `bio` | TextField | 个人简介 | 最多500字 |
| `tags` | CharField | 用户标签 | 最多10个，每个最长20字 |
| `visited_countries` | CharField | 访问过的国家 | 自由输入 |
| `level` | CharField | 用户等级 | 自动计算 |

## 🔌 API 端点

### 1. 获取用户资料

```http
GET /api/v1/auth/me/
Authorization: Bearer <token>
```

**响应示例：**
```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "date_joined": "2024-01-01T00:00:00Z",
  "profile": {
    "avatar": "/media/user_avatars/avatar.jpg",
    "avatar_url": "/media/user_avatars/avatar.jpg",
    "bio": "热爱旅行，喜欢摄影",
    "tags": "摄影爱好者,美食达人",
    "level": "adventurer",
    "visited_countries": "中国,日本,泰国"
  },
  "stats": {
    "trips_count": 15,
    "public_trips_count": 8,
    "comments_count": 45
  }
}
```

### 2. 更新个人资料

```http
PATCH /api/v1/users/update_profile/
Authorization: Bearer <token>
Content-Type: application/json

{
  "bio": "热爱旅行，喜欢摄影和美食",
  "tags": "摄影爱好者,美食达人,户外运动",
  "visited_countries": "中国,日本,泰国,新加坡"
}
```

**响应：**
```json
{
  "detail": "个人资料更新成功",
  "profile": {
    "avatar": "/media/user_avatars/avatar.jpg",
    "avatar_url": "/media/user_avatars/avatar.jpg",
    "bio": "热爱旅行，喜欢摄影和美食",
    "tags": "摄影爱好者,美食达人,户外运动",
    "level": "adventurer",
    "visited_countries": "中国,日本,泰国,新加坡"
  }
}
```

### 3. 上传头像

```http
POST /api/v1/users/{id}/upload_avatar/
Authorization: Bearer <token>
Content-Type: multipart/form-data

avatar: <file>
```

**响应：**
```json
{
  "avatar_url": "/media/user_avatars/new_avatar.jpg",
  "detail": "头像上传成功"
}
```

## ⚠️ 验证规则

### bio（个人简介）
- 最多 500 字
- 可以为空

### tags（用户标签）
- 逗号分隔，例如：`"摄影爱好者,美食达人,户外运动"`
- 最多 10 个标签
- 每个标签最长 20 个字符
- 自动去除多余空格

**示例：**
```json
// ✅ 正确
"摄影爱好者,美食达人,户外运动"

// ❌ 错误 - 超过10个标签
"tag1,tag2,tag3,tag4,tag5,tag6,tag7,tag8,tag9,tag10,tag11"

// ❌ 错误 - 单个标签超过20字
"这是一个超级超级超级长的标签名称超过了20个字限制"
```

### visited_countries（访问过的国家）
- 自由文本输入
- 建议使用逗号分隔

## 🤖 自动计算功能

### 用户等级自动计算

等级根据旅行计划和评论数量自动计算：

```python
# 计算规则
total = trips_count * 2 + comments_count

- 新手 (novice):     total < 5
- 探索者 (explorer): 5 <= total < 15
- 漫游者 (wanderer): 15 <= total < 30
- 冒险家 (adventurer): 30 <= total < 50
- 旅行大师 (master): total >= 50
```

每次更新个人资料后，系统会自动重新计算并更新等级。

## 💻 前端使用示例

### Vue 示例

```javascript
// 更新个人资料
const updateProfile = async (profileData) => {
  try {
    const response = await request.patch('/users/update_profile/', {
      bio: profileData.bio,
      tags: profileData.tags,
      visited_countries: profileData.visited_countries
    })
    
    console.log('更新成功：', response.data)
    return response.data
  } catch (error) {
    console.error('更新失败：', error)
    throw error
  }
}

// 使用示例
await updateProfile({
  bio: "热爱旅行，喜欢摄影和美食",
  tags: "摄影爱好者,美食达人",
  visited_countries: "中国,日本,泰国"
})
```

### React 示例

```javascript
// 更新个人资料
const updateProfile = async (profileData) => {
  const response = await fetch('/api/v1/users/update_profile/', {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(profileData)
  })
  
  if (!response.ok) {
    throw new Error('更新失败')
  }
  
  return await response.json()
}
```

## 📊 前端页面建议

### 个人中心编辑表单

建议在个人中心页面添加以下编辑项：

```html
<!-- 个人资料编辑表单 -->
<form @submit.prevent="updateProfile">
  <!-- 头像上传 -->
  <div class="avatar-upload">
    <label>头像</label>
    <input type="file" @change="handleAvatarChange" accept="image/*">
  </div>
  
  <!-- 个人简介 -->
  <div class="form-group">
    <label>个人简介</label>
    <textarea 
      v-model="profile.bio" 
      maxlength="500" 
      rows="5"
      placeholder="介绍一下自己吧...">
    </textarea>
    <span>{{ profile.bio?.length || 0 }}/500</span>
  </div>
  
  <!-- 用户标签 -->
  <div class="form-group">
    <label>个人标签（逗号分隔）</label>
    <input 
      v-model="profile.tags" 
      placeholder="例如：摄影爱好者,美食达人"
      maxlength="200">
    <small>最多10个标签，每个标签不超过20字</small>
  </div>
  
  <!-- 访问过的国家 -->
  <div class="form-group">
    <label>访问过的国家</label>
    <input 
      v-model="profile.visited_countries" 
      placeholder="例如：中国,日本,泰国">
  </div>
  
  <!-- 等级显示（只读） -->
  <div class="form-group">
    <label>当前等级</label>
    <div class="level-badge">{{ profile.levelText }}</div>
  </div>
  
  <button type="submit">保存更改</button>
</form>
```

## 🎨 UI 建议

### 等级徽章显示

```css
.level-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}

.level-novice { background: #e0e0e0; color: #666; }
.level-explorer { background: #bbdefb; color: #1976d2; }
.level-wanderer { background: #c8e6c9; color: #388e3c; }
.level-adventurer { background: #fff9c4; color: #f57f17; }
.level-master { background: #ffeb3b; color: #f57f17; }
```

### 标签输入组件

```javascript
// 标签输入组件
const TagInput = {
  template: `
    <div class="tag-input">
      <div class="tag-list">
        <span 
          v-for="(tag, index) in tags" 
          :key="index" 
          class="tag">
          {{ tag }}
          <button @click="removeTag(index)">×</button>
        </span>
      </div>
      <input 
        v-model="input" 
        @keyup.enter="addTag"
        @keyup.comma="addTag"
        placeholder="输入标签后按回车或逗号">
    </div>
  `,
  data() {
    return {
      tags: [],
      input: ''
    }
  },
  methods: {
    addTag() {
      if (this.input.trim() && this.tags.length < 10) {
        this.tags.push(this.input.trim())
        this.input = ''
      }
    },
    removeTag(index) {
      this.tags.splice(index, 1)
    }
  },
  computed: {
    tagsString() {
      return this.tags.join(',')
    }
  }
}
```

## 📝 总结

新增的 API 接口：

| 端点 | 方法 | 功能 | 认证 |
|------|------|------|------|
| `/api/v1/users/update_profile/` | PATCH/PUT | 更新个人资料 | ✅ 需要 |
| `/api/v1/users/{id}/upload_avatar/` | POST | 上传头像 | ✅ 需要 |
| `/api/v1/auth/me/` | GET | 获取当前用户信息 | ✅ 需要 |

**优势：**
- ✅ 支持部分更新（PATCH）
- ✅ 自动验证数据格式
- ✅ 自动计算用户等级
- ✅ 返回更新后的完整数据

