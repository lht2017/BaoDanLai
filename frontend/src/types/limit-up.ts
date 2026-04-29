export interface LimitUpStock {
  ts_code: string
  name: string
  consecutive_boards: number
  concepts: string[]
  float_market_cap: number
  limit_up_time: string
  pe_ratio: number | null
  profit_growth: number | null
  is_st: boolean
  ai_logic: string
  ai_risk: string
  ai_attention: string
}

export interface MarketMetrics {
  total_limit_up: number
  max_consecutive: number
  broken_board_rate: number
  sentiment: 'low' | 'medium' | 'high'
}
