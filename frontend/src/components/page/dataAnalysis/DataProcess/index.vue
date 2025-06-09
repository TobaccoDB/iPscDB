<template>
  <div class="DataProcess">
    <div class="DataProcess-inner">
      <div class="stepBar">
        <el-steps :active="stepActive" finish-status="success" :align-center="true">
          <el-step :style="{ cursor: index <= stepActive ? 'pointer' : 'auto' }" @click.native="setpClick(item, index)" :title="item.name"
            v-for="(item, index) in stepList"></el-step>
        </el-steps>
      </div>
      <div class="blast" v-if="!isShowResult" v-loading="pageLoading">
        <el-header>Data Process</el-header>
        <el-header>Normalize Data</el-header>
        <el-form ref="form1Ref" :inline="true" :model="data1Form" :rules="rules">
          <el-form-item label="selection.method" prop="selection_method">
            <el-input v-model="data1Form.selection_method"></el-input>
          </el-form-item>
          <el-form-item label="nfeatures" prop="nfeatures">
            <el-input v-model="data1Form.nfeatures"></el-input>
          </el-form-item>
        </el-form>
        <el-header>FindVariableFeatures Data</el-header>
        <el-form ref="form2Ref" :inline="true" :model="data1Form" :rules="rules">
          <el-form-item label="min_mean" prop="min_mean">
            <el-input v-model="data1Form.min_mean"></el-input>
          </el-form-item>
          <el-form-item label="max_mean" prop="max_mean">
            <el-input v-model="data1Form.max_mean"></el-input>
          </el-form-item>
          <el-form-item label="min_disp" prop="min_disp">
            <el-input v-model="data1Form.min_disp"></el-input>
          </el-form-item>
        </el-form>
        <el-header>Scale Data</el-header>
        <el-form ref="form3Ref" :inline="true" :model="data1Form" :rules="rules">
          <el-form-item label="n_jobs" prop="n_jobs">
            <el-input v-model="data1Form.n_jobs"></el-input>
          </el-form-item>
          <el-form-item label="max_value" prop="max_value">
            <el-input v-model="data1Form.max_value"></el-input>
          </el-form-item>
        </el-form>
        <el-header>Neighbor Data</el-header>
        <el-form ref="form4Ref" :inline="true" :model="data1Form" :rules="rules">
          <el-form-item label="n_neighbors" prop="n_neighbors">
            <el-slider style="width:200px;margin:0 10px;" :min="10" :max="50" v-model="data1Form.n_neighbors" :step="5">
            </el-slider>
          </el-form-item>
          <el-form-item label="n_pcs" prop="n_pcs">
            <el-input v-model="data1Form.n_pcs"></el-input>
          </el-form-item>
        </el-form>
        <div style="margin-top:20px;">
          <!-- <el-button class="btnSearch" :loading="loading" @click="implement">Run Data Process</el-button> -->
          <el-button class="btnSearch" :loading="loading" @click="implement">Next</el-button>
          <!-- <el-button @click="jumpResultPage">Result</el-button> -->
        </div>
      </div>
      <DataProcessResult :parent-msg="resultData" v-else="isShowResult"></DataProcessResult>
      <progressBar :progressVisible="progressVisible" :percentage="percentage" @dialogClose="dialogClose"></progressBar>
    </div>
  </div>
</template>

<script>
import { data_process_show, data_process, data_process_result, analysis_step_progress } from '@/api/analysis'
import DataProcessResult from '@/components/page/dataAnalysis/DataProcessResult/index'
import progressBar from '@/components/page/dataAnalysis/progressBar/index'

export default {
  name: 'DataProcess',
  components: {
    DataProcessResult,
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
      data1Form: {
        selection_method: '',
        nfeatures: '',
        min_mean: '',
        max_mean: '',
        min_disp: '',
        n_jobs: '',
        max_value: '',
        n_neighbors: 10,
        n_pcs: '',
      },
      rules: {
        // selection: [
        //   { required: true, message: 'Please enter', trigger: 'blur' }
        // ],
        // nfeatures: [
        //   { required: true, message: 'Please enter', trigger: 'blur' }
        // ],
        min_mean: [
          { required: true, message: 'Please enter', trigger: 'blur' }
        ],
        max_mean: [
          { required: true, message: 'Please enter', trigger: 'blur' }
        ],
        min_disp: [
          { required: true, message: 'Please enter', trigger: 'blur' }
        ],
        n_jobs: [
          { required: true, message: 'Please enter', trigger: 'blur' }
        ],
        max_value: [
          { required: true, message: 'Please enter', trigger: 'blur' }
        ],
        n_neighbors: [
          { required: true, message: 'Please choose', trigger: 'change' }
        ],
        n_pcs: [
          { required: true, message: 'Please enter', trigger: 'blur' }
        ],
      },
      isShowResult: false,
      loading: false,
      resultData: {},
      data1_sample_name: '',
      data2_sample_name: '',
      stepActive: 2,
      executeaAgain: false,
      pageLoading: false,
      progressVisible: false,
      timer: '',
      percentage: 1
    }
  },
  mounted() {
    if (this.$route.query.from == 'sample_qc') {
      this.stepList = [
        { name: 'Sample QC', link: 'SampleSampleQC', step: 'sample_qc' },
        { name: 'Data Process', link: 'DataProcess', step: 'data_process' },
        { name: 'Cluster', link: 'Cluster', step: 'cluster' },
        { name: 'Cell Annotation', link: 'DataAnalysisCellAnnotation', step: 'cell_annotation' },
      ]
    } else {
      this.stepList = [
        { name: 'Cell Ranger', link: 'CellRanger', step: 'cell_ranger' },
        { name: 'Sample QC', link: 'DataAnalysisSampleQC', step: 'sample_qc' },
        { name: 'Data Process', link: 'DataProcess', step: 'data_process' },
        { name: 'Cluster', link: 'Cluster', step: 'cluster' },
        { name: 'Cell Annotation', link: 'DataAnalysisCellAnnotation', step: 'cell_annotation' },
      ]
    }
    this.stepList.forEach((item, index) => {
      if (this.$route.query.step == item.step) {
        this.stepActive = index
        if (this.$route.query.step == 'cell_annotation') {
          this.stepActive = Number(this.stepActive) + 1
        }
      }
    });
    this.init()
    // if (this.$route.query.step == 'cluster' && this.$route.query.enterResults) {
    //   this.pageLoading = true
    //   this.jumpResultPage()
    // }
    if (this.$route.query.step == 'cluster' || this.$route.query.step == 'cell_annotation') {
      this.pageLoading = true
      this.jumpResultPage()
    }
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
  methods: {
    init() {
      data_process_show({
        uuid: this.$route.query.uuid
      }).then((res) => {
        if (res.code == 200) {
          this.data1Form.selection_method = res.data.results[0].selection_method
          this.data1Form.nfeatures = res.data.results[0].nfeatures
          this.data1Form.min_mean = res.data.results[0].min_mean
          this.data1Form.max_mean = res.data.results[0].max_mean
          this.data1Form.min_disp = res.data.results[0].min_disp
          this.data1Form.n_jobs = res.data.results[0].n_jobs
          this.data1Form.max_value = res.data.results[0].max_value
          this.data1Form.n_neighbors = res.data.results[0].n_neighbors
          this.data1Form.n_pcs = res.data.results[0].n_pcs
          this.data1_sample_name = res.data.results[0].data1_sample_name
          this.data2_sample_name = res.data.results[0].data2_sample_name
        }
      })
    },
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
      }
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
    async implement() { //执行
      this.percentage = 1
      try {
        await this.$refs.form1Ref.validate()
        await this.$refs.form2Ref.validate()
        await this.$refs.form3Ref.validate()
        await this.$refs.form4Ref.validate()
        //都校验成功之后，这里可以发请求
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
            this.$route.query.step = 'data_process'
            this.stepActive = 2
            this.executeaAgain = true
            data_process({
              uuid: this.$route.query.uuid,
              selection_method: this.data1Form.selection_method,
              nfeatures: this.data1Form.nfeatures,
              min_mean: this.data1Form.min_mean,
              max_mean: this.data1Form.max_mean,
              min_disp: this.data1Form.min_disp,
              n_jobs: this.data1Form.n_jobs,
              max_value: this.data1Form.max_value,
              n_neighbors: this.data1Form.n_neighbors,
              n_pcs: this.data1Form.n_pcs,
              data1_sample_name: this.data1_sample_name,
              data2_sample_name: this.data2_sample_name
            }).then((res) => {
              if (res.code == 200) {
                // this.$message(res.data)
                this.loading = false
                this.progressVisible = true
                this.timer = setInterval(this.valChange, 3000);
                // if (this.$route.query.from == 'sample_qc') {
                //   this.$router.push({
                //     path: '/analysisFromSampleQC',
                //     query: {}
                //   })
                // } else {
                //   this.$router.push({
                //     path: '/analysisFromCellranger',
                //     query: {}
                //   })
                // }
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
          data_process({
            uuid: this.$route.query.uuid,
            selection_method: this.data1Form.selection_method,
            nfeatures: this.data1Form.nfeatures,
            min_mean: this.data1Form.min_mean,
            max_mean: this.data1Form.max_mean,
            min_disp: this.data1Form.min_disp,
            n_jobs: this.data1Form.n_jobs,
            max_value: this.data1Form.max_value,
            n_neighbors: this.data1Form.n_neighbors,
            n_pcs: this.data1Form.n_pcs,
            data1_sample_name: this.data1_sample_name,
            data2_sample_name: this.data2_sample_name
          }).then((res) => {
            if (res.code == 200) {
              // this.$message(res.data)
              this.loading = false
              this.progressVisible = true
              this.timer = setInterval(this.valChange, 3000);
              // if (this.$route.query.from == 'sample_qc') {
              //   this.$router.push({
              //     path: '/analysisFromSampleQC',
              //     query: {}
              //   })
              // } else {
              //   this.$router.push({
              //     path: '/analysisFromCellranger',
              //     query: {}
              //   })
              // }
            } else {
              this.$message('Your task failed, please try again。')
              this.progressVisible = false
              this.loading = false
              clearInterval(this.timer);
            }
          })
        }
        // this.$message.success('表单校验成功')
      } catch (error) {
        console.error('表单校验失败', error)
      }
    },
    jumpResultPage() {
      data_process_result({
        uuid: this.$route.query.uuid
      }).then((res) => {
        if (res.code == 200) {
          if (res.data.results && res.data.results.length > 0) {
            this.resultData = res.data.results[0]
            if (this.executeaAgain) {
              this.$route.query.step = 'cluster'
            }
            this.isShowResult = true
            this.pageLoading = false
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
