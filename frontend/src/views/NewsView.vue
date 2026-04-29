<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">财经快讯</h1>
      <p class="page-subtitle">实时财经新闻与资讯聚合</p>
    </div>

    <!-- 筛选 -->
    <div class="action-bar" style="margin-bottom: 24px">
      <button
        v-for="level in [0, 3, 4, 5]"
        :key="level"
        :class="['btn', importance === level ? 'btn-primary' : 'btn-ghost']"
        @click="setImportance(level)"
      >
        {{ level === 0 ? '全部' : `${level}星+` }}
      </button>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="!newsList.length" class="empty-state">
      <div class="empty-state-icon">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/></svg>
      </div>
      暂无新闻
    </div>

    <div v-else style="display: flex; flex-direction: column; gap: 12px">
      <div v-for="n in newsList" :key="n.id" class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px">
          <strong style="font-size: 14px; line-height: 1.5">{{ n.title }}</strong>
          <span :class="importanceTag(n.importance)" style="flex-shrink: 0; margin-left: 12px">{{ n.importance }}星</span>
        </div>
        <div class="card-body">{{ n.content?.slice(0, 120) ?? '' }}</div>
        <div style="margin-top: 10px; font-size: 12px; color: var(--text-tertiary); display: flex; align-items: center; gap: 6px">
          <span v-if="n.source">{{ n.source }}</span>
          <span v-if="n.source && n.published_at">·</span>
          <span>{{ n.published_at?.slice(0, 16) ?? '' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getNewsList, type NewsItem } from '@/api'

const loading = ref(true)
const newsList = ref<NewsItem[]>([])
const importance = ref(0)

function importanceTag(level: number) {
  if (level >= 5) return 'tag tag-red'
  if (level >= 4) return 'tag tag-orange'
  return 'tag'
}

async function setImportance(level: number) {
  importance.value = level
  await loadNews()
}

async function loadNews() {
  loading.value = true
  try {
    const { data } = await getNewsList(importance.value || undefined)
    newsList.value = data
  } finally {
    loading.value = false
  }
}

onMounted(loadNews)
</script>
