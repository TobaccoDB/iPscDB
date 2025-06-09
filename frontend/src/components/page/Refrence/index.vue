<template>
    <div class="Refrence">
        <div class="crumbs">
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-breadcrumb-item :to="{ path: '/cellIdentification' }">Cell Identification</el-breadcrumb-item>
                <el-breadcrumb-item>Refrence</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="Refrence-inner" :style="{ minHeight: contentHeight }" v-loading="goLoading" element-loading-text="loading" element-loading-background="#fff">
            <p class="topTitle">{{ detailData.title }}</p>
            <p class="topSecondTitle">Overview</p>
            <div class="titleContent">
                <div class="imgCon"><img :src="detailData.cell_identification_pdf[0]" /></div>
                <ul class="formCon">
                    <li>Species：{{ detailData.species_name_down }}</li>
                    <li>Cells in Reference：{{ detailData.cells_reference }}</li>
                    <li>PMID：{{ detailData.pmid }}</li>
                    <li>
                        DOI：
                        <span style="color: #0a9daa; cursor: pointer" v-for="(item, index) in detailData.doi.split(',')" :key="index" @click="jumpPMIDDIO(item)">{{ item }} </span>
                    </li>
                    <!-- <li>Data Type：{{detailData.data_type}}</li> -->
                </ul>
            </div>
            <el-table
                size="small"
                :data="tableData"
                :header-cell-style="headerStyle"
                :header-cell-class-name="cellClass"
                v-loading="loading"
                element-loading-text="running"
                :cell-style="cellstyle"
                @cell-click="handlecell"
                border
                style="width: 100%"
            >
                <el-table-column type="index" width="55" align="center"> </el-table-column>
                <el-table-column
                    v-for="(item, index) in column"
                    :key="index"
                    :label="item.label"
                    :width="item.width"
                    :align="item.align === undefined ? 'center' : item.align"
                    :fixed="item.fixed === undefined ? false : item.fixed"
                    :sortable="item.sortable === undefined ? false : item.sortable"
                    :prop="item.key"
                >
                    <template slot-scope="scope">
                        <span v-if="item.label == 'Sample ID' && scope.row['is_sample_rds'] == '1'"
                            >{{ scope.row[item.key] }}
                            <i class="downloadIcon" @click="rdsDownload(scope.row.sample_id)"></i>
                        </span>
                        <span v-else-if="item.label == 'Process Status' && scope.row[item.key] == 'QC Fail'" class="statusSpan1">{{ scope.row[item.key] }} </span>
                        <span v-else-if="item.label == 'Process Status' && scope.row[item.key] == 'QC Pass'" class="statusSpan2">{{ scope.row[item.key] }} </span>
                        <span v-else-if="item.label == 'Process Status' && scope.row[item.key] == 'under process'" class="statusSpan3">{{ scope.row[item.key] }} </span>
                        <span v-else>{{ scope.row[item.key] }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="Publication" prop="lit_id" align="center" width="120">
                    <template slot-scope="scope">
                        <span v-for="(item, index) in scope.row.lit_id" :key="index">
                            <!-- <span v-if="/^(10\.|DOI:)/.test(item)" style="float:left;width:50%;">{{item}}</span> -->
                            <el-popover placement="top" trigger="hover" :content="item.label.toString()">
                                <!-- <span slot="reference">{{ `${scope.row[item.key].toString().trim().slice(0,showLen)}...` }}</span> -->
                                <span slot="reference" class="litClass" @click="jumpLink(item.label)">
                                    <i class="el-icon-document" style="font-size: 16px; color: #0a9daa"></i>
                                </span>
                            </el-popover>
                            <!-- <span class="litClass" @click="jumpLink(item.value)">
                <i class="el-icon-document"></i>
              </span> -->
                        </span>
                    </template>
                </el-table-column>
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
        </div>
    </div>
</template>

<script>
import jgTable from '@/components/jgTable/index'
import { cell_identification_reference_detail, cell_identification_reference_sample } from '@/api/api'
export default {
    name: 'Refrence',
    components: {
        jgTable
    },
    data() {
        return {
            contentHeight: window.innerHeight - 330 + 'px',
            goLoading: false,
            // listItem: [
            //   {
            //     title: "Arabidopsis thaliana -  Root tip",
            //     img: require("@/assets/img/LT5.png"),
            //     id: 'LT5'
            //   },
            //   {
            //     title: "Arabidopsis thaliana - Leaf",
            //     img: require("@/assets/img/LT9LT29.png"),
            //     id: 'LT9LT29'
            //   },
            //   {
            //     title: "Arabidopsis thaliana - Shoot apex",
            //     img: require("@/assets/img/LT11.png"),
            //     id: 'LT11'
            //   },
            //   {
            //     title: "Arabidopsis thaliana - Root",
            //     img: require("@/assets/img/LT24.png"),
            //     id: 'LT24'
            //   },
            //   {
            //     title: "Oryza sativa - Root",
            //     img: require("@/assets/img/LT30.png"),
            //     id: 'LT30'
            //   },
            //   {
            //     title: "Oryza sativa - Leaf",
            //     img: require("@/assets/img/LT32.png"),
            //     id: 'LT32'
            //   },
            //   {
            //     title: "Zea mays - Leaf",
            //     img: require("@/assets/img/LT34.png"),
            //     id: 'LT34'
            //   },
            //   {
            //     title: "Zea mays - Ear",
            //     img: require("@/assets/img/LT35.png"),
            //     id: 'LT35'
            //   },
            //   {
            //     title: "Nicotiana abacum - Flower",
            //     img: require("@/assets/img/LT39.png"),
            //     id: 'LT39'
            //   },
            //   {
            //     title: "Populus - Stem",
            //     img: require("@/assets/img/LT40.png"),
            //     id: 'LT40'
            //   }
            // ],
            detailData: {
                cells_reference: '',
                data_type: '',
                doi: '',
                pmid: '',
                species_name: ''
            },
            tableData: [],
            column: [
                { key: 'species_name', label: 'Specie Name', width: 200 },
                { key: 'project_id', label: 'Project ID', width: 150 },
                { key: 'sample_id', label: 'Sample ID', width: 180 },
                { key: 'tissue', label: 'Tissue', width: 100 },
                { key: 'process_status', label: 'Process Status', width: 150 },
                { key: 'sample_name', label: 'Sample Name', width: 260 },
                { key: 'geno_type', label: 'Genotype', width: 150 },
                { key: 'treament', label: 'Treament', width: 200 },
                { key: 'ecotype', label: 'Ecotype', width: 250 },
                { key: 'age', label: 'Age', width: 100 },
                { key: 'chemistry', label: 'Chemistry', width: 100 }
            ],
            paginationConfig: {
                page: 1,
                size: 10,
                sizes: [10, 20, 30],
                total: 0
            },
            loading: false,
            headerStyle: {
                color: '#fff',
                fontSize: '14px',
                background: '#24A461',
                fontFamily: 'Source Han Sans CN'
            }
        }
    },
    mounted() {
        this.init()
        this.getTableData()
    },
    methods: {
        init() {
            let params = {
                lit_id: this.$route.query.lit_id
            }
            this.goLoading = true
            cell_identification_reference_detail(params).then((res) => {
                if (res.code == 200) {
                    this.detailData = res.data.results[0]
                    this.goLoading = false
                }
            })
        },
        jumpPMIDDIO(id) {
            window.open(`${id}`, '_blank')
        },
        // 表格部分
        getTableData() {
            this.loading = true
            cell_identification_reference_sample({
                project_id: this.$route.query.project_id,
                page: this.paginationConfig.page,
                page_size: this.paginationConfig.size
            }).then((res) => {
                if (res.code == 200) {
                    this.tableData = res.data.results
                    this.paginationConfig.total = res.data.count
                    this.loading = false
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
        cellClass(row) {
            if (row.columnIndex === 0) {
                return 'DisableSelection'
            }
        },
        cellstyle({ row, column, rowIndex, columnIndex }) {
            // if (column.label === 'Lit ID') {
            //   return { color: "#0a9daa", cursor: "pointer" }
            // }
            return { fontSize: '14px' }
        },
        handlecell(row, col) {
            if (col.label == 'Lit ID') {
                // window.open(`https://pubmed.ncbi.nlm.nih.gov/${params.row.pmid}/`, '_blank')
            }
        },
        rdsDownload(sample_id) {
            this.jg_downloadFile('api/v1/plant_sample_rds_download/', {
                sample_id: sample_id
            })
        },
        jumpLink(url) {
            window.open(url, '_blank')
        }
    }
}
</script>
<style lang="scss" scoped>
@import './style.scss';
</style>
