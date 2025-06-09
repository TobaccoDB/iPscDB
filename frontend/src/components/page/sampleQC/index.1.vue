<template>
  <div class="sampleQC" :style="{height: contentHeight, minHeight: '390px'}">
    <div class="sampleQC-inner">
      <div class="scsa" v-loading="loading">
        <p class="keyword_p1">Sample QC:
          <!-- <span style="font-size:16px;">Reference data-based cell-type prediction</span> -->
        </p>
        <el-form ref="form1" :model="sampleQC_form" :inline="true" :rules="rules">
          <el-form-item label="Species" prop="species" style="width:100%;">
            <el-select style="width:200px;" size="large" v-model="sampleQC_form.species" placeholder="Choose">
              <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Sample ID" prop="sample_id" style="width:100%;">
            <el-input v-model="sampleQC_form.sample_id" size="large" placeholder="Please enter"></el-input>
          </el-form-item>
          <el-form-item label="File Type" style="width:100%;">
            <el-radio-group v-model="sampleQC_form.type" @change="fileTypeChange">
              <el-radio label="gz">GZ</el-radio>
              <el-radio label="rds">RDS</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item v-if="sampleQC_form.type == 'rds'" label="RDS" prop="rds_name">
            <p class="file_p" v-loading="fileLoading">
              <a href="javascript:;" class="file">Open File
                <input type="file" name="file" ref="file" @change="handleUpdate($event)" />
              </a>
              <span>{{sampleQC_form.rds_name}}</span>
            </p>
          </el-form-item>
          <el-form-item v-if="sampleQC_form.type == 'gz'" label="Barcodes" prop="Barcodes_name">
            <p class="file_p" v-loading="fileLoading1">
              <!-- <span style="padding:0 12px 0 0;">Barcodes</span> -->
              <a href="javascript:;" class="file">Open File
                <input type="file" name="file" ref="file" @change="handleUpdate1($event)" />
              </a>
              <span>{{sampleQC_form.Barcodes_name}}</span>
            </p>
          </el-form-item>
          <el-form-item v-if="sampleQC_form.type == 'gz'" label="Features" prop="Features_name">
            <p class="file_p" v-loading="fileLoading2">
              <a href="javascript:;" class="file">Open File
                <input type="file" name="file" ref="file2" @change="handleUpdate2($event)" />
              </a>
              <span>{{sampleQC_form.Features_name}}</span>
            </p>
          </el-form-item>
          <el-form-item v-if="sampleQC_form.type == 'gz'" label="Matrix" prop="Matrix_name">
            <p class="file_p" v-loading="fileLoading3">
              <a href="javascript:;" class="file">Open File
                <input type="file" name="file" ref="file3" @change="handleUpdate3($event)" />
              </a>
              <span>{{sampleQC_form.Matrix_name}}</span>
            </p>
          </el-form-item>
        </el-form>
        <el-row style="margin: 0px 0px 40px 0;">
          <el-button class="btnSearch" @click="example">Example</el-button>
          <el-button class="btnSearch" style="width:80px;" @click="search">GO</el-button>
          <el-button class="btnReset" @click="reset">Reset</el-button>
        </el-row>
        <ul class="scsa_bottom_ul" v-if="backText != ''">
          <li>{{backText}}</li>
          <li>Genes: {{backVal1}} Cells: {{backVal2}}
            <span class="statusSpan2">QC Pass
            </span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/api/http.js';
import Axios from 'axios'
import { plant_search_down, sample_qc_uuid, sample_qc_upload, sample_qc_upload_picture } from "@/api/api";
export default {
  name: "sampleQC",
  components: {

  },
  data() {
    return {
      contentHeight: (window.innerHeight - 100 - 60 - 120) + 'px',
      speciesOptions: [
      ],
      sampleQC_form: {
        species: "Arabidopsis_thaliana",
        type: 'gz',
        rds_name: "",
        sample_id: "GSM4212552",
        Barcodes_name: "",
        Features_name: "",
        Matrix_name: "",
      },
      rules: {
        species: [
          { required: true, message: 'Please select', trigger: 'change' }
        ],
        sample_id: [
          { required: true, message: 'Please enter', trigger: 'blur' }
        ],
        rds_name: [
          { required: true, message: 'Please select', trigger: 'change' }
        ],
        Barcodes_name: [
          { required: true, message: 'Please select', trigger: 'change' }
        ],
        Features_name: [
          { required: true, message: 'Please select', trigger: 'change' }
        ],
        Matrix_name: [
          { required: true, message: 'Please select', trigger: 'change' }
        ]
      },
      file: "",
      file1: "",
      file2: "",
      file3: "",
      loading: false,
      qcUuid: '',
      fileLoading: false,
      fileLoading1: false,
      fileLoading2: false,
      fileLoading3: false,
      backText: '',
      backVal1: '',
      backVal2: '',
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
      plant_search_down({}).then(res => {
        if (res.code == 200) {
          this.speciesOptions = res.data
        }
      });
      sample_qc_uuid({}).then(res => {
        if (res.code == 200) {
          this.qcUuid = res.data[0]
        }
      });
    },
    fileTypeChange(val) {
      // console.log(12, val)
    },
    example() {
      this.$router.push({
        path: '/sampleDetails',
        query: {
          sample_id: "GSM4212552",
          files_uuid: 'example',
          file_type: 'example'
        }
      })
    },
    search() {
      // if (this.sampleQC_form.type == 'rds' && (this.file == '' || this.sampleQC_form.species == "")) {
      //   this.$message.warning('Please upload a file！');
      //   return
      // }
      // if (this.sampleQC_form.type == 'gz' && (this.file1 == '' || this.file2 == '' || this.file3 == '' || this.sampleQC_form.species == "")) {
      //   this.$message.warning('Please upload a file！');
      //   return
      // }
      if (this.sampleQC_form.type == 'rds' && (this.sampleQC_form.rds_name == '' || this.sampleQC_form.species == "")) {
        this.$message.warning('Please upload a file！');
        return
      }
      if (this.sampleQC_form.type == 'gz' && (this.sampleQC_form.Barcodes_name == '' || this.sampleQC_form.Features_name == '' || this.sampleQC_form.Matrix_name == '' || this.sampleQC_form.species == "")) {
        this.$message.warning('Please upload a file！');
        return
      }
      if (this.fileLoading || this.fileLoading1 || this.fileLoading2 || this.fileLoading3) {
        this.$message.warning('Please wait for the file to upload！');
        return
      }
      this.$router.push({
        path: '/sampleDetails',
        query: {
          files_uuid: this.qcUuid,
          sample_id: this.sampleQC_form.sample_id,
          file_type: this.sampleQC_form.type
        }
      })
    },
    reset() {
      this.file = ''
      this.file2 = ''
      this.file3 = ''
      this.sampleQC_form = {
        type: 'gz',
        species: "Arabidopsis_thaliana",
        sample_id: 'GSM4212552',
        Barcodes_name: "",
        Features_name: "",
        Matrix_name: "",
      }
      this.backText = ''
      this.backVal1 = ''
      this.backVal2 = ''
      this.loading = false
      this.$refs['form1'].resetFields()
    },
    handleUpdate(event) {
      if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'rds') {
        this.$message.warning('Please upload .rds file！');
      } else {
        this.sampleQC_form.rds_name = event.target.files[0].name
        this.fileLoading = true
        this.openFile(this.qcUuid, event.target.files[0], 4, 'Rds')
      }

    },
    handleUpdate1(event) {
      if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'gz') {
        this.$message.warning('Please upload .gz file！');
      } else {
        this.sampleQC_form.Barcodes_name = event.target.files[0].name
        this.fileLoading1 = true
        this.openFile(this.qcUuid, event.target.files[0], 1, 'Barcodes')
      }

    },
    handleUpdate2(event) {
      if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'gz') {
        this.$message.warning('Please upload .gz file！');
      } else {
        this.sampleQC_form.Features_name = event.target.files[0].name
        this.fileLoading2 = true
        this.openFile(this.qcUuid, event.target.files[0], 2, 'Features')
      }
    },
    handleUpdate3(event) {
      if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'gz') {
        this.$message.warning('Please upload .gz file！');
      } else {
        this.sampleQC_form.Matrix_name = event.target.files[0].name
        this.fileLoading3 = true
        this.openFile(this.qcUuid, event.target.files[0], 3, 'Matrix')
      }
    },
    openFile(uuid, file, type, name) {
      this.$refs['form1'].validate((valid) => {

      });
      let formData = new FormData()
      formData.append('files_uuid', uuid)
      formData.append('myfile', file)
      formData.append('file_name', name)
      formData.append('file_type', this.sampleQC_form.type)
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      const $axios = Axios.create({
        baseURL: axios.defaults.baseURL,
        timeout: 1000000
      });

      $axios.post('/api/v1/sample_qc_upload_picture/', formData, config).then(res => {
        // $axios.post('/api/v1/sample_qc_upload/', formData, config).then(res => {
        if (res.data.code == 200) {
          if (type == 4) {
            this.file = file
          } else if (type == 1) {
            this.file1 = file
          } else if (type == 2) {
            this.file2 = file
          } else {
            this.file3 = file
          }
          this.$message.success(res.data.data.msg)
        } else {
          this.$message.warning(res.data.msg);
        }
        this.fileLoading = false
        this.fileLoading1 = false
        this.fileLoading2 = false
        this.fileLoading3 = false
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
