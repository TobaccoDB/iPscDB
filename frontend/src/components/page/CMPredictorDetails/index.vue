<template>
    <div class="CMPredictorDetails">
        <div class="crumbs">
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <!-- <el-breadcrumb-item :to="{ path: '/CMPredictor' }">CMPredictor</el-breadcrumb-item> -->
                <!-- <el-breadcrumb-item>CMPredictor Results</el-breadcrumb-item> -->
                <el-breadcrumb-item :to="{ path: '/search' }">Search</el-breadcrumb-item>
                <el-breadcrumb-item>Search Results</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="CMPredictorDetails-inner">
            <p class="title1">Results</p>
            <!-- 表格 -->
            <div class="cmp_table">
                <i class="el-icon-download pointer" style="padding-bottom: 20px; color: #24a461; float: right; cursor: pointer" @click="download('txt')">TXT</i>
                <i class="el-icon-download pointer" style="padding: 0 15px 20px 0; color: #24a461; float: right; cursor: pointer" @click="download('csv')">CSV</i>
                <jg-table
                    :tableData="tableData"
                    :column="column"
                    :loading="loading"
                    :tableHeight="tableHeight"
                    :paginationConfig="paginationConfig"
                    :cellstyle="cellstyle"
                    @handleCurrentChange="handleCurrentChange"
                    @handlecell="handlecell"
                ></jg-table>
            </div>
        </div>
    </div>
</template>

<script>
import { cell_search_cmpredictor } from '@/api/api'
import jgTable from '@/components/jgTable/index'
export default {
    name: 'CMPredictorDetails',
    components: {
        jgTable
    },
    data() {
        return {
            tableHeight: window.innerHeight - 396,
            tableData: [],
            column: [
                { key: 'Refernce_species', label: 'Refernce species', width: 160 },
                { key: 'Query_species', label: 'Query species', width: 160 },
                { key: 'Query', label: 'Query', width: 160 },
                { key: 'Target', label: 'Target', width: 200 },
                { key: 'Identity', label: 'Identity(%)', width: 100 },
                { key: 'Length', label: 'Length' },
                { key: 'Mismatch', label: 'Mismatch', width: 100 },
                { key: 'Gapopen', label: 'Gapopen', width: 100 },
                { key: 'Q-Start', label: 'Q-Start' },
                { key: 'Q-End', label: 'Q-End' },
                { key: 'T-Start', label: 'T-Start' },
                { key: 'T-End', label: 'T-End' },
                { key: 'E-value', label: 'E-value' },
                { key: 'Score', label: 'Score' }
            ],
            paginationConfig: {
                page: 1,
                size: 10,
                total: 0
            },
            loading: false,
            csv_download_file_name: '',
            txt_download_file_name: ''
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        init() {
            if (this.$route.query.marker_resource == 'all') {
                this.column.push({
                    key: 'all',
                    label: 'All',
                    width: 300
                })
            } else if (this.$route.query.marker_resource == 'Bulk RNA-seq') {
                this.column.push({
                    key: 'Bulk RNA-seq',
                    label: 'Bulk RNA-seq',
                    width: 300
                })
            } else if (this.$route.query.marker_resource == 'Experimental') {
                this.column.push({
                    key: 'Experimental',
                    label: 'Experimental',
                    width: 300
                })
            } else if (this.$route.query.marker_resource == 'scRNA-seq') {
                this.column.push({
                    key: 'scRNA-seq',
                    label: 'scRNA-seq',
                    width: 300
                })
            }
            this.getTableData()
        },
        getTableData() {
            this.loading = true
            cell_search_cmpredictor({
                ...this.$route.query,
                ...{
                    page: this.paginationConfig.page,
                    page_size: this.paginationConfig.size
                }
            }).then((res) => {
                if (res.code == 200) {
                    this.tableData = res.data.results
                    this.paginationConfig.total = res.data.count
                    if (res.data.count > 0) {
                        this.txt_download_file_name = res.data.results[0].txt_download_file_name
                        this.csv_download_file_name = res.data.results[0].csv_download_file_name
                    }
                    this.loading = false
                }
            })
        },
        handleCurrentChange(val) {
            this.paginationConfig.page = val
            this.getTableData()
        },
        download(type) {
            if (this.paginationConfig.total > 0) {
                this.jg_downloadFile('api/v1/cell_search_cmpredictor/cmp_reditor_download', { name: type == 'csv' ? this.csv_download_file_name : this.txt_download_file_name })
            }
        },
        cellstyle({ row, column, rowIndex, columnIndex }) {
            if (column.label === 'Query') {
                return { color: '#0a9daa', cursor: 'pointer' }
            }
            return { fontSize: '14px' }
        },
        handlecell(params) {
            if (params.col.label == 'Query') {
                sessionStorage.removeItem('CMPredictorDetailsQuery')
                sessionStorage.setItem('CMPredictorDetailsQuery', JSON.stringify(this.$route.query))
                this.$router.push({
                    path: '/searchDetails',
                    query: {
                        from: 'CMPredictorDetails',
                        id: params.row.id
                    }
                })
            }
        }
    }
}
</script>
<style lang="scss" scoped>
@import './style.scss';
</style>
