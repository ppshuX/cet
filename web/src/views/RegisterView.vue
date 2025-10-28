<template>
  <div class="register-container">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="card shadow">
            <div class="card-body p-5">
              <h2 class="text-center mb-4">用户注册</h2>
              
              <!-- 错误提示 -->
              <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
              </div>
              
              <!-- 成功提示 -->
              <div v-if="successMessage" class="alert alert-success">
                {{ successMessage }}
              </div>
              
              <form @submit.prevent="handleRegister">
                <!-- 用户名 -->
                <div class="mb-3">
                  <label for="username" class="form-label">用户名</label>
                  <input
                    type="text"
                    class="form-control"
                    id="username"
                    v-model="formData.username"
                    required
                    :disabled="submitting"
                    placeholder="请输入用户名"
                  />
                  <div v-if="errors.username" class="text-danger small mt-1">
                    {{ errors.username }}
                  </div>
                </div>
                
                <!-- 邮箱（可选） -->
                <div class="mb-3">
                  <label for="email" class="form-label">邮箱（可选）</label>
                  <input
                    type="email"
                    class="form-control"
                    id="email"
                    v-model="formData.email"
                    :disabled="submitting"
                    placeholder="请输入邮箱"
                  />
                  <div v-if="errors.email" class="text-danger small mt-1">
                    {{ errors.email }}
                  </div>
                </div>
                
                <!-- 密码 -->
                <div class="mb-3">
                  <label for="password" class="form-label">密码</label>
                  <input
                    type="password"
                    class="form-control"
                    id="password"
                    v-model="formData.password"
                    required
                    :disabled="submitting"
                    placeholder="请输入密码"
                  />
                  <div v-if="errors.password" class="text-danger small mt-1">
                    {{ errors.password }}
                  </div>
                  <small class="text-muted">
                    密码至少8位，包含字母和数字
                  </small>
                </div>
                
                <!-- 确认密码 -->
                <div class="mb-4">
                  <label for="password2" class="form-label">确认密码</label>
                  <input
                    type="password"
                    class="form-control"
                    id="password2"
                    v-model="formData.password2"
                    required
                    :disabled="submitting"
                    placeholder="请再次输入密码"
                  />
                  <div v-if="errors.password2" class="text-danger small mt-1">
                    {{ errors.password2 }}
                  </div>
                </div>
                
                <!-- 提交按钮 -->
                <button
                  type="submit"
                  class="btn btn-primary w-100 mb-3"
                  :disabled="submitting"
                >
                  <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
                  {{ submitting ? '注册中...' : '注册' }}
                </button>
                
                <!-- 登录链接 -->
                <div class="text-center">
                  <span class="text-muted">已有账号？</span>
                  <router-link to="/login" class="text-decoration-none">
                    立即登录
                  </router-link>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores'

export default {
  name: 'RegisterView',
  
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    
    const formData = ref({
      username: '',
      email: '',
      password: '',
      password2: ''
    })
    
    const errors = ref({})
    const errorMessage = ref('')
    const successMessage = ref('')
    const submitting = ref(false)
    
    // 表单验证
    const validateForm = () => {
      errors.value = {}
      
      if (!formData.value.username) {
        errors.value.username = '请输入用户名'
        return false
      }
      
      if (formData.value.username.length < 3) {
        errors.value.username = '用户名至少3个字符'
        return false
      }
      
      if (!formData.value.password) {
        errors.value.password = '请输入密码'
        return false
      }
      
      if (formData.value.password.length < 8) {
        errors.value.password = '密码至少8位'
        return false
      }
      
      if (!formData.value.password2) {
        errors.value.password2 = '请再次输入密码'
        return false
      }
      
      if (formData.value.password !== formData.value.password2) {
        errors.value.password2 = '两次密码不一致'
        return false
      }
      
      return true
    }
    
    // 处理注册
    const handleRegister = async () => {
      errorMessage.value = ''
      successMessage.value = ''
      
      if (!validateForm()) {
        return
      }
      
      submitting.value = true
      
      try {
        await userStore.register({
          username: formData.value.username,
          email: formData.value.email || undefined,
          password: formData.value.password,
          password2: formData.value.password2
        })
        
        successMessage.value = '注册成功！正在跳转...'
        
        // 2秒后跳转到首页
        setTimeout(() => {
          router.push('/')
        }, 2000)
        
      } catch (error) {
        console.error('注册失败:', error)
        
        // 处理错误信息
        if (error.response?.data) {
          const data = error.response.data
          
          // 如果是字段错误
          if (typeof data === 'object') {
            if (data.username) {
              errors.value.username = Array.isArray(data.username) ? data.username[0] : data.username
            }
            if (data.email) {
              errors.value.email = Array.isArray(data.email) ? data.email[0] : data.email
            }
            if (data.password) {
              errors.value.password = Array.isArray(data.password) ? data.password[0] : data.password
            }
            if (data.password2) {
              errors.value.password2 = Array.isArray(data.password2) ? data.password2[0] : data.password2
            }
            
            // 处理非字段错误
            if (data.non_field_errors) {
              errorMessage.value = Array.isArray(data.non_field_errors) ? data.non_field_errors[0] : data.non_field_errors
            }
            
            // 如果有通用错误消息
            if (!errorMessage.value && (data.detail || data.message || data.error)) {
              errorMessage.value = data.detail || data.message || data.error
            }
            
            if (!errorMessage.value) {
              errorMessage.value = '注册失败，请稍后重试'
            }
          } else {
            errorMessage.value = '注册失败，请稍后重试'
          }
        } else {
          errorMessage.value = '网络错误，请检查网络连接'
        }
      } finally {
        submitting.value = false
      }
    }
    
    return {
      formData,
      errors,
      errorMessage,
      successMessage,
      submitting,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
}

.card {
  border: none;
  border-radius: 15px;
}

.card-body {
  background: white;
  border-radius: 15px;
}

h2 {
  color: #333;
  font-weight: 600;
}

.form-label {
  font-weight: 500;
  color: #555;
}

.form-control {
  border-radius: 8px;
  padding: 12px;
  border: 1px solid #ddd;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 8px;
  padding: 12px;
  font-weight: 600;
  transition: transform 0.2s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.alert {
  border-radius: 8px;
}
</style>

