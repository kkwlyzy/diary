<template>
  <div class="page-wrapper">
    <div class="page-content">
      <div class="profile-card">
        <h2 class="page-title">个人中心</h2>
        
        <div class="avatar-section">
          <div class="avatar-circle">
            {{ form.nickname ? form.nickname.charAt(0).toUpperCase() : 'U' }}
          </div>
          <p class="username">{{ form.username }}</p>
        </div>
        
        <div class="form-section">
          <div class="form-row">
            <label class="form-label">用户名</label>
            <el-input v-model="form.username" disabled />
          </div>
          <div class="form-row">
            <label class="form-label">昵称</label>
            <el-input v-model="form.nickname" />
          </div>
          <div class="form-row">
            <label class="form-label">邮箱</label>
            <el-input v-model="form.email" />
          </div>
        </div>
        
        <div class="action-buttons">
          <NeonButton variant="primary" @click="handleSave">保存修改</NeonButton>
          <NeonButton variant="danger" @click="handleLogout">退出登录</NeonButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { authAPI } from '../api/auth'

const router = useRouter()
const form = reactive({ username: '', nickname: '', email: '' })

onMounted(async () => {
  try {
    const user = await authAPI.getMe()
    form.username = user.username
    form.nickname = user.nickname || ''
    form.email = user.email || ''
  } catch (err) { /* ignore */ }
})

async function handleSave() {
  try {
    await authAPI.updateMe({ nickname: form.nickname, email: form.email })
    ElMessage.success('保存成功')
  } catch (err) {
    ElMessage.error('保存失败')
  }
}

function handleLogout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  background: transparent;
}

.page-content {
  max-width: 500px;
  margin: 0 auto;
  padding: 24px 20px;
}

.profile-card {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 32px;
}

.page-title {
  margin: 0 0 24px 0;
  color: #fff;
  font-size: 24px;
  text-align: center;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 28px;
  padding-bottom: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  padding: 24px;
}

.avatar-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 12px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.username {
  margin: 0;
  color: #fff;
  font-size: 18px;
  font-weight: 600;
}

.form-section {
  margin-bottom: 28px;
}

.form-row {
  margin-bottom: 18px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  font-weight: 500;
}

.action-buttons {
  display: flex;
  gap: 12px;
  flex-direction: column;
}


</style>
