import request from './index'

export const authAPI = {
  login: (username, password) => request.post('/auth/login', { username, password }),
  register: (data) => request.post('/auth/register', data),
  getMe: () => request.get('/auth/me'),
  updateMe: (data) => request.put('/auth/me', data),
}
