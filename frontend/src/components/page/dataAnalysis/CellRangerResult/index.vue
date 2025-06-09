<template>
  <div class="CellRangerResult">
    <div class="CellRangerResult-inner">
      <div class="blast" v-loading="loading">
        <el-header>Cell Ranger Result</el-header>
        <el-tabs type="border-card" v-model="activeName" @tab-click="handleClick">
          <el-tab-pane label="Data1" name="data1">
            <div class="iframe-container">
              <iframe id="iframeID" :src="url" :width="width" :height="height" frameborder="0" allowfullscreen :onload="autoIframeHeight()"></iframe>
            </div>
            <el-button type="text" @click="download('barcodes_download_url')" class="textBtn" icon="el-icon-download">barcodes</el-button>
            <el-button type="text" @click="download('features_download_url')" class="textBtn" icon="el-icon-download">features</el-button>
            <el-button type="text" @click="download('matrix_download_url')" class="textBtn" icon="el-icon-download">mattix</el-button>
          </el-tab-pane>
          <el-tab-pane label="Data2" name="data2">
            <div class="iframe-container">
              <iframe id="" :src="url2" :width="width" :height="height" frameborder="0" allowfullscreen :onload="autoIframeHeight()"></iframe>
            </div>
            <el-button type="text" @click="download2('barcodes_download_url')" class="textBtn" icon="el-icon-download">barcodes</el-button>
            <el-button type="text" @click="download2('features_download_url')" class="textBtn" icon="el-icon-download">features</el-button>
            <el-button type="text" @click="download2('matrix_download_url')" class="textBtn" icon="el-icon-download">mattix</el-button>
          </el-tab-pane>
        </el-tabs>
        <el-button style="margin-top:20px;" class="btnSearch" @click="jumpSampleQC">Next</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { analysis_file_download, analysisCellrangerList } from '@/api/analysis'

export default {
  name: 'CellRangerResult',
  components: {
  },
  props: {
    parentMsg: {
      type: Object
    }
  },
  data() {
    return {
      url: "",
      url2: "",
      width: '100%',
      height: '500px',
      activeName: 'data1',
      downloadUrl: [
        { barcodes_download_url: '', features_download_url: '', matrix_download_url: '' },
        { barcodes_download_url: '', features_download_url: '', matrix_download_url: '' }
      ],
      loading: false,
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      this.loading = true
      analysis_file_download({
        file_uuid: this.$route.query.uuid || this.parentMsg.uuid,
        data_type: 'data1',
      }).then((res) => {
        if (res.code == 200) {
          this.url = res.data.web_summary_url
          this.downloadUrl[0].barcodes_download_url = res.data.barcodes_download_url
          this.downloadUrl[0].features_download_url = res.data.features_download_url
          this.downloadUrl[0].matrix_download_url = res.data.matrix_download_url
          this.loading = false
        }
      })
      analysis_file_download({
        file_uuid: this.$route.query.uuid || this.parentMsg.uuid,
        data_type: 'data2',
      }).then((res) => {
        if (res.code == 200) {
          this.url2 = res.data.web_summary_url
          this.downloadUrl[1].barcodes_download_url = res.data.barcodes_download_url
          this.downloadUrl[1].features_download_url = res.data.features_download_url
          this.downloadUrl[1].matrix_download_url = res.data.matrix_download_url
          this.loading = false
        }
      })
    },
    autoIframeHeight(param) {
      var iframe = document.getElementById("iframeID");
      if (iframe !== null) {
        // var contentWindow = iframe.contentWindow;
        // 其他操作
        // var bHeight = iframe.contentWindow.document.body.scrollHeight;
        // var dHeight = iframe.contentWindow.document.documentElement.scrollHeight;
        // var height = Math.max(bHeight, dHeight);
        // this.height = height + 'px'
        // console.log(33, iframe.contentWindow)
      }
    },
    handleClick() {
    },
    download(name) {
      window.open(this.downloadUrl[0][name], '_blank')
    },
    download2(name) {
      window.open(this.downloadUrl[0][name], '_blank')
    },
    jumpSampleQC() {
      if (this.$route.query.uuid) {
        this.$router.push({
          path: '/DataAnalysisSampleQC',
          query: {
            uuid: this.$route.query.uuid,
            id: this.$route.query.id,
            step: this.$route.query.step == 'cell_ranger' ? 'sample_qc' : this.$route.query.step,
            from: this.$route.query.from,
          }
        })
      } else {
        analysisCellrangerList({
          uuid: this.parentMsg.uuid,
          email: '', // 
          analysis_name: '',
          source: this.parentMsg.source,
          page: 1,
          page_size: 10
        }).then((res) => {
          if (res.code == 200) {
            this.$router.push({
              path: '/DataAnalysisSampleQC',
              query: {
                uuid: this.parentMsg.uuid,
                id: res.data.results[0].id,
                step: res.data.results[0].current_step,
                from: res.data.results[0].source
              }
            })
          }
        })
      }
    }
  }
}
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
