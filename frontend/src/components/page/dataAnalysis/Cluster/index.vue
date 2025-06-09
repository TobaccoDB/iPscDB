<template>
  <div class="Cluster">
    <div class="Cluster-inner">
      <div class="stepBar">
        <el-steps :active="stepActive" finish-status="success" :align-center="true">
          <el-step :style="{ cursor: index <= stepActive ? 'pointer' : 'auto' }" @click.native="setpClick(item, index)" :title="item.name"
            v-for="(item, index) in stepList"></el-step>
        </el-steps>
      </div>
      <div class="blast" v-if="!isShowResult" v-loading="pageLoading">
        <!-- <el-header>Cluster</el-header> -->
        <el-header>Cluster</el-header>
        <el-form ref="formData1" :inline="true" :model="data1Form" :rules="rules">
          <el-form-item label="Resolution" prop="Resolution">
            <el-slider style="width:200px;margin:0 10px;" :min="0.2" :max="1.2" v-model="data1Form.Resolution" :step="0.1">
            </el-slider>
            <!-- 0.2 - 1.2 每0.1一个刻度 -->
          </el-form-item>
        </el-form>
        <div style="margin-top:20px;">
          <el-button class="btnSearch" :loading="loading" @click="implement">Next</el-button>
          <!-- <el-button class="btnSearch" :loading="loading" @click="implement">Run Cluster</el-button> -->
          <!-- <el-button @click="jumpResultPage">Result</el-button> -->
        </div>
      </div>
      <ClusterResult :parent-msg="resultData" v-if="isShowResult"></ClusterResult>
      <progressBar :progressVisible="progressVisible" :percentage="percentage" @dialogClose="dialogClose"></progressBar>
    </div>
  </div>
</template>

<script>
import { cluster_resolution, cluster, cluster_result, analysisCellrangerList, analysis_step_progress } from '@/api/analysis'
import ClusterResult from '@/components/page/dataAnalysis/ClusterResult/index'
import progressBar from '@/components/page/dataAnalysis/progressBar/index'

export default {
  name: 'Cluster',
  components: {
    ClusterResult,
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
        Resolution: 0.2,
      },
      rules: {
        Resolution: [
          { required: true, message: 'Please choose', trigger: 'change' }
        ],
      },
      loading: false,
      isShowResult: false,
      resultData: {},
      stepActive: 3,
      executeaAgain: false,
      species_name: '',
      tissue: '',
      pageLoading: false,
      progressVisible: false,
      timer: '',
      percentage: 1
    }
  },
  mounted() {
    let source = ''
    if (this.$route.query.from == 'sample_qc') {
      source = 'sample_qc'
      this.stepList = [
        { name: 'Sample QC', link: 'SampleSampleQC', step: 'sample_qc' },
        { name: 'Data Process', link: 'DataProcess', step: 'data_process' },
        { name: 'Cluster', link: 'Cluster', step: 'cluster' },
        { name: 'Cell Annotation', link: 'DataAnalysisCellAnnotation', step: 'cell_annotation' },
      ]
    } else {
      source = 'cell_ranger'
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
    analysisCellrangerList({
      source: source,
      page: 1,
      page_size: 999
    }).then((res) => {
      if (res.code == 200) {
        res.data.results && res.data.results.forEach(item => {
          if (item.uuid == this.$route.query.uuid) {
            this.species_name = item.species_name
            this.tissue = item.transcriptome
          }
        });
      }
    })
    // if (this.$route.query.step == 'cell_annotation' && this.$route.query.enterResults) {
    if (this.$route.query.step == 'cell_annotation') {
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
      }
    },
    init() {
      cluster_resolution({
        uuid: this.$route.query.uuid
      }).then((res) => {
        if (res.code == 200) {
          this.data1Form.Resolution = res.data[0].resolution
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
    async implement() { //执行
      this.percentage = 1
      try {
        await this.$refs.formData1.validate()
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
            this.$route.query.step = 'cluster'
            this.stepActive = 3
            this.executeaAgain = true
            cluster({
              uuid: this.$route.query.uuid,
              resolution: this.data1Form.Resolution,
              species_name: this.species_name,
              tissue: this.tissue
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
          cluster({
            uuid: this.$route.query.uuid,
            resolution: this.data1Form.Resolution,
            species_name: this.species_name,
            tissue: this.tissue
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

      } catch (error) {
        console.error('表单校验失败', error)
      }
    },
    jumpResultPage() {
      cluster_result({
        uuid: this.$route.query.uuid
      }).then((res) => {
        if (res.code == 200) {
          if (res.data.results && res.data.results.length > 0) {
            this.resultData = res.data.results[0]
            if (this.executeaAgain) {
              this.$route.query.step = 'cell_annotation'
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
