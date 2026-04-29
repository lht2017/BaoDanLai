<template>
  <header class="header">
    <span class="header-breadcrumb">{{ currentTitle }}</span>
    <span class="header-right">{{ today }}</span>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const currentTitle = computed(() => (route.meta.title as string) ?? '爆单来')
const today = computed(() => {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
})
</script>
