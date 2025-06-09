<template>
    <div class="searchDetails">
        <div class="crumbs">
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-breadcrumb-item v-if="$route.query.from == 'search'" :to="{ path: '/search' }">Search</el-breadcrumb-item>
                <el-breadcrumb-item v-if="$route.query.from == 'home'" :to="{ path: '/homePage' }">Home</el-breadcrumb-item>
                <el-breadcrumb-item v-if="$route.query.from == 'browse'" :to="{ path: '/browse' }">Browse</el-breadcrumb-item>
                <el-breadcrumb-item v-if="$route.query.from == 'blast'" :to="{ path: '/blast' }">Blast</el-breadcrumb-item>
                <el-breadcrumb-item v-if="$route.query.from == 'blast'" :to="{ path: '/searchList' }">Blast Results</el-breadcrumb-item>
                <!-- <el-breadcrumb-item v-if="$route.query.from =='CMPredictorDetails'" :to="{ path: '/CMPredictor' }">CMPredictor</el-breadcrumb-item> -->
                <el-breadcrumb-item v-if="$route.query.from == 'CMPredictorDetails'" :to="{ path: '/search' }">Search</el-breadcrumb-item>
                <el-breadcrumb-item v-if="$route.query.from != 'browse' && $route.query.from != 'CMPredictorDetails' && $route.query.from != 'blast'">
                    <span style="cursor: pointer" @click="jumpRoute">Search result</span>
                </el-breadcrumb-item>
                <el-breadcrumb-item v-if="$route.query.from == 'CMPredictorDetails'">
                    <span style="cursor: pointer" @click="jumpRoute2">CMPredictor Results</span>
                </el-breadcrumb-item>
                <el-breadcrumb-item>Search Results</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="searchDetails-inner">
            <p class="title1">Basic information</p>
            <div class="content_detail" v-loading="top_loading">
                <div class="grid-content" v-for="(item, index) in itemList" :key="index">
                    {{ item.key }}：
                    <span v-if="item.key != 'NCBI Gene ID' && item.key != 'NCBI RNA ID' && item.key != 'NCBI Protein ID'">{{ item.value }}</span>
                    <span v-else v-for="i in item.value.split(';')" :key="i">
                        <span style="cursor: pointer; color: #24a461" @click="jumpNCBI(item.key, i)">{{ i }}</span>
                    </span>
                </div>
                <div class="grid-content">
                    Sequence Information：
                    <router-link :to="{ path: '/detailInfo', query: { id: itemList[2].value, name: 'pep' } }" target="_blank">
                        <span>Peptide Sequence</span>
                    </router-link>
                    <router-link :to="{ path: '/detailInfo', query: { id: itemList[2].value, name: 'cds' } }" target="_blank">
                        <span>CDS Sequence</span>
                    </router-link>
                </div>
            </div>
            <p class="title1">Supported Evidences</p>
            <div class="search-list-table">
                <el-table :data="seTableData" class="table" ref="multipleTable" :header-cell-style="headerStyle" :row-style="rowStyle">
                    <el-table-column label="Cell Type" prop="cell_type" align="center">
                        <template slot-scope="scope">
                            <span style="cursor: pointer; color: #24a461" @click="jumpNCBI('PO_num', scope.row.cell_type_po)">{{ scope.row.cell_type }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="experiment_evidence" align="center" label="Experimental Evidence">
                        <template slot-scope="scope">
                            <div v-for="item in scope.row.experiment_evidence.split(',')" :key="item">
                                <!-- <span v-if="/^(10\.|DOI:)/.test(item)" style="float:left;width:50%;">{{item}}</span> -->
                                <span style="cursor: pointer; color: #24a461; float: left; width: 50%" @click="jumpPMID(item)">{{ item }}</span>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column label="scRNA-seq Evidence" prop="single_cell_evidence" align="center">
                        <template slot-scope="scope">
                            <div v-for="item in scope.row.single_cell_evidence.split(',')" :key="item">
                                <!-- <span v-if="/^(10\.|DOI:)/.test(item)" style="float:left;width:50%;">{{item}}</span> -->
                                <span style="cursor: pointer; color: #24a461; float: left; width: 50%" @click="jumpPMID(item)">{{ item }}</span>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column label="Bulk RNA-seq Evidence" prop="transcriptome_evidence" align="center">
                        <template slot-scope="scope">
                            <div v-for="item in scope.row.transcriptome_evidence.split(',')" :key="item">
                                <!-- <span v-if="/^(10\.|DOI:)/.test(item)" style="float:left;width:50%;">{{item}}</span> -->
                                <span style="cursor: pointer; color: #24a461; float: left; width: 50%" @click="jumpPMID(item)">{{ item }}</span>
                            </div>
                        </template>
                    </el-table-column>
                    <el-table-column label="Total Evidences" prop="cell_type_count" align="center"> </el-table-column>
                </el-table>
            </div>
            <!-- iframe -->
            <p class="title1">eFP Image</p>
            <div class="content_efp" v-loading="loading">
                <el-form ref="form" class="efp_form" :inline="true" :model="efp_form">
                    <el-form-item label="Data Source">
                        <el-select size="large" style="width: 360px" v-model="efp_form.dataSource" placeholder="choose">
                            <el-option v-for="(item, index) in selectOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-button size="large" type="primary" @click="goSearch">GO</el-button>
                </el-form>
                <div class="svgClass" ref="efpPlant" v-if="isNicotiana_tabacum" v-html="stage_svg"></div>
                <img :src="reportUrl" v-else />
            </div>
            <!-- Transcriptome -->
            <p class="title1">Expression pattern by Bulk RNA-seq</p>
            <div class="Transcriptome">
                <el-form ref="form" class="efp_form" :inline="true" :model="bar_form" style="text-align: left; margin-top: 20px">
                    <el-form-item label="Dataset">
                        <el-select size="large" style="width: 360px" v-model="bar_form.pmid" placeholder="choose">
                            <el-option v-for="(item, index) in barOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-button size="large" type="primary" @click="pmidSearch">GO</el-button>
                </el-form>
                <!-- 柱形图 -->
                <div :style="{ width: '100%', height: barHeight, position: 'relative' }">
                    <div
                        v-if="barHeight == '100px'"
                        style="width: 100%; height: 178px; background: #fff; position: absolute; font-size: 16px; color: #666; line-height: 100px; text-align: center; z-index: 100"
                    >
                        No Data
                    </div>
                    <div ref="barChart1" :style="{ width: '100%', height: barHeight }"></div>
                </div>
                <el-pagination
                    style="text-align: right; padding: 20px 15px 20px 15px"
                    background
                    :current-page="paginationBar.page"
                    :page-size="paginationBar.page_size"
                    :total="paginationBar.total"
                    @current-change="barCurrentChange"
                    layout="total, prev, pager, next"
                ></el-pagination>
            </div>
            <!-- UMAP -->
            <p class="title1">Cluster map by scRNA-seq</p>
            <div class="UMAP">
                <el-form ref="form" class="efp_form" :inline="true" :model="umap_form" style="text-align: left; margin-top: 20px">
                    <el-form-item label="Dataset">
                        <el-select size="large" style="width: 360px" v-model="umap_form.umapData" placeholder="choose">
                            <el-option v-for="(item, index) in umapOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-button size="large" type="primary" @click="umapSearch">GO</el-button>
                    <el-radio-group v-model="radio" style="margin-left: 90px" @change="umapChange">
                        <el-radio label="UMAP">UMAP</el-radio>
                        <el-radio label="TSNE">TSNE</el-radio>
                    </el-radio-group>
                </el-form>
                <div :style="{ width: '100%', height: umapHeight }" v-loading="umapLoading">
                    <el-row :gutter="20" v-if="radio == 'UMAP'">
                        <el-col :span="12">
                            <div
                                v-if="umapHeight == '100px'"
                                style="width: 100%; height: 110px; background: #fff; position: absolute; font-size: 16px; color: #666; line-height: 100px; text-align: center; z-index: 100"
                            >
                                No Data
                            </div>
                            <div ref="barChart2" :style="{ width: '100%', height: umapHeight }"></div>
                        </el-col>
                        <el-col :span="12">
                            <div ref="barChart3" :style="{ width: '100%', height: umapHeight }"></div>
                        </el-col>
                    </el-row>
                    <el-row :gutter="20" v-else>
                        <el-col :span="12">
                            <div
                                v-if="umapHeight == '100px'"
                                style="width: 100%; height: 110px; background: #fff; position: absolute; font-size: 16px; color: #666; line-height: 100px; text-align: center; z-index: 100"
                            >
                                No Data
                            </div>
                            <div ref="barChart4" :style="{ width: '100%', height: umapHeight }"></div>
                        </el-col>
                        <el-col :span="12">
                            <div ref="barChart5" :style="{ width: '100%', height: umapHeight }"></div>
                        </el-col>
                    </el-row>
                </div>
            </div>
            <!-- 表格部分-文献 -->
            <p class="title1">References</p>
            <div class="content_document">
                <ul class="retrieval_pub_ul" ref="targetbox" id="targetbox">
                    <li v-for="(item, index) in tableData" :key="index" :style="{ backgroundColor: item.bgColor }">
                        <p @click="jumpClick(item.id)">{{ item.title }}</p>
                        <p>{{ item.author }}</p>
                        <p>{{ item.source }}</p>
                    </li>
                </ul>
                <!-- <el-pagination style="text-align:right;padding:20px 15px 0 15px;" background :current-page="paginationConfig.page" :page-size="paginationConfig.size"
          :total="paginationConfig.total" @current-change="handleCurrentChange" layout="total, prev, pager, next"></el-pagination> -->
            </div>
        </div>
    </div>
</template>

<script>
import echarts from 'echarts'
import { option1, option2, option3, option4, option5 } from './config'
import axios from '@/api/http.js'
import {
    cell_search_detail,
    cell_search_public_list,
    cell_search_efp,
    pmid_dataset,
    transcriptome,
    umap_dataset,
    umap_expression,
    tsne_expression,
    supported_evidences,
    nicotiana_tabacum_efp
} from '@/api/search'
export default {
    name: 'searchDetails',
    components: {},
    data() {
        return {
            top_loading: false,
            itemList: [
                { key: 'Species', value: '' },
                // { key: 'Tissue Type', value: '' },
                { key: 'Gene Symbol', value: '' },
                { key: 'Gene ID', value: '' },
                { key: 'Other ID', value: '' },
                { key: 'Chromosome', value: '' },
                { key: 'Start', value: '' },
                { key: 'End', value: '' },
                { key: 'Strand', value: '' },
                { key: 'NCBI Gene ID', value: '' },
                { key: 'NCBI RNA ID', value: '' },
                { key: 'NCBI Protein ID', value: '' },
                { key: 'Aliases', value: '' },
                { key: 'Description', value: '' }
            ],
            seTableData: [],
            headerStyle: {
                background: '#F5F5F5',
                fontSize: '16px',
                fontFamily: 'PingFang SC',
                fontWeight: 'bold',
                color: '#333'
            },
            rowStyle: {
                fontSize: '14px',
                fontFamily: 'PingFang SC',
                fontWeight: '400',
                color: '#666'
            },
            reportUrl: '',
            tableData: [],
            paginationConfig: {
                page: 1,
                size: 10,
                total: 0
            },
            efp_form: {
                dataSource: ''
            },
            selectOptions: [],
            loading: false,
            option1,
            option2,
            option3,
            option4,
            option5,
            umap_form: {
                umapData: ''
            },
            umapOptions: [],
            barHeight: '500px',
            umapHeight: '500px',
            barOptions: [],
            bar_form: {
                pmid: ''
            },
            radio: 'UMAP',
            umapLoading: false,
            bgColor: '',
            isNicotiana_tabacum: false,
            stage_svg: '',
            paginationBar: {
                page: 1,
                page_size: 20,
                total: 0
            }
        }
    },
    created() {
        // this.goSearch()
    },
    mounted() {
        this.init()
        this.getDocumentData()
    },
    methods: {
        init() {
            this.top_loading = true
            cell_search_detail(this.$route.query.id).then((res) => {
                if (res.code == 200) {
                    let data = res.data.data
                    this.itemList[0].value = data.species_type
                    // this.itemList[1].value = data.tissue_type
                    this.itemList[1].value = data.gene_symbol
                    this.itemList[2].value = data.gene_id
                    this.itemList[3].value = data.other_id
                    this.itemList[4].value = data.chromosome
                    this.itemList[5].value = data.start
                    this.itemList[6].value = data.end
                    this.itemList[7].value = data.strand
                    this.itemList[8].value = data.ncbi_gene_id
                    this.itemList[9].value = data.ncbi_rna_id
                    this.itemList[10].value = data.ncbi_protein_id
                    this.itemList[11].value = data.aliases
                    this.itemList[12].value = data.description
                    this.selectOptions = data.specie_efp_data_source
                    this.isNicotiana_tabacum = false
                    if (data.species_type == 'Arabidopsis thaliana') {
                        this.efp_form.dataSource = 'Klepikova_Atlas'
                    } else if (data.species_type == 'Oryza sativa') {
                        this.efp_form.dataSource = 'rice_mas'
                    } else if (data.species_type == 'Nicotiana tabacum') {
                        this.efp_form.dataSource = 'Sierro_N_et_al'
                        this.isNicotiana_tabacum = true
                    } else if (data.species_type == 'Zea mays') {
                        this.efp_form.dataSource = 'Downs_et_al_Atlas'
                    } else if (data.species_type == 'Glycine max') {
                        this.efp_form.dataSource = 'soybean'
                    } else if (data.species_type == 'Solanum lycopersicum') {
                        this.efp_form.dataSource = 'Rose_Lab_Atlas'
                    }
                    this.goSearch()
                    this.top_loading = false
                }
            })
            umap_dataset(this.$route.query.id).then((res) => {
                if (res.code == 200) {
                    this.umapOptions = res.data
                    this.umap_form.umapData = res.data[0] && res.data[0].value
                    this.showEcharts(this.umap_form.umapData)
                }
            })
            pmid_dataset(this.$route.query.id).then((res) => {
                if (res.code == 200) {
                    this.barOptions = res.data
                    this.bar_form.pmid = res.data[0] && res.data[0].value
                    this.getBarData(this.bar_form.pmid)
                }
            })
            supported_evidences(this.$route.query.id).then((res) => {
                if (res.code == 200) {
                    console.log(res.data)
                    this.seTableData = res.data
                }
            })
        },
        showEcharts(dataset) {
            let barChart2 = this.$refs.barChart2
            let barChart3 = this.$refs.barChart3
            let barChart4 = this.$refs.barChart4
            let barChart5 = this.$refs.barChart5
            let params = {
                id: this.$route.query.id,
                dataset: dataset
            }
            this.umapLoading = true
            if (this.radio == 'UMAP') {
                umap_expression(params).then((res) => {
                    if (res.code == 200) {
                        if (res.data.umpa_data.length > 0) {
                            this.umapHeight = '500px'
                            if (barChart2) {
                                this.option2.legend.data = []
                                this.option2.series = []
                                res.data.umpa_data.forEach((item) => {
                                    this.option2.legend.data.push(item.name)
                                    this.option2.series.push({
                                        symbolSize: 2,
                                        name: item.name,
                                        type: 'scatter',
                                        data: item.data
                                    })
                                })
                            }
                            if (barChart3) {
                                this.option3.series[0].data = res.data.expression_data
                            }
                        } else {
                            this.umapHeight = '100px'
                            // this.option2.title = {
                            //     text: 'No Data',
                            //     x: 'center',
                            //     y: 40,
                            //     textStyle: {
                            //       color: '#666',
                            //       fontWeight: 'normal',
                            //       fontSize: 16
                            //     }
                            //   }
                            // this.option3.title = this.option2.title
                        }
                        this.Echarts = echarts.init(barChart2)
                        this.Echarts.setOption(this.option2, true)
                        this.Echarts = echarts.init(barChart3)
                        this.Echarts.setOption(this.option3, true)
                        this.umapLoading = false
                    }
                })
            } else {
                tsne_expression(params).then((res) => {
                    if (res.code == 200) {
                        if (res.data.umpa_data.length > 0) {
                            this.umapHeight = '500px'
                            if (barChart4) {
                                this.option4.legend.data = []
                                this.option4.series = []
                                res.data.umpa_data.forEach((item) => {
                                    this.option4.legend.data.push(item.name)
                                    this.option4.series.push({
                                        symbolSize: 2,
                                        name: item.name,
                                        type: 'scatter',
                                        data: item.data
                                    })
                                })
                            }
                            if (barChart5) {
                                this.option5.series[0].data = res.data.expression_data
                            }
                        } else {
                            this.umapHeight = '100px'
                            // this.option4 = {
                            //   title: {
                            //     text: 'No Data',
                            //     x: 'center',
                            //     y: 40,
                            //     textStyle: {
                            //       color: '#666',
                            //       fontWeight: 'normal',
                            //       fontSize: 16
                            //     }
                            //   }
                            // }
                            // this.option5 = this.option4
                        }
                        this.Echarts = echarts.init(barChart4)
                        this.Echarts.setOption(this.option4, true)
                        this.Echarts = echarts.init(barChart5)
                        this.Echarts.setOption(this.option5, true)
                        this.umapLoading = false
                    }
                })
            }
        },
        getBarData(pmid) {
            // 获取柱形图数据
            let barChart1 = this.$refs.barChart1
            if (barChart1) {
                let params = {
                    page: this.paginationBar.page,
                    page_size: this.paginationBar.page_size,
                    id: this.$route.query.id,
                    pmid: pmid
                }
                transcriptome(params).then((res) => {
                    if (res.code == 200) {
                        this.paginationBar.total = res.data.count
                        if (res.data.series.length > 0) {
                            this.barHeight = '500px'
                            // barChart1.clear();
                            // barChart1 = this.$refs.barChart1
                            this.option1.series = []
                            // this.option1.legend.data = []
                            this.option1.yAxis.data = []
                            res.data.xAxis.forEach((item) => {
                                this.option1.yAxis.data.push('PMID:' + item)
                            })
                            this.option1.xAxis.boundaryGap = [0, 0.15]
                            res.data.series.forEach((item) => {
                                // this.option1.legend.data.push(item.name)
                                this.option1.series.push({
                                    name: item.name,
                                    type: 'bar',
                                    barMaxWidth: 26,
                                    barMinWidth: 16,
                                    data: item.data,
                                    label: {
                                        show: true,
                                        formatter: '{a}',
                                        fontWeight: 900,
                                        position: 'right'
                                    }
                                })
                            })
                        } else {
                            this.barHeight = '100px'
                            // barChart1.clear();
                            // barChart1 = this.$refs.barChart1
                            // this.option1 = {
                            //   title: {
                            //     text: 'No Data',
                            //     x: 'center',
                            //     y: 40,
                            //     textStyle: {
                            //       color: '#666',
                            //       fontWeight: 'normal',
                            //       fontSize: 16
                            //     }
                            //   }
                            // }
                        }
                        this.Echarts = echarts.init(barChart1)
                        this.Echarts.setOption(this.option1, true)
                    }
                })
            }
        },
        barCurrentChange(val) {
            this.paginationBar.page = val
            this.getBarData(this.bar_form.pmid)
        },
        getDocumentData() {
            let params = {
                id: this.$route.query.id
                // page: this.paginationConfig.page,
                // page_size: this.paginationConfig.size
            }
            cell_search_public_list(params).then((res) => {
                if (res.code == 200) {
                    this.tableData = res.data.results
                    this.paginationConfig.total = res.data.count
                }
            })
        },
        jumpPMID(id) {
            // let reg = /^(10\.|DOI:)/i;
            // if (reg.test(id)) {
            //   return
            // }
            this.tableData.forEach((item, index) => {
                if (item.pmid == id) {
                    this.$set(this.tableData[index], 'bgColor', '#ebebeb')
                } else {
                    this.$set(this.tableData[index], 'bgColor', '#fff')
                }
            })
            // if (key == 'PMID') {
            // window.open(`https://pubmed.ncbi.nlm.nih.gov/${id}/`, '_blank')
            // }
            let targetbox = document.getElementById('targetbox')
            if (targetbox.offsetTop > document.documentElement.scrollHeight) {
                document.getElementById('targetbox').scrollIntoView(false)
            } else {
                document.getElementById('targetbox').scrollIntoView(true)
            }
        },
        jumpClick(id) {
            this.$router.push({
                path: '/documentDetails',
                query: {
                    id: id
                }
            })
        },
        // 分页导航
        handleCurrentChange(val) {
            this.paginationConfig.page = val
            this.getDocumentData()
        },
        goSearch() {
            this.loading = true
            if (this.isNicotiana_tabacum) {
                // 烟草
                let params = {
                    gene_id: this.itemList[2].value,
                    data_source: this.efp_form.dataSource
                }
                this.stage_svg = ''
                nicotiana_tabacum_efp(params).then((res) => {
                    if (res.code == 200) {
                        this.loading = false
                        this.stage_svg = res.data.stage_svg
                        // debugger
                        Object.keys(res.data.stage_plant).forEach((clsItem) => {
                            // 每个中有多少个部位
                            this.$nextTick(function () {
                                // this.$refs.efpPlant.style.height = Number(this.$refs.efpPlant.querySelector('svg').clientHeight) + 'px'
                                this.$refs.efpPlant.querySelectorAll(`.${clsItem}`).forEach((item) => {
                                    item.style.fill = res.data.stage_plant[clsItem]
                                })
                            })
                        })
                    }
                })
            } else {
                let params = {
                    id: this.$route.query.id,
                    data_source: this.efp_form.dataSource
                }
                this.reportUrl = ''
                cell_search_efp(params).then((res) => {
                    if (res.code == 200) {
                        this.reportUrl = res.data.data.efp_url
                        setTimeout(() => {
                            this.loading = false
                        }, 1000)
                    }
                })
            }
        },
        umapSearch() {
            this.showEcharts(this.umap_form.umapData)
        },
        umapChange() {
            this.showEcharts(this.umap_form.umapData)
        },
        pmidSearch() {
            this.getBarData(this.bar_form.pmid)
        },
        jumpRoute(val) {
            // 路由跳转
            this.$router.push({
                path: '/searchResult',
                query: JSON.parse(sessionStorage.getItem('searchResultQuery'))
            })
            sessionStorage.removeItem('searchResultQuery')
        },
        jumpRoute2() {
            // 路由跳转
            this.$router.push({
                path: '/CMPredictorDetails',
                query: JSON.parse(sessionStorage.getItem('CMPredictorDetailsQuery'))
            })
            sessionStorage.removeItem('CMPredictorDetailsQuery')
        },
        jumpNCBI(key, value) {
            // detailsNCBI跳转
            if (key == 'NCBI Gene ID') {
                window.open(`https://www.ncbi.nlm.nih.gov/gene/?term=${value}`, '_blank')
            } else if (key == 'NCBI RNA ID') {
                window.open(`https://www.ncbi.nlm.nih.gov/nuccore/${value}/`, '_blank')
            } else if (key == 'NCBI Protein ID') {
                window.open(`https://www.ncbi.nlm.nih.gov/protein/${value}/`, '_blank')
            } else {
                window.open(`https://archive.plantontology.org/amigo/go.cgi?view=details&search_constraint=terms&depth=0&query=${value}&session_id=3535b1621820355&show_associations=list`, '_blank')
            }
        }
    }
}
</script>
<style lang="scss" scoped>
@import './style.scss';
</style>
