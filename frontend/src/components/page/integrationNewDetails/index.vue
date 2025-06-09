<template>
  <div class="integrationNewDetails">
    <div class="crumbs">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/Integration' }">Integration</el-breadcrumb-item>
        <el-breadcrumb-item>Detail</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="integrationNewDetails-inner" :style="{minHeight: contentHeight}" v-loading="goLoading" element-loading-text="loading"
      element-loading-background="#fff">

      <div class="UMAP" ref="imageTofile">
        <!-- <img :src="url" width="100%" height="560px"> -->
        <p class="secondTitle">Integration Result</p>
        <p class="thirdTitle">The script execution takes a long time. You can download the data and run it on your PC</p>
        <p class="thirdTitle">How to use?</p>
        <ul>
          <li>1. Click the Download button</li>
          <li>2. Unzip data.zip</li>
          <li>3. Open terminal in the folder</li>
          <li>4. Run command: Rscript {{backText}}</li>
        </ul>
        <el-button style="margin-top:20px;" type="primary" @click="download" :loading="downloadLoading">
          <i class="el-icon-download"></i> Download results</el-button>
      </div>
    </div>
  </div>
</template>

<script>

import { integration_zip_download } from "@/api/api";
export default {
  name: "integrationNewDetails",
  components: {
  },
  data() {
    return {
      contentHeight: (window.innerHeight - 330) + 'px',
      goLoading: false,
      downloadLoading: false,
      url: '',
      integration_zip: "",
      backText: 'Seurat.R -a ERR6908267.rds -b GSM4809928.rds'
    };
  },
  mounted() {
    let typeArr = ['-a', '-b', '-c', '-d', '-e']
    let str = ''
    this.$route.query.sample_id.split(',').forEach((item, index) => {
      str = str + ` ${typeArr[index]} ${item}.rds`
    });
    this.backText = `${this.$route.query.integration_type}.R ${str}`
  },
  methods: {
    download() {
      let params = {
        integration_type: this.$route.query.integration_type,
        sample_id: this.$route.query.sample_id,
      }
      this.downloadLoading = true
      integration_zip_download(params).then(res => {
        if (res.code == 200) {
          this.downloadLoading = false
          window.location.href = res.data.integration_zip
        }
      });
    },


  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>


