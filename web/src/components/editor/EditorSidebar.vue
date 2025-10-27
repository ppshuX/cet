<template>
  <div class="card mb-4 sticky-top" style="top: 140px;">
    <div class="card-header">
      <h5 class="mb-0">⚙️ 设置</h5>
    </div>
    <div class="card-body">
      <!-- 状态 -->
      <div class="mb-3">
        <label class="form-label">状态</label>
        <select 
          :value="modelValue.status" 
          @change="$emit('update:modelValue', { ...modelValue, status: $event.target.value })"
          class="form-select"
        >
          <option value="draft">草稿</option>
          <option value="published">已发布</option>
        </select>
      </div>
      
      <!-- 可见性 -->
      <div class="mb-3">
        <label class="form-label">可见性</label>
        <select 
          :value="modelValue.visibility" 
          @change="$emit('update:modelValue', { ...modelValue, visibility: $event.target.value })"
          class="form-select"
        >
          <option value="private">私有</option>
          <option value="public">公开</option>
        </select>
        <small class="text-muted">公开后其他人可以看到你的旅行计划</small>
      </div>
      
      <!-- 信息统计 -->
      <div class="info-stats mt-4">
        <div v-if="modelValue.created_at" class="stat-item">
          <span class="label">创建时间</span>
          <span class="value">{{ formatDate(modelValue.created_at) }}</span>
        </div>
        <div v-if="modelValue.updated_at" class="stat-item">
          <span class="label">更新时间</span>
          <span class="value">{{ formatDate(modelValue.updated_at) }}</span>
        </div>
        <div v-if="daysCount > 0" class="stat-item">
          <span class="label">旅行天数</span>
          <span class="value">{{ daysCount }}天</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditorSidebar',
  
  props: {
    modelValue: {
      type: Object,
      required: true
    },
    daysCount: {
      type: Number,
      default: 0
    }
  },
  
  emits: ['update:modelValue'],
  
  setup() {
    const formatDate = (dateStr) => {
      if (!dateStr) return '暂无'
      const date = new Date(dateStr)
      return date.toLocaleString('zh-CN')
    }
    
    return {
      formatDate
    }
  }
}
</script>

<style scoped>
.card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem 1.5rem;
}

.card-header h5 {
  margin: 0;
  font-weight: 600;
}

.info-stats {
  border-top: 1px solid #e0e0e0;
  padding-top: 1rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.stat-item .label {
  color: #666;
  font-size: 0.9rem;
}

.stat-item .value {
  color: #2c3e50;
  font-weight: 600;
  font-size: 0.9rem;
}

@media (max-width: 991px) {
  .card.sticky-top {
    position: relative !important;
    top: 0 !important;
  }
}
</style>

