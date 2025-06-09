<template>
  <div class="CellRanger">
    <div class="CellRanger-inner">
      <div class="stepBar">
        <el-steps :active="stepActive" finish-status="success" :align-center="true">
          <el-step :style="{ cursor: index <= stepActive ? 'pointer' : 'auto' }" @click.native="setpClick(item, index)" :title="item.name"
            v-for="(item, index) in stepList"></el-step>
        </el-steps>
      </div>
      <div class="blast" v-if="!isShowResult">
        <el-header>Cell Ranger</el-header>
        <el-form ref="formTop" :inline="true" v-if="isNewJob  && !$route.query.uuid" :model="formTop" :rules="rules">
          <el-form-item label="Email" prop="email">
            <el-input style="width: 177px" v-model="formTop.email" placeholder="Please enter"></el-input>
          </el-form-item>
          <el-form-item label="Analysis name">
            <el-input style="width: 177px" v-model="formTop.analysis_name" placeholder="Please enter"></el-input>
          </el-form-item>
          <el-form-item label="Species" prop="species_name">
            <el-select style="width: 177px" v-model="formTop.species_name" @change="speciesChange" placeholder="Please choose">
              <el-option v-for="(item, index) in speciesList" :key="index" :label="item.name" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Tissue" prop="transcriptome">
            <el-select style="width: 177px" v-model="formTop.transcriptome" placeholder="Please choose">
              <el-option v-for="(item, index) in TranscriptomeList" :key="index" :label="item.name" :value="item.name"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="">
            <el-button class="btnSearch" @click="newJob" :disabled="!isNewJob">new job</el-button>
          </el-form-item>
        </el-form>
        <div :style={opacity:opacity} v-loading="fileLoading">
          <el-header>Data1</el-header>
          <el-form ref="formData1" :inline="true" :model="data1Form" :rules="data1Rules">
            <el-form-item label="Sample Name" prop="sample_name">
              <el-input style="width: 177px" v-model="data1Form.sample_name" placeholder="Please enter" :disabled="isNewJob"></el-input>
            </el-form-item><br />
            <div v-for="(item, index) in data1_List" :key="index">
              <el-form-item label="R1" prop="R1" style="margin-bottom: 0">
                <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :key="fileKey" :disabled="isNewJob" @change="handleUpdate($event, index, 'R1')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.R1" placement="top">
                    <span>{{ item.R1 }}</span>
                  </el-tooltip>
                </p>
              </el-form-item>
              <el-form-item label="L1" style="margin-bottom: 0">
                <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :disabled="isNewJob" :key="fileKey" @change="handleUpdate($event, index, 'L1')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.L1" placement="top">
                    <span>{{ item.L1 }}</span>
                  </el-tooltip>
                </p>
              </el-form-item>
              <el-form-item label="R2" prop="R2" style="margin-bottom: 0">
                <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :disabled="isNewJob" :key="fileKey" @change="handleUpdate($event, index,'R2')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.R2" placement="top">
                    <span>{{ item.R2 }}</span>
                  </el-tooltip>
                </p>
              </el-form-item>
              <el-form-item label="L2" style="margin-bottom: 0">
                <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :disabled="isNewJob" :key="fileKey" @change="handleUpdate($event, index, 'L2')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.L2" placement="top">
                    <span>{{ item.L2 }}</span>
                  </el-tooltip>
                </p>
              </el-form-item>
              <el-form-item style="margin-bottom: 0;margin-right:0;" v-if="data1_List.length > 1">
                <el-button class="delBtn" :disabled="isNewJob" @click="data1_remove(index)" type="danger" icon="el-icon-delete" circle></el-button>
              </el-form-item>
            </div>
          </el-form>
          <el-button class="newBtn" icon="el-icon-plus" :disabled="isNewJob" @click="data1_add">new</el-button>
          <el-header style="margin-top:20px;">Data2</el-header>
          <el-form ref="formData2" :inline="true" :model="data2Form" :rules="data2Rules">
            <el-form-item label="Sample Name" prop="sample_name">
              <el-input style="width: 177px" v-model="data2Form.sample_name" placeholder="Please enter" :disabled="isNewJob"></el-input>
            </el-form-item><br />
            <div v-for="(item, index) in data2_List" :key="index">
              <el-form-item label="R1" prop="R1" style="margin-bottom: 0">
                <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :disabled="isNewJob" :key="fileKey" @change="handleUpdate2($event, index, 'R1')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.R1" placement="top">
                    <span>{{ item.R1 }}</span>
                  </el-tooltip>
                </p>
              </el-form-item>
              <el-form-item label="L1" style="margin-bottom: 0">
                <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :disabled="isNewJob" :key="fileKey" @change="handleUpdate2($event, index, 'L1')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.L1" placement="top">
                    <span>{{ item.L1 }}</span>
                  </el-tooltip>
                </p>
              </el-form-item>
              <el-form-item label="R2" prop="R2" style="margin-bottom: 0">
                <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :disabled="isNewJob" :key="fileKey" @change="handleUpdate2($event, index,'R2')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.R2" placement="top">
                    <span>{{ item.R2 }}</span>
                  </el-tooltip>
                </p>
              </el-form-item>
              <el-form-item label="L2" style="margin-bottom: 0">
                <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :disabled="isNewJob" :key="fileKey" @change="handleUpdate2($event, index, 'L2')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.L2" placement="top">
                    <span>{{ item.L2 }}</span>
                  </el-tooltip>
                </p>
              </el-form-item>
              <el-form-item style="margin-bottom: 0;margin-right:0;" v-if="data2_List.length > 1">
                <el-button class="delBtn" :disabled="isNewJob" @click="data2_remove(index)" type="danger" icon="el-icon-delete" circle></el-button>
              </el-form-item>
            </div>
          </el-form>
          <el-button class="newBtn" icon="el-icon-plus" :disabled="isNewJob" @click="data2_add">new</el-button>
          <div style="margin-top:20px;">
            <el-button class="btnSearch" v-if="!$route.query.uuid" @click="implement" :disabled="isNewJob" :loading="isImplement">Cell ranger</el-button>
            <el-button class="btnSearch" :disabled="isNewJob">One step</el-button>
            <el-button @click="jumpResultPage" :disabled="isNewJob && !$route.query.uuid">Result</el-button>
          </div>
        </div>
      </div>
      <CellRangerResult v-if="isShowResult"></CellRangerResult>
    </div>
  </div>
</template>

<script>
import axios from '@/api/analysisHttp.js';
import Axios from 'axios'
import { analysis_file_upload, analysis_new_job, specie_down_box, analysisCellranger, analysisInfo, specie_tissue_down_box } from '@/api/analysis'
import CellRangerResult from '@/components/page/dataAnalysis/CellRangerResult/index'

export default {
  name: 'CellRanger',
  components: {
    CellRangerResult
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
        email: '',
        analysis_name: '',
        species_name: '',
        transcriptome: '',
      },
      speciesList: [],
      TranscriptomeList: [],
      data1_List: [
        { L1: '', L2: '', R1: '', R2: '' }
      ],
      data2_List: [
        { L1: '', L2: '', R1: '', R2: '' }
      ],
      rules: {
        email: [
          { required: true, message: 'Please enter your email address', trigger: 'blur' },
          { type: 'email', message: 'Please enter the correct email address', trigger: ['blur', 'change'] }
        ],
        species_name: [
          { required: true, message: 'Please choose', trigger: 'change' }
        ],
        transcriptome: [
          { required: true, message: 'Please choose', trigger: 'change' }
        ],
      },
      data1Form: {
        sample_name: '',
      },
      data1Rules: {
        R1: [
          { required: true, message: 'Please choose', trigger: 'change' }
        ],
        R2: [
          { required: true, message: 'Please choose', trigger: 'change' }
        ],
        sample_name: [
          { required: true, message: 'Please enter', trigger: 'blur' }
        ],
      },
      data2Form: {
        sample_name: '',
      },
      data2Rules: {
        R1: [
          { required: true, message: 'Please choose', trigger: 'change' }
        ],
        R2: [
          { required: true, message: 'Please choose', trigger: 'change' }
        ],
        sample_name: [
          { required: true, message: 'Please enter', trigger: 'blur' }
        ],
      },
      fileLoading: false,
      isShowResult: false,
      isNewJob: true,
      opacity: 0.4,
      upload_id: '',
      species: '',
      transcriptome: '',
      status: '',
      totalChunks: 0,
      uploadIndex: 0,
      isImplement: false,
      isShowResultBtn: false,
      info: {},
      fileKey: 0, // 初始的key值
      stepActive: 0
    }
  },
  mounted() {
    if (this.$route.query.uuid) {
      this.upload_id = this.$route.query.uuid
      this.isNewJob = true
      this.opacity = 1
      this.analysisInfo()
      this.stepList.forEach((item, index) => {
        if (this.$route.query.step == item.step) {
          this.stepActive = index
          if (this.$route.query.step == 'cell_annotation') {
            this.stepActive = Number(this.stepActive) + 1
          }
        }
      });
    } else {
      this.getSpecie_down_box()
      this.isNewJob = true
      this.opacity = 0.4
    }
  },
  methods: {
    setpClick(item, index) {
      //   STEP_CHOICES = (
      // ('cell_ranger', 'Cell Ranger'),
      // ('sample_qc', 'Sample QC'),
      // ('data_process', 'Data Process'),
      // ('cluster', 'Cluster'),
      // ('cell_annotation', 'Cell Annotation'),)
      // let str = location.href; //取得整个地址栏
      // let num = str.indexOf("?")
      // str = str.substr(num + 1); //取得所有参数 stringvar.substr(start [, length ]
      // let arr = str.split("&"); //各个参数放到数组里
      // let query = {}
      // arr.forEach(item => {
      //   query[item.split('=')[0]] = item.split('=')[1]
      // })
      if (this.$route.query.uuid && (index < this.stepActive || index == this.stepActive)) {
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
    getSpecie_down_box() {
      specie_down_box({ type: 'species' }).then((res) => {
        if (res.code == 200) {
          this.speciesList = res.data
        }
      })
    },
    speciesChange(val) {
      specie_tissue_down_box({ species_name: val }).then((res) => {
        if (res.code == 200) {
          this.formTop.transcriptome = ''
          this.TranscriptomeList = res.data
        }
      })
    },
    analysisInfo() {
      analysisInfo(this.$route.query.id).then((res) => {
        if (res.code == 200) {
          this.info = res.data
          this.species = res.data.species_name
          this.transcriptome = res.data.transcriptome
          this.status = res.data.status
          this.data1_List = [
            { L1: '', L2: '', R1: '', R2: '' },
            { L1: '', L2: '', R1: '', R2: '' },
            { L1: '', L2: '', R1: '', R2: '' },
          ]
          this.data2_List = [
            { L1: '', L2: '', R1: '', R2: '' },
            { L1: '', L2: '', R1: '', R2: '' },
            { L1: '', L2: '', R1: '', R2: '' },
          ]
          res.data.file_name.forEach(item => {
            if (item.data_type == 'data1') {
              if (item.current_row == 'first') {
                this.data1_List[0][item.file_submit_name] = item.filename
              } else if (item.current_row == 'second') {
                this.data1_List[1][item.file_submit_name] = item.filename
              } else {
                this.data1_List[2][item.file_submit_name] = item.filename
              }
            } else {
              if (item.current_row == 'first') {
                this.data2_List[0][item.file_submit_name] = item.filename
              } else if (item.current_row == 'second') {
                this.data2_List[1][item.file_submit_name] = item.filename
              } else {
                this.data2_List[2][item.file_submit_name] = item.filename
              }
            }
          });
          this.data1_List.forEach((item, index) => {
            if (item.L1 == '' && item.L2 == '' && item.R1 == '' && item.R2 == '' && index > 0) {
              this.data1_List.splice(index, 3 - index);
            }
          });
          this.data2_List.forEach((item, index) => {
            if (item.L1 == '' && item.L2 == '' && item.R1 == '' && item.R2 == '' && index > 0) {
              this.data2_List.splice(index, 3 - index);
            }
          });

        }
      })
    },
    newJob() {
      this.$refs['formTop'].validate((valid) => {
        if (valid) {
          analysis_new_job(Object.assign({}, this.formTop, { source: 'cell_ranger' })).then((res) => {
            if (res.code == 200) {
              this.upload_id = res.data
              this.isNewJob = false
              this.opacity = 1
              this.species = this.formTop.species_name
              this.transcriptome = this.formTop.transcriptome
              this.$message.success('new Job successfully!')
            }
          })

        } else {
          return false;
        }
      });
    },
    // implement() { //执行 cell ranger
    //   this.$refs['formData1'].validate((valid) => {
    //     if (valid) {


    //     } else {
    //       return false;
    //     }
    //   });
    // },
    async implement() { //执行
      let isPass = true
      this.data1_List.forEach(item => {
        if (item.R1 == '' || item.R2 == '') {
          isPass = false
        }
      });
      this.data2_List.forEach(item => {
        if (item.R1 == '' || item.R2 == '') {
          isPass = false
        }
      });
      if (isPass) {
        this.isImplement = true
        analysisCellranger({
          uuid: this.upload_id,
          species_name: this.species,
          transcriptome: this.transcriptome,
        }).then((res) => {
          if (res.code == 200) {
            this.isImplement = false
            this.$router.push({
              path: '/analysisFromCellranger',
              query: {}
            })
          }
        })
      } else {
        this.$message('Please upload the required items!')
      }
      try {
        // await this.$refs.formData1.validate()
        // console.log('表单1校验通过')
        // await this.$refs.formData2.validate()
        // console.log('表单2校验通过')
        //都校验成功之后，这里可以发请求
        // this.$message.success('表单校验成功')
      } catch (error) {
        console.error('表单校验失败', error)
      }
    },
    // 上传
    async handleUpdate(event, index, param) {

      if (this.data1Form.sample_name == '') {
        this.$message('Please Choose sample name')
        this.fileKey++;
        return
      }
      if (!this.validateFileName(this.data1Form.sample_name, event.target.files[0].name)) {
        this.$message('The file name does not comply with the rules, please upload again!')
        this.fileKey++;
        return
      }
      this.data1_List[index][param] = event.target.files[0].name
      const chunkSize = 50 * 1024 * 1024; // 50 MB
      const totalChunks = Math.ceil(event.target.files[0].size / chunkSize);
      this.totalChunks = totalChunks
      this.uploadIndex = 0

      const uploadId = this.upload_id; // Generate a unique ID for this upload
      const dataType = 'data1'; // Example data type
      let fileIndex = index; // Example file index
      const fileName = event.target.files[0].name;
      const file_submit_name = param.split("_")[0]
      let current_row = 'first'
      if (index == 0) {
        current_row = 'first'
      } else if (index == 1) {
        current_row = 'second'
      } else {
        current_row = 'third'
      }

      for (let chunkNumber = 0; chunkNumber < totalChunks; chunkNumber++) {
        // fileIndex = chunkNumber
        const start = chunkNumber * chunkSize;
        const end = Math.min(event.target.files[0].size, start + chunkSize);
        const chunk = event.target.files[0].slice(start, end);
        await this.uploadChunk(chunk, uploadId, dataType, fileIndex, chunkNumber, totalChunks, fileName, file_submit_name, current_row, this.data1Form.sample_name, param, 1);
      }
    },
    async uploadChunk(chunk, uploadId, dataType, fileIndex, chunkNumber, totalChunks, fileName, file_submit_name, current_row, sample_name, param, idx) {
      this.fileLoading = true
      const formData = new FormData();
      formData.append('file', chunk);
      formData.append('upload_id', uploadId);
      formData.append('data_type', dataType);
      formData.append('file_index', fileIndex);
      formData.append('chunk_number', Number(chunkNumber) + 1);
      formData.append('total_chunks', totalChunks);
      formData.append('filename', fileName);
      formData.append('file_submit_name', file_submit_name);
      formData.append('current_row ', current_row);
      formData.append('sample_name ', sample_name);
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      const $axios = Axios.create({
        baseURL: axios.defaults.baseURL,
        timeout: 1000000
      })

      $axios.post('/v1/analysis_file_upload/', formData, config).then((res) => {
        if (res.data.code == 200) {
          this.uploadIndex = Number(this.uploadIndex) + 1
          if (this.uploadIndex == this.totalChunks) {
            this.$message.success('Upload successful!')
            this.fileLoading = false
          }
        } else {
          this.uploadIndex = Number(this.uploadIndex) + 1
          if (this.uploadIndex == this.totalChunks) {
            this.fileKey++;
            this.$message.warning('Upload failed!')
            if (idx == 1) {
              this.data1_List[fileIndex][param] = ''
            } else {
              this.data2_List[fileIndex][param] = ''
            }
            this.fileLoading = false
          }
        }

      }).catch((err) => {
        this.uploadIndex = Number(this.uploadIndex) + 1
        if (this.uploadIndex == this.totalChunks) {
          this.fileKey++;
          if (idx == 1) {
            this.data1_List[fileIndex][param] = ''
          } else {
            this.data2_List[fileIndex][param] = ''
          }
          this.$message.warning('Upload failed!')
          this.fileLoading = false
        }
      })
    },
    async handleUpdate2(event, index, param) {
      if (this.data2Form.sample_name == '') {
        this.$message('Please Choose sample name')
        this.fileKey++;
        return
      }
      if (!this.validateFileName(this.data2Form.sample_name, event.target.files[0].name)) {
        this.$message('The file name does not comply with the rules, please upload again!')
        this.fileKey++;
        return
      }
      this.data2_List[index][param] = event.target.files[0].name
      const chunkSize = 50 * 1024 * 1024; // 10 MB
      const totalChunks = Math.ceil(event.target.files[0].size / chunkSize);
      this.totalChunks = totalChunks
      this.uploadIndex = 0

      const uploadId = this.upload_id; // Generate a unique ID for this upload
      const dataType = 'data2'; // Example data type
      const fileIndex = index; // Example file index
      const fileName = event.target.files[0].name;
      const file_submit_name = param.split("_")[0]
      let current_row = 'first'
      if (index == 0) {
        current_row = 'first'
      } else if (index == 1) {
        current_row = 'second'
      } else {
        current_row = 'third'
      }
      for (let chunkNumber = 0; chunkNumber < totalChunks; chunkNumber++) {
        const start = chunkNumber * chunkSize;
        const end = Math.min(event.target.files[0].size, start + chunkSize);
        const chunk = event.target.files[0].slice(start, end);
        await this.uploadChunk(chunk, uploadId, dataType, fileIndex, chunkNumber, totalChunks, fileName, file_submit_name, current_row, this.data2Form.sample_name, param, 2);
      }
    },
    // 验证文件名是否符合规则
    validateFileName(prefix, filename) {
      // const pattern = /^[\w\-]+_S\d+_L\d+_R\d+_\d+\.fastq\.gz+$/i;
      // const prefix = "scDR1"; // 定义前缀 
      const pattern = new RegExp(`^${prefix}_S\\d+_L\\d+_R\\d+_\\d+\\.fastq\\.gz$`);// 定义正则表达式模式 
      return pattern.test(filename);
    },
    data1_add() {
      if (this.data1_List.length > 2) {
        this.$message({
          message: 'Add up to three new groups!'
        })
      } else {
        this.data1_List.push({ L1: '', L2: '', R1: '', R2: '' })
      }
    },
    data1_remove(index) {
      this.data1_List.splice(index, 1);
    },
    data2_add() {
      if (this.data2_List.length > 2) {
        this.$message({
          message: 'Add up to three new groups!'
        })
      } else {
        this.data2_List.push({ L1: '', L2: '', R1: '', R2: '' })
      }
    },
    data2_remove(index) {
      this.data2_List.splice(index, 1);
    },
    jumpResultPage() {
      if (this.status) {
        this.isShowResult = true
      }
    }
  }
}
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
