<template>
  <div class="metrics-grid">
    <div class="metric-card">
      <div class="metric-label">涨停总数</div>
      <div class="metric-value text-accent">{{ metrics.total_limit_up }}</div>
      <div class="metric-unit">今日涨停</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">最高连板</div>
      <div class="metric-value text-up">{{ metrics.max_consecutive }}板</div>
      <div class="metric-unit">连板梯队</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">炸板率</div>
      <div class="metric-value" :class="brokenRateClass">{{ metrics.broken_board_rate }}%</div>
      <div class="metric-unit">封板成功 {{ 100 - metrics.broken_board_rate }}%</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">市场情绪</div>
      <div class="metric-value" :class="sentimentClass">{{ sentimentLabel }}</div>
      <div class="metric-unit">当日情绪指标</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { MarketMetrics } from '@/types/limit-up'

const props = defineProps<{ metrics: MarketMetrics }>()

const sentimentLabel = computed(() => {
  const map = { low: '低迷', medium: '温和', high: '高涨' }
  return map[props.metrics.sentiment]
})

const sentimentClass = computed(() => {
  const map = { low: 'text-down', medium: '', high: 'text-up' }
  return map[props.metrics.sentiment]
})

const brokenRateClass = computed(() => {
  const r = props.metrics.broken_board_rate
  if (r > 30) return 'text-up'
  if (r < 20) return 'text-down'
  return ''
})
</script>
