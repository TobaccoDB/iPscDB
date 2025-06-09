<template>
  <div class="sampleDetails">
    <div class="crumbs">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/sampleQC' }">Sample QC</el-breadcrumb-item>
        <el-breadcrumb-item>File Upload</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="sampleDetails-inner" v-loading="goLoading" element-loading-text="loading" element-loading-background="#fff">
      <p class="title1">Cells uploaded {{backVal2}}</p>
      <div class="UMAP" v-if="isShowpic">
        <img :src="url" width="100%">
      </div>
      <div style="position:relative;top:-42px;background:#fff;padding-top:30px;">
        <ul class="sample_table">
          <li></li>
          <li>nCount_RNA</li>
          <li>nFeatuer_RNA</li>
          <li>percent.mt</li>
          <li>percent.pt</li>
        </ul>
        <ul class="sample_table">
          <li>min</li>
          <li>{{min.min_nCount_RNA}}</li>
          <li>{{min.min_nFeature_RNA}}</li>
          <li>{{min.min_percent_mt}}</li>
          <li>{{min.min_percent_pt}}</li>
        </ul>
        <ul class="sample_table">
          <li>max</li>
          <li>{{max.max_nCount_RNA}}</li>
          <li>{{max.max_nFeature_RNA}}</li>
          <li>{{max.max_percent_mt}}</li>
          <li>{{max.max_percent_pt}}</li>
        </ul>
      </div>
      <p class="title2">QC filter</p>
      <el-form class="form1" ref="form1" :inline="true" :model="form" label-width="140px">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="grid-content bg-purple">
              <el-form-item label="min nCount_RNA" prop="min_nCount_RNA">
                <el-input style="width:120px;" v-model="form.min_nCount_RNA"></el-input>
              </el-form-item>
              <el-form-item label="max nCount_RNA" prop="max_nCount_RNA">
                <el-input style="width:120px;" v-model="form.max_nCount_RNA"></el-input>
              </el-form-item>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="grid-content bg-purple">
              <el-form-item label="min nFeatuer_RNA" prop="min_nFeature_RNA">
                <el-input style="width:120px;" v-model="form.min_nFeature_RNA"></el-input>
              </el-form-item>
              <el-form-item label="max nFeatuer_RNA" prop="max_nFeature_RNA">
                <el-input style="width:120px;" v-model="form.max_nFeature_RNA"></el-input>
              </el-form-item>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="grid-content bg-purple">
              <el-form-item label="min percent.mt" prop="min_percent_mt">
                <el-input style="width:120px;" v-model="form.min_percent_mt"></el-input>
              </el-form-item>
              <el-form-item label="max percent.mt" prop="max_percent_mt">
                <el-input style="width:120px;" v-model="form.max_percent_mt"></el-input>
              </el-form-item>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="grid-content bg-purple">
              <el-form-item label="min percent.pt" prop="min_percent_pt">
                <el-input style="width:120px;" v-model="form.min_percent_pt"></el-input>
              </el-form-item>
              <el-form-item label="max percent.pt" prop="max_percent_pt">
                <el-input style="width:120px;" v-model="form.max_percent_pt"></el-input>
              </el-form-item>
            </div>
          </el-col>
        </el-row>

        <el-form-item style="width:100%;" label="">
          <el-button type="primary" @click="search">Run QC</el-button>
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
import { sample_qc_upload_picture } from "@/api/api";
export default {
  name: "sampleDetails",
  components: {
  },
  data() {
    return {
      min: {
        min_nCount_RNA: '',
        min_nFeature_RNA: '',
        min_percent_mt: '',
        min_percent_pt: '',
      },
      max: {
        max_nCount_RNA: '',
        max_nFeature_RNA: '',
        max_percent_mt: '',
        max_percent_pt: '',
      },
      form: {
        min_nCount_RNA: '',
        max_nCount_RNA: '',
        min_nFeature_RNA: '',
        max_nFeature_RNA: '',
        min_percent_mt: '',
        max_percent_mt: '',
        min_percent_pt: '',
        max_percent_pt: '',
      },
      isShowGenesCells: false,
      goLoading: false,
      backVal1: '',
      backVal2: '',
      url: '',
      isShowpic: true
    };
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      NProgress.start();
      let params = {
        files_uuid: this.$route.query.files_uuid,
        file_type: this.$route.query.file_type,
        sample_id: this.$route.query.sample_id,
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
      sample_qc_upload_picture(params).then(res => {
        if (res.code == 200) {
          this.url = res.data.picture
          this.min = {
            min_nCount_RNA: res.data.min_nCount_RNA,
            min_nFeature_RNA: res.data.min_nFeature_RNA,
            min_percent_mt: res.data.min_percent_mt,
            min_percent_pt: res.data.min_percent_pt,
          }
          this.max = {
            max_nCount_RNA: res.data.max_nCount_RNA,
            max_nFeature_RNA: res.data.max_nFeature_RNA,
            max_percent_mt: res.data.max_percent_mt,
            max_percent_pt: res.data.max_percent_pt,
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
            max_percent_pt: res.data.filter_max_pt_cutmax,
          }
        }
      });
    },
    search() {
      sessionStorage.removeItem("sampleFrom")
      sessionStorage.setItem("sampleFrom", JSON.stringify({
        filter_min_Feature_RNA_cutmin: this.form.min_nFeature_RNA,
        filter_min_mt_cutmin: this.form.min_percent_mt,
        filter_min_pt_cutmin: this.form.min_percent_pt,
        filter_max_Feature_RNA_cutax: this.form.max_nFeature_RNA,
        filter_max_mt_cutmax: this.form.max_percent_mt,
        filter_max_pt_cutmax: this.form.max_percent_pt,
      }));
      this.$router.push({
        path: '/sampleQCFilter',
        query: {
          species_name: this.$route.query.species_name,
          tissue: this.$route.query.tissue,
          files_uuid: this.$route.query.files_uuid,
          file_type: this.$route.query.file_type,
          sample_id: this.$route.query.sample_id
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
    }
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>


