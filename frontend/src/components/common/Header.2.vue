<template>
    <div class="header-content">
        <div class="header">
            <div class="logo">iPscDB</div>

            <el-menu
                :default-active="onRoutes"
                @click.native="removeKeepAlive"
                class="el-menu-demo"
                mode="horizontal"
                background-color="#24A461"
                text-color="#fff"
                active-text-color="#24A461"
                router
                @select="handleSelect"
            >
                <el-menu-item index="/homePage">
                    <span slot="title">Home</span>
                </el-menu-item>
                <el-submenu index="2">
                    <template slot="title">
                        <span style="color: #fff">Atlas</span>
                    </template>
                    <el-menu-item-group v-for="(items, index) in menuList" :key="index">
                        <template slot="title">
                            <span style="color: #24a461; font-size: 16px">{{ items.name.replace(/_/g, ' ') }}</span>
                        </template>
                        <el-menu-item v-for="(item, idx) in items.data" :key="idx">
                            <span slot="title" @click="jumpList(item, items.name)">{{ item.Tissue }}</span>
                        </el-menu-item>
                    </el-menu-item-group>
                </el-submenu>
                <el-submenu index="3">
                    <template slot="title">
                        <span style="color: #fff">Project Atlas</span>
                    </template>
                    <el-menu-item-group v-for="(items, index) in projectMenuList" :key="index">
                        <template slot="title">
                            <span style="color: #24a461; font-size: 16px">{{ items.species_name.replace(/_/g, ' ') }}</span>
                        </template>
                        <el-menu-item v-for="(item, idx) in items.project" :key="idx">
                            <span slot="title" @click="jumpList2(item.value, items.species_name, item.label)">{{ item.label }}</span>
                        </el-menu-item>
                    </el-menu-item-group>

                    <!-- <el-menu-item-group>
            <template slot="title">
            </template>
            <el-menu-item v-for="(item, idx) in projectMenuList" :key="idx">
              <span slot="title" @click="jumpList2(item.value)">{{ item.label }}</span>
            </el-menu-item>
          </el-menu-item-group> -->
                </el-submenu>
                <el-menu-item index="/search">
                    <span slot="title">Search</span>
                </el-menu-item>
                <el-submenu index="5">
                    <template slot="title">
                        <span style="color: #fff">Tools</span>
                    </template>
                    <el-menu-item-group>
                        <template slot="title">
                            <span class="sampleSpan" @click="jumpList3('sampleQC')">Sample QC</span>
                        </template>
                    </el-menu-item-group>
                </el-submenu>
            </el-menu>

            <!-- 头部菜单start -->
            <!-- <el-menu :default-active="onRoutes" @click.native="removeKeepAlive" class="el-menu-demo" mode="horizontal" background-color="#24A461"
        text-color="#fff" active-text-color="#24A461" router>
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
                <el-menu-item v-else :index="subItem.index" :key="subItem.index">{{ subItem.title }}
                </el-menu-item>
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
      </el-menu> -->
            <!-- 头部菜单end-->
        </div>
    </div>
</template>
<script>
import bus from '../common/bus'
import axios from '@/api/http.js'
import { atlas_tissue_cell_sample_count, project_lit_down } from '@/api/api'
export default {
    data() {
        return {
            menuList: [],
            projectMenuList: [],
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
                // {
                //   index: "/documentation",
                //   title: "Documentation",
                // },
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
        },
        handleSelect(key, keyPath) {
            console.log(key, keyPath)
        },
        jumpList(item, name) {
            // 跳转列表页
            this.$router.push({
                path: '/searchResult',
                query: {
                    Tissue: item.Tissue,
                    cell_count: item.cell_count,
                    name: name,
                    sample_count: item.sample_count
                }
            })
            if (this.$route.path == '/searchResult') {
                location.reload()
            }
        },
        jumpList2(item, name, project_id) {
            // 跳转列表页
            this.$router.push({
                path: '/projectResult',
                query: {
                    lit_id: item,
                    species_name: name,
                    project_id: project_id
                }
            })
            if (this.$route.path == '/projectResult') {
                location.reload()
            }
        },
        jumpList3(item) {
            // 跳转列表页
            this.$router.push({
                path: `/${item}`
            })
        }
    },
    mounted() {
        atlas_tissue_cell_sample_count().then((res) => {
            if (res.code == 200) {
                if (res.data.length > 0) {
                    this.menuList = res.data
                }
            }
        })
        project_lit_down().then((res) => {
            if (res.code == 200) {
                if (res.data.length > 0) {
                    this.projectMenuList = res.data
                }
            }
        })
    }
}
</script>
<style lang="scss" scoped>
.header-content {
    width: 100%;
    height: 60px;
    box-shadow: 0px 7px 7px -7px rgba(0, 0, 0, 0.09);
    // margin-bottom: 5px;
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
            // opacity: 0.8;
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
    i {
        color: #fff;
    }
}
.el-menu--horizontal > .el-submenu .el-submenu__title:hover {
}
.el-menu--horizontal .el-menu--popup-bottom-start {
    max-width: 440px;
    background: #fff !important;
    .el-menu-item-group {
        overflow: hidden;
        .el-menu-item-group__title {
            padding-left: 20px !important;
        }
        ul {
            overflow: hidden;
            padding: 0 10px;
            box-sizing: border-box;
        }
        .el-menu-item {
            color: #999 !important;
            background: #fff !important;
            float: left;
        }
    }
}

.el-menu--horizontal .el-menu--popup-bottom-start .el-menu-item:hover {
    color: #0a9daa !important;
    text-decoration: underline;
}
// }
.sampleSpan {
    color: #999;
    font-size: 14px;
    cursor: pointer;
}
.sampleSpan:hover {
    color: #24a461;
}
</style>
