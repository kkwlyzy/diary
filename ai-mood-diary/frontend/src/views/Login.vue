<template>
  <div class="page-bg">
    <div class="grid-overlay"></div>
    <div class="login-wrapper">
      <div class="login">
        <div class="h1">
          <span class="ui">AI</span>心情日记
        </div>

        <input v-model="form.username" type="text" placeholder="用户名" />
        <input v-model="form.password" type="password" placeholder="密码" @keyup.enter="handleSubmit" />

        <input v-if="isRegister" v-model="form.nickname" type="text" placeholder="昵称" />

        <div v-if="isRegister" class="captcha-row">
          <input v-model="form.captcha" type="text" placeholder="验证码" class="captcha-input" />
          <div v-if="captchaLoading" class="captcha-placeholder">加载中...</div>
          <img v-else-if="captchaUrl" :src="captchaUrl" @click="refreshCaptcha" class="captcha-img" title="点击刷新" />
          <div v-else class="captcha-placeholder" @click="refreshCaptcha">点击获取</div>
        </div>

        <input type="button" class="btn" :value="isRegister ? '注册' : '登录'" @click="handleSubmit" :disabled="loading" />

        <input type="button" :value="isRegister ? '已有账号？去登录' : '没有账号？去注册'" @click="handleSwitchRegister" style="background:transparent; color:rgba(255,255,255,0.6); font-size:0.7em; margin-top:10px; cursor:pointer;" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'
import request from '../api/index'

const router = useRouter()
const store = useUserStore()
const isRegister = ref(false)
const loading = ref(false)
const form = reactive({ username: '', password: '', nickname: '', captcha: '' })
const captchaUrl = ref('')
const captchaSession = ref('')
const captchaLoading = ref(false)

async function refreshCaptcha() {
  captchaLoading.value = true
  try {
    const res = await request.get('/captcha/json')
    captchaSession.value = res.session_id
    captchaUrl.value = res.image_base64
  } catch (err) {
    console.error('验证码加载失败:', err)
    ElMessage.error('获取验证码失败')
  } finally {
    captchaLoading.value = false
  }
}

function handleSwitchRegister() {
  isRegister.value = !isRegister.value
  if (isRegister.value) {
    refreshCaptcha()
  }
}

async function handleSubmit() {
  if (!form.username || !form.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    if (isRegister.value) {
      if (!form.captcha) {
        ElMessage.error('请输入验证码')
        loading.value = false
        return
      }
      if (!captchaSession.value) {
        ElMessage.error('请刷新验证码')
        loading.value = false
        return
      }
      const data = { ...form, captcha_session: captchaSession.value }
      await store.register(data)
      ElMessage.success('注册成功')
    } else {
      await store.login(form.username, form.password)
      ElMessage.success('登录成功')
    }
    router.push('/')
  } catch (err) {
    const errorMsg = err.response?.data?.detail || '操作失败'
    ElMessage.error(errorMsg)
    if (isRegister.value) {
      form.captcha = ''
      refreshCaptcha()
    }
  }
  loading.value = false
}
</script>

<style scoped>
.page-bg {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  position: relative;
  overflow: hidden;
}

.page-bg::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(
      ellipse at 20% 30%,
      rgba(138, 43, 226, 0.8) 0%,
      rgba(138, 43, 226, 0) 60%
    ),
    radial-gradient(
      ellipse at 80% 50%,
      rgba(0, 191, 255, 0.7) 0%,
      rgba(0, 191, 255, 0) 70%
    ),
    radial-gradient(
      ellipse at 50% 80%,
      rgba(50, 205, 50, 0.6) 0%,
      rgba(50, 205, 50, 0) 65%
    ),
    linear-gradient(135deg, #000000 0%, #0a0520 100%);
  background-blend-mode: overlay, screen, hard-light;
  overflow: hidden;
  animation: aurora-drift 25s infinite alternate ease-in-out;
}

.page-bg::after {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background: radial-gradient(
    circle at center,
    transparent 70%,
    rgba(10, 5, 32, 0.9) 100%
  );
  animation: aurora-pulse 8s infinite alternate;
  pointer-events: none;
}

.page-bg .grid-overlay {
  content: "";
  position: absolute;
  width: 200%;
  height: 200%;
  top: -50%;
  left: -50%;
  background: repeating-linear-gradient(
      45deg,
      rgba(255, 255, 255, 0.02) 0px,
      rgba(255, 255, 255, 0.02) 1px,
      transparent 1px,
      transparent 40px
    ),
    repeating-linear-gradient(
      -45deg,
      rgba(255, 255, 255, 0.03) 0px,
      rgba(255, 255, 255, 0.03) 1px,
      transparent 1px,
      transparent 60px
    );
  animation: grid-shift 20s linear infinite;
  pointer-events: none;
}

.login-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
  position: relative;
  z-index: 1;
}

.login {
  width: 340px;
  height: auto;
  min-height: 400px;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 47px;
  padding-bottom: 57px;
  color: #fff;
  border-radius: 30px;
  font-size: 1.3em;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 15px 15px 30px rgba(0, 0, 0, 0.4), -15px -15px 30px rgba(255, 255, 255, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.login input[type="text"],
.login input[type="password"] {
  opacity: 1;
  display: block;
  border: 1px solid rgba(255, 255, 255, 0.12);
  outline: none;
  width: 100%;
  padding: 13px 18px;
  margin: 20px 0 0 0;
  font-size: 0.8em;
  border-radius: 100px;
  background: rgba(255, 255, 255, 0.06);
  color: #fff;
  box-sizing: border-box;
  transition: border-color 0.3s, background 0.3s;
}

.login input[type="text"]:focus,
.login input[type="password"]:focus {
  border-color: rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
}

.login input:focus {
  animation: bounce 1s;
  -webkit-appearance: none;
}

.login input[type=submit],
.login input[type=button],
.h1 {
  border: 0;
  outline: 0;
  width: 100%;
  padding: 13px;
  margin: 40px 0 0 0;
  border-radius: 500px;
  font-weight: 600;
  animation: bounce2 1.6s;
  box-sizing: border-box;
}

.h1 {
  padding: 0;
  position: relative;
  top: -35px;
  display: block;
  margin-bottom: -0px;
  font-size: 1.3em;
  text-align: center;
}

.btn {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: #fff;
  padding: 16px !important;
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.35);
  color: #fff;
  padding: 16px !important;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login input[type=text] {
  animation: bounce 1s;
  -webkit-appearance: none;
}

.login input[type=password] {
  animation: bounce1 1.3s;
}

.ui {
  font-weight: bolder;
  background: -webkit-linear-gradient(#B563FF, #535EFC, #0EC8EE);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  border-bottom: 4px solid transparent;
  border-image: linear-gradient(0.25turn, #535EFC, #0EC8EE, #0EC8EE);
  border-image-slice: 1;
  display: inline;
}

.captcha-row {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-top: 20px;
}

.captcha-input {
  flex: 1;
  margin: 0 !important;
}

.captcha-img {
  height: 42px;
  border-radius: 100px;
  cursor: pointer;
  border: 1px solid rgba(255,255,255,0.1);
  background: #fff;
}

.captcha-placeholder {
  height: 42px;
  min-width: 100px;
  padding: 0 16px;
  border-radius: 100px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255,255,255,0.15);
  color: rgba(255, 255, 255, 0.6);
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.captcha-placeholder:hover {
  background: rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.8);
}

@media only screen and (max-width: 768px) {
  .login {
    width: 90%;
    padding: 30px;
  }
}

@keyframes aurora-drift {
  0% {
    transform: scale(1) translate(0, 0);
  }
  25% {
    transform: scale(1.15) translate(-3%, 2%);
  }
  50% {
    transform: scale(1.1) translate(3%, -3%);
  }
  75% {
    transform: scale(1.2) translate(-2%, -2%);
  }
  100% {
    transform: scale(1.15) translate(2%, 3%);
  }
}

@keyframes aurora-pulse {
  0% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.08);
  }
  100% {
    opacity: 0.7;
    transform: scale(1.02);
  }
}

@keyframes grid-shift {
  0% {
    transform: translate(0, 0) rotate(0deg);
  }
  25% {
    transform: translate(-30px, 20px) rotate(2deg);
  }
  50% {
    transform: translate(20px, -30px) rotate(-2deg);
  }
  75% {
    transform: translate(-20px, -20px) rotate(1deg);
  }
  100% {
    transform: translate(30px, 30px) rotate(-1deg);
  }
}

@keyframes bounce {
  0% {
    transform: scale(1);
  }
  60% {
    transform: scale(1.02);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes bounce1 {
  0% {
    transform: scale(1);
  }
  60% {
    transform: scale(1.02);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes bounce2 {
  0% {
    transform: scale(0.95);
    opacity: 0;
  }
  60% {
    transform: scale(1.02);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

</style>
