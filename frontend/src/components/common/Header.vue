<template>
    <div class="header-content" :style="{ 'margin-bottom': marginBottom }">
        <div class="header">
            <el-menu :default-active="onRoutes" @click.native="removeKeepAlive" class="el-menu-demo" mode="horizontal" background-color="#fff"
                text-color="#666" active-text-color="#24A461" router @select="handleSelect">
                <el-menu-item index="/homePage">
                    <span slot="title">Home</span>
                </el-menu-item>
                <el-menu-item index="/browse">
                    <span slot="title">Browse</span>
                </el-menu-item>
                <!-- 新增 -->
                <el-menu-item index="/projectAtlas" :class="{ searchIsActive: projectIsActive }">
                    <span slot="title">Atlas</span>
                </el-menu-item>
                <!-- 新增暂无数据 -->
                <el-menu-item index="/marker">
                    <span slot="title">Marker</span>
                </el-menu-item>
                <el-menu-item index="/searchForm">
                    <span slot="title">Search</span>
                </el-menu-item>
                <el-submenu index="Analysis" :class="{ AnalysisIsActive: activeAnalysis() }">
                    <template slot="title">Pipeline</template>
                    <!-- <template slot="title">Data Analysis</template> -->
                    <el-menu-item index="/browseResult">Browse results</el-menu-item>
                    <el-submenu index="1-2">
                        <template slot="title">Start new jobs</template>
                        <el-menu-item index="/CellRanger">Start with fastq files</el-menu-item>
                        <el-menu-item index="/SampleSampleQC">Start with cellranger files</el-menu-item>
                    </el-submenu>

                    <!-- <el-menu-item index="/CellRanger">Start fastq</el-menu-item> -->
                    <!-- <el-menu-item index="/SampleSampleQC">Start cellranger result</el-menu-item> -->

                    <!-- <el-menu-item index="/analysisFromCellranger">Analysis from cellranger</el-menu-item>
                    <el-menu-item index="/analysisFromSampleQC">Analysis from Sample QC</el-menu-item> -->
                </el-submenu>
                <!-- <el-menu-item index="/Integration">
                    <span slot="title">Search</span>
                </el-menu-item> -->
                <!-- <el-menu-item index="/tools" :class="{ sampleQCIsActive: sampleQCIsActive }">
                    <span slot="title">Tools</span>
                </el-menu-item> -->
                <el-submenu index="2" :class="{ sampleQCIsActive: activeTools() }">
                    <template slot="title">Tools</template>
                    <el-menu-item index="/geneExpression">Cross-species gene expression</el-menu-item>
                    <!-- <el-menu-item index="/cellCellInteractions">Cell-Cell interaction</el-menu-item> -->
                    <el-menu-item index="/monocle">Developmental trajectory</el-menu-item>
                    <el-menu-item index="/eSCP">electronic Single-Cell Pictograph</el-menu-item>
                    <el-menu-item index="/cellid">Plant CelliD</el-menu-item>
                    <!-- <el-menu-item index="/mtsc">Plant CtAnnotation</el-menu-item> -->
                    <el-menu-item index="/cellblast">Plant Cell-Blast</el-menu-item>
                    <!-- <el-menu-item index="/cellAnnotation">Cross-species cell annotaion</el-menu-item> -->
                </el-submenu>
                <!-- 新增暂无数据 -->
                <el-menu-item index="/documentation" :class="{ sampleQCIsActive: documentation() }">
                    <span slot="title">Documentation</span>
                </el-menu-item>
                <!--  -->

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
                <!-- <el-menu-item index="/projectAtlas" :class="{ projectIsActive: projectIsActive }">
                    <span slot="title">Project Atlas</span>
                </el-menu-item> -->
                <!-- <el-menu-item index="/sampleQCNew">
                    <span slot="title">Sample QC</span>
                </el-menu-item> -->
                <!-- <el-menu-item index="/Integration">
                    <span slot="title">Integration</span>
                </el-menu-item>
                <el-menu-item index="/cellIdentification" :class="{ cellIdentIsActive: cellIdentIsActive }">
                    <span slot="title">Cell Identification</span>
                </el-menu-item> -->

                <!-- <el-menu-item index="/download">
                    <span slot="title">Download</span>
                </el-menu-item>
                <el-menu-item index="/Contact">
                    <span slot="title">Contact</span>
                </el-menu-item> -->
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
            <div class="header-right">
                <el-select v-model="searchValue" placeholder="search" style="width: 100px; height: 36px; margin-right: 10px">
                    <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                </el-select>
                <el-input placeholder="Enter search keywords" style="width: 244px; height: 36px" suffix-icon="el-icon-search" v-model="inputValue"
                    @keydown.native.enter="goSearch" />
                <span class="header-right-search" @click="goSearch"></span>
            </div>
        </div>
    </div>
</template>
<script>
import bus from '../common/bus'
import axios from '@/api/http.js'
import { atlas_tissue_cell_sample_count, project_lit_down, menu_select_list } from '@/api/api'
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
            AnalysisIsActive: false,
            marginBottom: 0,
            options: [],
            searchValue: null,
            inputValue: null
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
                this.AnalysisIsActive = false
                this.cellIdentIsActive = false
                this.sampleQCIsActive = false
            } else if (this.$route.path == '/projectResult') {
                this.projectIsActive = true
                this.cellIdentIsActive = false
                this.AnalysisIsActive = false
                this.searchIsActive = false
                this.sampleQCIsActive = false
            } else if (this.$route.path == '/cellIdentificationScope') {
                this.projectIsActive = false
                this.AnalysisIsActive = false
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
                this.AnalysisIsActive = false
                this.cellIdentIsActive = false
                this.searchIsActive = false
            } else if (
                this.$route.path == '/browseResult' ||
                this.$route.path == '/CellRanger' ||
                this.$route.path == '/SampleSampleQC' ||
                this.$route.path == '/analysisFromCellranger' ||
                this.$route.path == '/analysisFromSampleQC'
            ) {
                this.AnalysisIsActive = true
                this.sampleQCIsActive = false
                this.projectIsActive = false
                this.cellIdentIsActive = false
                this.searchIsActive = false
            } else {
                this.AnalysisIsActive = false
                this.cellIdentIsActive = false
                this.projectIsActive = false
                this.searchIsActive = false
                this.sampleQCIsActive = false
            }
            sessionStorage.removeItem('isActive')
            sessionStorage.setItem(
                'isActive',
                JSON.stringify({
                    AnalysisIsActive: this.AnalysisIsActive,
                    searchIsActive: this.searchIsActive,
                    projectIsActive: this.projectIsActive,
                    cellIdentIsActive: this.cellIdentIsActive,
                    sampleQCIsActive: this.sampleQCIsActive
                })
            )
            return this.$route.path
        }
    },
    created() {
        this.getOptions()
    },
    methods: {
        goSearch() {
            let searchValue = this.searchValue
            let inputValue = this.inputValue
            this.$router.push({
                path: 'searchTable',
                query: {
                    searchValue,
                    inputValue
                }
            })
        },
        getOptions() {
            menu_select_list().then((res) => {
                if (res.code == 200) {
                    this.options = res.data.map((item, index) => {
                        return {
                            value: index + 1,
                            label: item
                        }
                    })

                    this.searchValue = 1
                    // this.searchValue = res.data && res.data.length > 0 ? res.data[0] : ''
                }
            })
        },
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
        activeTools() {
            let path = this.$route.path
            let activeData = ['/cellAnnotation', '/cellCellInteractions', '/monocle', '/eSCP', '/cellid', '/cellblast', '/mtsc', '/geneExpression']
            return activeData.includes(path)
        },
        activeAnalysis() {
            let path = this.$route.path
            let activeData = ['/analysisFromCellranger', '/analysisFromSampleQC', '/browseResult', '/CellRanger', '/SampleSampleQC']
            return activeData.includes(path)
        },
        documentation() {
            let path = this.$route.path
            let activeData = ['/documentation', '/documentation2', '/documentation3', '/documentation4']
            return activeData.includes(path)
        },
        handleSelect(key, keyPath) {
            if ((keyPath[0] == 'Analysis') && (key == this.$route.path)) {
                this.$router.push({
                    path: key
                })
                this.$router.go(0)

            }
            if (keyPath[0] == '/homePage') {
                this.marginBottom = 0
            } else {
                this.marginBottom = '6px'
            }
            if (keyPath[0] == '/searchResult') {
                this.searchIsActive = true
                this.projectIsActive = false
                this.AnalysisIsActive = false
                this.cellIdentIsActive = false
                this.sampleQCIsActive = false
            } else if (keyPath[0] == '/projectResult') {
                this.projectIsActive = true
                this.cellIdentIsActive = false
                this.AnalysisIsActive = false
                this.searchIsActive = false
                this.sampleQCIsActive = false
            } else if (keyPath[0] == '/cellIdentificationScope') {
                this.projectIsActive = false
                this.AnalysisIsActive = false
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
                this.AnalysisIsActive = false
                this.cellIdentIsActive = false
                this.searchIsActive = false
            } else if (
                keyPath[0] == '/browseResult' ||
                keyPath[0] == '/CellRanger' ||
                keyPath[0] == '/SampleSampleQC' ||
                keyPath[0] == '/analysisFromCellranger' ||
                keyPath[0] == '/analysisFromSampleQC'
            ) {
                this.AnalysisIsActive = true
                this.sampleQCIsActive = false
                this.projectIsActive = false
                this.cellIdentIsActive = false
                this.searchIsActive = false
            } else {
                this.AnalysisIsActive = false
                this.projectIsActive = false
                this.cellIdentIsActive = false
                this.searchIsActive = false
                this.sampleQCIsActive = false
            }
            sessionStorage.removeItem('isActive')
            sessionStorage.setItem(
                'isActive',
                JSON.stringify({
                    AnalysisIsActive: this.AnalysisIsActive,
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
            this.AnalysisIsActive = JSON.parse(sessionStorage.getItem('isActive')).AnalysisIsActive
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
  background-color: #fff !important;

  .header {
    .header-right {
      position: relative;

      .header-right-search {
        position: absolute;
        right: 10px;
        top: 6px;
        display: inline-block;
        // background: #24A461;
        width: 30px;
        height: 20px;
        cursor: pointer;
      }
    }

    background-color: #fff !important;
    /* position: fixed;
  top: 0; */
    box-sizing: border-box;
    width: 1240px;
    // padding-left: 50px;
    // background: url(~@/assets/img/logo2.png) no-repeat 0 50%;
    height: 60px;
    font-size: 20px;
    color: #666;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;

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
      background: #fff !important;
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
    // color: #fff;
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
  // color: #0a9daa !important;
  color: #24a461 !important;
  // text-decoration: underline;
}

.el-menu--horizontal .el-menu--popup-bottom-start .QCItem:hover {
  // color: #0a9daa !important;
  color: #24a461 !important;
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
.home .header-content .header .el-menu--horizontal .AnalysisIsActive {
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
