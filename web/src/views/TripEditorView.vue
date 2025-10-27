<template>
  <div class="editor-wrapper">
    <NavBar />
    
    <div class="editor-container">
      <!-- 顶部工具栏 -->
      <div class="editor-toolbar">
        <div class="container-fluid">
          <div class="d-flex justify-content-between align-items-center py-3">
            <div>
              <button class="btn btn-outline-secondary me-2" @click="goBack">
                <i class="bi bi-arrow-left me-1"></i>返回
              </button>
              <h5 class="d-inline-block mb-0 ms-3">
                {{ isEditMode ? '编辑旅行计划' : '创建旅行计划' }}
              </h5>
            </div>
            <div>
              <button 
                class="btn btn-outline-primary me-2" 
                @click="handleSave"
                :disabled="saving"
              >
                <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
                <i v-else class="bi bi-save me-1"></i>
                保存草稿
              </button>
              <button 
                class="btn btn-primary" 
                @click="handlePublish"
                :disabled="publishing || !canPublish"
              >
                <span v-if="publishing" class="spinner-border spinner-border-sm me-1"></span>
                <i v-else class="bi bi-send me-1"></i>
                发布
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 主编辑区 -->
      <div class="container py-4">
        <div class="row">
          <!-- 左侧：编辑面板 -->
          <div class="col-lg-8">
            <div class="edit-panel">
              <!-- 基本信息 -->
              <div class="card mb-4">
                <div class="card-header">
                  <h5 class="mb-0">📝 基本信息</h5>
                </div>
                <div class="card-body">
                  <!-- 标题 -->
                  <div class="mb-3">
                    <label class="form-label">旅行标题 *</label>
                    <input
                      v-model="tripData.title"
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
                      v-model="tripData.description"
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
                        v-model="tripData.start_date"
                        type="date"
                        class="form-control"
                      />
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">结束日期</label>
                      <input
                        v-model="tripData.end_date"
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
                          :class="{ active: tripData.icon === icon }"
                          @click="tripData.icon = icon"
                        >
                          {{ icon }}
                        </button>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <label class="form-label">主题颜色</label>
                      <input
                        v-model="tripData.theme_color"
                        type="color"
                        class="form-control form-control-color"
                      />
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 模块选择器 -->
              <div class="card mb-4">
                <div class="card-header">
                  <h5 class="mb-0">🧩 选择模块</h5>
                </div>
                <div class="card-body">
                  <p class="text-muted mb-3">选择你想在旅行计划中展示的内容模块</p>
                  <div class="modules-grid">
                    <div
                      v-for="module in availableModules"
                      :key="module.id"
                      class="module-card"
                      :class="{ active: isModuleEnabled(module.id) }"
                      @click="toggleModule(module.id)"
                    >
                      <div class="module-icon">{{ module.icon }}</div>
                      <div class="module-name">{{ module.name }}</div>
                      <div class="module-desc">{{ module.description }}</div>
                      <div class="module-check">
                        <i v-if="isModuleEnabled(module.id)" class="bi bi-check-circle-fill text-success"></i>
                        <i v-else class="bi bi-circle text-muted"></i>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 内容编辑区（根据启用的模块显示） -->
              <div v-if="isModuleEnabled('basicInfo')" class="card mb-4">
                <div class="card-header">
                  <h5 class="mb-0">ℹ️ 基本信息</h5>
                </div>
                <div class="card-body">
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label class="form-label">出发地</label>
                      <input v-model="tripData.overview.basicInfo.departure" type="text" class="form-control" />
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label">目的地</label>
                      <input v-model="tripData.overview.basicInfo.destination" type="text" class="form-control" />
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label">交通方式</label>
                      <input v-model="tripData.overview.basicInfo.transport" type="text" class="form-control" placeholder="例如：高铁往返" />
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label">住宿安排</label>
                      <input v-model="tripData.overview.basicInfo.accommodation" type="text" class="form-control" />
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 行程亮点 -->
              <div v-if="isModuleEnabled('highlights')" class="card mb-4">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h5 class="mb-0">✨ 行程亮点</h5>
                  <button class="btn btn-sm btn-primary" @click="addHighlight">
                    <i class="bi bi-plus-circle me-1"></i>添加
                  </button>
                </div>
                <div class="card-body">
                  <div v-for="(highlight, index) in tripData.overview.highlights" :key="index" class="mb-3">
                    <div class="input-group">
                      <input
                        v-model="tripData.overview.highlights[index]"
                        type="text"
                        class="form-control"
                        placeholder="例如：🏖️ 厦门植物园 - 热带雨林奇观"
                      />
                      <button class="btn btn-outline-danger" @click="removeHighlight(index)">
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </div>
                  <p v-if="tripData.overview.highlights.length === 0" class="text-muted text-center py-3 mb-0">
                    暂无亮点，点击上方"添加"按钮添加行程亮点
                  </p>
                </div>
              </div>
              
              <!-- 详细行程 -->
              <div v-if="isModuleEnabled('itinerary')" class="card mb-4">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h5 class="mb-0">📅 详细行程</h5>
                  <button class="btn btn-sm btn-primary" @click="addItinerary">
                    <i class="bi bi-plus-circle me-1"></i>添加一天
                  </button>
                </div>
                <div class="card-body">
                  <div v-for="(item, index) in tripData.overview.itinerary" :key="index" class="itinerary-item mb-4">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                      <h6>第{{ index + 1 }}天</h6>
                      <button class="btn btn-sm btn-outline-danger" @click="removeItinerary(index)">
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                    <div class="mb-2">
                      <label class="form-label small">日期标题</label>
                      <input
                        v-model="item.day"
                        type="text"
                        class="form-control form-control-sm"
                        placeholder="例如：第一天（6月22日）"
                      />
                    </div>
                    <div class="mb-2">
                      <label class="form-label small">时间</label>
                      <input
                        v-model="item.time"
                        type="text"
                        class="form-control form-control-sm"
                        placeholder="例如：09:00-18:00"
                      />
                    </div>
                    <div class="mb-2">
                      <label class="form-label small">详细内容</label>
                      <textarea
                        v-model="item.content"
                        class="form-control form-control-sm"
                        rows="3"
                        placeholder="详细的行程安排..."
                      ></textarea>
                    </div>
                    <div>
                      <label class="form-label small">亮点</label>
                      <input
                        v-model="item.highlight"
                        type="text"
                        class="form-control form-control-sm"
                        placeholder="例如：🏖️ 海滩美景"
                      />
                    </div>
                  </div>
                  <p v-if="tripData.overview.itinerary.length === 0" class="text-muted text-center py-3 mb-0">
                    暂无行程，点击上方"添加一天"按钮开始规划
                  </p>
                </div>
              </div>
              
              <!-- 预算参考 -->
              <div v-if="isModuleEnabled('budget')" class="card mb-4">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h5 class="mb-0">💰 预算参考</h5>
                  <button class="btn btn-sm btn-primary" @click="addBudgetItem">
                    <i class="bi bi-plus-circle me-1"></i>添加
                  </button>
                </div>
                <div class="card-body">
                  <div v-for="(item, index) in tripData.overview.budget.items" :key="index" class="row mb-3">
                    <div class="col-md-4">
                      <input
                        v-model="item.name"
                        type="text"
                        class="form-control form-control-sm"
                        placeholder="项目名称"
                      />
                    </div>
                    <div class="col-md-3">
                      <input
                        v-model.number="item.amount"
                        type="number"
                        class="form-control form-control-sm"
                        placeholder="金额"
                      />
                    </div>
                    <div class="col-md-4">
                      <input
                        v-model="item.note"
                        type="text"
                        class="form-control form-control-sm"
                        placeholder="备注"
                      />
                    </div>
                    <div class="col-md-1">
                      <button class="btn btn-sm btn-outline-danger w-100" @click="removeBudgetItem(index)">
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </div>
                  <div class="alert alert-info mt-3">
                    <strong>总计：</strong>¥{{ budgetTotal }}
                  </div>
                </div>
              </div>
              
              <!-- 实用提示 -->
              <div v-if="isModuleEnabled('tips')" class="card mb-4">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h5 class="mb-0">💡 实用提示</h5>
                  <button class="btn btn-sm btn-primary" @click="addTip">
                    <i class="bi bi-plus-circle me-1"></i>添加
                  </button>
                </div>
                <div class="card-body">
                  <div v-for="(tip, index) in tripData.overview.tips" :key="index" class="mb-3">
                    <div class="input-group">
                      <textarea
                        v-model="tripData.overview.tips[index]"
                        class="form-control"
                        rows="2"
                        placeholder="输入一条实用提示..."
                      ></textarea>
                      <button class="btn btn-outline-danger" @click="removeTip(index)">
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </div>
                  <p v-if="tripData.overview.tips.length === 0" class="text-muted text-center py-3 mb-0">
                    暂无提示，点击上方"添加"按钮添加实用提示
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 右侧：预览和设置 -->
          <div class="col-lg-4">
            <!-- 设置面板 -->
            <div class="card mb-4 sticky-top" style="top: 100px;">
              <div class="card-header">
                <h5 class="mb-0">⚙️ 设置</h5>
              </div>
              <div class="card-body">
                <!-- 状态 -->
                <div class="mb-3">
                  <label class="form-label">状态</label>
                  <select v-model="tripData.status" class="form-select">
                    <option value="draft">草稿</option>
                    <option value="published">已发布</option>
                  </select>
                </div>
                
                <!-- 可见性 -->
                <div class="mb-3">
                  <label class="form-label">可见性</label>
                  <select v-model="tripData.visibility" class="form-select">
                    <option value="private">私有</option>
                    <option value="public">公开</option>
                  </select>
                  <small class="text-muted">公开后其他人可以看到你的旅行计划</small>
                </div>
                
                <!-- 信息统计 -->
                <div class="info-stats mt-4">
                  <div class="stat-item">
                    <span class="label">创建时间</span>
                    <span class="value">{{ formatDate(tripData.created_at) }}</span>
                  </div>
                  <div v-if="tripData.updated_at" class="stat-item">
                    <span class="label">更新时间</span>
                    <span class="value">{{ formatDate(tripData.updated_at) }}</span>
                  </div>
                  <div v-if="tripData.start_date && tripData.end_date" class="stat-item">
                    <span class="label">旅行天数</span>
                    <span class="value">{{ daysCount }}天</span>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores'
import { getTripPlan, createTripPlan, updateTripPlan } from '@/api/tripPlan'
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'TripEditorView',
  
  components: {
    NavBar
  },
  
  setup() {
    const route = useRoute()
    const router = useRouter()
    const userStore = useUserStore()
    
    const saving = ref(false)
    const publishing = ref(false)
    
    // 图标选项
    const iconOptions = ['🏖️', '🌊', '🏙️', '🌄', '🌇', '🗺️', '✈️', '🚗', '🏔️', '🌴']
    
    // 可用模块
    const availableModules = [
      { id: 'basicInfo', name: '基本信息', icon: 'ℹ️', description: '出发地、目的地等' },
      { id: 'highlights', name: '行程亮点', icon: '✨', description: '主要景点和活动' },
      { id: 'itinerary', name: '详细行程', icon: '📅', description: '每日安排' },
      { id: 'budget', name: '预算参考', icon: '💰', description: '费用明细' },
      { id: 'tips', name: '实用提示', icon: '💡', description: '注意事项' },
    ]
    
    // 旅行数据
    const tripData = ref({
      title: '',
      description: '',
      icon: '🗺️',
      start_date: null,
      end_date: null,
      status: 'draft',
      visibility: 'private',
      theme_color: '#f0e68c',
      background_music: '',
      config: {
        enabledModules: ['basicInfo', 'highlights']
      },
      overview: {
        basicInfo: {
          departure: '',
          destination: '',
          transport: '',
          accommodation: ''
        },
        highlights: [],
        itinerary: [],
        budget: {
          items: [],
          total: 0
        },
        tips: []
      },
      created_at: null,
      updated_at: null
    })
    
    const isEditMode = computed(() => !!route.params.slug)
    
    const canPublish = computed(() => {
      return tripData.value.title && tripData.value.title.trim().length > 0
    })
    
    const daysCount = computed(() => {
      if (!tripData.value.start_date || !tripData.value.end_date) return 0
      const start = new Date(tripData.value.start_date)
      const end = new Date(tripData.value.end_date)
      return Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1
    })
    
    const budgetTotal = computed(() => {
      return tripData.value.overview.budget.items.reduce((sum, item) => sum + (item.amount || 0), 0)
    })
    
    // 模块管理
    const isModuleEnabled = (moduleId) => {
      return tripData.value.config.enabledModules.includes(moduleId)
    }
    
    const toggleModule = (moduleId) => {
      const index = tripData.value.config.enabledModules.indexOf(moduleId)
      if (index > -1) {
        tripData.value.config.enabledModules.splice(index, 1)
      } else {
        tripData.value.config.enabledModules.push(moduleId)
      }
    }
    
    // 亮点管理
    const addHighlight = () => {
      tripData.value.overview.highlights.push('')
    }
    
    const removeHighlight = (index) => {
      tripData.value.overview.highlights.splice(index, 1)
    }
    
    // 行程管理
    const addItinerary = () => {
      tripData.value.overview.itinerary.push({
        day: '',
        time: '',
        content: '',
        highlight: ''
      })
    }
    
    const removeItinerary = (index) => {
      tripData.value.overview.itinerary.splice(index, 1)
    }
    
    // 预算管理
    const addBudgetItem = () => {
      tripData.value.overview.budget.items.push({
        name: '',
        amount: 0,
        note: ''
      })
    }
    
    const removeBudgetItem = (index) => {
      tripData.value.overview.budget.items.splice(index, 1)
    }
    
    // 提示管理
    const addTip = () => {
      tripData.value.overview.tips.push('')
    }
    
    const removeTip = (index) => {
      tripData.value.overview.tips.splice(index, 1)
    }
    
    // 保存
    const handleSave = async () => {
      if (!canPublish.value) {
        alert('请至少填写标题')
        return
      }
      
      saving.value = true
      try {
        // 更新预算总计
        tripData.value.overview.budget.total = budgetTotal.value
        
        if (isEditMode.value) {
          await updateTripPlan(route.params.slug, tripData.value)
          alert('保存成功！')
        } else {
          const result = await createTripPlan(tripData.value)
          alert('创建成功！')
          router.push(`/editor/${result.slug}`)
        }
      } catch (error) {
        console.error('保存失败:', error)
        alert('保存失败：' + (error.response?.data?.detail || error.message))
      } finally {
        saving.value = false
      }
    }
    
    // 发布
    const handlePublish = async () => {
      if (!canPublish.value) {
        alert('请至少填写标题')
        return
      }
      
      if (!confirm('确定要发布这个旅行计划吗？发布后将可以被其他用户看到。')) {
        return
      }
      
      publishing.value = true
      try {
        tripData.value.status = 'published'
        tripData.value.overview.budget.total = budgetTotal.value
        
        if (isEditMode.value) {
          await updateTripPlan(route.params.slug, tripData.value)
        } else {
          const result = await createTripPlan(tripData.value)
          router.push(`/editor/${result.slug}`)
        }
        
        alert('发布成功！')
      } catch (error) {
        console.error('发布失败:', error)
        alert('发布失败：' + (error.response?.data?.detail || error.message))
      } finally {
        publishing.value = false
      }
    }
    
    const goBack = () => {
      if (confirm('确定要离开吗？未保存的更改将丢失。')) {
        router.push('/my-trips')
      }
    }
    
    const formatDate = (dateStr) => {
      if (!dateStr) return '暂无'
      const date = new Date(dateStr)
      return date.toLocaleString('zh-CN')
    }
    
    // 加载数据
    const loadTripData = async () => {
      if (isEditMode.value) {
        try {
          const data = await getTripPlan(route.params.slug)
          tripData.value = data
        } catch (error) {
          console.error('加载失败:', error)
          alert('加载旅行计划失败')
          router.push('/my-trips')
        }
      }
    }
    
    onMounted(() => {
      if (!userStore.isLoggedIn) {
        alert('请先登录')
        router.push('/login')
        return
      }
      loadTripData()
    })
    
    return {
      tripData,
      saving,
      publishing,
      isEditMode,
      canPublish,
      daysCount,
      budgetTotal,
      iconOptions,
      availableModules,
      isModuleEnabled,
      toggleModule,
      addHighlight,
      removeHighlight,
      addItinerary,
      removeItinerary,
      addBudgetItem,
      removeBudgetItem,
      addTip,
      removeTip,
      handleSave,
      handlePublish,
      goBack,
      formatDate
    }
  }
}
</script>

<style scoped>
.editor-wrapper {
  min-height: 100vh;
  background: #f5f7fa;
}

.editor-container {
  padding-top: 60px;
}

.editor-toolbar {
  position: fixed;
  top: 60px;
  left: 0;
  right: 0;
  background: white;
  border-bottom: 1px solid #e0e0e0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.edit-panel .card {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  overflow: hidden;
}

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

/* 图标选择器 */
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

/* 模块网格 */
.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
}

.module-card {
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.module-card:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.module-card.active {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
}

.module-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.module-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.module-desc {
  font-size: 0.85rem;
  color: #666;
}

.module-check {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  font-size: 1.2rem;
}

/* 行程项样式 */
.itinerary-item {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  background: #f8f9fa;
}

/* 信息统计 */
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

/* 响应式 */
@media (max-width: 991px) {
  .editor-container {
    padding-top: 120px;
  }
  
  .card.sticky-top {
    position: relative !important;
    top: 0 !important;
  }
}
</style>

