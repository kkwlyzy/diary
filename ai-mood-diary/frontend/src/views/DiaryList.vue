<template>
  <div class="page-wrapper">
    <div class="page-content">
      <div class="toolbar">
        <div class="filter-group">
          <div class="filter-item">
            <span class="filter-label">心情：</span>
            <el-select v-model="filter.mood_tag" placeholder="选择心情" style="width: 180px" @change="loadData">
              <el-option label="全部" value="" />
              <el-option label="快乐" value="happy" />
              <el-option label="悲伤" value="sad" />
              <el-option label="焦虑" value="anxious" />
              <el-option label="平静" value="calm" />
              <el-option label="愤怒" value="angry" />
              <el-option label="惊讶" value="surprised" />
            </el-select>
            <span v-if="filter.mood_tag" class="filter-selected">已选：{{ moodLabel(filter.mood_tag) }}</span>
          </div>
          <div class="filter-item">
            <el-date-picker v-model="filter.dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" @change="loadData" />
          </div>
        </div>
        <div class="action-group">
          <NeonButton variant="secondary" @click="showBatchActions = !showBatchActions">
            批量操作
          </NeonButton>
          <NeonButton variant="primary" @click="$router.push('/diary/new')">
            写日记
          </NeonButton>
        </div>
      </div>

      <div v-if="showBatchActions" class="batch-bar">
        <NeonButton variant="danger" size="sm" @click="batchDelete">批量删除</NeonButton>
        <NeonButton variant="default" size="sm" @click="batchExport">批量导出</NeonButton>
      </div>

      <div class="diary-table" v-loading="loading">
        <el-table :data="diaries" @selection-change="onSelectionChange">
          <el-table-column type="selection" width="55" v-if="showBatchActions" />
          <el-table-column prop="date" label="日期" width="140">
            <template #default="{ row }">
              <span class="date-text">{{ row.date }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="title" label="标题" min-width="200">
            <template #default="{ row }">
              <router-link :to="`/diary/${row.id}`" class="diary-title">{{ row.title || '无标题' }}</router-link>
            </template>
          </el-table-column>
          <el-table-column prop="mood_tag" label="心情" width="120">
            <template #default="{ row }">
              <span class="mood-badge" :class="moodType(row.mood_tag)">
                {{ moodLabel(row.mood_tag) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="weather" label="天气" width="100" />
          <el-table-column label="操作" width="180">
            <template #default="{ row }">
              <button class="btn-link btn-edit" @click="$router.push(`/diary/${row.id}/edit`)">编辑</button>
              <button class="btn-link btn-delete" @click="handleDelete(row.id)">删除</button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="page"
          :page-size="pageSize"
          :total="total"
          layout="prev, pager, next"
          @current-change="loadData"
        />
      </div>

      <div class="ai-analysis-card" v-if="aiStatus === 'completed' && todayAnalysis">
        <div class="ai-header">
          <span class="ai-icon">🤖</span>
          <span class="ai-title">今日 AI 情绪分析</span>
        </div>
        <div class="ai-content">
          <div class="emotion-row">
            <span class="emotion-label">今日心情：</span>
            <span class="emotion-value" :class="moodType(todayAnalysis.emotion_label)">
              {{ moodLabel(todayAnalysis.emotion_label) }}
            </span>
            <span class="emotion-score">强度：{{ todayAnalysis.emotion_score }}</span>
          </div>
          <div class="analysis-row">
            <span class="analysis-label">分析：</span>
            <span class="analysis-text">{{ todayAnalysis.analysis_detail }}</span>
          </div>
          <div class="suggestion-row">
            <span class="suggestion-label">建议：</span>
            <span class="suggestion-text">{{ todayAnalysis.suggestion }}</span>
          </div>
        </div>
      </div>

      <div class="ai-analysis-card unavailable" v-else-if="aiStatus === 'unavailable'">
        <div class="ai-header">
          <span class="ai-icon">🤖</span>
          <span class="ai-title">今日 AI 情绪分析</span>
        </div>
        <p class="unavailable-text">AI暂不可用</p>
      </div>

      <div class="ai-analysis-card empty" v-else-if="!analysisLoading">
        <div class="empty-content">
          <span class="empty-icon">📝</span>
          <span class="empty-text">今日暂无日记，写一篇日记让 AI 为你分析心情吧~</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { diaryAPI } from '../api/diary'
import request from '../api/index'

const loading = ref(false)
const diaries = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const showBatchActions = ref(false)
const selectedIds = ref([])
const filter = reactive({ mood_tag: '', dateRange: null })
const todayAnalysis = ref(null)
const analysisLoading = ref(true)
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

async function loadData() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (filter.mood_tag) params.mood_tag = filter.mood_tag
    if (filter.dateRange) {
      params.start_date = filter.dateRange[0].toISOString().split('T')[0]
      params.end_date = filter.dateRange[1].toISOString().split('T')[0]
    }
    const res = await diaryAPI.list(params)
    diaries.value = res.items
    total.value = res.total
  } catch (err) {
    ElMessage.error('加载失败')
  }
  loading.value = false
}

function onSelectionChange(rows) { selectedIds.value = rows.map(r => r.id) }

async function handleDelete(id) {
  await ElMessageBox.confirm('确定删除？')
  await diaryAPI.delete(id)
  ElMessage.success('删除成功')
  loadData()
  loadTodayAnalysis()
}

async function batchDelete() {
  if (!selectedIds.value.length) return ElMessage.warning('请选择日记')
  await ElMessageBox.confirm(`确定删除 ${selectedIds.value.length} 篇日记？`)
  await diaryAPI.batchDelete(selectedIds.value)
  ElMessage.success('批量删除成功')
  loadData()
  loadTodayAnalysis()
}

async function batchExport() {
  if (!selectedIds.value.length) return ElMessage.warning('请选择日记')
  const res = await diaryAPI.batchExport(selectedIds.value, 'markdown')
  const blob = new Blob([res.data], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = '日记导出.md'; a.click()
  URL.revokeObjectURL(url)
}

async function loadTodayAnalysis() {
  analysisLoading.value = true
  try {
    const res = await request.get('/ai/today-analysis')
    aiStatus.value = res.ai_status || 'pending'
    if (res.analysis) {
      todayAnalysis.value = res.analysis
    } else if (res.ai_status === 'unavailable') {
      todayAnalysis.value = { emotion_label: 'unavailable' }
    } else {
      todayAnalysis.value = null
    }
  } catch (err) {
    console.error('加载今日分析失败', err)
    aiStatus.value = 'unavailable'
  }
  analysisLoading.value = false
}

onMounted(() => {
  loadData()
  loadTodayAnalysis()
})
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  background: transparent;
}

.page-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 20px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.filter-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.filter-selected {
  color: #667eea;
  font-size: 13px;
  font-weight: 500;
  padding: 4px 8px;
  background: rgba(102, 126, 234, 0.15);
  border-radius: 8px;
}

.action-group {
  display: flex;
  gap: 10px;
}



.batch-bar {
  display: flex;
  gap: 12px;
  align-items: center;
  padding: 16px;
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  margin-bottom: 16px;
}

.batch-bar :deep(.neon-btn) {
  width: 100px;
}

.diary-table {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  overflow: hidden;
}

:deep(.el-table) {
  background: transparent !important;
}

:deep(.el-table__header-wrapper) {
  background: rgba(255, 255, 255, 0.04);
}

:deep(.el-table__body-wrapper) {
  background: transparent;
}

:deep(.el-table th) {
  background: rgba(255, 255, 255, 0.04) !important;
  color: rgba(255, 255, 255, 0.7) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

:deep(.el-table td) {
  background: #07182E !important;
  color: rgba(255, 255, 255, 0.9) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

:deep(.el-table tr:hover > td) {
  background: rgba(102, 126, 234, 0.15) !important;
}

:deep(.el-table__header-wrapper) {
  background: #07182E !important;
}

:deep(.el-table th) {
  background: #07182E !important;
  color: rgba(255, 255, 255, 0.7) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.el-select), :deep(.el-date-picker) {
  background: #07182E;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
}

:deep(.el-select__wrapper), :deep(.el-input__wrapper) {
  background: #07182E !important;
  border: none;
}

:deep(.el-input__inner) {
  color: rgba(255, 255, 255, 0.9);
  background: #07182E;
}

:deep(.el-select__wrapper:hover) {
  border-color: rgba(102, 126, 234, 0.5);
}

:deep(.el-select__wrapper.is-focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

:deep(.el-date-editor .el-input__wrapper) {
  background: #07182E !important;
}

:deep(.el-date-editor .el-input__inner) {
  color: rgba(255, 255, 255, 0.9);
}

:deep(.el-date-editor .el-input__prefix),
:deep(.el-date-editor .el-input__suffix) {
  color: rgba(255, 255, 255, 0.5);
}

.diary-title {
  color: #999;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.diary-title:hover {
  color: #bbb;
}

.date-text {
  color: #999;
  font-size: 13px;
}

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

.btn-link {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 13px;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s;
}

.btn-edit { color: #409eff; }
.btn-edit:hover { background: rgba(64, 158, 255, 0.15); }

.btn-delete { color: #f56c6c; }
.btn-delete:hover { background: rgba(245, 108, 108, 0.15); }

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

:deep(.el-pagination) {
  .btn-prev, .btn-next, .el-pager li {
    background: #07182E;
    color: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
  }
  .btn-prev:hover, .btn-next:hover, .el-pager li:hover {
    background: rgba(102, 126, 234, 0.2);
    border-color: rgba(102, 126, 234, 0.5);
  }
  .el-pager li.is-active {
    background: rgba(102, 126, 234, 0.6);
    color: #fff;
    border-color: rgba(102, 126, 234, 0.8);
  }
}

.ai-analysis-card {
  margin-top: 24px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
}

.ai-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.ai-icon {
  font-size: 20px;
}

.ai-title {
  font-size: 16px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.ai-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.emotion-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.emotion-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

.emotion-value {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
}

.emotion-score {
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
}

.analysis-row, .suggestion-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.analysis-label, .suggestion-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  flex-shrink: 0;
}

.analysis-text, .suggestion-text {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  line-height: 1.5;
}

.ai-analysis-card.empty {
  text-align: center;
}

.ai-analysis-card.unavailable {
  text-align: center;
  border-color: rgba(245, 108, 108, 0.2);
  background: rgba(245, 108, 108, 0.06);
}

.ai-analysis-card.unavailable .ai-title {
  color: #f56c6c;
}

.unavailable-text {
  color: #f56c6c;
  font-size: 15px;
  padding: 12px 0;
  margin: 0;
}

.empty-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.empty-icon {
  font-size: 24px;
}

.empty-text {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
}

:deep(.el-message-box) {
  width: 380px;
  border-radius: 30px;
  background: #212121;
  box-shadow: 15px 15px 30px rgb(25, 25, 25), -15px -15px 30px rgb(60, 60, 60);
  border: none;
}

:deep(.el-message-box__header) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  padding: 20px 24px 16px;
}

:deep(.el-message-box__title) {
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
}

:deep(.el-message-box__close) {
  color: rgba(255, 255, 255, 0.5);
}

:deep(.el-message-box__content) {
  padding: 24px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

:deep(.el-message-box__btns) {
  padding: 16px 24px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

:deep(.el-message-box__btns .el-button) {
  border-radius: 12px;
}

:deep(.el-message-box__btns .el-button--primary) {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  color: white;
}

:deep(.el-message-box__btns .el-button--default) {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: rgba(255, 255, 255, 0.8);
}

:deep(.el-overlay) {
  background-color: rgba(0, 0, 0, 0.6);
}
</style>
