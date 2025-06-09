<template>
  <div class="CellRanger">
    <div class="CellRanger-inner">
      <div class="stepBar">
        <el-steps :active="stepActive" finish-status="success" :align-center="true">
          <el-step :style="{ cursor: index <= stepActive ? 'pointer' : 'auto' }" @click.native="setpClick(item, index)" :title="item.name"
            v-for="(item, index) in stepList"></el-step>
        </el-steps>
      </div>
      <div class="blast" v-if="!isShowResult" v-loading="pageLoading">
        <el-header>Cell Ranger</el-header>
        <el-form ref="formTop" :inline="true" v-if="isNewJob  && !$route.query.uuid" :model="formTop" :rules="rules">
          <el-form-item label="Email" prop="email">
            <el-input style="width: 160px" v-model="formTop.email" placeholder="Please enter"></el-input>
          </el-form-item>
          <el-form-item label="Analysis name">
            <el-input style="width: 160px" v-model="formTop.analysis_name" placeholder="Please enter"></el-input>
          </el-form-item>
          <el-form-item label="Species" prop="species_name">
            <el-select style="width: 160px" v-model="formTop.species_name" @change="speciesChange" placeholder="Please choose">
              <el-option v-for="(item, index) in speciesList" :key="index" :label="item.name" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Tissue" prop="transcriptome">
            <el-select style="width: 160px" v-model="formTop.transcriptome" placeholder="Please choose">
              <el-option v-for="(item, index) in TranscriptomeList" :key="index" :label="item.name" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="">
            <el-button class="btnSearch" @click="newJob" :disabled="!isNewJob">new job</el-button>
          </el-form-item>
          <el-form-item label="">
            <el-button class="btnSearch" @click="example">Example</el-button>
          </el-form-item>
        </el-form>
        <div :style={opacity:opacity} v-loading="fileLoading" element-loading-text="Uploading">
          <el-header>Data1
            <el-tooltip effect="light" popper-class="tps">
              <span class="fileTips"></span>
              <span slot="content" style="color:#999;font-size: 14px;line-height: 24px;">
                It is highly likely that these files were initially processed with bcl2fastq, so you will need <br>to rename
                the files in the following format, once you track down their origin:<br><br> [Sample Name]_S1_L00[Lane Number]_[Read
                Type]_001.fastq.gz
                <br>
                <br> Where Read Type is one of:<br> I1: Sample index read (optional)<br> I2: Sample index read (optional)<br>                R1: Read 1<br> R2: Read 2
              </span>
            </el-tooltip>
          </el-header>
          <el-form class="uploadForm" ref="formData1" :inline="true" :model="data1Form" label-position="top" :rules="data1Rules">
            <el-form-item label="Sample Name" prop="sample_name" style="width:100%;float:left;display: flex;margin:0;">
              <el-input style="width: 177px;margin-left:10px;" v-model="data1Form.sample_name" placeholder="Please enter" :disabled="isNewJob"></el-input>
            </el-form-item><br />
            <div v-for="(item, index) in data1_List" :key="index" style="margin-top:10px;">
              <el-form-item label="R1" prop="R1" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :key="fileKey" :disabled="isNewJob" @change="handleUpdate($event, index, 'R1')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.R1" placement="top">
                    <span>{{ item.R1 }}</span>
                  </el-tooltip>
                </p> -->
                <span class="dragfileName" v-if="item.R1">{{ item.R1 }}
                  <i class="el-icon-delete delButton" v-if="item.R1 && !$route.query.uuid" @click="deleteFile('data1', item.R1, index, 'R1')"></i>
                </span>
                <div v-else ref="drag" id="drag" class="drag" :index="index" name="R1">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file" :key="fileKey + index" :disabled="isNewJob"
                        @change="handleUpdate($event, index, 'R1')" />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
              <el-form-item label="L1" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :disabled="isNewJob" :key="fileKey" @change="handleUpdate($event, index, 'L1')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.L1" placement="top">
                    <span>{{ item.L1 }}</span>
                  </el-tooltip>
                </p> -->
                <span class="dragfileName" v-if="item.L1">{{ item.L1 }}
                  <i class="el-icon-delete delButton" v-if="item.L1 && !$route.query.uuid" @click="deleteFile('data1', item.L1, index, 'L1')"></i>
                </span>
                <div v-else ref="drag" id="drag" class="drag" :index="index" name="L1">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file" :key="fileKey + index" :disabled="isNewJob"
                        @change="handleUpdate($event, index, 'L1')" />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
              <el-form-item label="R2" prop="R2" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :disabled="isNewJob" :key="fileKey" @change="handleUpdate($event, index,'R2')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.R2" placement="top">
                    <span>{{ item.R2 }}</span>
                  </el-tooltip>
                </p> -->
                <span class="dragfileName" v-if="item.R2">{{ item.R2 }}
                  <i class="el-icon-delete delButton" v-if="item.R2 && !$route.query.uuid" @click="deleteFile('data1', item.R2, index, 'R2')"></i>
                </span>
                <div v-else ref="drag" id="drag" class="drag" :index="index" name="R2">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file" :key="fileKey + index" :disabled="isNewJob"
                        @change="handleUpdate($event, index, 'R2')" />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
              <el-form-item label="L2" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :disabled="isNewJob" :key="fileKey" @change="handleUpdate($event, index, 'L2')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.L2" placement="top">
                    <span>{{ item.L2 }}</span>
                  </el-tooltip>
                </p> -->
                <span class="dragfileName" v-if="item.L2">{{ item.L2 }}
                  <i class="el-icon-delete delButton" v-if="item.L2 && !$route.query.uuid" @click="deleteFile('data1', item.L2, index, 'L2')"></i>
                </span>
                <div v-else ref="drag" id="drag" class="drag" :index="index" name="L2">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file" :key="fileKey + index" :disabled="isNewJob"
                        @change="handleUpdate($event, index, 'L2')" />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
              <el-form-item style="margin-bottom: 0;margin-right:0;" v-if="data1_List.length > 1">
                <el-button class="delBtn" :disabled="isNewJob" @click="data1_remove(index)" type="danger" icon="el-icon-delete" circle></el-button>
              </el-form-item>
            </div>
          </el-form>
          <el-button class="newBtn" icon="el-icon-plus" :disabled="isNewJob" @click="data1_add">new</el-button>
          <el-header style="margin-top:20px;">Data2
            <el-tooltip effect="light" popper-class="tps">
              <span class="fileTips"></span>
              <span slot="content" style="color:#999;font-size: 14px;line-height: 24px;">
                It is highly likely that these files were initially processed with bcl2fastq, so you will need <br>to rename
                the files in the following format, once you track down their origin:<br><br> [Sample Name]_S1_L00[Lane Number]_[Read
                Type]_001.fastq.gz
                <br>
                <br> Where Read Type is one of:<br> I1: Sample index read (optional)<br> I2: Sample index read (optional)<br>                R1: Read 1<br> R2: Read 2
              </span>
            </el-tooltip>
          </el-header>
          <el-form class="uploadForm" ref="formData2" :inline="true" :model="data2Form" label-position="top" :rules="data2Rules">
            <el-form-item label="Sample Name" prop="sample_name" style="width:100%;float:left;display: flex;margin:0;">
              <el-input style="width: 177px;margin-left:10px;" v-model="data2Form.sample_name" placeholder="Please enter" :disabled="isNewJob"></el-input>
            </el-form-item><br />
            <div v-for="(item, index) in data2_List" :key="index">
              <el-form-item label="R1" prop="R1" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :disabled="isNewJob" :key="fileKey" @change="handleUpdate2($event, index, 'R1')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.R1" placement="top">
                    <span>{{ item.R1 }}</span>
                  </el-tooltip>
                </p> -->
                <span class="dragfileName" v-if="item.R1">{{ item.R1 }}
                  <i class="el-icon-delete delButton" v-if="item.R1 && !$route.query.uuid" @click="deleteFile('data2', item.R1, index, 'R1')"></i>
                </span>
                <div v-else ref="drag2" id="drag" class="drag" :index="index" name="R1">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file" :key="fileKey" :disabled="isNewJob" @change="handleUpdate2($event, index, 'R1')"
                      />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
              <el-form-item label="L1" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :disabled="isNewJob" :key="fileKey" @change="handleUpdate2($event, index, 'L1')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.L1" placement="top">
                    <span>{{ item.L1 }}</span>
                  </el-tooltip>
                </p> -->
                <span class="dragfileName" v-if="item.L1">{{ item.L1 }}
                  <i class="el-icon-delete delButton" v-if="item.L1 && !$route.query.uuid" @click="deleteFile('data2', item.L1, index, 'L1')"></i>
                </span>
                <div v-else ref="drag2" id="drag" class="drag" :index="index" name="L1">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file" :key="fileKey" :disabled="isNewJob" @change="handleUpdate2($event, index, 'L1')"
                      />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
              <el-form-item label="R2" prop="R2" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :disabled="isNewJob" :key="fileKey" @change="handleUpdate2($event, index,'R2')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.R2" placement="top">
                    <span>{{ item.R2 }}</span>
                  </el-tooltip>
                </p> -->
                <span class="dragfileName" v-if="item.R2">{{ item.R2 }}
                  <i class="el-icon-delete delButton" v-if="item.R2 && !$route.query.uuid" @click="deleteFile('data2', item.R2, index, 'R2')"></i>
                </span>
                <div v-else ref="drag2" id="drag" class="drag" :index="index" name="R2">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file" :key="fileKey" :disabled="isNewJob" @change="handleUpdate2($event, index, 'R2')"
                      />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
              <el-form-item label="L2" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" :disabled="isNewJob" :key="fileKey" @change="handleUpdate2($event, index, 'L2')"
                    />
                  </a>
                  <el-tooltip class="item" effect="dark" :content="item.L2" placement="top">
                    <span>{{ item.L2 }}</span>
                  </el-tooltip>
                </p> -->
                <span class="dragfileName" v-if="item.L2">{{ item.L2 }}
                  <i class="el-icon-delete delButton" v-if="item.L2 && !$route.query.uuid" @click="deleteFile('data2', item.L2, index, 'L2')"></i>
                </span>
                <div v-else ref="drag2" id="drag" class="drag" :index="index" name="L2">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file" :key="fileKey" :disabled="isNewJob" @change="handleUpdate2($event, index, 'L2')"
                      />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
              <el-form-item style="margin-bottom: 0;margin-right:0;" v-if="data2_List.length > 1">
                <el-button class="delBtn" :disabled="isNewJob" @click="data2_remove(index)" type="danger" icon="el-icon-delete" circle></el-button>
              </el-form-item>
            </div>
          </el-form>
          <el-button class="newBtn" icon="el-icon-plus" :disabled="isNewJob" @click="data2_add">new</el-button>
          <div style="margin-top:20px;">
            <el-button class="btnSearch" :disabled="nextAble" @click="implement" :loading="isImplement">Next</el-button>
            <!-- <el-button class="btnSearch" @click="implement" :loading="isImplement">Cell ranger</el-button> -->
            <!-- <el-button class="btnSearch" @click="implement" :disabled="isNewJob" :loading="isImplement">Cell ranger</el-button> -->
            <el-button class="btnSearch" :disabled="oneAble" :loading="oneLoading" @click="oneStep">One step</el-button>
            <!-- <el-button class="btnSearch" :disabled="isNewJob" :loading="oneLoading" @click="oneStep">One step</el-button> -->
            <!-- <el-button @click="jumpResultPage" v-if="status == 'Finished'">Result</el-button> -->
          </div>
        </div>
        <div style="margin-top:20px;width:100%;height:auto;background: rgba(255, 85, 85, 0.06);color:#FF5555;font-size: 14px;line-height: 24px;padding:13px;box-sizing: border-box;">
          It is highly likely that these files were initially processed with bcl2fastq, so you will need to rename the files in the
          following format, once you track down their origin:<br><br> [Sample Name]_S1_L00[Lane Number]_[Read Type]_001.fastq.gz
          <br>
          <br> Where Read Type is one of:<br> I1: Sample index read (optional)<br> I2: Sample index read (optional)<br> R1:
          Read 1<br> R2: Read 2
        </div>
      </div>
      <CellRangerResult :parent-msg="resultData" v-if="isShowResult"></CellRangerResult>
      <progressBar :progressVisible="progressVisible" :percentage="percentage" @dialogClose="dialogClose"></progressBar>
    </div>
  </div>
</template>

<script>
import axios from '@/api/analysisHttp.js';
import Axios from 'axios'
import { analysis_file_upload, analysis_new_job, specie_down_box, analysisCellranger, analysisInfo, specie_tissue_down_box, upload_file_delete, analysis_step_progress, from_cell_ranger_one_step, analysisCellrangerList } from '@/api/analysis'
import CellRangerResult from '@/components/page/dataAnalysis/CellRangerResult/index'
import progressBar from '@/components/page/dataAnalysis/progressBar/index'

export default {
  name: 'CellRanger',
  components: {
    CellRangerResult,
    progressBar
  },
  data() {
    return {
      resultData: {},
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
      oneLoading: false,
      isShowResultBtn: false,
      info: {},
      fileKey: 0, // 初始的key值
      stepActive: 0,
      pageLoading: false,
      progressVisible: false,
      timer: '',
      percentage: 1,
      nextAble: true,
      oneAble: true,
    }
  },
  mounted() {
    if (this.$route.query.uuid && this.$route.query.enterResults == 'true') {
      this.upload_id = this.$route.query.uuid
      this.isNewJob = false
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
    } else if (this.$route.query.uuid && this.$route.query.enterResults == 'false') {
      this.upload_id = this.$route.query.uuid
      this.isNewJob = false
      this.nextAble = false
      this.oneAble = false
      this.opacity = 1
      this.formTop.species_name = this.$route.query.species_name
      this.formTop.transcriptome = this.$route.query.transcriptome
      this.species = this.$route.query.species_name
      this.transcriptome = this.$route.query.transcriptome
      setTimeout(() => {
        // 给容器绑定相关的拖拽事件
        this.bindEvents()
        this.bindEvents2()
      }, 300)
    } else {
      this.getSpecie_down_box()
      this.isNewJob = true
      this.opacity = 0.4
      setTimeout(() => {
        // 给容器绑定相关的拖拽事件
        this.bindEvents()
        this.bindEvents2()
      }, 300)
    }
    // if (this.$route.query.step == 'sample_qc' && this.$route.query.enterResults) {
    //   this.pageLoading = true
    //   this.jumpResultPage()
    // }
    if (this.$route.query.step == 'sample_qc' || this.$route.query.step == 'data_process' || this.$route.query.step == 'cluster' || this.$route.query.step == 'cell_annotation') {
      this.status = 'Finished'
      this.pageLoading = true
      this.jumpResultPage()
    }
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
  methods: {
    bindEvents() {
      this.$refs.drag && this.$refs.drag.forEach(item => {
        // 被拖动的对象进入目标容器
        item.addEventListener('dragover', e => {
          e.preventDefault()
          item.style.borderColor = 'rgb(36, 164, 97)'
          item.style.opacity = 0.4
        })
        // 被拖动的对象离开目标容器
        item.addEventListener('dragleave', e => {
          e.preventDefault()
          item.style.borderColor = '#b6b6b6'
          item.style.opacity = 1
        })
        // 被拖动的对象进入目标容器，释放鼠标键
        item.addEventListener('drop', e => {
          console.log('释放')
          e.preventDefault()
          item.style.borderColor = '#b6b6b6'
          item.style.opacity = 1
          const fileList = e.dataTransfer.files
          this.uploadFile1(e, item.getAttribute('index'), item.getAttribute('name'))
        })
      });

    },
    bindEvents2() {
      this.$refs.drag2 && this.$refs.drag2.forEach(item => {
        // 被拖动的对象进入目标容器
        item.addEventListener('dragover', e => {
          e.preventDefault()
          item.style.borderColor = 'rgb(36, 164, 97)'
          item.style.opacity = 0.4
        })
        // 被拖动的对象离开目标容器
        item.addEventListener('dragleave', e => {
          e.preventDefault()
          item.style.borderColor = '#b6b6b6'
          item.style.opacity = 1
        })
        // 被拖动的对象进入目标容器，释放鼠标键
        item.addEventListener('drop', e => {
          console.log('释放')
          e.preventDefault()
          item.style.borderColor = '#b6b6b6'
          item.style.opacity = 1
          const fileList = e.dataTransfer.files
          this.uploadFile2(e, item.getAttribute('index'), item.getAttribute('name'))
        })
      });

    },
    // 拖拽上传
    async uploadFile1(event, index, param) {

      if (this.data1Form.sample_name == '') {
        this.$message('Please Choose sample name')
        this.fileKey++;
        return
      }
      if (!this.validateFileName(this.data1Form.sample_name, event.dataTransfer.files[0].name)) {
        this.$message('The file name does not comply with the rules, please upload again!')
        this.fileKey++;
        return
      }
      this.data1_List[index][param] = event.dataTransfer.files[0].name
      const chunkSize = 50 * 1024 * 1024; // 50 MB
      const totalChunks = Math.ceil(event.dataTransfer.files[0].size / chunkSize);
      console.log('chunkSize', chunkSize)
      console.log('totalChunks', totalChunks)
      this.totalChunks = totalChunks
      this.uploadIndex = 0

      const uploadId = this.upload_id; // Generate a unique ID for this upload
      const dataType = 'data1'; // Example data type
      let fileIndex = index; // Example file index
      const fileName = event.dataTransfer.files[0].name;
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
        const end = Math.min(event.dataTransfer.files[0].size, start + chunkSize);
        const chunk = event.dataTransfer.files[0].slice(start, end);
        await this.uploadChunk(chunk, uploadId, dataType, fileIndex, chunkNumber, totalChunks, fileName, file_submit_name, current_row, this.data1Form.sample_name, param, 1);
      }
      event.dataTransfer.value = ''
    },
    // 拖拽上传
    async uploadFile2(event, index, param) {
      if (this.data2Form.sample_name == '') {
        this.$message('Please Choose sample name')
        this.fileKey++;
        return
      }
      if (!this.validateFileName(this.data2Form.sample_name, event.dataTransfer.files[0].name)) {
        this.$message('The file name does not comply with the rules, please upload again!')
        this.fileKey++;
        return
      }
      this.data2_List[index][param] = event.dataTransfer.files[0].name
      const chunkSize = 50 * 1024 * 1024; // 10 MB
      const totalChunks = Math.ceil(event.dataTransfer.files[0].size / chunkSize);
      this.totalChunks = totalChunks
      this.uploadIndex = 0

      const uploadId = this.upload_id; // Generate a unique ID for this upload
      const dataType = 'data2'; // Example data type
      const fileIndex = index; // Example file index
      const fileName = event.dataTransfer.files[0].name;
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
        const end = Math.min(event.dataTransfer.files[0].size, start + chunkSize);
        const chunk = event.dataTransfer.files[0].slice(start, end);
        await this.uploadChunk(chunk, uploadId, dataType, fileIndex, chunkNumber, totalChunks, fileName, file_submit_name, current_row, this.data2Form.sample_name, param, 2);
      }
      event.dataTransfer.value = ''
    },
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
          this.data1Form.sample_name = res.data.data1_sample_name
          this.data2Form.sample_name = res.data.data2_sample_name
          this.info = res.data
          this.species = res.data.species_name
          this.transcriptome = res.data.transcriptome
          this.status = res.data.status
          if (res.data.status == 'Finished') {
            this.isNewJob = true
          } else {
            this.isNewJob = false
          }
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
              this.nextAble = false
              this.oneAble = false
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
    dialogClose() {
      this.progressVisible = false
      clearInterval(this.timer);
    },
    valChange() {
      analysis_step_progress({
        uuid: this.$route.query.uuid || this.upload_id,
        current_step: this.$route.query.step || ''
      }).then((res) => {
        if (res.code == 200 && res.data[0].status != 'FAILURE') {
          this.percentage = res.data[0].progress
          if (res.data[0].progress == 100 && res.data[0].status == 'SUCCESS') {
            this.progressVisible = false
            clearInterval(this.timer);
            this.pageLoading = true
            this.status = 'Finished'
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
      this.oneAble = true
      this.percentage = 1
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
            this.progressVisible = true
            this.timer = setInterval(this.valChange, 3000);
            // this.$router.push({
            //   path: '/analysisFromCellranger',
            //   query: {}
            // })
            this.oneAble = false
          } else {
            this.oneAble = false
            this.$message('Your task failed, please try again。')
            this.progressVisible = false
            this.isImplement = false
            clearInterval(this.timer);
          }
        })
      } else {
        this.oneAble = false
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
        this.oneAble = false
        console.error('表单校验失败', error)
      }
    },
    // 上传
    async handleUpdate(event, index, param) {
      console.log('上传1', event, index, param)
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
      console.log('this.data1_List', this.data1_List)
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
        console.log('await', event.target.files[0])
      }
      event.target.value = ''
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
      formData.append('current_row', current_row);
      formData.append('sample_name', sample_name);
      if (dataType == 'data1') {
        formData.append('data1_sample_name', sample_name)
      } else {
        formData.append('data2_sample_name', sample_name)
      }
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
      event.target.value = ''
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
        setTimeout(() => {
          this.bindEvents()
        }, 300)
      }
    },
    data1_remove(index) {
      console.log(33, Object.values(this.data1_List[index]))
      let filenames = Object.values(this.data1_List[index]).filter(item => item)

      console.log('filenames', filenames)
      if (filenames.length > 0) {
        upload_file_delete({
          upload_id: this.upload_id,
          data_type: 'data1',
          file_name: filenames.join(','),
        }).then((res) => {
          if (res.code == 200) {
            this.data1_List.splice(index, 1);
            this.$message.success('File deleted successfully')
          }
        })
      } else {
        this.data1_List.splice(index, 1);
      }
      setTimeout(() => {
        this.bindEvents()
      }, 300)
    },
    data2_add() {
      if (this.data2_List.length > 2) {
        this.$message({
          message: 'Add up to three new groups!'
        })
      } else {
        this.data2_List.push({ L1: '', L2: '', R1: '', R2: '' })
        setTimeout(() => {
          this.bindEvents2()
        }, 300)
      }
    },
    data2_remove(index) {
      let filenames = Object.values(this.data2_List[index]).filter(item => item)
      if (filenames.length > 0) {
        upload_file_delete({
          upload_id: this.upload_id,
          data_type: 'data2',
          file_name: filenames.join(','),
        }).then((res) => {
          if (res.code == 200) {
            this.data2_List.splice(index, 1);
            this.$message.success('File deleted successfully')
          }
        })
      } else {
        this.data2_List.splice(index, 1);
      }
      setTimeout(() => {
        this.bindEvents2()
      }, 300)
    },
    deleteFile(data_type, file_name, index, type) {
      if (data_type == 'data1') {
        this.data1_List[index][type] = ''
      } else {
        this.data2_List[index][type] = ''
      }
      upload_file_delete({
        upload_id: this.upload_id,
        data_type: data_type,
        file_name: file_name,
      }).then((res) => {
        if (res.code == 200) {
          this.$message.success('File deleted successfully')
        }
      })
    },
    jumpResultPage() {
      if (this.status == 'Finished') {
        this.resultData.uuid = this.$route.query.uuid || this.upload_id
        this.resultData.source = 'cell_ranger'
        this.isShowResult = true
        this.pageLoading = false
      } else if (this.status == 'Started') {
        // this.$message('Executing, please try again later!')
      } else {
        this.$message('Your task failed, please try again。')
      }
    },
    oneStep() {
      this.oneLoading = true
      this.nextAble = true
      from_cell_ranger_one_step({
        uuid: this.$route.query.uuid || this.upload_id,
        species_name: this.formTop.species_name,
        transcriptome: this.formTop.transcriptome
      }).then((res) => {
        if (res.code == 200) {
          // this.$message.success('All steps processed successfully')
          this.loading = false
          this.progressVisible = true
          this.timer = setInterval(this.oneChange, 3000);
          this.nextAble = false
        } else {
          this.$message('Your task failed, please try again。')
          this.progressVisible = false
          this.loading = false
          this.nextAble = false
          clearInterval(this.timer);
        }
        this.oneLoading = false
      })
    },
    oneChange() {
      analysis_step_progress({
        uuid: this.$route.query.uuid || this.upload_id,
        source: 'cell_ranger'
      }).then((res) => {
        if (res.code == 200 && res.data[0].status != 'FAILURE') {
          this.percentage = res.data[0].progress
          if (res.data[0].progress == 100 && res.data[0].status == 'SUCCESS') {
            this.progressVisible = false
            clearInterval(this.timer);
            this.pageLoading = true
            this.status = 'Finished'
            analysisCellrangerList({
              uuid: this.$route.query.uuid || this.upload_id,
              email: '', // 
              analysis_name: '',
              source: 'cell_ranger',
              page: 1,
              page_size: 10
            }).then((res) => {
              if (res.code == 200) {
                this.$router.push({
                  path: '/DataAnalysisCellAnnotation',
                  query: {
                    uuid: this.$route.query.uuid || this.upload_id,
                    id: res.data.results[0].id,
                    step: 'cell_annotation',
                    from: 'cell_ranger',
                  }
                })
              }
            })
          }
        } else {
          this.$message('Your task failed, please try again。')
          this.progressVisible = false
          this.loading = false
          clearInterval(this.timer);
        }
      })
    },
    example() {
      this.resultData.uuid = "8b24bf97-2a04-483f-861a-2f187871870d"
      this.resultData.source = 'cell_ranger'
      this.isShowResult = true
      this.pageLoading = false
    }
  }
}
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
<style lang="scss" scoped>
.dragfileName {
  width: 271px;
  height: 115px;
  box-sizing: border-box;
  border: 1px dashed rgb(182, 182, 182);
  margin: 0 auto;
  display: block;
  text-align: left;
  padding: 10px;
  font-size: 12px;
  color: #333;
  line-height: 20px;
  margin-bottom: 10px;
  overflow: hidden;
  word-wrap: break-word;
  .delButton {
    width: 24px;
    height: 24px;
    cursor: pointer;
    display: none;
  }
}
.dragfileName:hover {
  .delButton {
    width: 24px;
    height: 24px;
    cursor: pointer;
    display: inline-block;
  }
}
.drag {
  width: 271px;
  height: 115px;
  box-sizing: border-box;
  border: 1px dashed rgb(182, 182, 182);
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 10px;
  overflow: hidden;
  .drag-icon-box {
    width: 100%;
    height: 50px;
    text-align: center;
    font-size: 50px;
    line-height: 50px;
    color: #606266;
    position: relative;
    .iconUpload {
      position: absolute;
      width: 30px;
      height: 22.75px;
      display: block;
      // top: 0;
      right: 0;
      left: 0;
      bottom: 0;
      margin: auto;
      background: url(~@/assets/img/upload.png) no-repeat 100%;
      background-size: contain;
    }
  }
  .drag-message {
    width: 100%;
    height: 50px;
    text-align: center;
    .drag-message-title {
      font-size: 14px;
      color: #333;
    }
    .drag-message-label {
      width: 120px;
      height: 50px;
      height: auto;
      position: relative;
      overflow: hidden;
      .drag-message-input {
        // position: absolute;
        // left: -100px;
        // top: -100px;
        // z-index: -1;
        // display: none;
        position: absolute;
        font-size: 5px;
        right: 0;
        top: 0;
        opacity: 0;
        cursor: pointer;
      }
      .drag-message-manual {
        font-size: 14px;
        color: #24a461;
        cursor: pointer;
      }
    }
  }
}
</style>
<style lang="scss">
.tps {
  border-radius: 4px;
  box-shadow: 0px 2px 12px 0px rgba(0, 0, 0, 0.1);
  background: rgb(255, 255, 255);
  border: none !important;
  .popper__arrow {
    border: none !important;
    box-shadow: 0px 2px 12px 0px rgba(0, 0, 0, 0.1);
  }
}
</style>
