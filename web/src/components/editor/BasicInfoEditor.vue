<template>
  <div class="card mb-4">
    <div class="card-header">
      <h5 class="mb-0">📝 基本信息</h5>
    </div>
    <div class="card-body">
      <!-- 标题 -->
      <div class="mb-3">
        <label class="form-label">旅行标题 *</label>
        <input
          :value="modelValue.title"
          @input="$emit('update:modelValue', { ...modelValue, title: $event.target.value })"
          type="text"
          class="form-control"
          placeholder="例如：厦门三天两夜游"
          required
        />
      </div>
      
      <!-- 简介 -->
      <div class="mb-3">
        <label class="form-label">简介描述</label>
        <textarea
          :value="modelValue.description"
          @input="$emit('update:modelValue', { ...modelValue, description: $event.target.value })"
          class="form-control"
          rows="3"
          placeholder="简单描述你的旅行计划..."
        ></textarea>
      </div>
      
      <!-- 日期 -->
      <div class="row mb-3">
        <div class="col-md-6">
          <label class="form-label">开始日期</label>
          <input
            :value="modelValue.start_date"
            @input="$emit('update:modelValue', { ...modelValue, start_date: $event.target.value })"
            type="date"
            class="form-control"
          />
        </div>
        <div class="col-md-6">
          <label class="form-label">结束日期</label>
          <input
            :value="modelValue.end_date"
            @input="$emit('update:modelValue', { ...modelValue, end_date: $event.target.value })"
            type="date"
            class="form-control"
          />
        </div>
      </div>
      
      <!-- 图标和颜色 -->
      <div class="row mb-3">
        <div class="col-md-6">
          <label class="form-label">旅行图标</label>
          <div class="icon-selector">
            <button
              v-for="icon in iconOptions"
              :key="icon"
              type="button"
              class="icon-btn"
              :class="{ active: modelValue.icon === icon }"
              @click="$emit('update:modelValue', { ...modelValue, icon })"
            >
              {{ icon }}
            </button>
          </div>
        </div>
        <div class="col-md-6">
          <label class="form-label">主题颜色</label>
          <input
            :value="modelValue.theme_color"
            @input="$emit('update:modelValue', { ...modelValue, theme_color: $event.target.value })"
            type="color"
            class="form-control form-control-color"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BasicInfoEditor',
  
  props: {
    modelValue: {
      type: Object,
      required: true
    }
  },
  
  emits: ['update:modelValue'],
  
  setup() {
    const iconOptions = ['🏖️', '🌊', '🏙️', '🌄', '🌇', '🗺️', '✈️', '🚗', '🏔️', '🌴']
    
    return {
      iconOptions
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

.icon-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.icon-btn {
  width: 50px;
  height: 50px;
  border: 2px solid #e0e0e0;
  background: white;
  border-radius: 8px;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.icon-btn:hover {
  border-color: #667eea;
  transform: scale(1.1);
}

.icon-btn.active {
  border-color: #667eea;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transform: scale(1.1);
}
</style>

