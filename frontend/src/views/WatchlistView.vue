<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">自选股</h1>
      <p class="page-subtitle">关注列表，实时跟踪</p>
    </div>

    <div v-if="!stockStore.watchlist.length" class="empty-state">
      <div class="empty-state-icon">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
      </div>
      暂无自选股，去首页搜索添加
    </div>

    <div v-else>
      <div class="section-title">{{ stockStore.watchlist.length }} 只自选</div>
      <div class="card" style="padding: 8px">
        <div
          v-for="w in stockStore.watchlist"
          :key="w.ts_code"
          class="list-item"
          @click="$router.push({ name: 'stock-detail', params: { tsCode: w.ts_code } })"
        >
          <div>
            <strong>{{ w.stock_name }}</strong>
            <span style="color: var(--text-tertiary); margin-left: 8px; font-size: 13px">{{ w.ts_code }}</span>
          </div>
          <button class="btn btn-ghost" @click.stop="stockStore.removeStock(w.ts_code)">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            移除
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useStockStore } from '@/stores/stock'

const stockStore = useStockStore()

onMounted(() => {
  stockStore.fetchWatchlist()
})
</script>
