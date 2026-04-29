<template>
  <div>
    <h1 class="page-title">自选股</h1>
    <p class="page-subtitle">关注列表，实时跟踪</p>

    <div v-if="!stockStore.watchlist.length" class="empty-state">
      暂无自选股，去首页搜索添加
    </div>

    <div v-else class="list-section">
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
        <button class="btn" @click.stop="stockStore.removeStock(w.ts_code)">移除</button>
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
