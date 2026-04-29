<template>
  <aside class="sidebar">
    <div class="sidebar-brand">
      <div class="sidebar-brand-icon">爆</div>
      <span>爆单来</span>
    </div>
    <div class="sidebar-divider"></div>
    <ul class="sidebar-nav">
      <li>
        <router-link to="/">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="12" width="4" height="9" rx="1" />
            <rect x="10" y="7" width="4" height="14" rx="1" />
            <rect x="17" y="3" width="4" height="18" rx="1" />
          </svg>
          市场总览
        </router-link>
      </li>
      <li>
        <router-link to="/review">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4L12 16.8l-6.2 4.5 2.4-7.4L2 9.4h7.6z" />
          </svg>
          AI复盘
        </router-link>
      </li>
      <li>
        <router-link to="/watchlist">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" />
          </svg>
          自选股
        </router-link>
      </li>
      <li>
        <router-link to="/news">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2" />
            <line x1="10" y1="6" x2="18" y2="6" />
            <line x1="10" y1="10" x2="18" y2="10" />
            <line x1="10" y1="14" x2="14" y2="14" />
          </svg>
          财经快讯
        </router-link>
      </li>
    </ul>
    <div class="sidebar-footer">
      爆单来 v1.0
    </div>
  </aside>
</template>
