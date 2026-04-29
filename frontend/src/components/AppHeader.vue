<template>
  <header class="header">
    <span class="header-breadcrumb">{{ currentTitle }}</span>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const currentTitle = computed(() => (route.meta.title as string) ?? '爆单来')
</script>
