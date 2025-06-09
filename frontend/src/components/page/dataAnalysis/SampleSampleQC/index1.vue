<template>
  <div class="SampleSampleQC">
    <div class="SampleSampleQC-inner">
      <div class="stepBar">
        <el-steps :active="stepActive" finish-status="success" :align-center="true">
          <el-step :style="{ cursor: index <= stepActive ? 'pointer' : 'auto' }" @click.native="setpClick(item, index)" :title="item.name"
            v-for="(item, index) in stepList"></el-step>
        </el-steps>
      </div>
      <div class="blast" v-if="isShowQC">
        <!--                       Sample QC                       -->
        <el-header>Sample QC</el-header>
        <el-form ref="formTop" :inline="true" v-if="isNewJob  && !$route.query.uuid" :model="formTop" :rules="formTopRules">
          <el-form-item label="Email" prop="email">
            <el-input style="width: 177px" v-model="formTop.email" placeholder="Please enter"></el-input>
          </el-form-item>
          <el-form-item label="Analysis name">
            <el-input style="width: 177px" v-model="formTop.analysis_name" placeholder="Please enter"></el-input>
          </el-form-item>
          <el-form-item label="Species" prop="species_name">
            <el-select style="width: 177px" v-model="formTop.species_name" @change="speciesChange" placeholder="Please choose">
              <el-option v-for="(item, index) in speciesList" :key="index" :label="item.name" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Tissue" prop="transcriptome">
            <el-select style="width: 177px" v-model="formTop.transcriptome" placeholder="Please choose">
              <el-option v-for="(item, index) in TranscriptomeList" :key="index" :label="item.name" :value="item.name"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="">
            <el-button class="btnSearch" @click="newJob" :disabled="!isNewJob">new job</el-button>
          </el-form-item>
        </el-form>
        <div :style={opacity:opacity} v-loading="fileLoading">
          <el-form ref="formFile1" :model="formFile1" :inline="true" :rules="rules">
            <el-header>Data1</el-header>
            <el-form-item label="Sample Name" prop="data1_sample_name">
              <el-input style="width: 177px" v-model="formFile1.data1_sample_name" placeholder="Please enter" :disabled="isNewJob"></el-input>
            </el-form-item>
            <el-form-item label="File Type">
              <el-radio-group v-model="formFile1.type" :disabled="isNewJob">
                <el-radio label="gz">GZ</el-radio>
                <el-radio label="h5">H5AD</el-radio>
              </el-radio-group>
            </el-form-item>
            <br />
            <el-form-item v-if="formFile1.type == 'h5'" label="H5AD" prop="filtered_feature_bc_matrix">
              <p class="file_p">
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file" :disabled="isNewJob" @change="handleUpdate1($event, 'filtered_feature_bc_matrix')"
                  />
                </a>
                <span style="width:1000px">{{ formFile1.filtered_feature_bc_matrix }}</span>
              </p>
            </el-form-item>
            <el-form-item v-if="formFile1.type == 'gz'" label="Barcodes" prop="barcodes">
              <p class="file_p">
                <!-- <span style="padding:0 12px 0 0;">Barcodes</span> -->
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file" :disabled="isNewJob" @change="handleUpdate1($event, 'barcodes')" />
                </a>
                <el-tooltip class="item" effect="dark" :content="formFile1.barcodes" placement="top">
                  <span>{{ formFile1.barcodes }}</span>
                </el-tooltip>
              </p>
            </el-form-item>
            <el-form-item v-if="formFile1.type == 'gz'" label="Features" prop="features">
              <p class="file_p">
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file2" :disabled="isNewJob" @change="handleUpdate1($event, 'features')" />
                </a>
                <el-tooltip class="item" effect="dark" :content="formFile1.features" placement="top">
                  <span>{{ formFile1.features }}</span>
                </el-tooltip>
              </p>
            </el-form-item>
            <el-form-item v-if="formFile1.type == 'gz'" label="Matrix" prop="matrix">
              <p class="file_p">
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file3" :disabled="isNewJob" @change="handleUpdate1($event, 'matrix')" />
                </a>
                <el-tooltip class="item" effect="dark" :content="formFile1.matrix" placement="top">
                  <span>{{ formFile1.matrix }}</span>
                </el-tooltip>
              </p>
            </el-form-item>
          </el-form>
          <el-header>Data2</el-header>
          <el-form ref="formFile2" :model="formFile2" :inline="true" :rules="rules">
            <el-form-item label="Sample Name" prop="data2_sample_name">
              <el-input style="width: 177px" v-model="formFile2.data2_sample_name" placeholder="Please enter" :disabled="isNewJob"></el-input>
            </el-form-item>
            <el-form-item label="File Type">
              <el-radio-group v-model="formFile2.type" :disabled="isNewJob">
                <el-radio label="gz">GZ</el-radio>
                <el-radio label="h5">H5AD</el-radio>
              </el-radio-group>
            </el-form-item>
            <br />
            <el-form-item v-if="formFile2.type == 'h5'" label="H5AD" prop="filtered_feature_bc_matrix">
              <p class="file_p">
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file" :disabled="isNewJob" @change="handleUpdate2($event, 'filtered_feature_bc_matrix')"
                  />
                </a>
                <span style="width:1000px">{{ formFile2.filtered_feature_bc_matrix }}</span>
              </p>
            </el-form-item>
            <el-form-item v-if="formFile2.type == 'gz'" label="Barcodes" prop="barcodes">
              <p class="file_p">
                <!-- <span style="padding:0 12px 0 0;">Barcodes</span> -->
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file" :disabled="isNewJob" @change="handleUpdate2($event, 'barcodes')" />
                </a>
                <el-tooltip class="item" effect="dark" :content="formFile2.barcodes" placement="top">
                  <span>{{ formFile2.barcodes }}</span>
                </el-tooltip>
              </p>
            </el-form-item>
            <el-form-item v-if="formFile2.type == 'gz'" label="Features" prop="features">
              <p class="file_p">
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file2" :disabled="isNewJob" @change="handleUpdate2($event, 'features')" />
                </a>
                <el-tooltip class="item" effect="dark" :content="formFile2.features" placement="top">
                  <span>{{ formFile2.features }}</span>
                </el-tooltip>
              </p>
            </el-form-item>
            <el-form-item v-if="formFile2.type == 'gz'" label="Matrix" prop="matrix">
              <p class="file_p">
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file3" :disabled="isNewJob" @change="handleUpdate2($event, 'matrix')" />
                </a>
                <el-tooltip class="item" effect="dark" :content="formFile2.matrix" placement="top">
                  <span>{{ formFile2.matrix }}</span>
                </el-tooltip>
              </p>
            </el-form-item>
          </el-form>

          <el-form :style={opacity:opacity} ref="formBottom" :inline="true" :model="formBottom" :rules="formBottomRules">
            <el-form-item label="pt" prop="pt">
              <el-input v-model="formBottom.pt" :disabled="isNewJob && !$route.query.uuid" clearable placeholder="Please enter"></el-input>
            </el-form-item>
            <el-form-item label="mt" prop="mt">
              <el-input v-model="formBottom.mt" :disabled="isNewJob && !$route.query.uuid" clearable placeholder="Please enter"></el-input>
            </el-form-item>
            <br />
            <el-form-item label="">
              <el-button class="btnSearch" :loading="runLoading" :disabled="isNewJob && !$route.query.uuid" @click="runQC('qc')">Run QC</el-button>
              <!-- <el-button :disabled="isNewJob && !$route.query.uuid" @click="runQC('qcResult')">Run QC result</el-button> -->
              <el-button v-if="$route.query.uuid" :loading="runLoading" @click="runQC('qcResult')">Run QC result</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
      <!--              Sample QC Result                   -->
      <div class="blast" v-if="!isShowResult&& !isShowQC">
        <el-header>Data1</el-header>
        <div style="">
          <ul class="sample_table">
            <li></li>
            <li>nCount_RNA</li>
            <li>nFeatuer_RNA</li>
            <li>percent.mt</li>
            <li>percent.pt</li>
          </ul>
          <ul class="sample_table">
            <li>min</li>
            <li>{{ data1.min_nCount_RNA }}</li>
            <li>{{ data1.min_nFeature_RNA }}</li>
            <li>{{ data1.min_percent_mt }}</li>
            <li>{{ data1.min_percent_pt }}</li>
          </ul>
          <ul class="sample_table">
            <li>max</li>
            <li>{{ data1.max_nCount_RNA }}</li>
            <li>{{ data1.max_nFeature_RNA }}</li>
            <li>{{ data1.max_percent_mt }}</li>
            <li>{{ data1.max_percent_pt }}</li>
          </ul>
        </div>
        <el-header>Data2</el-header>
        <div style="">
          <ul class="sample_table">
            <li></li>
            <li>nCount_RNA</li>
            <li>nFeatuer_RNA</li>
            <li>percent.mt</li>
            <li>percent.pt</li>
          </ul>
          <ul class="sample_table">
            <li>min</li>
            <li>{{ data2.min_nCount_RNA }}</li>
            <li>{{ data2.min_nFeature_RNA }}</li>
            <li>{{ data2.min_percent_mt }}</li>
            <li>{{ data2.min_percent_pt }}</li>
          </ul>
          <ul class="sample_table">
            <li>max</li>
            <li>{{ data2.max_nCount_RNA }}</li>
            <li>{{ data2.max_nFeature_RNA }}</li>
            <li>{{ data2.max_percent_mt }}</li>
            <li>{{ data2.max_percent_pt }}</li>
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
        </el-form>
        <div style="margin-top:20px;">
          <el-button class="btnSearch" @click="implement">Run QC fliter</el-button>
          <el-button @click="jumpResultPage">Result</el-button>
        </div>
      </div>
      <!-- QC Filter Result -->
      <SampleQCResult :parent-msg="resultData" v-if="isShowResult"></SampleQCResult>
    </div>
  </div>
</template>

<script>
import axios from '@/api/analysisHttp.js';
import Axios from 'axios'
import { analysis_new_job, specie_down_box, sqmpleQcDataShow, sample_qc_upload_show, qc_filter_data_show, sample_qc, qc_filter_data_result, specie_tissue_down_box } from '@/api/analysis'
import SampleQCResult from '@/components/page/dataAnalysis/SampleQCResult/index'

export default {
  name: 'SampleSampleQC',
  components: {
    SampleQCResult
  },
  data() {
    return {
      stepActive: 0,
      stepList: [
        { name: 'Sample QC', link: 'SampleSampleQC', step: 'sample_qc' },
        { name: 'Data Process', link: 'DataProcess', step: 'data_process' },
        { name: 'Cluster', link: 'Cluster', step: 'cluster' },
        { name: 'Cell Annotation', link: 'DataAnalysisCellAnnotation', step: 'cell_annotation' },
      ],
      formTop: {
        email: '',
        analysis_name: '',
        species_name: '',
        transcriptome: '',
      },
      formTopRules: {
        email: [
          { required: true, message: 'Please enter your email address', trigger: 'blur' },
          { type: 'email', message: 'Please enter the correct email address', trigger: ['blur', 'change'] }
        ],
        species_name: [
          { required: true, message: 'Please choose', trigger: 'change' }
        ],
        transcriptome: [
          { required: true, message: 'Please choose', trigger: 'change' }
        ],
      },
      rules: {
        filtered_feature_bc_matrix: [{ required: true, message: 'Please select', trigger: 'change' }],
        barcodes: [{ required: true, message: 'Please select', trigger: 'change' }],
        features: [{ required: true, message: 'Please select', trigger: 'change' }],
        matrix: [{ required: true, message: 'Please select', trigger: 'change' }],
        data1_sample_name: [
          { required: true, message: 'Please enter', trigger: ["blur", "change"] },
        ],
        data2_sample_name: [
          { required: true, message: 'Please enter', trigger: ["blur", "change"] },
        ],
      },
      speciesList: [],
      TranscriptomeList: [],
      isShowResult: false,
      isNewJob: true,
      opacity: 0.4,
      isShowQC: true,
      upload_id: '',
      tissue: 'Root',
      formFile1: {
        data1_sample_name: '',
        type: 'gz',
        filtered_feature_bc_matrix: '',
        barcodes: '',
        features: '',
        matrix: ''
      },
      formFile2: {
        data2_sample_name: '',
        type: 'gz',
        filtered_feature_bc_matrix: '',
        barcodes: '',
        features: '',
        matrix: ''
      },
      file: '',
      file1: '',
      file2: '',
      file3: '',
      formBottom: {
        pt: '',
        mt: '',
      },
      formBottomRules: {
        pt: [
          { required: true, message: 'Please enter', trigger: 'blur' },
        ],
        mt: [
          { required: true, message: 'Please enter', trigger: 'blur' },
        ],
      },
      // Sample QC Result
      data1: {
        min_nCount_RNA: '',
        min_nFeature_RNA: '',
        min_percent_mt: '',
        min_percent_pt: '',
        max_nCount_RNA: '',
        max_nFeature_RNA: '',
        max_percent_mt: '',
        max_percent_pt: ''
      },
      data2: {
        min_nCount_RNA: '',
        min_nFeature_RNA: '',
        min_percent_mt: '',
        min_percent_pt: '',
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
      resultData: {},
      fileLoading: false,
      runLoading: false,
    }
  },
  mounted() {
    if (this.$route.query.uuid) {
      this.upload_id = this.$route.query.uuid
      this.isNewJob = true
      this.opacity = 1
      this.sample_qc_upload_show()
      this.stepList.forEach((item, index) => {
        if (this.$route.query.step == item.step) {
          this.stepActive = index
          if (this.$route.query.step == 'cell_annotation') {
            this.stepActive = Number(this.stepActive) + 1
          }
        }
      });
    } else {
      this.getSpecie_down_box()
      this.isNewJob = true
      this.opacity = 0.4
    }
  },
  methods: {
    setpClick(item, index) {
      if (index < this.stepActive || index == this.stepActive) {
        this.$router.push({
          path: '/' + item.link,
          query: {
            uuid: this.$route.query.uuid,
            id: this.$route.query.id,
            step: this.$route.query.step,
            from: this.$route.query.from,
          }
        })
        this.isShowResult = false
        this.isShowQC = true
      }
    },
    getSpecie_down_box() {
      specie_down_box({ type: 'species' }).then((res) => {
        if (res.code == 200) {
          this.speciesList = res.data
        }
      })
    },
    speciesChange(val) {
      specie_tissue_down_box({ species_name: val }).then((res) => {
        if (res.code == 200) {
          this.formTop.transcriptome = ''
          this.TranscriptomeList = res.data
        }
      })
    },
    sample_qc_upload_show() {
      sample_qc_upload_show({ uuid: this.upload_id }).then((res) => {
        if (res.code == 200) {
          this.formFile1.data1_sample_name = res.data.results[0].data1_sample_name
          this.formFile2.data2_sample_name = res.data.results[0].data2_sample_name
          this.formFile1.type = res.data.results[0].data1_type
          this.formFile2.type = res.data.results[0].data2_type
          this.formBottom.mt = res.data.results[0].mt
          this.formBottom.pt = res.data.results[0].pt
          res.data.results[0].file_name && res.data.results[0].file_name.forEach(item => {
            if (item.data_type == 'data1') {
              this.formFile1[item.file_name.split('.')[0]] = item.file_source_name
            } else {
              this.formFile2[item.file_name.split('.')[0]] = item.file_source_name
            }
          });
        }
      })
    },
    newJob() {
      this.$refs['formTop'].validate((valid) => {
        if (valid) {
          analysis_new_job(Object.assign({}, this.formTop, { source: 'sample_qc' })).then((res) => {
            if (res.code == 200) {
              this.upload_id = res.data
              this.isNewJob = false
              this.opacity = 1
              this.species = this.formTop.species_name
              this.transcriptome = this.formTop.transcriptome
              this.$message.success('new Job successfully!')
            }
          })

        } else {
          return false;
        }
      });
    },
    handleUpdate1(event, file_name) {
      if (this.formFile1.data1_sample_name == '') {
        this.$message('Please Choose sample name!')
        event.target.value = ""
        return
      }
      if (file_name == 'filtered_feature_bc_matrix') {
        if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'h5ad') {
          this.$message.warning('Please upload .h5ad file！');
        } else {
          this.formFile1[file_name] = event.target.files[0].name
          this.fileLoading = true
          this.openFile(event.target.files[0], 'data1', file_name + '.h5')
        }
      } else {
        if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'gz') {
          this.$message.warning('Please upload .gz file！');
        } else {
          this.formFile1[file_name] = event.target.files[0].name
          this.fileLoading = true
          if (file_name == 'matrix') {
            this.openFile(event.target.files[0], 'data1', file_name + '.mtx.gz')
          } else {
            this.openFile(event.target.files[0], 'data1', file_name + '.tsv.gz')
          }
        }
      }
    },
    handleUpdate2(event, file_name) {
      if (this.formFile2.data2_sample_name == '') {
        this.$message('Please Choose sample name!')
        event.target.value = ""
        return
      }
      if (file_name == 'filtered_feature_bc_matrix') {
        if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'h5ad') {
          this.$message.warning('Please upload .h5ad file！');
        } else {
          this.formFile2[file_name] = event.target.files[0].name
          this.fileLoading = true
          this.openFile(event.target.files[0], 'data2', file_name + '.h5')
        }
      } else {
        if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'gz') {
          this.$message.warning('Please upload .gz file！');
        } else {
          this.formFile2[file_name] = event.target.files[0].name
          this.fileLoading = true
          if (file_name == 'matrix') {
            this.openFile(event.target.files[0], 'data2', file_name + '.mtx.gz')
          } else {
            this.openFile(event.target.files[0], 'data2', file_name + '.tsv.gz')
          }
        }
      }
    },
    openFile(file, data_type, file_name) {
      let formData = new FormData()
      formData.append('file', file)
      formData.append('upload_id', this.upload_id)
      formData.append('data_type', data_type)
      formData.append('file_name', file_name)
      if (data_type == 'data1') {
        formData.append('data1_sample_name', this.formFile1.data1_sample_name)
      } else {
        formData.append('data2_sample_name', this.formFile2.data2_sample_name)
      }
      // formData.append('analysis_name', data_type == 'data1' ? this.formFile1.analysis_name : this.formFile2.analysis_name)
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      const $axios = Axios.create({
        baseURL: axios.defaults.baseURL,
        timeout: 1000000
      });

      $axios.post('/v1/sample_qc_upload/', formData, config).then(res => {
        if (res.data.code == 200) {
          this.$message.success('Upload successful!')
        } else {
          this.$message.warning('Upload failed!')
        }
        this.fileLoading = false
      }).catch(err => {
        this.$message.warning('Upload failed!')
      });
    },
    async runQC(type) {
      try {
        await this.$refs.formFile1.validate()
        await this.$refs.formFile2.validate()
        await this.$refs.formBottom.validate()
        //都校验成功之后，这里可以发请求
        this.runLoading = true
        let param = {
          uuid: this.upload_id,
          mt: this.formBottom.mt,
          pt: this.formBottom.pt,
        }
        if (type == 'qcResult') {
          param = {
            uuid: this.upload_id
          }
        } else {
          param = {
            uuid: this.upload_id,
            mt: this.formBottom.mt,
            pt: this.formBottom.pt,
          }
        }
        sqmpleQcDataShow(param).then((res) => {
          if (res.code == 200) {
            this.runLoading = false
            this.isShowQC = false
            this.data1 = {
              min_nCount_RNA: res.data[0].data1.min_total_counts,
              min_nFeature_RNA: res.data[0].data1.min_n_genes_by_counts,
              min_percent_mt: res.data[0].data1.min_pct_counts_mt,
              min_percent_pt: res.data[0].data1.min_pct_counts_pt,
              max_nCount_RNA: res.data[0].data1.max_total_counts,
              max_nFeature_RNA: res.data[0].data1.max_n_genes_by_counts,
              max_percent_mt: res.data[0].data1.max_pct_counts_mt,
              max_percent_pt: res.data[0].data1.max_pct_counts_pt
            }
            this.data2 = {
              min_nCount_RNA: res.data[1].data2.min_total_counts,
              min_nFeature_RNA: res.data[1].data2.min_n_genes_by_counts,
              min_percent_mt: res.data[1].data2.min_pct_counts_mt,
              min_percent_pt: res.data[1].data2.min_pct_counts_pt,
              max_nCount_RNA: res.data[1].data2.max_total_counts,
              max_nFeature_RNA: res.data[1].data2.max_n_genes_by_counts,
              max_percent_mt: res.data[1].data2.max_pct_counts_mt,
              max_percent_pt: res.data[1].data2.max_pct_counts_pt
            }
            qc_filter_data_show({
              uuid: this.upload_id
            }).then((res) => {
              if (res.code == 200) {
                this.form = {
                  min_nCount_RNA: res.data.results[0].min_total_counts,
                  min_nFeature_RNA: res.data.results[0].min_n_genes_by_counts,
                  min_percent_mt: res.data.results[0].min_pct_counts_mt,
                  min_percent_pt: res.data.results[0].min_pct_counts_pt,
                  max_nCount_RNA: res.data.results[0].max_total_counts,
                  max_nFeature_RNA: res.data.results[0].max_n_genes_by_counts,
                  max_percent_mt: res.data.results[0].max_pct_counts_mt,
                  max_percent_pt: res.data.results[0].max_pct_counts_pt
                }
              }
            })
          }
        })
      } catch (error) {
        console.error('表单校验失败', error)
      }
    },
    implement() {
      let stepIndex = 0
      let currentIndex = 0
      this.stepList.forEach((item, index) => {
        if (this.$route.query.step == item.step) {
          stepIndex = index
        }
        if (location.href.split("?")[0].split('/ipscdb/')[1] == item.link) {
          currentIndex = index
        }
      });
      if (currentIndex < stepIndex) {
        this.$confirm('Are you sure to execute again? If confirmed, all subsequent results will be cleared!', 'Tips', {
          confirmButtonText: 'confirm',
          cancelButtonText: 'cancel',
          type: 'warning'
        }).then(() => {
          this.loading = true
          this.$route.query.step = 'sample_qc'
          this.stepActive = 1
          sample_qc({
            uuid: this.upload_id,
            max_n_genes_by_counts: this.form.max_nFeature_RNA,
            max_total_counts: this.form.max_nCount_RNA,
            max_pct_counts_mt: this.form.max_percent_mt,
            max_pct_counts_pt: this.form.max_percent_pt,
            min_n_genes_by_counts: this.form.min_nFeature_RNA,
            min_total_counts: this.form.min_nCount_RNA,
            min_pct_counts_mt: this.form.min_percent_mt,
            min_pct_counts_pt: this.form.min_percent_pt,
          }).then((res) => {
            if (res.code == 200) {
              this.$message(res.data.status)
              this.loading = false
              this.$router.push({
                path: '/analysisFromSampleQC',
                query: {}
              })
            }
          })
        })
      } else {
        this.loading = true
        sample_qc({
          uuid: this.upload_id,
          max_n_genes_by_counts: this.form.max_nFeature_RNA,
          max_total_counts: this.form.max_nCount_RNA,
          max_pct_counts_mt: this.form.max_percent_mt,
          max_pct_counts_pt: this.form.max_percent_pt,
          min_n_genes_by_counts: this.form.min_nFeature_RNA,
          min_total_counts: this.form.min_nCount_RNA,
          min_pct_counts_mt: this.form.min_percent_mt,
          min_pct_counts_pt: this.form.min_percent_pt,
        }).then((res) => {
          if (res.code == 200) {
            this.$message(res.data.status)
            this.loading = false
            this.$router.push({
              path: '/analysisFromSampleQC',
              query: {}
            })
          }
        })
      }

    },
    jumpResultPage() {
      qc_filter_data_result({
        uuid: this.$route.query.uuid,
        data_type: 'data1',
      }).then((res) => {
        if (res.code == 200) {
          if (res.data.results && res.data.results.length > 0) {
            this.resultData.data1 = res.data.results[0].result_data
            qc_filter_data_result({
              uuid: this.$route.query.uuid,
              data_type: 'data2',
            }).then((res) => {
              if (res.code == 200) {
                if (this.executeaAgain) {
                  this.$route.query.step = 'data_process'
                }
                this.resultData.data2 = res.data.results[0].result_data
                this.isShowResult = true
              }
            })
          } else {
            this.$message(res.msg)
          }
        }
      })
    }
  }
}
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
