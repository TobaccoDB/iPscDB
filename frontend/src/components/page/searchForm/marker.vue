<template>
    <div class="marker">
        <div class="marker-header">
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-breadcrumb-item :to="{ path: '/searchForm' }">Search</el-breadcrumb-item>
                <el-breadcrumb-item>Search result</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="marker-name">Statistical graph of cell markers</div>
        <div class="marker-content1">
            <div class="marker-content1-work" ref="wordCloud" v-loading="loading"></div>
            <div class="marker-content1-table">
                <div class="marker-content1-work-header">
                    <!-- <span class="el-icon-download" style="margin-right: 20px">CSV</span>
                    <span class="el-icon-download">TXT</span> -->
                </div>
                <el-table :data="tableData1" style="width: 100%" v-loading="count1Loading">
                    <el-table-column prop="name" label="Cell Markers" align="center"> </el-table-column>
                    <el-table-column prop="source_no" label="Supported NO." align="center"> </el-table-column>
                </el-table>
                <div class="TableItemBody">
                    <el-pagination
                        @size-change="handleSizeChange"
                        @current-change="handleCurrentChange"
                        :current-page="queryInfo.page"
                        :page-sizes="[10, 20, 30, 50]"
                        :page-size="queryInfo.page_size"
                        layout="prev, pager, next"
                        :total="count1"
                        background
                        :pager-count="5"
                    >
                    </el-pagination>
                </div>
            </div>
        </div>
        <div class="marker-name">Results</div>
        <div class="marker-content2">
            <div class="marker-content2-header">
                <div class="marker-content2-header-left">
                    <!-- <span style="margin-right: 10px">Marker resource</span>
                    <el-select v-model="selectValue" placeholder="Select.." style="width: 200px; margin-right: 20px">
                        <el-option label="Glycine max" value="2"> </el-option>
                    </el-select> -->
                </div>
                <div class="marker-content2-header-right">
                    <span class="el-icon-download" style="margin-right: 20px" @click="downLoad">CSV</span>
                    <!-- <span class="el-icon-download">TXT</span> -->
                </div>
            </div>
            <el-table :data="tableData2" style="width: 100%" v-loading="count2Loading">
                <el-table-column prop="gene_id" label="Gene ID" align="center">
                    <template slot-scope="scope">
                        <span style="color: #24a461; cursor: pointer" @click="goMarkerCell(scope.row)">{{ scope.row.gene_id }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="species" label="Species" align="center"> </el-table-column>
                <el-table-column prop="gene_symbol" label="Gene Symbol" align="center"> </el-table-column>
                <el-table-column prop="description" label="Description" align="center"> </el-table-column>
            </el-table>
            <div class="TableItemBody">
                <el-pagination
                    @size-change="handleSizeChange2"
                    @current-change="handleCurrentChange2"
                    :current-page="queryInfo2.page"
                    :page-sizes="[10, 20, 30, 50]"
                    :page-size="queryInfo.page_size"
                    layout="total, sizes, prev, pager, next"
                    :total="count2"
                    background
                >
                </el-pagination>
            </div>
        </div>
    </div>
</template>

<script>
import * as echarts from 'echarts'
import 'echarts-wordcloud'
import { marker_word_data, search_word_cloud_list, search_marker_gene_table } from '@/api/api'
export default {
    data() {
        return {
            tableData1: [],
            tableData2: [],
            selectValue: '',
            queryInfo: {
                page: 1,
                page_size: 10
            },
            count1: 0,
            count2: 0,
            loading: false,
            queryInfo2: {
                page: 1,
                page_size: 10
            },
            count1Loading: false,
            count2Loading: false,
            baseUrl: process.env.VUE_APP_BASE_URL
        }
    },
    mounted() {
        let species_name = this.$route.query.species_name
        let search_gene = this.$route.query.search_gene
        if (!species_name || !search_gene) {
            this.$router.back()
        }
        this.getWord()
        this.getTableTop()
        this.getTableBottom()
    },
    methods: {
        goMarkerCell(item) {
            this.$router.push({
                path: '/markerCell',
                query: {
                    gene_id: item.gene_id,
                    species_name: item.species
                }
            })
        },
        handleSizeChange(val) {
            this.queryInfo.page = 1
            this.queryInfo.page_size = val
            this.getTableTop()
        },
        handleCurrentChange(val) {
            this.queryInfo.page = val
            this.getTableTop()
        },
        getWord() {
            this.loading = true
            marker_word_data({
                species_name: this.$route.query.species_name,
                search_gene: this.$route.query.search_gene
            })
                .then((res) => {
                    if (res.code == 200) {
                        this.infoWordCloud(res.data)
                    }
                })
                .finally(() => {
                    this.loading = false
                })
        },
        getTableTop() {
            this.count1Loading = true
            search_word_cloud_list({
                species_name: this.$route.query.species_name,
                search_gene: this.$route.query.search_gene,
                ...this.queryInfo
            })
                .then((res) => {
                    if (res.code == 200) {
                        this.tableData1 = res.data.results
                        this.count1 = res.data.count
                    }
                })
                .finally(() => {
                    this.count1Loading = false
                })
        },
        handleSizeChange2(val) {
            this.queryInfo2.page = 1
            this.queryInfo2.page_size = val
            this.getTableBottom()
        },
        handleCurrentChange2(val) {
            this.queryInfo2.page = val
            this.getTableBottom()
        },
        getTableBottom() {
            this.count2Loading = true
            search_marker_gene_table({
                species_name: this.$route.query.species_name,
                search_gene: this.$route.query.search_gene,
                ...this.queryInfo2
            })
                .then((res) => {
                    if (res.code == 200) {
                        this.tableData2 = res.data.results
                        this.count2 = res.data.count
                    }
                })
                .finally(() => {
                    this.count2Loading = false
                })
        },
        downLoad() {
            let url = `${this.baseUrl}/api/v1/search_marker_gene_table/search_marker_gene_down?species_name=${this.$route.query.species_name}&search_gene=${this.$route.query.search_gene}`
            window.open(url, '_blank')
            // let fileName = new Date().getTime() + '.csv'
            // const a = document.createElement('a')
            // a.href = url
            // a.download = fileName
            // a.target = '_blank'
            // a.style.display = 'none'
            // document.body.appendChild(a)
            // a.click()
            // document.body.removeChild(a)
        },
        getRandomInt(min, max) {
            min = Math.ceil(min)
            max = Math.floor(max)
            return Math.floor(Math.random() * (max - min + 1)) + min
        },
        infoWordCloud(words) {
            let This = this
            let keywords = words.map((item) => {
                item.value = item.source_no
                return item
            })
            let myChart = echarts.init(this.$refs.wordCloud)
            let option = {
                series: [
                    {
                        type: 'wordCloud',
                        //maskImage: maskImage,
                        sizeRange: [30, 40],
                        rotationRange: [-45, 45],
                        rotationStep: 45,
                        gridSize: 8,
                        shape: 'pentagon',
                        width: '100%',
                        height: '100%',
                        textStyle: {
                            normal: {
                                color: function () {
                                    return 'rgb(' + [This.getRandomInt(0, 255), This.getRandomInt(0, 255), This.getRandomInt(0, 255)].join(',') + ')'
                                },
                                fontFamily: 'sans-serif',
                                fontWeight: 'normal'
                            },
                            emphasis: {
                                shadowBlur: 10,
                                shadowColor: '#333'
                            }
                        },
                        data: keywords
                    }
                ]
            }
            option && myChart.setOption(option)
        }
    }
}
</script>

<style scoped lang="scss">
.marker {
    width: 1240px;
    margin: 0 auto;
    height: auto;
    .marker-header {
        width: 100%;
        height: 40px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
    }
    .marker-name {
        width: 100%;
        height: 40px;
        font-size: 20px;
        font-family: PingFang SC;
        font-weight: 700;
        color: #fff;
        height: 40px;
        line-height: 40px;
        background: #24a461;
        padding-left: 20px;
        box-sizing: border-box;
    }
    .marker-content1 {
        width: 100%;
        height: 574px;
        padding: 20px;
        box-sizing: border-box;
        display: flex;
        background: #fff;
        .marker-content1-work {
            width: calc(100% - 390px);
            height: 100%;
        }
        .marker-content1-table {
            width: 390px;
            height: 100%;
            .marker-content1-work-header {
                width: 100%;
                height: 46px;
                text-align: right;
                line-height: 46px;
                span {
                    color: #24a461;
                    cursor: pointer;
                }
            }
        }
    }
    .marker-content2 {
        width: 100%;
        padding: 20px;
        box-sizing: border-box;
        background: #fff;
        .marker-content2-header {
            width: 100%;
            height: 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            .marker-content2-header-right {
                text-align: right;
                span {
                    color: #24a461;
                    cursor: pointer;
                }
            }
        }
    }
    .TableItemBody {
        height: 50px;
        width: 100%;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
}
</style>

<style lang="scss">
.TableItemBody {
    .el-pagination.is-background .el-pager li:not(.disabled).active {
        background-color: #24a461 !important;
    }
    .el-radio__input.is-checked + .el-radio__label {
        color: #24a461 !important;
    }
    .el-radio__input.is-checked .el-radio__inner {
        background: #24a461 !important;
        color: #24a461 !important;
        border-color: #24a461 !important;
    }
    .el-button--primary {
        background: #24a461 !important;
        border-color: #24a461 !important;
        font-size: 16px;
    }
}
</style>
