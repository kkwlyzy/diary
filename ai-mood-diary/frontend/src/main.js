import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './global.css'
import App from './App.vue'
import router from './router'
import NeonButton from './components/ui/NeonButton.vue'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.component('NeonButton', NeonButton)
app.mount('#app')
