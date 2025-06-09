<template>
  <div class="cellIdentification" :style="{height: contentHeight, minHeight: '390px'}">
    <div class="cellIdentification-inner">
      <div class="scsa" v-loading="loading">
        <p class="keyword_p1">Cell Identification:
        </p>
        <el-form ref="form1" :model="cellIdentification_form" :inline="true" :rules="rules">
          <el-form-item label="Species" prop="species" style="width:100%;">
            <el-select style="width:200px;" size="large" v-model="cellIdentification_form.species" @change="speciesChange" placeholder="Choose">
              <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Tissue" prop="tissue" style="width:100%;">
            <el-select style="width:200px;" size="large" v-model="cellIdentification_form.tissue" placeholder="Choose">
              <el-option v-for="(item, index) in tissueOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Identification Type" prop="type" style="width:100%;">
            <el-radio-group v-model="cellIdentification_form.type" @change="fileTypeChange">
              <el-radio label="Garnnet">Garnnet</el-radio>
              <!-- <el-radio disabled label="Single">SingleR</el-radio> -->
            </el-radio-group>
          </el-form-item>
          <el-form-item label="RDS" prop="rds_name">
            <p class="file_p" v-loading="fileLoading">
              <a href="javascript:;" class="file">Open File
                <input type="file" name="file" ref="file" @change="handleUpdate($event)" />
              </a>
              <span>{{cellIdentification_form.rds_name}}</span>
            </p>
          </el-form-item>
        </el-form>
        <el-row style="margin: 0px 0px 40px 0;">
          <el-button class="btnSearch" @click="example">Example</el-button>
          <el-button class="btnSearch" style="width:80px;" @click="search">GO</el-button>
          <el-button class="btnReset" @click="reset">Reset</el-button>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/api/http.js';
import Axios from 'axios'
import { cell_identification_species_down, cell_tissue_type_down, cell_identification_upload } from "@/api/api";
export default {
  name: "cellIdentification",
  components: {

  },
  data() {
    return {
      contentHeight: (window.innerHeight - 100 - 60 - 120) + 'px',
      speciesOptions: [],
      tissueOptions: [],
      cellIdentification_form: {
        species: "Arabidopsis_thaliana",
        type: 'Garnnet',
        rds_name: "",
        tissue: "",
      },
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
        rds_name: [
          { required: true, message: 'Please select', trigger: 'change' }
        ],
      },
      file: "",
      loading: false,
      fileLoading: false,
      screenHeight: document.body.clientHeight,
      timer: false
    };
  },
  watch: {
    screenHeight(val) {
      // 为了避免频繁触发resize函数导致页面卡顿，使用定时器
      if (!this.timer) {
        // 一旦监听到的screenHeight值改变，就将其重新赋给data里的screenHeight
        this.contentHeight = (val - 100 - 60 - 120) + 'px'
        this.timer = true
        let that = this
        setTimeout(function () {
          that.timer = false
        }, 400)
      }
    },
  },
  mounted() {
    const that = this
    let firstFire = null;
    window.addEventListener('resize', () => {
      if (firstFire === null) {
        firstFire = setTimeout(function () {
          firstFire = null;
          return (() => {
            window.screenHeight = window.innerHeight
            that.screenHeight = window.screenHeight
          })()
        }, 100);
      }
    })

    this.init()
  },
  methods: {
    init() {
      cell_identification_species_down({}).then(res => {
        if (res.code == 200) {
          this.speciesOptions = res.data
        }
      });
      cell_tissue_type_down({ specie_type: this.cellIdentification_form.species }).then(res => {
        if (res.code == 200) {
          this.tissueOptions = res.data
        }
      });
    },
    speciesChange(val) {
      this.cellIdentification_form.tissue = ''
      this.tissueOptions = []
      cell_tissue_type_down({ specie_type: val }).then(res => {
        if (res.code == 200) {
          this.tissueOptions = res.data
        }
      });
    },
    fileTypeChange(val) {
      // console.log(12, val)
    },
    example() {
      this.$router.push({
        path: '/identificationDetails',
        query: {
          from: 'example'
        }
      })
    },
    search() {
      if (this.fileLoading) {
        this.$message.warning('Please wait for the file to upload！');
        return
      }
      this.$refs['form1'].validate((valid) => {
        if (valid) {
          this.$router.push({
            path: '/identificationDetails',
            query: {
              tissue_type: this.cellIdentification_form.tissue,
              specie_type: this.cellIdentification_form.species,
              identification_type: this.cellIdentification_form.type,
              from: 'identification'
            }
          })
        } else {
          return false;
        }
      });


    },
    reset() {
      this.file = ''
      sessionStorage.removeItem("identification_path")
      this.cellIdentification_form = {
        type: 'Garnnet',
        species: "Arabidopsis_thaliana",
        tissue: '',
      }
      this.fileLoading = false
      this.loading = false
      this.$refs['form1'].resetFields()
    },
    handleUpdate(event) {
      if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'rds') {
        this.$message.warning('Please upload .rds file！');
      } else {
        this.cellIdentification_form.rds_name = event.target.files[0].name
        this.fileLoading = true
        this.openFile(event.target.files[0])
      }

    },
    openFile(file) {
      let formData = new FormData()
      formData.append('myfile', file)
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      const $axios = Axios.create({
        baseURL: axios.defaults.baseURL,
        timeout: 1000000
      });

      sessionStorage.removeItem("identification_path")
      $axios.post('/api/v1/cell_identification_upload/', formData, config).then(res => {
        if (res.data.code == 200) {
          this.file = file
          sessionStorage.setItem("identification_path", res.data.data.identification_path);
          this.$refs["form1"].clearValidate('rds_name');
          this.$message.success('File uploaded successfully！')
        } else {
          this.$message.warning(res.data.msg);
        }
        this.fileLoading = false
      }).catch(err => {
        this.$message.warning(err.data.msg);
      });
    }
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
