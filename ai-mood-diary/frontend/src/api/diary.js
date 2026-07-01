import request from './index'

export const diaryAPI = {
  list: (params) => request.get('/diaries', { params }),
  get: (id) => request.get(`/diaries/${id}`),
  create: (data) => request.post('/diaries', data),
  update: (id, data) => request.put(`/diaries/${id}`, data),
  delete: (id) => request.delete(`/diaries/${id}`),
  batchDelete: (ids) => request.post('/diaries/batch-delete', { ids }),
  batchMood: (ids, mood_tag) => request.post('/diaries/batch-mood', { ids, mood_tag }),
  batchExport: (ids, format) => request.post('/diaries/batch-export', { ids, format }),
}
