<template>
  <div class="trip-detail-container" :style="{ background: (trip && trip.theme_color) || '#f0e68c' }">
    <!-- 导航栏 -->
    <NavBar />
    
    <!-- 返回按钮 -->
    <button class="back-btn" @click="goBack" title="返回首页">
      🏠
    </button>
    
    <!-- 跳转到评论按钮（右上角） -->
    <button class="scroll-btn" @click="scrollToComments" title="跳到评论区">
      ⬇️
    </button>
    
    <!-- 背景音乐按钮 -->
    <button class="music-btn" @click="toggleMusic" :title="isPlaying ? '暂停音乐' : '播放音乐'">
      {{ isPlaying ? '🔊' : '🔇' }}
    </button>
    
    <audio ref="audioPlayer" :src="musicSrc || ''" preload="auto" loop></audio>
    
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
            <h1 class="mb-3">{{ trip.name || trip.title }}</h1>
            <p class="text-muted mb-0">{{ trip.description }}</p>
          </div>
        </div>
        
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
                <span class="info-label">👥 Roamioer：</span>
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
          <div v-if="tripConfig.overview.budget && tripConfig.overview.budget.items">
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
          </div>

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
        
        <!-- 统计组件：显示浏览量与点赞；若无统计则显示0并禁用点赞（移动至评论区上方） -->
        <TripStats
          :views="trip.stats?.views || 0"
          :likes="trip.stats?.likes || 0"
          :can-like="trip.overview ? (trip.visibility === 'public') : true"
          @like="handleLike"
        />

        <!-- 评论区组件 ⭐ -->
        <CommentSection
          ref="commentSectionRef"
          :comments="comments"
          :is-admin="isAdmin"
          :is-author="isAuthor"
          :get-avatar-url="getAvatarUrl"
          @submit-comment="handleSubmitComment"
          @delete-comment="handleDeleteComment"
          @add-image="handleAddImage"
          @update-comment="handleUpdateComment"
          @submit-reply="handleSubmitReply"
          @load-replies="handleLoadReplies"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores'
import { getTripDetail, likeTrip, getTripStats, getTripPlanStats, likeTripPlan, viewTripPlan } from '@/api/trip'
import { getCommentList, createComment, deleteComment, addCommentImage, updateComment, getCommentReplies } from '@/api/comment'
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
      // 显式选择“无背景音乐”时返回空字符串；未设置时使用默认雨声
      const bg = trip.value?.background_music
      if (bg === '') return ''
      return bg || '/static/music/rain.mp3'
    })
    
    const isAdmin = computed(() => userStore.isAdmin)
    
    // 判断是否为旅行作者
    const isAuthor = computed(() => {
      return trip.value?.author?.id === userStore.userInfo?.id
    })
    
    // 获取旅行详情
    const fetchTripDetail = async () => {
      const slug = route.params.slug
      try {
        trip.value = await getTripDetail(slug)
        // 确保有stats对象用于前端展示
        if (!trip.value.stats) {
          trip.value.stats = { views: 0, likes: 0 }
        }
        
        // 如果是新Trip模型，不需要getTripConfig
        // 如果是旧SiteStat模型，使用getTripConfig
        if (trip.value.overview) {
          // 新Trip模型，已经有完整的配置和数据
          // 处理 budget.summary -> budget.total 的兼容性
          const overview = { ...trip.value.overview }
          if (overview.budget && overview.budget.summary) {
            overview.budget.total = overview.budget.summary
          }
          
          tripConfig.value = {
            dates: {
              start: trip.value.start_date,
              end: trip.value.end_date
            },
            overview
          }
        } else {
          // 旧SiteStat模型，使用静态配置
          tripConfig.value = getTripConfig(slug)
        }
        // 首次获取实时统计
        try {
          let stats
          if (trip.value && trip.value.overview) {
            stats = await getTripPlanStats(slug)
          } else {
            stats = await getTripStats(slug)
          }
          if (stats) {
            trip.value.stats = { views: stats.views, likes: stats.likes }
          }
        } catch (e) { /* ignore */ }
        
        // 更新页面标题为旅行名称（去掉平台后缀）
        if (trip.value?.name || trip.value?.title) {
          document.title = `${trip.value.name || trip.value.title}`
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
        const slug = route.params.slug
        let result
        if (trip.value && trip.value.overview) {
          result = await likeTripPlan(slug)
        } else {
          result = await likeTrip(slug)
        }
        if (trip.value.stats) {
          trip.value.stats.likes = result.likes
        }
        alert('点赞成功！')
      } catch (error) {
        console.error('点赞失败:', error)
        alert('点赞失败，请稍后重试')
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
      // 删除前提示确认
      if (!confirm('确定要删除这条内容吗？删除后无法恢复。')) {
        return
      }
      
      // 先向后端发送删除请求
      try {
        await deleteComment(commentId)
      } catch (error) {
        console.error('删除评论失败:', error)
        const errorMsg = error.response?.data?.detail || error.message || '删除失败，请稍后重试'
        alert(errorMsg)
        return
      }
      
      // 删除成功后，从UI中移除
      const deletedComment = comments.value.find(c => c.id === commentId)
      
      if (!deletedComment) {
        // 如果是回复，从replyLists中删除
        for (const comment of comments.value) {
          if (commentSectionRef.value && commentSectionRef.value.replyLists) {
            const replyList = commentSectionRef.value.replyLists[comment.id]
            if (replyList && replyList.some(r => r.id === commentId)) {
              const filteredReplies = replyList.filter(r => r.id !== commentId)
              if (commentSectionRef.value.updateReplyList) {
                commentSectionRef.value.updateReplyList(comment.id, filteredReplies)
              }
              return
            }
          }
        }
        return
      }
      
      const isReply = !!deletedComment.parent_id
      const parentId = deletedComment.parent_id
      let parentComment = null
      
      if (isReply) {
        // 这是回复的删除
        parentComment = comments.value.find(c => c.id === parentId)
        if (parentComment && parentComment.replies) {
          // 立即从UI中移除
          parentComment.replies = parentComment.replies.filter(r => r.id !== commentId)
          // 更新CommentSection的replyLists
          if (commentSectionRef.value && commentSectionRef.value.updateReplyList) {
            commentSectionRef.value.updateReplyList(parentId, parentComment.replies)
          }
        }
      } else {
        // 这是顶层评论的删除，从列表中立即移除
        comments.value = comments.value.filter(c => c.id !== commentId)
      }
    }
    
    // 添加图片
    const handleAddImage = async ({ commentId, file }) => {
      try {
        const formData = new FormData()
        formData.append('image', file)
        
        await addCommentImage(commentId, formData)
        alert('图片添加成功！')
        await fetchComments()
      } catch (error) {
        console.error('添加图片失败:', error)
        alert('添加图片失败：' + (error.response?.data?.detail || error.message))
      }
    }
    
    // 更新评论
    const handleUpdateComment = async ({ commentId, content }) => {
      try {
        await updateComment(commentId, { content })
        alert('评论更新成功！')
        await fetchComments()
      } catch (error) {
        console.error('更新评论失败:', error)
        alert('更新评论失败：' + (error.response?.data?.detail || error.message))
      }
    }
    
    // 提交回复
    const handleSubmitReply = async ({ commentId, content }) => {
      try {
        const formData = new FormData()
        formData.append('content', content)
        formData.append('page', route.params.slug)
        formData.append('parent', commentId)  // 设置父评论ID
        
        await createComment(formData)
        alert('回复成功！')
        // 提交成功后重新加载该评论的回复列表
        await handleLoadReplies(commentId)
      } catch (error) {
        console.error('提交回复失败:', error)
        alert('提交回复失败：' + (error.response?.data?.detail || error.message))
      }
    }
    
    // 保存commentSectionRef用于直接访问子组件
    const commentSectionRef = ref(null)
    
    // 加载回复列表
    const handleLoadReplies = async (commentId) => {
      try {
        const replies = await getCommentReplies(commentId)
        
        // 将回复列表保存到comments数组中对应评论的replies属性
        const comment = comments.value.find(c => c.id === commentId)
        if (comment) {
          comment.replies = replies || []
        }
        
        // 等待下一个tick，确保ref已经初始化
        await new Promise(resolve => setTimeout(resolve, 100))
        
        // 更新CommentSection组件的replyLists
        if (commentSectionRef.value && commentSectionRef.value.updateReplyList) {
          commentSectionRef.value.updateReplyList(commentId, replies || [])
        }
      } catch (error) {
        console.error(`加载评论 ${commentId} 的回复列表失败:`, error)
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
    
    // 滚动到评论区
    const scrollToComments = () => {
      // 优先使用组件根元素滚动
      if (commentSectionRef.value && commentSectionRef.value.$el) {
        commentSectionRef.value.$el.scrollIntoView({ behavior: 'smooth', block: 'start' })
        return
      }
      // 回退：根据页面上第一个评论列表容器滚动
      const el = document.querySelector('.comment-list')
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
    
    // 当音乐源变化时，重新加载并在需要时继续播放
    watch(musicSrc, async () => {
      if (!audioPlayer.value) return
      try { audioPlayer.value.load() } catch (e) { /* ignore */ }
      if (isPlaying.value) {
        try {
          audioPlayer.value.volume = 0.3
          await audioPlayer.value.play()
        } catch (e) { /* ignore */ }
      }
    })

    let statsTimer = null
    onMounted(async () => {
      await fetchTripDetail()
      await fetchComments()
      // 公开行程记录一次浏览
      try {
        const slug = route.params.slug
        if (trip.value && trip.value.overview && trip.value.visibility === 'public') {
          await viewTripPlan(slug)
        }
      } catch (e) {
        // ignore view errors
      }
      // 统计轮询（不增加浏览量）
      statsTimer = setInterval(async () => {
        try {
          const slug = route.params.slug
          let stats
          if (trip.value && trip.value.overview) {
            stats = await getTripPlanStats(slug)
          } else {
            stats = await getTripStats(slug)
          }
          if (trip.value) {
            if (!trip.value.stats) trip.value.stats = { views: 0, likes: 0 }
            trip.value.stats.views = stats.views
            trip.value.stats.likes = stats.likes
          }
        } catch (e) {
          // ignore when stats not available
        }
      }, 15000)
    })

    onUnmounted(() => {
      if (statsTimer) clearInterval(statsTimer)
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
      commentSectionRef,
      handleLike,
      handleSubmitComment,
      handleDeleteComment,
      handleAddImage,
      handleUpdateComment,
      handleSubmitReply,
      handleLoadReplies,
      goBack,
      toggleMusic,
      scrollToComments,
      getAvatarUrl,
      isAuthor
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

/* 跳转到评论按钮 */
.scroll-btn {
  position: fixed;
  top: 100px;
  right: 20px;
  background: linear-gradient(135deg, #ffffff 0%, #f7f7ff 100%);
  border: 2px solid rgba(0, 0, 0, 0.05);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 1.4rem;
  cursor: pointer;
  z-index: 1000;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  opacity: 0.8;
}

.scroll-btn:hover {
  transform: translateY(2px) scale(1.05);
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

