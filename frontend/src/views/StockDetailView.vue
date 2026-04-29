<template>
  <div>
    <h1 class="page-title">{{ tsCode }}</h1>
    <p class="page-subtitle">个股详情与日K线数据</p>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else>
      <!-- 操作栏 -->
      <div style="margin-bottom: 20px; display: flex; gap: 8px">
        <button class="btn" @click="toggleWatch">
          {{ isWatched ? '移出自选' : '加入自选' }}
        </button>
      </div>

      <!-- K线表格 -->
      <div v-if="quotes.length" class="card">
        <table style="width: 100%; border-collapse: collapse; font-size: 13px">
          <thead>
            <tr style="border-bottom: 1px solid var(--border-color)">
              <th style="padding: 8px; text-align: left">日期</th>
              <th style="padding: 8px; text-align: right">开盘</th>
              <th style="padding: 8px; text-align: right">最高</th>
              <th style="padding: 8px; text-align: right">最低</th>
              <th style="padding: 8px; text-align: right">收盘</th>
              <th style="padding: 8px; text-align: right">涨跌%</th>
              <th style="padding: 8px; text-align: right">成交量</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="q in quotes" :key="q.trade_date" class="list-item" style="border-radius: 0">
              <td style="padding: 8px">{{ q.trade_date }}</td>
              <td style="padding: 8px; text-align: right">{{ q.open.toFixed(2) }}</td>
              <td style="padding: 8px; text-align: right">{{ q.high.toFixed(2) }}</td>
              <td style="padding: 8px; text-align: right">{{ q.low.toFixed(2) }}</td>
              <td style="padding: 8px; text-align: right">{{ q.close.toFixed(2) }}</td>
              <td :class="pctClass(q.change_pct)" style="padding: 8px; text-align: right">
                {{ q.change_pct?.toFixed(2) ?? '—' }}%
              </td>
              <td style="padding: 8px; text-align: right; color: var(--text-tertiary)">
                {{ q.vol ? (q.vol / 10000).toFixed(0) + '万' : '—' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="empty-state">暂无行情数据</div>
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
