<template>
  <div class="app-header">
    <div class="header-inner">
      <div class="logo">
        <span class="logo-text">AI心情日记</span>
      </div>
      <div class="nav-buttons">
        <router-link to="/" class="nav-btn" :class="{ active: $route.path === '/' }">
          日记列表
        </router-link>
        <router-link to="/calendar" class="nav-btn" :class="{ active: $route.path === '/calendar' }">
          日历视图
        </router-link>
        <router-link to="/trend" class="nav-btn" :class="{ active: $route.path === '/trend' }">
          心情趋势
        </router-link>
        <router-link to="/statistics" class="nav-btn" :class="{ active: $route.path === '/statistics' }">
          统计分析
        </router-link>
        <router-link to="/profile" class="nav-btn" :class="{ active: $route.path === '/profile' }">
          个人中心
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.app-header {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #fff;
  font-size: 20px;
  font-weight: bold;
}



.nav-buttons {
  display: flex;
  gap: 4px;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.65);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.2s ease;
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}

.nav-btn.active {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  font-weight: 600;
}

@media (max-width: 768px) {
  .header-inner {
    flex-direction: column;
    height: auto;
    padding: 12px 20px;
    gap: 12px;
  }
  
  .nav-buttons {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .nav-btn {
    padding: 6px 12px;
    font-size: 13px;
  }
}
</style>
