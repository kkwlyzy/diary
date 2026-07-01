<template>
  <div class="page-wrapper">
    <div class="page-content">
      <div class="calendar-card">
        <div class="calendar-header">
          <NeonButton variant="secondary" size="sm" @click="changeMonth(-1)">上个月</NeonButton>
          <h2 class="month-title">{{ year }}年{{ month }}月</h2>
          <NeonButton variant="secondary" size="sm" @click="changeMonth(1)">下个月</NeonButton>
        </div>

        <div class="week-days">
          <div class="week-day">一</div>
          <div class="week-day">二</div>
          <div class="week-day">三</div>
          <div class="week-day">四</div>
          <div class="week-day">五</div>
          <div class="week-day">六</div>
          <div class="week-day">日</div>
        </div>

        <div class="calendar-grid">
          <div v-for="(week, weekIndex) in calendarData" :key="weekIndex" class="calendar-week">
            <div 
              v-for="(day, dayIndex) in week" 
              :key="dayIndex"
              class="calendar-day"
              :class="{ 'has-mood': day.mood, 'empty': !day.num }"
            >
              <span v-if="day.num" class="day-num">{{ day.num }}</span>
              <span v-if="day.mood" class="day-mood">●</span>
            </div>
          </div>
        </div>

        <div class="legend">
          <span v-for="mood in moodTypes" :key="mood.value" class="legend-item">{{ mood.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { statisticsAPI } from '../api/statistics'

const now = new Date()
const year = ref(now.getFullYear())
const month = ref(now.getMonth() + 1)
const calendarData = ref([])

const moodTypes = [
  { value: 'happy', label: '快乐' },
  { value: 'sad', label: '悲伤' },
  { value: 'anxious', label: '焦虑' },
  { value: 'calm', label: '平静' },
  { value: 'angry', label: '愤怒' },
  { value: 'surprised', label: '惊讶' },
]

function changeMonth(delta) {
  month.value += delta
  if (month.value > 12) { month.value = 1; year.value++ }
  if (month.value < 1) { month.value = 12; year.value-- }
  loadData()
}

async function loadData() {
  try {
    const res = await statisticsAPI.calendar({ year: year.value, month: month.value })
    const moodMap = {}
    res.forEach(item => { moodMap[item.date] = item.mood_tag })
    
    const firstDay = new Date(year.value, month.value - 1, 1).getDay()
    const daysInMonth = new Date(year.value, month.value, 0).getDate()
    const startCol = firstDay === 0 ? 6 : firstDay - 1
    
    const weeks = []
    let currentWeek = []
    
    for (let i = 0; i < startCol; i++) {
      currentWeek.push({ num: null, mood: null })
    }
    
    for (let d = 1; d <= daysInMonth; d++) {
      const dateStr = `${year.value}-${String(month.value).padStart(2, '0')}-${String(d).padStart(2, '0')}`
      currentWeek.push({ num: d, mood: moodMap[dateStr] || null })
      if (currentWeek.length === 7) {
        weeks.push([...currentWeek])
        currentWeek = []
      }
    }
    
    if (currentWeek.length > 0) {
      while (currentWeek.length < 7) {
        currentWeek.push({ num: null, mood: null })
      }
      weeks.push([...currentWeek])
    }
    
    calendarData.value = weeks
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
  max-width: 800px;
  margin: 0 auto;
  padding: 24px 20px;
}

.calendar-card {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 24px;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.month-title {
  margin: 0;
  color: #fff;
  font-size: 22px;
  font-weight: 600;
}



.week-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  margin-bottom: 12px;
}

.week-day {
  text-align: center;
  padding: 10px;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 600;
  font-size: 14px;
}

.calendar-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.calendar-week {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.calendar-day {
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 8px;
  gap: 4px;
}

.calendar-day.empty {
  background: transparent;
}

.calendar-day.has-mood {
  background: rgba(103, 194, 58, 0.15);
  border: 1px solid rgba(103, 194, 58, 0.3);
}

.day-num {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.day-mood {
  font-size: 10px;
  color: #67c23a;
}

.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.legend-item {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.5);
}
</style>
