<template>
    <div class="searchResult">
        <div class="crumbs">
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-breadcrumb-item v-if="$route.query.from == 'search'" :to="{ path: '/search' }">Search</el-breadcrumb-item>
                <el-breadcrumb-item v-if="$route.query.from == 'home'" :to="{ path: '/homePage' }">Home</el-breadcrumb-item>
                <el-breadcrumb-item>Search result</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <p class="title1">Statistical graph of cell markers</p>
        <div class="search-inner" v-loading="chartLoading">
            <!-- 图表 -->
            <el-row :gutter="20">
                <el-col :span="16">
                    <div id="myChart" style="width: 100%; height: 442px"></div>
                </el-col>
                <el-col :span="8">
                    <div class="chartTable">
                        <i class="el-icon-download pointer" style="padding: 15px 0 15px 15px; color: #24a461; float: right; cursor: pointer" @click="chartDownload('txt')">TXT</i>
                        <i class="el-icon-download pointer" style="padding: 15px 0 15px 15px; color: #24a461; float: right; cursor: pointer" @click="chartDownload('csv')">CSV</i>
                        <jg-table
                            :tableData="chartTableData"
                            :column="chartColumn"
                            layout="prev, pager, next"
                            :cellstyle="cellstyle"
                            :paginationConfig="chartConfig"
                            :pagerCount="5"
                            @handleCurrentChange="chartHandleCurrentChange"
                            @handlecell="handlecell"
                        ></jg-table>
                    </div>
                </el-col>
            </el-row>
        </div>
        <p class="title1">Results</p>
        <div class="search-inner">
            <!-- 表格 -->
            <i class="el-icon-download pointer" style="padding-top: 15px; color: #24a461; float: right; cursor: pointer" @click="download('txt')">TXT</i>
            <i class="el-icon-download pointer" style="padding: 15px 15px 0 0; color: #24a461; float: right; cursor: pointer" @click="download('csv')">CSV</i>
            <el-form ref="form1" :inline="true">
                <el-form-item label="Marker resource">
                    <el-select size="large" @change="resourceChange" v-model="marker_resource" placeholder="Choose">
                        <el-option v-for="(item, index) in resourceOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <jg-table
                :tableData="tableData"
                :column="column"
                :loading="loading"
                :cellstyle="cellstyle"
                :paginationConfig="paginationConfig"
                @handleCurrentChange="handleCurrentChange"
                @handleSizeChange="handleSizeChange"
                @handlecell="handlecell"
            ></jg-table>
        </div>
    </div>
</template>

<script>
import { cell_search, cell_search_marker, search_marker, page_search_heat_map, all_search_heat_map } from '@/api/search'
import jgTable from '@/components/jgTable/index'

export default {
    name: 'searchResult',
    components: {
        jgTable
    },
    data() {
        return {
            chartLoading: false,
            // tableHeight: (window.innerHeight - 416),
            tableData: [],
            column: [
                { key: 'gene_id', label: 'Gene ID' },
                { key: 'species_type', label: 'Species' },
                { key: 'gene_symbol', label: 'Gene Symbol' },
                { key: 'cell_type', label: 'Cell Type' },
                { key: 'marker_resource', label: 'Marker Resource' }
                // { key: 'Description', label: 'Description' },
                // { key: 'pmid', label: 'PMID', width: 140 }
            ],
            paginationConfig: {
                page: 1,
                size: 10,
                sizes: [10, 20, 30],
                total: 0
            },
            loading: false,
            marker_resource: '',
            resourceOptions: [
                {
                    label: 'All',
                    value: ''
                },
                {
                    label: 'Bulk RNA-seq',
                    value: 'Bulk RNA-seq'
                },
                {
                    label: 'Experimental',
                    value: 'Experimental'
                },
                {
                    label: 'scRNA-seq',
                    value: 'scRNA-seq'
                }
            ],
            chartTableData: [],
            chartColumn: [
                { key: 'gene_id', label: 'Cell Markers' },
                { key: 'supported', label: 'Supported NO.' }
            ],
            chartConfig: {
                page: 1,
                size: 10,
                // sizes: [10, 20, 30],
                total: 0
            }
        }
    },
    mounted() {
        if (this.$route.query.marker_resource != '' && this.$route.query.marker_resource != undefined) {
            this.marker_resource = this.$route.query.marker_resource
        }
        this.getTableData()
        this.getZingChartData()
        this.getChartTableData()
    },
    methods: {
        getTableData() {
            this.loading = true
            this.column = [
                { key: 'gene_id', label: 'Gene ID' },
                { key: 'species_type', label: 'Species' },
                { key: 'gene_symbol', label: 'Gene Symbol' },
                { key: 'cell_type', label: 'Cell Type' },
                { key: 'marker_resource', label: 'Marker Resource' }
                // { key: 'Description', label: 'Description' },
            ]
            if (this.$route.query.type == 'keyword_form') {
                this.column = [
                    { key: 'gene_id', label: 'Gene ID', width: 200 },
                    { key: 'species_type', label: 'Species', width: 200 },
                    { key: 'gene_symbol', label: 'Gene Symbol', width: 200 },
                    // { key: 'cell_type', label: 'Cell Type' },
                    // { key: 'marker_resource', label: 'Marker resource' },
                    { key: 'description', label: 'Description' }
                ]
                cell_search({
                    ...this.$route.query,
                    ...{
                        marker_resource: this.marker_resource,
                        page: this.paginationConfig.page,
                        page_size: this.paginationConfig.size
                    }
                }).then((res) => {
                    if (res.code == 200) {
                        this.tableData = res.data.results
                        this.paginationConfig.total = res.data.count
                        this.loading = false
                    }
                })
            } else if (this.$route.query.type == 'cellMarker_form') {
                cell_search_marker({
                    ...this.$route.query,
                    ...{
                        marker_resource: this.marker_resource,
                        page: this.paginationConfig.page,
                        page_size: this.paginationConfig.size
                    }
                }).then((res) => {
                    if (res.code == 200) {
                        this.tableData = res.data.results
                        this.paginationConfig.total = res.data.count
                        this.loading = false
                    }
                })
            } else if (this.$route.query.type == 'marker_form') {
                search_marker({
                    ...this.$route.query,
                    ...{
                        marker_resource: this.marker_resource,
                        page: this.paginationConfig.page,
                        page_size: this.paginationConfig.size
                    }
                }).then((res) => {
                    if (res.code == 200) {
                        this.tableData = res.data.results
                        this.paginationConfig.total = res.data.count
                        this.loading = false
                    }
                })
            }
        },
        getChartTableData() {
            page_search_heat_map({
                ...this.$route.query,
                ...{
                    marker_resource: this.marker_resource,
                    page: this.chartConfig.page,
                    page_size: this.chartConfig.size
                }
            }).then((res) => {
                if (res.code == 200) {
                    this.chartTableData = res.data.results
                    this.chartConfig.total = res.data.count
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
        chartHandleCurrentChange(val) {
            this.chartConfig.page = val
            this.getChartTableData()
        },
        cellstyle({ row, column, rowIndex, columnIndex }) {
            if (column.label === 'PMID' || column.label === 'Gene ID' || column.label === 'Gene Name') {
                return { color: '#0a9daa', cursor: 'pointer' }
            }
            return { fontSize: '14px' }
        },
        handlecell(params) {
            if (params.col.label == 'PMID') {
                window.open(`https://pubmed.ncbi.nlm.nih.gov/${params.row.pmid}/`, '_blank')
            } else if (params.col.label == 'Gene ID' || params.col.label == 'Gene Name') {
                sessionStorage.removeItem('searchResultQuery')
                sessionStorage.setItem('searchResultQuery', JSON.stringify(this.$route.query))
                this.$router.push({
                    path: '/searchDetails',
                    query: {
                        from: this.$route.query.from,
                        id: params.row.id,
                        gene_id: params.row.gene_id
                    }
                })
            }
        },
        download(type) {
            if (this.paginationConfig.total > 0) {
                this.jg_downloadFile('api/v1/cell_search/cell_search_download/', {
                    ...this.$route.query,
                    ...{
                        marker_resource: this.marker_resource,
                        type: type
                    }
                })
            }
        },
        resourceChange(val) {
            this.paginationConfig.page = 1
            this.chartConfig.page = 1
            this.getTableData()
            this.getZingChartData()
            this.getChartTableData()
        },
        getZingChartData() {
            this.chartLoading = true
            all_search_heat_map({
                ...this.$route.query,
                ...{
                    marker_resource: this.marker_resource
                }
            }).then((res) => {
                if (res.code == 200) {
                    ZC.LICENSE = ['569d52cefae586f634c54f86dc99e6a9', 'b55b025e438fa8a98e32482b5f768ff5']

                    res.data.forEach((item) => {
                        item.text = item.gene_id
                        item.count = item.supported
                    })
                    var myConfig = {
                        graphset: [
                            {
                                type: 'wordcloud',
                                options: {
                                    style: {
                                        tooltip: {
                                            visible: true,
                                            text: '%text: %hits'
                                        }
                                    },
                                    words: res.data
                                }
                            }
                        ]
                    }
                    zingchart.render({
                        id: 'myChart',
                        data: myConfig,
                        hideprogresslogo: true,
                        height: '100%',
                        width: '100%',
                        events: {
                            complete: (p) => {
                                this.chartLoading = false
                            }
                        }
                    })
                }
            })
        },
        chartDownload(type) {
            if (this.chartConfig.total > 0) {
                this.jg_downloadFile('api/v1/cell_search/all_search_heat_download', {
                    ...this.$route.query,
                    ...{
                        marker_resource: this.marker_resource,
                        type: type
                    }
                })
            }
        }
    }
}
</script>

<style>
#myChart-license-text {
    display: none;
}
</style>

<style lang="scss" scoped>
.searchResult {
    width: 1240px;
    height: 100%;
    margin: 0 auto;
    background: #fafafa;
    padding: 0 0 30px 0;
    .crumbs {
        height: 28px;
        padding-top: 12px;
        margin: 0;
    }
    .title1 {
        font-size: 20px;
        font-family: PingFang SC;
        font-weight: bold;
        color: #fff;
        height: 40px;
        line-height: 40px;
        background: #24a461;
        padding-left: 20px;
    }
    .search-inner {
        width: 1200px;
        padding: 20px;
        margin: 0 auto;
        overflow: hidden;
        background: rgba(255, 255, 255, 1);
    }
    // .chartTable ::v-deep .el-pagination.is-background .btn-next,
    // .chartTable ::v-deep .el-pagination.is-background .btn-prev,
    // .chartTable ::v-deep .el-pagination.is-background .el-pager,
    // .chartTable ::v-deep .el-pagination.is-background .el-pager li {
    //   float: left !important;
    //   margin-bottom: 10px;
    // }
}
</style>
