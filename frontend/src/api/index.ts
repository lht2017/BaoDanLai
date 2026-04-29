/**
 * API 客户端 — 统一封装后端请求
 * 后期迁移小程序时只需替换 axios 为 wx.request
 */

import axios from 'axios'

const http = axios.create({
  baseURL: '/api/v1',
  timeout: 15000,
})

// ── 股票 ──

export interface Stock {
  id: number
  ts_code: string
  symbol: string
  name: string
  industry: string | null
  market: string | null
}

export interface WatchlistItem {
  id: number
  ts_code: string
  stock_name: string
  note: string | null
  created_at: string | null
}

export interface DailyQuote {
  ts_code: string
  trade_date: string
  open: number
  high: number
  low: number
  close: number
  pre_close: number | null
  change_pct: number | null
  vol: number | null
}

export const searchStocks = (keyword: string) =>
  http.get<Stock[]>('/stocks/search', { params: { keyword } })

export const getStockDaily = (tsCode: string, limit = 60) =>
  http.get<DailyQuote[]>(`/stocks/${tsCode}/daily`, { params: { limit } })

export const getWatchlist = () =>
  http.get('/stocks/watchlist')

export const addToWatchlist = (ts_code: string, stock_name: string, note?: string) =>
  http.post('/stocks/watchlist', { ts_code, stock_name, note })

export const removeFromWatchlist = (ts_code: string) =>
  http.delete(`/stocks/watchlist/${ts_code}`)

// ── 复盘 ──

export interface AIReview {
  id: number
  review_date: string
  market_summary: string | null
  hot_sectors: string | null
  risk_warning: string | null
  strategy_advice: string | null
}

export interface ReviewDetail {
  review: AIReview
  picks: StockPick[]
}

export interface StockPick {
  ts_code: string
  stock_name: string
  analysis: string
  rating: string | null
  reason_tags: string | null
}

export const getLatestReview = () =>
  http.get<AIReview | null>('/reviews/latest')

export const getReviewList = (limit = 30) =>
  http.get<AIReview[]>('/reviews/list', { params: { limit } })

export const getReviewDetail = (date: string) =>
  http.get<ReviewDetail | null>(`/reviews/${date}`)

// ── 新闻 ──

export interface NewsItem {
  id: number
  title: string
  source: string | null
  url: string | null
  content: string | null
  importance: number
  tags: string | null
  published_at: string | null
}

export const getNewsList = (importance?: number, limit = 50, offset = 0) =>
  http.get<NewsItem[]>('/news/', { params: { importance, limit, offset } })
