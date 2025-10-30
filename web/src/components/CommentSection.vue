<template>
  <div class="card">
    <div class="card-body">
      <h3 class="mb-4">🌳 Roamio Stories.</h3>
      
      <!-- 发表评论入口（仅作者可见） -->
      <div v-if="isAuthor" class="mb-3">
        <button
          v-if="!showForm"
          class="btn btn-outline-primary"
          @click="showForm = true"
        >
          ✍️ 记录一下
        </button>
        <button
          v-else
          class="btn btn-outline-secondary mb-3"
          @click="showForm = false"
        >
          取消记录
        </button>
      </div>
      <CommentForm
        v-if="isAuthor && showForm"
        :submitting="submitting"
        @submit="handleSubmit"
      />
      
      <!-- 评论列表 -->
      <div class="comment-list">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5 class="mb-0">记录列表 ({{ comments.length }}条)</h5>
          <!-- 管理评论模式切换按钮 -->
          <button
            v-if="hasManageableComments"
            class="btn btn-sm"
            :class="isManageMode ? 'btn-secondary' : 'btn-outline-secondary'"
            @click="toggleManageMode"
            title="管理评论"
          >
            {{ isManageMode ? '完成管理' : '管理评论' }}
          </button>
        </div>
        
        <div v-if="comments.length === 0" class="text-center text-muted py-4">
          暂无记录，快来留下你的旅行脚印吧！
        </div>
        
        <CommentItem
          v-for="comment in comments"
          :key="comment.id"
          :comment="comment"
          :editing="editingComments[comment.id] !== undefined && editingComments[comment.id] !== false"
          :is-expanded="expandedReplies[comment.id] || false"
          :reply-count="(replyLists[comment.id] || []).length"
          :replies="replyLists[comment.id] || []"
          :get-avatar-url="getAvatarUrl"
          @show-image-modal="showImageModal"
          @toggle-reply="toggleReplySection"
          @update:content="(content) => updateLocalContent(comment.id, content)"
        >
          <!-- 操作按钮插槽 -->
          <template #actions>
                  <template v-if="isManageMode">
                    <!-- 编辑模式按钮 -->
                    <button
                      v-if="comment.can_delete && !editingComments[comment.id]"
                      class="btn btn-sm btn-outline-primary"
                      @click="startEditing(comment.id, comment.content)"
                      title="编辑评论"
                    >
                      ✏️
                    </button>
                    <!-- 保存按钮 -->
                    <button
                      v-if="editingComments[comment.id]"
                      class="btn btn-sm btn-success"
                      @click="handleSaveComment(comment.id)"
                      title="保存修改"
                    >
                      ✓
                    </button>
              <!-- 添加/替换图片按钮 -->
                    <button
                      v-if="canAddImage(comment) && editingComments[comment.id]"
                      class="btn btn-sm btn-outline-success"
                      @click="handleAddImage(comment.id)"
                      :title="comment.image ? '替换图片' : '添加图片'"
                    >
                      📷
                    </button>
                    <!-- 取消编辑按钮 -->
                    <button
                      v-if="editingComments[comment.id]"
                      class="btn btn-sm btn-outline-secondary"
                      @click="cancelEditing(comment.id)"
                      title="取消"
                    >
                      ✕
                    </button>
              <!-- 删除按钮 -->
                    <button
                      v-if="comment.can_delete"
                      class="btn btn-sm btn-outline-danger"
                      @click="handleDelete(comment.id)"
                      title="删除这条评论"
                    >
                      🗑️
                    </button>
                  </template>
          </template>
          
          <!-- 回复区域插槽 -->
          <template #replies>
            <ReplySection
              v-if="expandedReplies[comment.id]"
              :expanded="expandedReplies[comment.id]"
              :replies="replyLists[comment.id] || []"
              :submitting="submittingReply[comment.id] || false"
              :get-avatar-url="getAvatarUrl"
              @submit="(content) => handleSubmitReply(comment.id, content)"
              @cancel="() => cancelReply(comment.id)"
              @delete-reply="handleDeleteReply"
            />
          </template>
        </CommentItem>
      </div>
    </div>
    
    <!-- 图片放大模态框 -->
    <div v-if="showModal" class="image-modal" @click="closeImageModal">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="closeImageModal">✕</button>
        <img :src="modalImageUrl" alt="放大图片" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import CommentForm from './comments/CommentForm.vue'
import CommentItem from './comments/CommentItem.vue'
import ReplySection from './comments/ReplySection.vue'

export default {
  name: 'CommentSection',
  
  components: {
    CommentForm,
    CommentItem,
    ReplySection
  },
  
  props: {
    comments: {
      type: Array,
      default: () => []
    },
    isAdmin: {
      type: Boolean,
      default: false
    },
    isAuthor: {
      type: Boolean,
      default: false
    },
    getAvatarUrl: {
      type: Function,
      required: true
    }
  },
  
  emits: ['submit-comment', 'delete-comment', 'add-image', 'update-comment', 'submit-reply', 'load-replies'],
  
  setup(props, { emit }) {
    const submitting = ref(false)
    const showForm = ref(false)
    const editingComments = ref({})
    const isManageMode = ref(false)
    const showModal = ref(false)
    const modalImageUrl = ref('')
    
    // 回复功能相关
    const expandedReplies = ref({})
    const replyForms = ref({})
    const submittingReply = ref({})
    const replyLists = ref({})
    const replyCounts = ref({})
    
    // 计算属性
    const hasManageableComments = computed(() => {
      return props.comments.some(comment => comment.can_delete)
    })
    
    
    // 提交评论
    const handleSubmit = async (commentData) => {
      submitting.value = true
      try {
        await emit('submit-comment', commentData)
      } finally {
        submitting.value = false
      }
    }
    
    // 删除评论
    const handleDelete = (commentId) => {
      emit('delete-comment', commentId)
    }
    
    // 显示/关闭图片模态框
    const showImageModal = (url) => {
      modalImageUrl.value = url
      showModal.value = true
    }
    
    const closeImageModal = () => {
      showModal.value = false
      modalImageUrl.value = ''
    }
    
    // 可以添加图片的判断
    const canAddImage = (comment) => {
      return !comment.video && comment.can_delete
    }
    
    // 编辑相关
    const startEditing = (commentId, originalContent) => {
      editingComments.value[commentId] = {
        isEditing: true,
        content: originalContent
      }
    }
    
    const cancelEditing = (commentId) => {
      editingComments.value[commentId] = false
    }
    
    const updateLocalContent = (commentId, content) => {
      if (editingComments.value[commentId]) {
        editingComments.value[commentId].content = content
      }
    }
    
    const handleSaveComment = (commentId) => {
      const editedContent = editingComments.value[commentId]?.content
      if (editedContent && editedContent.trim()) {
        emit('update-comment', {
          commentId,
          content: editedContent.trim()
        })
        editingComments.value[commentId] = false
      }
    }
    
    // 管理相关
    const toggleManageMode = () => {
      isManageMode.value = !isManageMode.value
      if (!isManageMode.value) {
        editingComments.value = {}
      }
    }
    
    // 添加图片
    const handleAddImage = (commentId) => {
      const input = document.createElement('input')
      input.type = 'file'
      input.accept = 'image/*'
      input.onchange = (e) => {
        const file = e.target.files[0]
        if (file) {
          emit('add-image', { commentId, file })
          editingComments.value[commentId] = false
        }
      }
      input.click()
    }
    
    // 回复相关
    const toggleReplySection = (commentId) => {
      expandedReplies.value[commentId] = !expandedReplies.value[commentId]
      
      if (expandedReplies.value[commentId]) {
        // 初始化相关状态
        if (!replyForms.value[commentId]) {
          replyForms.value[commentId] = { content: '' }
        }
        if (submittingReply.value[commentId] === undefined) {
          submittingReply.value[commentId] = false
        }
        if (!replyLists.value[commentId]) {
          replyLists.value[commentId] = []
          // 立即加载回复列表
          emit('load-replies', commentId)
        }
      }
    }
    
    const handleSubmitReply = async (commentId, content) => {
      submittingReply.value[commentId] = true
      try {
        await emit('submit-reply', {
          commentId,
          content
        })
        replyForms.value[commentId].content = ''
        // 提交成功后，父组件会调用load-replies，这里不需要重复加载
      } catch (error) {
        console.error('提交回复失败:', error)
        alert('提交回复失败')
      } finally {
        submittingReply.value[commentId] = false
      }
    }
    
    const cancelReply = (commentId) => {
      replyForms.value[commentId].content = ''
    }
    
    // 处理删除回复
    const handleDeleteReply = (replyId) => {
      emit('delete-comment', replyId)
    }
    
    // 从外部更新回复列表的方法（暴露给父组件调用）
    const updateReplyList = (commentId, replies) => {
      // 使用Vue的响应式更新
      replyLists.value = {
        ...replyLists.value,
        [commentId]: replies || []
      }
    }
    
    return {
      submitting,
      showForm,
      editingComments,
      isManageMode,
      hasManageableComments,
      expandedReplies,
      replyForms,
      submittingReply,
      replyLists,
      replyCounts,
      showModal,
      modalImageUrl,
      handleSubmit,
      handleDelete,
      showImageModal,
      closeImageModal,
      canAddImage,
      startEditing,
      cancelEditing,
      updateLocalContent,
      handleSaveComment,
      toggleManageMode,
      handleAddImage,
      toggleReplySection,
      handleSubmitReply,
      cancelReply,
      handleDeleteReply,
      updateReplyList
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

.comment-list {
  margin-top: 2rem;
}

/* 模态框样式 */
.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  cursor: pointer;
  animation: fadeIn 0.2s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  cursor: default;
  animation: zoomIn 0.2s ease-in;
}

@keyframes zoomIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.modal-content img {
  max-width: 100%;
  max-height: 90vh;
  width: auto;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
  object-fit: contain;
}

.close-button {
  position: absolute;
  top: -40px;
  right: 0;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  color: #333;
}

.close-button:hover {
  background: rgba(255, 255, 255, 1);
  transform: rotate(90deg);
}

/* 按钮透明度 */
.btn-outline-danger,
.btn-outline-success,
.btn-outline-primary,
.btn-outline-secondary {
  opacity: 0.7;
  transition: all 0.3s ease;
}

.btn-outline-danger:hover,
.btn-outline-success:hover,
.btn-outline-primary:hover,
.btn-outline-secondary:hover {
  opacity: 1;
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .card-body {
    padding: 1rem;
  }
  
  .card-body h3 {
    font-size: 1.1rem;
    padding-bottom: 0.5rem;
  }
  
  .checkin-section {
    padding: 1rem;
  }
  
  .modal-content {
    max-width: 95vw;
  }
  
  .close-button {
    top: -35px;
    width: 32px;
    height: 32px;
    font-size: 18px;
  }
}
</style>