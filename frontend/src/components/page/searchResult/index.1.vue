<template>
    <div class="searchResult">
        <!-- <div class="crumbs">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item v-if="$route.query.from =='search'" :to="{ path: '/search' }">Search</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/homePage' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>Search result</el-breadcrumb-item>
      </el-breadcrumb>
    </div> -->
        <!-- <p class="title1">Statistical graph of cell markers</p> -->
        <div class="search-inner" v-loading="chartLoading">
            <!-- <div style="margin-bottom:10px;">
        <el-radio-group v-model="firstRadio" @change="firstRadioClick">
          <el-radio label="Static">Static UMAP</el-radio>
          <el-radio label="Interactive">Interactive UMAP</el-radio>
        </el-radio-group>
        <span style="font-size: 16px;color: #333;padding-left:40px;">*Interactive plot is based on sampled data(500 per cell type).</span>
      </div>
      <el-form :inline="true" :model="formInline" class="demo-form-inline" size="large">
        <el-form-item label="Gene">
          <el-input v-model="formInline.gene_id"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="firstGeneGo">GO</el-button>
        </el-form-item>
      </el-form> -->
            <!-- 图表 -->
            <!-- <el-form ref="form1" :inline="true">
        <el-form-item label="Metadata">
          <el-select size="large" @change="resourceChange" v-model="marker_resource" placeholder="Choose">
            <el-option v-for="(item, index) in resourceOptions" :key="index" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="">
          <el-button type="primary" size="large" @click="search">GO</el-button>
        </el-form-item>
      </el-form> -->
            <p class="title_text">{{ title_text }}</p>
            <el-row :gutter="20">
                <el-col :span="12">
                    <div class="homepage_img_left" v-loading="chartLoading1" v-show="isShow">
                        <div ref="barChart1" :style="{ width: '100%', height: '100%' }"></div>
                    </div>
                    <div class="homepage_img_left" v-show="!isShow">
                        <div style="width: 100%; height: 512px; overflow: hidden; line-height: 512px; font-size: 12px; color: #999; text-align: center" v-loading="chartLoading1">No data</div>
                    </div>
                </el-col>
                <el-col :span="12">
                    <div class="homepage_img_left" v-loading="chartLoading1" v-show="isShow">
                        <div ref="barChart1_2" :style="{ width: '100%', height: '100%' }"></div>
                    </div>
                    <div class="homepage_img_left" v-show="!isShow">
                        <div style="width: 100%; height: 512px; overflow: hidden; line-height: 512px; font-size: 12px; color: #999; text-align: center" v-loading="chartLoading1">No data</div>
                    </div>
                </el-col>
            </el-row>

            <!-- <div style="margin-bottom:10px;">
        <el-radio-group v-model="secondRadio" @change="secondRadioClick">
          <el-radio label="Overview">Overview</el-radio>
          <el-radio label="Expression">Cell Type Expression</el-radio>
        </el-radio-group>
      </div>
      <el-form :inline="true" :model="secondForm" class="demo-form-inline" size="large">
        <el-form-item label="Gene">
          <el-input v-model="secondForm.gene_id"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="secondGeneGo">GO</el-button>
        </el-form-item>
      </el-form>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="homepage_img_left" v-loading="chartLoading2">
            <div ref='barChart3' :style="{width:'100%',height: '100%'}"></div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="homepage_img_left" v-loading="chartLoading2">
            <div ref='barChart3' :style="{width:'100%',height: '100%'}"></div>
          </div>
        </el-col>
      </el-row> -->
        </div>
        <!-- <p class="title1">Results</p> -->
        <div class="search-inner">
            <!-- 表格 -->
            <div style="margin-bottom: 10px">
                <!-- <i class="pointer" style="color:#24A461;float:right;cursor:pointer;text-decoration:underline;" @click="download('txt')">Export Table</i> -->
                <el-radio-group v-model="radio" @change="radioClick">
                    <el-radio :label="1">Cell Type</el-radio>
                    <!-- <el-radio :label="2">Feature Gene</el-radio>
          <el-radio :label="3">Gene Exp</el-radio>
          <el-radio :label="4">Cell Type Freq</el-radio> -->
                    <el-radio :label="5">Cluster Marker</el-radio>
                    <el-radio :label="6">Sample</el-radio>
                </el-radio-group>
            </div>
            <el-table
                v-if="radio == '1'"
                size="small"
                :data="tableData"
                :header-cell-style="headerStyle"
                v-loading="loading"
                element-loading-text="running"
                :cell-style="cellstyle"
                border
                style="width: 100%"
            >
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
                        <div v-if="item.label == 'Cell Marker'">
                            <span
                                v-for="(gene_id, geneIndex) in scope.row[item.key]"
                                style="display: inline-block; border: 1px solid #ccc; padding: 0 4px; margin: 2px; background: #f1f3f9"
                                :key="geneIndex"
                                >{{ gene_id }}</span
                            >
                        </div>
                        <span v-else>{{ scope.row[item.key] }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="DOI" prop="doi" align="center" width="90">
                    <template slot-scope="scope">
                        <el-popover placement="top" trigger="hover" :content="scope.row.doi">
                            <span v-if="scope.row.doi != ''" slot="reference" class="litClass" @click="jumpLink(scope.row.doi)">
                                <i class="el-icon-document" style="font-size: 16px"></i>
                            </span>
                        </el-popover>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
                v-if="radio == '1'"
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
            <el-table
                v-if="radio == '5'"
                size="small"
                :data="tableData"
                :header-cell-style="headerStyle"
                v-loading="loading"
                element-loading-text="running"
                :cell-style="cellstyle"
                @cell-click="handlecell"
                border
                style="width: 100%"
            >
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
                        <span>{{ scope.row[item.key] }}</span>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
                v-if="radio == '5'"
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
            <el-table
                v-if="radio == '6'"
                size="small"
                :data="tableData"
                :header-cell-style="headerStyle"
                v-loading="loading"
                element-loading-text="running"
                :cell-style="cellstyle"
                border
                style="width: 100%"
            >
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
                <el-table-column label="DOI" prop="lit_id" align="center" width="90">
                    <template slot-scope="scope">
                        <span v-for="(item, index) in scope.row.lit_id" :key="index">
                            <el-popover placement="top" trigger="hover" :content="item.label">
                                <!-- <span slot="reference">{{ `${scope.row[item.key].toString().trim().slice(0,showLen)}...` }}</span> -->
                                <span slot="reference" class="litClass" @click="jumpLink(item.label)">
                                    <i class="el-icon-document" style="font-size: 16px"></i>
                                </span>
                            </el-popover>
                            <!-- <span v-if="/^(10\.|DOI:)/.test(item)" style="float:left;width:50%;">{{item}}</span> -->
                        </span>
                    </template>
                </el-table-column>
                <el-table-column label="Sam ID" prop="sam_id" align="center" width="90">
                    <template slot-scope="scope">
                        <div>
                            <span>{{ scope.row.sam_id }}</span>
                        </div>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
                v-if="radio == '6'"
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
            <!-- <jg-table ref="searchReslut_table" v-if="radio == '1' || radio == '5'|| radio == '6'" :tableData="tableData" :column='column'
        :loading='loading' :cellstyle="cellstyle" :paginationConfig="paginationConfig" @handleCurrentChange="handleCurrentChange"
        @handleSizeChange="handleSizeChange" @handlecell='handlecell'></jg-table> -->
            <div v-show="radio == '2' || radio == '3' || radio == '4'" class="homepage_img_left">
                <!-- <div ref='barChart2' style="width:100%;height: 100%;"></div> -->
            </div>
        </div>
    </div>
</template>

<script>
import echarts from 'echarts'
import { option1, option2, option1_2, optionBar } from './config'
import { cell_search, cell_search_marker, search_marker, page_search_heat_map, all_search_heat_map } from '@/api/search'
import { umap_expression, plant_atlas_list } from '@/api/api'
import jgTable from '@/components/jgTable/index'

export default {
    name: 'searchResult',
    components: {
        jgTable
    },
    data() {
        return {
            firstRadio: 'Static',
            formInline: {
                gene_id: ''
            },
            secondForm: {
                gene_id: ''
            },
            secondRadio: 'Overview',
            chartLoading1: false,
            chartLoading2: false,
            isShow: true,
            marker_resource: 'Clusters',
            resourceOptions: [
                {
                    label: 'Clusters',
                    value: 'Clusters'
                },
                {
                    label: 'Project ID',
                    value: 'Project_ID'
                },
                {
                    label: 'Sample ID',
                    value: 'Sample_ID'
                }
            ],
            chartLoading: false,
            // tableHeight: (window.innerHeight - 416),
            tableData: [],
            column: [],
            cell_type_column: [
                { key: 'clusters', label: 'Cluster ID', width: 100 },
                { key: 'cluster_name', label: 'Cluster Name', width: 300 },
                // { key: 'cell_name', label: 'Cell Name' },
                { key: 'cell_po', label: 'Cell PO' },
                { key: 'tissue_po', label: 'Tissue PO', width: 160 },
                // { key: 'tissue_id', label: 'Tissue Name', width: 120 },
                // { key: 'po_num', label: 'PO Num', width: 120 },
                { key: 'gene_id_arr', label: 'Cell Marker', width: 250 }
                // { key: 'doi', label: 'DOI' },
                // { key: 'species_name', label: 'Species name' },
                // { key: 'tissue_id', label: 'Tissue ID' },
                // { key: 'cell_id', label: 'Cell ID' },
                // { key: 'gene_symbol', label: 'Gene symbol' },
                // { key: 'gene_id', label: 'Gene ID' },
                // { key: 'gene_id_other', label: 'Gene ID Other' },
                // { key: 'lit_id', label: 'Publication' },
                // { key: 'source_id', label: 'Source ID' },
            ],
            marker_column: [
                { key: 'cluster_id', label: 'Cluster ID', width: 100, align: 'center' },
                { key: 'gene_id', label: 'Gene ID' },
                { key: 'cell_type', label: 'Cell Type' },
                { key: 'pct1', label: 'pct1', width: 100 },
                { key: 'pct2', label: 'pct2', width: 100 },
                { key: 'log_2fc', label: 'Log2FC', width: 200 },
                { key: 'p_va1', label: 'P val', width: 200 },
                { key: 'p_val_adj', label: 'P val adj', width: 200 }
            ],
            sample_colum: [
                { key: 'species_name', label: 'Species name' },
                { key: 'sample_id', label: 'Sample ID' },
                { key: 'project_id', label: 'Project ID' },
                { key: 'sample_type', label: 'Sample type' },
                { key: 'tissue', label: 'Tissue' },
                { key: 'chemistry', label: 'Chemistry' }
                // { key: 'doi', label: 'DOI' },
                // { key: 'sam_id', label: 'Sam ID' },
            ],
            paginationConfig: {
                page: 1,
                size: 10,
                sizes: [10, 20, 30],
                total: 0
            },
            loading: false,
            radio: 1,
            option1,
            option1_2,
            option2,
            optionBar,
            table_type: 'cell_type',
            headerStyle: {
                color: '#fff',
                fontSize: '14px',
                background: '#24A461',
                fontFamily: 'Source Han Sans CN'
            },
            title_text: ''
        }
    },
    mounted() {
        // if (this.$route.query.marker_resource != '' && this.$route.query.marker_resource != undefined) {
        //   this.marker_resource = this.$route.query.marker_resource
        // }
        this.column = this.cell_type_column
        this.getTableData(this.table_type)
        this.showEcharts()
        this.showBarEcharts()
    },
    // updated() {
    //   this.$refs.searchReslut_table.$refs.jgTable.doLayout()
    // },
    methods: {
        search() {
            this.showEcharts()
        },
        resourceChange(val) {},
        showEcharts() {
            this.chartLoading1 = true
            let barChart1 = this.$refs.barChart1
            let barChart1_2 = this.$refs.barChart1_2
            let params = {
                tissue: this.$route.query.Tissue,
                species_name: this.$route.query.name,
                mata_data_type: this.marker_resource
            }
            umap_expression(params).then((res) => {
                if (res.code == 200) {
                    if (res.data.clusters_data) {
                        this.isShow = true
                        if (barChart1) {
                            let selfName = ''
                            if (this.$route.query.name == 'Populus') {
                                selfName = 'Populus alba'
                            } else if (this.$route.query.name == 'Nicotiana_tabacum') {
                                selfName = 'Nicotiana attenuate'
                            } else {
                                selfName = this.$route.query.name.replace(/_/g, ' ')
                            }
                            // this.option1.title.text = `${selfName} ${this.$route.query.Tissue} (${this.$route.query.sample_count} samples, ${this.$route.query.cell_count} cells)`
                            this.title_text = `${selfName} ${this.$route.query.Tissue} (${this.$route.query.sample_count} samples, ${this.$route.query.cell_count} cells)`
                            this.option1.legend.data = []
                            this.option1.series = []
                            res.data.clusters_data.forEach((item) => {
                                this.option1.legend.data.push(item.sort.toString())
                                this.option1.series.push({
                                    symbolSize: 2,
                                    name: item.sort.toString(),
                                    type: 'scatter',
                                    data: item.data
                                })
                            })
                            this.option1_2.legend.data = []
                            this.option1_2.series = []
                            res.data.cell_type_data.forEach((item) => {
                                this.option1_2.legend.data.push(item.name)
                                this.option1_2.series.push({
                                    symbolSize: 2,
                                    name: item.name,
                                    type: 'scatter',
                                    data: item.data
                                })
                            })
                        }
                    } else {
                        this.isShow = false
                    }
                    this.Echarts = echarts.init(barChart1)
                    this.Echarts_2 = echarts.init(barChart1_2)
                    this.Echarts.setOption(this.option1, true)
                    this.Echarts_2.setOption(this.option1_2, true)
                    this.chartLoading1 = false
                }
            })
        },
        showBarEcharts() {
            this.chartLoading2 = true
            let barChart3 = this.$refs.barChart3
            let params = {
                tissue: this.$route.query.Tissue,
                species_name: this.$route.query.name,
                mata_data_type: this.marker_resource
            }
            umap_expression(params).then((res) => {
                if (res.code == 200) {
                    if (res.data.clusters_data) {
                        this.isShow = true
                        if (barChart3) {
                            let selfName = ''
                            if (this.$route.query.name == 'Populus') {
                                selfName = 'Populus alba'
                            } else if (this.$route.query.name == 'Nicotiana_tabacum') {
                                selfName = 'Nicotiana attenuate'
                            } else {
                                selfName = this.$route.query.name.replace(/_/g, ' ')
                            }
                            this.option1.title.text = `${selfName} ${this.$route.query.Tissue} (${this.$route.query.sample_count} samples, ${this.$route.query.cell_count} cells)`
                            this.option1.legend.data = []
                            this.option1.series = []
                            res.data.clusters_data.forEach((item) => {
                                this.option1.legend.data.push(item.name)
                                this.option1.series.push({
                                    symbolSize: 2,
                                    name: item.name,
                                    type: 'scatter',
                                    data: item.data
                                })
                            })
                        }
                    } else {
                        this.isShow = false
                    }
                    this.Echarts = echarts.init(barChart3)
                    this.Echarts.setOption(this.optionBar, true)
                    this.chartLoading2 = false
                }
            })
        },
        firstRadioClick(val) {
            if (val == 'Static') {
            } else {
            }
        },
        secondRadioClick(val) {
            if (val == 'Overview') {
            } else {
            }
        },
        firstGeneGo() {},
        secondGeneGo() {},
        radioClick(val) {
            this.paginationConfig.page = 1
            if (val == 1) {
                this.table_type = 'cell_type'
                this.column = this.cell_type_column
                this.getTableData(this.table_type)
            } else if (val == 2) {
                let barChart2 = this.$refs.barChart2
                this.Echarts = echarts.init(barChart2)
                this.Echarts.setOption(this.option2, true)
            } else if (val == 5) {
                this.table_type = 'marker'
                this.column = this.marker_column
                this.getTableData(this.table_type)
            } else if (val == 6) {
                this.table_type = 'sample'
                this.column = this.sample_colum
                this.getTableData(this.table_type)
            }
        },
        getTableData(type) {
            this.loading = true
            plant_atlas_list({
                tag_list_type: type,
                species_name: this.$route.query.name,
                tissue: this.$route.query.Tissue,
                page: this.paginationConfig.page,
                page_size: this.paginationConfig.size
            }).then((res) => {
                if (res.code == 200) {
                    this.tableData = res.data.results
                    // if (type == 'sample') {
                    //   this.tableData.forEach(items => {
                    //     items.doi = ''
                    //     items.lit_id.forEach(item => {
                    //       items.doi = items.doi + ' ' + item.value
                    //     })
                    //   })
                    // }
                    if (type == 'cell_type') {
                        this.tableData.forEach((item) => {
                            // item.gene_id = item.gene_id.replace(/,/g, '  ')
                            if (item.gene_id != '') {
                                item.gene_id_arr = item.gene_id.split(',')
                            }
                            item.cell_po = item.cell_po ? `${item.cell_name} - ${item.cell_po}` : item.cell_name
                            item.tissue_po = item.po_num ? `${item.tissue_id} - ${item.po_num}` : item.tissue_id
                        })
                    }

                    this.paginationConfig.total = res.data.count
                    this.loading = false
                }
            })
        },
        handleCurrentChange(val) {
            this.paginationConfig.page = val
            this.getTableData(this.table_type)
        },
        handleSizeChange(val) {
            this.paginationConfig.page = 1
            this.paginationConfig.size = val
            this.getTableData(this.table_type)
        },
        cellstyle({ row, column, rowIndex, columnIndex }) {
            if (column.label === 'DOI') {
                return { color: '#0a9daa', cursor: 'pointer' }
            }
            return { fontSize: '14px' }
        },
        handlecell(row, col) {
            if (col.label == 'DOI') {
                window.open(`${row.doi}`, '_blank')
            }
        },
        // handlecell(params) {
        //   console.log(222, params)
        //   if (params.col.label == 'DOI') {
        //     window.open(`${params.row.doi}`, '_blank')
        //   }
        //   // if (params.col.label == 'PMID') {
        //   //   window.open(`https://pubmed.ncbi.nlm.nih.gov/${params.row.pmid}/`, '_blank')
        //   // } else if (params.col.label == 'Gene ID' || params.col.label == 'Gene Name') {
        //   //   sessionStorage.removeItem("searchResultQuery");
        //   //   sessionStorage.setItem("searchResultQuery", JSON.stringify(this.$route.query));
        //   //   this.$router.push({
        //   //     path: '/searchDetails',
        //   //     query: {
        //   //       from: this.$route.query.from,
        //   //       id: params.row.id,
        //   //       gene_id: params.row.gene_id
        //   //     }
        //   //   })
        //   // }
        // },
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
        jumpLink(url) {
            window.open(url, '_blank')
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
    width: 100%;
    height: 100%;
    margin: 0 auto;
    background: #fff;
    // padding: 0 0 30px 0;
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
    .title_text {
        font-weight: 400;
        color: #666666;
        font-size: 24px;
        text-align: center;
    }
    .search-inner {
        width: 1200px;
        padding: 20px;
        margin: 0 auto;
        overflow: hidden;
        background: rgba(255, 255, 255, 1);
        .demo-form-inline {
            margin-top: 20px;
        }
        .homepage_img_left {
            width: 100%;
            height: 564px;
            position: relative;
        }
        .litClass {
            cursor: pointer;
            display: inline-block;
            width: 50%;
            color: #0a9daa;
            text-decoration: underline;
            text-align: center;
        }
    }
}
</style>
