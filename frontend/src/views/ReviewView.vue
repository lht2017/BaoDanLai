<template>
  <div>
    <h1 class="page-title">AI复盘</h1>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="!detail" class="empty-state">
      今日暂无复盘报告，请稍后查看
    </div>

    <div v-else>
      <!-- 日期选择 -->
      <div style="margin-bottom: 20px">
        <input type="date" v-model="selectedDate" class="search-box" style="width: auto" @change="loadDetail" />
      </div>

      <!-- 大盘综述 -->
      <div class="card" style="margin-bottom: 20px">
        <div class="card-title">大盘综述</div>
        <div class="card-body">{{ detail.review.market_summary }}</div>
      </div>

      <!-- 热门板块 -->
      <div class="card" style="margin-bottom: 20px">
        <div class="card-title">热门板块</div>
        <div class="card-body">{{ detail.review.hot_sectors || '暂无' }}</div>
      </div>

      <!-- 风险提示 -->
      <div class="card" style="margin-bottom: 20px">
        <div class="card-title">风险提示</div>
        <div class="card-body">{{ detail.review.risk_warning || '暂无' }}</div>
      </div>

      <!-- 操作建议 -->
      <div class="card" style="margin-bottom: 20px">
        <div class="card-title">操作建议</div>
        <div class="card-body">{{ detail.review.strategy_advice || '暂无' }}</div>
      </div>

      <!-- 个股点评 -->
      <div v-if="detail.picks.length">
        <div class="card-title" style="margin-bottom: 8px">个股点评</div>
        <div class="list-section">
          <div
            v-for="pick in detail.picks"
            :key="pick.ts_code"
            class="card"
            style="margin-bottom: 8px"
          >
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px">
              <strong>{{ pick.stock_name }} <span style="color: var(--text-tertiary); font-size: 13px">{{ pick.ts_code }}</span></strong>
              <span :class="ratingClass(pick.rating)">{{ pick.rating || '—' }}</span>
            </div>
            <div class="card-body">{{ pick.analysis }}</div>
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
