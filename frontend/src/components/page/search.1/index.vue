<template>
  <div class="search">
    <div class="search-inner">
      <div class="blast" v-loading="loading" element-loading-text="running">
        <p class="keyword_p1">Sample</p>
        <el-form ref="form4" :inline="true" :model="sample_form">
          <el-form-item label="Species Name" prop="species_name">
            <el-select style="width:200px;" size="large" @change="species_nameChange('sample_form')" v-model="sample_form.species_name"
              placeholder="Choose">
              <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Tissue" prop="tissue">
            <el-select clearable style="width:200px;" @change="tissueChange('sample_form')" size="large" v-model="sample_form.tissue"
              placeholder="Choose">
              <el-option v-for="(item, index) in sample_form_option.tissueOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Project ID" prop="project_id">
            <el-select clearable style="width:200px;" @change="project_idChange" size="large" v-model="sample_form.project_id" placeholder="Choose">
              <el-option v-for="item in sample_form_option.project_idOptions" :key="item.label" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Sample ID">
            <el-select clearable style="width:200px;" size="large" v-model="sample_form.sample_id" placeholder="Choose">
              <el-option v-for="(item, index) in sample_form_option.sample_idOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <el-row style="margin: 20px 0px 40px 0;">
          <el-button class="btnSearch" @click="example('sample_form')">Example</el-button>
          <el-button class="btnSearch" @click="search('sample_form')">Search</el-button>
          <el-button class="btnReset" @click="reset('sample_form')">Reset</el-button>
        </el-row>
      </div>
      <div class="cmpredictor">
        <p class="keyword_p1">Cluster Marker</p>
        <el-form ref="form5" :inline="true" :model="clusterMarker_form">
          <el-form-item label="Species Name" prop="species_name">
            <el-select style="width:195px;" size="large" @change="species_nameChange('clusterMarker_form')" v-model="clusterMarker_form.species_name"
              placeholder="Choose">
              <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Tissue ID" prop="tissue">
            <el-select clearable style="width:195px;" @change="tissueChange('clusterMarker_form')" size="large" v-model="clusterMarker_form.tissue"
              placeholder="Choose">
              <el-option v-for="(item, index) in clusterMarker_form_option.tissueOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Cluster Name" prop="cluster_name">
            <el-select clearable size="large" style="width:195px;" v-model="clusterMarker_form.cluster_name" @change="cluster_nameChange"
              placeholder="Choose">
              <el-option v-for="(item, index) in clusterMarker_form_option.cluster_nameOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Cluster Marker" prop="cluster_marker">
            <el-select clearable size="large" style="width:195px;" v-model="clusterMarker_form.cluster_marker" placeholder="Choose">
              <el-option v-for="(item, index) in clusterMarker_form_option.cluster_markerOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <el-row style="margin: 0 0px 40px 0;">
          <el-button class="btnSearch" @click="example('clusterMarker_form')">Example</el-button>
          <el-button class="btnSearch" style="width:126px;" @click="search('clusterMarker_form')" :loading="loading">Search</el-button>
          <el-button class="btnReset" @click="reset('clusterMarker_form')">Reset</el-button>
        </el-row>
        <!-- <cmpredictor></cmpredictor> -->
      </div>
      <div class="cellMarker">
        <p class="keyword_p1">Cell Marker</p>
        <el-form ref="form2" :inline="true" :model="cellMarker_form">
          <el-form-item label="Species Name" prop="species_name">
            <el-select style="width:200px;" size="large" @change="species_nameChange('cellMarker_form')" v-model="cellMarker_form.species_name"
              placeholder="Choose">
              <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Tissue ID" prop="tissue">
            <el-select clearable style="width:200px;" @change="tissueChange('cellMarker_form')" size="large" v-model="cellMarker_form.tissue"
              placeholder="Choose">
              <el-option v-for="(item, index) in cellMarker_form_option.tissueOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Cell ID">
            <el-select clearable style="width:200px;" size="large" v-model="cellMarker_form.cell_id" @change="cell_idChange" placeholder="Choose">
              <el-option v-for="(item, index) in cellMarker_form_option.cell_idOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Gene Symbol">
            <el-select clearable style="width:200px;" size="large" v-model="cellMarker_form.gene_symbol" placeholder="Choose">
              <el-option v-for="(item, index) in cellMarker_form_option.gene_symbolOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <el-row style="margin: 20px 0px 40px 0;">
          <el-button class="btnSearch" @click="example('cellMarker_form')">Example</el-button>
          <el-button class="btnSearch" @click="search('cellMarker_form')">Search</el-button>
          <el-button class="btnReset" @click="reset('cellMarker_form')">Reset</el-button>
        </el-row>
      </div>

    </div>
  </div>
</template>

<script>
import axios from '@/api/http.js';
import Axios from 'axios'
import { cell_search_down, cell_type_down } from "@/api/search";
import { plant_search_down, tissue_type_down, project_id_down, sample_id_down, cluster_name_down, cluster_marker_down, cell_id_down, gene_symbol_down } from "@/api/api";
import cmpredictor from "../CMPredictor/index"
export default {
  name: "search",
  // components: {
  //   "cmpredictor": cmpredictor
  // },
  data() {
    return {
      sample_form: {
        species_name: "",
        tissue: "",
        project_id: "",
        sample_id: "",
      },
      speciesOptions: [],
      sample_form_option: {
        tissueOptions: [],
        project_idOptions: [],
        sample_idOptions: [],
      },

      clusterMarker_form: {
        species_name: "",
        tissue: "",
        cluster_name: "",
        cluster_marker: "",
      },
      clusterMarker_form_option: {
        tissueOptions: [],
        cluster_nameOptions: [],
        cluster_markerOptions: [],
      },

      cellMarker_form: {
        species_name: "",
        tissue: "",
        cell_id: "",
        gene_symbol: "",
      },
      cellMarker_form_option: {
        tissueOptions: [],
        cell_idOptions: [],
        gene_symbolOptions: [],
      },

      loading: false,

    };
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      plant_search_down({}).then(res => {
        if (res.code == 200) {
          this.speciesOptions = res.data
        }
      });
    },
    species_nameChange(formType) {
      if (formType == 'sample_form') {
        tissue_type_down({ species_name: this.sample_form.species_name }).then(res => {
          if (res.code == 200) {
            this.sample_form.tissue = ''
            this.sample_form.project_id = ''
            this.sample_form.sample_id = ''
            this.sample_form_option.project_idOptions = []
            this.sample_form_option.sample_idOptions = []
            this.sample_form_option.tissueOptions = res.data
          }
        });
      } else if (formType == 'clusterMarker_form') {
        tissue_type_down({ species_name: this.clusterMarker_form.species_name }).then(res => {
          if (res.code == 200) {
            this.clusterMarker_form.tissue = ''
            this.clusterMarker_form.cluster_name = ''
            this.clusterMarker_form.cluster_marker = ''
            this.clusterMarker_form_option.cluster_nameOptions = []
            this.clusterMarker_form_option.cluster_markerOptions = []
            this.clusterMarker_form_option.tissueOptions = res.data
          }
        });
      } else if (formType == 'cellMarker_form') {
        tissue_type_down({ species_name: this.cellMarker_form.species_name }).then(res => {
          if (res.code == 200) {
            this.cellMarker_form.tissue = ''
            this.cellMarker_form.cell_id = ''
            this.cellMarker_form.gene_symbol = ''
            this.cellMarker_form_option.cell_idOptions = []
            this.cellMarker_form_option.gene_symbolOptions = []
            this.cellMarker_form_option.tissueOptions = res.data
          }
        });
      }

    },
    tissueChange(formType) {
      if (formType == 'sample_form') {
        project_id_down({ species_name: this.sample_form.species_name, tissue: this.sample_form.tissue }).then(res => {
          if (res.code == 200) {
            this.sample_form.project_id = ''
            this.sample_form.sample_id = ''
            this.sample_form_option.sample_idOptions = []
            this.sample_form_option.project_idOptions = res.data
          }
        });
      } else if (formType == 'clusterMarker_form') {
        cluster_name_down({ species_name: this.clusterMarker_form.species_name, tissue: this.clusterMarker_form.tissue }).then(res => {
          if (res.code == 200) {
            this.clusterMarker_form.cluster_name = ''
            this.clusterMarker_form.cluster_marker = ''
            this.clusterMarker_form_option.cluster_markerOptions = []
            this.clusterMarker_form_option.cluster_nameOptions = res.data
          }
        });
      } else if (formType == 'cellMarker_form') {
        cell_id_down({ species_name: this.cellMarker_form.species_name, tissue: this.cellMarker_form.tissue }).then(res => {
          if (res.code == 200) {
            this.cellMarker_form.cell_id = ''
            this.cellMarker_form.gene_symbol = ''
            this.cellMarker_form_option.gene_symbolOptions = []
            this.cellMarker_form_option.cell_idOptions = res.data
          }
        });
      }
    },
    project_idChange(val) {
      sample_id_down({
        species_name: this.sample_form.species_name,
        tissue: this.sample_form.tissue,
        project_id: val,
      }).then(res => {
        if (res.code == 200) {
          this.sample_form.sample_id = ''
          this.sample_form_option.sample_idOptions = res.data
        }
      });
    },
    cluster_nameChange(val) {
      cluster_marker_down({
        species_name: this.clusterMarker_form.species_name,
        tissue: this.clusterMarker_form.tissue,
        cluster_name: val,
      }).then(res => {
        if (res.code == 200) {
          this.clusterMarker_form.cluster_marker = ''
          this.clusterMarker_form_option.cluster_markerOptions = res.data
        }
      });
    },
    cell_idChange(val) {
      gene_symbol_down({
        species_name: this.cellMarker_form.species_name,
        tissue: this.cellMarker_form.tissue,
        cell_id: val,
      }).then(res => {
        if (res.code == 200) {
          this.cellMarker_form.gene_symbol = ''
          this.cellMarker_form_option.gene_symbolOptions = res.data
        }
      });
    },
    example(param) {
      if (param == "sample_form") {
        this.sample_form = {
          species_name: "Arabidopsis_Thaliana",
          tissue: "Root",
          project_id: "",
          sample_id: "",
        };
      } else if (param == "cellMarker_form") {
        this.cellMarker_form = {
          species_name: "Arabidopsis_Thaliana",
          tissue: "Root",
          cell_id: "",
          gene_symbol: "",
        };
      } else if (param == "clusterMarker_form") {
        this.clusterMarker_form = {
          species_name: "Arabidopsis_Thaliana",
          tissue: "Root",
          cluster_name: "",
          cluster_marker: "",
        };
      }
    },
    search(param) {
      if (param == "sample_form") {
        this.$router.push({
          path: '/searchList',
          query: {
            ...this.sample_form,
            ...{
              type: "sample_form"
            }
          }
        })
      } else if (param == "cellMarker_form") {
        this.$router.push({
          path: '/searchList',
          query: {
            ...this.cellMarker_form,
            ...{
              type: "cellMarker_form"
            }
          }
        })
      } else if (param == "clusterMarker_form") {
        this.$router.push({
          path: '/searchList',
          query: {
            ...this.clusterMarker_form,
            ...{
              type: "clusterMarker_form"
            }
          }
        })

      }
    },
    reset(param) {
      if (param == "sample_form") {
        this.sample_form = {
          species_name: "",
          tissue: "",
          project_id: "",
          sample_id: "",
        };
      } else if (param == "cellMarker_form") {
        this.cellMarker_form = {
          species_name: "",
          tissue: "",
          cell_id: "",
          gene_symbol: "",
        };
      } else if (param == "clusterMarker_form") {
        this.clusterMarker_form = {
          species_name: "",
          tissue: "",
          cluster_name: "",
          cluster_marker: "",
        };
      }
    },
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
