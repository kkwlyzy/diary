<template>
  <div class="page-wrapper">
    <div class="page-content">
      <h2 class="page-title">统计分析</h2>
      
      <div class="filter-bar">
        <el-date-picker v-model="dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" @change="loadData" />
      </div>

      <div class="stats-grid">
        <div class="stat-card summary-card">
          <h3>汇总</h3>
          <div class="stat-row">
            <span class="stat-label">日记总数</span>
            <span class="stat-value">{{ summary?.total_diaries || 0 }}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">时间范围</span>
            <span class="stat-text">{{ summary?.start_date || '-' }} ~ {{ summary?.end_date || '-' }}</span>
          </div>
        </div>

        <div class="stat-card pie-card">
          <h3>情绪分布</h3>
          <div ref="pieRef" class="chart-container"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { statisticsAPI } from '../api/statistics'

const pieRef = ref(null)
const summary = ref(null)
const dateRange = ref([new Date(Date.now() - 30 * 86400000), new Date()])

const moodLabels = { happy: '快乐', sad: '悲伤', anxious: '焦虑', calm: '平静', angry: '愤怒', surprised: '惊讶' }
const moodColors = { happy: '#67c23a', sad: '#409eff', anxious: '#f56c6c', calm: '#909399', angry: '#d91e1e', surprised: '#e6a23c' }

async function loadData() {
  if (!dateRange.value) return
  const params = {
    start_date: dateRange.value[0].toISOString().split('T')[0],
    end_date: dateRange.value[1].toISOString().split('T')[0],
  }
  try {
    const [dist, sum] = await Promise.all([
      statisticsAPI.moodDistribution(params),
      statisticsAPI.summary(params),
    ])
    summary.value = sum

    await nextTick()
    const chart = echarts.init(pieRef.value)
    chart.setOption({
      tooltip: { trigger: 'item' },
      series: [{
        type: 'pie',
        radius: '60%',
        data: dist.map(item => ({
          name: moodLabels[item.mood_tag] || item.mood_tag,
          value: item.count,
          itemStyle: { color: moodColors[item.mood_tag] },
        })),
        label: { formatter: '{b}: {c}' },
      }],
    })
  } catch (err) { /* ignore */ }
}

onMounted(loadData)
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  background: transparent;
}

.page-content {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 20px;
}

.page-title {
  margin: 0 0 20px 0;
  color: #fff;
  font-size: 24px;
}

.filter-bar {
  margin-bottom: 24px;
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 16px;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 20px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 24px;
}

.stat-card h3 {
  margin: 0 0 20px 0;
  color: #fff;
  font-size: 18px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.stat-row:last-child { border-bottom: none; }

.stat-label { color: rgba(255, 255, 255, 0.5); font-size: 14px; }

.stat-value {
  font-size: 28px;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-text { color: rgba(255, 255, 255, 0.7); font-size: 14px; }

.chart-container { height: 300px; }

@media (max-width: 768px) {
  .stats-grid { grid-template-columns: 1fr; }
}
</style>
