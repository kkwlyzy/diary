<template>
  <div class="page-wrapper">
    <div class="page-content">
      <h2 class="page-title">心情趋势</h2>
      
      <div class="filter-bar">
        <el-date-picker v-model="dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" @change="loadData" />
      </div>
      
      <div class="chart-card">
        <div ref="chartRef" class="chart-container"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { statisticsAPI } from '../api/statistics'

const chartRef = ref(null)
const dateRange = ref([new Date(Date.now() - 30 * 86400000), new Date()])

const moodOrder = { happy: 5, calm: 4, surprised: 3, anxious: 2, sad: 1, angry: 0 }
const moodColors = { happy: '#67c23a', calm: '#909399', surprised: '#e6a23c', anxious: '#f56c6c', sad: '#409eff', angry: '#d91e1e' }
const moodLabels = { happy: '快乐', sad: '悲伤', anxious: '焦虑', calm: '平静', angry: '愤怒', surprised: '惊讶' }

async function loadData() {
  if (!dateRange.value) return
  const params = {
    start_date: dateRange.value[0].toISOString().split('T')[0],
    end_date: dateRange.value[1].toISOString().split('T')[0],
  }
  try {
    const res = await statisticsAPI.moodTrend(params)
    const dateMap = {}
    res.forEach(item => {
      if (!dateMap[item.date]) dateMap[item.date] = []
      dateMap[item.date].push(item)
    })
    const dates = Object.keys(dateMap).sort()
    const series = Object.keys(moodOrder).map(tag => ({
      name: moodLabels[tag] || tag,
      type: 'line',
      data: dates.map(d => {
        const items = dateMap[d].filter(i => i.mood_tag === tag)
        return items.length ? items.length : null
      }),
      smooth: true,
      lineStyle: { color: moodColors[tag], width: 2 },
      itemStyle: { color: moodColors[tag] },
    }))

    await nextTick()
    const chart = echarts.init(chartRef.value)
    chart.setOption({
      tooltip: { trigger: 'axis' },
      legend: { data: Object.values(moodLabels) },
      xAxis: { type: 'category', data: dates },
      yAxis: { type: 'value', min: 0 },
      series,
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
  margin-bottom: 20px;
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 16px;
}

.chart-card {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 24px;
}

.chart-container {
  height: 400px;
}
</style>
