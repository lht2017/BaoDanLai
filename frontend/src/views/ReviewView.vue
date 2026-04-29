<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">AI复盘</h1>
      <p class="page-subtitle">基于AI的每日市场分析与策略建议</p>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="!detail" class="empty-state">
      <div class="empty-state-icon">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      </div>
      今日暂无复盘报告，请稍后查看
    </div>

    <div v-else>
      <!-- 日期选择 -->
      <div style="margin-bottom: 24px">
        <input type="date" v-model="selectedDate" class="search-box" style="width: auto; max-width: 200px" @change="loadDetail" />
      </div>

      <div style="display: flex; flex-direction: column; gap: 16px">
        <!-- 大盘综述 -->
        <div class="card">
          <div class="card-title">大盘综述</div>
          <div class="card-body">{{ detail.review.market_summary }}</div>
        </div>

        <!-- 热门板块 -->
        <div class="card">
          <div class="card-title">热门板块</div>
          <div class="card-body">{{ detail.review.hot_sectors || '暂无' }}</div>
        </div>

        <!-- 风险提示 -->
        <div class="card">
          <div class="card-title">风险提示</div>
          <div class="card-body">{{ detail.review.risk_warning || '暂无' }}</div>
        </div>

        <!-- 操作建议 -->
        <div class="card">
          <div class="card-title">操作建议</div>
          <div class="card-body">{{ detail.review.strategy_advice || '暂无' }}</div>
        </div>

        <!-- 个股点评 -->
        <div v-if="detail.picks.length">
          <div class="section-title" style="margin-top: 8px">个股点评</div>
          <div style="display: flex; flex-direction: column; gap: 12px">
            <div
              v-for="pick in detail.picks"
              :key="pick.ts_code"
              class="card"
            >
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px">
                <div>
                  <strong>{{ pick.stock_name }}</strong>
                  <span style="color: var(--text-tertiary); margin-left: 8px; font-size: 13px">{{ pick.ts_code }}</span>
                </div>
                <span :class="ratingClass(pick.rating)">{{ pick.rating || '—' }}</span>
              </div>
              <div class="card-body">{{ pick.analysis }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getLatestReview, getReviewDetail, type ReviewDetail } from '@/api'

const loading = ref(true)
const detail = ref<ReviewDetail | null>(null)
const selectedDate = ref('')

function ratingClass(rating: string | null) {
  if (rating === '看多') return 'tag tag-green'
  if (rating === '看空') return 'tag tag-red'
  return 'tag'
}

async function loadDetail() {
  if (!selectedDate.value) return
  loading.value = true
  try {
    const { data } = await getReviewDetail(selectedDate.value)
    detail.value = data
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    const { data } = await getLatestReview()
    if (data) {
      selectedDate.value = data.review_date
      await loadDetail()
    }
  } finally {
    loading.value = false
  }
})
</script>
