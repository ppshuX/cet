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
      
      <!-- 主题色 -->
      <div class="mb-3">
        <label class="form-label">🎨 主题色</label>
        <div class="color-picker">
          <input 
            type="color" 
            :value="modelValue.theme_color || '#f0e68c'"
            @input="$emit('update:modelValue', { ...modelValue, theme_color: $event.target.value })"
            class="form-control form-control-color"
          />
          <div class="color-preview" :style="{ background: modelValue.theme_color || '#f0e68c' }"></div>
        </div>
        <small class="text-muted">选择卡片头部的背景色</small>
      </div>
      
      <!-- 背景音乐 -->
      <div class="mb-3">
        <label class="form-label">🎵 背景音乐</label>
        <select 
          :value="modelValue.background_music"
          @change="$emit('update:modelValue', { ...modelValue, background_music: $event.target.value })"
          class="form-select"
        >
          <option value="">无背景音乐</option>
          <option value="/static/music/rain.mp3">BGM 1</option>
          <option value="/static/music/road.mp3">BGM 2</option>
          <option value="/static/music/windy.mp3">BGM 3</option>
        </select>
        <small class="text-muted">选择适合旅行场景的背景音乐</small>

        <!-- 预览控制 -->
        <div class="mt-2 d-flex align-items-center gap-2">
          <button type="button" class="btn btn-sm btn-outline-primary" :disabled="!hasMusic" @click="togglePreview">
            {{ isPreviewPlaying ? '暂停预览' : '预览播放' }}
          </button>
          <small class="text-muted" v-if="!hasMusic">未选择音乐</small>
        </div>
        <audio ref="previewAudio" :src="modelValue.background_music || ''" preload="auto"></audio>
      </div>
      
      <!-- 图标 -->
      <div class="mb-3">
        <label class="form-label">📍 图标</label>
        <input 
          type="text" 
          :value="modelValue.icon"
          @input="$emit('update:modelValue', { ...modelValue, icon: $event.target.value })"
          class="form-control"
          placeholder="例如：🗺️"
        />
        <small class="text-muted">使用emoji表情</small>
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
import { ref, computed, watch } from 'vue'
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
  
  setup(props) {
    const formatDate = (dateStr) => {
      if (!dateStr) return '暂无'
      const date = new Date(dateStr)
      return date.toLocaleString('zh-CN')
    }
    // 音乐预览
    const previewAudio = ref(null)
    const isPreviewPlaying = ref(false)
    const hasMusic = computed(() => !!props.modelValue.background_music)
    const stopIfPlaying = () => {
      if (previewAudio.value) {
        try {
          previewAudio.value.pause()
        } catch (e) {
          // ignore pause errors
          void e
        }
        isPreviewPlaying.value = false
      }
    }
    const togglePreview = () => {
      if (!hasMusic.value || !previewAudio.value) return
      if (isPreviewPlaying.value) {
        previewAudio.value.pause()
        isPreviewPlaying.value = false
      } else {
        previewAudio.value.currentTime = 0
        previewAudio.value.volume = 0.2
        previewAudio.value.play().then(() => {
          isPreviewPlaying.value = true
        }).catch(() => { return null })
      }
    }
    watch(() => props.modelValue.background_music, () => {
      // 音乐切换时停止并重新加载资源
      stopIfPlaying()
      if (previewAudio.value) {
        try { previewAudio.value.load() } catch (e) { void e }
      }
    })

    // 同步播放状态
    const attachListeners = () => {
      if (!previewAudio.value) return
      previewAudio.value.addEventListener('ended', () => { isPreviewPlaying.value = false })
      previewAudio.value.addEventListener('pause', () => { isPreviewPlaying.value = false })
      previewAudio.value.addEventListener('play', () => { 
        previewAudio.value.volume = 0.2
        isPreviewPlaying.value = true 
      })
    }
    setTimeout(attachListeners, 0)
    
    return {
      formatDate,
      previewAudio,
      isPreviewPlaying,
      hasMusic,
      togglePreview
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

.color-picker {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-control-color {
  width: 60px;
  height: 38px;
  padding: 0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.color-preview {
  width: 80px;
  height: 38px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

@media (max-width: 991px) {
  .card.sticky-top {
    position: relative !important;
    top: 0 !important;
  }
}
</style>

