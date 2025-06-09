<template>
  <div class="CellAnnotation">
    <div class="CellAnnotation-inner">
      <div class="stepBar">
        <el-steps :active="4" finish-status="success" :align-center="true">
          <el-step style="cursor:pointer;" @click.native="setpClick(item)" :title="item.name" v-for="(item, index) in stepList"></el-step>
        </el-steps>
      </div>
      <div class="blast">
        <el-header>CellAnnotation</el-header>
        <div id="myDiv" style="width: 100%; height: 600px;"></div>
        <el-header>Gene expression</el-header>
        <!-- 表格 -->
        <div class="firstTable">
          <jg-table :tableData="tableData" :column="column" :loading="loading" :cellstyle="cellstyle" :paginationConfig="paginationConfig"
            @handleCurrentChange="handleCurrentChange" @handleSizeChange="handleSizeChange" @handlecell="handlecell"></jg-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { monocle_expressed_list } from '@/api/api'
import jgTable from '@/components/jgTable/index'
import Plotly from 'plotly.js-dist'
export default {
  name: 'CellAnnotation',
  components: {
    jgTable
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
      data1Form: {
        sampleName: '',
      },
      tableData: [],
      column: [
        { key: 'gene_id', label: 'Grop' },
        { key: 'status', label: 'Cluster' },
        { key: 'family', label: 'Gene name' },
        { key: 'pval', label: 'Scores' },
        { key: 'qval', label: 'Logfoldchanges' },
        { key: 'gene_short_name', label: 'Pvals' },
        { key: 'num_cells_expressed', label: 'Pvals adj' }
      ],
      paginationConfig: {
        page: 1,
        size: 10,
        sizes: [10, 20, 30],
        total: 0
      },
      loading: false,
      isShowResult: false,
      chartData1: []
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      let country = ['Switzerland (2011)', 'Chile (2013)', 'Japan (2014)', 'United States (2012)', 'Slovenia (2014)', 'Canada (2011)', 'Poland (2010)', 'Estonia (2015)', 'Luxembourg (2013)', 'Portugal (2011)'];
      let votingPop = [40, 45.7, 52, 53.6, 54.1, 54.2, 54.5, 54.7, 55.1, 56.6];
      let regVoters = [49.1, 42, 52.7, 84.3, 51.7, 61.1, 55.3, 64.2, 91.1, 58.9];

      for (let i = 0; i < 90; i++) {
        let arr = [];
        for (let j = 0; j < 9; j++) {
          let item = Math.floor(Math.random() * 10000 + 1);
          arr.push(item);
        }

        this.chartData1.push({
          type: 'scatter', //scatter中的markers
          x: arr,
          y: country,
          mode: 'markers',
          name: 'Percent',
          marker: {
            // color: 'rgba(156, 165, 196, 0.95)',
            line: {
              color: 'rgba(156, 165, 196, 1.0)',
              width: 1,
            },
            symbol: 'circle',
            size: 8
          }
        });
      }

      let layout = {
        title: 'OECD countries title',
        xaxis: {
          showgrid: false,
          showline: true,
          linecolor: 'rgb(102, 102, 102)',
          // title: 'x-axis-title',
          // titlefont: {
          //   color: 'black',
          //   size: 16
          // },
          // tickfont: {
          //   color: 'black'
          // },
          // autotick: false,    //自动刻度设置
          // // dtick: 20,         //刻度间距
          // ticks: 'inside',     //tick在坐标轴上的位置
          // side: 'bottom',
          // tickcolor: 'rgba(204, 204, 204, 1)'
        },
        margin: {
          l: 140,
          r: 140,
          b: 50,
          t: 100
        },
        legend: {
          bgcolor: 'rgba(254, 237, 224,0)',  //透明背景
          // yanchor: 'bottom',
          // xanchor: 'right',
          x: 1,               // 图例的 x 位置（范围从 0 到 2）
          y: 0.5,               // 图例的 y 位置（范围从 0 到 1）
          font: {
            family: 'Arial',  // 图例文字的字体
            size: 16,        // 图例文字的大小
            color: '#000000' // 图例文字的颜色
          }
        },
        // width: 600,
        // height: 600,
        // paper_bgcolor: 'rgb(254, 247, 234)',   //底层画布背景
        // plot_bgcolor: 'rgb(254, 237, 224)',    //图像背景
        hovermode: 'x'                   //悬停模式
      };

      Plotly.newPlot('myDiv', this.chartData1, layout);

    },
    setpClick(item) {
      this.$router.push({
        path: '/' + item.link,
        query: {}
      })
    },
    // 表格部分
    getTableData() {
      this.loading = true
      monocle_expressed_list({
        ...this.monocleForm,
        ...{
          page: this.paginationConfig.page,
          page_size: this.paginationConfig.size
        }
      }).then((res) => {
        if (res.code == 200) {
          if (res.count) {
            this.tableData = res.data
            this.paginationConfig.total = res.count
          } else {
            this.tableData = []
            this.paginationConfig.total = 0
          }
          this.loading = false
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
    handlecell(params) {
      if (params.col.label == 'Gene ID') {

      }
    },
  }
}
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
