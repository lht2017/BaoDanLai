<template>
  <div>
    <h1 class="page-title">市场总览</h1>
    <p class="page-subtitle">A股AI自动复盘 — 今日市场全景</p>

    <!-- 搜索 -->
    <div style="margin-bottom: 24px">
      <input
        v-model="keyword"
        class="search-box"
        placeholder="搜索股票代码或名称..."
        @keyup.enter="onSearch"
      />
    </div>

    <!-- 搜索结果 -->
    <div v-if="stockStore.searchResults.length" class="list-section" style="margin-bottom: 32px">
      <div class="card-title" style="margin-bottom: 8px">搜索结果</div>
      <div
        v-for="s in stockStore.searchResults"
        :key="s.ts_code"
        class="list-item"
        @click="goDetail(s.ts_code)"
      >
        <div>
          <strong>{{ s.name }}</strong>
          <span style="color: var(--text-tertiary); margin-left: 8px; font-size: 13px">{{ s.ts_code }}</span>
        </div>
        <div>
          <span v-if="s.industry" class="tag">{{ s.industry }}</span>
        </div>
      </div>
    </div>

    <!-- 最新复盘摘要 -->
    <div v-if="latestReview" style="margin-bottom: 32px">
      <div class="card">
        <div class="card-title">最新AI复盘 — {{ latestReview.review_date }}</div>
        <div class="card-body">{{ latestReview.market_summary || '暂无综述' }}</div>
        <router-link to="/review" class="btn" style="margin-top: 12px">查看完整复盘</router-link>
      </div>
    </div>

    <!-- 自选股快照 -->
    <div v-if="stockStore.watchlist.length">
      <div class="card-title" style="margin-bottom: 8px">我的自选</div>
      <div class="list-section">
        <div
          v-for="w in stockStore.watchlist"
          :key="w.ts_code"
          class="list-item"
          @click="goDetail(w.ts_code)"
        >
          <strong>{{ w.stock_name }}</strong>
          <span style="color: var(--text-tertiary); font-size: 13px">{{ w.ts_code }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStockStore } from '@/stores/stock'
import { getLatestReview, type AIReview } from '@/api'

const router = useRouter()
const stockStore = useStockStore()
const keyword = ref('')
const latestReview = ref<AIReview | null>(null)

function onSearch() {
  if (keyword.value.trim()) {
    stockStore.search(keyword.value.trim())
  }
}

function goDetail(tsCode: string) {
  router.push({ name: 'stock-detail', params: { tsCode } })
}

onMounted(async () => {
  stockStore.fetchWatchlist()
  try {
    const { data } = await getLatestReview()
    latestReview.value = data
  } catch { /* 后端未启动时静默 */ }
})
</script>
