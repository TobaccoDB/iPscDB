<template>
  <div class="search">
    <div class="search-inner">
      <div class="blast" v-loading="loading" element-loading-text="running">
        <p class="keyword_p1">Blast</p>
        <el-form ref="form4" :inline="true" :model="blast_form">
          <el-form-item style="width:100%;" class="firstItem">
            <el-input type="textarea" :autosize="{ minRows: 4, maxRows: 6}" placeholder="Input a FASTA sequence here" v-model="blast_form.query_sequence"
              style="width:100%;">
            </el-input>
          </el-form-item>
          <el-form-item label="Program" prop="search_method">
            <el-select clearable style="width:200px;" @change="search_methodChange" size="large" v-model="blast_form.search_method" placeholder="Choose">
              <el-option v-for="(item, index) in methodOptions" :key="index" :label="item" :value="item">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Species" prop="species">
            <el-select style="width:200px;" size="large" v-model="blast_form.species" placeholder="Choose">
              <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Database" prop="database">
            <el-select clearable style="width:200px;" size="large" v-model="blast_form.database" placeholder="Choose">
              <el-option v-for="item in DatabaseOptions" :key="item.label" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="E-value">
            <el-select clearable style="width:200px;" size="large" v-model="blast_form.evalue" placeholder="Choose">
              <el-option v-for="(item, index) in valueOptions" :key="index" :label="item" :value="item">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <p class="file_p">
          or upload sequence FASTA file
          <a href="javascript:;" class="file">Browse
            <input type="file" name="file" ref="file" @change="handleUpdate($event)" />
          </a>
          <span>{{fileName}}</span>
        </p>
        <el-row style="margin: 20px 0px 40px 0;">
          <el-button class="btnSearch" @click="example('blast_form')">Example</el-button>
          <el-button class="btnSearch" @click="search('blast_form')">Search</el-button>
          <el-button class="btnReset" @click="reset('blast_form')">Reset</el-button>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/api/http.js';
import Axios from 'axios'
import { plant_search_down } from "@/api/api";
export default {
  name: "blast",
  components: {
  },
  data() {
    return {
      speciesOptions: [],
      blast_form: {
        search_method: "",
        query_sequence: "",
        database: "",
        species: "",
        evalue: "",
      },
      rules: {
        search_method: [
          { required: true, message: 'Please select', trigger: 'change' }
        ],
        query_sequence: [
          { required: true, message: 'Please enter', trigger: 'blur' }
        ],
        database: [
          { required: true, message: 'Please select', trigger: 'change' }
        ],
        species: [
          { required: true, message: 'Please select', trigger: 'change' }
        ]
      },
      methodOptions: ['blastp', 'blastx', 'blastn', 'tblastn'],
      // methodOptions: ['blastp', 'blastx', 'blastn', 'tblastn', 'tblastx'],
      DatabaseOptions: [
        // {
        //   label: 'lncRNA Sequences',
        //   value: 'lncRNA'
        // },
        {
          label: 'CDS Sequences',
          value: 'cds'
        },
        // {
        //   label: 'Genome Sequences',
        //   value: 'chromosome'
        // },
        {
          label: 'Peptide Sequences',
          value: 'pep'
        },
        // {
        //   label: 'Gene Sequences',
        //   value: 'gene'
        // }
      ],
      valueOptions: ['1e-20', '1e-10', '1e-5', '0.01', '0.1', '1', '10', '100'],
      file: "",
      fileName: '',
      loading: false
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
    example(param) {
      if (param == "blast_form") {
        this.blast_form = {
          search_method: "blastn",
          query_sequence: ">Test_seq\nATGCAGATCTTTGTTAAGACTCTCACCGGAAAGACTATCACCCTCGAGGTGGAAAGCTCTGACACCATCGACAACGTTAA\nGGCCAAGATCCAGGATAAGGAAGGCATTCCTCCGGATCAGCAGAGGTTGATCTTCGCTGGAAAGCAGTTGGAGGATGGCA\nGAACTCTTGCTGACTACAACATCCAGAAGGAGTCCACACTTCATCTTGTTCTCAGGCTCCGTGGTGGTATGCAGATCTTT\nGTCAAGACGTTGACTGGAAAGACTATCACTTTGGAGGTGGAGAGCTCTGACACTATCGACAATGTCAAAGCCAAGATCCA\nGGACAAAGAGGGTATCCCACCGGACCAGCAGAGATTGATCTTCGCCGGAAAACAACTTGAAGATGGTAGAACTTTGGCTG\nACTACAACATTCAGAAGGAGTCTACACTTCACTTGGTGTTGCGTCTCCGTGGAGGTATGCAGATTTTCGTGAAGACTCTC\nACTGGAAAGACCATTACTCTTGAAGTTGAGAGCTCCGACACCATTGACAACGTGAAGGCTAAGATCCAGGACAAGGAAGG\nTATCCCTCCGGACCAGCAGCGTCTCATCTTCGCTGGAAAACAGCTTGAGGATGGTCGTACTTTGGCCGACTACAACATCC\nAGAAGGAGTCTACCCTTCACTTGGTGCTAAGGCTCCGTGGTGGTTTCTAA",
          database: "cds",
          species: "Arabidopsis_thaliana",
          evalue: "1e-5",
        };
      }
    },
    search(param) {
      if (param == "blast_form") {
        this.loading = true
        let formData = new FormData()
        formData.append('species', this.blast_form.species)
        formData.append('database', this.blast_form.database)
        formData.append('file', this.file)
        formData.append('query_sequence', this.blast_form.query_sequence)
        formData.append('search_method', this.blast_form.search_method)
        formData.append('evalue', this.blast_form.evalue)
        let config = {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
        sessionStorage.removeItem("tableParams3");
        const $axios = Axios.create({
          baseURL: axios.defaults.baseURL,
          timeout: 100000
        });

        $axios.post('api/v1/blast_data/', formData, config).then(res => {
          if (res.data.code == 200) {
            sessionStorage.setItem("tableParams3", JSON.stringify(res.data.data));
            this.loading = false
            this.$router.push("/searchList");
          } else {
            this.$message.warning(res.data.msg);
          }
        }).catch(err => {
          this.$message.warning(err.data.msg);
        });
      }
    },
    reset(param) {
      if (param == "blast_form") {
        this.fileName = ''
        this.file = ''
        this.blast_form = {
          search_method: "",
          query_sequence: "",
          database: "",
          species: "",
          evalue: "",
        };
      }
      this.$refs['form1'].resetFields()
    },
    handleUpdate(event) {
      if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'fa') {
        this.$message.warning('Please upload .fa file！');
      } else {
        this.fileName = event.target.files[0].name
        this.file = event.target.files[0]
        sessionStorage.setItem("files", JSON.stringify(event.target.files[0]));
      }
    },
    search_methodChange(val) {
      if (val == 'blastp' || val == 'blastx') {
        this.DatabaseOptions = [{
          label: 'Peptide Sequences',
          value: 'pep'
        }]
      } else {
        this.DatabaseOptions = [{
          label: 'CDS Sequences',
          value: 'cds'
        }]
      }
    }
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
