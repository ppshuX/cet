<template>
  <div class="card">
    <div class="card-body">
      <h3 class="mb-4">📍 打卡与留言</h3>
      
      <!-- 打卡按钮 -->
      <div class="checkin-section mb-4">
        <button
          class="btn btn-success btn-lg"
          @click="handleCheckin"
          :disabled="checking || hasCheckedIn"
        >
          <span v-if="checking" class="spinner-border spinner-border-sm me-2"></span>
          {{ checkinButtonText }}
        </button>
        <p v-if="hasCheckedIn" class="text-success mt-2 mb-0">
          ✅ 您已打卡成功！
        </p>
      </div>
      
      <!-- 发表评论表单 -->
      <div v-if="isAdmin" class="comment-form mb-4">
        <h5 class="mb-3">发表评论（仅管理员）</h5>
        <form @submit.prevent="handleSubmit">
          <div class="mb-3">
            <textarea
              v-model="formData.content"
              class="form-control"
              rows="4"
              placeholder="分享你的旅行故事..."
              required
            ></textarea>
          </div>
          
          <div class="row mb-3">
            <div class="col-md-6 mb-2">
              <label class="form-label">上传图片</label>
              <input
                type="file"
                class="form-control"
                accept="image/*"
                @change="handleImageChange"
              />
            </div>
            <div class="col-md-6 mb-2">
              <label class="form-label">上传视频</label>
              <input
                type="file"
                class="form-control"
                accept="video/*"
                @change="handleVideoChange"
              />
            </div>
          </div>
          
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="submitting"
          >
            <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
            {{ submitting ? '发布中...' : '发布评论' }}
          </button>
        </form>
      </div>
      
      <!-- 评论列表 -->
      <div class="comment-list">
        <h5 class="mb-3">评论列表 ({{ comments.length }}条)</h5>
        
        <div v-if="comments.length === 0" class="text-center text-muted py-4">
          暂无评论，快来留下第一条评论吧！
        </div>
        
        <div
          v-for="comment in comments"
          :key="comment.id"
          class="comment-item"
        >
          <div class="d-flex align-items-start">
            <img
              :src="getAvatarUrl(comment.user.profile?.avatar_url)"
              class="rounded-circle me-3"
              width="48"
              height="48"
              alt="avatar"
            />
            <div class="flex-grow-1">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <strong>{{ comment.user.username }}</strong>
                <div class="d-flex gap-2 align-items-center">
                  <small class="text-muted">{{ formatDate(comment.timestamp) }}</small>
                  <button
                    v-if="isAdmin"
                    class="btn btn-sm btn-danger"
                    @click="handleDelete(comment.id)"
                  >
                    删除
                  </button>
                </div>
              </div>
              
              <p class="mb-2">{{ comment.content }}</p>
              
              <!-- 图片 -->
              <div v-if="comment.image" class="mb-2">
                <img
                  :src="comment.image"
                  class="img-fluid rounded"
                  style="max-width: 300px; cursor: pointer;"
                  @click="showImageModal(comment.image)"
                  alt="评论图片"
                />
              </div>
              
              <!-- 视频 -->
              <div v-if="comment.video" class="mb-2">
                <video
                  :src="comment.video"
                  controls
                  class="rounded"
                  style="max-width: 400px;"
                >
                  您的浏览器不支持视频播放
                </video>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'CommentSection',
  
  props: {
    comments: {
      type: Array,
      default: () => []
    },
    isAdmin: {
      type: Boolean,
      default: false
    },
    hasCheckedIn: {
      type: Boolean,
      default: false
    },
    getAvatarUrl: {
      type: Function,
      required: true
    }
  },
  
  emits: ['checkin', 'submit-comment', 'delete-comment'],
  
  setup(props, { emit }) {
    const checking = ref(false)
    const submitting = ref(false)
    
    const formData = ref({
      content: '',
      image: null,
      video: null
    })
    
    const checkinButtonText = computed(() => {
      if (props.hasCheckedIn) return '✓ 已打卡'
      if (checking.value) return '打卡中...'
      return '📍 我来过这里'
    })
    
    const handleCheckin = async () => {
      checking.value = true
      try {
        await emit('checkin')
      } finally {
        setTimeout(() => {
          checking.value = false
        }, 500)
      }
    }
    
    const handleImageChange = (event) => {
      formData.value.image = event.target.files[0]
    }
    
    const handleVideoChange = (event) => {
      formData.value.video = event.target.files[0]
    }
    
    const handleSubmit = async () => {
      submitting.value = true
      try {
        await emit('submit-comment', {
          content: formData.value.content,
          image: formData.value.image,
          video: formData.value.video
        })
        
        // 重置表单
        formData.value = {
          content: '',
          image: null,
          video: null
        }
      } finally {
        submitting.value = false
      }
    }
    
    const handleDelete = (commentId) => {
      if (confirm('确定要删除这条评论吗？')) {
        emit('delete-comment', commentId)
      }
    }
    
    const formatDate = (dateStr) => {
      const date = new Date(dateStr)
      return date.toLocaleString('zh-CN')
    }
    
    const showImageModal = (url) => {
      window.open(url, '_blank')
    }
    
    return {
      checking,
      submitting,
      formData,
      checkinButtonText,
      handleCheckin,
      handleImageChange,
      handleVideoChange,
      handleSubmit,
      handleDelete,
      formatDate,
      showImageModal
    }
  }
}
</script>

<style scoped>
.card {
  background: #fff;
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
}

.card-body {
  padding: 2rem;
}

.card-body h3 {
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 600;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 0.8rem;
}

.checkin-section {
  text-align: center;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 12px;
}

.comment-form {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 12px;
}

.comment-item {
  background: #f0f0f0;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.comment-item:hover {
  background: #e8e8e8;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.comment-item:last-child {
  margin-bottom: 0;
}

.rounded-circle {
  border: 2px solid #e0e0e0;
  object-fit: cover;
}

@media (max-width: 768px) {
  .card-body {
    padding: 1.5rem;
  }
  
  .comment-item {
    padding: 1rem;
  }
}
</style>

