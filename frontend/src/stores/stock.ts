/**
 * Pinia Store — 股票/自选股状态管理
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  searchStocks as apiSearch,
  getWatchlist as apiGetWatchlist,
  addToWatchlist as apiAdd,
  removeFromWatchlist as apiRemove,
  type Stock,
  type WatchlistItem,
} from '../api'

export const useStockStore = defineStore('stock', () => {
  const searchResults = ref<Stock[]>([])
  const watchlist = ref<WatchlistItem[]>([])
  const loading = ref(false)

  async function search(keyword: string) {
    loading.value = true
    try {
      const { data } = await apiSearch(keyword)
      searchResults.value = data
    } finally {
      loading.value = false
    }
  }

  async function fetchWatchlist() {
    const { data } = await apiGetWatchlist()
    watchlist.value = data
  }

  async function addStock(ts_code: string, stock_name: string, note?: string) {
    await apiAdd(ts_code, stock_name, note)
    await fetchWatchlist()
  }

  async function removeStock(ts_code: string) {
    await apiRemove(ts_code)
    await fetchWatchlist()
  }

  return { searchResults, watchlist, loading, search, fetchWatchlist, addStock, removeStock }
})
