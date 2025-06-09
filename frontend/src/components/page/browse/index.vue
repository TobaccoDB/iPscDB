<template>
    <div class="browse">
        <div class="browse-inner">
            <!-- 统计 -->
            <div class="statistics_top">
                <el-row :gutter="20" style="display: flex; justify-content: space-between">
                    <el-col>
                        <dl>
                            <dt style="color: #fbb02d">{{ formatNumber(Statistics.species) }}</dt>
                            <dd>Species</dd>
                        </dl>
                    </el-col>
                    <el-col>
                        <dl>
                            <dt style="color: #24a461">{{ formatNumber(Statistics.datasets) }}</dt>
                            <dd>Datasets</dd>
                        </dl>
                    </el-col>
                    <el-col>
                        <dl>
                            <dt style="color: #76ac13">{{ formatNumber(Statistics.experiments) }}</dt>
                            <dd>Experiments</dd>
                        </dl>
                    </el-col>
                    <el-col>
                        <dl>
                            <dt style="color: #f08839">{{ formatNumber(Statistics.technologies) }}</dt>
                            <dd>Technologies</dd>
                        </dl>
                    </el-col>
                </el-row>
                <el-row :gutter="20" style="display: flex; justify-content: space-between">
                    <el-col>
                        <dl>
                            <dt style="color: #f08839">{{ formatNumber(Statistics.atlases) }}</dt>
                            <dd>Atlases</dd>
                        </dl>
                    </el-col>
                    <el-col>
                        <dl>
                            <dt style="color: #76ac13">{{ formatNumber(Statistics.classic_markers) }}</dt>
                            <dd>Classic Markers</dd>
                        </dl>
                    </el-col>
                    <el-col>
                        <dl>
                            <dt style="color: #24a461">{{ formatNumber(Statistics.marker_genes) }}</dt>
                            <dd>Marker genes</dd>
                        </dl>
                    </el-col>
                    <el-col>
                        <dl>
                            <dt style="color: #fbb02d">{{ formatNumber(Statistics.cells) }}</dt>
                            <dd>Cells</dd>
                        </dl>
                    </el-col>
                    <el-col>
                        <dl>
                            <dt style="color: #24a461">{{ formatNumber(Statistics.cell_types) }}</dt>
                            <dd>Cell types</dd>
                        </dl>
                    </el-col>
                </el-row>
            </div>
            <!-- 饼图 -->
            <div class="Statistics">
                <div class="Statistics_content">
                    <p class="title">
                        <span class="title_header">Statistics</span>
                    </p>
                    <el-row :gutter="20" v-loading="chartLoading">
                        <el-col :span="8">
                            <div ref="pieChart1" style="width: 100%; height: 300px"></div>
                        </el-col>
                        <el-col :span="8">
                            <div style="width: 100%; height: 300px">
                                <div ref="pieChart2" style="width: 100%; height: 300px"></div>
                            </div>
                        </el-col>
                        <el-col :span="8">
                            <div ref="pieChart3" style="width: 100%; height: 300px"></div>
                        </el-col>
                    </el-row>
                </div>
            </div>

            <!-- 表格 -->
            <div class="browse_table">
                <div class="title">
                    <span class="title_header" style="line-height: 20px">Dataset information</span>
                    <!-- <el-form style="float:right;" :inline="true" @submit.native.prevent size="lager" :model="formInline" class="demo-form-inline">
            <el-form-item label="search">
              <el-input v-model="formInline.search" clearable @change="searchTitle" @keyup.enter.native="searchTitle" placeholder="Please enter"></el-input>
            </el-form-item>
          </el-form> -->
                </div>
                <!-- <jg-table
                    :tableData="tableData"
                    :column="column"
                    :loading="tableLoading"
                    :cellstyle="cellstyle"
                    :paginationConfig="paginationConfig"
                    @handleCurrentChange="handleCurrentChange"
                    @handleSizeChange="handleSizeChange"
                    @handlecell="handlecell"
                ></jg-table> -->
                <PTable></PTable>
            </div>
        </div>
    </div>
</template>

<script>
import echarts from 'echarts'
import { option1, option2, option3, column } from './config'
import { cell_browse_statistics, browse_list, species_relation_statistics } from '@/api/api'
import jgTable from '@/components/jgTable/index'
import PTable from './common/PTable.vue'
let pieChart1 = null
let pieChart2 = null
let pieChart3 = null
export default {
    name: 'browse',
    components: {
        jgTable,
        PTable
    },
    data() {
        return {
            Statistics: {
                species: 0,
                datasets: 0,
                experiments: 0,
                technologies: 0,
                atlases: 0,
                markers: 0,
                classic_markers: 0,
                marker_genes: 0,
                cells: 0,
                cell_types: 0
            },
            formInline: {
                search: ''
            },
            tableData: [],
            column,
            paginationConfig: {
                page: 1,
                size: 10,
                sizes: [10, 20, 30],
                total: 0
            },
            option1,
            option2,
            option3,
            chartLoading: false,
            tableLoading: false
        }
    },
    mounted() {
        this.showEcharts()
        this.getTableData()
        species_relation_statistics().then((res) => {
            if (res.code == 200) {
                if (res.data.length > 0) {
                    this.Statistics = {
                        species: res.data[0].species,
                        datasets: res.data[0].datasets,
                        experiments: res.data[0].experiments,
                        technologies: res.data[0].technologies,
                        atlases: res.data[0].atlases,
                        markers: res.data[0].markers,
                        classic_markers: res.data[0].classic_markers,
                        marker_genes: res.data[0].marker_genes,
                        cells: res.data[0].cells,
                        cell_types: res.data[0].cell_types
                    }
                }
            }
        })
    },
    beforeDestory() {
        pieChart1.dispose && pieChart1.dispose()
        pieChart2.dispose && pieChart2.dispose()
        pieChart3.dispose && pieChart3.dispose()
        pieChart1 = null
        pieChart2 = null
        pieChart3 = null
    },
    methods: {
        getTableData() {
            this.tableLoading = true
            browse_list({
                species_name: '',
                title: this.formInline.search,
                page: this.paginationConfig.page,
                page_size: this.paginationConfig.size
            }).then((res) => {
                if (res.code == 200) {
                    this.tableData = res.data.results
                    this.paginationConfig.total = res.data.count
                    this.tableLoading = false
                }
            })
        },
        searchTitle() {
            this.paginationConfig.page = 1
            this.getTableData(this.formInline.search)
        },
        showEcharts() {
            pieChart1 = this.$refs.pieChart1
            pieChart2 = this.$refs.pieChart2
            pieChart3 = this.$refs.pieChart3
            this.chartLoading = true
            cell_browse_statistics({}).then((res) => {
                if (res.code == 200) {
                    this.option1.series[0].data = res.data.speace_cell_total
                    this.option2.series[0].data = res.data.project_id_total
                    this.option3.series[0].data = res.data.marker_total.map((item) => {
                        item.name = item.species
                        return item
                    })
                    if (pieChart1) {
                        this.Echarts1 = echarts.init(pieChart1)
                        this.Echarts1.setOption(this.option1)
                    }
                    if (pieChart2) {
                        this.Echarts2 = echarts.init(pieChart2)
                        this.Echarts2.setOption(this.option2)
                        // this.Echarts3.setOption(this.option3)
                        this.chartLoading = false
                    }
                    if (pieChart3) {
                        let Echarts3 = echarts.init(pieChart3)
                        Echarts3.setOption(this.option3)
                    }
                }
            })
        },
        handleCurrentChange(val) {
            this.paginationConfig.page = val
            this.getTableData()
        },
        handleSizeChange(val) {
            this.paginationConfig.page = 1
            this.paginationConfig.size = val
            this.getTableData()
        },
        cellstyle({ row, column, rowIndex, columnIndex }) {
            if (column.label === 'Title' || column.label === 'Project ID') {
                return { color: '#0a9daa', cursor: 'pointer' }
            }
            // 针对Safari表格width与showOverflowTooltip暂不能共存异常
            const tempWidth = column.realWidth || column.width
            if (column.showOVerflowTooltip) {
                return {
                    minWidth: tempWidth + 'px',
                    maxWidth: tempWidth + 'px'
                }
            }
            return { fontSize: '14px' }
        },
        handlecell(params) {
            if (params.col.label == 'Title') {
                window.open(`${params.row.doi}`, '_blank')
            } else if (params.col.label == 'Project ID') {
                this.$router.push({
                    path: '/projectResult',
                    query: {
                        lit_id: params.row.lit_id,
                        species_name: params.row.species_value,
                        tissue: params.row.tissue,
                        project_id: params.row.project_id,
                        sample_count: params.row.sample_count,
                        cell_count: params.row.cell_count
                    }
                })
            }
            // if (params.col.label == 'PMID') {
            //   window.open(`https://pubmed.ncbi.nlm.nih.gov/${params.row.pmid}/`, '_blank')
            // } else if (params.col.label == 'Gene ID') {
            //   this.$router.push({
            //     path: '/searchDetails',
            //     query: {
            //       from: 'browse',
            //       id: params.row.id
            //     }
            //   })
            // }
        },
        formatNumber(num) {
            return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
        }
    }
}
</script>

<style lang="scss" scoped>
@import './style.scss';
</style>
