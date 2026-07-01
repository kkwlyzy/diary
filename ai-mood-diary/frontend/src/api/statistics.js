import request from './index'

export const statisticsAPI = {
  calendar: (params) => request.get('/statistics/calendar', { params }),
  moodTrend: (params) => request.get('/statistics/mood-trend', { params }),
  moodDistribution: (params) => request.get('/statistics/mood-distribution', { params }),
  summary: (params) => request.get('/statistics/summary', { params }),
}
