<template>
  <aside class="sidebar">
    <div class="sidebar-brand">爆单来</div>
    <ul class="sidebar-nav">
      <li>
        <router-link to="/">
          <span class="nav-icon">&#9632;</span>
          市场总览
        </router-link>
      </li>
      <li>
        <router-link to="/review">
          <span class="nav-icon">&#9733;</span>
          AI复盘
        </router-link>
      </li>
      <li>
        <router-link to="/watchlist">
          <span class="nav-icon">&#9830;</span>
          自选股
        </router-link>
      </li>
      <li>
        <router-link to="/news">
          <span class="nav-icon">&#9993;</span>
          财经快讯
        </router-link>
      </li>
    </ul>
  </aside>
</template>

<style scoped>
.nav-icon {
  font-size: 14px;
  opacity: 0.6;
}
</style>
