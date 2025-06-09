<template>
    <div class="tableItem">
        <div class="TableItemHeader">
            <div class="TableItemHeader-left">
                <span>Pct Diff</span>
                <el-slider
                    v-model="pctVlaue"
                    :step="pctStep"
                    :format-tooltip="formatTooltipPct"
                    range
                    show-stops
                    style="width: 120px; margin-right: 50px"
                    :min="pctRange.min"
                    :max="pctRange.max"
                    input-size="mini"
                    @change="changeSlider"
                ></el-slider>
                <span>Avg log2FC</span>
                <el-slider
                    v-model="avgValue"
                    :step="avgStep"
                    :format-tooltip="formatTooltipPct"
                    range
                    show-stops
                    style="width: 120px"
                    :min="avgRange.min"
                    :max="avgRange.max"
                    input-size="mini"
                    @change="changeSlider"
                ></el-slider>
            </div>
            <div class="TableItemHeader-right">
                <el-input v-model="searchVal" placeholder="Search.." @keyup.enter.native="keydown" style="width: 210px; margin-right: 10px" suffix-icon="el-icon-search"></el-input>
                <el-button icon="el-icon-download" type="success">
                    <span style="font-size: 12px" :loading="loadingButton" @click="getDownload">CSV</span>
                </el-button>
            </div>
        </div>
        <el-table :data="tableData" style="width: 100%" v-loading="loading" height="680px">
            <el-table-column prop="gene" label="Gene ID" width="120px">
                <template slot-scope="scope">
                    <span style="color: #24a461; text-decoration: underline; cursor: pointer; font-size: 12px" @click="goMarkerCell(scope.row.gene)">{{ scope.row.gene }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="name" label="Gene Name" width="120px"> </el-table-column>
            <el-table-column prop="p_val" label="p value" width="120px"> </el-table-column>
            <el-table-column prop="p_val_adj" label="p adj" width="120px"> </el-table-column>
            <el-table-column prop="pct_1" label="Pct 1" width="120px"> </el-table-column>
            <el-table-column prop="pct_2" label="Pct 2" width="120px"> </el-table-column>
            <el-table-column prop="pct_diff" label="Pct diff" width="120px"> </el-table-column>
            <el-table-column prop="avg_log2FC" label="Avg log2FC" width="120px"> </el-table-column>
            <el-table-column prop="celltype_id" label="Celltype" width="220px"> </el-table-column>
            <el-table-column prop="celltype_id" label="Celltype" width="220px"> </el-table-column>
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
import { marker_details_list, marker_details_download, marker_details_search_data } from '@/api/api'
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
            pctVlaue: [0, 0],
            avgValue: [0, 0],
            pctRange: {},
            avgRange: {},
            pctStep: 1,
            avgStep: 1,
            baseUrl: process.env.VUE_APP_BASE_URL
        }
    },
    async created() {
        // await this.getMinMax()
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
        async getMinMax(item) {
            let result = await marker_details_search_data({
                species_name: item.root
            })
            if (result.code == 200) {
                this.pctRange = result.data.pct_diff
                this.pctVlaue = [result.data.pct_diff.min, result.data.pct_diff.max]
                this.pctStep = (result.data.pct_diff.max - result.data.pct_diff.min) / 100
                this.avgRange = result.data.avg_log2FC
                this.avgValue = [result.data.avg_log2FC.min, result.data.avg_log2FC.max]
                this.avgStep = (result.data.avg_log2FC.max - result.data.avg_log2FC.min) / 100
            }
        },
        formatTooltipPct(val) {
            if (val) {
                return Number(val.toFixed(4))
            } else {
                return val
            }
        },
        keydown(e) {
            this.searchValue = this.searchVal
            this.queryInfo.page = 1
            this.queryInfo.page_size = 10
            this.getTable(this.selectValue)
        },
        changeSlider() {
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
            marker_details_list({
                ...infoData,
                ...this.queryInfo,
                search_gene: this.searchValue,
                pct_diff_min: this.pctVlaue[0],
                pct_diff_max: this.pctVlaue[1],
                avg_log2FC_min: this.avgValue[0],
                avg_log2FC_max: this.avgValue[1]
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
            let url = `${this.baseUrl}/api/v1/marker_details_list/marker_details_download?species_name=${this.selectValue.root}&tissue_name=${this.selectValue.parent}&search_gene=${this.searchValue}&pct_diff_min=${this.pctVlaue[0]}&pct_diff_max=${this.pctVlaue[1]}&avg_log2FC_min=${this.avgValue[0]}&avg_log2FC_max=${this.avgValue[1]}&page=${this.queryInfo.page}&page_size=${this.queryInfo.page_size}`
            if (this.selectValue.level > 2) {
                url = url + `&cell_name=${this.selectValue.name}`
            }
            let fileName = new Date().getTime() + '.csv'
            const a = document.createElement('a')
            a.href = url
            a.download = fileName
            a.target = '_blank'
            a.style.display = 'none'
            document.body.appendChild(a)
            a.click()
            document.body.removeChild(a)
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
            async handler(newVal) {
                this.queryInfo.page = 1
                await this.getMinMax(newVal)
                this.getTable(newVal)
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
        justify-content: space-between;
        align-items: center;
        .TableItemHeader-left {
            display: flex;
            font-size: 14px;
            align-items: center;
            span {
                margin-right: 20px;
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
.TableItemHeader-left {
    .el-slider__stop {
        background: #e4e7ed;
    }
    .el-slider__bar {
        background: #409eff;
    }
    .el-slider__button {
        border-color: #409eff;
        width: 12px;
        height: 12px;
    }
}
.TableItemHeader-right .el-button--success {
    background: #24a461;
}
</style>
