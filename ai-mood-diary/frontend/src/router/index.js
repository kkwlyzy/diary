import { createRouter, createWebHistory } from 'vue-router'
import Layout from '../views/Layout.vue'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  {
    path: '/',
    component: Layout,
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'DiaryList', component: () => import('../views/DiaryList.vue') },
      { path: 'diary/new', name: 'DiaryNew', component: () => import('../views/DiaryEditor.vue') },
      { path: 'diary/:id', name: 'DiaryDetail', component: () => import('../views/DiaryDetail.vue') },
      { path: 'diary/:id/edit', name: 'DiaryEdit', component: () => import('../views/DiaryEditor.vue') },
      { path: 'calendar', name: 'Calendar', component: () => import('../views/CalendarView.vue') },
      { path: 'trend', name: 'Trend', component: () => import('../views/TrendChart.vue') },
      { path: 'statistics', name: 'Statistics', component: () => import('../views/Statistics.vue') },
      { path: 'profile', name: 'Profile', component: () => import('../views/Profile.vue') },
    ]
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
