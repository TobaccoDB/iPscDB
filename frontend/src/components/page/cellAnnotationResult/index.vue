<template>
    <div class="cellAnnotationResult">
        <div class="crumbs">
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-breadcrumb-item :to="{ path: '/tools' }">Tools</el-breadcrumb-item>
                <el-breadcrumb-item :to="{ path: '/cellAnnotation' }">Cross-species cell annotation</el-breadcrumb-item>
                <el-breadcrumb-item>Cell Annotation Result</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="cellAnnotationResult-inner" :style="{ minHeight: contentHeight }" v-loading="goLoading" element-loading-text="loading" element-loading-background="#fff">
            <h2>Cell Annotation Result</h2>
            <p class="title">
                Cell Annotation
                <i class="el-icon-download pointer" @click="download('cell_type')">Download</i>
            </p>
            <el-table size="small" :data="tableData" :header-cell-style="headerStyle" v-loading="loading" element-loading-text="running" border style="width: 100%; border-top: 1px solid #24a461">
                <el-table-column :prop="item.key" :label="item.label" align="center" v-for="(item, index) in column" :key="index"></el-table-column>
            </el-table>
            <el-pagination
                style="text-align: right; padding: 10px 5px"
                background
                :current-page="paginationConfig.page"
                :page-sizes="paginationConfig.sizes"
                :page-size="paginationConfig.size"
                :pager-count="7"
                :total="paginationConfig.total"
                @current-change="handleCurrentChange"
                @size-change="handleSizeChange"
                layout="total, sizes, prev, pager, next"
            >
            </el-pagination>
            <p class="title">
                <el-select style="width: 200px" size="large" @change="cellTypeChange" v-model="cell_type" placeholder="Choose">
                    <el-option v-if="item.label != 'Cell Name'" v-for="(item, index) in column" :key="index" :label="item.label" :value="item.label"> </el-option>
                </el-select>
                <i class="el-icon-download pointer" @click="download('cors_matrix')">Download</i>
            </p>
            <div ref="barChartRight1" style="width: 100%; height: 400px" v-loading="loading_cors"></div>
            <!-- <el-table size="small" :data="tableData_cors" :header-cell-style="headerStyle" v-loading="loading_cors" element-loading-text="running"
        border style="width: 100%;border-top:1px solid #24A461;">
        <el-table-column :prop="item.key" :label="item.label" align="center" v-for="(item, index) in itemClumn" :key="index"></el-table-column>
      </el-table>
      <el-pagination style="text-align:right;padding:10px 5px;" background :current-page="paginationConfig_cors.page" :page-sizes="paginationConfig_cors.sizes"
        :page-size="paginationConfig_cors.size" :pager-count="7" :total="paginationConfig_cors.total" @current-change="handleCurrentChange_cors"
        @size-change="handleSizeChange_cors" layout="total, sizes, prev, pager, next">
      </el-pagination> -->
            <dl>
                <dt>
                    <el-button type="primary" @click="download('all')">Download all results</el-button>
                </dt>
                <dd>* Results contained 4 parts:</dd>
                <dd>cors_matrix: Pearson correlation coefficient matrix of each cell and cell type.</dd>
                <dd>top_cors: equals to numbers_plot</dd>
                <dd>Cell_type : the most relevant cell type for each query cell</dd>
                <dd>Cell_type_probility: the top n relevant cell types for each query cell</dd>
            </dl>
        </div>
    </div>
</template>

<script>
import {
    cell_identification_csv,
    cell_identification_cell_type_list,
    cell_identification_cors_matrix_list,
    cell_identification_csv_zip_download,
    cell_identification_filter_csv,
    cell_identification_cell_type_map
} from '@/api/api'
import echarts from 'echarts'
import { optionRight1 } from './config'
export default {
    name: 'cellAnnotationResult',
    components: {},
    data() {
        return {
            optionRight1,
            contentHeight: window.innerHeight - 330 + 'px',
            tableData: [],
            tableData_cors: [],
            column: [{ key: 'id', label: '' }],
            itemClumn: [{ key: 'id', label: '' }],
            paginationConfig: {
                page: 1,
                size: 10,
                sizes: [10, 20, 30],
                total: 0
            },
            loading: false,
            paginationConfig_cors: {
                page: 1,
                size: 10,
                sizes: [10, 20, 30],
                total: 0
            },
            loading_cors: false,
            headerStyle: {
                color: '#666',
                fontWeight: 400,
                fontSize: '14px',
                // background: '#24A461',
                fontFamily: 'Source Han Sans CN'
            },
            classifier_cell_type_csv: '',
            classifier_cors_matrix_csv: '',
            goLoading: false,
            tempData: [],
            cell_type: ''
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        init() {
            this.goLoading = true
            if (this.$route.query.file_name) {
                cell_identification_csv({
                    reference_name: this.$route.query.reference_name,
                    tissue: this.$route.query.tissue,
                    file_name: this.$route.query.file_name,
                    num_top: this.$route.query.num_top
                }).then((res) => {
                    if (res.code == 200) {
                        this.classifier_cell_type_csv = res.data.classifier_cell_type_csv
                        this.classifier_cors_matrix_csv = res.data.classifier_cors_matrix_csv
                        this.getTableData()
                        // this.getTableData_cors()
                        this.goLoading = false
                    }
                })
            } else {
                cell_identification_filter_csv({
                    species_name: this.$route.query.species_name,
                    tissue: this.$route.query.tissue,
                    uuid_rds: this.$route.query.uuid_rds
                }).then((res) => {
                    if (res.code == 200) {
                        this.classifier_cell_type_csv = res.data.classifier_cell_type_csv
                        this.classifier_cors_matrix_csv = res.data.classifier_cors_matrix_csv
                        this.getTableData()
                        // this.getTableData_cors()
                        this.goLoading = false
                    }
                })
            }
        },
        // 表格部分
        getTableData() {
            this.loading = true
            cell_identification_cell_type_list({
                file_name: this.classifier_cors_matrix_csv,
                top: this.$route.query.num_top,
                species_name: this.$route.query.species_name
                // page: this.paginationConfig.page,
                // page_size: this.paginationConfig.size
            }).then((res) => {
                if (res.code == 200) {
                    if (res.data.cellt_ype_data) {
                        this.column = []
                        this.tempData = []
                        Object.entries(res.data.cellt_ype_data).forEach((item) => {
                            this.column.unshift({ key: item[0].replace(/\ /g, '_'), label: item[0] })
                            item[1].forEach((element, index) => {
                                this.tempData[index] = { ...this.tempData[index], ...{ [item[0].replace(/\ /g, '_')]: element } }
                            })
                        })
                        this.cell_type = this.column[1].label
                        this.cellTypeChange(this.column[1].label)
                        this.tableData = this.tempData.slice((this.paginationConfig.page - 1) * this.paginationConfig.size, this.paginationConfig.page * this.paginationConfig.size)
                        this.paginationConfig.total = this.tempData.length

                        this.loading_cors = true
                        let barChartRight1 = this.$refs.barChartRight1
                        if (barChartRight1) {
                            this.optionRight1.xAxis.data = []
                            this.optionRight1.series[0].data = []
                            Object.entries(res.data.histogram_count).forEach((item) => {
                                this.optionRight1.xAxis.data.push(item[0])
                                this.optionRight1.series[0].data.push({ name: item[0], value: item[1] })
                            })

                            const color10 = [
                                '#ee724c',
                                '#b69d78',
                                '#4faf51',
                                '#367cb3',
                                '#faa851',
                                '#98cd96',
                                '#ea9352',
                                '#eb5753',
                                '#a8cde1',
                                '#835c96',
                                '#af5d31',
                                '#f5f39a',
                                '#b393c4',
                                '#ee724c',
                                '#b69d78',
                                '#4faf51',
                                '#367cb3',
                                '#faa851',
                                '#98cd96',
                                '#ea9352',
                                '#eb5753',
                                '#a8cde1',
                                '#835c96',
                                '#af5d31',
                                '#f5f39a',
                                '#b393c4',
                                '#ee724c',
                                '#b69d78',
                                '#4faf51',
                                '#367cb3',
                                '#faa851',
                                '#98cd96',
                                '#ea9352',
                                '#eb5753',
                                '#a8cde1',
                                '#835c96',
                                '#af5d31',
                                '#f5f39a',
                                '#b393c4',
                                '#ee724c',
                                '#b69d78',
                                '#4faf51',
                                '#367cb3',
                                '#faa851',
                                '#98cd96',
                                '#ea9352',
                                '#eb5753',
                                '#a8cde1',
                                '#835c96',
                                '#af5d31',
                                '#f5f39a',
                                '#b393c4'
                            ]
                            this.optionRight1.series[0].data.forEach((item, index) => {
                                item.itemStyle = {
                                    color: color10[index]
                                }
                            })
                        }

                        this.Echarts = echarts.init(barChartRight1)
                        this.Echarts.setOption(this.optionRight1, true)
                        this.loading_cors = false
                    }

                    this.loading = false
                }
            })
        },
        handleCurrentChange(val) {
            this.paginationConfig.page = val
            // this.getTableData()
            this.tableData = this.tempData.slice((this.paginationConfig.page - 1) * this.paginationConfig.size, this.paginationConfig.page * this.paginationConfig.size)
        },
        handleSizeChange(val) {
            this.paginationConfig.page = 1
            this.paginationConfig.size = val
            // this.getTableData()
            this.tableData = this.tempData.slice((this.paginationConfig.page - 1) * this.paginationConfig.size, this.paginationConfig.page * this.paginationConfig.size)
        },
        getTableData_cors() {
            this.loading_cors = true
            cell_identification_cors_matrix_list({
                file_name: this.classifier_cors_matrix_csv,
                page: this.paginationConfig_cors.page,
                page_size: this.paginationConfig_cors.size
            }).then((res) => {
                if (res.code == 200) {
                    if (res.data.count > 0) {
                        this.itemClumn = [{ key: 'id', label: '' }]
                        Object.keys(res.data.results[0]).forEach((element) => {
                            if (element != 'id') {
                                this.itemClumn.push({ key: element.replace(/\./g, '-'), label: element })
                            }
                        })
                        let tempData = []
                        res.data.results.forEach((element) => {
                            let obj = {}
                            Object.entries(element).forEach((item) => {
                                obj = { ...obj, ...{ [item[0].replace(/\./g, '-')]: item[1] } }
                            })
                            tempData.push(obj)
                        })
                        this.tableData_cors = tempData
                        this.paginationConfig_cors.total = res.data.count
                    }

                    this.loading_cors = false
                }
            })
        },
        handleCurrentChange_cors(val) {
            this.paginationConfig_cors.page = val
            this.getTableData_cors()
        },
        handleSizeChange_cors(val) {
            this.paginationConfig_cors.page = 1
            this.paginationConfig_cors.size = val
            this.getTableData_cors()
        },
        download(type) {
            cell_identification_csv_zip_download({
                file_name: this.classifier_cell_type_csv,
                file_type: type
            }).then((res) => {
                if (res.code == 200) {
                    window.open(res.data.cell_identification_csv_zip, '_blank')
                }
            })
        },
        cellTypeChange(cell_type) {
            cell_identification_cell_type_map({
                file_name: this.classifier_cors_matrix_csv,
                species_name: this.$route.query.species_name,
                top: this.$route.query.num_top,
                cell_type: cell_type
            }).then((res) => {
                if (res.code == 200) {
                    this.loading_cors = true
                    let barChartRight1 = this.$refs.barChartRight1
                    if (barChartRight1) {
                        this.optionRight1.xAxis.data = []
                        this.optionRight1.series[0].data = []
                        Object.entries(res.data.histogram_count).forEach((item) => {
                            this.optionRight1.xAxis.data.push(item[0])
                            this.optionRight1.series[0].data.push({ name: item[0], value: item[1] })
                        })

                        const color10 = [
                            '#ee724c',
                            '#b69d78',
                            '#4faf51',
                            '#367cb3',
                            '#faa851',
                            '#98cd96',
                            '#ea9352',
                            '#eb5753',
                            '#a8cde1',
                            '#835c96',
                            '#af5d31',
                            '#f5f39a',
                            '#b393c4',
                            '#ee724c',
                            '#b69d78',
                            '#4faf51',
                            '#367cb3',
                            '#faa851',
                            '#98cd96',
                            '#ea9352',
                            '#eb5753',
                            '#a8cde1',
                            '#835c96',
                            '#af5d31',
                            '#f5f39a',
                            '#b393c4',
                            '#ee724c',
                            '#b69d78',
                            '#4faf51',
                            '#367cb3',
                            '#faa851',
                            '#98cd96',
                            '#ea9352',
                            '#eb5753',
                            '#a8cde1',
                            '#835c96',
                            '#af5d31',
                            '#f5f39a',
                            '#b393c4',
                            '#ee724c',
                            '#b69d78',
                            '#4faf51',
                            '#367cb3',
                            '#faa851',
                            '#98cd96',
                            '#ea9352',
                            '#eb5753',
                            '#a8cde1',
                            '#835c96',
                            '#af5d31',
                            '#f5f39a',
                            '#b393c4'
                        ]
                        this.optionRight1.series[0].data.forEach((item, index) => {
                            item.itemStyle = {
                                color: color10[index]
                            }
                        })
                    }

                    this.Echarts = echarts.init(barChartRight1)
                    this.Echarts.setOption(this.optionRight1, true)
                    this.loading_cors = false
                }
            })
        }
    }
}
</script>
<style lang="scss" scoped>
@import './style.scss';
</style>
