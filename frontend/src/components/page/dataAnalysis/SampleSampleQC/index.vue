<template>
  <div class="SampleSampleQC">
    <div class="SampleSampleQC-inner">
      <div class="stepBar">
        <el-steps :active="stepActive" finish-status="success" :align-center="true">
          <el-step :style="{ cursor: index <= stepActive ? 'pointer' : 'auto' }" @click.native="setpClick(item, index)" :title="item.name"
            v-for="(item, index) in stepList"></el-step>
        </el-steps>
      </div>
      <div class="blast" v-if="isShowQC" v-loading="pageLoading">
        <!--                       Sample QC                       -->
        <el-header>Sample QC</el-header>
        <el-form ref="formTop" :inline="true" v-if="isNewJob  && !$route.query.uuid" :model="formTop" :rules="formTopRules">
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
          <el-form class="uploadForm" ref="formFile1" :model="formFile1" label-position="top" :inline="true" :rules="rules">
            <el-header>Data1</el-header>
            <el-form-item label="Sample Name" prop="data1_sample_name" style="float:left;display: flex;margin:0;">
              <el-input style="width: 177px;margin-left:10px;" v-model="formFile1.data1_sample_name" placeholder="Please enter" :disabled="isNewJob"></el-input>
            </el-form-item>
            <el-form-item label="File Type" style="width:60%;float:left;display: flex;margin:0;margin-left:10px;">
              <el-radio-group style="margin-left:10px;" @input="radioChange1" v-model="formFile1.type" :disabled="isNewJob">
                <el-radio label="gz">GZ</el-radio>
                <el-radio label="h5">H5</el-radio>
              </el-radio-group>
            </el-form-item>
            <br />
            <div v-for="(item, index) in data1_List" :key="index">
              <el-form-item v-if="formFile1.type == 'h5'" label="H5" prop="filtered_feature_bc_matrix" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file" :disabled="isNewJob" @change="handleUpdate1($event, 'filtered_feature_bc_matrix')"
                  />
                </a>
                <span style="width:1000px">{{ formFile1.filtered_feature_bc_matrix }}</span>
              </p> -->
                <span class="dragfileName" v-if="formFile1.filtered_feature_bc_matrix">{{ formFile1.filtered_feature_bc_matrix }}
                  <i class="el-icon-delete delButton" v-if="formFile1.filtered_feature_bc_matrix && !$route.query.uuid" @click="deleteFile('data1', formFile1.filtered_feature_bc_matrix, 'filtered_feature_bc_matrix')"></i>
                </span>
                <div v-else ref="drag" id="drag" class="drag" index="0" name="filtered_feature_bc_matrix">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file" :disabled="isNewJob" @change="handleUpdate1($event, 'filtered_feature_bc_matrix')"
                      />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
              <el-form-item v-if="formFile1.type == 'gz'" label="Barcodes" prop="barcodes" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                <span style="padding:0 12px 0 0;">Barcodes</span>
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file" :disabled="isNewJob" @change="handleUpdate1($event, 'barcodes')" />
                </a>
                <el-tooltip class="item" effect="dark" :content="formFile1.barcodes" placement="top">
                  <span>{{ formFile1.barcodes }}</span>
                </el-tooltip>
              </p> -->
                <span class="dragfileName" v-if="formFile1.barcodes">{{ formFile1.barcodes }}
                  <i class="el-icon-delete delButton" v-if="formFile1.barcodes && !$route.query.uuid" @click="deleteFile('data1', formFile1.barcodes, 'barcodes')"></i>
                </span>
                <div v-else ref="drag" id="drag" class="drag" index="1" name="barcodes">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file" :disabled="isNewJob" @change="handleUpdate1($event, 'barcodes')"
                      />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
              <el-form-item v-if="formFile1.type == 'gz'" label="Features" prop="features" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file2" :disabled="isNewJob" @change="handleUpdate1($event, 'features')" />
                </a>
                <el-tooltip class="item" effect="dark" :content="formFile1.features" placement="top">
                  <span>{{ formFile1.features }}</span>
                </el-tooltip>
              </p> -->
                <span class="dragfileName" v-if="formFile1.features">{{ formFile1.features }}
                  <i class="el-icon-delete delButton" v-if="formFile1.features && !$route.query.uuid" @click="deleteFile('data1', formFile1.features, 'features')"></i>
                </span>
                <div v-else ref="drag" id="drag" class="drag" index="2" name="features">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file" :disabled="isNewJob" @change="handleUpdate1($event, 'features')"
                      />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
              <el-form-item v-if="formFile1.type == 'gz'" label="Matrix" prop="matrix" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file3" :disabled="isNewJob" @change="handleUpdate1($event, 'matrix')" />
                </a>
                <el-tooltip class="item" effect="dark" :content="formFile1.matrix" placement="top">
                  <span>{{ formFile1.matrix }}</span>
                </el-tooltip>
              </p> -->
                <span class="dragfileName" v-if="formFile1.matrix">{{ formFile1.matrix }}
                  <i class="el-icon-delete delButton" v-if="formFile1.matrix && !$route.query.uuid" @click="deleteFile('data1', formFile1.matrix, 'matrix')"></i>
                </span>
                <div v-else ref="drag" id="drag" class="drag" index="3" name="matrix">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file" :disabled="isNewJob" @change="handleUpdate1($event, 'matrix')"
                      />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
            </div>
          </el-form>
          <el-header style="width:100%;overflow: hidden;">Data2</el-header>
          <el-form class="uploadForm" ref="formFile2" :model="formFile2" label-position="top" :inline="true" :rules="rules">
            <el-form-item label="Sample Name" prop="data2_sample_name" style="float:left;display: flex;margin:0;">
              <el-input style="width: 177px;margin-left:10px;" v-model="formFile2.data2_sample_name" placeholder="Please enter" :disabled="isNewJob"></el-input>
            </el-form-item>
            <el-form-item label="File Type" style="width:60%;float:left;display: flex;margin:0;margin-left:10px;">
              <el-radio-group style="margin-left:10px;" @input="radioChange2" v-model="formFile2.type" :disabled="isNewJob">
                <el-radio label="gz">GZ</el-radio>
                <el-radio label="h5">H5</el-radio>
              </el-radio-group>
            </el-form-item>
            <br />
            <div v-for="(item, index) in data1_List" :key="index">
              <el-form-item v-if="formFile2.type == 'h5'" label="H5" prop="filtered_feature_bc_matrix" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file" :disabled="isNewJob" @change="handleUpdate2($event, 'filtered_feature_bc_matrix')"
                  />
                </a>
                <span style="width:1000px">{{ formFile2.filtered_feature_bc_matrix }}</span>
              </p> -->
                <span class="dragfileName" v-if="formFile2.filtered_feature_bc_matrix">{{ formFile2.filtered_feature_bc_matrix }}
                  <i class="el-icon-delete delButton" v-if="formFile2.filtered_feature_bc_matrix && !$route.query.uuid" @click="deleteFile('data2', formFile2.filtered_feature_bc_matrix, 'filtered_feature_bc_matrix')"></i>
                </span>
                <div v-else ref="drag2" id="drag" class="drag" name="filtered_feature_bc_matrix">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file" :disabled="isNewJob" @change="handleUpdate2($event, 'filtered_feature_bc_matrix')"
                      />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
              <el-form-item v-if="formFile2.type == 'gz'" label="Barcodes" prop="barcodes" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                <span style="padding:0 12px 0 0;">Barcodes</span>
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file" :disabled="isNewJob" @change="handleUpdate2($event, 'barcodes')" />
                </a>
                <el-tooltip class="item" effect="dark" :content="formFile2.barcodes" placement="top">
                  <span>{{ formFile2.barcodes }}</span>
                </el-tooltip>
              </p> -->
                <span class="dragfileName" v-if="formFile2.barcodes">{{ formFile2.barcodes }}
                  <i class="el-icon-delete delButton" v-if="formFile2.barcodes && !$route.query.uuid" @click="deleteFile('data2', formFile2.barcodes, 'barcodes')"></i>
                </span>
                <div v-else ref="drag2" id="drag" class="drag" name="barcodes">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file" :disabled="isNewJob" @change="handleUpdate2($event, 'barcodes')"
                      />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
              <el-form-item v-if="formFile2.type == 'gz'" label="Features" prop="features" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file2" :disabled="isNewJob" @change="handleUpdate2($event, 'features')" />
                </a>
                <el-tooltip class="item" effect="dark" :content="formFile2.features" placement="top">
                  <span>{{ formFile2.features }}</span>
                </el-tooltip>
              </p> -->
                <span class="dragfileName" v-if="formFile2.features">{{ formFile2.features }}
                  <i class="el-icon-delete delButton" v-if="formFile2.features && !$route.query.uuid" @click="deleteFile('data2', formFile2.features, 'features')"></i>
                </span>
                <div v-else ref="drag2" id="drag" class="drag" name="features">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file2" :disabled="isNewJob" @change="handleUpdate2($event, 'features')"
                      />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
              <el-form-item v-if="formFile2.type == 'gz'" label="Matrix" prop="matrix" style="text-align:center;margin-right: 20px;">
                <!-- <p class="file_p">
                <a href="javascript:;" class="file">Open File
                  <input type="file" name="file" ref="file3" :disabled="isNewJob" @change="handleUpdate2($event, 'matrix')" />
                </a>
                <el-tooltip class="item" effect="dark" :content="formFile2.matrix" placement="top">
                  <span>{{ formFile2.matrix }}</span>
                </el-tooltip>
              </p> -->
                <span class="dragfileName" v-if="formFile2.matrix">{{ formFile2.matrix }}
                  <i class="el-icon-delete delButton" v-if="formFile2.matrix && !$route.query.uuid" @click="deleteFile('data2', formFile2.matrix, 'matrix')"></i>
                </span>
                <div v-else ref="drag2" id="drag" class="drag" name="matrix">
                  <div class="drag-icon-box">
                    <i class="iconUpload"></i>
                  </div>
                  <div class="drag-message">
                    <span class="drag-message-title">Drop file here or </span>
                    <label for="file" class="drag-message-label">
                      <input class="drag-message-input" type="file" id="file" name="file" ref="file3" :disabled="isNewJob" @change="handleUpdate2($event, 'matrix')"
                      />
                      <span class="drag-message-manual">click to upload</span>
                    </label>
                  </div>
                </div>
              </el-form-item>
            </div>
          </el-form>

          <el-form :style={opacity:opacity} ref="formBottom" :inline="true" :model="formBottom" :rules="formBottomRules">
            <el-form-item label="pt">
              <el-input v-model="formBottom.pt" :disabled="isNewJob && !$route.query.uuid" clearable placeholder="Please enter"></el-input>
            </el-form-item>
            <el-form-item label="mt">
              <el-input v-model="formBottom.mt" :disabled="isNewJob && !$route.query.uuid" clearable placeholder="Please enter"></el-input>
            </el-form-item>
            <br />
            <el-form-item label="">
              <el-button class="btnSearch" :loading="runLoading" :disabled="nextAble" @click="runQC('qc')">Next</el-button>
              <!-- <el-button class="btnSearch" :loading="runLoading" :disabled="isNewJob && !$route.query.uuid && nextAble" @click="runQC('qc')">Next</el-button> -->
              <!-- <el-button class="btnSearch" :loading="runLoading" :disabled="isNewJob && !$route.query.uuid" @click="runQC('qc')">Run QC</el-button> -->
              <el-button class="btnSearch" :disabled="oneAble" :loading="oneLoading" @click="oneStep">One step</el-button>
              <!-- <el-button class="btnSearch" :disabled="isNewJob && !$route.query.uuid && oneAble" :loading="oneLoading" @click="oneStep">One step</el-button> -->
              <!-- <el-button :disabled="isNewJob && !$route.query.uuid" @click="runQC('qcResult')">Run QC result</el-button> -->
              <!-- <el-button v-if="$route.query.uuid" :loading="runResultLoading" @click="runQC('qcResult')">Run QC result</el-button> -->
            </el-form-item>
          </el-form>
        </div>
      </div>
      <!--              Sample QC Result                   -->
      <div class="blast" v-if="!isShowResult&& !isShowQC">
        <el-header>Data1</el-header>
        <div style="">
          <ul class="sample_table">
            <li></li>
            <li>nCount_RNA</li>
            <li>nFeatuer_RNA</li>
            <li v-if="formBottom.mt">percent.mt</li>
            <li v-if="formBottom.pt">percent.pt</li>
          </ul>
          <ul class="sample_table">
            <li>min</li>
            <li>{{ data1.min_nCount_RNA }}</li>
            <li>{{ data1.min_nFeature_RNA }}</li>
            <li v-if="formBottom.mt">{{ data1.min_percent_mt }}</li>
            <li v-if="formBottom.pt">{{ data1.min_percent_pt }}</li>
          </ul>
          <ul class="sample_table">
            <li>max</li>
            <li>{{ data1.max_nCount_RNA }}</li>
            <li>{{ data1.max_nFeature_RNA }}</li>
            <li v-if="formBottom.mt">{{ data1.max_percent_mt }}</li>
            <li v-if="formBottom.pt">{{ data1.max_percent_pt }}</li>
          </ul>
        </div>
        <el-header>Data2</el-header>
        <div style="">
          <ul class="sample_table">
            <li></li>
            <li>nCount_RNA</li>
            <li>nFeatuer_RNA</li>
            <li v-if="formBottom.mt">percent.mt</li>
            <li v-if="formBottom.pt">percent.pt</li>
          </ul>
          <ul class="sample_table">
            <li>min</li>
            <li>{{ data2.min_nCount_RNA }}</li>
            <li>{{ data2.min_nFeature_RNA }}</li>
            <li v-if="formBottom.mt">{{ data2.min_percent_mt }}</li>
            <li v-if="formBottom.pt">{{ data2.min_percent_pt }}</li>
          </ul>
          <ul class="sample_table">
            <li>max</li>
            <li>{{ data2.max_nCount_RNA }}</li>
            <li>{{ data2.max_nFeature_RNA }}</li>
            <li v-if="formBottom.mt">{{ data2.max_percent_mt }}</li>
            <li v-if="formBottom.pt">{{ data2.max_percent_pt }}</li>
          </ul>
        </div>
        <p class="title2">QC filter</p>
        <el-form class="form1" ref="form1" :inline="true" :model="form" label-width="140px">
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="grid-content bg-purple">
                <el-form-item label="min nCount_RNA" prop="min_nCount_RNA">
                  <el-input style="width: 120px" v-model="form.min_nCount_RNA"></el-input>
                </el-form-item>
                <el-form-item label="max nCount_RNA" prop="max_nCount_RNA">
                  <el-input style="width: 120px" v-model="form.max_nCount_RNA"></el-input>
                </el-form-item>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="grid-content bg-purple">
                <el-form-item label="min nFeatuer_RNA" prop="min_nFeature_RNA">
                  <el-input style="width: 120px" v-model="form.min_nFeature_RNA"></el-input>
                </el-form-item>
                <el-form-item label="max nFeatuer_RNA" prop="max_nFeature_RNA">
                  <el-input style="width: 120px" v-model="form.max_nFeature_RNA"></el-input>
                </el-form-item>
              </div>
            </el-col>
            <el-col :span="6" v-if="formBottom.mt">
              <div class="grid-content bg-purple">
                <el-form-item label="min percent.mt" prop="min_percent_mt">
                  <el-input style="width: 120px" v-model="form.min_percent_mt"></el-input>
                </el-form-item>
                <el-form-item label="max percent.mt" prop="max_percent_mt">
                  <el-input style="width: 120px" v-model="form.max_percent_mt"></el-input>
                </el-form-item>
              </div>
            </el-col>
            <el-col :span="6" v-if="formBottom.pt">
              <div class="grid-content bg-purple">
                <el-form-item label="min percent.pt" prop="min_percent_pt">
                  <el-input style="width: 120px" v-model="form.min_percent_pt"></el-input>
                </el-form-item>
                <el-form-item label="max percent.pt" prop="max_percent_pt">
                  <el-input style="width: 120px" v-model="form.max_percent_pt"></el-input>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
        </el-form>
        <div style="margin-top:20px;">
          <el-button class="btnSearch" @click="implement">Next</el-button>
          <!-- <el-button class="btnSearch" @click="implement">Run QC fliter</el-button>
          <el-button @click="jumpResultPage">Result</el-button> -->
        </div>
      </div>
      <!-- QC Filter Result -->
      <SampleQCResult :parent-msg="resultData" v-if="isShowResult"></SampleQCResult>
      <progressBar :progressVisible="progressVisible" :percentage="percentage" @dialogClose="dialogClose"></progressBar>
    </div>
  </div>
</template>

<script>
import axios from '@/api/analysisHttp.js';
import Axios from 'axios'
import { analysis_new_job, specie_down_box, sqmpleQcDataShow, sample_qc_upload_show, qc_filter_data_show, sample_qc, qc_filter_data_result, specie_tissue_down_box, upload_file_delete, analysis_step_progress, from_sample_qc_one_step, analysisCellrangerList } from '@/api/analysis'
import SampleQCResult from '@/components/page/dataAnalysis/SampleQCResult/index'
import progressBar from '@/components/page/dataAnalysis/progressBar/index'

export default {
  name: 'SampleSampleQC',
  components: {
    SampleQCResult,
    progressBar
  },
  data() {
    return {
      data1_List: [1],
      stepActive: 0,
      stepList: [
        { name: 'Sample QC', link: 'SampleSampleQC', step: 'sample_qc' },
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
      formTopRules: {
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
      rules: {
        filtered_feature_bc_matrix: [{ required: true, message: 'Please select', trigger: 'change' }],
        barcodes: [{ required: true, message: 'Please select', trigger: 'change' }],
        features: [{ required: true, message: 'Please select', trigger: 'change' }],
        matrix: [{ required: true, message: 'Please select', trigger: 'change' }],
        data1_sample_name: [
          { required: true, message: 'Please enter', trigger: ["blur", "change"] },
        ],
        data2_sample_name: [
          { required: true, message: 'Please enter', trigger: ["blur", "change"] },
        ],
      },
      speciesList: [],
      TranscriptomeList: [],
      isShowResult: false,
      isNewJob: true,
      opacity: 0.4,
      isShowQC: true,
      upload_id: '',
      tissue: 'Root',
      formFile1: {
        data1_sample_name: '',
        type: 'gz',
        filtered_feature_bc_matrix: '',
        barcodes: '',
        features: '',
        matrix: ''
      },
      formFile2: {
        data2_sample_name: '',
        type: 'gz',
        filtered_feature_bc_matrix: '',
        barcodes: '',
        features: '',
        matrix: ''
      },
      file: '',
      file1: '',
      file2: '',
      file3: '',
      formBottom: {
        pt: '',
        mt: '',
      },
      formBottomRules: {
        // pt: [
        //   { required: true, message: 'Please enter', trigger: 'blur' },
        // ],
        // mt: [
        //   { required: true, message: 'Please enter', trigger: 'blur' },
        // ],
      },
      // Sample QC Result
      data1: {
        min_nCount_RNA: '',
        min_nFeature_RNA: '',
        min_percent_mt: '',
        min_percent_pt: '',
        max_nCount_RNA: '',
        max_nFeature_RNA: '',
        max_percent_mt: '',
        max_percent_pt: ''
      },
      data2: {
        min_nCount_RNA: '',
        min_nFeature_RNA: '',
        min_percent_mt: '',
        min_percent_pt: '',
        max_nCount_RNA: '',
        max_nFeature_RNA: '',
        max_percent_mt: '',
        max_percent_pt: ''
      },
      form: {
        min_nCount_RNA: '',
        max_nCount_RNA: '',
        min_nFeature_RNA: '',
        max_nFeature_RNA: '',
        min_percent_mt: '',
        max_percent_mt: '',
        min_percent_pt: '',
        max_percent_pt: ''
      },
      resultData: {},
      fileLoading: false,
      runLoading: false,
      oneLoading: false,
      runResultLoading: false,
      pageLoading: false,
      progressVisible: false,
      timer: '',
      percentage: 1,
      nextAble: true,
      oneAble: true
    }
  },
  mounted() {
    if (this.$route.query.uuid && this.$route.query.enterResults == 'true') {
      this.upload_id = this.$route.query.uuid
      this.isNewJob = true
      this.opacity = 1
      this.sample_qc_upload_show()
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
      this.species = this.$route.query.species_name
      this.transcriptome = this.$route.query.transcriptome
      if (this.$route.query.species_name == 'Arabidopsis_thaliana') {
        this.formBottom.mt = 'ATMG'
        this.formBottom.pt = 'ATCG'
      }
      // 给容器绑定相关的拖拽事件
      this.bindEvents()
      this.bindEvents2()
    } else {
      console.log(3333)
      this.getSpecie_down_box()
      this.isNewJob = true
      this.opacity = 0.4
      // 给容器绑定相关的拖拽事件
      this.bindEvents()
      this.bindEvents2()
    }
    // if (this.$route.query.step == 'data_process' && this.$route.query.enterResults) {
    //   this.pageLoading = true
    //   this.jumpResultPage()
    // }
    if (this.$route.query.step == 'sample_qc' || this.$route.query.step == 'data_process' || this.$route.query.step == 'cluster' || this.$route.query.step == 'cell_annotation') {
      if (this.$route.query.is_run_qc == 1) {
        let param = {
          uuid: this.upload_id,
          mt: this.formBottom.mt,
          pt: this.formBottom.pt,
        }
        this.runResultLoading = true
        param = {
          uuid: this.upload_id
        }
        sqmpleQcDataShow(param).then((res) => {
          if (res.code == 200) {
            if (res.data.length > 0) {
              this.runLoading = false
              this.runResultLoading = false
              this.isShowQC = false
              this.data1 = {
                min_nCount_RNA: res.data[0].data1.min_total_counts,
                min_nFeature_RNA: res.data[0].data1.min_n_genes_by_counts,
                min_percent_mt: res.data[0].data1.min_pct_counts_mt,
                min_percent_pt: res.data[0].data1.min_pct_counts_pt,
                max_nCount_RNA: res.data[0].data1.max_total_counts,
                max_nFeature_RNA: res.data[0].data1.max_n_genes_by_counts,
                max_percent_mt: res.data[0].data1.max_pct_counts_mt,
                max_percent_pt: res.data[0].data1.max_pct_counts_pt
              }
              this.data2 = {
                min_nCount_RNA: res.data[1].data2.min_total_counts,
                min_nFeature_RNA: res.data[1].data2.min_n_genes_by_counts,
                min_percent_mt: res.data[1].data2.min_pct_counts_mt,
                min_percent_pt: res.data[1].data2.min_pct_counts_pt,
                max_nCount_RNA: res.data[1].data2.max_total_counts,
                max_nFeature_RNA: res.data[1].data2.max_n_genes_by_counts,
                max_percent_mt: res.data[1].data2.max_pct_counts_mt,
                max_percent_pt: res.data[1].data2.max_pct_counts_pt
              }
              qc_filter_data_show({
                uuid: this.upload_id
              }).then((resFilter) => {
                if (res.code == 200) {
                  this.form = {
                    min_nCount_RNA: resFilter.data.results[0].min_total_counts,
                    min_nFeature_RNA: resFilter.data.results[0].min_n_genes_by_counts,
                    min_percent_mt: resFilter.data.results[0].min_pct_counts_mt || res.data[1].data2.min_pct_counts_mt,
                    min_percent_pt: resFilter.data.results[0].min_pct_counts_pt || res.data[1].data2.min_pct_counts_pt,
                    max_nCount_RNA: resFilter.data.results[0].max_total_counts,
                    max_nFeature_RNA: resFilter.data.results[0].max_n_genes_by_counts,
                    max_percent_mt: resFilter.data.results[0].max_pct_counts_mt || res.data[1].data2.max_pct_counts_mt,
                    max_percent_pt: resFilter.data.results[0].max_pct_counts_pt || res.data[1].data2.max_pct_counts_pt
                  }
                }
              })
            } else {
              this.runResultLoading = false
              this.$message('Run QC has not been executed yet. Please execute it first!')
            }

          }
        })
      } else {
        this.pageLoading = true
        this.jumpResultPage()
      }
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
          e.preventDefault()
          item.style.borderColor = '#b6b6b6'
          item.style.opacity = 1
          const fileList = e.dataTransfer.files
          this.uploadFile1(e, item.getAttribute('name'))
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
          e.preventDefault()
          item.style.borderColor = '#b6b6b6'
          item.style.opacity = 1
          const fileList = e.dataTransfer.files
          this.uploadFile2(e, item.getAttribute('name'))
        })
      });

    },
    uploadFile1(event, file_name) {
      if (this.formFile1.data1_sample_name == '') {
        this.$message('Please Choose sample name!')
        event.dataTransfer.value = ""
        return
      }
      if (file_name == 'filtered_feature_bc_matrix') {
        if (event.dataTransfer.files[0].name.split('.')[event.dataTransfer.files[0].name.split('.').length - 1] != 'h5') {
          this.$message.warning('Please upload .h5 file！');
        } else {
          this.formFile1[file_name] = event.dataTransfer.files[0].name
          this.fileLoading = true
          this.openFile(event.dataTransfer.files[0], 'data1', file_name + '.h5')
          event.dataTransfer.value = ''
        }
      } else {
        if (event.dataTransfer.files[0].name.split('.')[event.dataTransfer.files[0].name.split('.').length - 1] != 'gz') {
          this.$message.warning('Please upload .gz file！');
        } else {
          this.formFile1[file_name] = event.dataTransfer.files[0].name
          this.fileLoading = true
          if (file_name == 'matrix') {
            this.openFile(event.dataTransfer.files[0], 'data1', file_name + '.mtx.gz')
          } else {
            this.openFile(event.dataTransfer.files[0], 'data1', file_name + '.tsv.gz')
          }
          event.dataTransfer.value = ''
        }
      }
    },
    uploadFile2(event, file_name) {
      if (this.formFile2.data2_sample_name == '') {
        this.$message('Please Choose sample name!')
        event.dataTransfer.value = ""
        return
      }
      if (file_name == 'filtered_feature_bc_matrix') {
        if (event.dataTransfer.files[0].name.split('.')[event.dataTransfer.files[0].name.split('.').length - 1] != 'h5') {
          this.$message.warning('Please upload .h5 file！');
        } else {
          this.formFile2[file_name] = event.dataTransfer.files[0].name
          this.fileLoading = true
          this.openFile(event.dataTransfer.files[0], 'data2', file_name + '.h5')
          event.dataTransfer.value = ''
        }
      } else {
        if (event.dataTransfer.files[0].name.split('.')[event.dataTransfer.files[0].name.split('.').length - 1] != 'gz') {
          this.$message.warning('Please upload .gz file！');
        } else {
          this.formFile2[file_name] = event.dataTransfer.files[0].name
          this.fileLoading = true
          if (file_name == 'matrix') {
            this.openFile(event.dataTransfer.files[0], 'data2', file_name + '.mtx.gz')
          } else {
            this.openFile(event.dataTransfer.files[0], 'data2', file_name + '.tsv.gz')
          }
          event.dataTransfer.value = ''
        }
      }
    },
    radioChange1() {
      setTimeout(() => {
        this.bindEvents()
      }, 300)
    },
    radioChange2() {
      setTimeout(() => {
        this.bindEvents2()
      }, 300)
    },
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
            is_run_qc: this.$route.query.is_run_qc,
          }
        })
        this.isShowResult = false
        this.isShowQC = true
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
    sample_qc_upload_show() {
      sample_qc_upload_show({ uuid: this.upload_id }).then((res) => {
        if (res.code == 200) {
          this.formFile1.data1_sample_name = res.data.results[0].data1_sample_name
          this.formFile2.data2_sample_name = res.data.results[0].data2_sample_name
          this.formFile1.type = res.data.results[0].data1_type
          this.formFile2.type = res.data.results[0].data2_type
          this.formBottom.mt = res.data.results[0].mt
          this.formBottom.pt = res.data.results[0].pt
          res.data.results[0].file_name && res.data.results[0].file_name.forEach(item => {
            if (item.data_type == 'data1') {
              this.formFile1[item.file_name.split('.')[0]] = item.file_source_name
            } else {
              this.formFile2[item.file_name.split('.')[0]] = item.file_source_name
            }
          });
        }
      })
    },
    newJob() {
      this.$refs['formTop'].validate((valid) => {
        if (valid) {
          analysis_new_job(Object.assign({}, this.formTop, { source: 'sample_qc' })).then((res) => {
            if (res.code == 200) {
              this.upload_id = res.data
              this.isNewJob = false
              this.nextAble = false
              this.oneAble = false
              this.opacity = 1
              this.species = this.formTop.species_name
              this.transcriptome = this.formTop.transcriptome
              if (this.formTop.species_name == 'Arabidopsis_thaliana') {
                this.formBottom.mt = 'ATMG'
                this.formBottom.pt = 'ATCG'
              }
              this.$message.success('new Job successfully!')
            }
          })

        } else {
          return false;
        }
      });
    },
    handleUpdate1(event, file_name) {
      if (this.formFile1.data1_sample_name == '') {
        this.$message('Please Choose sample name!')
        event.target.value = ""
        return
      }
      if (file_name == 'filtered_feature_bc_matrix') {
        if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'h5') {
          this.$message.warning('Please upload .h5 file！');
        } else {
          this.formFile1[file_name] = event.target.files[0].name
          this.fileLoading = true
          this.openFile(event.target.files[0], 'data1', file_name + '.h5')
          event.target.value = ''
        }
      } else {
        if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'gz') {
          this.$message.warning('Please upload .gz file！');
        } else {
          this.formFile1[file_name] = event.target.files[0].name
          this.fileLoading = true
          if (file_name == 'matrix') {
            this.openFile(event.target.files[0], 'data1', file_name + '.mtx.gz')
          } else {
            this.openFile(event.target.files[0], 'data1', file_name + '.tsv.gz')
          }
          event.target.value = ''
        }
      }
    },
    handleUpdate2(event, file_name) {
      if (this.formFile2.data2_sample_name == '') {
        this.$message('Please Choose sample name!')
        event.target.value = ""
        return
      }
      if (file_name == 'filtered_feature_bc_matrix') {
        if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'h5') {
          this.$message.warning('Please upload .h5 file！');
        } else {
          this.formFile2[file_name] = event.target.files[0].name
          this.fileLoading = true
          this.openFile(event.target.files[0], 'data2', file_name + '.h5')
          event.target.value = ''
        }
      } else {
        if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'gz') {
          this.$message.warning('Please upload .gz file！');
        } else {
          this.formFile2[file_name] = event.target.files[0].name
          this.fileLoading = true
          if (file_name == 'matrix') {
            this.openFile(event.target.files[0], 'data2', file_name + '.mtx.gz')
          } else {
            this.openFile(event.target.files[0], 'data2', file_name + '.tsv.gz')
          }
          event.target.value = ''
        }
      }
    },
    openFile(file, data_type, file_name) {
      let formData = new FormData()
      formData.append('file', file)
      formData.append('upload_id', this.upload_id)
      formData.append('data_type', data_type)
      formData.append('file_name', file_name)
      if (data_type == 'data1') {
        formData.append('data1_sample_name', this.formFile1.data1_sample_name)
      } else {
        formData.append('data2_sample_name', this.formFile2.data2_sample_name)
      }
      // formData.append('analysis_name', data_type == 'data1' ? this.formFile1.analysis_name : this.formFile2.analysis_name)
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      const $axios = Axios.create({
        baseURL: axios.defaults.baseURL,
        timeout: 1000000
      });

      $axios.post('/v1/sample_qc_upload/', formData, config).then(res => {
        if (res.data.code == 200) {
          this.$message.success('Upload successful!')
        } else {
          this.$message.warning('Upload failed!')
        }
        this.fileLoading = false
      }).catch(err => {
        this.$message.warning('Upload failed!')
      });
    },
    async runQC(type) {
      this.oneAble = true
      try {
        await this.$refs.formFile1.validate()
        await this.$refs.formFile2.validate()
        await this.$refs.formBottom.validate()
        //都校验成功之后，这里可以发请求
        let param = {
          uuid: this.upload_id,
          mt: this.formBottom.mt,
          pt: this.formBottom.pt,
        }
        if (type == 'qcResult') {
          this.runResultLoading = true
          param = {
            uuid: this.upload_id
          }
        } else {
          this.runLoading = true
          param = {
            uuid: this.upload_id,
            mt: this.formBottom.mt,
            pt: this.formBottom.pt,
            tag: 'run'
          }
        }
        sqmpleQcDataShow(param).then((res) => {
          if (res.code == 200) {
            if (res.data.length > 0) {
              this.runLoading = false
              this.runResultLoading = false
              this.isShowQC = false
              this.data1 = {
                min_nCount_RNA: res.data[0].data1.min_total_counts,
                min_nFeature_RNA: res.data[0].data1.min_n_genes_by_counts,
                min_percent_mt: res.data[0].data1.min_pct_counts_mt,
                min_percent_pt: res.data[0].data1.min_pct_counts_pt,
                max_nCount_RNA: res.data[0].data1.max_total_counts,
                max_nFeature_RNA: res.data[0].data1.max_n_genes_by_counts,
                max_percent_mt: res.data[0].data1.max_pct_counts_mt,
                max_percent_pt: res.data[0].data1.max_pct_counts_pt
              }
              this.data2 = {
                min_nCount_RNA: res.data[1].data2.min_total_counts,
                min_nFeature_RNA: res.data[1].data2.min_n_genes_by_counts,
                min_percent_mt: res.data[1].data2.min_pct_counts_mt,
                min_percent_pt: res.data[1].data2.min_pct_counts_pt,
                max_nCount_RNA: res.data[1].data2.max_total_counts,
                max_nFeature_RNA: res.data[1].data2.max_n_genes_by_counts,
                max_percent_mt: res.data[1].data2.max_pct_counts_mt,
                max_percent_pt: res.data[1].data2.max_pct_counts_pt
              }
              this.oneAble = false
              qc_filter_data_show({
                uuid: this.upload_id
              }).then((resFilter) => {
                if (res.code == 200) {
                  this.form = {
                    min_nCount_RNA: resFilter.data.results[0].min_total_counts,
                    min_nFeature_RNA: resFilter.data.results[0].min_n_genes_by_counts,
                    min_percent_mt: resFilter.data.results[0].min_pct_counts_mt || res.data[1].data2.min_pct_counts_mt,
                    min_percent_pt: resFilter.data.results[0].min_pct_counts_pt || res.data[1].data2.min_pct_counts_pt,
                    max_nCount_RNA: resFilter.data.results[0].max_total_counts,
                    max_nFeature_RNA: resFilter.data.results[0].max_n_genes_by_counts,
                    max_percent_mt: resFilter.data.results[0].max_pct_counts_mt || res.data[1].data2.max_pct_counts_mt,
                    max_percent_pt: resFilter.data.results[0].max_pct_counts_pt || res.data[1].data2.max_pct_counts_pt
                  }
                }
                this.oneAble = false
              })
            } else {
              this.oneAble = false
              this.runResultLoading = false
              this.$message('Run QC has not been executed yet. Please execute it first!')
            }

          }
        })
      } catch (error) {
        this.oneAble = false
        console.error('表单校验失败', error)
      }
    },
    dialogClose() {
      this.progressVisible = false
      clearInterval(this.timer);
    },
    valChange() {
      analysis_step_progress({
        uuid: this.$route.query.uuid,
        current_step: this.$route.query.step || ''
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
    implement() {
      this.percentage = 1
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
          this.$route.query.step = 'sample_qc'
          this.stepActive = 1
          let param = {
            uuid: this.upload_id,
            max_n_genes_by_counts: this.form.max_nFeature_RNA,
            max_total_counts: this.form.max_nCount_RNA,
            min_n_genes_by_counts: this.form.min_nFeature_RNA,
            min_total_counts: this.form.min_nCount_RNA,
          }
          if (this.formBottom.pt) {
            param.min_pct_counts_pt = this.form.min_percent_pt
            param.max_pct_counts_pt = this.form.max_percent_pt
          }
          if (this.formBottom.mt) {
            param.min_pct_counts_mt = this.form.min_percent_mt
            param.max_pct_counts_mt = this.form.max_percent_mt
          }
          sample_qc(param).then((res) => {
            if (res.code == 200) {
              // this.$message(res.data.status)
              this.loading = false
              this.progressVisible = true
              this.timer = setInterval(this.valChange, 3000);
              // this.$router.push({
              //   path: '/analysisFromSampleQC',
              //   query: {}
              // })
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
        let param = {
          uuid: this.upload_id,
          max_n_genes_by_counts: this.form.max_nFeature_RNA,
          max_total_counts: this.form.max_nCount_RNA,
          min_n_genes_by_counts: this.form.min_nFeature_RNA,
          min_total_counts: this.form.min_nCount_RNA,
        }
        if (this.formBottom.pt) {
          param.min_pct_counts_pt = this.form.min_percent_pt
          param.max_pct_counts_pt = this.form.max_percent_pt
        }
        if (this.formBottom.mt) {
          param.min_pct_counts_mt = this.form.min_percent_mt
          param.max_pct_counts_mt = this.form.max_percent_mt
        }
        sample_qc(param).then((res) => {
          if (res.code == 200) {
            // this.$message(res.data.status)
            this.loading = false
            this.progressVisible = true
            this.timer = setInterval(this.valChange, 3000);
            // this.$router.push({
            //   path: '/analysisFromSampleQC',
            //   query: {}
            // })
          } else {
            this.$message('Your task failed, please try again。')
            this.progressVisible = false
            this.loading = false
            clearInterval(this.timer);
          }
        })
      }

    },
    jumpResultPage() {
      qc_filter_data_result({
        uuid: this.$route.query.uuid || this.upload_id,
        data_type: 'data1',
      }).then((res) => {
        if (res.code == 200) {
          if (res.data.results && res.data.results.length > 0) {
            this.resultData.data1 = res.data.results[0].result_data
            qc_filter_data_result({
              uuid: this.$route.query.uuid || this.upload_id,
              data_type: 'data2',
            }).then((res) => {
              if (res.code == 200) {
                if (this.executeaAgain) {
                  this.$route.query.step = 'data_process'
                }
                this.resultData.data2 = res.data.results[0].result_data
                this.resultData.formTop = this.formBottom
                this.resultData.uuid = this.$route.query.uuid || this.upload_id
                this.resultData.source = 'sample_qc'
                this.isShowResult = true
                this.pageLoading = false
                this.isShowQC = false
              }
            })
          } else {
            // this.$message('Executing, please try again later!')
            this.pageLoading = false
          }
        }
      })
    },
    deleteFile(data_type, file_name, type) {
      upload_file_delete({
        upload_id: this.upload_id,
        data_type: data_type,
        file_name: file_name,
      }).then((res) => {
        if (res.code == 200) {
          if (data_type == 'data1') {
            this.formFile1[type] = ''
          } else {
            this.formFile2[type] = ''
          }
          this.$message.success('File deleted successfully')
        }
      })
    },
    oneStep() {
      this.oneLoading = true
      this.nextAble = true
      from_sample_qc_one_step({
        uuid: this.$route.query.uuid || this.upload_id,
        mt: this.formBottom.mt,
        pt: this.formBottom.pt,
        tag: 'run'
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
          clearInterval(this.timer);
          this.nextAble = false
        }
        this.oneLoading = false
      })
    },
    oneChange() {
      analysis_step_progress({
        uuid: this.$route.query.uuid || this.upload_id,
        source: 'sample_qc'
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
              source: 'sample_qc',
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
                    from: 'sample_qc',
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
      this.pageLoading = true
      // this.upload_id = "0b473372-5bd7-4b37-9ed6-5d2211db7da7" //   测试
      this.upload_id = "7ac1f661-26cf-47ad-acf8-532945153a2a"   //  正式
      this.jumpResultPage()
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
