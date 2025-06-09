<template>
  <div class="SampleQC">
    <div class="SampleQC-inner">
      <div class="stepBar">
        <el-steps :active="stepActive" finish-status="success" :align-center="true">
          <el-step :style="{ cursor: index <= stepActive ? 'pointer' : 'auto' }" @click.native="setpClick(item, index)" :title="item.name"
            v-for="(item, index) in stepList"></el-step>
        </el-steps>
      </div>
      <div class="blast" v-if="isShowQC" v-loading="pageLoading">
        <el-header>Sample QC</el-header>
        <el-form ref="formTop" :inline="true" :model="formTop" :rules="rules">
          <el-form-item label="pt">
            <el-input v-model="formTop.pt" clearable placeholder="Please enter"></el-input>
          </el-form-item>
          <el-form-item label="mt">
            <el-input v-model="formTop.mt" clearable placeholder="Please enter"></el-input>
          </el-form-item>
          <br />
          <el-form-item label="">
            <el-button class="btnSearch" :loading="runQCloading" @click="runQC('qc')">Run QC</el-button>
            <el-button @click="runQC('qcResult')" :loading="runQCResultloading">Run QC result</el-button>
          </el-form-item>
        </el-form>
      </div>
      <div class="blast" v-if="!isShowResult&& !isShowQC" v-loading="pageLoading">
        <!-- <el-header>Sample QC</el-header> -->
        <el-header>Data1</el-header>
        <div style="">
          <ul class="sample_table">
            <li></li>
            <li>nCount_RNA</li>
            <li>nFeatuer_RNA</li>
            <li v-if="formTop.mt">percent.mt</li>
            <li v-if="formTop.pt">percent.pt</li>
          </ul>
          <ul class="sample_table">
            <li>min</li>
            <li>{{ data1.min_nCount_RNA }}</li>
            <li>{{ data1.min_nFeature_RNA }}</li>
            <li v-if="formTop.mt">{{ data1.min_percent_mt }}</li>
            <li v-if="formTop.pt">{{ data1.min_percent_pt }}</li>
          </ul>
          <ul class="sample_table">
            <li>max</li>
            <li>{{ data1.max_nCount_RNA }}</li>
            <li>{{ data1.max_nFeature_RNA }}</li>
            <li v-if="formTop.mt">{{ data1.max_percent_mt }}</li>
            <li v-if="formTop.pt">{{ data1.max_percent_pt }}</li>
          </ul>
        </div>
        <el-header>Data2</el-header>
        <div style="">
          <ul class="sample_table">
            <li></li>
            <li>nCount_RNA</li>
            <li>nFeatuer_RNA</li>
            <li v-if="formTop.mt">percent.mt</li>
            <li v-if="formTop.pt">percent.pt</li>
          </ul>
          <ul class="sample_table">
            <li>min</li>
            <li>{{ data2.min_nCount_RNA }}</li>
            <li>{{ data2.min_nFeature_RNA }}</li>
            <li v-if="formTop.mt">{{ data2.min_percent_mt }}</li>
            <li v-if="formTop.pt">{{ data2.min_percent_pt }}</li>
          </ul>
          <ul class="sample_table">
            <li>max</li>
            <li>{{ data2.max_nCount_RNA }}</li>
            <li>{{ data2.max_nFeature_RNA }}</li>
            <li v-if="formTop.mt">{{ data2.max_percent_mt }}</li>
            <li v-if="formTop.pt">{{ data2.max_percent_pt }}</li>
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
            <el-col :span="6" v-if="formTop.mt">
              <div class="grid-content bg-purple">
                <el-form-item label="min percent.mt" prop="min_percent_mt">
                  <el-input style="width: 120px" v-model="form.min_percent_mt"></el-input>
                </el-form-item>
                <el-form-item label="max percent.mt" prop="max_percent_mt">
                  <el-input style="width: 120px" v-model="form.max_percent_mt"></el-input>
                </el-form-item>
              </div>
            </el-col>
            <el-col :span="6" v-if="formTop.pt">
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
          <el-button class="btnSearch" @click="implement" :loading="loading">Next</el-button>
          <!-- <el-button class="btnSearch" @click="implement" :loading="loading">Run QC filter</el-button>
          <el-button @click="jumpResultPage">Result</el-button> -->
        </div>
      </div>
      <SampleQCResult :parent-msg="resultData" v-if="isShowResult"></SampleQCResult>
      <progressBar :progressVisible="progressVisible" :percentage="percentage" @dialogClose="dialogClose"></progressBar>
    </div>
  </div>
</template>

<script>
import { sample_qc_pt_mt, sqmple_qc_data_show, qc_filter_data_show, sample_qc, qc_filter_data_result, analysis_step_progress } from '@/api/analysis'
import SampleQCResult from '@/components/page/dataAnalysis/SampleQCResult/index'
import progressBar from '@/components/page/dataAnalysis/progressBar/index'

export default {
  name: 'SampleQC',
  components: {
    SampleQCResult,
    progressBar
  },
  data() {
    return {
      stepList: [
        { name: 'Cell Ranger', link: 'CellRanger', step: 'cell_ranger' },
        { name: 'Sample QC', link: 'DataAnalysisSampleQC', step: 'sample_qc' },
        { name: 'Data Process', link: 'DataProcess', step: 'data_process' },
        { name: 'Cluster', link: 'Cluster', step: 'cluster' },
        { name: 'Cell Annotation', link: 'DataAnalysisCellAnnotation', step: 'cell_annotation' },
      ],
      formTop: {
        pt: '',
        mt: '',
      },
      rules: {
        // pt: [
        //   { required: true, message: 'Please enter', trigger: 'blur' },
        // ],
        // mt: [
        //   { required: true, message: 'Please enter', trigger: 'blur' },
        // ],
      },
      isShowQC: true,
      isShowResult: false,
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
      loading: false,
      resultData: {},
      stepActive: 1,
      executeaAgain: false,
      runQCloading: false,
      runQCResultloading: false,
      pageLoading: false,
      progressVisible: false,
      timer: '',
      percentage: 1
    }
  },
  mounted() {
    this.stepList.forEach((item, index) => {
      if (this.$route.query.step == item.step) {
        this.stepActive = index
        if (this.$route.query.step == 'cell_annotation') {
          this.stepActive = Number(this.stepActive) + 1
        }
      }
    });
    this.init()
    // if (this.$route.query.step == 'data_process' && this.$route.query.enterResults) {
    //   this.pageLoading = true
    //   this.jumpResultPage()
    // }
    if (this.$route.query.step == 'data_process' || this.$route.query.step == 'cluster' || this.$route.query.step == 'cell_annotation') {
      this.pageLoading = true
      this.jumpResultPage()
    }
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
  methods: {
    setpClick(item, index) {
      if (index < this.stepActive || index == this.stepActive) {
        if (this.$route.path == ('/' + item.link)) return
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
    init() {
      sample_qc_pt_mt({
        uuid: this.$route.query.uuid
      }).then((res) => {
        if (res.code == 200) {
          this.formTop.pt = res.data[0].pt
          this.formTop.mt = res.data[0].mt
        }
      })

    },
    runQC(type) {
      let param = { uuid: this.$route.query.uuid }
      if (type == 'qcResult') {
        this.runQCResultloading = true
        param = { uuid: this.$route.query.uuid }
        sqmple_qc_data_show(param).then((res) => {
          if (res.code == 200) {
            if (res.data.length > 0) {
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
              this.getQcFilter()

              this.isShowQC = false
            } else {
              this.$message('Run QC has not been executed yet. Please execute it first!')
            }
            this.runQCResultloading = false
          }
        })
      } else {
        this.$refs['formTop'].validate((valid) => {
          if (valid) {
            this.runQCloading = true
            param = Object.assign({}, this.formTop, { uuid: this.$route.query.uuid, tag: 'run' })
            sqmple_qc_data_show(param).then((res) => {
              if (res.code == 200) {
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
                this.getQcFilter()
                this.runQCloading = false
                this.isShowQC = false
              }
            })
          } else {
            return false;
          }
        });
      }

    },
    getQcFilter() {
      qc_filter_data_show({
        uuid: this.$route.query.uuid
      }).then((res) => {
        if (res.code == 200) {
          this.form = {
            min_nCount_RNA: res.data.results[0].min_total_counts,
            min_nFeature_RNA: res.data.results[0].min_n_genes_by_counts,
            min_percent_mt: res.data.results[0].min_pct_counts_mt || this.data1.min_percent_mt,
            min_percent_pt: res.data.results[0].min_pct_counts_pt || this.data1.min_percent_pt,
            // min_nCount_RNA: res.data.filter_min_nCount_RNA < res.data.min_nCount_RNA ? res.data.min_nCount_RNA : res.data.filter_min_nCount_RNA,
            // min_nFeature_RNA: res.data.filter_min_Feature_RNA_cutmin < res.data.min_nFeature_RNA ? res.data.min_nFeature_RNA : res.data.filter_min_Feature_RNA_cutmin,
            // min_percent_mt: res.data.filter_min_mt_cutmin < res.data.min_percent_mt ? res.data.min_percent_mt : res.data.filter_min_mt_cutmin,
            // min_percent_pt: res.data.filter_min_pt_cutmin < res.data.min_percent_pt ? res.data.min_percent_pt : res.data.filter_min_pt_cutmin,
            max_nCount_RNA: res.data.results[0].max_total_counts,
            max_nFeature_RNA: res.data.results[0].max_n_genes_by_counts,
            max_percent_mt: res.data.results[0].max_pct_counts_mt || this.data1.max_percent_mt,
            max_percent_pt: res.data.results[0].max_pct_counts_pt || this.data1.max_percent_pt
          }
        }
      })
    },
    dialogClose() {
      this.progressVisible = false
      clearInterval(this.timer);
    },
    valChange() {
      analysis_step_progress({
        uuid: this.$route.query.uuid,
        current_step: this.$route.query.step
      }).then((res) => {
        if (res.code == 200 && res.data[0].status != 'FAILURE') {
          this.percentage = res.data[0].progress
          if (res.data[0].progress == 100 && res.data[0].status == 'SUCCESS') {
            this.progressVisible = false
            clearInterval(this.timer);
            this.pageLoading = true
            this.jumpResultPage()
          }
        } else {
          this.$message('Your task failed, please try again。')
          this.progressVisible = false
          this.loading = false
          clearInterval(this.timer);
        }
      })
    },
    implement() {
      this.percentage = 1
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
          this.executeaAgain = true
          let param = {
            uuid: this.$route.query.uuid,
            max_n_genes_by_counts: this.form.max_nFeature_RNA,
            max_total_counts: this.form.max_nCount_RNA,
            min_n_genes_by_counts: this.form.min_nFeature_RNA,
            min_total_counts: this.form.min_nCount_RNA,
          }
          if (this.formTop.pt) {
            param.min_pct_counts_pt = this.form.min_percent_pt
            param.max_pct_counts_pt = this.form.max_percent_pt
          }
          if (this.formTop.mt) {
            param.min_pct_counts_mt = this.form.min_percent_mt
            param.max_pct_counts_mt = this.form.max_percent_mt
          }
          sample_qc(param).then((res) => {
            if (res.code == 200) {
              // this.$message(res.data.status)
              this.loading = false
              this.progressVisible = true
              this.timer = setInterval(this.valChange, 3000);
              // this.$router.push({
              //   path: '/analysisFromCellranger',
              //   query: {}
              // })
            } else {
              this.$message('Your task failed, please try again。')
              this.progressVisible = false
              this.loading = false
              clearInterval(this.timer);
            }
          })
        })
      } else {
        this.loading = true
        let param = {
          uuid: this.$route.query.uuid,
          max_n_genes_by_counts: this.form.max_nFeature_RNA,
          max_total_counts: this.form.max_nCount_RNA,
          min_n_genes_by_counts: this.form.min_nFeature_RNA,
          min_total_counts: this.form.min_nCount_RNA,
        }
        if (this.formTop.pt) {
          param.min_pct_counts_pt = this.form.min_percent_pt
          param.max_pct_counts_pt = this.form.max_percent_pt
        }
        if (this.formTop.mt) {
          param.min_pct_counts_mt = this.form.min_percent_mt
          param.max_pct_counts_mt = this.form.max_percent_mt
        }
        sample_qc(param).then((res) => {
          if (res.code == 200) {
            // this.$message(res.data.status)
            this.loading = false
            this.progressVisible = true
            this.timer = setInterval(this.valChange, 3000);
            // this.$router.push({
            //   path: '/analysisFromCellranger',
            //   query: {}
            // })
          } else {
            this.$message('Your task failed, please try again。')
            this.progressVisible = false
            this.loading = false
            clearInterval(this.timer);
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
                this.resultData.formTop = this.formTop
                this.isShowResult = true
                this.pageLoading = false
                this.isShowQC = false
              }
            })
          } else {
            this.$message('Executing, please try again later!')
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

