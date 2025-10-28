<template>
  <div class="user-center-wrapper">
  <NavBar />
  <div class="user-center-container">
    <!-- 返回按钮 -->
    <button class="back-btn" @click="goBack" title="返回首页">
      🏠
    </button>
    
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
              <h4 class="username-display mb-1">{{ username }}</h4>
              <p class="email-display mb-3">{{ email || '未设置邮箱' }}</p>
              
              <!-- 标签和等级 -->
              <div class="mb-3 d-flex gap-2 justify-content-center align-items-center">
                <span v-if="isAdmin" class="badge bg-danger">管理员</span>
                <span v-else class="badge bg-primary">普通用户</span>
                <span :class="'badge level-badge-small ' + getLevelClass(profileData.level)">
                  {{ getLevelText(profileData.level) }}
                </span>
              </div>
              
              <!-- 注册时间 -->
              <small class="text-muted">
                注册时间：{{ formatDate(userInfo?.date_joined) }}
              </small>
            </div>
          </div>
          
          <!-- 我的统计 -->
          <div class="card shadow-sm mt-3">
            <div class="card-header bg-white">
              <h5 class="mb-0">📊 我的统计</h5>
            </div>
            <div class="card-body">
              <div class="row text-center">
                <div class="col-12 mb-3">
                  <div class="stat-box-small">
                    <h4 class="text-primary mb-1">{{ stats.comments_count || 0 }}</h4>
                    <p class="text-muted mb-0 small">评论数</p>
                  </div>
                </div>
                <div class="col-6 mb-3">
                  <div class="stat-box-small">
                    <h4 class="text-success mb-1">{{ stats.trips_count || 0 }}</h4>
                    <p class="text-muted mb-0 small">旅行数</p>
                  </div>
                </div>
                <div class="col-6 mb-3">
                  <div class="stat-box-small">
                    <h4 class="text-warning mb-1">{{ stats.public_trips_count || 0 }}</h4>
                    <p class="text-muted mb-0 small">公开旅行</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 编辑个人中心按钮 -->
          <button
            v-if="!isEditingBasic && !isEditingProfile"
            class="btn btn-primary w-100 mt-3"
            @click="startEditing"
          >
            ✏️ 编辑个人中心
          </button>
          
          <!-- 保存/取消按钮 -->
          <template v-else>
            <button
              class="btn btn-success w-100 mt-3"
              @click="saveAllChanges"
              :disabled="savingAll"
            >
              <span v-if="savingAll" class="spinner-border spinner-border-sm me-2"></span>
              {{ savingAll ? '保存中...' : '💾 保存所有更改' }}
            </button>
            <button
              class="btn btn-outline-secondary w-100 mt-2"
              @click="cancelAllEdit"
              :disabled="savingAll"
            >
              取消编辑
            </button>
          </template>
        </div>
        
        <!-- 右侧：信息编辑 -->
        <div class="col-md-8">
          <!-- 基本信息 -->
          <div class="card shadow-sm mb-4">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
              <h5 class="mb-0">基本信息</h5>
              <button
                v-if="!isEditingBasic"
                class="btn btn-sm btn-outline-primary"
                @click="isEditingBasic = true"
              >
                ✏️ 编辑
              </button>
            </div>
            <div class="card-body">
              <!-- 只读显示 -->
              <template v-if="!isEditingBasic">
                <div class="info-display">
                  <div class="info-card mb-3">
                    <div class="info-item">
                      <label class="info-label">用户名</label>
                      <p class="info-content">{{ editForm.username }}</p>
                    </div>
                  </div>
                  <div class="info-card">
                    <div class="info-item">
                      <label class="info-label">邮箱</label>
                      <p class="info-content">{{ editForm.email || '未设置' }}</p>
                    </div>
                  </div>
                </div>
              </template>
              
              <!-- 编辑表单 -->
              <form v-else @submit.prevent="handleUpdateInfo">
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
                
                <!-- 操作按钮 -->
                <div class="d-flex gap-2">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="updating"
                  >
                    <span v-if="updating" class="spinner-border spinner-border-sm me-2"></span>
                    {{ updating ? '保存中...' : '💾 保存' }}
                  </button>
                  <button
                    type="button"
                    class="btn btn-outline-secondary"
                    @click="cancelBasicEdit"
                    :disabled="updating"
                  >
                    取消
                  </button>
                </div>
              </form>
            </div>
          </div>
          
          <!-- 旅行者资料 -->
          <div class="card shadow-sm mb-4">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
              <h5 class="mb-0">✨ 旅行者资料</h5>
              <button
                v-if="!isEditingProfile"
                class="btn btn-sm btn-outline-primary"
                @click="isEditingProfile = true"
              >
                ✏️ 编辑
              </button>
            </div>
            <div class="card-body">
              <!-- 用户等级 -->
              <div class="mb-3">
                <label class="form-label">🎖️ 当前等级</label>
                <div>
                  <span :class="'badge level-badge ' + getLevelClass(profileData.level)">
                    {{ getLevelText(profileData.level) }}
                  </span>
                </div>
                <small class="text-muted">根据旅行和评论数量自动计算</small>
              </div>
              
              <!-- 只读显示 -->
              <template v-if="!isEditingProfile">
                <div class="info-display">
                  <div class="info-card mb-3">
                    <label class="info-label">📝 个人简介</label>
                    <p class="info-content">{{ profileData.bio || '还没有写个人简介' }}</p>
                  </div>
                  <div class="info-card mb-3">
                    <label class="info-label">🏷️ 个人标签</label>
                    <div v-if="profileData.tags">
                      <span 
                        v-for="(tag, index) in profileData.tags.split(',')" 
                        :key="index"
                        class="badge bg-light text-dark me-1"
                      >
                        {{ tag.trim() }}
                      </span>
                    </div>
                    <p v-else class="info-content text-muted">还没有添加标签</p>
                  </div>
                  <div class="info-card">
                    <label class="info-label">🌍 访问过的国家</label>
                    <p class="info-content">{{ profileData.visited_countries || '还没有记录' }}</p>
                  </div>
                </div>
              </template>
              
              <!-- 编辑表单 -->
              <form v-else @submit.prevent="handleUpdateProfile">
                <!-- 个人简介 -->
                <div class="mb-3">
                  <label class="form-label">📝 个人简介</label>
                  <textarea
                    class="form-control"
                    v-model="profileData.bio"
                    rows="4"
                    maxlength="500"
                    placeholder="介绍一下自己吧..."
                  ></textarea>
                  <small class="text-muted">{{ profileData.bio?.length || 0 }}/500</small>
                </div>
                
                <!-- 用户标签 -->
                <div class="mb-3">
                  <label class="form-label">🏷️ 个人标签</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="profileData.tags"
                    placeholder="例如：摄影爱好者,美食达人,户外运动"
                    maxlength="200"
                  />
                  <small class="text-muted">逗号分隔，最多10个标签，每个不超过20字</small>
                </div>
                
                <!-- 访问过的国家 -->
                <div class="mb-3">
                  <label class="form-label">🌍 访问过的国家</label>
                  <input
                    type="text"
                    class="form-control"
                    v-model="profileData.visited_countries"
                    placeholder="例如：中国,日本,泰国"
                    maxlength="200"
                  />
                  <small class="text-muted">逗号分隔的国家列表</small>
                </div>
                
                <div class="d-flex gap-2">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="updatingProfile"
                  >
                    <span v-if="updatingProfile" class="spinner-border spinner-border-sm me-2"></span>
                    {{ updatingProfile ? '保存中...' : '💾 保存' }}
                  </button>
                  <button
                    type="button"
                    class="btn btn-outline-secondary"
                    @click="cancelProfileEdit"
                    :disabled="updatingProfile"
                  >
                    取消
                  </button>
                </div>
              </form>
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
import { getUserStats, updateProfile, updateUser, uploadAvatar } from '@/api/user'
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'UserCenterView',
  
  components: {
    NavBar
  },
  
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    
    const loading = ref(false)
    const updating = ref(false)
    const updatingProfile = ref(false)
    const savingAll = ref(false)
    const isEditingBasic = ref(false)
    const isEditingProfile = ref(false)
    const stats = ref({
      comments_count: 0,
      trips_count: 0,
      public_trips_count: 0
    })
    
    const avatarInput = ref(null)
    
    const editForm = ref({
      username: '',
      email: ''
    })
    
    const originalForm = ref({
      username: '',
      email: ''
    })
    
    const profileData = ref({
      bio: '',
      tags: '',
      visited_countries: '',
      level: 'novice'
    })
    
    const originalProfile = ref({
      bio: '',
      tags: '',
      visited_countries: '',
      level: 'novice'
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
      const username = userInfo.value?.username || ''
      const email = userInfo.value?.email || ''
      
      editForm.value = { username, email }
      originalForm.value = { username, email }
      
      const bio = userInfo.value?.profile?.bio || ''
      const tags = userInfo.value?.profile?.tags || ''
      const visited_countries = userInfo.value?.profile?.visited_countries || ''
      const level = userInfo.value?.profile?.level || 'novice'
      
      profileData.value = { bio, tags, visited_countries, level }
      originalProfile.value = { bio, tags, visited_countries, level }
    }
    
    // 取消编辑基本信息
    const cancelBasicEdit = () => {
      editForm.value = { ...originalForm.value }
      isEditingBasic.value = false
    }
    
    // 取消编辑旅行者资料
    const cancelProfileEdit = () => {
      profileData.value = { ...originalProfile.value }
      isEditingProfile.value = false
    }
    
    // 开始编辑
    const startEditing = () => {
      isEditingBasic.value = true
      isEditingProfile.value = true
    }
    
    // 取消所有编辑
    const cancelAllEdit = () => {
      cancelBasicEdit()
      cancelProfileEdit()
    }
    
    // 保存所有更改
    const saveAllChanges = async () => {
      savingAll.value = true
      
      try {
        // 保存基本信息
        if (editForm.value.username !== originalForm.value.username || 
            editForm.value.email !== originalForm.value.email) {
          await updateUser(userInfo.value.id, editForm.value)
        }
        
        // 保存旅行者资料
        if (profileData.value.bio !== originalProfile.value.bio ||
            profileData.value.tags !== originalProfile.value.tags ||
            profileData.value.visited_countries !== originalProfile.value.visited_countries) {
          await updateProfile({
            bio: profileData.value.bio,
            tags: profileData.value.tags,
            visited_countries: profileData.value.visited_countries
          })
        }
        
        // 重新获取用户信息
        await userStore.fetchUserInfo()
        initEditForm()
        
        alert('所有更改已保存！')
      } catch (error) {
        console.error('保存失败:', error)
        alert('保存失败，请稍后重试')
      } finally {
        savingAll.value = false
      }
    }
    
    // 等级文本
    const getLevelText = (level) => {
      const levels = {
        'novice': '新手',
        'explorer': '探索者',
        'wanderer': '漫游者',
        'adventurer': '冒险家',
        'master': '旅行大师'
      }
      return levels[level] || '新手'
    }
    
    // 等级样式类
    const getLevelClass = (level) => {
      const classes = {
        'novice': 'level-novice',
        'explorer': 'level-explorer',
        'wanderer': 'level-wanderer',
        'adventurer': 'level-adventurer',
        'master': 'level-master'
      }
      return classes[level] || 'level-novice'
    }
    
    // 更新个人资料
    const handleUpdateProfile = async () => {
      updatingProfile.value = true
      
      try {
        await updateProfile({
          bio: profileData.value.bio,
          tags: profileData.value.tags,
          visited_countries: profileData.value.visited_countries
        })
        
        // 重新获取用户信息
        await userStore.fetchUserInfo()
        initEditForm()
        
        alert('资料更新成功！')
      } catch (error) {
        console.error('更新失败:', error)
        alert('更新失败，请稍后重试')
      } finally {
        updatingProfile.value = false
      }
    }
    
    // 更新用户信息
    const handleUpdateInfo = async () => {
      updating.value = true
      
      try {
        await updateUser(userInfo.value.id, editForm.value)
        
        // 重新获取用户信息
        await userStore.fetchUserInfo()
        initEditForm()
        
        isEditingBasic.value = false
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
        await uploadAvatar(userInfo.value.id, file)
        
        // 重新获取用户信息
        await userStore.fetchUserInfo()
        
        alert('头像上传成功！')
      } catch (error) {
        console.error('头像上传失败:', error)
        alert('头像上传失败，请稍后重试')
      }
    }
    
    // 返回按钮
    const goBack = () => {
      router.push('/')
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
      updatingProfile,
      savingAll,
      isEditingBasic,
      isEditingProfile,
      stats,
      avatarInput,
      editForm,
      profileData,
      userInfo,
      username,
      email,
      isAdmin,
      userAvatar,
      formatDate,
      goBack,
      handleUpdateInfo,
      handleUpdateProfile,
      cancelBasicEdit,
      cancelProfileEdit,
      startEditing,
      cancelAllEdit,
      saveAllChanges,
      getLevelText,
      getLevelClass,
      triggerFileInput,
      handleAvatarChange,
      handleLogout
    }
  }
}
</script>

<style scoped>
.user-center-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #e8f4fd 0%, #d1ecf1 100%);
}

.user-center-container {
  padding: 2rem 0;
}

/* 返回按钮 */
.back-btn {
  position: fixed;
  top: 100px;
  left: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 1.8rem;
  cursor: pointer;
  z-index: 1000;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  opacity: 0.7;
}

.back-btn:hover {
  background: linear-gradient(135deg, #5568d3 0%, #6a3f91 100%);
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  opacity: 1;
}

h2 {
  color: #2c3e50;
  font-weight: 700;
}

.card {
  border: none;
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.12);
  overflow: hidden;
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.16);
}

.card-header {
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.25rem 1.5rem;
  font-weight: 600;
}

.card-body {
  padding: 2rem;
}

.avatar-container {
  position: relative;
  display: inline-block;
}

.avatar-container img {
  border: 4px solid #fff;
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
  transition: all 0.3s ease;
}

.avatar-container:hover img {
  transform: scale(1.05);
  box-shadow: 0 12px 35px rgba(0,0,0,0.2);
}

.avatar-upload-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: 3px solid #fff;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

.avatar-upload-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.username-display {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.5rem;
  margin-top: 1rem;
}

.email-display {
  color: #6c757d;
  font-size: 1rem;
}

.badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
}

.badge.bg-danger {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
}

.badge.bg-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

.stat-box {
  padding: 1.5rem;
  border-radius: 12px;
  background: #f8f9fa;
  transition: all 0.3s ease;
}

.stat-box:hover {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

.stat-box h3 {
  margin-bottom: 0.5rem;
  font-weight: 700;
  font-size: 2.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-box p {
  font-weight: 500;
  color: #6c757d;
  margin: 0;
}

.form-label {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.form-control {
  border-radius: 12px;
  border: 2px solid #e9ecef;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  font-weight: 600;
  padding: 0.75rem 2rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.btn-primary:disabled {
  opacity: 0.7;
}

.btn-outline-danger {
  border: 2px solid #f5576c;
  color: #f5576c;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  transition: all 0.3s ease;
}

.btn-outline-danger:hover {
  background: #f5576c;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
}

/* 信息卡片样式 */
.info-card {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  transition: all 0.3s ease;
}

.info-card:hover {
  background: #ffffff;
  border-color: #dee2e6;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.info-label {
  font-size: 0.85rem;
  color: #6c757d;
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-content {
  color: #2c3e50;
  font-size: 1rem;
  line-height: 1.8;
  margin: 0;
  white-space: pre-wrap;
}

.badge.bg-light {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
  border: 1px solid #dee2e6;
  padding: 0.4rem 0.8rem;
  border-radius: 15px;
}

.d-flex.gap-2 {
  gap: 0.5rem;
}

/* 小统计盒子样式 */
.stat-box-small {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.stat-box-small:hover {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.stat-box-small h4 {
  margin: 0;
  font-weight: 700;
}

/* 等级徽章样式 */
.level-badge {
  font-size: 1rem;
  padding: 0.5rem 1.5rem;
  border-radius: 25px;
  font-weight: 700;
}

.level-badge-small {
  font-size: 0.85rem;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-weight: 600;
}

.level-novice {
  background: linear-gradient(135deg, #e0e0e0 0%, #bdbdbd 100%);
  color: #666;
}

.level-explorer {
  background: linear-gradient(135deg, #bbdefb 0%, #90caf9 100%);
  color: #1976d2;
}

.level-wanderer {
  background: linear-gradient(135deg, #c8e6c9 0%, #a5d6a7 100%);
  color: #388e3c;
}

.level-adventurer {
  background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%);
  color: #f57f17;
}

.level-master {
  background: linear-gradient(135deg, #ffeb3b 0%, #ffc107 100%);
  color: #f57f17;
}

@media (max-width: 768px) {
  .user-center-container {
    padding: 1rem 0;
  }
  
  h2 {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .card-body {
    padding: 1.5rem;
  }
  
  .stat-box h3 {
    font-size: 2rem;
  }
  
  .back-btn {
    top: 80px;
    left: 15px;
    width: 45px;
    height: 45px;
    font-size: 1.5rem;
  }
}
</style>

