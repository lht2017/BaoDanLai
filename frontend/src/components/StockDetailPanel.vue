<template>
  <transition name="slide">
    <div v-if="stock" class="detail-panel">
      <div class="detail-grid">
        <!-- 所属概念 -->
        <div class="detail-card">
          <div class="detail-label">所属概念</div>
          <div class="detail-tags">
            <span v-for="c in stock.concepts" :key="c" class="tag tag-blue">{{ c }}</span>
          </div>
        </div>

        <!-- 核心基本面 -->
        <div class="detail-card">
          <div class="detail-label">核心基本面</div>
          <div class="detail-values">
            <div class="detail-item">
              <span class="detail-item-label">市盈率</span>
              <span class="detail-item-value">{{ stock.pe_ratio != null ? stock.pe_ratio.toFixed(1) : '—' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-item-label">业绩增速</span>
              <span class="detail-item-value" :class="growthClass(stock.profit_growth)">
                {{ stock.profit_growth != null ? (stock.profit_growth >= 0 ? '+' : '') + stock.profit_growth.toFixed(1) + '%' : '—' }}
              </span>
            </div>
            <div class="detail-item">
              <span class="detail-item-label">ST状态</span>
              <span class="detail-item-value" :class="stock.is_st ? 'text-up' : 'text-down'">{{ stock.is_st ? 'ST风险' : '正常' }}</span>
            </div>
          </div>
        </div>

        <!-- AI 分析 -->
        <div class="detail-card">
          <div class="detail-label">AI 分析结论</div>
          <div class="detail-ai-grid">
            <div class="detail-ai-item">
              <div class="detail-ai-title">炒作逻辑</div>
              <div class="detail-ai-body">{{ stock.ai_logic || '待分析' }}</div>
            </div>
            <div class="detail-ai-item">
              <div class="detail-ai-title">风险点</div>
              <div class="detail-ai-body">{{ stock.ai_risk || '待分析' }}</div>
            </div>
            <div class="detail-ai-item">
              <div class="detail-ai-title">明日关注度</div>
              <div class="detail-ai-body">{{ stock.ai_attention || '待分析' }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import type { LimitUpStock } from '@/types/limit-up'

defineProps<{ stock: LimitUpStock | null }>()

function growthClass(val: number | null) {
  if (val == null) return ''
  return val >= 0 ? 'text-up' : 'text-down'
}
</script>
