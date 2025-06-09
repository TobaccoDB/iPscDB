<template>
  <div class="geneExpression">
    <div class="geneExpression-inner" v-loading="umapLoading">
      <div class="blast">
        <el-form ref="form1" :inline="true" :model="geneExpression_form" :rules="rules">
          <el-form-item label="Species" prop="species_name">
            <el-select clearable style="width:200px;" size="large" @change="species_nameChange" v-model="geneExpression_form.species_name"
              placeholder="Choose">
              <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Tissue" prop="tissue">
            <el-select clearable style="width:200px;" @change="tissueChange" size="large" v-model="geneExpression_form.tissue" placeholder="Choose">
              <el-option v-for="(item, index) in geneExpression_form_option.tissueOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Gene ID" prop="gene_id">
            <el-select filterable clearable style="width:200px;" size="large" v-model="geneExpression_form.gene_id" placeholder="Choose">
              <el-option v-for="item in geneExpression_form_option.gene_idOptions" :key="item.label" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="">
            <el-button class="btnSearch" @click="search">GO</el-button>
          </el-form-item>
        </el-form>
        <div :style="{width:'100%',height: umapHeight}">
          <!-- <el-empty v-if="umapHeight == '100px'" style="width:1200px;height:300px;position: absolute;font-size:16px;color:#666;text-align:center;"
            description="No Data"></el-empty> -->
          <p v-if="umapHeight == '100px'" style="width:1200px;height:110px;background:#fff;position: absolute;font-size:16px;color:#666;line-height:300px;text-align:center;z-index:100;">
            No Data
          </p>
          <div v-show="umapHeight == '500px'" ref='barChart1' :style="{width:'1200px',height: '500px'}"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import echarts from 'echarts';
import { gene_expression_species_name, gene_expression_tissue, gene_id_express_down, gene_express_umap } from "@/api/api";
import { option1, } from "./config";
export default {
  name: "geneExpression",
  components: {
  },
  data() {
    return {
      option1,
      geneExpression_form: {
        species_name: "Arabidopsis_thaliana",
        tissue: "Root",
        gene_id: "AT1G01070",
      },
      rules: {
        species_name: [
          { required: true, message: 'Please select', trigger: 'change' }
        ],
        tissue: [
          { required: true, message: 'Please select', trigger: 'change' }
        ]
      },
      speciesOptions: [],
      geneExpression_form_option: {
        tissueOptions: [],
        gene_idOptions: [],
      },
      umapHeight: '100px',
      umapLoading: false,
    };
  },
  mounted() {
    this.init()
    this.search()
  },
  methods: {
    init() {
      gene_expression_species_name({}).then(res => {
        if (res.code == 200) {
          this.speciesOptions = res.data
        }
      });
      gene_expression_tissue({ species_name: this.geneExpression_form.species_name }).then(res => {
        if (res.code == 200) {
          this.geneExpression_form_option.tissueOptions = res.data
        }
      });
      gene_id_express_down({ species_name: this.geneExpression_form.species_name, tissue: this.geneExpression_form.tissue }).then(res => {
        if (res.code == 200) {
          this.geneExpression_form_option.gene_idOptions = res.data
        }
      });
    },
    species_nameChange() {
      gene_expression_tissue({ species_name: this.geneExpression_form.species_name }).then(res => {
        if (res.code == 200) {
          this.geneExpression_form.tissue = ''
          this.geneExpression_form.gene_id = ''
          this.geneExpression_form_option.gene_idOptions = []
          this.geneExpression_form_option.tissueOptions = res.data
        }
      });
    },
    tissueChange() {
      gene_id_express_down({ species_name: this.geneExpression_form.species_name, tissue: this.geneExpression_form.tissue }).then(res => {
        if (res.code == 200) {
          this.geneExpression_form.gene_id = ''
          this.geneExpression_form_option.gene_idOptions = res.data
        }
      });
    },
    search() {
      this.$refs['form1'].validate((valid) => {
        if (valid) {
          let barChart1 = this.$refs.barChart1
          this.umapLoading = true
          gene_express_umap(this.geneExpression_form).then(res => {
            if (res.code == 200) {
              if (res.data.expression_data.length > 0) {
                this.umapHeight = '500px'
                if (barChart1) {
                  this.option1.series[0].data = res.data.expression_data
                }
              } else {
                this.umapHeight = '100px'
              }
              this.Echarts = echarts.init(barChart1);
              this.Echarts.setOption(this.option1, true)
              this.umapLoading = false
            }
          });
        } else {
          return false;
        }
      });

    },
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
