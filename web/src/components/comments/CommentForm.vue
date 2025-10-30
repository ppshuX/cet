<template>
  <div class="comment-form mb-4">
    <h5 class="mb-3">记录一下</h5>
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
        {{ submitting ? '记录中...' : '记录一下' }}
      </button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'CommentForm',
  
  props: {
    submitting: {
      type: Boolean,
      default: false
    }
  },
  
  emits: ['submit'],
  
  setup(props, { emit }) {
    const formData = ref({
      content: '',
      image: null,
      video: null
    })
    
    const handleImageChange = (event) => {
      formData.value.image = event.target.files[0]
    }
    
    const handleVideoChange = (event) => {
      formData.value.video = event.target.files[0]
    }
    
    const handleSubmit = () => {
      emit('submit', {
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
    }
    
    return {
      formData,
      handleImageChange,
      handleVideoChange,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.comment-form {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 12px;
}

@media (max-width: 768px) {
  .comment-form {
    padding: 1rem;
  }
  
  .comment-form textarea {
    font-size: 14px;
    min-height: 80px;
  }
  
  .comment-form input[type="file"] {
    font-size: 14px;
  }
}
</style>
