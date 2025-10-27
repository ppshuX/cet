<template>
  <div class="trip-detail-container">
    <!-- 导航栏 -->
    <NavBar />
    
    <!-- 返回按钮 -->
    <button class="back-btn" @click="goBack" title="返回首页">
      🏠
    </button>
    
    <!-- 背景音乐按钮 -->
    <button class="music-btn" @click="toggleMusic" :title="isPlaying ? '暂停音乐' : '播放音乐'">
      {{ isPlaying ? '🔊' : '🔇' }}
    </button>
    
    <audio ref="audioPlayer" loop>
      <source :src="musicSrc" type="audio/mpeg">
    </audio>
    
    <div class="container py-5">
      <!-- Loading状态 -->
      <div v-if="loading" class="text-center">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">加载中...</span>
        </div>
      </div>
      
      <!-- 旅行详情 -->
      <div v-else-if="trip">
        <!-- 页面标题 -->
        <div class="card shadow-lg mb-4">
          <div class="card-body p-5">
            <h1 class="mb-3">{{ trip.name }}</h1>
            <p class="text-muted mb-0">{{ trip.description }}</p>
          </div>
        </div>
        
        <!-- 统计组件 ⭐ (仅旧页面) -->
        <TripStats
          v-if="trip.stats"
          :views="trip.stats.views"
          :likes="trip.stats.likes"
          @like="handleLike"
        />
        
        <!-- 旅行进度条组件 ⭐ -->
        <TripProgress
          v-if="(tripConfig && tripConfig.dates) || (trip.start_date && trip.end_date)"
          :start-date="tripConfig?.dates?.start || trip.start_date"
          :end-date="tripConfig?.dates?.end || trip.end_date"
        />
        
        <!-- 行程概览组件 ⭐ (动态内容) -->
        <TripOverview v-if="tripConfig && tripConfig.overview" title="行程概览">
          <!-- 基本信息 -->
          <div v-if="tripConfig.overview.basicInfo" class="basic-info-section">
            <h4>🧭 基本信息</h4>
            <div class="info-grid">
              <div v-if="tripConfig.overview.basicInfo.participants" class="info-item">
                <span class="info-label">👥 旅行人员：</span>
                <span class="info-value">{{ tripConfig.overview.basicInfo.participants }}</span>
              </div>
              <div v-if="tripConfig.overview.basicInfo.departure" class="info-item">
                <span class="info-label">🚩 出发地：</span>
                <span class="info-value">{{ tripConfig.overview.basicInfo.departure }}</span>
              </div>
              <div v-if="tripConfig.overview.basicInfo.destination" class="info-item">
                <span class="info-label">🎯 目的地：</span>
                <span class="info-value">{{ tripConfig.overview.basicInfo.destination }}</span>
              </div>
              <div v-if="tripConfig.overview.basicInfo.transport" class="info-item">
                <span class="info-label">🚗 交通方式：</span>
                <span class="info-value">{{ tripConfig.overview.basicInfo.transport }}</span>
              </div>
              <div v-if="tripConfig.overview.basicInfo.accommodation" class="info-item">
                <span class="info-label">🏨 住宿：</span>
                <span class="info-value">{{ tripConfig.overview.basicInfo.accommodation }}</span>
              </div>
              <div v-if="tripConfig.overview.basicInfo.duration" class="info-item">
                <span class="info-label">⏱️ 行程时长：</span>
                <span class="info-value">{{ tripConfig.overview.basicInfo.duration }}</span>
              </div>
              <div v-if="tripConfig.overview.basicInfo.budget" class="info-item">
                <span class="info-label">💰 预算：</span>
                <span class="info-value">{{ tripConfig.overview.basicInfo.budget }}</span>
              </div>
              <div v-if="tripConfig.overview.basicInfo.theme" class="info-item">
                <span class="info-label">🎨 主题：</span>
                <span class="info-value">{{ tripConfig.overview.basicInfo.theme }}</span>
              </div>
            </div>
          </div>

          <!-- 行程亮点 -->
          <h4>📍 行程亮点</h4>
          <ul class="highlights-list">
            <li v-for="(highlight, index) in tripConfig.overview.highlights" :key="index">
              {{ highlight }}
            </li>
          </ul>
          
          <!-- 行程安排 -->
          <h4>🗓️ 详细行程</h4>
          <div class="itinerary-section">
            <div v-for="(item, index) in tripConfig.overview.itinerary" :key="index" class="itinerary-item">
              <div class="itinerary-header">
                <strong class="itinerary-day">{{ item.day }}</strong>
                <span v-if="item.time" class="itinerary-time">⏰ {{ item.time }}</span>
              </div>
              <div class="itinerary-content">{{ item.content }}</div>
              <div v-if="item.highlight" class="itinerary-highlight">
                {{ item.highlight }}
              </div>
            </div>
          </div>
          
          <!-- 预算参考 -->
          <h4>💰 预算参考</h4>
          <table>
            <thead>
              <tr>
                <th>项目</th>
                <th>金额（元）</th>
                <th>备注</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in tripConfig.overview.budget.items" :key="index">
                <td>{{ item.name }}</td>
                <td>¥{{ item.amount }}</td>
                <td>{{ item.note }}</td>
              </tr>
              <tr class="total-row">
                <td><strong>总计</strong></td>
                <td><strong>¥{{ tripConfig.overview.budget.total }}</strong></td>
                <td>人均预算</td>
              </tr>
            </tbody>
          </table>

          <!-- 实用提示 -->
          <div v-if="tripConfig.overview.tips && tripConfig.overview.tips.length" class="tips-section">
            <h4>💡 实用提示</h4>
            <ul class="tips-list">
              <li v-for="(tip, index) in tripConfig.overview.tips" :key="index">
                {{ tip }}
              </li>
            </ul>
          </div>
        </TripOverview>
        
        <!-- 如果没有配置，显示默认内容 -->
        <TripOverview v-else title="行程概览">
          <p class="text-muted text-center">行程内容正在筹划中，敬请期待...</p>
        </TripOverview>
        
        <!-- 评论区组件 ⭐ -->
        <CommentSection
          :comments="comments"
          :is-admin="isAdmin"
          :has-checked-in="trip.stats?.checked_in || false"
          :get-avatar-url="getAvatarUrl"
          @checkin="handleCheckin"
          @submit-comment="handleSubmitComment"
          @delete-comment="handleDeleteComment"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores'
import { getTripDetail, likeTrip, checkinTrip } from '@/api/trip'
import { getCommentList, createComment, deleteComment } from '@/api/comment'
import { getAvatarUrl } from '@/config/api'
import { getTripConfig } from '@/config/tripConfig'
import NavBar from '@/components/NavBar.vue'
import TripProgress from '@/components/TripProgress.vue'
import TripStats from '@/components/TripStats.vue'
import TripOverview from '@/components/TripOverview.vue'
import CommentSection from '@/components/CommentSection.vue'

export default {
  name: 'TripDetailView',
  
  components: {
    NavBar,
    TripProgress,
    TripStats,
    TripOverview,
    CommentSection
  },
  
  setup() {
    const route = useRoute()
    const router = useRouter()
    const userStore = useUserStore()
    
    const trip = ref(null)
    const comments = ref([])
    const loading = ref(true)
    const tripConfig = ref(null)
    
    // 音乐相关
    const isPlaying = ref(false)
    const audioPlayer = ref(null)
    const musicSrc = computed(() => {
      // 根据不同的旅行页面返回不同的音乐
      const slug = route.params.slug
      const musicMap = {
        'trip': '/static/music/rain.mp3',
        'trip1': '/static/music/windy.mp3',
        'trip2': '/static/music/windy.mp3',
        'trip3': '/static/music/windy.mp3',
        'trip4': '/static/music/road.mp3'
      }
      return musicMap[slug] || '/static/music/rain.mp3'
    })
    
    const isAdmin = computed(() => userStore.isAdmin)
    
    // 获取旅行详情
    const fetchTripDetail = async () => {
      const slug = route.params.slug
      try {
        trip.value = await getTripDetail(slug)
        
        // 如果是新Trip模型，不需要getTripConfig
        // 如果是旧SiteStat模型，使用getTripConfig
        if (trip.value.overview) {
          // 新Trip模型，已经有完整的配置和数据
          tripConfig.value = {
            dates: {
              start: trip.value.start_date,
              end: trip.value.end_date
            },
            overview: trip.value.overview
          }
        } else {
          // 旧SiteStat模型，使用静态配置
          tripConfig.value = getTripConfig(slug)
        }
      } catch (error) {
        console.error('获取旅行详情失败:', error)
        if (error.response?.status === 404 || error.status === 404) {
          alert('旅行页面不存在')
          router.push('/')
        }
      }
    }
    
    // 获取评论列表
    const fetchComments = async () => {
      const slug = route.params.slug
      try {
        const data = await getCommentList({ trip: slug })
        comments.value = data.results || data || []
      } catch (error) {
        console.error('获取评论列表失败:', error)
        comments.value = []
      } finally {
        loading.value = false
      }
    }
    
    // 点赞
    const handleLike = async () => {
      try {
        const result = await likeTrip(route.params.slug)
        trip.value.stats.likes = result.likes
        alert('点赞成功！')
      } catch (error) {
        console.error('点赞失败:', error)
        alert('点赞失败，请稍后重试')
      }
    }
    
    // 打卡
    const handleCheckin = async () => {
      try {
        await checkinTrip(route.params.slug)
        alert('打卡成功！')
        await fetchTripDetail() // 刷新数据以更新打卡状态
      } catch (error) {
        console.error('打卡失败:', error)
        alert('打卡失败，请稍后重试')
      }
    }
    
    // 提交评论（接收组件传来的数据）
    const handleSubmitComment = async (commentData) => {
      try {
        const formData = new FormData()
        formData.append('page', route.params.slug)
        
        if (commentData.content) {
          formData.append('content', commentData.content)
        }
        if (commentData.image) {
          formData.append('image', commentData.image)
        }
        if (commentData.video) {
          formData.append('video', commentData.video)
        }
        
        await createComment(formData)
        alert('评论发表成功！')
        await fetchComments()
      } catch (error) {
        console.error('发表评论失败:', error)
        alert('发表评论失败：' + error.message)
      }
    }
    
    // 删除评论
    const handleDeleteComment = async (commentId) => {
      try {
        await deleteComment(commentId)
        alert('删除成功！')
        await fetchComments()
      } catch (error) {
        console.error('删除评论失败:', error)
        alert('删除失败，请稍后重试')
      }
    }
    
    // 返回按钮
    const goBack = () => {
      router.push('/')
    }
    
    // 音乐控制
    const toggleMusic = async () => {
      if (!audioPlayer.value) return
      
      if (isPlaying.value) {
        audioPlayer.value.pause()
      } else {
        try {
          audioPlayer.value.volume = 0.3 // 降低音量
          await audioPlayer.value.play()
        } catch (error) {
          console.error('播放音乐失败:', error)
        }
      }
      isPlaying.value = !isPlaying.value
    }
    
    onMounted(async () => {
      await fetchTripDetail()
      await fetchComments()
    })
    
    return {
      trip,
      comments,
      loading,
      tripConfig,
      isAdmin,
      isPlaying,
      audioPlayer,
      musicSrc,
      handleLike,
      handleCheckin,
      handleSubmitComment,
      handleDeleteComment,
      goBack,
      toggleMusic,
      getAvatarUrl
    }
  }
}
</script>

<style scoped>
.trip-detail-container {
  min-height: 100vh;
  background: #f0e68c;  /* 厦门旅行页面的浅黄色背景 */
  font-family: 'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  line-height: 1.8;
  color: #333;
  padding-bottom: 40px;
}

/* 卡片样式 */
:deep(.card) {
  background: #fff;
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
  overflow: hidden;
}

:deep(.card-body) {
  padding: 2rem;
}

/* 统计卡片 */
.stat-card {
  text-align: center;
  padding: 1.5rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.stat-card:hover {
  background: #f9f9f9;
  transform: translateY(-3px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 0.3rem;
}

.stat-label {
  color: #666;
  font-size: 0.95rem;
}

/* 操作按钮 */
:deep(.btn-primary) {
  background-color: #3498db;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

:deep(.btn-primary:hover) {
  background-color: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

:deep(.btn-success) {
  background-color: #2ecc71;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

:deep(.btn-success:hover) {
  background-color: #27ae60;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3);
}

/* 评论区域 */
.comment-item {
  background: #f0f0f0;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
  border: none;
}

.comment-item:hover {
  background: #e8e8e8;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.comment-item:last-child {
  margin-bottom: 0;
}

/* 表单控件 */
:deep(.form-control),
:deep(.form-select),
:deep(textarea) {
  border-radius: 8px;
  border: 1px solid #ccc;
  padding: 0.7rem 1rem;
  transition: all 0.3s ease;
}

:deep(.form-control:focus),
:deep(.form-select:focus),
:deep(textarea:focus) {
  border-color: #3498db;
  box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
  outline: none;
}

:deep(textarea) {
  min-height: 100px;
  resize: vertical;
}

/* 头像 */
:deep(.rounded-circle) {
  border: 2px solid #e0e0e0;
  object-fit: cover;
}

/* 删除按钮 */
:deep(.btn-danger) {
  background-color: #c0392b;
  border: none;
  border-radius: 6px;
  padding: 0.4rem 0.8rem;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

:deep(.btn-danger:hover) {
  background-color: #a02818;
  transform: scale(1.05);
}

/* 表格样式（如需要） */
:deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

:deep(table), :deep(th), :deep(td) {
  border: 1px solid #ccc;
}

:deep(th), :deep(td) {
  padding: 0.75rem;
  text-align: left;
}

:deep(th) {
  background-color: #f0f0f0;
  font-weight: 600;
}

/* 基本信息区域 */
.basic-info-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 12px;
  border: 1px solid #e0e0e0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  padding: 0.8rem;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.info-label {
  font-weight: 600;
  color: #555;
  margin-bottom: 0.3rem;
  font-size: 0.9rem;
}

.info-value {
  color: #2c3e50;
  font-size: 1rem;
}

/* 行程亮点列表 */
.highlights-list {
  list-style: none;
  padding-left: 0;
}

.highlights-list li {
  padding: 0.8rem 1rem;
  margin-bottom: 0.8rem;
  background: linear-gradient(90deg, #f8f9fa 0%, #ffffff 100%);
  border-left: 4px solid #3498db;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.highlights-list li:hover {
  background: linear-gradient(90deg, #e8f4fd 0%, #f8f9fa 100%);
  border-left-color: #2980b9;
  transform: translateX(5px);
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.15);
}

/* 详细行程区域 */
.itinerary-section {
  margin-top: 1rem;
}

.itinerary-item {
  padding: 1.2rem;
  margin-bottom: 1.5rem;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.itinerary-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.itinerary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
  padding-bottom: 0.6rem;
  border-bottom: 2px solid #f0f0f0;
}

.itinerary-day {
  color: #2c3e50;
  font-size: 1.1rem;
}

.itinerary-time {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.itinerary-content {
  line-height: 1.8;
  color: #555;
  margin-bottom: 0.8rem;
}

.itinerary-highlight {
  padding: 0.6rem 1rem;
  background: linear-gradient(90deg, #e8f4fd 0%, #f0f8ff 100%);
  border-left: 3px solid #3498db;
  border-radius: 6px;
  color: #2c3e50;
  font-size: 0.95rem;
  margin-top: 0.8rem;
}

/* 实用提示区域 */
.tips-section {
  margin-top: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #fff8dc 0%, #fffaed 100%);
  border-radius: 12px;
  border: 1px solid #f0e68c;
}

.tips-list {
  list-style: none;
  padding-left: 0;
  margin-top: 1rem;
}

.tips-list li {
  padding: 0.6rem 0.8rem;
  margin-bottom: 0.6rem;
  background: #fff;
  border-radius: 6px;
  border-left: 3px solid #f39c12;
  color: #555;
  transition: all 0.2s ease;
}

.tips-list li:hover {
  background: #fffbf0;
  transform: translateX(3px);
}

/* 预算表格总计行 */
.total-row {
  font-weight: bold;
  background-color: #f9f9f9;
  border-top: 2px solid #3498db;
}

.total-row td {
  color: #2c3e50;
  font-size: 1.05rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  :deep(.card-body) {
    padding: 1.5rem;
  }
  
  .stat-card {
    padding: 1rem;
  }
  
  .stat-icon {
    font-size: 2rem;
  }
  
  .stat-value {
    font-size: 1.5rem;
  }
  
  .comment-item {
    padding: 1rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .basic-info-section {
    padding: 1rem;
  }
  
  .highlights-list li {
    padding: 0.6rem 0.8rem;
    font-size: 0.95rem;
  }
  
  .itinerary-item {
    padding: 1rem;
  }
  
  .itinerary-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.3rem;
  }
  
  .itinerary-time {
    font-size: 0.85rem;
  }
  
  .itinerary-content {
    font-size: 0.95rem;
  }
  
  .tips-section {
    padding: 1rem;
  }
  
  .tips-list li {
    font-size: 0.9rem;
  }
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

/* 音乐按钮 */
.music-btn {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background: rgba(255, 255, 255, 0.95);
  border: none;
  border-radius: 50%;
  width: 56px;
  height: 56px;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.7;
}

.music-btn:hover {
  background: white;
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  opacity: 1;
}

/* 移动端按钮适配 */
@media (max-width: 768px) {
  .back-btn {
    top: 80px;
    left: 15px;
    width: 45px;
    height: 45px;
    font-size: 1.5rem;
  }
  
  .music-btn {
    bottom: 20px;
    right: 20px;
    width: 50px;
    height: 50px;
    font-size: 20px;
  }
}
</style>

