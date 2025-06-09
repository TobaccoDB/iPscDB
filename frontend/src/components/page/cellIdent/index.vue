<template>
  <div class="cellIdent">
    <div class="crumbs">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/cellIdentification' }">Cell Identification</el-breadcrumb-item>
        <el-breadcrumb-item>Cell ident</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="cellIdent-inner" :style="{minHeight: contentHeight}" v-loading="goLoading" element-loading-text="loading" element-loading-background="#fff">
      <el-container>
        <el-header>Cell type identificaiton</el-header>
        <el-container>
          <el-aside width="400px">
            <el-form ref="form1" :model="cellIdent_form" :inline="true">
              <el-form-item label="Input File" prop="file" style="margin-bottom:0;">
                <p class="file_p" v-loading="fileLoading">
                  <a href="javascript:;" class="file">Open File
                    <input type="file" name="file" ref="file" @change="handleUpdate($event)" />
                  </a>
                  <span>{{cellIdent_form.fileName}}</span>
                </p>
              </el-form-item>
              <el-form-item>
                <i class="el-icon-download pointer" @click="download">
                  <span>Download Example File</span>
                </i>
              </el-form-item>
              <el-form-item label="Prediction number" prop="num_top">
                <el-select style="width:200px;" size="large" v-model="cellIdent_form.num_top" placeholder="Choose">
                  <el-option v-for="(item, index) in 5" :key="index" :label="item" :value="item">
                  </el-option>
                </el-select>
              </el-form-item>
            </el-form>
            <el-row style="margin: 0px 0px 40px 0;">
              <el-button class="btnSearch" style="width:80px;" @click="search">GO</el-button>
              <el-button class="btnReset" @click="reset">Reset</el-button>
            </el-row>
          </el-aside>
          <el-main>
            <h3>Input file explain</h3>
            <p>*Raw counts DGE requirement: Gene (row) * Cell (column);</p>
            <p>Gene ID: gene symbol only;</p>
            <p>File size:
              <=200mb;</p>
                <p>File format: txt/csv (comma or tab separated);</p>
                <p>File name: no space or other special character.</p>
                <p>* Input file format as follows:</p>
                <ul>
                  <li v-for="(item, index) in itemList" :key="index">{{item}}</li>
                </ul>

                <p>* If you paste your data to Excel, please format the cell as text before pasting data on it. Otherwise, some
                  gene names will be converted to Date and will introduce redundant gene names.</p>
                <p>* If you use Seurat in R, you can run these scripts to generate input:</p>
                <div class="bottom_p">
                  <p>rna.data.average = AverageExpression(rna.data)</p>
                  <p># This will generate average expression for each cluster</p>
                  <p>write.table(rna.data.average, "Cell_ident_input.csv", quote = F, col.names = T, row.names = T, sep="\t")</p>
                  <p># Then, you can upload this file to predict cell types</p>
                </div>
                <h3>Reference genome information：</h3>
                <div class="ReferenceTable">
                  <el-row>
                    <el-col :span="6">
                      <div class="grid-Reference">Species</div>
                    </el-col>
                    <el-col :span="8">
                      <div class="grid-Reference">Refrence Genome</div>
                    </el-col>
                    <el-col :span="10">
                      <div class="grid-Reference">Download information</div>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">
                      <div class="grid-Reference">Arabidopsis thaliana</div>
                    </el-col>
                    <el-col :span="8">
                      <div class="grid-Reference">TAIR10</div>
                    </el-col>
                    <el-col :span="10">
                      <div class="grid-Reference">https://www.arabidopsis.org/</div>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">
                      <div class="grid-Reference" style="height:64px;line-height:64px;">Nicotiana attenuata</div>
                    </el-col>
                    <el-col :span="8">
                      <div class="grid-Reference" style="height:64px;line-height:64px;">NIATTr2</div>
                    </el-col>
                    <el-col :span="10">
                      <div class="grid-Reference" style="height:64px;">https://www.ncbi.nlm.nih.gov/assembly/GCF_001879085.1/</div>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">
                      <div class="grid-Reference" style="height:64px;line-height:64px;">Zea mays</div>
                    </el-col>
                    <el-col :span="8">
                      <div class="grid-Reference" style="height:64px;line-height:64px;">B73</div>
                    </el-col>
                    <el-col :span="10">
                      <div class="grid-Reference" style="height:64px;">fasta and gff3 downloaded from Ensembl B73 RefGen V4</div>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">
                      <div class="grid-Reference" style="height:64px;">Populus alba var. pyramidalis</div>
                    </el-col>
                    <el-col :span="8">
                      <div class="grid-Reference" style="height:64px;">P. alba var. pyramidalis reference genome</div>
                    </el-col>
                    <el-col :span="10">
                      <div class="grid-Reference" style="height:64px;">P. alba var. pyramidalis reference genome Publication: PMID 33750794</div>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">
                      <div class="grid-Reference" style="height:64px;line-height:64px;">Solanum lycopersicum</div>
                    </el-col>
                    <el-col :span="8">
                      <div class="grid-Reference" style="height:64px;line-height:64px;">ITAG4.0</div>
                    </el-col>
                    <el-col :span="10">
                      <div class="grid-Reference" style="height:64px;">ftp://ftp.solgenomics.net/tomato_genome/annotation/ITAG4.0_release</div>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">
                      <div class="grid-Reference">Oryza sativa</div>
                    </el-col>
                    <el-col :span="8">
                      <div class="grid-Reference">IRGSP-1.0</div>
                    </el-col>
                    <el-col :span="10">
                      <div class="grid-Reference">https://rapdb.dna.affrc.go.jp/index.html</div>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">
                      <div class="grid-Reference">Fragaria vesca</div>
                    </el-col>
                    <el-col :span="8">
                      <div class="grid-Reference">F. vesca v4.0.a1</div>
                    </el-col>
                    <el-col :span="10">
                      <div class="grid-Reference">https://www.rosaceae.org/</div>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="6">
                      <div class="grid-Reference">Phalaenopsis aphrodite</div>
                    </el-col>
                    <el-col :span="8">
                      <div class="grid-Reference">Orchidstra 2.0</div>
                    </el-col>
                    <el-col :span="10">
                      <div class="grid-Reference">http://orchidstra2.abrc.sinica.edu.tw</div>
                    </el-col>
                  </el-row>
                </div>

          </el-main>
        </el-container>
      </el-container>
    </div>
  </div>
</template>

<script>
import axios from '@/api/http.js';
import Axios from 'axios'
import { cell_identification_reference_detail, cell_identification_csv_download } from "@/api/api";
export default {
  name: "cellIdent",
  components: {
  },
  data() {
    return {
      contentHeight: (window.innerHeight - 330) + 'px',
      goLoading: false,
      cellIdent_form: {
        num_top: 3,
        fileName: '',
        file: ''
      },
      file_name: '',
      fileLoading: false,
      itemList: ['', 'Cell01', 'Cell02', 'Cell03', 'Gene1', '1.33', '0', '0', 'Gene2', '0', '0.75', '0', 'Gene3', '0', '1', '0.43', 'Gene4', '0', '0', '3.17'],
    };
  },
  mounted() {
    // this.init()
  },
  methods: {
    init() {
      let params = {
        lit_id: this.$route.query.lit_id
      }
      this.goLoading = true
      cell_identification_reference_detail(params).then(res => {
        if (res.code == 200) {
          this.detailData = res.data.results[0]
          this.goLoading = false
        }
      });
    },
    download() {
      cell_identification_csv_download({
        species_name: this.$route.query.species_name,
        tissue: this.$route.query.tissue
      }).then(res => {
        if (res.code == 200) {
          window.open(res.data.cell_identification_example_file, '_blank')
        }
      });
    },
    search() {
      if (this.file_name == '') {
        this.$message.warning('Please upload a file！');
        return
      }
      this.$router.push({
        path: '/cellIdentResult',
        query: {
          file_name: this.file_name,
          num_top: this.cellIdent_form.num_top,
          species_name: this.$route.query.species_name,
          tissue: this.$route.query.tissue,
          lit_id: this.$route.query.lit_id
        }
      })
    },
    reset() {
      this.file_name = ''
      this.cellIdent_form = {
        num_top: 3,
        fileName: '',
        file: ''
      }
      this.$refs.file.value = ''
    },
    handleUpdate(event) {
      // if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'csv') {
      //   this.$message.warning('Please upload .csv file！');
      // } else {
      this.cellIdent_form.fileName = event.target.files[0].name
      this.fileLoading = true

      let formData = new FormData()
      formData.append('myfile', event.target.files[0])
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      const $axios = Axios.create({
        baseURL: axios.defaults.baseURL,
        timeout: 1000000
      });

      $axios.post('/api/v1/cell_reference_identification_upload/', formData, config).then(res => {
        if (res.data.code == 200) {
          this.cellIdent_form.file = event.target.files[0]
          this.file_name = res.data.data.file_name
          this.$message.success(res.data.data.msg)
        } else {
          this.$message.warning(res.data.msg);
        }
        this.fileLoading = false
      }).catch(err => {
        this.$message.warning(err.data.msg);
      });
      // }

    },
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>


