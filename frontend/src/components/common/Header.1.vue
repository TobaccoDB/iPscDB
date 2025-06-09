<template>
    <div class="header-content">
        <div class="header">
            <div class="logo">iPscDB</div>
            <!-- 头部菜单start -->
            <el-menu :default-active="onRoutes" @click.native="removeKeepAlive" class="el-menu-demo" mode="horizontal" background-color="#24A461" text-color="#fff" active-text-color="#24A461" router>
                <template v-for="item in items">
                    <template v-if="item.subs">
                        <el-submenu :index="item.index" :key="item.index">
                            <template slot="title">
                                <span slot="title">{{ item.title }}</span>
                            </template>
                            <template v-for="subItem in item.subs">
                                <el-submenu v-if="subItem.subs" :index="subItem.index" :key="subItem.index" popper-class="select-down">
                                    <template slot="title">{{ subItem.title }}</template>
                                </el-submenu>
                                <el-menu-item v-else :index="subItem.index" :key="subItem.index">{{ subItem.title }} </el-menu-item>
                            </template>
                        </el-submenu>
                    </template>
                    <template v-else>
                        <el-menu-item :index="item.index" :key="item.index">
                            <i :class="item.icon"></i>
                            <span slot="title">{{ item.title }}</span>
                        </el-menu-item>
                    </template>
                </template>
            </el-menu>
            <!-- 头部菜单end-->
        </div>
    </div>
</template>
<script>
import bus from '../common/bus'
import axios from '@/api/http.js'
export default {
    data() {
        return {
            items: [
                {
                    index: '/homePage',
                    title: 'Home'
                },
                {
                    index: '/browse',
                    title: 'Browse'
                },
                {
                    index: '/search',
                    title: 'Search'
                },
                {
                    index: '/tools',
                    title: 'Tools',
                    subs: [
                        { index: '/scsa', title: 'SCSA' },
                        { index: '/singleR', title: 'SingleR' },
                        // { index: "/CMPredictor", title: "CMPredictor" },
                        { index: '/blast', title: 'Blast' }
                    ]
                },
                {
                    index: '/documentation',
                    title: 'Documentation'
                },
                {
                    index: '/submit',
                    title: 'Submit'
                },
                {
                    index: '/download',
                    title: 'Download'
                }
            ]
        }
    },
    computed: {
        onRoutes() {
            return this.$route.path
        }
    },
    methods: {
        removeKeepAlive() {
            if (this.onRoutes == '/search') {
                this.$route.meta.keepAlive = false
            }
        }
    },
    mounted() {}
}
</script>
<style lang="scss" scoped>
.header-content {
    width: 100%;
    height: 60px;
    box-shadow: 0px 7px 7px -7px rgba(0, 0, 0, 0.09);
    margin-bottom: 5px;
    background-color: #24a461 !important;
    .header {
        background-color: #24a461 !important;
        /* position: fixed;
  top: 0; */
        box-sizing: border-box;
        width: 1240px;
        padding-left: 50px;
        background: url(~@/assets/img/logo.png) no-repeat 0 50%;
        height: 60px;
        font-size: 20px;
        color: #666;
        margin: 0 auto;
        /* box-shadow: 0 2px 10px 0 rgba(0, 0, 0, 0.1); */
        .logo {
            float: left;
            width: 240px;
            line-height: 60px;
            font-weight: bold;
            color: #fff;
            font-size: 30px;
        }
        .el-dropdown-menu__item {
            text-align: center;
        }
        .el-menu-demo {
            float: left;
            height: 60px;
            border: none;
        }
        .el-menu--horizontal > .el-menu-item {
            font-size: 16px;
            height: 60px;
            line-height: 60px;
        }
        .el-menu--horizontal > .el-menu-item:hover {
            opacity: 0.8;
            background: rgba(0, 0, 0, 0.2) !important;
            color: #fff !important;
            border-bottom-color: #24a461 !important;
        }
        .el-menu--horizontal > .el-submenu {
            font-size: 17px;
            height: 60px;
            line-height: 60px;
        }

        .el-menu--horizontal > .is-active {
            opacity: 0.8;
            background: rgba(0, 0, 0, 0.2) !important;
            color: #fff !important;
            border-bottom-color: #24a461 !important;
        }
    }
}
</style>
<style lang="scss">
// .header {
.el-menu--horizontal > .el-submenu .el-submenu__title {
    font-size: 17px !important;
    height: 60px !important;
    line-height: 60px !important;
}
.el-menu--horizontal > .el-submenu .el-submenu__title:hover {
    // background: #fff !important;
    // color: #24A461 !important;
    // border-bottom-color: #24A461 !important;
    opacity: 0.8;
    background: rgba(0, 0, 0, 0.2) !important;
    color: #fff !important;
    border-bottom-color: #24a461 !important;
}
.el-menu--horizontal .el-menu--popup-bottom-start .el-menu-item {
    background: #24a461 !important;
}

.el-menu--horizontal .el-menu--popup-bottom-start .el-menu-item:hover {
    // background: #fff !important;
    // color: #24A461 !important;
    opacity: 0.8;
    background: rgba(0, 0, 0, 0.2) !important;
    color: #fff !important;
    border-bottom-color: #24a461 !important;
}
// }
</style>
