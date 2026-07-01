<template>
  <button
    :class="['neon-btn', `neon-${variant}`, `neon-${size}`, { disabled: disabled }]"
    @click="$emit('click', $event)"
    :disabled="disabled"
  >
    <span v-if="neon" class="neon-top" />
    <span class="button-content">
      <slot />
    </span>
    <span v-if="neon" class="neon-bottom" />
  </button>
</template>

<script setup>
defineProps({
  variant: { type: String, default: 'default' },
  size: { type: String, default: 'default' },
  neon: { type: Boolean, default: true },
  disabled: { type: Boolean, default: false },
  className: { type: String, default: '' }
})

defineEmits(['click'])
</script>

<style scoped>
.neon-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  border: 1px solid;
  border-radius: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  overflow: hidden;
  text-decoration: none;
}

.neon-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.neon-btn:active {
  transform: translateY(0);
}

.neon-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

/* Sizes */
.neon-sm { padding: 6px 14px; font-size: 13px; }
.neon-default { padding: 10px 20px; font-size: 14px; }
.neon-lg { padding: 12px 28px; font-size: 15px; }

/* Variants */
.neon-default {
  background: white;
  color: #666;
  border-color: #e0e0e0;
}
.neon-default:hover {
  background: #f5f5f5;
}

.neon-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-color: transparent;
}
.neon-primary:hover {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.neon-solid {
  background: #409eff;
  color: white;
  border-color: transparent;
}
.neon-solid:hover {
  background: #3a8ee6;
}

.neon-ghost {
  background: transparent;
  color: #667eea;
  border-color: #667eea;
}
.neon-ghost:hover {
  background: rgba(102, 126, 234, 0.05);
}

.neon-success {
  background: linear-gradient(135deg, #67c23a, #5daf34);
  color: white;
  border-color: transparent;
}

.neon-danger {
  background: linear-gradient(135deg, #f56c6c, #e74c3c);
  color: white;
  border-color: transparent;
}

.neon-warning {
  background: linear-gradient(135deg, #e6a23c, #d4891a);
  color: white;
  border-color: transparent;
}

.neon-secondary {
  background: #f5f5f5;
  color: #666;
  border-color: #e0e0e0;
}
.neon-secondary:hover {
  background: #eee;
}

/* Neon glow lines */
.neon-top {
  position: absolute;
  height: 1px;
  opacity: 0;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 75%;
  background: linear-gradient(to right, transparent, #667eea, #764ba2, transparent);
  transition: all 0.5s ease-in-out;
  pointer-events: none;
}

.neon-btn:hover .neon-top {
  opacity: 1;
}

.neon-bottom {
  position: absolute;
  height: 1px;
  bottom: -1px;
  left: 50%;
  transform: translateX(-50%);
  width: 75%;
  background: linear-gradient(to right, transparent, #667eea, #764ba2, transparent);
  transition: all 0.5s ease-in-out;
  opacity: 0.3;
  pointer-events: none;
}

.neon-btn:hover .neon-bottom {
  opacity: 0.7;
}

.button-content {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
</style>
