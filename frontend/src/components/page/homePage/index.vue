<template>
    <div class="homepage">
        <!-- 统计 -->
        <!-- <div class="homepage_statistics">
            <div class="statistics_content">
                <div class="homepage_statistics_left">
                    <h3>Atlas</h3>
                    <div class="sta_left_content">
                        <el-row :gutter="20" style="width: 100%; height: auto; overflow: hidden">
                            <el-col :span="8" v-for="(item, index) in listItem" :key="index">
                                <div class="grid-content">
                                    <i class="title">{{ item.label }}</i>
                                    <ul class="ul-content">
                                        <li><img :src="item.species_whole_plant" @click="jumpProjectResult(item, index)" /></li>
                                        <li style="width: 30%">
                                            <img
                                                v-if="tissue.Tissue != 'WholePlant'"
                                                :class="{ active: cur[index] == i }"
                                                :style="tissue.is_show == '1' ? 'cursor: pointer;' : 'filter: grayscale(100%) opacity(40%);'"
                                                :src="tissue.tissue_head_link"
                                                v-for="(tissue, i) in item.data"
                                                :key="i"
                                                @click="imgClick(item.name, tissue, index, i)"
                                            />
                                        </li>
                                    </ul>
                                </div>
                            </el-col>
                        </el-row>
                    </div>
                </div>
                <div class="homepage_statistics_right">
                    <h3>Statistics</h3>
                    <div class="sta_right_content">
                        <dl v-for="(item, index) in AtlasListRight" :key="index">
                            <dt></dt>
                            <dd>{{ item.value }}</dd>
                            <dd>{{ item.name }}</dd>
                        </dl>
                    </div>
                    <h3>Update log</h3>
                    <div class="sta_right_content" style="height: 178px">
                        <ul>
                            <li class="logLi" v-for="(item, index) in logsList" @click="goToUpdateLog(item.id)" :key="index">
                                <span>{{ item.title }}</span>
                                <span>{{ item.updated_at }}</span>
                            </li>
                        </ul>
                    </div>
                    <h3>Citation</h3>
                    <div class="sta_right_content" style="height: 178px">
                        <ul>
                            <li style="text-align: justify">iPscDB v1.0: a Integrated Plant Single-Cell Database.</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div> -->
        <!-- 幻灯片 -->
        <div class="home_page_banner">
            <div class="home_page_banner-left">
                <span @click="back" v-show="activeIndex > 0"></span>
            </div>
            <div class="home_page_banner-right">
                <span @click="next" v-show="activeIndex < listItem.length - 6"></span>
            </div>
            <div class="home_page_banner-main">
                <!-- 真正的幻灯片区域 -->
                <div class="home_page_banner-main-centent">
                    <div class="home_page_banner-main-centent-main" ref="bannerMain" :style="{ left: -activeIndex * 208 + 'px' }">
                        <div class="home_page_banner-main-centent-item" v-for="(item, index) in listItem" :key="index" @mouseover="mouseleaveItem(index)" @mouseout="mouseoutItem">
                            <div class="home_page_banner-main-centent-item-public home_page_banner-main-centent-item-top">
                                <div class="grid-content grid-content-item">
                                    <i class="title">{{ item.label }}</i>
                                    <div class="grid-content-item-image">
                                        <img :src="item.species_whole_plant" @click="jumpProjectResult(item, index)" />
                                    </div>
                                </div>
                            </div>
                            <div class="home_page_banner-main-centent-item-public home_page_banner-main-centent-item-bottom">
                                <div class="grid-content grid-content-bottom">
                                    <i class="title">{{ item.label }}</i>
                                    <ul class="ul-content">
                                        <li><img :src="item.species_whole_plant" @click="jumpProjectResult(item, index)" /></li>
                                        <li style="width: 40%">
                                            <!-- <img
                                                v-if="tissue.Tissue != 'WholePlant'"
                                                :class="{ active: cur[index] == i }"
                                                :style="tissue.is_show == '1' ? 'cursor: pointer;' : 'filter: grayscale(100%) opacity(40%);'"
                                                :src="tissue.tissue_head_link"
                                                v-for="(tissue, i) in item.data"
                                                :key="i"
                                                @click="imgClick(item.name, tissue, index, i, item)"
                                            /> -->
                                            <div class="ul-content-li">
                                                <img
                                                    v-if="tissue.Tissue != 'WholePlant' && i < 5"
                                                    :class="{ active: cur[index] == i }"
                                                    :style="tissue.is_show == '1' ? 'cursor: pointer;' : 'filter: grayscale(100%) opacity(40%);'"
                                                    :src="tissue.tissue_head_link"
                                                    v-for="(tissue, i) in item.data"
                                                    :key="i"
                                                    @click="imgClick(item.name, tissue, index, i, item)"
                                                />
                                            </div>
                                            <div class="ul-content-li">
                                                <img
                                                    v-if="tissue.Tissue != 'WholePlant' && i >= 5"
                                                    :class="{ active: cur[index] == i }"
                                                    :style="tissue.is_show == '1' ? 'cursor: pointer;' : 'filter: grayscale(100%) opacity(40%);'"
                                                    :src="tissue.tissue_head_link"
                                                    v-for="(tissue, i) in item.data"
                                                    :key="i"
                                                    @click="imgClick(item.name, tissue, index, i, item)"
                                                />
                                            </div>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- 指针 -->
                <div class="home_page_pointer">
                    <span class="home_page_pointer-index" :class="pointerActive == item - 1 ? 'home_page_pointer-indexActive' : ''" v-for="item in 6" :key="item"></span>
                </div>
            </div>
        </div>
        <!-- 切换 -->
        <div class="home_page_switch">
            <!-- 左侧 -->
            <div class="home_page_switch_left">
                <el-tabs v-model="tabActive">
                    <el-tab-pane :label="item.label" :name="item.value" v-for="(item, index) in tabsList" :key="index">
                        <div class="home_page_switch_left-content" :class="`home_page_image_${index}`" v-if="item.image">
                            <img :src="item.image" />
                        </div>
                    </el-tab-pane>
                </el-tabs>
            </div>
            <!-- 右侧 -->
            <div class="home_page_switch_right">
                <div class="home_page_switch_right-title">Statistics</div>
                <div class="homepage_statistics_right">
                    <div class="sta_right_content sta_right_content-main">
                        <dl v-for="(item, index) in AtlasListRight" :key="index">
                            <dt></dt>
                            <dd>{{ item.value }}</dd>
                            <dd>{{ item.name }}</dd>
                        </dl>
                    </div>
                </div>
            </div>
        </div>
        <div class="footer-top">
            <div class="footer-top-left">
                <div class="footer-top-left-name">Update log</div>
                <!-- <p style="color: #fff; margin-bottom: 5px;"> 2024-10-28                </p> -->
                <div class="footer-top-left-center">
                    <span>iPscDB v1.2 Pipeline Updataed</span>
                    <span>2025-03-22</span>
                </div>
                <div class="footer-top-left-center">
                    <span>iPscDB v1.1 Updated</span>
                    <span>2024-10-28</span>
                </div>
                <div class="footer-top-left-center">
                    <span>iPscDB v1.0 released</span>
                    <span>2023-07-01</span>
                    <span>iPscDB v1.0 Beta Test</span>
                    <span>2022-12-08</span>
                </div>
                <div class="footer-top-left-center">
                    <span>iPscDB v1.0 Beta Online</span>
                    <span>2023-01-14</span>
                    <span>iPscDB v1.0 Beta Develop</span>
                    <span>2022-11-09</span>
                </div>
            </div>
            <div class="footer-top-right">
                <div class="footer-top-right-name">Citation</div>
                <div class="footer-top-right-center">iPscDB: a versatile database of multiple species cell atlases at the single-cell level in plants.</div>
            </div>
        </div>
    </div>
</template>

<script>
import { home_update_logs, species_relation_statistics, atlas_tissue_cell_sample_count } from '@/api/api'
import TagImag1 from '../../../assets/img/tag2-1.png'
import TagImag20 from '../../../assets/img/tag3-2.png'
import TagImag2 from '../../../assets/img/tag2.png'
import TagImag3 from '../../../assets/img/tag3-3.png'
import IconA1 from '@/assets/img/icon_A1.png'
import IconA2 from '@/assets/img/icon_A2.png'
import IconA3 from '@/assets/img/icon_A3.png'
import IconA4 from '@/assets/img/icon_A4.png'
import IconA5 from '@/assets/img/icon_A5.png'
import IconA6 from '@/assets/img/icon_A6.png'

export default {
    name: 'homePage',
    components: {},
    data() {
        return {
            AtlasListRight: [],
            logsList: [
                {
                    content: '',
                    title: 'iPscDB v1.0 released',
                    updated_at: '2023/04/09'
                },
                {
                    content: '',
                    title: 'iPscDB v1.0 Beta Online',
                    updated_at: '2023/01/14'
                }
            ],
            listItem: [],
            cur: [100, 100, 100, 100, 100],
            tempData: [],
            tabsList: [
                // {
                //     value: 'scEnrichment',
                //     label: 'scEnrichment',
                //     image: TagImag1
                // },
                {
                    value: 'Database Structure',
                    label: 'Database Structure',
                    image: TagImag2
                },
                {
                    value: 'CELLiD',
                    label: 'Plant CELLiD',
                    image: TagImag20
                },
                // ----------------------- 2025-04-29
                // {
                //     value: 'mtSC',
                //     label: 'Plant CtAnnotation',
                //     image: TagImag3
                // }
                // --------------------------------
                // {
                //     value: 'Online Intergration',
                //     label: 'Online Intergration'
                // },
            ],
            tabActive: 'Database Structure',
            activeIndex: 0,
            tableList: 20,
            isLast: false,
            pointerActive: -1
        }
    },
    async mounted() {
        this.init()

        let result = await species_relation_statistics()
        let itemData = {}

        if (result.data && result.data.length > 0) {
            itemData = result.data[0]
        }

        this.AtlasListRight = [
            { name: 'Species', value: itemData.species, image: IconA1 },
            { name: 'Experiments', value: itemData.experiments, image: IconA6 },
            { name: 'Atlases', value: itemData.atlases, image: IconA3 },
            { name: 'Markers', value: itemData.markers, image: IconA4 },
            { name: 'Cells', value: itemData.cells, image: IconA5 },
            { name: 'Cells types', value: itemData.cell_types, image: IconA2 }
        ]

        // species_relation_statistics().then((res) => {
        //     if (res.code == 200) {
        //         if (res.data.length > 0) {
        //             this.AtlasListRight = [
        //                 { name: 'Species', value: res.data[0].Species },
        //                 { name: 'Tissues', value: res.data[0].Tissue },
        //                 { name: 'Atlases', value: res.data[0].Atlas },
        //                 { name: 'Samples', value: res.data[0].Sample },
        //                 { name: 'Cells', value: res.data[0].cells }
        //             ]
        //         }
        //     }
        // })
    },
    methods: {
        back() {
            if (this.activeIndex > 0) {
                this.activeIndex = this.activeIndex - 1
            }
        },
        next() {
            if (this.activeIndex < this.listItem.length - 1 - 5) {
                this.activeIndex = this.activeIndex + 1
            }
        },
        mouseleaveItem(index) {
            this.pointerActive = index - this.activeIndex
            if (this.activeIndex + 5 == index) {
                this.isLast = true
                this.activeIndex = this.activeIndex + 1
            }
        },
        mouseoutItem() {
            this.pointerActive = -1
            if (this.isLast) {
                this.isLast = false
                this.activeIndex = this.activeIndex - 1
            }
        },
        init() {
            home_update_logs({}).then((res) => {
                this.logsList = res.data.results
            })
            atlas_tissue_cell_sample_count().then((res) => {
                if (res.code == 200) {
                    if (res.data.length > 0) {
                        this.listItem = res.data
                    }
                }
            })
        },
        imgClick(name, item, index, i, parentItem) {
            // console.log(parentItem)
            if (item.is_show == '1') {
                // this.cur[index] = Number(i)
                this.tempData[index] = item
                this.$set(this.cur, index, Number(i))
                this.$router.push({
                    path: '/searchResult',
                    query: {
                        Tissue: this.tempData[index].Tissue,
                        tissue_label: this.tempData[index].tissue_label,
                        cell_count: this.tempData[index].cell_num,
                        // cell_count: this.tempData[index].cell_count,
                        name: name,
                        sample_count: this.tempData[index].sample_count,
                        nameLabel: parentItem.label
                    }
                })
            }
        },
        jumpProjectResult(item, index) {
            if (this.tempData.length == 0) {
                // 整株
                item.data.forEach((element) => {
                    if (element.Tissue == 'WholePlant') {
                        this.$router.push({
                            path: '/searchResult',
                            query: {
                                Tissue: element.Tissue,
                                tissue_label: element.tissue_label,
                                cell_count: element.cell_num,
                                // cell_count: element.cell_count,
                                name: item.name,
                                sample_count: element.sample_count,
                                nameLabel: item.label
                            }
                        })
                    }
                })
            } else {
                if (this.tempData[index] && this.tempData[index].is_show == '1') {
                    this.$router.push({
                        path: '/searchResult',
                        query: {
                            Tissue: this.tempData[index].Tissue,
                            tissue_label: this.tempData[index].tissue_label,
                            cell_count: this.tempData[index].cell_num,
                            // cell_count: this.tempData[index].cell_count,
                            name: item.name,
                            sample_count: this.tempData[index].sample_count,
                            nameLabel: item.label
                        }
                    })
                }
            }
        },
        goToUpdateLog(id) {
            this.$router.push({
                path: '/UpdateLog',
                query: { id: id }
            })
        }
    }
}
</script>

<style lang="scss" scoped>
@import './style.scss';
</style>

<style scoped>
>>> .el-tabs__item.is-active {
    color: #24a461 !important;
}
>>> .el-tabs__active-bar {
    background-color: #24a461 !important;
}
</style>
