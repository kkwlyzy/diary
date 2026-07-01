<template>
  <Transition :name="transitionName" mode="out-in">
    <router-view :key="$route.fullPath" />
  </Transition>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const transitionName = ref('')
const isFromLogin = ref(false)

watch(() => route.path, (toPath, fromPath) => {
  isFromLogin.value = fromPath === '/login'
  transitionName.value = isFromLogin.value ? 'fade-slide' : ''
})
</script>

<style>
.fade-slide-enter-active {
  transition: all 0.5s ease-out;
}

.fade-slide-leave-active {
  transition: all 0.4s ease-in;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: scale(0.9);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: scale(1.1);
}
</style>
