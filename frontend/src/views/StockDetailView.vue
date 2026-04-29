<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">{{ tsCode }}</h1>
      <p class="page-subtitle">个股详情与日K线数据</p>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else>
      <!-- 操作栏 -->
      <div class="action-bar" style="margin-bottom: 24px">
        <button :class="['btn', isWatched ? 'btn-primary' : 'btn-accent']" @click="toggleWatch">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
          {{ isWatched ? '移出自选' : '加入自选' }}
        </button>
      </div>

      <!-- K线表格 -->
      <div v-if="quotes.length" class="card" style="padding: 0; overflow: hidden">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px">
          <thead>
            <tr style="border-bottom: 1px solid var(--border-color)">
              <th style="padding: 12px 16px; text-align: left; font-weight: 600; font-size: 12px; color: var(--text-tertiary)">日期</th>
              <th style="padding: 12px 16px; text-align: right; font-weight: 600; font-size: 12px; color: var(--text-tertiary)">开盘</th>
              <th style="padding: 12px 16px; text-align: right; font-weight: 600; font-size: 12px; color: var(--text-tertiary)">最高</th>
              <th style="padding: 12px 16px; text-align: right; font-weight: 600; font-size: 12px; color: var(--text-tertiary)">最低</th>
              <th style="padding: 12px 16px; text-align: right; font-weight: 600; font-size: 12px; color: var(--text-tertiary)">收盘</th>
              <th style="padding: 12px 16px; text-align: right; font-weight: 600; font-size: 12px; color: var(--text-tertiary)">涨跌%</th>
              <th style="padding: 12px 16px; text-align: right; font-weight: 600; font-size: 12px; color: var(--text-tertiary)">成交量</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="q in quotes" :key="q.trade_date" style="border-bottom: 1px solid var(--border-color); transition: background 0.15s; cursor: default" onmouseover="this.style.background='var(--bg-hover)'" onmouseout="this.style.background='transparent'">
              <td style="padding: 10px 16px; color: var(--text-secondary)">{{ q.trade_date }}</td>
              <td style="padding: 10px 16px; text-align: right">{{ q.open.toFixed(2) }}</td>
              <td style="padding: 10px 16px; text-align: right">{{ q.high.toFixed(2) }}</td>
              <td style="padding: 10px 16px; text-align: right">{{ q.low.toFixed(2) }}</td>
              <td style="padding: 10px 16px; text-align: right; font-weight: 500">{{ q.close.toFixed(2) }}</td>
              <td :class="pctClass(q.change_pct)" style="padding: 10px 16px; text-align: right; font-weight: 500">
                {{ q.change_pct?.toFixed(2) ?? '—' }}%
              </td>
              <td style="padding: 10px 16px; text-align: right; color: var(--text-tertiary)">
                {{ q.vol ? (q.vol / 10000).toFixed(0) + '万' : '—' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="empty-state">
        <div class="empty-state-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
        </div>
        暂无行情数据
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getStockDaily, type DailyQuote } from '@/api'
import { useStockStore } from '@/stores/stock'

const route = useRoute()
const stockStore = useStockStore()
const tsCode = route.params.tsCode as string
const loading = ref(true)
const quotes = ref<DailyQuote[]>([])

const isWatched = computed(() => stockStore.watchlist.some(w => w.ts_code === tsCode))

function pctClass(pct: number | null) {
  if (pct == null) return ''
  return pct >= 0 ? 'tag-green' : 'tag-red'
}

async function toggleWatch() {
  if (isWatched.value) {
    await stockStore.removeStock(tsCode)
  } else {
    await stockStore.addStock(tsCode, tsCode)
  }
}

onMounted(async () => {
  try {
    const { data } = await getStockDaily(tsCode)
    quotes.value = data
  } finally {
    loading.value = false
  }
})
</script>
