<template>
    <div class="header-content" :style="{ 'margin-bottom': marginBottom }">
        <div class="header">
            <div class="logo">iPscDB</div>

            <el-menu
                :default-active="onRoutes"
                @click.native="removeKeepAlive"
                class="el-menu-demo"
                mode="horizontal"
                background-color="#f6f9f9"
                text-color="#666"
                active-text-color="#24A461"
                router
                @select="handleSelect"
            >
                <el-menu-item index="/homePage">
                    <span slot="title">Home</span>
                </el-menu-item>
                <el-menu-item index="/browse">
                    <span slot="title">Browse</span>
                </el-menu-item>

                <!-- <el-menu-item index="/atlas" :class="{ 'searchIsActive': searchIsActive }">
          <span slot="title">Atlas</span>
        </el-menu-item> -->
                <!-- <el-submenu index="/searchResult" :class="{ 'searchIsActive': searchIsActive }">
          <template slot="title">
            <span style="color:#fff;">Atlas</span>
          </template>
          <el-menu-item-group v-for="(items, index) in menuList" :key="index">
            <template slot="title">
              <span style="color:#24A461;font-size:16px;">{{items.label.replace(/_/g, ' ')}}</span>
            </template>
            <el-menu-item v-for="(item, idx) in items.data" :key="idx" @click="jumpList(item, items.name)">
              <span slot="title">{{ item.Tissue }}</span>
            </el-menu-item>
          </el-menu-item-group>
        </el-submenu> -->
                <!-- <el-submenu index="/projectResult" :class="{ 'projectIsActive': projectIsActive }">
          <template slot="title">
            <span style="color:#fff;">Project Atlas</span>
          </template>
          <el-menu-item-group v-for="(items, index) in projectMenuList" :key="index">
            <template slot="title">
              <span style="color:#24A461;font-size:16px;">{{items.label.replace(/_/g, ' ')}}</span>
            </template>
            <el-menu-item v-for="(item, idx) in items.project" :key="idx" @click="jumpList2(item,items.species_name)">
              <span slot="title">{{ item.label }}</span>
            </el-menu-item>
          </el-menu-item-group>

        </el-submenu> -->
                <el-menu-item index="/projectAtlas" :class="{ projectIsActive: projectIsActive }">
                    <span slot="title">Project Atlas</span>
                </el-menu-item>
                <el-menu-item index="/sampleQCNew">
                    <!-- <el-menu-item index="/sampleQC"> -->
                    <span slot="title">Sample QC</span>
                </el-menu-item>
                <el-menu-item index="/Integration">
                    <span slot="title">Integration</span>
                </el-menu-item>
                <el-menu-item index="/cellIdentification" :class="{ cellIdentIsActive: cellIdentIsActive }">
                    <span slot="title">Cell Identification</span>
                </el-menu-item>

                <el-menu-item index="/tools" :class="{ sampleQCIsActive: sampleQCIsActive }">
                    <span slot="title">Tools</span>
                </el-menu-item>
                <el-menu-item index="/download">
                    <span slot="title">Download</span>
                </el-menu-item>
                <el-menu-item index="/Contact">
                    <span slot="title">Contact</span>
                </el-menu-item>
                <!-- <el-submenu index="/geneExpression" :class="{ 'sampleQCIsActive': sampleQCIsActive }">
          <template slot="title">
            <span style="color:#fff;">Tools</span>
          </template> -->
                <!-- <el-menu-item-group>
            <template slot="title">
              <el-menu-item class="QCItem" @click="jumpList3('sampleQC')">
                <span class="sampleSpan">Sample QC</span>
              </el-menu-item>
            </template>
          </el-menu-item-group> -->
                <!-- <el-menu-item-group>
            <template slot="title">
              <el-menu-item class="QCItem" @click="jumpList3('geneExpression')">
                <span class="sampleSpan" @click="jumpList3('geneExpression')">GeneExpression</span>
              </el-menu-item>
            </template>
          </el-menu-item-group>
          <el-menu-item-group>
            <template slot="title">
              <el-menu-item class="QCItem" @click="jumpList3('tissueStructure')">
                <span class="sampleSpan" @click="jumpList3('tissueStructure')">Tissue structure</span>
              </el-menu-item>
            </template>
          </el-menu-item-group> -->
                <!-- <el-menu-item-group>
            <template slot="title">
              <el-menu-item class="QCItem" @click="jumpList3('blast')">
                <span class="sampleSpan" @click="jumpList3('blast')">Blast</span>
              </el-menu-item>
            </template>
          </el-menu-item-group> -->
                <!-- <el-menu-item-group>
            <template slot="title">
              <el-menu-item class="QCItem" @click="jumpList3('eSCP')">
                <span class="sampleSpan" @click="jumpList3('eSCP')">eSCP</span>
              </el-menu-item>
            </template>
          </el-menu-item-group>
          <el-menu-item-group>
            <template slot="title">
              <el-menu-item class="QCItem" @click="jumpList3('monocle')">
                <span class="sampleSpan" @click="jumpList3('monocle')">Monocle</span>
              </el-menu-item>
            </template>
          </el-menu-item-group>
        </el-submenu> -->
            </el-menu>
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
            ],
            searchIsActive: false,
            projectIsActive: false,
            cellIdentIsActive: false,
            sampleQCIsActive: false,
            marginBottom: 0
        }
    },
    computed: {
        onRoutes() {
            if (this.$route.path == '/homePage') {
                this.marginBottom = 0
            } else {
                this.marginBottom = '6px'
            }
            if (this.$route.path == '/searchResult') {
                this.searchIsActive = true
                this.projectIsActive = false
                this.cellIdentIsActive = false
                this.sampleQCIsActive = false
            } else if (this.$route.path == '/projectResult') {
                this.projectIsActive = true
                this.cellIdentIsActive = false
                this.searchIsActive = false
                this.sampleQCIsActive = false
            } else if (this.$route.path == '/cellIdentificationScope') {
                this.projectIsActive = false
                this.cellIdentIsActive = true
                this.searchIsActive = false
                this.sampleQCIsActive = false
            } else if (
                this.$route.path == '/geneExpression' ||
                this.$route.path == '/blast' ||
                this.$route.path == '/tissueStructure' ||
                this.$route.path == '/eSCP' ||
                this.$route.path == '/monocle' ||
                this.$route.path == '/cellCellInteractions'
            ) {
                this.sampleQCIsActive = true
                this.projectIsActive = false
                this.cellIdentIsActive = false
                this.searchIsActive = false
            } else {
                this.cellIdentIsActive = false
                this.projectIsActive = false
                this.searchIsActive = false
                this.sampleQCIsActive = false
            }
            sessionStorage.removeItem('isActive')
            sessionStorage.setItem(
                'isActive',
                JSON.stringify({
                    searchIsActive: this.searchIsActive,
                    projectIsActive: this.projectIsActive,
                    cellIdentIsActive: this.cellIdentIsActive,
                    sampleQCIsActive: this.sampleQCIsActive
                })
            )
            return this.$route.path
        }
    },
    methods: {
        removeKeepAlive() {
            if (this.onRoutes == '/homePage') {
                this.marginBottom = 0
            } else {
                this.marginBottom = '6px'
            }
            if (this.onRoutes == '/search') {
                this.$route.meta.keepAlive = false
            }
        },
        handleSelect(key, keyPath) {
            if (keyPath[0] == '/homePage') {
                this.marginBottom = 0
            } else {
                this.marginBottom = '6px'
            }
            if (keyPath[0] == '/searchResult') {
                this.searchIsActive = true
                this.projectIsActive = false
                this.cellIdentIsActive = false
                this.sampleQCIsActive = false
            } else if (keyPath[0] == '/projectResult') {
                this.projectIsActive = true
                this.cellIdentIsActive = false
                this.searchIsActive = false
                this.sampleQCIsActive = false
            } else if (keyPath[0] == '/cellIdentificationScope') {
                this.projectIsActive = false
                this.cellIdentIsActive = true
                this.searchIsActive = false
                this.sampleQCIsActive = false
            } else if (
                keyPath[0] == '/geneExpression' ||
                keyPath[0] == '/blast' ||
                keyPath[0] == '/tissueStructure' ||
                keyPath[0] == '/eSCP' ||
                keyPath[0] == '/monocle' ||
                keyPath[0] == '/cellCellInteractions'
            ) {
                this.sampleQCIsActive = true
                this.projectIsActive = false
                this.cellIdentIsActive = false
                this.searchIsActive = false
            } else {
                this.projectIsActive = false
                this.cellIdentIsActive = false
                this.searchIsActive = false
                this.sampleQCIsActive = false
            }
            sessionStorage.removeItem('isActive')
            sessionStorage.setItem(
                'isActive',
                JSON.stringify({
                    searchIsActive: this.searchIsActive,
                    projectIsActive: this.projectIsActive,
                    cellIdentIsActive: this.cellIdentIsActive,
                    sampleQCIsActive: this.sampleQCIsActive
                })
            )
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
        jumpList2(item, name) {
            // 跳转列表页
            this.$router.push({
                path: '/projectResult',
                query: {
                    lit_id: item.value,
                    species_name: name,
                    project_id: item.label,
                    sample_count: item.sample_count,
                    cell_count: item.cell_count
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
        if (sessionStorage.getItem('isActive')) {
            this.projectIsActive = JSON.parse(sessionStorage.getItem('isActive')).projectIsActive
            this.cellIdentIsActive = JSON.parse(sessionStorage.getItem('isActive')).cellIdentIsActive
            this.searchIsActive = JSON.parse(sessionStorage.getItem('isActive')).searchIsActive
            this.sampleQCIsActive = JSON.parse(sessionStorage.getItem('isActive')).sampleQCIsActive
        }
        // atlas_tissue_cell_sample_count().then(res => {
        //   if (res.code == 200) {
        //     if (res.data.length > 0) {
        //       this.menuList = res.data
        //     }
        //   }
        // });
        // project_lit_down().then(res => {
        //   if (res.code == 200) {
        //     if (res.data.length > 0) {
        //       this.projectMenuList = res.data
        //     }
        //   }
        // });
    }
}
</script>
<style lang="scss" scoped>
.header-content {
    width: 100%;
    height: 60px;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.07);
    // margin-bottom: 6px;
    background-color: #f6f9f9 !important;
    .header {
        background-color: #f6f9f9 !important;
        /* position: fixed;
  top: 0; */
        box-sizing: border-box;
        width: 1240px;
        padding-left: 50px;
        background: url(~@/assets/img/logo2.png) no-repeat 0 50%;
        height: 60px;
        font-size: 20px;
        color: #666;
        margin: 0 auto;
        /* box-shadow: 0 2px 10px 0 rgba(0, 0, 0, 0.1); */
        .logo {
            float: left;
            width: 124px;
            line-height: 60px;
            font-weight: bold;
            color: #24a461;
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
            padding: 0 20px !important;
        }
        .el-menu--horizontal > .el-menu-item:hover {
            // opacity: 0.8;
            // background: rgba(0, 0, 0, 0.2) !important;
            background: none !important;
            color: #24a461 !important;
            border-bottom-color: #24a461 !important;
        }
        .el-menu--horizontal > .el-submenu {
            font-size: 17px;
            height: 60px;
            line-height: 60px;
        }

        .el-menu--horizontal > .is-active {
            // opacity: 0.8;
            // background: rgba(0, 0, 0, 0.2) !important;
            background: #f6f9f9 !important;
            color: #24a461 !important;
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
            color: #666 !important;
            background: #fff !important;
            float: left;
        }
    }
}

.el-menu--horizontal .el-menu--popup-bottom-start .el-menu-item:hover {
    color: #0a9daa !important;
    text-decoration: underline;
}
.el-menu--horizontal .el-menu--popup-bottom-start .QCItem:hover {
    color: #0a9daa !important;
    text-decoration: none;
}
// }
.sampleSpan {
    color: #666;
    font-size: 14px;
    cursor: pointer;
}
.sampleSpan:hover {
    color: #24a461;
}

.home .header-content .header .el-menu--horizontal .searchIsActive {
    // background: none !important;
    // div {
    // background: rgba(0, 0, 0, 0.2) !important;
    color: #666 !important;
    border-bottom-color: #24a461 !important;
    // }
}
.home .header-content .header .el-menu--horizontal .projectIsActive {
    // background: none !important;
    // div {
    // opacity: 0.8;
    // background: rgba(0, 0, 0, 0.2) !important;
    color: #666 !important;
    border-bottom-color: #24a461 !important;
    // }
}
.home .header-content .header .el-menu--horizontal .cellIdentIsActive {
    // background: none !important;
    // div {
    // opacity: 0.8;
    // background: rgba(0, 0, 0, 0.2) !important;
    color: #666 !important;
    border-bottom-color: #24a461 !important;
    // }
}
.home .header-content .header .el-menu--horizontal .sampleQCIsActive {
    // background: none !important;
    // div {
    // background: rgba(0, 0, 0, 0.2) !important;
    color: #666 !important;
    border-bottom-color: #24a461 !important;
    // }
}
</style>
