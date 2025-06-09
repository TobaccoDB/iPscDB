<template>
    <div class="homepage">
        <div class="banner">
            <p class="banner_title">
                <span>I</span>ntegrated <span>P</span>lant
                <span>S</span>
                <span style="color: #fff">ingle</span>
                <span>-C</span>ell
                <span>D</span>
                <span style="color: #fff">ata</span>
                <span>b</span>ase
            </p>
            <p class="banner_p">
                iPscDB is a single-cell transcriptomics data resource that provides<br />a comprehensive and relatively accurate atlas of cell integration<br />for different tissues of different
                plants.
            </p>
        </div>
        <!-- 统计 -->
        <div class="homepage_statistics">
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
        </div>
    </div>
</template>

<script>
import { home_update_logs, species_relation_statistics, atlas_tissue_cell_sample_count } from '@/api/api'
export default {
    name: 'homePage',
    components: {},
    data() {
        return {
            AtlasListRight: [
                { name: 'Species', value: 0 },
                { name: 'Tissues', value: 0 },
                { name: 'Atlases', value: 0 },
                { name: 'Samples', value: 0 },
                { name: 'Cells', value: 0 }
            ],
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
            tempData: []
        }
    },
    mounted() {
        this.init()
        species_relation_statistics().then((res) => {
            if (res.code == 200) {
                if (res.data.length > 0) {
                    this.AtlasListRight = [
                        { name: 'Species', value: res.data[0].Species },
                        { name: 'Tissues', value: res.data[0].Tissue },
                        { name: 'Atlases', value: res.data[0].Atlas },
                        { name: 'Samples', value: res.data[0].Sample },
                        { name: 'Cells', value: res.data[0].cells }
                    ]
                }
            }
        })
    },
    methods: {
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
        imgClick(name, item, index, i) {
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
                        sample_count: this.tempData[index].sample_count
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
                                sample_count: element.sample_count
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
                            sample_count: this.tempData[index].sample_count
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
