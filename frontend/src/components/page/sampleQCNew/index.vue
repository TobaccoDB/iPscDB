<template>
    <div class="sampleQCNew">
        <!-- <div class="crumbs">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/sampleQC' }">Sample QC1</el-breadcrumb-item>
        <el-breadcrumb-item>File Upload</el-breadcrumb-item>
      </el-breadcrumb>
    </div> -->
        <div class="sampleQCNew-inner" v-loading="goLoading" element-loading-text="loading" element-loading-background="#fff">
            <!-- 新增部分 -->
            <div class="scsa">
                <p class="title1" style="margin: 0 0 20px 0">Sample Quality Control</p>
                <el-form ref="formTop" :model="sampleQC_form" :inline="true" :rules="rules">
                    <el-form-item label="Species" prop="species">
                        <el-select style="width: 200px" size="large" v-model="sampleQC_form.species" placeholder="Choose">
                            <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Sample ID" prop="sample_id">
                        <el-input style="width: 200px" v-model="sampleQC_form.sample_id" size="large" placeholder="Please enter"></el-input>
                    </el-form-item>
                    <br />
                    <el-form-item label="File Type">
                        <el-radio-group v-model="sampleQC_form.type">
                            <el-radio label="gz">GZ</el-radio>
                            <el-radio label="rds">RDS</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <br />
                    <el-form-item v-if="sampleQC_form.type == 'rds'" label="RDS" prop="rds_name">
                        <p class="file_p" v-loading="fileLoading">
                            <a href="javascript:;" class="file"
                                >Open File
                                <input type="file" name="file" ref="file" @change="handleUpdate($event)" />
                            </a>
                            <span>{{ sampleQC_form.rds_name }}</span>
                        </p>
                    </el-form-item>
                    <el-form-item v-if="sampleQC_form.type == 'gz'" label="Barcodes" prop="Barcodes_name">
                        <p class="file_p" v-loading="fileLoading1">
                            <!-- <span style="padding:0 12px 0 0;">Barcodes</span> -->
                            <a href="javascript:;" class="file"
                                >Open File
                                <input type="file" name="file" ref="file" @change="handleUpdate1($event)" />
                            </a>
                            <span>{{ sampleQC_form.Barcodes_name }}</span>
                        </p>
                    </el-form-item>
                    <el-form-item v-if="sampleQC_form.type == 'gz'" label="Features" prop="Features_name">
                        <p class="file_p" v-loading="fileLoading2">
                            <a href="javascript:;" class="file"
                                >Open File
                                <input type="file" name="file" ref="file2" @change="handleUpdate2($event)" />
                            </a>
                            <span>{{ sampleQC_form.Features_name }}</span>
                        </p>
                    </el-form-item>
                    <el-form-item v-if="sampleQC_form.type == 'gz'" label="Matrix" prop="Matrix_name">
                        <p class="file_p" v-loading="fileLoading3">
                            <a href="javascript:;" class="file"
                                >Open File
                                <input type="file" name="file" ref="file3" @change="handleUpdate3($event)" />
                            </a>
                            <span>{{ sampleQC_form.Matrix_name }}</span>
                        </p>
                    </el-form-item>
                </el-form>
                <el-row style="border-bottom: 1px solid #aaa; padding-bottom: 20px">
                    <!-- <el-button class="btnSearch" @click="example">Example</el-button> -->
                    <el-button class="btnSearch" style="width: 80px" @click="search">GO</el-button>
                    <el-button class="btnReset" @click="reset">Reset</el-button>
                </el-row>
            </div>

            <p v-if="isInit" class="Note">Note: {{ $route.query.species }}_{{ $route.query.dataset }}.rds file has been uploaded.</p>
            <p class="title1">Cells uploaded {{ backVal2 }}</p>
            <div style="" class="UMAP" v-if="isShowpic">
                <img :src="url" width="100%" />
            </div>
            <div style="position: relative; top: -42px; background: #fff; padding-top: 30px">
                <ul class="sample_table">
                    <li></li>
                    <li>nCount_RNA</li>
                    <li>nFeatuer_RNA</li>
                    <li>percent.mt</li>
                    <li>percent.pt</li>
                </ul>
                <ul class="sample_table">
                    <li>min</li>
                    <li>{{ min.min_nCount_RNA }}</li>
                    <li>{{ min.min_nFeature_RNA }}</li>
                    <li>{{ min.min_percent_mt }}</li>
                    <li>{{ min.min_percent_pt }}</li>
                </ul>
                <ul class="sample_table">
                    <li>max</li>
                    <li>{{ max.max_nCount_RNA }}</li>
                    <li>{{ max.max_nFeature_RNA }}</li>
                    <li>{{ max.max_percent_mt }}</li>
                    <li>{{ max.max_percent_pt }}</li>
                </ul>
            </div>
            <p class="title2">QC filter</p>
            <el-form class="form1" ref="form1" :inline="true" :model="form" label-width="140px">
                <el-row :gutter="20">
                    <el-col :span="6">
                        <div class="grid-content bg-purple">
                            <el-form-item label="min nCount_RNA" prop="min_nCount_RNA">
                                <el-input style="width: 120px" v-model="form.min_nCount_RNA"></el-input>
                            </el-form-item>
                            <el-form-item label="max nCount_RNA" prop="max_nCount_RNA">
                                <el-input style="width: 120px" v-model="form.max_nCount_RNA"></el-input>
                            </el-form-item>
                        </div>
                    </el-col>
                    <el-col :span="6">
                        <div class="grid-content bg-purple">
                            <el-form-item label="min nFeatuer_RNA" prop="min_nFeature_RNA">
                                <el-input style="width: 120px" v-model="form.min_nFeature_RNA"></el-input>
                            </el-form-item>
                            <el-form-item label="max nFeatuer_RNA" prop="max_nFeature_RNA">
                                <el-input style="width: 120px" v-model="form.max_nFeature_RNA"></el-input>
                            </el-form-item>
                        </div>
                    </el-col>
                    <el-col :span="6">
                        <div class="grid-content bg-purple">
                            <el-form-item label="min percent.mt" prop="min_percent_mt">
                                <el-input style="width: 120px" v-model="form.min_percent_mt"></el-input>
                            </el-form-item>
                            <el-form-item label="max percent.mt" prop="max_percent_mt">
                                <el-input style="width: 120px" v-model="form.max_percent_mt"></el-input>
                            </el-form-item>
                        </div>
                    </el-col>
                    <el-col :span="6">
                        <div class="grid-content bg-purple">
                            <el-form-item label="min percent.pt" prop="min_percent_pt">
                                <el-input style="width: 120px" v-model="form.min_percent_pt"></el-input>
                            </el-form-item>
                            <el-form-item label="max percent.pt" prop="max_percent_pt">
                                <el-input style="width: 120px" v-model="form.max_percent_pt"></el-input>
                            </el-form-item>
                        </div>
                    </el-col>
                </el-row>

                <el-form-item style="width: 100%" label="">
                    <el-button type="primary" @click="RunQC">Run QC</el-button>
                </el-form-item>
            </el-form>
            <!-- <ul class="scsa_bottom_ul" v-if="isShowGenesCells">
        <li>Genes: {{backVal1}} Cells: {{backVal2}}
          <span class="statusSpan2">QC Pass
          </span>
        </li>
      </ul> -->
        </div>
    </div>
</template>

<script>
import axios from '@/api/http.js'
import Axios from 'axios'
//顶部页面加载条
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
NProgress.configure({
    easing: 'ease',
    speed: 500,
    showSpinner: false,
    trickleSpeed: 200,
    minimum: 0.3
})
import { plant_search_down, sample_qc_uuid, sample_qc_upload, sample_qc_upload_picture, cell_identification_reference_detail } from '@/api/api'
export default {
    name: 'sampleQCNew',
    components: {},
    data() {
        return {
            speciesOptions: [],
            tissue: 'Root',
            sampleQC_form: {
                species: '',
                type: 'rds',
                rds_name: '',
                sample_id: '',
                Barcodes_name: '',
                Features_name: '',
                Matrix_name: ''
            },
            rules: {
                species: [{ required: true, message: 'Please select', trigger: 'change' }],
                sample_id: [{ required: true, message: 'Please enter', trigger: 'blur' }],
                rds_name: [{ required: true, message: 'Please select', trigger: 'change' }],
                Barcodes_name: [{ required: true, message: 'Please select', trigger: 'change' }],
                Features_name: [{ required: true, message: 'Please select', trigger: 'change' }],
                Matrix_name: [{ required: true, message: 'Please select', trigger: 'change' }]
            },
            file: '',
            file1: '',
            file2: '',
            file3: '',
            loading: false,
            qcUuid: 'example',
            fileLoading: false,
            fileLoading1: false,
            fileLoading2: false,
            fileLoading3: false,
            min: {
                min_nCount_RNA: '',
                min_nFeature_RNA: '',
                min_percent_mt: '',
                min_percent_pt: ''
            },
            max: {
                max_nCount_RNA: '',
                max_nFeature_RNA: '',
                max_percent_mt: '',
                max_percent_pt: ''
            },
            form: {
                min_nCount_RNA: '',
                max_nCount_RNA: '',
                min_nFeature_RNA: '',
                max_nFeature_RNA: '',
                min_percent_mt: '',
                max_percent_mt: '',
                min_percent_pt: '',
                max_percent_pt: ''
            },
            isShowGenesCells: false,
            goLoading: false,
            backVal1: '',
            backVal2: '',
            url: '',
            isShowpic: true,
            isInit: true,
            baseUrl: process.env.VUE_APP_BASE_URL
        }
    },
    mounted() {
        this.sampleQC_form.species = this.$route.query.species
        this.sampleQC_form.sample_id = this.$route.query.dataset
        this.init()
    },
    methods: {
        init() {
            NProgress.start()
            plant_search_down({}).then((res) => {
                if (res.code == 200) {
                    this.speciesOptions = res.data
                }
            })
            sample_qc_uuid({}).then((res) => {
                if (res.code == 200) {
                    this.qcUuid = res.data[0]
                }
            })
            let params = {
                files_uuid: 'example',
                file_type: 'example',
                sample_id: this.$route.query.dataset
                // files_uuid: this.$route.query.files_uuid,
                // file_type: this.$route.query.file_type,
                // sample_id: this.$route.query.sample_id,
                // filter_min_Feature_RNA_cutmin: this.form.min_nFeature_RNA,
                // filter_min_mt_cutmin: this.form.min_percent_mt,
                // filter_min_pt_cutmin: this.form.min_percent_pt,
                // filter_max_Feature_RNA_cutax: this.form.max_nFeature_RNA,
                // filter_max_mt_cutmax: this.form.max_percent_mt,
                // filter_max_pt_cutmax: this.form.max_percent_pt,
                // min_nFeature_RNA: this.form.min_nFeature_RNA,
                // min_percent_mt: this.form.min_percent_mt,
                // min_percent_pt: this.form.min_percent_pt,
                // max_nFeature_RNA: this.form.max_nFeature_RNA,
                // max_percent_mt: this.form.max_percent_mt,
                // max_percent_pt: this.form.max_percent_pt,
            }
            this.goLoading = true
            // sample_qc_upload_picture(params).then(res => {
            let res = {
                data: ''
            }
            res.data = {
                min_nFeature_RNA: '245',
                max_nFeature_RNA: '10377',
                min_nCount_RNA: '500',
                max_nCount_RNA: '170328',
                min_percent_mt: '0',
                max_percent_mt: '17.50742',
                min_percent_pt: '0',
                max_percent_pt: '11.00746',
                filter_min_Feature_RNA_cutmin: '-298.9358',
                filter_max_Feature_RNA_cutax: '5677.252',
                filter_min_nCount_RNA: '500',
                filter_max_nCount_RNA: '170328',
                filter_min_mt_cutmin: '0',
                filter_max_mt_cutmax: '1.152455',
                filter_min_pt_cutmin: '0',
                filter_max_pt_cutmax: '0.3690952',
                result: '[1] 245\n[1] 10377\n[1] 500\n[1] 170328\n[1] 0\n[1] 17.50742\n[1] 0\n[1] 11.00746\n[1] -298.9358\n[1] 5677.252\n[1] 500\n[1] 170328\n[1] 0\n[1] 1.152455\n[1] 0\n[1] 0.3690952\n',
                picture: this.baseUrl + '/Sample_QC/qc_picture/example.svg'
            }
            // if (res.code == 200) {
            this.url = res.data.picture
            this.min = {
                min_nCount_RNA: res.data.min_nCount_RNA,
                min_nFeature_RNA: res.data.min_nFeature_RNA,
                min_percent_mt: res.data.min_percent_mt,
                min_percent_pt: res.data.min_percent_pt
            }
            this.max = {
                max_nCount_RNA: res.data.max_nCount_RNA,
                max_nFeature_RNA: res.data.max_nFeature_RNA,
                max_percent_mt: res.data.max_percent_mt,
                max_percent_pt: res.data.max_percent_pt
            }
            this.goLoading = false

            // this.backText = res.data.result
            // this.backVal1 = res.data.genes
            // this.backVal2 = res.data.cells
            NProgress.done()
            this.form = {
                min_nCount_RNA: res.data.filter_min_nCount_RNA < res.data.min_nCount_RNA ? res.data.min_nCount_RNA : res.data.filter_min_nCount_RNA,
                min_nFeature_RNA: res.data.filter_min_Feature_RNA_cutmin < res.data.min_nFeature_RNA ? res.data.min_nFeature_RNA : res.data.filter_min_Feature_RNA_cutmin,
                min_percent_mt: res.data.filter_min_mt_cutmin < res.data.min_percent_mt ? res.data.min_percent_mt : res.data.filter_min_mt_cutmin,
                min_percent_pt: res.data.filter_min_pt_cutmin < res.data.min_percent_pt ? res.data.min_percent_pt : res.data.filter_min_pt_cutmin,
                max_nCount_RNA: res.data.filter_max_nCount_RNA,
                max_nFeature_RNA: res.data.filter_max_Feature_RNA_cutax,
                max_percent_mt: res.data.filter_max_mt_cutmax,
                max_percent_pt: res.data.filter_max_pt_cutmax
            }
            // }
            // });
        },
        RunQC() {
            sessionStorage.removeItem('sampleFrom')
            sessionStorage.setItem(
                'sampleFrom',
                JSON.stringify({
                    filter_min_Feature_RNA_cutmin: this.form.min_nFeature_RNA,
                    filter_min_mt_cutmin: this.form.min_percent_mt,
                    filter_min_pt_cutmin: this.form.min_percent_pt,
                    filter_max_Feature_RNA_cutax: this.form.max_nFeature_RNA,
                    filter_max_mt_cutmax: this.form.max_percent_mt,
                    filter_max_pt_cutmax: this.form.max_percent_pt
                })
            )
            this.$router.push({
                path: '/sampleQCFilter',
                query: {
                    species_name: this.sampleQC_form.species,
                    tissue: this.tissue,
                    // species_name: this.$route.query.species_name,
                    // tissue: this.$route.query.tissue,
                    files_uuid: this.isInit ? 'example' : this.qcUuid,
                    file_type: this.sampleQC_form.type,
                    sample_id: this.sampleQC_form.sample_id,
                    // files_uuid: 'example',
                    // file_type: 'example',
                    // sample_id: 'GSM4212552',
                    pageType: 'QCNew'
                }
            })
            // NProgress.start();
            // let params = {
            //   files_uuid: this.$route.query.files_uuid,
            //   sample_id: this.$route.query.sample_id,
            //   file_type: 'filter',
            //   filter_min_Feature_RNA_cutmin: this.form.min_nFeature_RNA,
            //   filter_min_mt_cutmin: this.form.min_percent_mt,
            //   filter_min_pt_cutmin: this.form.min_percent_pt,
            //   filter_max_Feature_RNA_cutax: this.form.max_nFeature_RNA,
            //   filter_max_mt_cutmax: this.form.max_percent_mt,
            //   filter_max_pt_cutmax: this.form.max_percent_pt,
            // }
            // this.goLoading = true
            // this.isShowpic = false
            // sample_qc_upload_picture(params).then(res => {
            //   if (res.code == 200) {
            //     if (res.data.picture == '') {
            //       this.$message(res.data.result);
            //     } else {
            //       this.url = res.data.picture
            //       this.backVal1 = res.data.genes
            //       this.backVal2 = res.data.cells
            //       this.isShowGenesCells = true
            //     }
            //     NProgress.done()
            //     this.goLoading = false
            //     this.isShowpic = true
            //   }
            // });
        },
        example() {
            this.$router.push({
                path: '/sampleDetails',
                query: {
                    species_name: this.sampleQC_form.species,
                    tissue: this.tissue,
                    sample_id: this.$route.query.dataset,
                    files_uuid: 'example',
                    file_type: 'example'
                }
            })
        },
        search() {
            if (this.sampleQC_form.type == 'rds' && (this.sampleQC_form.rds_name == '' || this.sampleQC_form.species == '')) {
                this.$message.warning('Please upload a file！')
                return
            }
            if (
                this.sampleQC_form.type == 'gz' &&
                (this.sampleQC_form.Barcodes_name == '' || this.sampleQC_form.Features_name == '' || this.sampleQC_form.Matrix_name == '' || this.sampleQC_form.species == '')
            ) {
                this.$message.warning('Please upload a file！')
                return
            }
            if (this.fileLoading || this.fileLoading1 || this.fileLoading2 || this.fileLoading3) {
                this.$message.warning('Please wait for the file to upload！')
                return
            }
            // this.$router.push({
            //   path: '/sampleDetails',
            //   query: {
            //     species_name: this.sampleQC_form.species,
            //     tissue: this.tissue,
            //     files_uuid: this.qcUuid,
            //     sample_id: this.sampleQC_form.sample_id,
            //     file_type: this.sampleQC_form.type
            //   }
            // })
            NProgress.start()
            let params = {
                files_uuid: this.qcUuid,
                file_type: this.sampleQC_form.type,
                sample_id: this.sampleQC_form.sample_id
                // filter_min_Feature_RNA_cutmin: this.form.min_nFeature_RNA,
                // filter_min_mt_cutmin: this.form.min_percent_mt,
                // filter_min_pt_cutmin: this.form.min_percent_pt,
                // filter_max_Feature_RNA_cutax: this.form.max_nFeature_RNA,
                // filter_max_mt_cutmax: this.form.max_percent_mt,
                // filter_max_pt_cutmax: this.form.max_percent_pt,
                // min_nFeature_RNA: this.form.min_nFeature_RNA,
                // min_percent_mt: this.form.min_percent_mt,
                // min_percent_pt: this.form.min_percent_pt,
                // max_nFeature_RNA: this.form.max_nFeature_RNA,
                // max_percent_mt: this.form.max_percent_mt,
                // max_percent_pt: this.form.max_percent_pt,
            }
            this.goLoading = true
            sample_qc_upload_picture(params).then((res) => {
                if (res.code == 200) {
                    this.url = res.data.picture
                    this.min = {
                        min_nCount_RNA: res.data.min_nCount_RNA,
                        min_nFeature_RNA: res.data.min_nFeature_RNA,
                        min_percent_mt: res.data.min_percent_mt,
                        min_percent_pt: res.data.min_percent_pt
                    }
                    this.max = {
                        max_nCount_RNA: res.data.max_nCount_RNA,
                        max_nFeature_RNA: res.data.max_nFeature_RNA,
                        max_percent_mt: res.data.max_percent_mt,
                        max_percent_pt: res.data.max_percent_pt
                    }
                    this.goLoading = false

                    // this.backText = res.data.result
                    // this.backVal1 = res.data.genes
                    // this.backVal2 = res.data.cells
                    NProgress.done()
                    this.form = {
                        min_nCount_RNA: res.data.filter_min_nCount_RNA < res.data.min_nCount_RNA ? res.data.min_nCount_RNA : res.data.filter_min_nCount_RNA,
                        min_nFeature_RNA: res.data.filter_min_Feature_RNA_cutmin < res.data.min_nFeature_RNA ? res.data.min_nFeature_RNA : res.data.filter_min_Feature_RNA_cutmin,
                        min_percent_mt: res.data.filter_min_mt_cutmin < res.data.min_percent_mt ? res.data.min_percent_mt : res.data.filter_min_mt_cutmin,
                        min_percent_pt: res.data.filter_min_pt_cutmin < res.data.min_percent_pt ? res.data.min_percent_pt : res.data.filter_min_pt_cutmin,
                        max_nCount_RNA: res.data.filter_max_nCount_RNA,
                        max_nFeature_RNA: res.data.filter_max_Feature_RNA_cutax,
                        max_percent_mt: res.data.filter_max_mt_cutmax,
                        max_percent_pt: res.data.filter_max_pt_cutmax
                    }
                }
            })
        },
        reset() {
            this.file = ''
            this.file2 = ''
            this.file3 = ''
            this.sampleQC_form = {
                type: 'rds',
                species: 'Arabidopsis_thaliana',
                sample_id: this.$route.query.dataset,
                Barcodes_name: '',
                Features_name: '',
                Matrix_name: ''
            }
            this.backText = ''
            this.backVal1 = ''
            this.backVal2 = ''
            this.loading = false
            this.isInit = true
            this.$refs['formTop'].resetFields()
        },
        handleUpdate(event) {
            if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'rds') {
                this.$message.warning('Please upload .rds file！')
            } else {
                this.isInit = false
                this.sampleQC_form.rds_name = event.target.files[0].name
                this.fileLoading = true
                this.openFile(this.qcUuid, event.target.files[0], 4, 'Rds')
            }
        },
        handleUpdate1(event) {
            if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'gz') {
                this.$message.warning('Please upload .gz file！')
            } else {
                this.isInit = false
                this.sampleQC_form.Barcodes_name = event.target.files[0].name
                this.fileLoading1 = true
                this.openFile(this.qcUuid, event.target.files[0], 1, 'Barcodes')
            }
        },
        handleUpdate2(event) {
            if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'gz') {
                this.$message.warning('Please upload .gz file！')
            } else {
                this.isInit = false
                this.sampleQC_form.Features_name = event.target.files[0].name
                this.fileLoading2 = true
                this.openFile(this.qcUuid, event.target.files[0], 2, 'Features')
            }
        },
        handleUpdate3(event) {
            if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'gz') {
                this.$message.warning('Please upload .gz file！')
            } else {
                this.isInit = false
                this.sampleQC_form.Matrix_name = event.target.files[0].name
                this.fileLoading3 = true
                this.openFile(this.qcUuid, event.target.files[0], 3, 'Matrix')
            }
        },
        openFile(uuid, file, type, name) {
            this.$refs['formTop'].validate((valid) => {})
            let formData = new FormData()
            formData.append('files_uuid', uuid)
            formData.append('myfile', file)
            formData.append('file_name', name)
            formData.append('file_type', this.sampleQC_form.type)
            let config = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
            const $axios = Axios.create({
                baseURL: axios.defaults.baseURL,
                timeout: 1000000
            })

            $axios
                .post('/api/v1/sample_qc_upload_picture/', formData, config)
                .then((res) => {
                    // $axios.post('/api/v1/sample_qc_upload/', formData, config).then(res => {
                    if (res.data.code == 200) {
                        if (type == 4) {
                            this.file = file
                        } else if (type == 1) {
                            this.file1 = file
                        } else if (type == 2) {
                            this.file2 = file
                        } else {
                            this.file3 = file
                        }
                        this.$message.success(res.data.data.msg)
                    } else {
                        this.$message.warning(res.data.msg)
                    }
                    this.fileLoading = false
                    this.fileLoading1 = false
                    this.fileLoading2 = false
                    this.fileLoading3 = false
                })
                .catch((err) => {
                    this.$message.warning(err.data.msg)
                })
        }
    }
}
</script>
<style lang="scss" scoped>
@import './style.scss';
</style>
