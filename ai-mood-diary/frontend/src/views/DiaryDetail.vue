<template>
  <div class="page-wrapper">
    <div class="page-content" v-loading="loading">
      <div v-if="diary" class="detail-card">
        <div class="detail-header">
          <h2>{{ diary.title || '无标题' }}</h2>
          <div class="meta-info">
            <span class="date">{{ diary.date }}</span>
            <span class="mood-badge" :class="moodType(diary.mood_tag)">
              {{ moodLabel(diary.mood_tag) }}
            </span>
            <span v-if="diary.weather" class="weather">{{ diary.weather }}</span>
          </div>
        </div>
        
        <div class="content">
          {{ diary.content }}
        </div>

        <div class="divider"></div>

        <div v-if="aiStatus === 'completed'" class="emotion-card">
          <h3>AI 情绪分析</h3>
          <div class="emotion-item">
            <span class="emotion-label">情绪：</span>
            <span class="emotion-value">{{ emotionLabel(emotion.emotion_label) }}</span>
            <span class="emotion-score">（强度：{{ emotion.emotion_score }}）</span>
          </div>
          <div class="emotion-item">
            <span class="emotion-label">分析：</span>
            <span class="emotion-text">{{ emotion.analysis_detail }}</span>
          </div>
          <div class="emotion-item">
            <span class="emotion-label">建议：</span>
            <span class="emotion-text">{{ emotion.suggestion }}</span>
          </div>
        </div>
        <div v-else-if="aiStatus === 'unavailable'" class="emotion-card unavailable">
          <h3>AI 情绪分析</h3>
          <p class="unavailable-text">AI暂不可用</p>
        </div>
        <div v-else class="emotion-card loading">
          <p>AI 情绪分析正在生成中，请稍后查看...</p>
        </div>

        <div class="action-buttons">
          <NeonButton variant="primary" @click="$router.push(`/diary/${diary.id}/edit`)">编辑</NeonButton>
          <NeonButton variant="secondary" @click="$router.back()">返回</NeonButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { diaryAPI } from '../api/diary'

const route = useRoute()
const loading = ref(true)
const diary = ref(null)
const emotion = ref(null)
const aiStatus = ref('pending')

const moodMap = { 
  happy: ['mood-happy', '快乐'], 
  sad: ['mood-sad', '悲伤'], 
  anxious: ['mood-anxious', '焦虑'], 
  calm: ['mood-calm', '平静'], 
  angry: ['mood-angry', '愤怒'], 
  surprised: ['mood-surprised', '惊讶'] 
}
function moodType(tag) { return moodMap[tag]?.[0] || '' }
function moodLabel(tag) { return moodMap[tag]?.[1] || tag || '未标记' }
function emotionLabel(tag) { return moodMap[tag]?.[1] || tag || '未知' }

onMounted(async () => {
  try {
    const res = await diaryAPI.get(route.params.id)
    diary.value = res.diary
    emotion.value = res.emotion
    aiStatus.value = res.ai_status || 'pending'
  } catch (err) { /* ignore */ }
  loading.value = false
})
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  background: transparent;
}

.page-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px 20px;
}

.detail-card {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 32px;
}

.detail-header {
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.detail-header h2 {
  margin: 0 0 12px 0;
  color: #fff;
  font-size: 24px;
}

.meta-info {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.date { color: rgba(255, 255, 255, 0.5); font-size: 14px; }
.weather { color: rgba(255, 255, 255, 0.7); font-size: 14px; }

.content {
  white-space: pre-wrap;
  line-height: 1.8;
  color: #fff;
  font-size: 15px;
  margin-bottom: 24px;
}

.divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.08);
  margin: 24px 0;
}

.emotion-card {
  background: rgba(255, 255, 255, 0.06);
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 24px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.emotion-card.loading {
  background: rgba(255, 255, 255, 0.04);
}

.emotion-card.unavailable {
  background: rgba(245, 108, 108, 0.08);
  border-color: rgba(245, 108, 108, 0.2);
}

.emotion-card.unavailable h3 {
  color: #f56c6c;
}

.unavailable-text {
  color: #f56c6c;
  font-size: 15px;
  text-align: center;
  padding: 12px 0;
  margin: 0;
}

.emotion-card h3 {
  margin: 0 0 16px 0;
  color: #67c23a;
  font-size: 18px;
}

.emotion-item {
  margin-bottom: 10px;
  line-height: 1.6;
}

.emotion-label { color: rgba(255, 255, 255, 0.7); font-weight: 500; }
.emotion-value { color: #67c23a; font-weight: 600; }
.emotion-score { color: rgba(255, 255, 255, 0.5); font-size: 13px; }
.emotion-text { color: #fff; }

.mood-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.mood-happy { background: #f0f9eb; color: #67c23a; }
.mood-sad { background: #ecf5ff; color: #409eff; }
.mood-anxious { background: #fdf6ec; color: #e6a23c; }
.mood-calm { background: #f4f4f5; color: #909399; }
.mood-angry { background: #fef0f0; color: #f56c6c; }
.mood-surprised { background: #f0f2f5; color: #606266; }

.action-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
}


</style>
