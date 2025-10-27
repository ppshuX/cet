<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
    <div class="container-fluid">
      <!-- Logo -->
      <router-link to="/" class="navbar-brand">
        <strong>CET旅行平台</strong>
      </router-link>
      
      <!-- Toggle按钮（移动端） -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <!-- 导航项 -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link to="/" class="nav-link">
              <i class="bi bi-house-door me-1"></i>
              旅行列表
            </router-link>
          </li>
          <li class="nav-item">
            <a href="/api/docs/" target="_blank" class="nav-link">
              <i class="bi bi-book me-1"></i>
              API文档
            </a>
          </li>
        </ul>
        
        <!-- 右侧用户信息 -->
        <div class="d-flex align-items-center">
          <!-- 已登录 -->
          <template v-if="isLoggedIn">
            <div class="dropdown">
              <a
                href="#"
                class="d-flex align-items-center text-white text-decoration-none dropdown-toggle"
                id="dropdownUser"
                data-bs-toggle="dropdown"
              >
                <img
                  :src="avatar"
                  alt="avatar"
                  width="32"
                  height="32"
                  class="rounded-circle me-2"
                />
                <span>{{ username }}</span>
              </a>
              <ul class="dropdown-menu dropdown-menu-end text-small">
                <li>
                  <router-link to="/user/center" class="dropdown-item">
                    <i class="bi bi-person me-2"></i>个人中心
                  </router-link>
                </li>
                <li><hr class="dropdown-divider" /></li>
                <li>
                  <a href="#" class="dropdown-item" @click.prevent="handleLogout">
                    <i class="bi bi-box-arrow-right me-2"></i>退出登录
                  </a>
                </li>
              </ul>
            </div>
          </template>
          
          <!-- 未登录 -->
          <template v-else>
            <router-link to="/login" class="btn btn-outline-light btn-sm me-2">
              登录
            </router-link>
            <router-link to="/register" class="btn btn-light btn-sm">
              注册
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores'

export default {
  name: 'NavBar',
  
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    
    const isLoggedIn = computed(() => userStore.isLoggedIn)
    const username = computed(() => userStore.username)
    const avatar = computed(() => userStore.avatar)
    
    const handleLogout = async () => {
      if (!confirm('确定要退出登录吗？')) return
      
      try {
        await userStore.logout()
        router.push('/login')
      } catch (error) {
        console.error('退出失败:', error)
      }
    }
    
    return {
      isLoggedIn,
      username,
      avatar,
      handleLogout
    }
  }
}
</script>

<style scoped>
.navbar {
  border-bottom: 3px solid #0056b3;
}

.navbar-brand {
  font-size: 1.25rem;
}

.nav-link {
  color: rgba(255, 255, 255, 0.9) !important;
  transition: color 0.2s;
}

.nav-link:hover {
  color: white !important;
}

.dropdown-menu {
  min-width: 200px;
}

.dropdown-item {
  padding: 0.5rem 1rem;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}
</style>

