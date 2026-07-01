<template>
  <div class="page-wrapper">
    <div class="page-content">
      <div class="editor-card">
        <h2 class="page-title">{{ isEdit ? '编辑日记' : '写日记' }}</h2>
        
        <div class="form-row">
          <label class="form-label">日期</label>
          <el-date-picker v-model="form.date" type="date" class="full-width" />
        </div>
        
        <div class="form-row">
          <label class="form-label">标题</label>
          <el-input v-model="form.title" placeholder="给日记起个标题" class="full-width" />
        </div>
        
        <div class="form-row">
          <label class="form-label">心情</label>
          <div class="mood-selector">
            <button 
              v-for="mood in moods" 
              :key="mood.value"
              class="mood-btn"
              :class="{ active: form.mood_tag === mood.value }"
              @click="form.mood_tag = form.mood_tag === mood.value ? '' : mood.value"
            >
              <span class="mood-emoji">{{ mood.emoji }}</span>
              <span class="mood-label">{{ mood.label }}</span>
            </button>
          </div>
        </div>
        
        <div class="form-row">
          <label class="form-label">天气</label>
          <el-input v-model="form.weather" placeholder="晴/多云/雨..." style="width:200px" />
        </div>
        
        <div class="form-row">
          <label class="form-label">内容</label>
          <div class="content-textarea-wrapper">
            <el-input v-model="form.content" type="textarea" :rows="12" placeholder="今天发生了什么？" class="content-textarea" />
          </div>
        </div>
        
        <div class="action-buttons">
          <NeonButton v-if="!saving" variant="primary" @click="handleSave">
            {{ isEdit ? '保存修改' : '保存日记' }}
          </NeonButton>
          <div v-else class="capybaraloader">
            <div class="capybara">
              <div class="capy"></div>
              <div class="capyleg">
                <div class="capyleg2"></div>
                <div class="capyleg2"></div>
              </div>
              <div class="capyhead">
                <div class="capyear">
                  <div class="capyear2"></div>
                </div>
                <div class="capyear">
                  <div class="capyear2"></div>
                </div>
                <div class="capyeye"></div>
                <div class="capyeye"></div>
                <div class="capymouth">
                  <div class="capylips"></div>
                  <div class="capylips"></div>
                </div>
              </div>
            </div>
            <div class="loader">
              <div class="loaderline"></div>
            </div>
          </div>
          <NeonButton variant="secondary" @click="$router.back()" :disabled="saving">取消</NeonButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { diaryAPI } from '../api/diary'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)
const saving = ref(false)
const form = reactive({
  date: new Date(),
  title: '',
  mood_tag: '',
  weather: '',
  content: '',
})

const moods = [
  { label: '快乐', value: 'happy', emoji: '😊' },
  { label: '悲伤', value: 'sad', emoji: '😢' },
  { label: '焦虑', value: 'anxious', emoji: '😰' },
  { label: '平静', value: 'calm', emoji: '😌' },
  { label: '愤怒', value: 'angry', emoji: '😤' },
  { label: '惊讶', value: 'surprised', emoji: '😲' }
]
const moodMap = { '快乐': 'happy', '悲伤': 'sad', '焦虑': 'anxious', '平静': 'calm', '愤怒': 'angry', '惊讶': 'surprised' }

onMounted(async () => {
  if (isEdit.value) {
    const res = await diaryAPI.get(route.params.id)
    const d = res.diary
    form.date = new Date(d.date)
    form.title = d.title || ''
    form.mood_tag = d.mood_tag || ''
    form.weather = d.weather || ''
    form.content = d.content || ''
  }
})

async function handleSave() {
  saving.value = true
  try {
    const data = { ...form }
    if (isEdit.value) {
      delete data.date
      await diaryAPI.update(route.params.id, data)
      ElMessage.success('修改成功')
    } else {
      data.date = form.date.toISOString().split('T')[0]
      await diaryAPI.create(data)
      ElMessage.success('保存成功，AI正在分析你的心情...')
    }
    router.push('/')
  } catch (err) {
    ElMessage.error('保存失败')
  }
  saving.value = false
}
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

.editor-card {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 32px;
}

.page-title {
  margin: 0 0 28px 0;
  color: #fff;
  font-size: 24px;
}

.form-row {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  font-weight: 500;
}

.full-width { width: 100%; }

.form-row :deep(.el-input__wrapper),
.form-row :deep(.el-date-editor),
.form-row :deep(.el-input__inner) {
  background-color: #07182E !important;
  --el-input-bg-color: #07182E;
  --el-date-editor-bg-color: #07182E;
  color: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
}

.form-row :deep(.el-input__wrapper) {
  background-color: #07182E !important;
  box-shadow: none;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.form-row :deep(.el-input__wrapper:hover) {
  border-color: rgba(102, 126, 234, 0.5);
}

.form-row :deep(.el-input__wrapper.is-focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

.form-row :deep(.el-input__inner) {
  background-color: transparent !important;
  color: rgba(255, 255, 255, 0.9);
}

.form-row :deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.4);
}

.form-row :deep(.el-date-editor.el-input) {
  width: 100%;
}

.form-row :deep(.el-date-editor .el-input__wrapper) {
  background-color: #07182E !important;
}

.form-row :deep(.el-date-editor .el-input__inner) {
  color: rgba(255, 255, 255, 0.9);
}

.form-row :deep(.el-date-editor .el-input__prefix) {
  color: rgba(255, 255, 255, 0.5);
}

.form-row :deep(.el-date-editor .el-input__suffix) {
  color: rgba(255, 255, 255, 0.5);
}

.mood-selector {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.mood-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 12px 16px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 14px;
  min-width: 80px;
}

.mood-emoji {
  font-size: 28px;
  line-height: 1;
  margin-bottom: 4px;
}

.mood-label {
  font-size: 12px;
}

.mood-btn:hover {
  border-color: #667eea;
  color: #667eea;
  background: rgba(102, 126, 234, 0.15);
}

.mood-btn.active {
  border-color: #667eea;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  align-items: center;
}

.capybaraloader {
  width: 14em;
  height: 10em;
  position: relative;
  z-index: 1;
  --color: rgb(204, 125, 45);
  --color2: rgb(83, 56, 28);
  transform: scale(0.75);
}
.capybara {
  width: 100%;
  height: 7.5em;
  position: relative;
  z-index: 1;
}
.loader {
  width: 100%;
  height: 2.5em;
  position: relative;
  z-index: 1;
  overflow: hidden;
}
.capy {
  width: 85%;
  height: 100%;
  background: linear-gradient(var(--color), 90%, var(--color2));
  border-radius: 45%;
  position: relative;
  z-index: 1;
  animation: movebody 1s linear infinite;
}
.capyhead {
  width: 7.5em;
  height: 7em;
  bottom: 0em;
  right: 0em;
  position: absolute;
  background-color: var(--color);
  z-index: 3;
  border-radius: 3.5em;
  box-shadow: -1em 0em var(--color2);
  animation: movebody 1s linear infinite;
}
.capyear {
  width: 2em;
  height: 2em;
  background: linear-gradient(-45deg, var(--color), 90%, var(--color2));
  top: 0em;
  left: 0em;
  border-radius: 100%;
  position: absolute;
  overflow: hidden;
  z-index: 3;
}
.capyear:nth-child(2) {
  left: 5em;
  background: linear-gradient(25deg, var(--color), 90%, var(--color2));
}
.capyear2 {
  width: 100%;
  height: 1em;
  background-color: var(--color2);
  bottom: 0em;
  left: 0.5em;
  border-radius: 100%;
  position: absolute;
  transform: rotate(-45deg);
}
.capymouth {
  width: 3.5em;
  height: 2em;
  background-color: var(--color2);
  position: absolute;
  bottom: 0em;
  left: 2.5em;
  border-radius: 50%;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 0.5em;
}
.capylips {
  width: 0.25em;
  height: 0.75em;
  border-radius: 100%;
  transform: rotate(-45deg);
  background-color: var(--color);
}
.capylips:nth-child(2) {
  transform: rotate(45deg);
}
.capyeye {
  width: 2em;
  height: 0.5em;
  background-color: var(--color2);
  position: absolute;
  bottom: 3.5em;
  left: 1.5em;
  border-radius: 5em;
  transform: rotate(45deg);
}
.capyeye:nth-child(4) {
  transform: rotate(-45deg);
  left: 5.5em;
  width: 1.75em;
}
.capyleg {
  width: 6em;
  height: 5em;
  bottom: 0em;
  left: 0em;
  position: absolute;
  background: linear-gradient(var(--color), 95%, var(--color2));
  z-index: 2;
  border-radius: 2em;
  animation: movebody 1s linear infinite;
}
.capyleg2 {
  width: 1.75em;
  height: 3em;
  bottom: 0em;
  left: 3.25em;
  position: absolute;
  background: linear-gradient(var(--color), 80%, var(--color2));
  z-index: 2;
  border-radius: 0.75em;
  box-shadow: inset 0em -0.5em var(--color2);
  animation: moveleg 1s linear infinite;
}
.capyleg2:nth-child(3) {
  width: 1.25em;
  left: 0.5em;
  height: 2em;
  animation: moveleg2 1s linear infinite 0.075s;
}

@keyframes moveleg {
  0% {
    transform: rotate(-45deg) translateX(-5%);
  }
  50% {
    transform: rotate(45deg) translateX(5%);
  }
  100% {
    transform: rotate(-45deg) translateX(-5%);
  }
}

@keyframes moveleg2 {
  0% {
    transform: rotate(45deg);
  }
  50% {
    transform: rotate(-45deg);
  }
  100% {
    transform: rotate(45deg);
  }
}

@keyframes movebody {
  0% {
    transform: translateX(0%);
  }
  50% {
    transform: translateX(2%);
  }
  100% {
    transform: translateX(0%);
  }
}

.loaderline {
  width: 50em;
  height: 0.5em;
  border-top: 0.5em dashed var(--color2);
  animation: moveline 10s linear infinite;
}

@keyframes moveline {
  0% {
    transform: translateX(0%);
    opacity: 0%;
  }
  5% {
    opacity: 100%;
  }
  95% {
    opacity: 100%;
  }
  100% {
    opacity: 0%;
    transform: translateX(-70%);
  }
}

.content-textarea-wrapper {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  padding: 2px;
}

.content-textarea-wrapper::before {
  content: '';
  position: absolute;
  width: 200px;
  background-image: linear-gradient(180deg, rgb(0, 183, 255), rgb(255, 48, 255));
  height: 200%;
  top: -50%;
  left: 50%;
  margin-left: -100px;
  animation: rotBGimg 3s linear infinite;
  transition: all 0.2s linear;
}

@keyframes rotBGimg {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.content-textarea-wrapper::after {
  content: '';
  position: absolute;
  background: #07182E;
  inset: 5px;
  border-radius: 15px;
  z-index: 0;
}

.content-textarea {
  position: relative;
  z-index: 1;
  --el-input-bg-color: transparent;
  --el-input-border-color: transparent;
  --el-input-hover-border-color: transparent;
  --el-input-focus-border-color: transparent;
  --el-input-text-color: rgba(255, 255, 255, 0.9);
  --el-input-placeholder-color: rgba(255, 255, 255, 0.4);
}

.content-textarea :deep(.el-textarea__inner) {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.9);
  padding: 12px;
  resize: none;
}

.content-textarea :deep(.el-textarea__inner:focus) {
  background: transparent;
  border: none;
  box-shadow: none;
}
</style>
