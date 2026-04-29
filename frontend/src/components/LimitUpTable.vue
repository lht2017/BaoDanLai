<template>
  <div>
    <!-- 表头 -->
    <div class="zt-table-header">
      <div class="zt-col zt-col-code" @click="toggleSort('ts_code')">
        代码
        <svg v-if="sortKey === 'ts_code'" class="sort-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline :points="sortAsc ? '18 15 12 9 6 15' : '6 9 12 15 18 9'" /></svg>
      </div>
      <div class="zt-col zt-col-name">名称</div>
      <div class="zt-col zt-col-boards" @click="toggleSort('consecutive_boards')">
        连板
        <svg v-if="sortKey === 'consecutive_boards'" class="sort-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline :points="sortAsc ? '18 15 12 9 6 15' : '6 9 12 15 18 9'" /></svg>
      </div>
      <div class="zt-col zt-col-concept">所属概念</div>
      <div class="zt-col zt-col-cap" @click="toggleSort('float_market_cap')">
        流通市值
        <svg v-if="sortKey === 'float_market_cap'" class="sort-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline :points="sortAsc ? '18 15 12 9 6 15' : '6 9 12 15 18 9'" /></svg>
      </div>
      <div class="zt-col zt-col-time" @click="toggleSort('limit_up_time')">
        涨停时间
        <svg v-if="sortKey === 'limit_up_time'" class="sort-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline :points="sortAsc ? '18 15 12 9 6 15' : '6 9 12 15 18 9'" /></svg>
      </div>
    </div>

    <!-- 表体 -->
    <div class="zt-table-body">
      <div
        v-for="stock in sortedList"
        :key="stock.ts_code"
        class="zt-row"
        :class="{
          'zt-row-expanded': expandedCode === stock.ts_code,
          'zt-row-hot': stock.consecutive_boards >= 3,
        }"
        @click="toggleExpand(stock.ts_code)"
      >
        <div class="zt-col zt-col-code">
          <span class="zt-toggle">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" :style="{ transform: expandedCode === stock.ts_code ? 'rotate(90deg)' : '', transition: 'transform 0.15s' }"><polyline points="9 18 15 12 9 6"/></svg>
          </span>
          {{ stock.ts_code }}
        </div>
        <div class="zt-col zt-col-name">
          <strong>{{ stock.name }}</strong>
          <span v-if="stock.is_st" class="tag tag-red" style="margin-left: 4px">ST</span>
        </div>
        <div class="zt-col zt-col-boards">
          <span class="zt-board-badge" :class="boardClass(stock.consecutive_boards)">{{ stock.consecutive_boards }}板</span>
        </div>
        <div class="zt-col zt-col-concept">
          <span v-for="c in stock.concepts.slice(0, 3)" :key="c" class="tag" style="margin-right: 4px; margin-bottom: 2px">{{ c }}</span>
          <span v-if="stock.concepts.length > 3" class="tag">+{{ stock.concepts.length - 3 }}</span>
        </div>
        <div class="zt-col zt-col-cap">{{ formatCap(stock.float_market_cap) }}</div>
        <div class="zt-col zt-col-time zt-time">{{ stock.limit_up_time }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { LimitUpStock } from '@/types/limit-up'

const props = defineProps<{ list: LimitUpStock[] }>()
const emit = defineEmits<{ expand: [code: string | null] }>()

const sortKey = ref<keyof LimitUpStock>('consecutive_boards')
const sortAsc = ref(false)
const expandedCode = ref<string | null>(null)

const sortedList = computed(() => {
  const arr = [...props.list]
  const key = sortKey.value
  arr.sort((a, b) => {
    const va = a[key]
    const vb = b[key]
    if (typeof va === 'number' && typeof vb === 'number') {
      return sortAsc.value ? va - vb : vb - va
    }
    return sortAsc.value ? String(va).localeCompare(String(vb)) : String(vb).localeCompare(String(va))
  })
  return arr
})

function toggleSort(key: keyof LimitUpStock) {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value
  } else {
    sortKey.value = key
    sortAsc.value = false
  }
}

function toggleExpand(code: string) {
  expandedCode.value = expandedCode.value === code ? null : code
  emit('expand', expandedCode.value)
}

function boardClass(n: number) {
  if (n >= 5) return 'board-high'
  if (n >= 3) return 'board-mid'
  return 'board-low'
}

function formatCap(val: number) {
  if (val >= 100) return (val / 100).toFixed(1) + '百亿'
  return val.toFixed(1) + '亿'
}
</script>
