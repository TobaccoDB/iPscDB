<template>
    <div id="app" style="background:#fafafa;">
        <!-- <router-view v-if="isRouterAlive"></router-view> -->
        <keep-alive>
            <router-view v-if="$route.meta.keepAlive && isRouterAlive"></router-view>
        </keep-alive>
        <router-view v-if="!$route.meta.keepAlive && isRouterAlive"></router-view>
    </div>
</template>
<script>
export default {
    name: 'App',
    provide() {
        return {
            reload: this.reload
        }
    },
    data() {
        return {
            isRouterAlive: true
        }
    },
    methods: {
        reload() {
            this.isRouterAlive = false;
            this.$nextTick(function () {
                this.isRouterAlive = true
            });
        },
    },

}
</script>
<style>
@import "./assets/css/main.css";
/* @import "./assets/css/color-dark.css"; */ /*深色主题*/
/* @import "./assets/css/theme-selfs/index.css";  绿色主题 */
@import "./assets/css/theme/index.css"; /*  绿色主题 */
.el-button.is-disabled,
.el-button.is-disabled:focus,
.el-button.is-disabled:hover {
  color: #bfcbd9;
  cursor: not-allowed;
  background-image: none;
  background-color: #eef1f6;
  border-color: #d1dbe5;
}
.el-table .cell {
  word-break: break-word !important;
}

#nprogress .bar {
  background: #8dc21f !important;
  /* 进度条自定义颜色 */
}
</style>