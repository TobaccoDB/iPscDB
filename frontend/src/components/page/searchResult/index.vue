<template>
    <div id="topAnchor" class="searchResult">
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
                <el-radio-group v-model="firstRadio" @change="firstRadioClick">
                    <!-- <el-radio label="Static">Static UMAP</el-radio> -->
                    <el-radio label="Interactive">Interactive UMAP</el-radio>
                    <!-- <el-radio label="StaticTsne">Static tSNE</el-radio> -->
                    <el-radio label="InteractiveTsne">Interactive tSNE</el-radio>
                </el-radio-group>
                <span style="font-size: 16px; color: #333; padding-left: 40px">*Interactive plot is based on sampled data(500 per cell type).</span>
            </div>
            <el-form :inline="true" :model="formInline" class="demo-form-inline" size="large" v-if="firstRadio == 'Interactive' || firstRadio == 'InteractiveTsne'">
                <el-form-item label="View by">
                    <el-select size="large" v-model="formInline.type" @change="viewByChange" placeholder="Choose">
                        <el-option label="Cell type" value="Cell_type"></el-option>
                        <el-option v-if="$route.query.Tissue == 'WholePlant'" label="Tissue" value="Clusters"></el-option>
                        <el-option v-if="$route.query.Tissue != 'WholePlant'" label="Cluster" value="Clusters"></el-option>
                        <el-option label="Sample" value="Project_ID"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="Gene">
                    <!-- <el-input clearable v-model="formInline.gene_id"></el-input> -->
                    <el-select v-model="formInline.gene_id" filterable remote reserve-keyword placeholder="Please enter" :remote-method="remoteMethod"
                        clearable :loading="GeneLoading">
                        <el-option v-for="item in GeneOptions" :key="item.value" :label="item.name" :value="item.value"> </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="firstGeneGoV2">GO</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="firstExample">Example</el-button>
                </el-form-item>
            </el-form>
            <p class="title_text" v-show="firstRadio != 'Static' && firstRadio != 'StaticTsne'">{{ title_text }}</p>
            <el-row :gutter="20" v-show="firstRadio != 'Static' && firstRadio != 'StaticTsne'">
                <!-- <el-col :span="12" v-show="isHaveGeneid">
                    <div class="homepage_img_left" style="text-align: center; overflow: hidden; padding-top: 32px">
                        <img style="max-width: 100%; max-height: 95%; margin-top: 10px" v-if="staticUrl" :src="staticUrl" />
                        <div style="width: 100%; height: 512px; overflow: hidden; line-height: 512px; font-size: 14px; color: #999; text-align: center" v-if="!staticUrl">No data</div>
                    </div>
                </el-col> -->
                <!--  v-show="!isHaveGeneid" -->
                <el-col :span="12">
                    <div style="overflow: hidden">
                        <el-button type="text" @click="downloadEcharts" style="color: #0a9daa; float: right; margin-right: 20px">
                            <i class="el-icon-download el-icon--right"></i>Export Plot
                        </el-button>
                    </div>
                    <div class="homepage_img_left 1" v-loading="chartLoading1" element-loading-background="#fff" v-show="(isShow && firstRadio == 'Interactive') || (isShow && firstRadio == 'InteractiveTsne')">
                        <div ref="barChart1" style="width: 590px; height: 534px"></div>
                    </div>
                    <div class="homepage_img_left 2" v-show="(!isShow && firstRadio == 'Interactive') || (!isShow && firstRadio == 'InteractiveTsne')">
                        <div style="width: 100%; height: 512px; overflow: hidden; line-height: 512px; font-size: 12px; color: #999; text-align: center"
                            v-loading="chartLoading1" element-loading-background="#fff">
                            No data
                        </div>
                    </div>
                </el-col>
                <el-col :span="12" v-show="!isHaveGeneid">
                    <div class="homepage_img_left 3" v-loading="barChartRightLoading1" element-loading-background="#fff" v-show="(isShow && firstRadio == 'Interactive') || (isShow && firstRadio == 'InteractiveTsne')">
                        <div ref="barChartRight1" style="width: 590px; height: 267px"></div>
                        <div ref="boxChartRight1" style="width: 590px; height: 267px"></div>
                    </div>
                    <div class="homepage_img_left 4" v-loading="boxChartRightLoading" element-loading-background="#fff" v-show="(!isShow && firstRadio == 'Interactive') || (!isShow && firstRadio == 'InteractiveTsne')">
                        <div style="width: 100%; height: 512px; overflow: hidden; line-height: 512px; font-size: 12px; color: #999; text-align: center"
                            v-loading="chartLoading1" element-loading-background="#fff">
                            No data
                        </div>
                    </div>
                </el-col>
                <el-col :span="12" v-show="isHaveGeneid">
                    <div style="overflow: hidden">
                        <el-button type="text" @click="downloadEcharts1_2" style="color: #0a9daa; float: right; margin-right: 20px">
                            <i class="el-icon-download el-icon--right"></i>Export Plot
                        </el-button>
                    </div>
                    <div class="homepage_img_left 50" v-loading="!isShow2" element-loading-background="#fff">
                        <!-- <div v-show="(isShow2 && firstRadio == 'Interactive') || (isShow2 && firstRadio == 'InteractiveTsne')">
                            <div ref="barChart1_2" style="width: 590px; height: 534px"></div>
                        </div> -->

                        <div v-show="isShow2" ref="barChart1_2" class="6556" :style="{ width: '590px', height: '534px' }"></div>
                        <!-- <div ref="barChart1_2_tsne" class="7777" v-show=" firstRadio == 'InteractiveTsne'" :style="{ width: '590px', height: '534px' }"></div> -->
                    </div>
                    <div class="homepage_img_left 6 " v-show="(!isShow && firstRadio == 'Interactive')">
                        <div style="width: 100%; height: 512px; overflow: hidden; line-height: 512px; font-size: 12px; color: #999; text-align: center"
                            v-loading="chartLoading1" element-loading-background="#fff">
                            No data
                        </div>
                    </div>
                </el-col>
            </el-row>

            <div class="homepage_img_left 7" style="text-align: center" v-if="firstRadio == 'Static' || firstRadio == 'StaticTsne'">
                <img style="max-width: 100%; max-height: 95%; margin-top: 10px" v-if="staticUrl" :src="staticUrl" />
                <div style="width: 100%; height: 512px; overflow: hidden; line-height: 512px; font-size: 14px; color: #999; text-align: center"
                    v-if="!staticUrl">No data</div>
            </div>

            <!-- <div style="margin:10px 0;">
        <el-radio-group v-model="secondRadio" @change="secondRadioClick">
          <el-radio label="Overview">Overview</el-radio>
          <el-radio label="Expression">Cell Type Expression</el-radio>
        </el-radio-group>
      </div> -->
            <el-form :inline="true" :model="secondForm" class="demo-form-inline" size="large" v-show="!isOverview">
                <el-form-item label="Gene">
                    <el-input clearable v-model="secondForm.gene_id"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="secondGeneGo">GO</el-button>
                </el-form-item>
            </el-form>
            <el-row :gutter="20" v-show="!isHaveGeneid">
                <!-- <el-row :gutter="20" v-show="isOverview"> -->
                <el-col :span="12">
                    <div class="homepage_img_left" v-loading="chartLoading2">
                        <img class="homepage_img_left-image3" width="100%" :src="chart3Url" />
                        <div class="homepage_img_left-name3">Cell to cell similarity</div>
                    </div>
                </el-col>
                <el-col :span="12">
                    <div class="homepage_img_left" v-loading="chartLoading2">
                        <div ref="barChart3" :style="{ width: '100%', height: '100%' }"></div>
                    </div>
                </el-col>
            </el-row>
            <el-row :gutter="20" v-show="isHaveGeneid">
                <!-- <el-row :gutter="20" v-show="!isOverview"> -->
                <el-col :span="12" v-loading="chartLoading2">
                    <div class="homepage_img_left" style="text-align: center; height: auto">
                        <img style="max-width: 100%; max-height: 100%" :src="ExpressionUrl1" />
                        <div style="width: 100%; height: 333px; overflow: hidden; line-height: 333px; font-size: 14px; color: #999; text-align: center"
                            v-if="!ExpressionUrl1">No data</div>
                    </div>
                </el-col>
                <el-col :span="12" v-loading="chartLoading2">
                    <div class="homepage_img_left" style="text-align: center; height: auto">
                        <img style="max-width: 100%; max-height: 100%" :src="ExpressionUrl2" />
                        <div style="width: 100%; height: 333px; overflow: hidden; line-height: 333px; font-size: 14px; color: #999; text-align: center"
                            v-if="!ExpressionUrl2">No data</div>
                    </div>
                </el-col>
            </el-row>
            <el-button v-show="isHaveGeneid" @click="downloadExpressionData" type="primary">Download expression data</el-button>
        </div>
        <!-- <p class="title1">Results</p> -->
        <div class="search-inner">
            <!-- 表格 -->
            <div style="margin-bottom: 10px">
                <!-- <i class="pointer" style="color:#24A461;float:right;cursor:pointer;text-decoration:underline;" @click="download(
          'txt')">Export Table</i> -->
                <el-radio-group v-model="radio" @change="radioClick" v-loading="loading">
                    <el-radio :label="1">Marker</el-radio>
                    <!-- <el-radio :label="2">Feature Gene</el-radio>
          <el-radio :label="3">Gene Exp</el-radio>
          <el-radio :label="4">Cell Type Freq</el-radio> -->
                    <el-radio :label="5">Detail</el-radio>
                    <!-- <el-radio :label="6">Sample</el-radio> -->
                </el-radio-group>
            </div>
            <!-- <el-table
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
            </el-pagination> -->
            <TableItem3 v-if="radio == '1'" type="searchResult" @setVal="setVal"></TableItem3>
            <el-table v-if="radio == '5'" size="small" :data="tableData" stripe :header-cell-style="headerStyle" v-loading="loading"
                element-loading-text="running" :cell-style="cellstyle" @cell-click="handlecell" border style="width: 100%">
                <el-table-column v-for="(item, index) in column" :key="index" :label="item.label" :width="item.width" :align="item.align === undefined ? 'center' : item.align"
                    :fixed="item.fixed === undefined ? false : item.fixed" :sortable="item.sortable === undefined ? false : item.sortable"
                    :prop="item.key">
                    <template slot-scope="scope">
                        <span>{{ scope.row[item.key] }}</span>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination v-if="radio == '5'" style="text-align: right; padding: 10px 5px" background :current-page="paginationConfig.page"
                :page-sizes="paginationConfig.sizes" :page-size="paginationConfig.size" :pager-count="7" :total="paginationConfig.total"
                @current-change="handleCurrentChange" @size-change="handleSizeChange" layout="total, sizes, prev, pager, next">
            </el-pagination>
            <el-table v-if="radio == '6'" size="small" :data="tableData" :header-cell-style="headerStyle" v-loading="loading" element-loading-text="running"
                :cell-style="cellstyle" stripe border style="width: 100%">
                <el-table-column v-for="(item, index) in column" :key="index" :label="item.label" :width="item.width" :align="item.align === undefined ? 'center' : item.align"
                    :fixed="item.fixed === undefined ? false : item.fixed" :sortable="item.sortable === undefined ? false : item.sortable"
                    :prop="item.key">
                    <template slot-scope="scope">
                        <span v-if="item.label == 'Sample ID' && scope.row['is_sample_rds'] == '1'">{{ scope.row[item.key] }}
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
                <!-- <el-table-column label="Sam ID" prop="sam_id" align='center' width="90">
          <template slot-scope="scope">
            <div>
              <span>{{scope.row.sam_id}}</span>
            </div>
          </template>
        </el-table-column> -->
            </el-table>
            <el-pagination v-if="radio == '6'" style="text-align: right; padding: 10px 5px" background :current-page="paginationConfig.page"
                :page-sizes="paginationConfig.sizes" :page-size="paginationConfig.size" :pager-count="7" :total="paginationConfig.total"
                @current-change="handleCurrentChange" @size-change="handleSizeChange" layout="total, sizes, prev, pager, next">
            </el-pagination>
            <!-- <jg-table ref="searchReslut_table" v-if="radio=='1' || radio=='5' || radio=='6'" :tableData="tableData" :column='column'
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
import dataTool from 'echarts/extension/dataTool'
import { option1, optionRight1, optionBoxplot, option2, option1_2, optionBar } from './config'
import { cell_search, cell_search_marker, search_marker, page_search_heat_map, all_search_heat_map, atlas_static_umap_png, home_atlas_static } from '@/api/search'
import {
    umap_expression,
    tsne_umap_dataset,
    plant_atlas_list,
    atlas_expressed_gene_cell_type_count,
    atlas_expressed_gene_violin_box_plot,
    atlas_gene_cell_type_count,
    cell_atlas_detail_diagram_map,
    cell_atlas_gene_symbol_download,
    marker_summary_list
} from '@/api/api'
import jgTable from '@/components/jgTable/index'
import TableItem3 from '../markerDefault/TableItem3.vue'
// import { resData } from './data'
// import { data2 } from './data2'
// import { data3 } from './data3'

export default {
    name: 'searchResult',
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
                gene_id: 'AT1G01010'
            },
            secondRadio: 'Overview',
            isOverview: true,

            chartLoading1: false,
            chartLoading2: false,
            chart3Url: '',
            staticUrl: '',
            staticUrlData: {},
            ExpressionUrl1: '',
            ExpressionUrl2: '',
            isShow: true,
            isShow2: true,
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
                // { key: 'tissue_id', label: 'Tissue Name', width: 120 },
                // { key: 'po_num', label: 'PO Num', width: 120 },
                { key: 'gene_id_arr', label: 'Published Cell Marker', width: 415 }
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
                // { key: 'cluster_id', label: 'Cluster ID', width: 100, align: 'center' },
                { key: 'gene_id', label: 'Gene ID' },
                { key: 'gene_symbol', label: 'Gene Name', width: 120 },
                { key: 'cell_type', label: 'Cell Type' },
                { key: 'pct1', label: 'pct1', width: 100 },
                { key: 'pct2', label: 'pct2', width: 100 },
                { key: 'log_2fc', label: 'Log2FC', width: 180 },
                { key: 'p_va1', label: 'P val', width: 180 },
                { key: 'p_val_adj', label: 'P val adj', width: 180 }
            ],
            sample_colum: [
                { key: 'species_name', label: 'Species name' },
                { key: 'sample_id', label: 'Sample ID' },
                { key: 'project_id', label: 'Project ID' },
                { key: 'sample_type', label: 'Sample type' },
                { key: 'tissue', label: 'Tissue' },
                { key: 'chemistry', label: 'Platform' }
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
            optionRight1,
            optionBoxplot,
            option1_2,
            option2,
            optionBar,
            table_type: 'cell_type',
            headerStyle: {
                // color: '#fff',
                fontSize: '14px',
                // background: '#24A461',
                fontFamily: 'Source Han Sans CN'
            },
            title_text: '',
            option1_2MinMax: [],
            isHaveGeneid: false,
            barChartRightLoading1: false,
            boxChartRightLoading: false,
            GeneOptions: [],
            GeneLoading: false,
            list: [],
            exampleValue: null,
            exampleShow: null,
        }
    },
    mounted() {
        // if (this.$route.query.marker_resource != '' && this.$route.query.marker_resource != undefined) {
        //   this.marker_resource = this.$route.query.marker_resource
        // }
        // if (this.$route.query.name == 'Oryza_sativa') {
        //   if (this.$route.query.Tissue == 'WholePlant') {
        //     this.secondForm.gene_id = 'Os04g0599650'
        //   } else if (this.$route.query.Tissue == 'Root') {
        //     this.secondForm.gene_id = 'Os05g0160300'
        //   } else if (this.$route.query.Tissue == 'Leaf') {
        //     this.secondForm.gene_id = 'Os09g0481200'
        //   } else if (this.$route.query.Tissue == 'Flower') {
        //     this.secondForm.gene_id = 'Os03g0279200'
        //   }
        // } else if (this.$route.query.name == 'Zea_mays') {
        //   if (this.$route.query.Tissue == 'WholePlant') {
        //     this.secondForm.gene_id = 'Zm00001d027500'
        //   } else if (this.$route.query.Tissue == 'Root') {
        //     this.secondForm.gene_id = 'Zm00001d004728'
        //   } else if (this.$route.query.Tissue == 'Leaf') {
        //     this.secondForm.gene_id = 'Zm00001d028471'
        //   } else if (this.$route.query.Tissue == 'Ear') {
        //     this.secondForm.gene_id = 'Zm00001d007254'
        //   } else if (this.$route.query.Tissue == 'SAM') {
        //     this.secondForm.gene_id = 'Zm00001d038211'
        //   }
        // } else if (this.$route.query.name == 'Nicotiana_tabacum') {
        //   if (this.$route.query.Tissue == 'Flower') {
        //     this.secondForm.gene_id = 'A4A49-30297'
        //   } else {
        //     this.secondForm.gene_id = 'ENSRNA050025876'
        //   }
        // } else if (this.$route.query.name == 'Popular_alba') {
        //   if (this.$route.query.Tissue == 'Stem') {
        //     this.secondForm.gene_id = 'pal-pou24718'
        //   } else {
        //     this.secondForm.gene_id = 'pal-pou40191'
        //   }
        // } else if (this.$route.query.name == 'Hybrid_poplar') {
        //   if (this.$route.query.Tissue == 'Shoot') {
        //     this.secondForm.gene_id = 'Potri.012G080400'
        //   } else {
        //     this.secondForm.gene_id = 'Potri.T178800'
        //   }
        // } else if (this.$route.query.name == 'Solanum_lycopersicum') {
        //   if (this.$route.query.Tissue == 'WholePlant') {
        //     this.secondForm.gene_id = 'Solyc06g075040'
        //   } else if (this.$route.query.Tissue == 'Root') {
        //     this.secondForm.gene_id = 'Solyc05g015300'
        //   } else {
        //     this.secondForm.gene_id = 'Solyc12g100130'
        //   }
        // } else if (this.$route.query.name == 'Fragaria_vesca') {
        //   if (this.$route.query.Tissue == 'WholePlant') {
        //     this.secondForm.gene_id = 'FvH4-2g06140'
        //   } else if (this.$route.query.Tissue == 'Leaf') {
        //     this.secondForm.gene_id = 'FvH4-2g06140'
        //   } else {
        //     this.secondForm.gene_id = 'FvH4-c3g00210'
        //   }
        // } else if (this.$route.query.name == 'Phalaenopsis_aphrodite') {
        //   if (this.$route.query.Tissue == 'WholePlant') {
        //     this.secondForm.gene_id = 'PAXXG313900'
        //   } else {
        //     this.secondForm.gene_id = 'PAXXG388540'
        //   }
        // } else if (this.$route.query.name == 'Arabidopsis_thaliana') {
        //   if (this.$route.query.Tissue == 'WholePlant') {
        //     this.secondForm.gene_id = 'AT5G24800'
        //   } else if (this.$route.query.Tissue == 'Root') {
        //     this.secondForm.gene_id = 'AT1G47410'
        //   } else if (this.$route.query.Tissue == 'Leaf') {
        //     this.secondForm.gene_id = 'AT3G05730'
        //   } else if (this.$route.query.Tissue == 'Shoot') {
        //     this.secondForm.gene_id = 'AT1G64370'
        //   } else if (this.$route.query.Tissue == 'Flower') {
        //     this.secondForm.gene_id = 'AT1G63100'
        //   }
        // }
        this.column = this.cell_type_column
        // ================================================================
        // 取消初始化
        this.getTableData(this.table_type, true)
        this.showEcharts()

        this.showBarEcharts()
        // ================================================================

        // this.firstExample()
        // this.showExpression()
        // atlas_static_umap_png({
        //   species_name: this.$route.query.name,
        //   tissue: this.$route.query.Tissue
        // }).then(res => {
        //   if (res.code == 200) {
        //     this.staticUrlData = res.data
        //     this.staticUrl = this.staticUrlData.project_static_umap_png
        //   }
        // });
        // home_atlas_static({
        //   species_name: this.$route.query.name,
        //   tissue: this.$route.query.Tissue,
        //   umap_type: this.firstRadio == 'Interactive' ? 'umap' : 'tsne',
        //   view_type: this.formInline.type
        // }).then(res => {
        //   if (res.code == 200) {
        //     this.staticUrlData = res.data
        //     this.staticUrl = this.staticUrlData.home_atlas_static_png
        //   }
        // });
    },
    // updated() {
    //   this.$refs.searchReslut_table.$refs.jgTable.doLayout()
    // },
    methods: {
        setVal(val) {
            console.log(val)
            this.exampleValue = val
            // this.formInline.gene_id = val
            // this.formInline.gene_id = val
            // this.$nextTick(() =>{
            //     this.firstGeneGo()
            // })
        },
        resourceChange(val) { },
        viewByChange(val) {
            // this.showEcharts()
        },
        showEcharts() {
            // this.chartLoading1 = true

            let barChart1 = this.$refs.barChart1
            let barChart1_2 = this.$refs.barChart1_2
            let params = {
                tissue: this.$route.query.Tissue,
                species_name: this.$route.query.name,
                gene_id: this.formInline.gene_id || this.exampleShow,
                umap_type: this.formInline.type
            }
            this.isShow2 = false
            this.showEcharts1()

            const getRandomInt = (a, b) => {
                // 确保a小于等于b
                if (a > b) {
                    [a, b] = [b, a];
                }
                // Math.random()生成[0,1)之间的随机数
                // 乘以(b - a + 1)后范围变为[0, b - a + 1)
                // 再加上a后范围变为[a, b + 1)
                // 最后用Math.floor向下取整得到[a, b]之间的整数
                return Math.floor(Math.random() * (b - a + 1)) + a;
            }

            const getRandomInt2 = (a, b) => {
                // 确保a小于等于b
                if (a > b) {
                    [a, b] = [b, a];
                }
                return [a, b]
            }
            const methodMap = {
                Interactive: umap_expression,
                InteractiveTsne: tsne_umap_dataset
            };
            // if (this.firstRadio == 'Interactive') {
            methodMap[this.firstRadio](params).then((res) => {


                if (res.code == 200) {
                    if (res.data.clusters_data) {
                        this.isShow = true
                        this.isShow2 = true
                        if (barChart1) {
                            let selfName = ''
                            if (this.$route.query.name == 'Popular_alba') {
                                selfName = 'Populus alba var.pyramidalis'
                                // selfName = 'Populus alba'
                            } else if (this.$route.query.name == 'Nicotiana_tabacum') {
                                selfName = 'Nicotiana tabacum'
                            } else if (this.$route.query.name == 'Hybrid_poplar') {
                                selfName = 'Populus tremula × alba'
                            } else {
                                selfName = this.$route.query.name.replace(/_/g, ' ')
                            }
                            // this.option1.title.text = `${selfName} ${this.$route.query.Tissue} (${this.$route.query.sample_count} samples, ${this.$route.query.cell_count} cells)`
                            this.title_text = `${selfName} ${this.$route.query.tissue_label} ` //(${this.$route.query.sample_count} samples, ${this.$route.query.cell_count} cells)`
                            this.option1.legend.data = []
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
                            this.option1_2.legend.data = []
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
                        this.isShow2 = false
                    }
                    if (this.formInline.gene_id || this.exampleShow) {
                        this.option1.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#ccc']
                        this.option1_2.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#ccc']
                        // this.option1.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#dab77d', '#d9c583', '#D7DA8B', '#dddeb0', '#ccc']
                        this.option1.visualMap = {
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
                        this.option1_2.visualMap = Object.assign({}, this.option1.visualMap)
                        this.option1_2.legend.show = false
                        this.option1_2.visualMap.show = true
                    } else {
                        // delete this.option1.visualMap
                        delete this.option1_2.visualMap
                        this.option1_2.legend.show = true
                        // this.option1.color = [
                        //     '#ef8839',
                        //     '#21c85d',
                        //     '#fbb02d',
                        //     '#ff0054',
                        //     '#ff5400',
                        //     '#f72585',
                        //     '#41c1e9',
                        //     '#7cb518',
                        //     '#c46cfd',
                        //     '#4cbcaf',
                        //     '#3f9fe0',
                        //     '#fb5607',
                        //     '#8338ec',
                        //     '#3a86ff',
                        //     '#ffd23f',
                        //     '#2ad4ad',
                        //     '#0ead69',
                        //     '#427aa1',
                        //     '#679436'
                        // ]
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

                    // this.Echarts = echarts.init(barChart1)
                    /***
                     * 以下是 2025年1月16日 操作
                     * 
                     * */
                    this.Echarts_2 = echarts.init(barChart1_2)
                    this.Echarts_2.setOption(this.option1_2, true)
                    // let color = [
                    //         '#ef8839',
                    //         '#21c85d',
                    //         '#fbb02d',
                    //         '#ff0054',
                    //         '#ff5400',
                    //         '#f72585',
                    //         '#41c1e9',
                    //         '#7cb518',
                    //         '#c46cfd',
                    //         '#4cbcaf',
                    //         '#3f9fe0',
                    //         '#fb5607',
                    //         '#8338ec',
                    //         '#3a86ff',
                    //         '#ffd23f',
                    //         '#2ad4ad',
                    //         '#0ead69',
                    //         '#427aa1',
                    //         '#679436'
                    // ]
                    // let cell_type_data3 = res.data.cell_type_data
                    //     let newData3 = []
                    //     for(let i=0; i< cell_type_data3.length; i++){
                    //         let itemName = cell_type_data3[i].name;
                    //         let truncatedName = itemName.length > 10 ? itemName.substring(0, 10) + '...' : itemName;

                    //         let item = { 
                    //             x: [],
                    //             y: [],
                    //             name: truncatedName,
                    //             hoverinfo: 'text',
                    //             mode: 'markers',
                    //             marker: {
                    //                     // color: ['rgb(93, 164, 214)', 'rgb(255, 144, 14)',  'rgb(44, 160, 101)', 'rgb(255, 65, 54)'],
                    //                     // color: ['#000000'],
                    //                     size: 2,
                    //                     color: []
                    //                 }
                    //             }
                    //         for(let j=0; j<cell_type_data3[i].data.length; j++){
                    //             let dataPoint = cell_type_data3[i].data[j];
                    //             item.x.push(dataPoint[0])
                    //             item.y.push(dataPoint[1])
                    //             let pointColor = dataPoint[2] === 0 ? '#cccccc' : color[i % color.length];
                    //                 item.marker.color.push(pointColor);
                    //         }
                    //         newData3.push(item)
                    //     }
                    //     var layout3 = {
                    //         margin: {
                    //             l: 50,  // 左边距
                    //             r: 150,  // 右边距
                    //             b: 50,  // 底边距
                    //             t: 50   // 顶边距
                    //         },
                    //     };
                    //     Plotly.newPlot(barChart1_2, newData3, layout3);
                    /**
                     * 以上是 2025年1月16日 操作
                     * */
                    // this.Echarts_2.resize()
                    // this.Echarts.setOption(this.option1, true)

                    // this.chartLoading1 = false
                }
            })
            // } else if (this.firstRadio == 'InteractiveTsne') {
            //     // this.$refs.barChart1_2_tsne.innerHTML = null
            //     tsne_umap_dataset(params).then((res) => {
            //         if (res.code == 200) {
            //             if (res.data.clusters_data) {
            //                 this.isShow = true
            //                 this.isShow2 = true
            //                 if (barChart1) {
            //                     let selfName = ''
            //                     if (this.$route.query.name == 'Popular_alba') {
            //                         selfName = 'Populus alba'
            //                     } else if (this.$route.query.name == 'Nicotiana_tabacum') {
            //                         selfName = 'Nicotiana tabacum'
            //                     } else {
            //                         selfName = this.$route.query.name.replace(/_/g, ' ')
            //                     }

            //                     this.title_text = `${selfName} ${this.$route.query.tissue_label}`
            //                     this.option1.legend.data = []
            //                     this.option1.series = []
            //                     res.data.clusters_data.forEach((item) => {
            //                         this.option1.legend.data.push(item.name.toString())
            //                         this.option1.series.push({
            //                             symbolSize: 2,
            //                             name: item.name.toString(),
            //                             type: 'scatter',
            //                             data: item.data
            //                         })
            //                     })
            //                     this.option1_2.legend.data = []
            //                     this.option1_2.series = []
            //                     let option1_2visualMapData = []
            //                     res.data.cell_type_data.forEach((item) => {
            //                         this.option1_2.legend.data.push(item.name)
            //                         this.option1_2.series.push({
            //                             symbolSize: 2,
            //                             name: item.name,
            //                             type: 'scatter',
            //                             data: item.data
            //                         })
            //                         option1_2visualMapData = [...option1_2visualMapData, ...item.data]
            //                     })
            //                     this.option1_2MinMax = []
            //                     option1_2visualMapData.forEach((item) => {
            //                         this.option1_2MinMax.push(item[2])
            //                     })


            //                 }

            //                 this.isShow2 = false
            //             } else {
            //                 this.isShow = false
            //                 this.isShow2 = false
            //             }
            //             if (this.formInline.gene_id || this.exampleShow) {
            //                 this.option1.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#ccc', '#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#ccc']
            //                 this.option1_2.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#ccc', '#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#ccc']

            //                 this.option1.visualMap = {
            //                     show: false,
            //                     top: 'center',
            //                     right: 'left',
            //                     orient: 'vertical',

            //                     min: Number(Math.min.apply(null, this.option1_2MinMax)),
            //                     max: Number(Math.max.apply(null, this.option1_2MinMax)) || 1,
            //                     text: [Math.max.apply(null, this.option1_2MinMax).toString(), Math.min.apply(null, this.option1_2MinMax).toString()],

            //                     dimension: 2,
            //                     inRange: {
            //                         color: ['#ccc', '#E15457']
            //                     },
            //                     itemGap: 0
            //                 }
            //                 this.option1_2.visualMap = Object.assign({}, this.option1.visualMap)
            //                 this.option1_2.legend.show = false
            //                 this.option1_2.visualMap.show = true
            //             } else {
            //                 delete this.option1.visualMap
            //                 delete this.option1_2.visualMap
            //                 this.option1_2.legend.show = true

            //                 this.option1_2.color = [
            //                     '#ef8839',
            //                     '#21c85d',
            //                     '#fbb02d',
            //                     '#ff0054',
            //                     '#ff5400',
            //                     '#f72585',
            //                     '#41c1e9',
            //                     '#7cb518',
            //                     '#c46cfd',
            //                     '#4cbcaf',
            //                     '#3f9fe0',
            //                     '#fb5607',
            //                     '#8338ec',
            //                     '#3a86ff',
            //                     '#ffd23f',
            //                     '#2ad4ad',
            //                     '#0ead69',
            //                     '#427aa1',
            //                     '#679436',
            //                     '#ef8839',
            //                     '#21c85d',
            //                     '#fbb02d',
            //                     '#ff0054',
            //                     '#ff5400',
            //                     '#f72585',
            //                     '#41c1e9',
            //                     '#7cb518',
            //                     '#c46cfd',
            //                     '#4cbcaf',
            //                     '#3f9fe0',
            //                     '#fb5607',
            //                     '#8338ec',
            //                     '#3a86ff',
            //                     '#ffd23f',
            //                     '#2ad4ad',
            //                     '#0ead69',
            //                     '#427aa1',
            //                     '#679436'
            //                 ]
            //             }
            //             // this.Echarts = echarts.init(barChart1)
            //             let DOM = this.$refs.barChart1_2_tsne
            //             this.Echarts_2 = echarts.init(DOM)
            //             // this.Echarts.setOption(this.option1, true)
            //             this.Echarts_2.setOption(this.option1_2, true)

            //             console.log('---------------', DOM)
            //             // this.chartLoading1 = false
            //             this.isShow2 = false
            //         }
            //     })
            // }
        },
        showEcharts1() {
            this.chartLoading1 = true
            let barChart1 = this.$refs.barChart1
            let barChart1_2 = this.$refs.barChart1_2
            let params = {
                tissue: this.$route.query.Tissue,
                species_name: this.$route.query.name,
                gene_id: '',
                umap_type: this.formInline.type
            }
            const methodMap = {
                Interactive: umap_expression,
                InteractiveTsne: tsne_umap_dataset
            };

            // if (this.firstRadio == 'Interactive') {
            methodMap[this.firstRadio](params).then((res) => {
                if (res.code == 200) {
                    if (res.data.clusters_data) {
                        this.isShow = true
                        if (barChart1) {
                            let selfName = ''
                            if (this.$route.query.name == 'Popular_alba') {
                                selfName = 'Populus alba var.pyramidalis'
                                // selfName = 'Populus alba'
                            } else if (this.$route.query.name == 'Nicotiana_tabacum') {
                                selfName = 'Nicotiana tabacum'
                            } else if (this.$route.query.name == 'Hybrid_poplar') {
                                selfName = 'Populus tremula × alba'
                            } else {
                                selfName = this.$route.query.name.replace(/_/g, ' ')
                            }
                            // this.option1.title.text = `${selfName} ${this.$route.query.Tissue} (${this.$route.query.sample_count} samples, ${this.$route.query.cell_count} cells)`
                            this.title_text = `${selfName} ${this.$route.query.tissue_label} ` //(${this.$route.query.sample_count} samples, ${this.$route.query.cell_count} cells)`
                            this.option1.legend.data = []
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
                            this.option1_2.legend.data = []
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
                    if (this.formInline.gene_id || this.exampleShow) {
                        this.option1.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#cccccc']
                        this.option1_2.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#cccccc']
                        // this.option1.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#dab77d', '#d9c583', '#D7DA8B', '#dddeb0', '#ccc']
                        this.option1.visualMap = {
                            show: false,
                            top: 'center',
                            right: 'left',
                            orient: 'vertical',
                            min: Number(Math.min.apply(null, this.option1_2MinMax)),
                            max: Number(Math.max.apply(null, this.option1_2MinMax)) || 1,
                            text: [Math.max.apply(null, this.option1_2MinMax).toString(), Math.min.apply(null, this.option1_2MinMax).toString()],
                            dimension: 2,
                            inRange: {
                                color: ['#cccccc', '#E15457']
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
                        this.option1_2.visualMap = Object.assign({}, this.option1.visualMap)
                        this.option1_2.legend.show = false
                        this.option1_2.visualMap.show = true
                    } else {
                        delete this.option1.visualMap
                        delete this.option1_2.visualMap
                        this.option1_2.legend.show = true
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
                    /***
                     * 以下 2025年1月16日 操作
                     * 
                     * 
                     * */
                    this.Echarts = echarts.init(barChart1)
                    // let color = [
                    //         '#ef8839',
                    //         '#21c85d',
                    //         '#fbb02d',
                    //         '#ff0054',
                    //         '#ff5400',
                    //         '#f72585',
                    //         '#41c1e9',
                    //         '#7cb518',
                    //         '#c46cfd',
                    //         '#4cbcaf',
                    //         '#3f9fe0',
                    //         '#fb5607',
                    //         '#8338ec',
                    //         '#3a86ff',
                    //         '#ffd23f',
                    //         '#2ad4ad',
                    //         '#0ead69',
                    //         '#427aa1',
                    //         '#679436'
                    // ]
                    // let cell_type_data3 = res.data.cell_type_data
                    //     let newData3 = []
                    //     for(let i=0; i< cell_type_data3.length; i++){
                    //         let itemName = cell_type_data3[i].name;
                    //         let truncatedName = itemName.length > 10 ? itemName.substring(0, 10) + '...' : itemName;

                    //         let item = { 
                    //             x: [],
                    //             y: [],
                    //             name: truncatedName,
                    //             hoverinfo: 'text',
                    //             mode: 'markers',
                    //             marker: {
                    //                     // color: ['rgb(93, 164, 214)', 'rgb(255, 144, 14)',  'rgb(44, 160, 101)', 'rgb(255, 65, 54)'],
                    //                     // color: ['#000000'],
                    //                     size: 2,
                    //                     color: []
                    //                 }
                    //             }
                    //         for(let j=0; j<cell_type_data3[i].data.length; j++){
                    //             let dataPoint = cell_type_data3[i].data[j];
                    //             item.x.push(dataPoint[0])
                    //             item.y.push(dataPoint[1])
                    //             let pointColor = dataPoint[2] === 0 ? '#cccccc' : color[i % color.length];
                    //                 item.marker.color.push(pointColor);
                    //         }
                    //         newData3.push(item)
                    //     }
                    //     var layout3 = {
                    //         margin: {
                    //             l: 50,  // 左边距
                    //             r: 150,  // 右边距
                    //             b: 50,  // 底边距
                    //             t: 50   // 顶边距
                    //         },
                    //     };
                    //     Plotly.newPlot(barChart1, newData3, layout3);

                    /**
                     * 以上
                     * 
                     * */
                    // this.Echarts_2 = echarts.init(barChart1_2)
                    // this.Echarts_2.resize()
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
                    this.Echarts.setOption(this.option1, true)
                    // this.Echarts_2.setOption(this.option1_2, true)
                    this.chartLoading1 = false
                }
            })


            return
            // } else if (this.firstRadio == 'InteractiveTsne') {
            //     tsne_umap_dataset(params).then((res) => {
            //         if (res.code == 200) {
            //             if (res.data.clusters_data) {
            //                 this.isShow = true
            //                 if (barChart1) {
            //                     let selfName = ''
            //                     if (this.$route.query.name == 'Popular_alba') {
            //                         selfName = 'Populus alba'
            //                     } else if (this.$route.query.name == 'Nicotiana_tabacum') {
            //                         selfName = 'Nicotiana tabacum'
            //                     } else {
            //                         selfName = this.$route.query.name.replace(/_/g, ' ')
            //                     }

            //                     this.title_text = `${selfName} ${this.$route.query.tissue_label}` 
            //                     this.option1.legend.data = []
            //                     this.option1.series = []
            //                     res.data.clusters_data.forEach((item) => {
            //                         this.option1.legend.data.push(item.name.toString())
            //                         this.option1.series.push({
            //                             symbolSize: 2,
            //                             name: item.name.toString(),
            //                             type: 'scatter',
            //                             data: item.data
            //                         })
            //                     })
            //                     this.option1_2.legend.data = []
            //                     this.option1_2.series = []
            //                     let option1_2visualMapData = []
            //                     res.data.cell_type_data.forEach((item) => {
            //                         this.option1_2.legend.data.push(item.name)
            //                         this.option1_2.series.push({
            //                             symbolSize: 2,
            //                             name: item.name,
            //                             type: 'scatter',
            //                             data: item.data
            //                         })
            //                         option1_2visualMapData = [...option1_2visualMapData, ...item.data]
            //                     })
            //                     this.option1_2MinMax = []
            //                     option1_2visualMapData.forEach((item) => {
            //                         this.option1_2MinMax.push(item[2])
            //                     })

            //                     this.isShow2 = false
            //                 }
            //             } 


            //                 this.option1.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#cccccc', '#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#cccccc']
            //                 this.option1_2.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#cccccc', '#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#cccccc']

            //                 this.option1.visualMap = {
            //                     show: false,
            //                     top: 'center',
            //                     right: 'left',
            //                     orient: 'vertical',

            //                     min: Number(Math.min.apply(null, this.option1_2MinMax)),
            //                     max: Number(Math.max.apply(null, this.option1_2MinMax)) || 1,
            //                     text: [Math.max.apply(null, this.option1_2MinMax).toString(), Math.min.apply(null, this.option1_2MinMax).toString()],

            //                     dimension: 2,
            //                     inRange: {
            //                         color: ['#cccccc', '#E15457']
            //                     },
            //                     itemGap: 0

            //                 }
            //                 this.option1_2.visualMap = Object.assign({}, this.option1.visualMap)
            //                 this.option1_2.legend.show = false
            //                 this.option1_2.visualMap.show = true

            //             this.Echarts = echarts.init(barChart1)

            //             this.option1.color = [
            //                 '#ef8839',
            //                 '#21c85d',
            //                 '#fbb02d',
            //                 '#ff0054',
            //                 '#ff5400',
            //                 '#f72585',
            //                 '#41c1e9',
            //                 '#7cb518',
            //                 '#c46cfd',
            //                 '#4cbcaf',
            //                 '#3f9fe0',
            //                 '#fb5607',
            //                 '#8338ec',
            //                 '#3a86ff',
            //                 '#ffd23f',
            //                 '#2ad4ad',
            //                 '#0ead69',
            //                 '#427aa1',
            //                 '#679436',
            //                 '#ef8839',
            //                 '#21c85d',
            //                 '#fbb02d',
            //                 '#ff0054',
            //                 '#ff5400',
            //                 '#f72585',
            //                 '#41c1e9',
            //                 '#7cb518',
            //                 '#c46cfd',
            //                 '#4cbcaf',
            //                 '#3f9fe0',
            //                 '#fb5607',
            //                 '#8338ec',
            //                 '#3a86ff',
            //                 '#ffd23f',
            //                 '#2ad4ad',
            //                 '#0ead69',
            //                 '#427aa1',
            //                 '#679436'
            //             ]
            //             this.Echarts.setOption(this.option1, true)
            //             // this.Echarts_2.setOption(this.option1_2, true)
            //             this.chartLoading1 = false
            //             // console.log('=============', barChart1_2)
            //             this.isShow2 = false
            //         }
            //     })
            // }
        },
        showBarEcharts() {
            this.chartLoading2 = true
            this.barChartRightLoading1 = true
            this.boxChartRightLoading = true
            let barChartRight1 = this.$refs.barChartRight1
            let boxChartRight1 = this.$refs.boxChartRight1
            let barChart3 = this.$refs.barChart3
            let params = {
                species_name: this.$route.query.name,
                tissue: this.$route.query.Tissue,
                view_by: this.formInline.type
            }
            atlas_expressed_gene_cell_type_count(params).then((res) => {
                if (res.code == 200) {
                    if (barChart3) {
                        this.optionBar.yAxis.data = []
                        res.data.cell_count &&
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
            atlas_gene_cell_type_count(params).then((res) => {
                if (res.code == 200) {
                    if (barChartRight1) {
                        if (this.formInline.type == 'Cell_type') {
                            this.optionRight1.title.text = `Cell Number in Each Cell type`
                        } else if (this.formInline.type == 'Project_ID') {
                            this.optionRight1.title.text = `Cell Number in Each Sample`
                        }
                        if (this.formInline.type == 'Clusters') {
                            if (this.$route.query.Tissue == 'WholePlant') {
                                this.optionRight1.title.text = `Cell Number in Each Tissue`
                            } else {
                                this.optionRight1.title.text = `Cell Number in Each Cluster`
                            }
                        }
                        this.optionRight1.xAxis.data = []
                        res.data.cell_count &&
                            res.data.cell_count.forEach((item) => {
                                this.optionRight1.xAxis.data.push(item.name)
                            })
                        this.optionRight1.series[0].data = res.data.cell_count
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
                    this.barChartRightLoading1 = false
                }
            })
            // 箱图
            cell_atlas_detail_diagram_map(params).then((res) => {
                if (res.code == 200) {
                    if (boxChartRight1) {
                        let ydata = []
                        this.optionBoxplot.xAxis.data = Object.keys(res.data)
                        this.optionBoxplot.series[0].data = []
                        // this.optionBoxplot.xAxis.data = []
                        // this.optionBoxplot.series[0].data = []
                        // res.data && res.data.forEach(item => {
                        //   ydata.push(item[1])
                        //   this.optionBoxplot.xAxis.data.push(item[0])
                        // });
                        res.data &&
                            Object.values(res.data).forEach((item) => {
                                ydata.push(item)
                                // this.optionBoxplot.xAxis.data.push(item[0])
                            })
                        if (this.formInline.type == 'Cell_type') {
                            this.optionBoxplot.title.text = `Gene Number in Each Cell`
                        } else if (this.formInline.type == 'Project_ID') {
                            this.optionBoxplot.title.text = `Cell Number in Each Sample`
                        }
                        if (this.formInline.type == 'Clusters') {
                            if (this.$route.query.Tissue == 'WholePlant') {
                                this.optionBoxplot.title.text = `Cell Number in Each Tissue`
                            } else {
                                this.optionBoxplot.title.text = `Cell Number in Each Cluster`
                            }
                        }

                        ydata = echarts.dataTool.prepareBoxplotData(ydata)
                        // this.optionBoxplot.xAxis.data = ydata.axisData
                        // this.optionBoxplot.series[1].data = ydata.outliers
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
                        ydata.boxData.forEach((element, index) => {
                            this.optionBoxplot.series[0].data.push({
                                value: element,
                                itemStyle: {
                                    normal: {
                                        borderColor: '#666',
                                        // borderColor: '#4B96F3',
                                        borderWidth: 1,
                                        color: color10[index]
                                    }
                                }
                            })
                        })
                        this.Echarts = echarts.init(boxChartRight1)
                        this.Echarts.setOption(this.optionBoxplot, true)
                        this.boxChartRightLoading = false
                    }
                }
            })
        },
        firstRadioClick(val) {
            //if (val == 'Interactive' || val == 'InteractiveTsne') {
            //this.showEcharts()
            //} else if (val == 'Static') {
            // this.staticUrl = this.staticUrlData.project_static_umap_png
            //} else if (val == 'StaticTsne') {
            //  this.staticUrl = this.staticUrlData.project_static_tsne_png
            // }

            home_atlas_static({
                species_name: this.$route.query.name,
                tissue: this.$route.query.Tissue,
                umap_type: this.firstRadio == 'Interactive' ? 'umap' : 'tsne',
                view_type: this.formInline.type
            }).then((res) => {
                if (res.code == 200) {
                    this.staticUrlData = res.data
                    this.staticUrl = this.staticUrlData.home_atlas_static_png
                }
            })

            if (val == 'Interactive') {
                this.showEcharts()
                this.staticUrl = this.staticUrlData.project_static_umap_png
            } else if (val == 'InteractiveTsne') {
                this.showEcharts()
                this.staticUrl = this.staticUrlData.project_static_tsne_png
            }
        },
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
        firstGeneGoV2() {
            this.exampleShow = null
            this.$nextTick(() => {
                this.firstGeneGo()
            })
        },
        firstGeneGo() {
            if (this.formInline.gene_id || this.exampleShow) {
                this.isHaveGeneid = true
                home_atlas_static({
                    species_name: this.$route.query.name,
                    tissue: this.$route.query.Tissue,
                    umap_type: this.firstRadio == 'Interactive' ? 'umap' : 'tsne',
                    view_type: this.formInline.type
                }).then((res) => {
                    if (res.code == 200) {
                        this.staticUrlData = res.data
                        this.staticUrl = this.staticUrlData.home_atlas_static_png
                    }
                })
                this.showExpression()
            } else {
                this.isHaveGeneid = false
                this.showBarEcharts()
            }
            this.showEcharts()
        },
        firstExample() {
            this.formInline.gene_id = this.exampleValue
            // this.exampleShow = this.exampleValue
            this.$nextTick(() => {
                this.firstGeneGo()
            })

            // if (this.$route.query.name == 'Oryza_sativa') {
            //   this.formInline.gene_id = 'Os06g0160100'
            // } else if (this.$route.query.name == 'Zea_mays') {
            //   this.formInline.gene_id = 'Zm00001d018973'
            // } else if (this.$route.query.name == 'Nicotiana_tabacum') {
            //   this.formInline.gene_id = 'ENSRNA050025876'
            // } else if (this.$route.query.name == 'Popular_alba') {
            //   this.formInline.gene_id = 'pal-pou40191'
            // } else if (this.$route.query.name == 'Hybrid_poplar') {
            //   this.formInline.gene_id = 'Potri.T178800'
            // } else if (this.$route.query.name == 'Solanum_lycopersicum') {
            //   this.formInline.gene_id = 'Solyc12g100130'
            // } else if (this.$route.query.name == 'Fragaria_vesca') {
            //   this.formInline.gene_id = 'FvH4-c3g00210'
            // } else if (this.$route.query.name == 'Phalaenopsis_aphrodite') {
            //   this.formInline.gene_id = 'PAXXG388540'
            // } else {
            //   if (this.$route.query.project_id == 'GSM4423536') {
            //     this.formInline.gene_id = 'AT1G27950'
            //   } else {
            //     this.formInline.gene_id = 'AT1G01010'
            //   }
            // }

            // -----------------------------------------------
            // 2024-05-07 注销

            // if (this.$route.query.name == 'Oryza_sativa') {
            //     if (this.$route.query.Tissue == 'WholePlant') {
            //         this.formInline.gene_id = 'Os04g0599650'
            //     } else if (this.$route.query.Tissue == 'Root') {
            //         this.formInline.gene_id = 'Os05g0160300'
            //     } else if (this.$route.query.Tissue == 'Leaf') {
            //         this.formInline.gene_id = 'Os09g0481200'
            //     } else if (this.$route.query.Tissue == 'Flower') {
            //         this.formInline.gene_id = 'Os03g0279200'
            //     }
            // } else if (this.$route.query.name == 'Zea_mays') {
            //     if (this.$route.query.Tissue == 'WholePlant') {
            //         this.formInline.gene_id = 'Zm00001d027500'
            //     } else if (this.$route.query.Tissue == 'Root') {
            //         this.formInline.gene_id = 'Zm00001d004728'
            //     } else if (this.$route.query.Tissue == 'Leaf') {
            //         this.formInline.gene_id = 'Zm00001d028471'
            //     } else if (this.$route.query.Tissue == 'Ear') {
            //         this.formInline.gene_id = 'Zm00001d007254'
            //     } else if (this.$route.query.Tissue == 'SAM') {
            //         this.formInline.gene_id = 'Zm00001d038211'
            //     }
            // } else if (this.$route.query.name == 'Nicotiana_tabacum') {
            //     if (this.$route.query.Tissue == 'Flower') {
            //         this.formInline.gene_id = 'A4A49-30297'
            //     } else {
            //         this.formInline.gene_id = 'ENSRNA050025876'
            //     }
            // } else if (this.$route.query.name == 'Popular_alba') {
            //     if (this.$route.query.Tissue == 'Stem') {
            //         this.formInline.gene_id = 'pal-pou24718'
            //     } else {
            //         this.formInline.gene_id = 'pal-pou40191'
            //     }
            // } else if (this.$route.query.name == 'Hybrid_poplar') {
            //     if (this.$route.query.Tissue == 'Shoot') {
            //         this.formInline.gene_id = 'Potri.012G080400'
            //     } else {
            //         this.formInline.gene_id = 'Potri.T178800'
            //     }
            // } else if (this.$route.query.name == 'Solanum_lycopersicum') {
            //     if (this.$route.query.Tissue == 'WholePlant') {
            //         this.formInline.gene_id = 'Solyc06g075040'
            //     } else if (this.$route.query.Tissue == 'Root') {
            //         this.formInline.gene_id = 'Solyc05g015300'
            //     } else {
            //         this.formInline.gene_id = 'Solyc12g100130'
            //     }
            // } else if (this.$route.query.name == 'Fragaria_vesca') {
            //     if (this.$route.query.Tissue == 'WholePlant') {
            //         this.formInline.gene_id = 'FvH4-2g06140'
            //     } else if (this.$route.query.Tissue == 'Leaf') {
            //         this.formInline.gene_id = 'FvH4-2g06140'
            //     } else {
            //         this.formInline.gene_id = 'FvH4-c3g00210'
            //     }
            // } else if (this.$route.query.name == 'Phalaenopsis_aphrodite') {
            //     if (this.$route.query.Tissue == 'WholePlant') {
            //         this.formInline.gene_id = 'PAXXG313900'
            //     } else {
            //         this.formInline.gene_id = 'PAXXG388540'
            //     }
            // } else if (this.$route.query.name == 'Arabidopsis_thaliana') {
            //     if (this.$route.query.Tissue == 'WholePlant') {
            //         this.formInline.gene_id = 'AT5G24800'
            //     } else if (this.$route.query.Tissue == 'Root') {
            //         this.formInline.gene_id = 'AT1G47410'
            //     } else if (this.$route.query.Tissue == 'Leaf') {
            //         this.formInline.gene_id = 'AT3G05730'
            //     } else if (this.$route.query.Tissue == 'Shoot') {
            //         this.formInline.gene_id = 'AT1G04800'
            //     } else if (this.$route.query.Tissue == 'Flower') {
            //         this.formInline.gene_id = 'AT1G63100'
            //     } else if (this.$route.query.Tissue == 'Embryos') {
            //         this.formInline.gene_id = 'AT1G68320'
            //     }
            // }
            // -----------------------------------------------

            // 一下是2025年1月9日z注释的
            // if (this.formInline.gene_id || this.exampleShow) {
            //     this.isHaveGeneid = true
            // } else {
            //     this.isHaveGeneid = false
            // }
            // this.showEcharts()
            // this.showExpression()
            // home_atlas_static({
            //     species_name: this.$route.query.name,
            //     tissue: this.$route.query.Tissue,
            //     umap_type: this.firstRadio == 'Interactive' ? 'umap' : 'tsne',
            //     view_type: this.formInline.type
            // }).then((res) => {
            //     if (res.code == 200) {
            //         this.staticUrlData = res.data
            //         this.staticUrl = this.staticUrlData.home_atlas_static_png
            //     }
            // })
        },
        secondGeneGo() {
            this.showExpression()
        },
        showExpression() {
            let params = {
                species_name: this.$route.query.name,
                tissue: this.$route.query.Tissue,
                gene_id: this.formInline.gene_id || this.exampleShow,
                type: this.firstRadio == 'InteractiveTsne' ? 'tsne_data' : 'umap_data',
                view_type: this.formInline.type
                // gene_id: this.secondForm.gene_id
            }
            this.chartLoading2 = true
            atlas_expressed_gene_violin_box_plot(params).then((res) => {
                if (res.code == 200) {
                    this.ExpressionUrl1 = res.data.violinplot_png
                    this.ExpressionUrl2 = res.data.boxplot_png
                    this.chartLoading2 = false
                }
            })
        },
        markerSummaryList() {
            marker_summary_list({
                query_type: 'home',
                species_name: this.$route.query.name,
                tissue_name: this.$route.query.Tissue,
                cell_name: this.$route.query.tissue_label,
                page: this.paginationConfig.page,
                page_size: this.paginationConfig.size
            }).then((res) => {
                if (res.code == 200) {
                    console.log('res.data.results------------')
                    this.tableData = res.data.results
                    this.paginationConfig.total = res.data.count
                }
                this.loading = false
            })
        },
        radioClick(val) {
            this.tableData = []
            this.paginationConfig.page = 1
            if (val == 1) {
                // this.table_type = 'cell_type'
                // this.column = this.cell_type_column
                // this.getTableData(this.table_type)
                console.log(this.radio, '==================')
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

            console.log(this.$route.query.name, 'type')
            plant_atlas_list({
                tag_list_type: type,
                species_name: this.$route.query.nameLabel,
                tissue: this.$route.query.Tissue,
                page: this.paginationConfig.page,
                page_size: this.paginationConfig.size
            }).then((res) => {
                if (res.code == 200) {
                    console.log('res.data.results================')
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
                            // if (item.gene_id != '') {
                            //   item.gene_id_arr = item.gene_id.split(',')
                            // }
                            // item.cell_po = item.cell_po ? `${item.cell_name} - ${item.cell_po}` : item.cell_name
                            // item.tissue_po = item.po_num ? `${item.tissue_id} - ${item.po_num}` : item.tissue_id
                            item.gene_id_arr = item.gene_id
                        })
                    }

                    this.paginationConfig.total = res.data.count
                    this.loading = false
                    console.log(this.tableData, 'this.tableData')
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
        handlecell(row, col) {
            if (col.label == 'Refrence') {
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
        },
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
        downloadExpressionData() {
            this.jg_downloadFile('/api/v1/atlas_gene_id_download/', {
                species_name: this.$route.query.name,
                tissue: this.$route.query.Tissue,
                gene_id: this.formInline.gene_id || this.exampleShow
            })
        },
        remoteMethod(query) {
            if (query !== '') {
                this.GeneLoading = true
                cell_atlas_gene_symbol_download({
                    species_name: this.$route.query.name,
                    gene_id: query,
                    tissue: this.$route.query.tissue_label
                    // gene_id: this.formInline.gene_id
                }).then((res) => {
                    if (res.code == 200) {
                        // this.list = res.data
                        this.GeneOptions = res.data
                        this.GeneLoading = false
                    }
                })
                // console.log(333322, query)
                // this.GeneLoading = true;
                // setTimeout(() => {
                //   this.GeneLoading = false;
                //   this.GeneOptions = this.list.filter(item => {
                //     return item.name.toLowerCase()
                //       .indexOf(query.toLowerCase()) > -1;
                //   });
                // }, 200);
            } else {
                this.GeneOptions = []
            }
        }
    },
    components: {
        TableItem3
    }
}
</script>

<style>
#myChart-license-text {
  display: none;
}
.searchResult
  .el-table--striped
  .el-table__body
  tr.el-table__row--striped
  td.el-table__cell {
  /* background: #eff6f7 !important; */
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
    //    background: #24a461;
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
      height: 534px;
      position: relative;
      .homepage_img_left-image3 {
        width: 575px;
        height: 490px;
      }
      .homepage_img_left-name3 {
        width: 100%;
        height: 30px;
        font-weight: bold;
        font-size: 20px;
        color: #333333;
        text-align: center;
        line-height: 32px;
      }
    }
    .litClass {
      cursor: pointer;
      display: inline-block;
      width: 25%;
      color: #0a9daa;
      text-decoration: underline;
      text-align: center;
    }
  }
}
</style>
