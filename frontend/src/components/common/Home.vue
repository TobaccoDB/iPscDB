<template>
    <div class="home">
        <div class="banner">
            <div class="home-logo">
                <img src="~@/assets/img/logo1.png" alt="logo" />
                <span>iPscDB</span>
            </div>
            <p class="banner_title">
                <span>I</span>ntegrated
                <span>P</span>lant
                <span>S</span>
                <span style="color: #fff">ingle</span>-
                <span>C</span>ell
                <span>D</span>
                <span style="color: #fff">ata</span>
                <span>b</span>ase
            </p>
            <p class="banner_p">
                iPscDB is a single-cell transcriptomics data resource that provides<br />a comprehensive and relatively accurate
                atlas of cell integration<br />for different tissues of different plants.
            </p>
        </div>
        <v-head></v-head>
        <!--  <div class="content-box" ref="main" :style="{ height: contentHeight }"> -->
        <div class="content-box" ref="main">
            <!-- <div class="content" :style="{ minHeight: scrollerHeight }"> -->
            <div class="content">
                <transition name="move" mode="out-in">
                    <keep-alive :include="tagsList">
                        <router-view></router-view>
                    </keep-alive>
                </transition>
            </div>
            <v-footer></v-footer>
        </div>
    </div>
</template>

<script>
import vHead from './Header.vue'
import vFooter from './Footer.vue'
import bus from './bus'
import { total_data } from '@/api/api'
export default {
    data() {
        return {
            tagsList: [],
            contentHeight: window.innerHeight - 60 - +'px',
            scrollerHeight: window.innerHeight - 100 - 60 - 60 + 'px',
            screenHeight: document.body.clientHeight,
            timer: false
        }
    },
    watch: {
        screenHeight(val) {
            // 为了避免频繁触发resize函数导致页面卡顿，使用定时器
            if (!this.timer) {
                // 一旦监听到的screenHeight值改变，就将其重新赋给data里的screenHeight
                // this.screenHeight = val
                this.contentHeight = val - 60 + 'px'
                this.scrollerHeight = val - 100 - 60 - 60 + 'px'
                this.timer = true
                let that = this
                setTimeout(function () {
                    // 打印screenHeight变化的值
                    that.timer = false
                }, 400)
            }
        },
        $route() {
            let main = this.$refs.main
            main.scrollTo(0, 0)
        }
    },
    components: {
        vHead,
        vFooter
    },
    mounted() {
        this.init()
    },
    methods: {
        init() {
            const that = this
            let firstFire = null
            window.onresize = function () {
                if (firstFire === null) {
                    firstFire = setTimeout(function () {
                        firstFire = null
                        return (() => {
                            window.screenHeight = window.innerHeight
                            that.screenHeight = window.screenHeight
                        })()
                    }, 100)
                }
            }
        }
    }
}
</script>
<style lang="scss" scoped>
.home {
  .banner {
    width: 100%;
    height: 300px;
    background: url(~@/assets/img/banner2024.png) no-repeat center;
    position: relative;
    .home-logo {
      width: 120px;
      height: 33px;
      font-family: PingFangSC-Medium;
      font-size: 24px;
      color: #ffffff;
      font-weight: 500;
      position: absolute;
      left: calc(50% - 620px);
      top: 19px;
      display: flex;
      align-items: center;
      img {
        width: 32px;
        height: 32px;
        margin-right: 5px;
      }
    }

    // background-image: linear-gradient(-45deg, #00a35f, #009e6e);
    background-size: 100% 100%;
    .banner_title {
      width: 1240px;
      height: auto;
      margin: 0 auto;
      overflow: hidden;
      color: #fff;
      font-weight: bold;
      padding-top: 87px;
      font-size: 31px;
      word-spacing: 2px;
      span {
        color: #e6ef82;
      }
    }
    .banner_p {
      width: 1240px;
      height: auto;
      margin: 0 auto;
      overflow: hidden;
      color: #fff;
      padding-top: 20px;
      font-size: 18px;
      word-spacing: 2px;
    }
  }
  .content-box {
    width: 100%;
    min-height: calc(100vh - 366px);
    height: auto;
    overflow: auto;
    // padding-bottom: 30px;
    -webkit-transition: left 0.3s ease-in-out;
    transition: left 0.3s ease-in-out;
    background: #fafafa;
    padding-bottom: 160px;
    // padding-bottom: 70px;
  }

  .content {
    width: 100%;
    min-height: calc(100% - 70px);
    height: auto;
    /* padding: 10px; */
    /* overflow-y: scroll; */
    box-sizing: border-box;
    margin: 0 auto;
  }
}
</style>
