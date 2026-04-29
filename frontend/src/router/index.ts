/**
 * Vue Router 路由配置
 * 后期迁移小程序时，路由映射为小程序页面
 */

import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
      meta: { title: '市场总览' },
    },
    {
      path: '/review',
      name: 'review',
      component: () => import('@/views/ReviewView.vue'),
      meta: { title: 'AI复盘' },
    },
    {
      path: '/stock/:tsCode',
      name: 'stock-detail',
      component: () => import('@/views/StockDetailView.vue'),
      meta: { title: '个股详情' },
    },
    {
      path: '/watchlist',
      name: 'watchlist',
      component: () => import('@/views/WatchlistView.vue'),
      meta: { title: '自选股' },
    },
    {
      path: '/news',
      name: 'news',
      component: () => import('@/views/NewsView.vue'),
      meta: { title: '财经快讯' },
    },
  ],
})

router.beforeEach((to) => {
  document.title = `${to.meta.title ?? '爆单来'} — 爆单来`
})

export default router
