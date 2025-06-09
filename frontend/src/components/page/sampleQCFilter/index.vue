<template>
  <div class="sampleQCFilter">
    <div class="crumbs">
      <el-breadcrumb separator-class="el-icon-arrow-right" v-if="$route.query.pageType">
        <el-breadcrumb-item :to="{ path: '/sampleQCNew' }">Sample QC</el-breadcrumb-item>
        <!-- <el-breadcrumb-item :to="{ path: `/sampleDeta      ils?tissue=${this.$route.query.tissue}&species_name=${this.$route.query.species_name}&sample_id=${this.$route.query.sample_id}&files_uuid=${this.$route.query.files_uuid}&file_type=${this.$route.query.file_type}` }">File Upload</el-breadcrumb-item> -->
        <el-breadcrumb-item>QC filter</el-breadcrumb-item>
      </el-breadcrumb>
      <el-breadcrumb separator-class="el-icon-arrow-right" v-else>
        <el-breadcrumb-item :to="{ path: '/sampleQC' }">Sample QC</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: `/sampleDetails?tissue=${this.$route.query.tissue}&species_name=${this.$route.query.species_name}&sample_id=${this.$route.query.sample_id}&files_uuid=${this.$route.query.files_uuid}&file_type=${this.$route.query.file_type}` }">File Upload</el-breadcrumb-item>
        <el-breadcrumb-item>QC filter</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="sampleQCFilter-inner" v-loading="goLoading" element-loading-text="loading" element-loading-background="#fff">
      <p class="title1">Cells uploaded {{backVal2}}</p>
      <div class="UMAP" v-if="isShowpic">
        <img :src="url" width="100%">
      </div>

      <ul class="scsa_bottom_ul" style="position:relative;top:-42px;background:#fff;padding-top:30px;">
        <li>
          <span class="statusSpan1">{{backVal1}}</span>
          <span class="statusSpan2">Genes</span>
        </li>
        <li>
          <span class="statusSpan1">{{backVal2}}</span>
          <span class="statusSpan2">Cells</span>
        </li>
        <li>
          <span class="statusSpan1">QC</span>
          <span class="statusSpan2">Pass</span>
        </li>
      </ul>
      <el-button style="margin:-30px 0 30px 20px;" type="primary" @click="Download">Download</el-button>
      <!-- 新增 Cell Identification功能-->
      <div class="scsa">
        <p class="keyword_p1">Cell Identification
        </p>
        <el-form ref="form1" :model="cellIdentification_form" :inline="true" :rules="rules">
          <el-form-item label="Species" prop="species">
            <el-select style="width:200px;" size="large" v-model="cellIdentification_form.species" @change="speciesChange" placeholder="Choose">
              <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.name" :value="item.label">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Tissue" prop="tissue">
            <el-select style="width:200px;" size="large" v-model="cellIdentification_form.tissue" placeholder="Choose">
              <el-option v-for="(item, index) in tissueOptions" :key="index" :label="item" :value="item">
              </el-option>
            </el-select>
          </el-form-item>
          <!-- <el-form-item label="Identification Type" prop="type" style="width:100%;">
            <el-radio-group v-model="cellIdentification_form.type">
              <el-radio label="Garnnet">Garnnet</el-radio>
              <el-radio disabled label="Single">SingleR</el-radio>
            </el-radio-group>
          </el-form-item> -->
        </el-form>
        <el-row style="margin: 0px 0px 40px 0;">
          <el-button type="primary" @click="goCellIdentResult">GO</el-button>
          <!-- <el-button type="primary" @click="goIdentification">GO</el-button> -->
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>

import { sample_qc_upload_picture, cell_species_tissues, cell_tissue_type_down } from "@/api/api";
export default {
  name: "sampleQCFilter",
  components: {
  },
  data() {
    return {
      goLoading: false,
      backVal1: '',
      backVal2: '',
      url: '',
      isShowpic: true,
      result_rds: '',
      cellIdentification_form: {
        species: "Arabidopsis_thaliana",
        type: 'Garnnet',
        tissue: "Root",
      },
      speciesOptions: [],
      tissueOptions: [],
      rules: {
        species: [
          { required: true, message: 'Please select', trigger: 'change' }
        ],
        tissue: [
          { required: true, message: 'Please select', trigger: 'change' }
        ],
        type: [
          { required: true, message: 'Please select', trigger: 'change' }
        ],
      },
    };
  },
  mounted() {
    this.cellIdentification_form.species = this.$route.query.species_name || "Arabidopsis_thaliana"
    this.cellIdentification_form.tissue = this.$route.query.tissue || "Root"
    this.init()
  },
  methods: {
    init() {
      cell_species_tissues({}).then(res => {
        if (res.code == 200) {
          this.speciesOptions = res.data
          this.speciesOptions.forEach(item => {
            if (item.label == this.cellIdentification_form.species) {
              this.tissueOptions = item.value
            }
          });
        }
      });
      // cell_tissue_type_down({ specie_type: this.cellIdentification_form.species }).then(res => {
      //   if (res.code == 200) {
      //     this.tissueOptions = res.data
      //   }
      // });
      // let params = {
      //   files_uuid: this.$route.query.files_uuid,
      //   file_type: this.$route.query.file_type,
      //   sample_id: this.$route.query.sample_id,

      // }
      // this.goLoading = true
      // sample_qc_upload_picture(params).then(res => {
      //   if (res.code == 200) {
      //     this.url = res.data.picture

      //     this.goLoading = false
      //   }
      // });
      let params = {
        files_uuid: this.$route.query.files_uuid,
        sample_id: this.$route.query.sample_id,
        file_type: 'filter',
        filter_min_Feature_RNA_cutmin: JSON.parse(sessionStorage.getItem("sampleFrom")).filter_min_Feature_RNA_cutmin,
        filter_min_mt_cutmin: JSON.parse(sessionStorage.getItem("sampleFrom")).filter_min_mt_cutmin,
        filter_min_pt_cutmin: JSON.parse(sessionStorage.getItem("sampleFrom")).filter_min_pt_cutmin,
        filter_max_Feature_RNA_cutax: JSON.parse(sessionStorage.getItem("sampleFrom")).filter_max_Feature_RNA_cutax,
        filter_max_mt_cutmax: JSON.parse(sessionStorage.getItem("sampleFrom")).filter_max_mt_cutmax,
        filter_max_pt_cutmax: JSON.parse(sessionStorage.getItem("sampleFrom")).filter_max_pt_cutmax,
      }
      this.goLoading = true
      // this.isShowpic = false
      sessionStorage.removeItem("identification_path")
      sample_qc_upload_picture(params).then(res => {
        if (res.code == 200) {
          if (res.data.picture == '') {
            this.$message(res.data.result);
          } else {
            this.url = res.data.picture
            this.backVal1 = res.data.genes
            this.backVal2 = res.data.cells
            this.result_rds = res.data.result_rds
            sessionStorage.setItem("identification_path", res.data.identification_path);
            // this.isShowGenesCells = true
          }
          // NProgress.done()
          this.goLoading = false
          // this.isShowpic = true
        }
      });
    },
    speciesChange(val) {
      this.cellIdentification_form.tissue = ''
      this.tissueOptions = []

      this.speciesOptions.forEach(item => {
        if (item.label == val) {
          this.tissueOptions = item.value
        }
      });

      // cell_tissue_type_down({ specie_type: val }).then(res => {
      //   if (res.code == 200) {
      //     this.tissueOptions = res.data
      //   }
      // });
    },
    Download() {
      window.location.href = this.result_rds
    },
    goIdentification() {
      this.$refs['form1'].validate((valid) => {
        if (valid) {
          this.$router.push({
            path: '/identificationDetails',
            query: {
              tissue_type: this.cellIdentification_form.tissue,
              specie_type: this.cellIdentification_form.species,
              identification_type: this.cellIdentification_form.type,
              files_uuid: this.$route.query.files_uuid,
              file_type: this.$route.query.file_type,
              sample_id: this.$route.query.sample_id
            }
          })
        } else {
          return false;
        }
      });
    },
    goCellIdentResult() {
      this.$refs['form1'].validate((valid) => {
        if (valid) {
          this.$router.push({
            path: '/cellIdentResult',
            query: {
              tissue: this.cellIdentification_form.tissue,
              species_name: this.cellIdentification_form.species,
              uuid_rds: this.result_rds,
              files_uuid: this.$route.query.files_uuid,
              file_type: this.$route.query.file_type,
              sample_id: this.$route.query.sample_id,
              pageType: this.$route.query.pageType
            }
          })
        } else {
          return false;
        }
      });
    }
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>


