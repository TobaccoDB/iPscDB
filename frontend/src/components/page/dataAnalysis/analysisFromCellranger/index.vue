<template>
  <div class="analysisFromCellranger">
    <div class="analysisFromCellranger-inner">
      <div class="blast">
        <el-header>Analysis from cellranger</el-header>
        <el-form ref="form1" :inline="true" :model="monocleForm" :rules="rules">
          <el-form-item label="E-mail" prop="email">
            <el-input style="width: 200px" clearable v-model="monocleForm.email" placeholder="Please enter"></el-input>
          </el-form-item>
          <el-form-item label="Analysis name">
            <el-input style="width: 200px" clearable v-model="monocleForm.analysis_name" placeholder="Please enter"></el-input>
          </el-form-item>
          <el-form-item label="">
            <el-button class="btnSearch" @click="search">Search</el-button>
            <el-button class="btnSearch" :loading="refreshLoading" @click="Refresh">Refresh</el-button>
          </el-form-item>
          <el-form-item label="" style="float:right;">
            <el-button class="btnSearch" @click="jumpCellRanger">New Analysis</el-button>
          </el-form-item>
        </el-form>
      </div>
      <!-- 表格 -->
      <div class="firstTable">
        <div class="centerTable">
          <!-- <jg-table :tableData="tableData" :column="column" :loading="loading" :cellstyle="cellstyle" :paginationConfig="paginationConfig"
            operationText="Operation" :isHaveView="true" :isHaveDelete="true" @viewHandle="viewHandle" @deleteHandle="deleteHandle"
            @handleCurrentChange="handleCurrentChange" @handleSizeChange="handleSizeChange"></jg-table> -->
          <el-table :cell-style="cellstyle" :data="tableData" :loading="loading" border style="width: 100%">
            <el-table-column v-for="(item, index) in column" :prop="item.key" :label="item.label" :align="item.align === undefined ? 'center' : item.align">
            </el-table-column>
            <el-table-column fixed="right" label="Operation" width="120" align="center">
              <template slot-scope="scope">
                <i v-if="(scope.row.status == 'Finished' || scope.row.status == 'Failure')&&scope.row.email.split('@')[0] != 'xxxxx'" class="el-icon-view pointer"
                  style="padding: 0 5px; color: #24a461" @click="viewHandle(scope)"></i>
                <i v-if="(scope.row.status == 'Finished' || scope.row.status == 'Failure')&&scope.row.email.split('@')[0] == 'xxxxx'" class="el-icon-view"
                  style="padding: 0 5px;color: #c0c4cc;cursor: not-allowed;"></i>
                <i v-if="scope.row.email.split('@')[0] != 'xxxxx'" class="el-icon-delete pointer" style="padding: 0 5px; color: #24a461"
                  @click="deleteHandle(scope)"></i>
                <i v-if="scope.row.email.split('@')[0] == 'xxxxx'" class="el-icon-delete" style="padding: 0 5px; color: #c0c4cc;cursor: not-allowed;"></i>
                <!-- <span v-if="scope.row.email.split('@')[0] == 'xxxxx'">XXX</span> -->
              </template>
            </el-table-column>
          </el-table>
          <el-pagination style="text-align: right; padding: 10px 5px" background :current-page="paginationConfig.page" :page-sizes="paginationConfig.sizes"
            :page-size="paginationConfig.size" :pager-count="7" :total="paginationConfig.total" @current-change="handleCurrentChange"
            @size-change="handleSizeChange" layout='total, sizes, prev, pager, next'>
          </el-pagination>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { analysisCellrangerList, analysisDelete } from '@/api/analysis'
import jgTable from '@/components/jgTable/index'

export default {
  name: 'analysisFromCellranger',
  components: {
    jgTable
  },
  data() {
    return {
      monocleForm: {
        email: '', // 862536612@qq.com
        analysis_name: ''
      },
      rules: {
        email: [
          { required: true, message: 'Please enter your email address', trigger: 'blur' },
          { type: 'email', message: 'Please enter the correct email address', trigger: ['blur', 'change'] }
        ],
      },
      tableData: [],
      column: [
        { key: 'id', label: 'Number' },
        { key: 'email', label: 'E-mail' },
        { key: 'analysis_name', label: 'Analysis name' },
        { key: 'status', label: 'Status' },
        { key: 'update_time', label: 'End time' },
        { key: 'create_time', label: 'Start time' },
        // { key: '', label: 'Operation' }
      ],
      paginationConfig: {
        page: 1,
        size: 10,
        sizes: [10, 20, 30],
        total: 0
      },
      loading: false,
      refreshLoading: false,
    }
  },
  mounted() {
    this.getTableData()
  },
  methods: {
    search() {
      this.$refs['form1'].validate((valid) => {
        if (valid) {
          this.paginationConfig.page = 1
          this.getTableData()
        } else {
          return false;
        }
      });
    },
    Refresh() {
      this.refreshLoading = true
      this.paginationConfig.page = 1
      this.getTableData()
    },
    jumpCellRanger() {
      this.$router.push({
        path: '/CellRanger',
        query: {

        }
      })
    },
    // 表格部分
    getTableData() {
      this.loading = true
      analysisCellrangerList({
        ...this.monocleForm,
        ...{
          source: 'cell_ranger',
          page: this.paginationConfig.page,
          page_size: this.paginationConfig.size
        }
      }).then((res) => {
        if (res.code == 200) {
          if (res.data.count) {
            this.tableData = res.data.results
            this.tableData.forEach(item => {
              if (item.status == 'STARTED') {
                item.status = 'Started'
              }
              // string.charAt(0).toUpperCase() + string.toLowerCase().slice(1);
            });
            this.paginationConfig.total = res.data.count
          } else {
            this.tableData = []
            this.paginationConfig.total = 0
          }
          this.loading = false
          this.refreshLoading = false
        }
      })
    },
    handleCurrentChange(val) {
      this.paginationConfig.page = val
      this.getTableData()
    },
    handleSizeChange(val) {
      this.paginationConfig.page = 1
      this.paginationConfig.size = val
      this.getTableData()
    },
    cellstyle({ row, column, rowIndex, columnIndex }) {
      if (column.label === 'Gene ID') {
        return { color: '#0a9daa', cursor: 'pointer' }
      }
      // 针对Safari表格width与showOverflowTooltip暂不能共存异常
      const tempWidth = column.realWidth || column.width
      if (column.showOVerflowTooltip) {
        return {
          minWidth: tempWidth + 'px',
          maxWidth: tempWidth + 'px'
        }
      }
      return { fontSize: '14px' }
    },
    viewHandle(params) {
      let stepList = []
      if (params.row.status == 'Failure') {
        stepList = [
          { name: 'Cell Ranger', link: 'CellRanger', step: 'cell_ranger', enterResults: false },
          { name: 'Sample QC', link: 'DataAnalysisSampleQC', step: 'sample_qc', enterResults: false },
          { name: 'Data Process', link: 'DataProcess', step: 'data_process', enterResults: false },
          { name: 'Cluster', link: 'Cluster', step: 'cluster', enterResults: false },
          { name: 'Cell Annotation', link: 'DataAnalysisCellAnnotation', step: 'cell_annotation', enterResults: false },
        ]
      } else {
        stepList = [
          { name: 'Cell Ranger', link: 'CellRanger', step: 'cell_ranger', enterResults: true },
          { name: 'Sample QC', link: 'CellRanger', step: 'sample_qc', enterResults: true },
          { name: 'Data Process', link: 'DataAnalysisSampleQC', step: 'data_process', enterResults: true },
          { name: 'Cluster', link: 'DataProcess', step: 'cluster', enterResults: true },
          { name: 'Cell Annotation', link: 'Cluster', step: 'cell_annotation', enterResults: true },
          // { name: 'Cell Ranger', link: 'CellRanger', step: 'cell_ranger' },
          // { name: 'Sample QC', link: 'DataAnalysisSampleQC', step: 'sample_qc' },
          // { name: 'Data Process', link: 'DataProcess', step: 'data_process' },
          // { name: 'Cluster', link: 'Cluster', step: 'cluster' },
          // { name: 'Cell Annotation', link: 'DataAnalysisCellAnnotation', step: 'cell_annotation' },
        ]
      }
      stepList.forEach((item, index) => {
        if (params.row.current_step == item.step) {
          this.$router.push({
            path: '/' + item.link,
            query: {
              uuid: params.row.uuid,
              id: params.row.id,
              step: params.row.current_step,
              from: params.row.source,
              enterResults: item.enterResults
            }
          })
        }
      });
    },
    deleteHandle(row) {
      this.$confirm('Are you sure to delete！', 'Tips', {
        confirmButtonText: 'confirm',
        cancelButtonText: 'cancel',
        type: 'warning'
      }).then(() => {
        analysisDelete(row.row.id).then(res => {
          if (res.code === 200) {
            this.$message.success(res.data.msg);
            this.getTableData()
          }
        });
      })
    }
  }
}
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
