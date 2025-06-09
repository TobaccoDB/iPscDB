<template>
  <div class="tissueStructure">
    <div class="tissueStructure-inner" v-loading="umapLoading">
      <div class="blast">
        <el-form ref="form1" :inline="true">
          <el-form-item label="Tissue" prop="tissue">
            <el-select style="width:200px;" @change="tissueChange" size="large" v-model="tissue" placeholder="Choose">
              <el-option label="Root" value="Root"></el-option>
              <el-option label="leaf" value="leaf"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-radio-group style="margin-top:10px;" v-model="radio">
              <el-radio label="Tree">Cell Type Tree</el-radio>
              <el-radio label="Reference">Reference Cell Type</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>

        <div v-show="radio == 'Tree'" :style="{width:'100%',height: '660px'}">
          <div ref='barChart1' :style="{width:'1200px',height: '660px'}"></div>
        </div>
        <el-form v-show="radio == 'Reference'" :inline="true" @submit.native.prevent size="lager" :model="formInline" class="demo-form-inline">
          <el-form-item label="Cell Type">
            <el-input v-model="formInline.cell_type" clearable placeholder="Please enter"></el-input>
          </el-form-item>
          <el-form-item label="Type">
            <el-input v-model="formInline.types" clearable placeholder="Please enter"></el-input>
          </el-form-item>
          <el-form-item label="Parent">
            <el-input v-model="formInline.parent" clearable placeholder="Please enter"></el-input>
          </el-form-item>
          <el-form-item label="">
            <el-button type="primary" @click="search">GO</el-button>
          </el-form-item>
        </el-form>
        <jg-table v-show="radio == 'Reference'" :tableData="tableData" :column='column' :loading="tableLoading" :paginationConfig="paginationConfig"
          @handleCurrentChange="handleCurrentChange" @handleSizeChange="handleSizeChange"></jg-table>
      </div>
    </div>
  </div>
</template>

<script>
import echarts from 'echarts';
import { tissue_structure, reference_cell_type_list } from "@/api/api";
import { option, column } from "./config";
import jgTable from '@/components/jgTable/index'
export default {
  name: "tissueStructure",
  components: {
    jgTable
  },
  data() {
    return {
      tissue: 'Root',
      option,
      umapLoading: false,
      radio: 'Tree',
      formInline: {
        cell_type: '',
        types: '',
        parent: '',
      },
      tableData: [],
      column,
      paginationConfig: {
        page: 1,
        size: 10,
        sizes: [10, 20, 30],
        total: 0
      },
      tableLoading: false,
    };
  },
  mounted() {
    this.init()
    this.getTableData()
  },
  methods: {
    tissueChange() {
      this.init()
      this.getTableData()
    },
    init() {
      let barChart1 = this.$refs.barChart1
      this.umapLoading = true
      tissue_structure({
        tissue: this.tissue
      }).then(res => {
        if (res.code == 200) {
          if (barChart1) {
            this.option.series[0].data = [res.data]
          }
          this.Echarts = echarts.init(barChart1);
          this.Echarts.setOption(this.option, true)
          this.umapLoading = false
        }
      });
    },
    getTableData() {
      this.tableLoading = true
      reference_cell_type_list({
        cell_type: this.formInline.cell_type,
        types: this.formInline.types,
        parent: this.formInline.parent,
        tissue: this.tissue,
        page: this.paginationConfig.page,
        page_size: this.paginationConfig.size
      }).then(res => {
        if (res.code == 200) {
          this.tableData = res.data.results
          this.paginationConfig.total = res.data.count
          this.tableLoading = false
        }
      });
    },
    search() {
      this.paginationConfig.page = 1
      this.getTableData()
    },
    handleCurrentChange(val) {
      this.paginationConfig.page = val;
      this.getTableData()
    },
    handleSizeChange(val) {
      this.paginationConfig.page = 1
      this.paginationConfig.size = val
      this.getTableData()
    },
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
