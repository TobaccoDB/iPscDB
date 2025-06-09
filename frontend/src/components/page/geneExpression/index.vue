<template>
    <div class="geneExpression">
        <div class="geneExpression-inner">
            <div class="efpTitle">Cross-species gene expression</div>
            <div class="blast">
                <el-form ref="form1" :inline="true" :model="geneExpression_form" :rules="rules">
                    <el-form-item label="Specie" prop="species_name">
                        <el-select clearable style="width: 200px" size="large" @change="species_nameChange" v-model="geneExpression_form.species_name" placeholder="Choose">
                            <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <!-- <el-form-item label="Reference" prop="reference">
            <el-select clearable style="width:180px;" size="large" @change="referenceChange" v-model="geneExpression_form.reference"
              placeholder="Choose">
              <el-option v-for="(item, index) in referenceOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item> -->
                    <el-form-item label="Tissue" prop="tissue">
                        <el-select clearable style="width: 200px" size="large" v-model="geneExpression_form.tissue" placeholder="Choose">
                            <el-option v-for="(item, index) in tissueOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Gene" prop="gene_id">
                        <!-- <el-select filterable clearable style="width:200px;" size="large" v-model="geneExpression_form.gene_id" placeholder="Choose">
              <el-option v-for="item in gene_idOptions" :key="item.label" :label="item.label" :value="item.value">
              </el-option>
            </el-select> -->
                        <el-select
                            v-model="geneExpression_form.gene_id"
                            size="large"
                            filterable
                            remote
                            reserve-keyword
                            placeholder="Please enter keywords"
                            :remote-method="remoteMethod"
                            :loading="selectLoading"
                        >
                            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="">
                        <el-button class="btnSearch" @click="search">GO</el-button>
                    </el-form-item>
                    <el-form-item label="">
                        <el-button class="btnSearch" @click="exampleClick">Example</el-button>
                    </el-form-item>
                </el-form>
                <div :style="{ width: '100%', height: 'auto' }">
                    <div class="title_header">UMAP visualization of cell types</div>
                    <el-row :gutter="20">
                        <el-col :span="8" v-loading="umapLoading1" element-loading-background="#fff">
                            <div v-show="option1.series.length">
                                <div ref="barChart1" :style="{ width: '400px', height: '300px' }"></div>
                                <p class="echarts_title">{{ species_name1.replace(/_/g, ' ') }}（{{ geneExpression_form.tissue }}）</p>
                            </div>
                            <div class="homepage_img_left" v-show="!option1.series.length">
                                <div style="width: 100%; height: 300px; overflow: hidden; line-height: 300px; font-size: 14px; color: #999; text-align: center">No data</div>
                            </div>
                        </el-col>
                        <el-col :span="8" v-loading="umapLoading2" element-loading-background="#fff">
                            <div v-show="option2.series.length">
                                <div ref="barChart2" :style="{ width: '400px', height: '300px' }"></div>
                                <p class="echarts_title">{{ species_name2.replace(/_/g, ' ') }}（{{ geneExpression_form.tissue }}）</p>
                            </div>

                            <div class="homepage_img_left" v-show="!option2.series.length">
                                <div style="width: 100%; height: 300px; overflow: hidden; line-height: 300px; font-size: 14px; color: #999; text-align: center">No data</div>
                            </div>
                        </el-col>
                        <el-col :span="8" v-loading="umapLoading3" element-loading-background="#fff">
                            <div v-show="option3.series.length">
                                <div ref="barChart3" :style="{ width: '400px', height: '300px' }"></div>
                                <p class="echarts_title">{{ species_name3.replace(/_/g, ' ') }}（{{ geneExpression_form.tissue }}）</p>
                            </div>

                            <div class="homepage_img_left" v-show="!option3.series.length">
                                <div style="width: 100%; height: 300px; overflow: hidden; line-height: 300px; font-size: 14px; color: #999; text-align: center">No data</div>
                            </div>
                        </el-col>
                    </el-row>

                    <!-- Gene expression -->
                    <div class="title_header">Gene expression</div>
                    <el-row :gutter="20">
                        <el-col :span="8" v-loading="expressionLoading1" element-loading-background="#fff">
                            <div class="homepage_img_left" v-show="option2_1.series.length">
                                <div ref="barChart2_1" style="width: 400px; height: 300px"></div>
                            </div>
                            <div class="homepage_img_left" v-show="!option2_1.series.length">
                                <div style="width: 100%; height: 300px; overflow: hidden; line-height: 300px; font-size: 14px; color: #999; text-align: center">No data</div>
                            </div>
                        </el-col>
                        <el-col :span="8" v-loading="expressionLoading2" element-loading-background="#fff">
                            <div class="homepage_img_left" v-show="option2_2.series.length">
                                <div ref="barChart2_2" style="width: 400px; height: 300px"></div>
                                <!-- <div ref='barChart2_2' :style="{width: '100%',height: '100%'}"></div> -->
                            </div>
                            <div class="homepage_img_left" v-show="!option2_2.series.length">
                                <div style="width: 100%; height: 300px; overflow: hidden; line-height: 300px; font-size: 14px; color: #999; text-align: center">No data</div>
                            </div>
                        </el-col>
                        <el-col :span="8" v-loading="expressionLoading3" element-loading-background="#fff">
                            <div class="homepage_img_left" v-show="option2_3.series.length">
                                <div ref="barChart2_3" style="width: 400px; height: 300px"></div>
                            </div>
                            <div class="homepage_img_left" v-show="!option2_3.series.length">
                                <div style="width: 100%; height: 300px; overflow: hidden; line-height: 300px; font-size: 14px; color: #999; text-align: center">No data</div>
                            </div>
                        </el-col>
                    </el-row>
                    <!-- Expression in cell types -->
                    <div class="title_header">Expression in cell types</div>
                    <el-row :gutter="20" v-loading="chartLoading3">
                        <el-col :span="8">
                            <div class="homepage_img_left" style="text-align: center" v-if="ExpressionUrl1">
                                <img style="max-width: 100%; max-height: 100%" :src="ExpressionUrl1" />
                            </div>
                            <div class="homepage_img_left" v-show="!ExpressionUrl1">
                                <div style="width: 100%; height: 300px; overflow: hidden; line-height: 300px; font-size: 14px; color: #999; text-align: center">No data</div>
                            </div>
                        </el-col>
                        <el-col :span="8">
                            <div class="homepage_img_left" style="text-align: center" v-if="ExpressionUrl2">
                                <img style="max-width: 100%; max-height: 100%" :src="ExpressionUrl2" />
                            </div>
                            <div class="homepage_img_left" v-show="!ExpressionUrl2">
                                <div style="width: 100%; height: 300px; overflow: hidden; line-height: 300px; font-size: 14px; color: #999; text-align: center">No data</div>
                            </div>
                        </el-col>
                        <el-col :span="8">
                            <div class="homepage_img_left" style="text-align: center" v-if="ExpressionUrl3">
                                <img style="max-width: 100%; max-height: 100%" :src="ExpressionUrl3" />
                            </div>
                            <div class="homepage_img_left" v-show="!ExpressionUrl3">
                                <div style="width: 100%; height: 300px; overflow: hidden; line-height: 300px; font-size: 14px; color: #999; text-align: center">No data</div>
                            </div>
                        </el-col>
                        <!-- <el-col :span="24" v-if="!ExpressionUrl1">
              <div style="width:100%;height:110px;overflow:hidden;line-height:110px;font-size:14px;color:#999;text-align:center;">
                No Data
              </div>
            </el-col> -->
                    </el-row>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import echarts from 'echarts'
import { cross_reference_specie_down, cross_specie_gene_down, cross_specie_expression, cross_specie_gene_expression, cross_specie_violin_box_plot, cross_specie_name_down } from '@/api/api'
import { option1, option2, option3, option2_1, option2_2, option2_3 } from './config'
export default {
    name: 'geneExpression',
    components: {},
    data() {
        return {
            option1,
            option2,
            option3,
            option2_1,
            option2_2,
            option2_3,
            geneExpression_form: {
                species_name: 'Arabidopsis_thaliana',
                // reference: 'Oryza_sativa',
                tissue: 'Root',
                gene_id: 'AT5G50850'
            },
            rules: {
                // species_name: [
                //   { required: true, message: 'Please select', trigger: 'change' }
                // ],
                // tissue: [
                //   { required: true, message: 'Please select', trigger: 'change' }
                // ]
            },
            speciesOptions: [
                // { label: "Arabidopsis thaliana", value: "Arabidopsis_thaliana" },
                // { label: "Oryza sativa", value: "Oryza_sativa" },
                // { label: "Zea mays", value: "Zea_mays" }
            ],
            referenceOptions: [],
            tissueOptions: [
                { label: 'Root', value: 'Root' },
                { label: 'Leaf', value: 'Leaf' }
            ],
            options: [],
            selectLoading: false,
            gene_idOptions: [],
            umapLoading1: false,
            umapLoading2: false,
            umapLoading3: false,
            // Gene expression
            expressionLoading1: false,
            expressionLoading2: false,
            expressionLoading3: false,
            // Expression in cell types
            chartLoading3: false,
            ExpressionUrl1: '',
            ExpressionUrl2: '',
            ExpressionUrl3: '',
            species_name1: '',
            species_name2: '',
            species_name3: '',
            option2_1MinMax: [],
            option2_2MinMax: [],
            option2_3MinMax: []
        }
    },
    mounted() {
        this.init()
        this.showUMAP()
        this.showExpression()
        this.showViolin_box_plot()
    },
    methods: {
        init() {
            // cross_reference_specie_down({ species_name: this.geneExpression_form.species_name }).then(res => {
            //   if (res.code == 200) {
            //     this.referenceOptions = res.data
            //   }
            // });
            cross_specie_name_down().then((res) => {
                if (res.code == 200) {
                    this.speciesOptions = res.data
                }
            })
            cross_specie_gene_down({ species_name: this.geneExpression_form.species_name }).then((res) => {
                if (res.code == 200) {
                    this.gene_idOptions = res.data
                }
            })
        },
        remoteMethod(query) {
            if (query !== '') {
                this.selectLoading = true
                // setTimeout(() => {
                //     this.selectLoading = false
                //     this.options = this.gene_idOptions
                //         .filter((item) => {
                //             return item.label.toLowerCase().indexOf(query.toLowerCase()) > -1
                //         })
                //         .slice(0, 20)
                // }, 200)

                cross_specie_gene_down({ 
                    species_name: this.geneExpression_form.species_name,
                    gene_id: query
                 }).then((res) => {
                    this.selectLoading = false
                    if (res.code == 200) {
                        this.options = res.data
                    }
                })

            } else {
                this.options = []
            }
        },
        species_nameChange() {
            // cross_reference_specie_down({ species_name: this.geneExpression_form.species_name }).then(res => {
            //   if (res.code == 200) {
            //     this.geneExpression_form.reference = ''
            //     this.geneExpression_form.gene_id = ''
            //     this.gene_idOptions = []
            //     this.referenceOptions = res.data
            //   }
            // });
            cross_specie_gene_down({ species_name: this.geneExpression_form.species_name }).then((res) => {
                if (res.code == 200) {
                    this.gene_idOptions = res.data
                    this.geneExpression_form.gene_id = res.data[0] && res.data[0].value
                }
            })
        },
        referenceChange() {},
        search() {
            this.showUMAP()
            this.showExpression()
            this.showViolin_box_plot()
        },
        exampleClick() {
            this.geneExpression_form = {
                species_name: 'Arabidopsis_thaliana',
                // reference: 'Oryza_sativa',
                tissue: 'Root',
                gene_id: 'AT1G50920'
            }
            this.search()
        },
        // UMAP visualization of cell types
        showUMAP() {
            let barChart1 = this.$refs.barChart1
            let barChart2 = this.$refs.barChart2
            let barChart3 = this.$refs.barChart3
            this.umapLoading1 = true
            this.umapLoading2 = true
            this.umapLoading3 = true
            cross_specie_expression({
                species_name: this.geneExpression_form.species_name,
                // reference_name: this.geneExpression_form.reference,
                tissue: this.geneExpression_form.tissue
            }).then((res) => {
                if (res.code == 200) {
                    if (res.data) {
                        if (barChart2) {
                            this.option2.legend.data = []
                            this.option2.series = []
                            res.data.secsend_specie_umap_data &&
                                res.data.secsend_specie_umap_data.forEach((item) => {
                                    this.species_name2 = item.specie
                                    this.option2.legend.data.push(item.name)
                                    this.option2.series.push({
                                        symbolSize: 2,
                                        name: item.name,
                                        type: 'scatter',
                                        data: item.data
                                    })
                                })
                        }
                        if (barChart1) {
                            this.option1.legend.data = []
                            this.option1.series = []
                            res.data.specice_umap_data &&
                                res.data.specice_umap_data.forEach((item) => {
                                    this.species_name1 = item.specie
                                    this.option1.legend.data.push(item.name)
                                    this.option1.series.push({
                                        symbolSize: 2,
                                        name: item.name,
                                        type: 'scatter',
                                        data: item.data
                                    })
                                })
                        }
                        if (barChart3) {
                            this.option3.legend.data = []
                            this.option3.series = []
                            res.data.third_specie_umap_data &&
                                res.data.third_specie_umap_data.forEach((item) => {
                                    this.species_name3 = item.specie
                                    this.option3.legend.data.push(item.name)
                                    this.option3.series.push({
                                        symbolSize: 2,
                                        name: item.name,
                                        type: 'scatter',
                                        data: item.data
                                    })
                                })
                        }
                    }
                    this.Echarts = echarts.init(barChart1)
                    this.Echarts.setOption(this.option1, true)
                    this.umapLoading1 = false
                    this.Echarts = echarts.init(barChart2)
                    this.Echarts.setOption(this.option2, true)
                    this.umapLoading2 = false
                    this.Echarts = echarts.init(barChart3)
                    this.Echarts.setOption(this.option3, true)
                    this.umapLoading3 = false
                }
            })
        },
        // Gene expression
        showExpression() {
            this.expressionLoading1 = true
            this.expressionLoading2 = true
            this.expressionLoading3 = true
            let barChart2_1 = this.$refs.barChart2_1
            let barChart2_2 = this.$refs.barChart2_2
            let barChart2_3 = this.$refs.barChart2_3
            let params = {
                // reference_name: this.geneExpression_form.reference,
                species_name: this.geneExpression_form.species_name,
                tissue: this.geneExpression_form.tissue,
                gene_id: this.geneExpression_form.gene_id
            }
            cross_specie_gene_expression(params).then((res) => {
                if (res.code == 200) {
                    if (res.data) {
                        if (barChart2_2) {
                            this.option2_2.legend.data = []
                            this.option2_2.series = []
                            let option2_2visualMapData = []
                            res.data.reference_data_list &&
                                res.data.reference_data_list.forEach((item) => {
                                    this.option2_2.legend.data.push(item.name.toString())
                                    this.option2_2.series.push({
                                        symbolSize: 2,
                                        name: item.name.toString(),
                                        type: 'scatter',
                                        data: item.data
                                    })
                                    option2_2visualMapData = [...option2_2visualMapData, ...item.data]
                                })
                            this.option2_2MinMax = []
                            option2_2visualMapData.forEach((item) => {
                                this.option2_2MinMax.push(item[2])
                            })




                            this.option2_1.legend.data = []
                            this.option2_1.series = []
                            let option2_1visualMapData = []
                            res.data.species_gene_data &&
                                res.data.species_gene_data.forEach((item) => {
                                    this.option2_1.legend.data.push(item.name)
                                    this.option2_1.series.push({
                                        symbolSize: 2,
                                        name: item.name,
                                        type: 'scatter',
                                        data: item.data
                                    })
                                    option2_1visualMapData = [...option2_1visualMapData, ...item.data]
                                })
                            this.option2_1MinMax = []
                            option2_1visualMapData.forEach((item) => {
                                this.option2_1MinMax.push(item[2])
                            })
                            this.option2_3.legend.data = []
                            this.option2_3.series = []
                            let option2_3visualMapData = []
                            res.data.third_data_list &&
                                res.data.third_data_list.forEach((item) => {
                                    this.option2_3.legend.data.push(item.name)
                                    this.option2_3.series.push({
                                        symbolSize: 2,
                                        name: item.name,
                                        type: 'scatter',
                                        data: item.data
                                    })
                                    option2_3visualMapData = [...option2_3visualMapData, ...item.data]
                                })
                            this.option2_3MinMax = []
                            option2_3visualMapData.forEach((item) => {
                                this.option2_3MinMax.push(item[2])
                            })
                        }
                    }
                    if (this.geneExpression_form.gene_id) {
                        this.option2_2.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#ccc']
                        this.option2_1.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#ccc']
                        this.option2_3.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#ccc']
                        // this.option2_2.color = ['#E15457', '#e1655e', '#df7463', '#de8369', '#dd8e6d', '#dc9d74', '#daac79', '#dab77d', '#d9c583', '#D7DA8B', '#dddeb0', '#ccc']
                        this.option2_1.visualMap = {
                            show: false,
                            top: 'center',
                            right: 'left',
                            orient: 'vertical',
                            min: this.option2_1MinMax.length > 0 ?  Number(Math.min.apply(null, this.option2_1MinMax)) : 0,
                            max: this.option2_1MinMax.length > 0 ?  Number(Math.max.apply(null, this.option2_1MinMax)) : 1,
                            text: [Math.max.apply(null, this.option2_1MinMax).toString(), Math.min.apply(null, this.option2_1MinMax).toString()],
                            dimension: 2,
                            inRange: {
                                color: ['#ccc', '#E15457']
                            },
                            itemGap: 0
                        }
                
                        this.option2_2.visualMap = {
                            show: false,
                            top: 'center',
                            right: 'left',
                            orient: 'vertical',
                            min: 0,
                            max: 1,
                            text: [0, 1],
                            min: this.option2_2MinMax.length > 0 ? Number(Math.min.apply(null, this.option2_2MinMax)) : 0,
                            max: this.option2_1MinMax.length > 0 ?  Number(Math.max(...this.option2_2MinMax)) > Number(Math.min(...this.option2_2MinMax)) ?  Number(Math.max(...this.option2_2MinMax)) :  Number(Math.max(...this.option2_2MinMax)) + 1 : 1,
                            text: [ Number(Math.max(...this.option2_2MinMax)), Math.min.apply(null, this.option2_2MinMax).toString()],
                            dimension: 2,
                            inRange: {
                                color: ['#ccc', '#E15457']
                            },
                            itemGap: 0
                        }


                      
                        // console.log( Number(Math.min(...this.option2_2MinMax)), Number(Math.max(...this.option2_2MinMax)), this.option2_2MinMax)

               
                        this.option2_3.visualMap = {
                            show: false,
                            top: 'center',
                            right: 'left',
                            orient: 'vertical',
                            min: this.option2_3MinMax.length > 0 ? Number(Math.min(...this.option2_3MinMax)) : 0,
                            max: this.option2_3MinMax.length > 0 ?  Number(Math.max(...this.option2_3MinMax)) > Number(Math.min(...this.option2_3MinMax)) ?  Number(Math.max(...this.option2_3MinMax)) :  Number(Math.max(... this.option2_3MinMax)) + 1 : 1,
                            text: [  Number(Math.max(...this.option2_3MinMax)).toString(),  Math.min.apply(null, this.option2_3MinMax).toString()],
                            dimension: 2,
                            inRange: {
                                color: ['#ccc', '#E15457']
                            },
                            itemGap: 0
                        }


                        // this.option2_1.visualMap = Object.assign({}, this.option2_2.visualMap)
                        // this.option2_3.visualMap = Object.assign({}, this.option2_2.visualMap)
                        this.option2_1.legend.show = false
                        this.option2_2.legend.show = false
                        this.option2_3.legend.show = false
                        this.option2_1.visualMap.show = true
                        this.option2_2.visualMap.show = true
                        this.option2_3.visualMap.show = true
                    } else {
                        delete this.option2_2.visualMap
                        delete this.option2_1.visualMap
                        delete this.option2_3.visualMap
                        this.option2_1.legend.show = true
                        this.option2_2.legend.show = true
                        this.option2_3.legend.show = true
                        this.option2_2.color = [
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
                        this.option2_1.color = [
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
                        this.option2_3.color = [
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
                    this.Echarts = echarts.init(barChart2_2)
                    this.Echarts_2 = echarts.init(barChart2_1)
                    this.Echarts_3 = echarts.init(barChart2_3)
                    // this.Echarts_2.resize()
                    this.Echarts.setOption(this.option2_2, true)
                    this.expressionLoading1 = false
                    this.Echarts_2.setOption(this.option2_1, true)
                    this.expressionLoading2 = false
                    this.Echarts_3.setOption(this.option2_3, true)
                    this.expressionLoading3 = false
                }
            })
        },
        // Expression in cell types
        showViolin_box_plot() {
            let params = {
                // reference_name: this.geneExpression_form.reference,
                species_name: this.geneExpression_form.species_name,
                tissue: this.geneExpression_form.tissue,
                gene_id: this.geneExpression_form.gene_id
            }
            this.chartLoading3 = true
            cross_specie_violin_box_plot(params).then((res) => {
                if (res.code == 200) {
                    this.ExpressionUrl1 = res.data.species_violinplot_png
                    this.ExpressionUrl2 = res.data.reference_violinplot_png
                    this.ExpressionUrl3 = res.data.third_specie_violinplot_png

                    this.chartLoading3 = false
                }
            })
        }
    }
}
</script>
<style lang="scss" scoped>
@import './style.scss';
</style>
