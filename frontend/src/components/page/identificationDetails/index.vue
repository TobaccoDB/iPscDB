<template>
  <div class="identificationDetails">
    <div class="crumbs">
      <el-breadcrumb v-if="$route.query.from == 'identification' || $route.query.from == 'example'" separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/cellIdentification' }">Cell Identification</el-breadcrumb-item>
        <el-breadcrumb-item>Identification Detail</el-breadcrumb-item>
      </el-breadcrumb>
      <el-breadcrumb v-else separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/sampleQC' }">Sample QC</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: `/sampleDetails?sample_id=${this.$route.query.sample_id}&files_uuid=${this.$route.query.files_uuid}&file_type=${this.$route.query.file_type}` }">File Upload</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: `/sampleQCFilter?sample_id=${this.$route.query.sample_id}&files_uuid=${this.$route.query.files_uuid}&file_type=${this.$route.query.file_type}` }">QC filter</el-breadcrumb-item>
        <el-breadcrumb-item>Identification Detail</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="identificationDetails-inner" :style="{minHeight: contentHeight}" v-loading="goLoading" element-loading-text="loading"
      element-loading-background="#fff">
      <p class="topTitle">
        <el-button type="text" @click="downloadImg('jpg')" style="float:right;color:#0a9daa;margin-left:10px;">
          <i class="el-icon-download"></i> jpg</el-button>
        <el-button type="text" @click="downloadImg('png')" style="float:right;color:#0a9daa;margin-left:10px;">
          <i class="el-icon-download"></i> png</el-button>
        <el-button type="text" @click="downloadImg('svg')" style="float:right;color:#0a9daa;margin-left:10px;">
          <i class="el-icon-download"></i> svg</el-button>
      </p>
      <div class="UMAP" ref="imageTofile">
        <img :src="url" width="100%" height="560px">
      </div>
    </div>
  </div>
</template>

<script>

import axios from '@/api/http.js';
import Axios from 'axios'
//顶部页面加载条
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';
NProgress.configure({
  easing: 'ease',
  speed: 500,
  showSpinner: false,
  trickleSpeed: 200,
  minimum: 0.3
})
import { cell_identification_svg_show, cell_identification_example_svg_show } from "@/api/api";
export default {
  name: "identificationDetails",
  components: {
  },
  data() {
    return {
      contentHeight: (window.innerHeight - 330) + 'px',
      goLoading: false,
      url: '',
      integration_download_png: "",
      integration_download_svg: "",
      integration_download_jpg: "",
    };
  },
  mounted() {
    if (this.$route.query.from == 'example') {
      this.example()
    } else {
      this.init()
    }
  },
  methods: {
    example() {
      this.goLoading = true
      cell_identification_example_svg_show({}).then(res => {
        if (res.code == 200) {
          this.url = res.data.classifier_picture_show_svg
          this.integration_download_svg = res.data.classifier_picture_download_svg
          this.integration_download_png = res.data.classifier_picture_download_png
          this.integration_download_jpg = res.data.classifier_picture_download_jpg
          this.goLoading = false
        }
      });
    },
    init() {
      let params = {
        specie_type: this.$route.query.specie_type,
        tissue_type: this.$route.query.tissue_type,
        identification_type: this.$route.query.identification_type,
        identification_path: sessionStorage.getItem("identification_path")
      }
      this.goLoading = true
      cell_identification_svg_show(params).then(res => {
        if (res.code == 200) {
          this.url = res.data.classifier_picture_show_svg
          this.integration_download_svg = res.data.classifier_picture_download_svg
          this.integration_download_png = res.data.classifier_picture_download_png
          this.integration_download_jpg = res.data.classifier_picture_download_jpg
          this.goLoading = false
        }
      });
    },
    downloadImg(name) {
      let imgUrl = ''
      if (name == 'svg') {
        imgUrl = this.integration_download_svg
      } else if (name == 'png') {
        imgUrl = this.integration_download_png
      } else {
        imgUrl = this.integration_download_jpg
      }
      const link = document.createElement("a"); //自己创建的a标签
      link.href = imgUrl;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(imgUrl);
    },
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>


