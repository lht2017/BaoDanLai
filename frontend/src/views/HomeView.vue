<template>
  <div>
    <!-- ① 头部标题区 -->
    <div class="page-header">
      <h1 class="page-title">市场总览</h1>
      <p class="page-subtitle">A股涨停股全景复盘 — 今日共 <strong style="color: var(--color-blue)">{{ metrics.total_limit_up }}</strong> 只涨停</p>
    </div>

    <!-- ② 顶部关键指标 -->
    <LimitUpMetrics :metrics="metrics" style="margin-bottom: 32px" />

    <!-- ③ 涨停股列表 -->
    <div class="section-title">涨停股列表</div>
    <div class="card zt-table-card" style="padding: 0; overflow: hidden; margin-bottom: 16px">
      <LimitUpTable :list="stocks" @expand="onExpand" />
    </div>

    <!-- ④ 个股详情面板 -->
    <StockDetailPanel :stock="expandedStock" />

    <!-- ⑤ 底部操作按钮 -->
    <div class="action-bar zt-bottom-bar">
      <button class="btn" @click="onRefresh">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2v6h-6"/><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M3 22v-6h6"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/></svg>
        刷新数据
      </button>
      <button class="btn" @click="onExport">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        导出复盘
      </button>
      <button class="btn btn-accent" @click="onAIAnalyze">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
        生成AI分析
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import LimitUpMetrics from '@/components/LimitUpMetrics.vue'
import LimitUpTable from '@/components/LimitUpTable.vue'
import StockDetailPanel from '@/components/StockDetailPanel.vue'
import type { LimitUpStock, MarketMetrics } from '@/types/limit-up'

const metrics = ref<MarketMetrics>({
  total_limit_up: 67,
  max_consecutive: 5,
  broken_board_rate: 23.5,
  sentiment: 'high',
})

const stocks = ref<LimitUpStock[]>([
  { ts_code: '000001.SZ', name: '平安银行', consecutive_boards: 1, concepts: ['金融科技', '银行', '深证成指'], float_market_cap: 2850, limit_up_time: '09:32:15', pe_ratio: 5.2, profit_growth: 12.3, is_st: false, ai_logic: '金融科技政策催化', ai_risk: '大盘波动风险', ai_attention: '关注' },
  { ts_code: '002594.SZ', name: '比亚迪', consecutive_boards: 3, concepts: ['新能源汽车', '固态电池', '储能'], float_market_cap: 6800, limit_up_time: '09:45:30', pe_ratio: 22.1, profit_growth: 35.6, is_st: false, ai_logic: '固态电池量产预期', ai_risk: '估值偏高', ai_attention: '高度关注' },
  { ts_code: '300750.SZ', name: '宁德时代', consecutive_boards: 2, concepts: ['锂电池', '储能', '新能源'], float_market_cap: 9200, limit_up_time: '10:02:18', pe_ratio: 18.5, profit_growth: 28.9, is_st: false, ai_logic: '储能订单超预期', ai_risk: '行业产能过剩', ai_attention: '高度关注' },
  { ts_code: '600519.SH', name: '贵州茅台', consecutive_boards: 1, concepts: ['白酒', '消费龙头', '沪股通'], float_market_cap: 21000, limit_up_time: '10:15:42', pe_ratio: 28.3, profit_growth: 15.2, is_st: false, ai_logic: '白酒板块轮动', ai_risk: '消费数据承压', ai_attention: '一般关注' },
  { ts_code: '002475.SZ', name: '立讯精密', consecutive_boards: 5, concepts: ['苹果产业链', 'AI硬件', '机器人'], float_market_cap: 3200, limit_up_time: '09:25:03', pe_ratio: 32.1, profit_growth: 45.8, is_st: false, ai_logic: 'AI硬件订单爆发+机器人概念', ai_risk: '客户集中度高', ai_attention: '高度关注' },
  { ts_code: '600036.SH', name: '招商银行', consecutive_boards: 1, concepts: ['银行', '金融科技', '高股息'], float_market_cap: 7800, limit_up_time: '13:05:22', pe_ratio: 6.8, profit_growth: 8.5, is_st: false, ai_logic: '高股息策略', ai_risk: '息差收窄', ai_attention: '一般关注' },
  { ts_code: '002230.SZ', name: '科大讯飞', consecutive_boards: 2, concepts: ['AI大模型', '教育', '国产算力'], float_market_cap: 950, limit_up_time: '09:38:10', pe_ratio: 120.5, profit_growth: -5.2, is_st: false, ai_logic: 'AI大模型商业化加速', ai_risk: '持续亏损', ai_attention: '高度关注' },
  { ts_code: '300059.SZ', name: '东方财富', consecutive_boards: 1, concepts: ['券商', '互联网', '基金销售'], float_market_cap: 2100, limit_up_time: '10:28:55', pe_ratio: 25.6, profit_growth: 18.7, is_st: false, ai_logic: '市场成交回暖', ai_risk: '监管政策变化', ai_attention: '关注' },
  { ts_code: '000651.SZ', name: '格力电器', consecutive_boards: 1, concepts: ['家电', '高股息', '智能制造'], float_market_cap: 2200, limit_up_time: '13:42:08', pe_ratio: 8.1, profit_growth: 5.3, is_st: false, ai_logic: '家电以旧换新政策', ai_risk: '地产周期拖累', ai_attention: '一般关注' },
  { ts_code: '002415.SZ', name: '海康威视', consecutive_boards: 4, concepts: ['AI安防', '机器人', '国企改革'], float_market_cap: 2800, limit_up_time: '09:41:33', pe_ratio: 15.8, profit_growth: 22.4, is_st: false, ai_logic: '安防AI化+机器人业务拓展', ai_risk: '海外市场风险', ai_attention: '高度关注' },
])

const expandedCode = ref<string | null>(null)

const expandedStock = computed(() => {
  if (!expandedCode.value) return null
  return stocks.value.find(s => s.ts_code === expandedCode.value) ?? null
})

function onExpand(code: string | null) {
  expandedCode.value = code
}

function onRefresh() {
  window.location.reload()
}

function onExport() {
  // TODO: 对接导出API
}

function onAIAnalyze() {
  // TODO: 对接AI分析API
}
</script>
