<template>
  <div>
    <h1 class="page-title">财经快讯</h1>

    <!-- 筛选 -->
    <div style="margin-bottom: 20px; display: flex; gap: 8px">
      <button
        v-for="level in [0, 3, 4, 5]"
        :key="level"
        :class="['btn', importance === level ? 'btn-primary' : '']"
        @click="setImportance(level)"
      >
        {{ level === 0 ? '全部' : `${level}星+` }}
      </button>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="!newsList.length" class="empty-state">暂无新闻</div>

    <div v-else class="list-section">
      <div v-for="n in newsList" :key="n.id" class="card" style="margin-bottom: 8px">
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px">
          <strong style="font-size: 14px">{{ n.title }}</strong>
          <span :class="importanceTag(n.importance)">{{ n.importance }}星</span>
        </div>
        <div class="card-body">{{ n.content?.slice(0, 120) ?? '' }}</div>
        <div style="margin-top: 6px; font-size: 12px; color: var(--text-tertiary)">
          {{ n.source }} · {{ n.published_at?.slice(0, 16) ?? '' }}
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
