<template>
    <div id="topAnchor" class="projectResult">
        <!-- <div class="crumbs">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item v-if="$route.query.from =='search'" :to="{ path: '/search' }">Search</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: '/homePage' }">Home</el-breadcrumb-item>
        <el-breadcrumb-item>Search result</el-breadcrumb-item>
      </el-breadcrumb>
    </div> -->
        <!-- <p class="title1">Statistical graph of cell markers</p> -->
        <div class="search-inner" v-loading="chartLoading">
            <div style="margin-bottom: 10px">
                <!-- <el-radio-group v-model="firstRadio" @change="firstRadioClick">
          <el-radio label="Static">Static UMAP</el-radio>
          <el-radio label="Interactive">Interactive UMAP</el-radio>
        </el-radio-group> -->
                <span style="font-size: 16px; color: #333">*Interactive plot is based on sampled data(500 per cell type).</span>
            </div>
            <el-form :inline="true" :model="formInline" class="demo-form-inline" size="large" v-if="firstRadio == 'Interactive'">
                <el-form-item label="View by">
                    <el-select size="large" v-model="formInline.type" @change="viewByChange" placeholder="Choose">
                        <el-option label="Cell type" value="Cell_type"></el-option>
                        <el-option v-if="$route.query.lit_id != 'LT68'" label="Cluster" value="Clusters"></el-option>
                        <el-option label="Sample" value="Project_ID"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="Gene">
                    <el-input clearable v-model="formInline.gene_id"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="firstGeneGo">GO</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="firstExample">Example</el-button>
                </el-form-item>
                <!-- <el-form-item style="float:right;">
          <el-button type="text" @click="downloadEcharts" style="color:#0a9daa;">
            <i class="el-icon-download el-icon--right"></i>Export Plot
          </el-button>
        </el-form-item> -->
            </el-form>
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
            <p class="title_text" v-show="firstRadio != 'Static'">{{ title_text }}</p>
            <el-row :gutter="20" v-show="firstRadio != 'Static'">
                <!-- <el-col :span="12">
          <div class="homepage_img_left" style="text-align:center;overflow:hidden;padding-top:32px;">
            <img style="max-width: 100%;max-height: 95%;margin-top:10px;" v-if="staticUrl" :src="staticUrl">
            <div style="width:100%;height:512px;overflow:hidden;line-height:512px;font-size:14px;color:#999;text-align:center;" v-if="!staticUrl">
              No data
            </div>
          </div>
        </el-col> -->
                <el-col :span="12">
                    <!-- <el-col :span="12" v-show="!formInline.gene_id"> -->
                    <div style="overflow: hidden">
                        <el-button type="text" @click="downloadEcharts" style="color: #0a9daa; float: right; margin-right: 20px">
                            <i class="el-icon-download el-icon--right"></i>Export Plot
                        </el-button>
                    </div>

                    <div class="homepage_img_left" v-loading="chartLoading1" v-show="isShow && firstRadio == 'Interactive'">
                        <div id="barChart1" ref="barChart1" style="width: 590px; height: 534px"></div>
                    </div>
                    <div class="homepage_img_left" v-show="!isShow && firstRadio == 'Interactive'">
                        <div style="width: 100%; height: 512px; overflow: hidden; line-height: 512px; font-size: 12px; color: #999; text-align: center" v-loading="chartLoading1">No data</div>
                    </div>
                </el-col>
                <el-col :span="12">
                    <!-- <el-col :span="12" v-show="formInline.gene_id"> -->
                    <div style="overflow: hidden">
                        <el-button type="text" @click="downloadEcharts1_2" style="color: #0a9daa; float: right; margin-right: 20px">
                            <i class="el-icon-download el-icon--right"></i>Export Plot
                        </el-button>
                    </div>
                    <div class="homepage_img_left" v-loading="chartLoading1" v-show="isShow && firstRadio == 'Interactive'">
                        <div id="barChart1_2" ref="barChart1_2" style="width: 590px; height: 534px"></div>
                    </div>
                    <div class="homepage_img_left" v-show="!isShow && firstRadio == 'Interactive'">
                        <div style="width: 100%; height: 512px; overflow: hidden; line-height: 512px; font-size: 12px; color: #999; text-align: center" v-loading="chartLoading1">No data</div>
                    </div>
                </el-col>
            </el-row>

            <div class="homepage_img_left" style="text-align: center" v-if="firstRadio == 'Static'">
                <img style="max-width: 100%; max-height: 95%; margin-top: 10px" v-if="staticUrl" :src="staticUrl" />
                <div style="width: 100%; height: 512px; overflow: hidden; line-height: 512px; font-size: 14px; color: #999; text-align: center" v-if="!staticUrl">No data</div>
            </div>

            <div style="margin: 10px 0">
                <el-radio-group v-model="secondRadio" @change="secondRadioClick">
                    <el-radio label="Overview">Overview</el-radio>
                    <el-radio label="Expression">Cell Type Expression</el-radio>
                </el-radio-group>
            </div>
            <el-form :inline="true" :model="secondForm" class="demo-form-inline" size="large" v-show="!isOverview">
                <el-form-item label="Gene">
                    <el-input clearable v-model="secondForm.gene_id"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="secondGeneGo">GO</el-button>
                </el-form-item>
            </el-form>
            <el-row :gutter="20" v-show="isOverview">
                <el-col :span="12">
                    <div class="homepage_img_left" v-loading="chartLoading2">
                        <img width="100%" :src="chart3Url" />
                    </div>
                </el-col>
                <el-col :span="12">
                    <div class="homepage_img_left" v-loading="chartLoading2">
                        <div ref="barChart3" :style="{ width: '100%', height: '100%' }"></div>
                    </div>
                </el-col>
            </el-row>
            <el-row :gutter="20" v-show="!isOverview">
                <el-col :span="24">
                    <div class="homepage_img_left" style="text-align: center" v-loading="chartLoading2">
                        <img style="max-width: 100%; max-height: 100%" :src="ExpressionUrl1" />
                        <div style="width: 100%; height: 512px; overflow: hidden; line-height: 512px; font-size: 14px; color: #999; text-align: center" v-if="!ExpressionUrl1">No data</div>
                    </div>
                </el-col>
                <el-col :span="24" v-if="ExpressionUrl2">
                    <div class="homepage_img_left" style="text-align: center" v-loading="chartLoading2">
                        <img style="max-width: 100%; max-height: 100%" :src="ExpressionUrl2" />
                    </div>
                </el-col>
            </el-row>
        </div>
        <!-- <p class="title1">Results</p> -->
        <div class="search-inner">
            <!-- 表格 -->
            <div style="margin-bottom: 10px">
                <!-- <i class="pointer" style="color:#24A461;float:right;cursor:pointer;text-decoration:underline;" @click="download('txt')">Export Table</i> -->
                <el-radio-group v-model="radio" @change="radioClick">
                    <el-radio :label="1">Cell Marker</el-radio>
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
                stripe
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
                        <div v-if="item.label == 'Published Cell Marker'">
                            <el-tooltip :content="gene_id.label" placement="top" effect="light" v-for="(gene_id, geneIndex) in scope.row[item.key]" :key="geneIndex">
                                <span @click="jumpTop(gene_id.name)" style="display: inline-block; border: 1px solid #ccc; padding: 0 4px; margin: 2px; background: #f1f3f9; cursor: pointer">
                                    <a style="color: #606266" href="#topAnchor">{{ gene_id.name }}</a>
                                </span>
                            </el-tooltip>
                        </div>
                        <span v-else>{{ scope.row[item.key] }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="Refrence" prop="doi" align="center" width="120">
                    <template slot-scope="scope">
                        <el-popover placement="top" trigger="hover" :content="item.label" v-for="(item, index) in scope.row.doi" :key="index">
                            <span v-if="item.label != ''" slot="reference" class="litClass" @click="jumpLink(item.label)">
                                <i class="el-icon-document" style="font-size: 16px; color: #0a9daa"></i>
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
                stripe
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
                stripe
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
                <el-table-column label="Refrence" prop="lit_id" align="center" width="90">
                    <template slot-scope="scope">
                        <span v-for="(item, index) in scope.row.lit_id" :key="index">
                            <el-popover placement="top" trigger="hover" :content="item.label">
                                <!-- <span slot="reference">{{ `${scope.row[item.key].toString().trim().slice(0,showLen)}...` }}</span> -->
                                <span slot="reference" class="litClass" @click="jumpLink(item.label)">
                                    <i class="el-icon-document" style="font-size: 16px; color: #0a9daa"></i>
                                </span>
                            </el-popover>
                            <!-- <span v-if="/^(10\.|DOI:)/.test(item)" style="float:left;width:50%;">{{item}}</span> -->
                        </span>
                    </template>
                </el-table-column>
                <el-table-column label="Process Status" prop="sam_id" align="center" width="130">
                    <template slot-scope="scope">
                        <!-- <div>
              <span>{{scope.row.sam_id}}</span>
            </div> -->
                        <span v-if="scope.row.process_status == 'QC Fail'" class="statusSpan1">{{ scope.row.process_status }} </span>
                        <span v-else-if="scope.row.process_status == 'QC Pass'" class="statusSpan2">{{ scope.row.process_status }} </span>
                        <span v-else-if="scope.row.process_status == 'under process'" class="statusSpan3">{{ scope.row.process_status }} </span>
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
            <!-- <jg-table ref="projectReslut_table" v-if="radio == '1' || radio == '5' || radio == '6'" :tableData="tableData" :column='column'
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
import { option1, option1_2, option2, optionBar } from './config'
import { cell_search, cell_search_marker, search_marker, page_search_heat_map, all_search_heat_map, project_static_umap_png } from '@/api/search'
import { project_umap_dataset, project_atlas_list, cluster_marker, sample_list, expressed_gene_cell_type_count, expressed_gene_violin_box_plot, expressed_gene_umap_dataset } from '@/api/api'
import jgTable from '@/components/jgTable/index'

export default {
    name: 'projectResult',
    components: {
        jgTable
    },
    data() {
        return {
            firstRadio: 'Interactive',
            formInline: {
                gene_id: '',
                type: 'Cell_type'
            },
            secondForm: {
                gene_id: 'AT1G12560'
            },
            secondRadio: 'Overview',
            isOverview: true,
            chart3Url: '',
            staticUrl: '',
            // staticUrl: require("@/assets/img/Static.png"),
            ExpressionUrl1: '',
            ExpressionUrl2: '',
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
                // { key: 'clusters', label: 'Cluster ID', width: 100 },
                { key: 'cluster_name', label: 'Cell Name', width: 200 },
                // { key: 'cell_name', label: 'Cell Name' },
                { key: 'cell_po', label: 'Cell PO' },
                { key: 'tissue_id', label: 'Tissue', width: 160 },
                { key: 'gene_id_arr', label: 'Published Cell Marker', width: 415 }
                // { key: 'doi', label: 'DOI' },
            ],
            marker_column: [
                { key: 'cluster_id', label: 'Cluster ID', width: 100 },
                { key: 'gene_id', label: 'Gene ID' },
                { key: 'cell_type', label: 'Cell Type' },
                { key: 'pct1', label: 'pct1', width: 100 },
                { key: 'pct2', label: 'pct2', width: 100 },
                { key: 'log_2fc', label: 'Log2FC' },
                { key: 'p_va1', label: 'P val' },
                { key: 'p_val_adj', label: 'P val adj' }
            ],
            sample_colum: [
                { key: 'species_name', label: 'Species name' },
                { key: 'sample_id', label: 'Sample ID' },
                { key: 'project_id', label: 'Project ID' },
                { key: 'sample_type', label: 'Sample type' },
                { key: 'tissue', label: 'Tissue', width: 100 },
                { key: 'chemistry', label: 'Platform' }
                // { key: 'lit_id', label: 'Publication' },
                // { key: 'sam_id', label: 'Sam ID', width: 100 },
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
            title_text: '',
            option1_2MinMax: []
        }
    },
    mounted() {
        // if (this.$route.query.marker_resource != '' && this.$route.query.marker_resource != undefined) {
        //   this.marker_resource = this.$route.query.marker_resource
        // }
        if (this.$route.query.species_name == 'Oryza_sativa') {
            this.secondForm.gene_id = 'Os01g0169900'
        } else if (this.$route.query.species_name == 'Zea_mays') {
            this.secondForm.gene_id = 'Zm00001d027266'
        } else if (this.$route.query.species_name == 'Nicotiana_tabacum') {
            this.secondForm.gene_id = 'ENSRNA050025876'
        } else if (this.$route.query.species_name == 'Popular_alba') {
            this.secondForm.gene_id = 'pal-pou40191'
        } else if (this.$route.query.species_name == 'Hybrid_poplar') {
            this.secondForm.gene_id = 'Potri.T178800'
        } else if (this.$route.query.species_name == 'Solanum_lycopersicum') {
            this.secondForm.gene_id = 'Solyc12g100130'
        } else if (this.$route.query.species_name == 'Fragaria_vesca') {
            this.secondForm.gene_id = 'FvH4-c3g00210'
        } else if (this.$route.query.species_name == 'Phalaenopsis_aphrodite') {
            this.secondForm.gene_id = 'PAXXG388540'
        } else {
            if (this.$route.query.project_id == 'GSM4423536') {
                this.secondForm.gene_id = 'AT1G27950'
            } else {
                this.secondForm.gene_id = 'AT1G12560'
            }
        }
        this.column = this.cell_type_column
        this.getTableData(this.table_type)
        this.firstExample()
        // this.showEcharts()
        this.showBarEcharts()
        this.showExpression()

        // project_static_umap_png({ lit_id: this.$route.query.lit_id, project_id: this.$route.query.project_id }).then(res => {
        //   if (res.code == 200) {
        //     this.staticUrl = res.data.project_static_umap_png
        //   }
        // });
    },
    // updated() {
    //   this.$refs.projectReslut_table.$refs.jgTable.doLayout()
    // },
    methods: {
        search() {
            this.showEcharts()
        },
        viewByChange(val) {
            this.showEcharts()
        },
        resourceChange(val) {},
        downloadEcharts() {
            const link = document.createElement('a')
            link.download = 'plot'
            link.style.display = 'none'
            let barChart1 = this.$refs.barChart1
            this.Echarts = echarts.init(barChart1)
            link.href = this.Echarts.getDataURL({
                type: 'png',
                pixelRatio: 1.5,
                backgroundColor: '#fff'
            }) // 导出图表图片，返回一个 base64 的 URL
            document.body.appendChild(link)
            link.click()
            URL.revokeObjectURL(link.href) //释放URL对象
        },
        downloadEcharts1_2() {
            const link = document.createElement('a')
            link.download = 'plot'
            link.style.display = 'none'
            let barChart1_2 = this.$refs.barChart1_2
            this.Echarts = echarts.init(barChart1_2)
            link.href = this.Echarts.getDataURL({
                type: 'png',
                pixelRatio: 1.5,
                backgroundColor: '#fff'
            }) // 导出图表图片，返回一个 base64 的 URL
            document.body.appendChild(link)
            link.click()
            URL.revokeObjectURL(link.href) //释放URL对象
        },
        showEcharts() {
            this.chartLoading1 = true
            let barChart1 = this.$refs.barChart1
            let barChart1_2 = this.$refs.barChart1_2
            let params = {
                species_name: this.$route.query.species_name,
                lit_id: this.$route.query.lit_id,
                gene_id: this.formInline.gene_id,
                umap_type: this.formInline.type,
                project_id: this.$route.query.project_id
            }
            expressed_gene_umap_dataset(params).then((res) => {
                if (res.code == 200) {
                    if (res.data.clusters_data.length > 0) {
                        this.isShow = true
                        if (barChart1) {
                            let selfName = ''
                            if (this.$route.query.species_name == 'Popular_alba') {
                                selfName = 'Populus alba var.pyramidalis'
                                // selfName = 'Populus alba'
                            } else if (this.$route.query.species_name == 'Nicotiana_tabacum') {
                                selfName = 'Nicotiana attenuate'
                            } else if (this.$route.query.species_name == 'Hybrid_poplar') {
                                selfName = 'Populus tremula × alba'
                            } else {
                                selfName = this.$route.query.species_name.replace(/_/g, ' ')
                            }
                            // this.option1.title.text = `${selfName} ${this.$route.query.project_id} (${this.$route.query.sample_count} samples, ${this.$route.query.cell_count} cells)`
                            this.title_text = `${selfName} ${this.$route.query.project_id} (${this.$route.query.sample_count} samples, ${this.$route.query.cell_count} cells)`
                            this.option1.series = []
                            res.data.clusters_data.forEach((item) => {
                                this.option1.legend.data.push(item.name.toString())
                                this.option1.series.push({
                                    symbolSize: 2,
                                    name: item.name.toString(),
                                    type: 'scatter',
                                    data: item.data
                                })
                            })

                            this.option1_2.series = []
                            let option1_2visualMapData = []
                            res.data.cell_type_data.forEach((item) => {
                                this.option1_2.legend.data.push(item.name)
                                this.option1_2.series.push({
                                    symbolSize: 2,
                                    name: item.name,
                                    type: 'scatter',
                                    data: item.data
                                })
                                option1_2visualMapData = [...option1_2visualMapData, ...item.data]
                            })
                            this.option1_2MinMax = []
                            option1_2visualMapData.forEach((item) => {
                                this.option1_2MinMax.push(item[2])
                            })
                        }
                    } else {
                        this.isShow = false
                    }
                    if (this.formInline.gene_id) {
                        this.option1.color = [
                            '#ef8839',
                            '#21c85d',
                            '#fbb02d',
                            '#ff0054',
                            '#ff5400',
                            '#f72585',
                            '#41c1e9',
                            '#7cb518',
                            '#c46cfd',
                            '#4cbcaf',
                            '#3f9fe0',
                            '#fb5607',
                            '#8338ec',
                            '#3a86ff',
                            '#ffd23f',
                            '#2ad4ad',
                            '#0ead69',
                            '#427aa1',
                            '#679436'
                        ]
                        this.option1_2.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#ccc']
                        // this.option1.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#dab77d', '#d9c583', '#D7DA8B', '#dddeb0', '#ccc']
                        this.option1_2.visualMap = {
                            show: false,
                            top: 'center',
                            right: 'left',
                            orient: 'vertical',
                            min: Number(Math.min.apply(null, this.option1_2MinMax)),
                            max: Number(Math.max.apply(null, this.option1_2MinMax)) || 1,
                            text: [Math.max.apply(null, this.option1_2MinMax).toString(), Math.min.apply(null, this.option1_2MinMax).toString()],
                            dimension: 2,
                            inRange: {
                                color: ['#ccc', '#E15457']
                            },
                            itemGap: 0
                            // itemSymbol: 'circle',
                            // pieces: [{
                            //   symbol: 'rect',
                            //   gte: 1,
                            //   color: '#E15457'
                            // },
                            // {
                            //   symbol: 'rect',
                            //   gte: 1,
                            //   lt: 0.9,
                            //   color: '#e1655e'
                            // },
                            // {
                            //   symbol: 'rect',
                            //   gte: 0.9,
                            //   lt: 0.8,
                            //   color: '#df7463'
                            // },
                            // {
                            //   symbol: 'rect',
                            //   gte: 0.8,
                            //   lt: 0.7,
                            //   color: '#de8369'
                            // },
                            // {
                            //   symbol: 'rect',
                            //   gte: 0.7,
                            //   lt: 0.6,
                            //   color: '#dd8e6d'
                            // },
                            // {
                            //   symbol: 'rect',
                            //   gte: 0.6,
                            //   lt: 0.5,
                            //   color: '#dc9d74'
                            // },
                            // {
                            //   symbol: 'rect',
                            //   gte: 0.5,
                            //   lt: 0.4,
                            //   color: '#daac79'
                            // },
                            // {
                            //   symbol: 'rect',
                            //   gte: 0.4,
                            //   lt: 0.3,
                            //   color: '#dab77d'
                            // },
                            // {
                            //   symbol: 'rect',
                            //   gte: 0.3,
                            //   lt: 0.2,
                            //   color: '#d9c583'
                            // },
                            // {
                            //   symbol: 'rect',
                            //   gte: 0.2,
                            //   lt: 0.1,
                            //   color: '#D7DA8B'
                            // },
                            // {
                            //   symbol: 'rect',
                            //   gte: 0.1,
                            //   lt: 0,
                            //   color: '#dddeb0'
                            // },
                            // {
                            //   symbol: 'rect',
                            //   value: 0,
                            //   color: '#ccc'
                            // },
                            // ]
                        }
                        // this.option1_2.visualMap = Object.assign({}, this.option1.visualMap)
                        this.option1_2.legend.show = false
                        this.option1_2.visualMap.show = true
                    } else {
                        // delete this.option1.visualMap;
                        // delete this.option1_2.visualMap;
                        // this.option1_2.legend.show = true
                        this.option1.color = [
                            '#ef8839',
                            '#21c85d',
                            '#fbb02d',
                            '#ff0054',
                            '#ff5400',
                            '#f72585',
                            '#41c1e9',
                            '#7cb518',
                            '#c46cfd',
                            '#4cbcaf',
                            '#3f9fe0',
                            '#fb5607',
                            '#8338ec',
                            '#3a86ff',
                            '#ffd23f',
                            '#2ad4ad',
                            '#0ead69',
                            '#427aa1',
                            '#679436'
                        ]
                        this.option1_2.color = [
                            '#ef8839',
                            '#21c85d',
                            '#fbb02d',
                            '#ff0054',
                            '#ff5400',
                            '#f72585',
                            '#41c1e9',
                            '#7cb518',
                            '#c46cfd',
                            '#4cbcaf',
                            '#3f9fe0',
                            '#fb5607',
                            '#8338ec',
                            '#3a86ff',
                            '#ffd23f',
                            '#2ad4ad',
                            '#0ead69',
                            '#427aa1',
                            '#679436'
                        ]
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
                species_name: this.$route.query.species_name,
                lit_id: this.$route.query.lit_id,
                project_id: this.$route.query.project_id
            }
            expressed_gene_cell_type_count(params).then((res) => {
                if (res.code == 200) {
                    if (barChart3) {
                        this.optionBar.yAxis.data = []
                        res.data.cell_count.forEach((item) => {
                            this.optionBar.yAxis.data.push(item.name)
                        })
                        this.optionBar.series[0].data = res.data.cell_count
                    }
                    this.Echarts = echarts.init(barChart3)
                    this.Echarts.setOption(this.optionBar, true)
                    this.chart3Url = res.data.hot_png
                    this.chartLoading2 = false
                }
            })
        },
        showExpression() {
            let params = {
                species_name: this.$route.query.species_name,
                lit_id: this.$route.query.lit_id,
                project_id: this.$route.query.project_id,
                gene_id: this.secondForm.gene_id
            }
            this.chartLoading2 = true
            expressed_gene_violin_box_plot(params).then((res) => {
                if (res.code == 200) {
                    this.ExpressionUrl1 = res.data.violinplot_png
                    this.ExpressionUrl2 = res.data.boxplot_png
                    this.chartLoading2 = false
                }
            })
        },
        // firstRadioClick(val) {
        //   if (val == 'Static') {

        //   } else {

        //   }
        // },
        secondRadioClick(val) {
            if (val == 'Overview') {
                this.isOverview = true
            } else {
                this.isOverview = false
            }
        },
        jumpTop(id) {
            this.formInline.gene_id = id
            this.firstGeneGo()
        },
        firstGeneGo() {
            this.showEcharts()
        },
        firstExample() {
            if (this.$route.query.species_name == 'Oryza_sativa') {
                this.formInline.gene_id = 'Os01g0169900'
            } else if (this.$route.query.species_name == 'Zea_mays') {
                this.formInline.gene_id = 'Zm00001d027266'
            } else if (this.$route.query.species_name == 'Nicotiana_tabacum') {
                this.formInline.gene_id = 'ENSRNA050025876'
            } else if (this.$route.query.species_name == 'Popular_alba') {
                this.formInline.gene_id = 'pal-pou40191'
            } else if (this.$route.query.species_name == 'Hybrid_poplar') {
                this.formInline.gene_id = 'Potri.T178800'
            } else if (this.$route.query.species_name == 'Solanum_lycopersicum') {
                this.formInline.gene_id = 'Solyc12g100130'
            } else if (this.$route.query.species_name == 'Fragaria_vesca') {
                this.formInline.gene_id = 'FvH4-c3g00210'
            } else if (this.$route.query.species_name == 'Phalaenopsis_aphrodite') {
                this.formInline.gene_id = 'PAXXG388540'
            } else {
                if (this.$route.query.project_id == 'GSM4423536') {
                    this.formInline.gene_id = 'AT1G27950'
                } else {
                    this.formInline.gene_id = 'AT1G12560'
                }
            }
            this.showEcharts()
        },
        secondGeneGo() {
            this.showExpression()
        },
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
            this.tableData = []
            if (type == 'cell_type') {
                project_atlas_list({
                    species_name: this.$route.query.species_name,
                    tissue: this.$route.query.tissue,
                    lit_id: this.$route.query.lit_id,
                    page: this.paginationConfig.page,
                    page_size: this.paginationConfig.size
                }).then((res) => {
                    if (res.code == 200) {
                        this.tableData = res.data.results
                        this.tableData.forEach((item) => {
                            // item.gene_id = item.gene_id.replace(/,/g, '  ')
                            item.gene_id_arr = item.gene_id
                            // if (item.gene_id != '') {
                            //   item.gene_id_arr = item.gene_id.split(',')
                            // }
                            // item.cell_po = item.cell_po ? `${item.cell_name} - ${item.cell_po}` : item.cell_name
                            // item.tissue_po = item.po_num ? `${item.tissue_id} - ${item.po_num}` : item.tissue_id
                        })
                        this.paginationConfig.total = res.data.count
                        this.loading = false
                    }
                })
            } else if (type == 'marker') {
                cluster_marker({
                    species_name: this.$route.query.species_name,
                    lit_id: this.$route.query.lit_id,
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
            } else {
                sample_list({
                    species_name: this.$route.query.species_name,
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
            }
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
            // if (row.sorce == 0) {
            //   return { background: '#FBFDFB', fontSize: '14px' }
            // }
            // if (row.sorce == 1) {
            //   return { background: '#F4FAF4', fontSize: '14px' }
            // }
            // if (row.sorce == 2) {
            //   return { background: '#EDF7ED', fontSize: '14px' }
            // }
            // if (row.sorce == 3) {
            //   return { background: '#E6F4E6', fontSize: '14px' }
            // }
            if (column.label === 'Refrence') {
                return { color: '#0a9daa', cursor: 'pointer', fontSize: '14px' }
            }
            return { fontSize: '14px' }
        },
        // handlecell(params) {
        //   if (params.col.label == 'DOI') {
        //     window.open(`${params.row.doi}`, '_blank')
        //   }
        // },
        handlecell(row, col) {
            if (col.label == 'Refrence') {
                window.open(`${row.doi}`, '_blank')
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
.projectResult .el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell {
    background: #eff6f7 !important;
}
</style>

<style lang="scss" scoped>
.projectResult {
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
    .title_text {
        font-weight: 400;
        color: #666666;
        font-size: 24px;
        text-align: center;
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
        .homepage_img_left {
            width: 100%;
            height: 534px;
            position: relative;
        }
        .litClass {
            cursor: pointer;
            display: inline-block;
            width: 25%;
            color: #0a9daa;
            text-decoration: underline;
        }
        .statusSpan1 {
            width: auto;
            background: #fff1f0;
            border: 1px solid #ffaca7;
            color: #d9656f;
            font-weight: 400;
            display: inline-block;
            padding: 0 10px;
        }
        .statusSpan2 {
            width: auto;
            background: #f6ffed;
            border: 1px solid #beed99;
            color: #3b9f57;
            font-weight: 400;
            display: inline-block;
            padding: 0 10px;
        }
        .statusSpan3 {
            width: auto;
            background: #fff7e6;
            border: 1px solid #ffd99b;
            color: #e49028;
            font-weight: 400;
            display: inline-block;
            padding: 0 10px;
        }
    }
}
</style>
