<template>
  <div class="CMPredictor">
    <div class="CMPredictor-inner">
      <div class="scsa">
        <p class="keyword_p1">By Blast Homology</p>
        <!-- <p class="keyword_p1">CMPredictor:
          <span style="font-size:16px;">Cell marker predictor based on homology</span>
        </p> -->
        <el-form ref="form1" :inline="true" :rules="rules" :model="CMPredictor_form">
          <el-form-item label="Query species">
            <el-select size="large" v-model="CMPredictor_form.query_specie" @change="querySpecieChange" placeholder="Choose">
              <el-option v-for="(item, index) in QuerysOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item style="margin-left:15px;" label="Reference species">
            <el-select size="large" v-model="CMPredictor_form.refer_specie" placeholder="Choose">
              <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item style="margin-left:15px;" label="Tissue type" prop="tissue_type">
            <el-select size="large" v-model="CMPredictor_form.tissue_type" placeholder="Choose">
              <el-option v-for="(item, index) in TissuseOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="">
            <el-radio-group v-model="CMPredictor_form.marker_resource">
              <el-radio label="all">All</el-radio>
              <el-radio label="Bulk RNA-seq">Bulk RNA-seq</el-radio>
              <el-radio label="Experimental">Experimental</el-radio>
              <el-radio label="scRNA-seq">scRNA-seq</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="Other option：" class="item3">
            <!-- <el-checkbox-group v-model="otherRadio"> -->
            <!-- <el-checkbox label="e_value">E-value</el-checkbox> -->
            <el-form-item label="E-value" prop="e_value">
              <el-select size="large" v-model="CMPredictor_form.e_value" placeholder="Choose">
                <el-option v-for="(item, index) in valueOptions" :key="index" :label="item" :value="item">
                </el-option>
              </el-select>
            </el-form-item>
            <!-- <el-checkbox style="margin-left:15px;" label="identity">Identity</el-checkbox> -->
            <el-form-item label="Identity" prop="identity">
              <el-select size="large" v-model="CMPredictor_form.identity" placeholder="Choose">
                <el-option v-for="(item, index) in IdentityOptions" :key="index" :label="item" :value="item">
                </el-option>
              </el-select>
            </el-form-item>
            <!-- </el-checkbox-group> -->
          </el-form-item>
        </el-form>

        <el-row style="margin: 0 0px 40px 0;">
          <el-button class="btnSearch" @click="example">Example</el-button>
          <el-button class="btnSearch" style="width:126px;" @click="search" :loading="loading">Search</el-button>
          <el-button class="btnReset" @click="reset">Reset</el-button>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
import { query_specie_list, specie_list, tissue_type_list } from "@/api/api";
export default {
  name: "CMPredictor",
  components: {

  },
  data() {
    return {
      deleteQuerySpecieArray: ["Physcomitrella_patens", "Selaginella_moellendorffii", "Marchantia_polymorpha"],
      deleteTissueTypeArray: ["flower", "seed"],
      QuerysOptions: [],
      speciesOptions: [],
      TissuseOptions: [],
      CMPredictor_form: {
        refer_specie: "Arabidopsis_thaliana",
        query_specie: "Actinidia_chinensis",
        tissue_type: "PO:0025034-leaf",
        marker_resource: 'all',
        e_value: "",
        identity: "",
      },
      valueOptions: ['1e-10', '1e-20', '1e-50', '1e-100', '1e-200'],
      IdentityOptions: [30, 50, 70, 90],
      rules: {
        refer_specie: [
          { required: true, message: 'Please enter', trigger: 'change' }
        ],
        query_specie: [
          { required: true, message: 'Please select', trigger: 'change' }
        ]
      },
      loading: false,
      otherRadio: []
    };
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      query_specie_list({}).then(res => {
        if (res.code == 200) {
          this.QuerysOptions = res.data
        }
      });
      specie_list({}).then(res => {
        if (res.code == 200) {
          this.speciesOptions = res.data
        }
      });
      tissue_type_list({}).then(res => {
        if (res.code == 200) {
          if (this.deleteQuerySpecieArray.indexOf(this.CMPredictor_form.query_specie) != -1) {
            for (let i =0; i<res.data.length; i++) {
              if (this.deleteTissueTypeArray.indexOf(res.data[i].label) != -1) {
                res.data.splice(i, 1)
              }
            }
          }    

          this.TissuseOptions = res.data
        }
      });
    },
    querySpecieChange() {
      tissue_type_list({}).then(res => {
        if (res.code == 200) {
          if (this.deleteQuerySpecieArray.indexOf(this.CMPredictor_form.query_specie) != -1) {
            for (let i =0; i<res.data.length; i++) {
              if (this.deleteTissueTypeArray.indexOf(res.data[i].label) != -1) {
                res.data.splice(i, 1)
              }
            }
          }    
          this.TissuseOptions = res.data
        }
      });
    },
    example() {
      this.CMPredictor_form = {
        refer_specie: "Arabidopsis_thaliana",
        query_specie: "Solanum_tuberosum",
        tissue_type: "PO:0025034-leaf",
        marker_resource: 'all',
        e_value: "1e-20",
        identity: "30",
      };
      // this.otherRadio = ['e_value', 'identity']
    },
    search() {
      this.$refs['form1'].validate((valid) => {
        if (valid) {
          let params = {
            refer_specie: this.CMPredictor_form.refer_specie,
            query_specie: this.CMPredictor_form.query_specie,
            tissue_type: this.CMPredictor_form.tissue_type,
            marker_resource: this.CMPredictor_form.marker_resource,
            identity: this.CMPredictor_form.identity,
            e_value: this.CMPredictor_form.e_value,
          }
          // this.otherRadio.forEach(item => {
          //   if (item == 'e_value') {
          //     params = {
          //       ...params,
          //       ...{
          //         e_value: this.CMPredictor_form.e_value
          //       }
          //     }
          //   } else if (item == 'identity') {
          //     params = {
          //       ...params,
          //       ...{
          //         identity: this.CMPredictor_form.identity
          //       }
          //     }
          //   }
          // })
          this.$router.push({
            path: '/CMPredictorDetails',
            query: params
          })
        } else {
          return false;
        }
      })
    },
    reset() {
      this.CMPredictor_form = {
        refer_specie: "Arabidopsis_thaliana",
        query_specie: "Solanum_tuberosum",
        tissue_type: "PO:0025034-leaf",
        marker_resource: 'all',
        e_value: "",
        identity: "",
      };
      this.otherRadio = []
      this.loading = false
      this.$refs['form1'].resetFields()
    },
    // radioChange(val) {
    //   this.CMPredictor_form.e_value = ""
    //   this.CMPredictor_form.identity = ""
    //   this.otherRadio.forEach(item => {
    //     if (item == 'e_value') {
    //       this.CMPredictor_form.e_value = "1e-20"
    //     } else if (item == 'identity') {
    //       this.CMPredictor_form.identity = "30"
    //     }
    //   })
    // }
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
