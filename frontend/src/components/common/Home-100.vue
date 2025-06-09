<template>
    <div class="home">
        <v-head></v-head>
        <div class="content-box" ref="main" :style="{ height: contentHeight }">
            <div class="content" :style="{ minHeight: scrollerHeight }">
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
    .content-box {
        width: 100%;
        height: auto;
        overflow: auto;
        // padding-bottom: 30px;
        -webkit-transition: left 0.3s ease-in-out;
        transition: left 0.3s ease-in-out;
        background: #fafafa;
    }

    .content {
        width: 100%;
        height: auto;
        /* padding: 10px; */
        /* overflow-y: scroll; */
        box-sizing: border-box;
        margin: 0 auto;
    }
}
</style>
