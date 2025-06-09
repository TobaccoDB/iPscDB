<template>
    <div class="tableItem">
        <div class="TableItemHeader">
            <el-input v-model="searchVal" placeholder="Search.." @keyup.enter.native="keydown" style="width: 210px; margin-right: 10px" suffix-icon="el-icon-search"></el-input>
            <el-button icon="el-icon-download" type="success"> <span style="font-size: 12px" :loading="loadingButton" @click="getDownload">CSV</span></el-button>
        </div>
        <el-table :data="tableData" style="width: 100%" v-loading="loading">
            <el-table-column prop="gene" label="Gene ID" width="140px" align="center">
                <template slot-scope="scope">
                    <span style="color: #24a461; text-decoration: underline; cursor: pointer; font-size: 12px" @click="goMarkerCell(scope.row.gene)">{{ scope.row.gene }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="name" label="Gene Name" width="140px" align="center"> </el-table-column>
            <el-table-column prop="cellType_id" label="Celltype ID" width="140px" align="center"> </el-table-column>
            <el-table-column prop="source_no" label="Classic Marker" width="120px" align="center">
                <template slot-scope="scope">
                    <span class="tableItemTableIcon" :class="scope.row.classic_marker == '1' ? 'el-icon-star-on tableItemTableIconActive' : 'el-icon-star-off '"></span>
                </template>
            </el-table-column>
            <el-table-column prop="source_no" label="Source No." width="100px" align="center"> </el-table-column>
            <el-table-column prop="dataset" label="Source Dataset" align="center"> </el-table-column>
        </el-table>
        <div class="TableItemBody">
            <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="queryInfo.page"
                :page-sizes="[10, 20, 30, 50]"
                :page-size="queryInfo.page_size"
                layout="total, sizes, prev, pager, next"
                :total="count"
                background
            >
            </el-pagination>
        </div>
    </div>
</template>

<script>
import { marker_summary_list, marker_summary_download } from '@/api/api'
export default {
    props: {
        selectValue: {
            type: Object,
            default: () => {},
            required: true
        }
    },
    data() {
        return {
            searchVal: '',
            searchValue: '',
            currentPage4: 4,
            tableData: [],
            queryInfo: {
                page: 1,
                page_size: 10
            },
            count: 0,
            loading: false,
            loadingButton: false,
            baseUrl: process.env.VUE_APP_BASE_URL
        }
    },
    methods: {
        goMarkerCell(val) {
            this.$router.push({
                path: '/markerCell',
                query: {
                    gene_id: val,
                    species_name: this.selectValue.root
                }
            })
        },
        keydown(e) {
            this.searchValue = this.searchVal
            this.queryInfo.page = 1
            this.queryInfo.page_size = 10
            this.getTable(this.selectValue)
        },
        getTable(item) {
            let infoData = {
                species_name: item.root
            }
            if (item.level > 1) {
                infoData.tissue_name = item.parent
            }
            if (item.level > 2) {
                infoData.cell_name = item.name
            }
            this.loading = true
            marker_summary_list({
                ...infoData,
                ...this.queryInfo,
                search_gene: this.searchValue
            })
                .then((res) => {
                    if (res.code === 200) {
                        this.count = res.data.count
                        this.tableData = res.data.results
                    } else {
                        this.tableData = []
                    }
                    this.loading = false
                })
                .catch((err) => {
                    this.tableData = []
                    this.loading = false
                })
        },
        getDownload() {
            let url = `${this.baseUrl}/api/v1/marker_summary_list/marker_summary_download?species_name=${this.selectValue.root}&tissue_name=${this.selectValue.parent}&search_gene=${this.searchValue}`
            if (this.selectValue.level > 2) {
                url = url + `&cell_name=${this.selectValue.name}`
            }
            window.open(url)
    
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
        handleSizeChange(val) {
            this.queryInfo.page = 1
            this.queryInfo.page_size = val
            this.getTable(this.selectValue)
        },
        handleCurrentChange(val) {
            this.queryInfo.page = val
            this.getTable(this.selectValue)
        }
    },
    watch: {
        selectValue: {
            handler(newVal) {
                this.queryInfo.page = 1
                this.getTable(newVal)

                console.log(newVal)
            },
            deep: true,
            immediate: true
        }
    }
}
</script>

<style scoped lang="scss">
.tableItem {
    width: 100%;
    height: auto;
    padding: 12px 0;
    box-sizing: border-box;
    .TableItemHeader {
        width: 100%;
        height: 40px;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
    .TableItemBody {
        height: 50px;
        width: 100%;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
    .tableItemTableIcon {
        font-size: 30px;
    }
    .tableItemTableIconActive {
        color: #f7af04;
        font-size: 38px;
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

.TableItemHeader .el-button--success {
    background: #24a461;
}
</style>
