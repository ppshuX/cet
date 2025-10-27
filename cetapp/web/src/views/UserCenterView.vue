<template>
  <div class="user-center-container">
    <div class="container py-5">
      <!-- 页面标题 -->
      <h2 class="mb-4">个人中心</h2>
      
      <!-- Loading状态 -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">加载中...</span>
        </div>
      </div>
      
      <!-- 用户信息 -->
      <div v-else class="row">
        <!-- 左侧：用户信息卡片 -->
        <div class="col-md-4 mb-4">
          <div class="card shadow-sm">
            <div class="card-body text-center p-4">
              <!-- 头像 -->
              <div class="avatar-container mb-3">
                <img
                  :src="userAvatar"
                  alt="头像"
                  class="rounded-circle"
                  width="120"
                  height="120"
                />
                <button
                  class="btn btn-sm btn-light avatar-upload-btn"
                  @click="triggerFileInput"
                >
                  <i class="bi bi-camera"></i>
                </button>
                <input
                  ref="avatarInput"
                  type="file"
                  accept="image/*"
                  style="display: none"
                  @change="handleAvatarChange"
                />
              </div>
              
              <!-- 用户名 -->
              <h4 class="mb-1">{{ username }}</h4>
              <p class="text-muted mb-3">{{ email || '未设置邮箱' }}</p>
              
              <!-- 标签 -->
              <div class="mb-3">
                <span v-if="isAdmin" class="badge bg-danger">管理员</span>
                <span v-else class="badge bg-primary">普通用户</span>
              </div>
              
              <!-- 注册时间 -->
              <small class="text-muted">
                注册时间：{{ formatDate(userInfo?.date_joined) }}
              </small>
            </div>
          </div>
          
          <!-- 退出登录 -->
          <button
            class="btn btn-outline-danger w-100 mt-3"
            @click="handleLogout"
          >
            退出登录
          </button>
        </div>
        
        <!-- 右侧：信息编辑 -->
        <div class="col-md-8">
          <!-- 基本信息 -->
          <div class="card shadow-sm mb-4">
            <div class="card-header bg-white">
              <h5 class="mb-0">基本信息</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleUpdateInfo">
                <!-- 用户名 -->
                <div class="mb-3">
                  <label class="form-label">用户名</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="editForm.username"
                    :disabled="updating"
                  />
                </div>
                
                <!-- 邮箱 -->
                <div class="mb-3">
                  <label class="form-label">邮箱</label>
                  <input
                    type="email"
                    class="form-control"
                    v-model="editForm.email"
                    :disabled="updating"
                  />
                </div>
                
                <!-- 提交按钮 -->
                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="updating"
                >
                  <span v-if="updating" class="spinner-border spinner-border-sm me-2"></span>
                  {{ updating ? '保存中...' : '保存修改' }}
                </button>
              </form>
            </div>
          </div>
          
          <!-- 统计信息 -->
          <div class="card shadow-sm">
            <div class="card-header bg-white">
              <h5 class="mb-0">我的统计</h5>
            </div>
            <div class="card-body">
              <div class="row text-center">
                <div class="col-4">
                  <div class="stat-box">
                    <h3 class="text-primary">{{ stats.comments_count }}</h3>
                    <p class="text-muted mb-0">评论数</p>
                  </div>
                </div>
                <div class="col-4">
                  <div class="stat-box">
                    <h3 class="text-success">{{ stats.likes_count || 0 }}</h3>
                    <p class="text-muted mb-0">获赞数</p>
                  </div>
                </div>
                <div class="col-4">
                  <div class="stat-box">
                    <h3 class="text-warning">{{ stats.views_count || 0 }}</h3>
                    <p class="text-muted mb-0">浏览数</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores'
import { getUserStats, updateUserInfo, uploadAvatar } from '@/api/user'

export default {
  name: 'UserCenterView',
  
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    
    const loading = ref(false)
    const updating = ref(false)
    const stats = ref({
      comments_count: 0,
      likes_count: 0,
      views_count: 0
    })
    
    const avatarInput = ref(null)
    
    const editForm = ref({
      username: '',
      email: ''
    })
    
    // 从store获取用户信息
    const userInfo = computed(() => userStore.userInfo)
    const username = computed(() => userStore.username)
    const email = computed(() => userInfo.value?.email)
    const isAdmin = computed(() => userStore.isAdmin)
    const userAvatar = computed(() => userStore.avatar)
    
    // 格式化日期
    const formatDate = (dateStr) => {
      if (!dateStr) return '未知'
      const date = new Date(dateStr)
      return date.toLocaleDateString('zh-CN')
    }
    
    // 加载用户统计
    const loadStats = async () => {
      if (!userInfo.value?.id) return
      
      try {
        const data = await getUserStats(userInfo.value.id)
        stats.value = data
      } catch (error) {
        console.error('加载统计失败:', error)
      }
    }
    
    // 初始化编辑表单
    const initEditForm = () => {
      editForm.value = {
        username: userInfo.value?.username || '',
        email: userInfo.value?.email || ''
      }
    }
    
    // 更新用户信息
    const handleUpdateInfo = async () => {
      updating.value = true
      
      try {
        await updateUserInfo(userInfo.value.id, editForm.value)
        
        // 重新获取用户信息
        await userStore.fetchUserInfo()
        
        alert('更新成功！')
      } catch (error) {
        console.error('更新失败:', error)
        alert('更新失败，请稍后重试')
      } finally {
        updating.value = false
      }
    }
    
    // 触发文件选择
    const triggerFileInput = () => {
      avatarInput.value?.click()
    }
    
    // 上传头像
    const handleAvatarChange = async (event) => {
      const file = event.target.files?.[0]
      if (!file) return
      
      // 检查文件类型
      if (!file.type.startsWith('image/')) {
        alert('请选择图片文件')
        return
      }
      
      // 检查文件大小（5MB）
      if (file.size > 5 * 1024 * 1024) {
        alert('图片大小不能超过5MB')
        return
      }
      
      try {
        const formData = new FormData()
        formData.append('avatar', file)
        
        await uploadAvatar(userInfo.value.id, formData)
        
        // 重新获取用户信息
        await userStore.fetchUserInfo()
        
        alert('头像上传成功！')
      } catch (error) {
        console.error('头像上传失败:', error)
        alert('头像上传失败，请稍后重试')
      }
    }
    
    // 退出登录
    const handleLogout = async () => {
      if (!confirm('确定要退出登录吗？')) return
      
      try {
        await userStore.logout()
        router.push('/login')
      } catch (error) {
        console.error('退出失败:', error)
      }
    }
    
    onMounted(async () => {
      // 检查登录状态
      if (!userStore.isLoggedIn) {
        router.push('/login')
        return
      }
      
      loading.value = true
      
      try {
        await loadStats()
        initEditForm()
      } catch (error) {
        console.error('加载失败:', error)
      } finally {
        loading.value = false
      }
    })
    
    return {
      loading,
      updating,
      stats,
      avatarInput,
      editForm,
      userInfo,
      username,
      email,
      isAdmin,
      userAvatar,
      formatDate,
      handleUpdateInfo,
      triggerFileInput,
      handleAvatarChange,
      handleLogout
    }
  }
}
</script>

<style scoped>
.user-center-container {
  min-height: 100vh;
  background: #f8f9fa;
}

.card {
  border: none;
  border-radius: 10px;
}

.card-header {
  border-bottom: 2px solid #f0f0f0;
  padding: 1rem 1.5rem;
}

.avatar-container {
  position: relative;
  display: inline-block;
}

.avatar-upload-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.stat-box {
  padding: 1rem;
}

.stat-box h3 {
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-label {
  font-weight: 500;
  color: #555;
}

.form-control {
  border-radius: 8px;
}

.btn {
  border-radius: 8px;
  padding: 10px 20px;
}
</style>

