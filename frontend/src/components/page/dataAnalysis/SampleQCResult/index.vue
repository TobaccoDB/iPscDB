<template>
  <div class="SampleQCResult">
    <div class="SampleQCResult-inner">
      <div class="blast">
        <el-header>Sample QC Result</el-header>
        <el-tabs type="border-card">
          <el-tab-pane label="Data1">
            <!-- <p class="title1">Cells uploaded</p> -->
            <!-- <div style="" class="UMAP">
              <img src='http://47.96.22.63/Sample_QC/qc_picture/example.svg' width="100%" />
            </div> -->
            <el-row :gutter="20">
              <el-col :span="6" style="text-align:right;">
                <el-button type="text" class="chartBtn" icon="el-icon-edit" @click="editChart1">edit</el-button>
                <el-button type="text" class="chartBtn" icon="el-icon-download" :loading="downloadLoading[0].loading" @click="chartDownload('chart1', 0, ruleForm1.titleName)">download</el-button>
                <div id="myDiv1" ref="chart1" style="width: 297px; height: 400px"></div>
              </el-col>
              <el-col :span="6" style="text-align:right;">
                <el-button type="text" class="chartBtn" icon="el-icon-edit" @click="editChart2">edit</el-button>
                <el-button type="text" class="chartBtn" icon="el-icon-download" :loading="downloadLoading[1].loading" @click="chartDownload('chart2', 1, ruleForm2.titleName)">download</el-button>
                <div id="myDiv2" ref="chart2" style="width: 297px; height: 400px"></div>
              </el-col>
              <el-col :span="6" style="text-align:right;" v-show="formTop.mt">
                <el-button type="text" class="chartBtn" icon="el-icon-edit" @click="editChart3">edit</el-button>
                <el-button type="text" class="chartBtn" icon="el-icon-download" :loading="downloadLoading[2].loading" @click="chartDownload('chart3', 2, ruleForm3.titleName)">download</el-button>
                <div id="myDiv3" ref="chart3" style="width: 297px; height: 400px"></div>
              </el-col>
              <el-col :span="6" style="text-align:right;" v-show="formTop.pt">
                <el-button type="text" class="chartBtn" icon="el-icon-edit" @click="editChart4">edit</el-button>
                <el-button type="text" class="chartBtn" icon="el-icon-download" :loading="downloadLoading[3].loading" @click="chartDownload('chart4', 3, ruleForm4.titleName)">download</el-button>
                <div id="myDiv4" ref="chart4" style="width: 297px; height: 400px"></div>
              </el-col>
            </el-row>
            <ul class="scsa_bottom_ul">
              <li>
                <span class="statusSpan1">{{backVal1}}</span>
                <span class="statusSpan2">Genes</span>
              </li>
              <li>
                <span class="statusSpan1">{{backVal2}}</span>
                <span class="statusSpan2">Cells</span>
              </li>
              <li>
                <span class="statusSpan1">QC</span>
                <span class="statusSpan2">Pass</span>
              </li>
            </ul>
            <el-button type="text" class="textBtn" @click="download" icon="el-icon-download">h5ad</el-button>
          </el-tab-pane>
          <el-tab-pane label="Data2">
            <!-- <p class="title1">Cells uploaded</p> -->
            <el-row :gutter="20">
              <el-col :span="6" style="text-align:right;">
                <el-button type="text" class="chartBtn" icon="el-icon-edit" @click="editChart5">edit</el-button>
                <el-button type="text" class="chartBtn" icon="el-icon-download" :loading="downloadLoading[4].loading" @click="chartDownload('chart5', 4, ruleForm5.titleName)">download</el-button>
                <div id="myDiv5" ref="chart5" style="width: 297px; height: 400px"></div>
              </el-col>
              <el-col :span="6" style="text-align:right;">
                <el-button type="text" class="chartBtn" icon="el-icon-edit" @click="editChart6">edit</el-button>
                <el-button type="text" class="chartBtn" icon="el-icon-download" :loading="downloadLoading[5].loading" @click="chartDownload('chart6', 5, ruleForm6.titleName)">download</el-button>
                <div id="myDiv6" ref="chart6" style="width: 297px; height: 400px"></div>
              </el-col>
              <el-col :span="6" style="text-align:right;" v-show="formTop.mt">
                <el-button type="text" class="chartBtn" icon="el-icon-edit" @click="editChart7">edit</el-button>
                <el-button type="text" class="chartBtn" icon="el-icon-download" :loading="downloadLoading[6].loading" @click="chartDownload('chart7', 6, ruleForm7.titleName)">download</el-button>
                <div id="myDiv7" ref="chart7" style="width: 297px; height: 400px"></div>
              </el-col>
              <el-col :span="6" style="text-align:right;" v-show="formTop.pt">
                <el-button type="text" class="chartBtn" icon="el-icon-edit" @click="editChart8">edit</el-button>
                <el-button type="text" class="chartBtn" icon="el-icon-download" :loading="downloadLoading[7].loading" @click="chartDownload('chart8', 7, ruleForm8.titleName)">download</el-button>
                <div id="myDiv8" ref="chart8" style="width: 297px; height: 400px"></div>
              </el-col>
            </el-row>
            <ul class="scsa_bottom_ul">
              <li>
                <span class="statusSpan1">{{backVal3}}</span>
                <span class="statusSpan2">Genes</span>
              </li>
              <li>
                <span class="statusSpan1">{{backVal4}}</span>
                <span class="statusSpan2">Cells</span>
              </li>
              <li>
                <span class="statusSpan1">QC</span>
                <span class="statusSpan2">Pass</span>
              </li>
            </ul>
            <el-button type="text" class="textBtn" @click="download2" icon="el-icon-download">h5ad</el-button>
          </el-tab-pane>
        </el-tabs>
        <!-- 修改图表配置弹窗 -->
        <el-dialog title="Configuration" :visible.sync="ruleForm1.isShowTitle" width="400px" v-dialogDrag :close-on-click-modal="false">
          <chartSet :chartForm="ruleForm1" @submitForm="submitForm1"></chartSet>
        </el-dialog>
        <el-dialog title="Configuration" :visible.sync="ruleForm2.isShowTitle" width="400px" v-dialogDrag :close-on-click-modal="false">
          <chartSet :chartForm="ruleForm2" @submitForm="submitForm2"></chartSet>
        </el-dialog>
        <el-dialog title="Configuration" :visible.sync="ruleForm3.isShowTitle" width="400px" v-dialogDrag :close-on-click-modal="false">
          <chartSet :chartForm="ruleForm3" @submitForm="submitForm3"></chartSet>
        </el-dialog>
        <el-dialog title="Configuration" :visible.sync="ruleForm4.isShowTitle" width="400px" v-dialogDrag :close-on-click-modal="false">
          <chartSet :chartForm="ruleForm4" @submitForm="submitForm4"></chartSet>
        </el-dialog>

        <el-dialog title="Configuration" :visible.sync="ruleForm5.isShowTitle" width="400px" v-dialogDrag :close-on-click-modal="false">
          <chartSet :chartForm="ruleForm5" @submitForm="submitForm5"></chartSet>
        </el-dialog>
        <el-dialog title="Configuration" :visible.sync="ruleForm6.isShowTitle" width="400px" v-dialogDrag :close-on-click-modal="false">
          <chartSet :chartForm="ruleForm6" @submitForm="submitForm6"></chartSet>
        </el-dialog>
        <el-dialog title="Configuration" :visible.sync="ruleForm7.isShowTitle" width="400px" v-dialogDrag :close-on-click-modal="false">
          <chartSet :chartForm="ruleForm7" @submitForm="submitForm7"></chartSet>
        </el-dialog>
        <el-dialog title="Configuration" :visible.sync="ruleForm8.isShowTitle" width="400px" v-dialogDrag :close-on-click-modal="false">
          <chartSet :chartForm="ruleForm8" @submitForm="submitForm8"></chartSet>
        </el-dialog>
        <el-button style="margin-top:20px;" class="btnSearch" @click="jumpSampleQC">Next</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { qc_filter_data_result, analysisCellrangerList } from '@/api/analysis'
import Plotly from 'plotly.js-dist'
import chartSet from './chartSet'
import html2canvas from 'html2canvas'

export default {
  name: 'SampleQCResult',
  components: {
    chartSet
  },
  props: {
    parentMsg: {
      type: Object
    }
  },
  data() {
    return {
      activeName: 'first',
      ruleForm1: {
        isShowTitle: false,
        titleShow: true,
        Xshow: true,
        Yshow: true,
        hovermode: true,
        titleName: "nCount_RNA",
        axisColor: '#333',
        plotColor: '#333',
        violinColor: '#F8766D',
        plotSize: 2,
        showticklabels: true
      },
      ruleForm2: {
        isShowTitle: false,
        titleShow: true,
        Xshow: true,
        Yshow: true,
        hovermode: true,
        titleName: "nFeature_RNA",
        axisColor: '#333',
        plotColor: '#333',
        violinColor: '#F8766D',
        plotSize: 2,
        showticklabels: true
      },
      ruleForm3: {
        isShowTitle: false,
        titleShow: true,
        Xshow: true,
        Yshow: true,
        hovermode: true,
        titleName: "percent.mt",
        axisColor: '#333',
        plotColor: '#333',
        violinColor: '#F8766D',
        plotSize: 2,
        showticklabels: true
      },
      ruleForm4: {
        isShowTitle: false,
        titleShow: true,
        Xshow: true,
        Yshow: true,
        hovermode: true,
        titleName: "percent.pt",
        axisColor: '#333',
        plotColor: '#333',
        violinColor: '#F8766D',
        plotSize: 2,
        showticklabels: true
      },
      ruleForm5: {
        isShowTitle: false,
        titleShow: true,
        Xshow: true,
        Yshow: true,
        hovermode: true,
        titleName: "nCount_RNA",
        axisColor: '#333',
        plotColor: '#333',
        violinColor: '#F8766D',
        plotSize: 2,
        showticklabels: true
      },
      ruleForm6: {
        isShowTitle: false,
        titleShow: true,
        Xshow: true,
        Yshow: true,
        hovermode: true,
        titleName: "nFeature_RNA",
        axisColor: '#333',
        plotColor: '#333',
        violinColor: '#F8766D',
        plotSize: 2,
        showticklabels: true
      },
      ruleForm7: {
        isShowTitle: false,
        titleShow: true,
        Xshow: true,
        Yshow: true,
        hovermode: true,
        titleName: "percent.mt",
        axisColor: '#333',
        plotColor: '#333',
        violinColor: '#F8766D',
        plotSize: 2,
        showticklabels: true
      },
      ruleForm8: {
        isShowTitle: false,
        titleShow: true,
        Xshow: true,
        Yshow: true,
        hovermode: true,
        titleName: "percent.pt",
        axisColor: '#333',
        plotColor: '#333',
        violinColor: '#F8766D',
        plotSize: 2,
        showticklabels: true
      },
      backVal1: 0,
      backVal2: 0,
      backVal3: 0,
      backVal4: 0,
      layout1: {},
      config1: {},
      layout2: {},
      config2: {},
      layout3: {},
      config3: {},
      layout4: {},
      config4: {},
      layout5: {},
      config5: {},
      layout6: {},
      config6: {},
      layout7: {},
      config7: {},
      layout8: {},
      config8: {},
      downloadLoading: [{ loading: false }, { loading: false }, { loading: false }, { loading: false }, { loading: false }, { loading: false }, { loading: false }, { loading: false }],
      formTop: {}
    }
  },
  mounted() {
    this.backVal1 = this.parentMsg.data1.n_genes
    this.backVal2 = this.parentMsg.data1.n_cells
    this.backVal3 = this.parentMsg.data2.n_genes
    this.backVal4 = this.parentMsg.data2.n_cells
    this.formTop = this.parentMsg.formTop
    console.log(222, this.parentMsg)
    this.init()
    this.init2()
  },
  methods: {
    editChart1() {
      this.ruleForm1.isShowTitle = true
    },
    editChart2() {
      this.ruleForm2.isShowTitle = true
    },
    editChart3() {
      this.ruleForm3.isShowTitle = true
    },
    editChart4() {
      this.ruleForm4.isShowTitle = true
    },
    editChart5() {
      this.ruleForm5.isShowTitle = true
    },
    editChart6() {
      this.ruleForm6.isShowTitle = true
    },
    editChart7() {
      this.ruleForm7.isShowTitle = true
    },
    editChart8() {
      this.ruleForm8.isShowTitle = true
    },
    init() {
      // 准备数据
      const traces1 = [{
        type: 'violin',
        y: this.parentMsg.data1.nCount_RNA,
        name: '',
        // name: 'nCount_RNA',
        line: {
          color: this.ruleForm1.violinColor
        },
      }]
      const traces2 = [{
        type: 'violin',
        y: this.parentMsg.data1.nFeature_RNA,
        name: '',
        line: {
          color: this.ruleForm2.violinColor
        },
      }]
      const traces3 = [{
        type: 'violin',
        y: this.parentMsg.data1.percent_mt,
        name: '',
        line: {
          color: this.ruleForm3.violinColor
        },
      }]
      const traces4 = [{
        type: 'violin',
        y: this.parentMsg.data1.percent_pt,
        name: '',
        line: {
          color: this.ruleForm4.violinColor
        },
      }]
      traces1.push({
        y: this.parentMsg.data1.nCount_RNA,
        name: "nCount_RNA",
        type: "scatter",
        mode: "markers",
        xaxis: 'x2', // 指定使用第二个x轴
        marker: {
          size: this.ruleForm1.plotSize, // 散点大小
          color: this.ruleForm1.plotColor,// 散点颜色
        },
      });
      traces2.push({
        y: this.parentMsg.data1.nFeature_RNA,
        name: "nFeature_RNA",
        type: "scatter",
        mode: "markers",
        xaxis: 'x2', // 指定使用第二个x轴
        marker: {
          size: this.ruleForm2.plotSize, // 散点大小
          color: this.ruleForm2.plotColor,// 散点颜色
        },
      });
      traces3.push({
        y: this.parentMsg.data1.percent_mt,
        name: "percent.mt",
        type: "scatter",
        mode: "markers",
        xaxis: 'x2', // 指定使用第二个x轴
        marker: {
          size: this.ruleForm3.plotSize, // 散点大小
          color: this.ruleForm3.plotColor,// 散点颜色
        },
      });
      traces4.push({
        y: this.parentMsg.data1.percent_pt,
        name: "percent.pt",
        type: "scatter",
        mode: "markers",
        xaxis: 'x2', // 指定使用第二个x轴
        marker: {
          size: this.ruleForm4.plotSize, // 散点大小
          color: this.ruleForm4.plotColor,// 散点颜色
        },
      });
      this.layout1 = {
        grid: {
          rows: 1,
          columns: 1,
          pattern: 'independent',
        },
        // y: 0.5,
        showlegend: false, // 设置不显示图例
        hovermode: this.ruleForm1.hovermode,  // 隐藏悬浮显示
        hoverinfo: 'none', //'x'、‌'y'、‌'text'、‌'name'和'all'
        scattermode: "overlay",
        title: this.ruleForm1.titleName,  // 是否显示标题
        scattergap: 0.8,
        violingap: 0,
        violingroupgap: 0,
        yaxis: {
          // title: '',
          // zeroline: true,  // 是否显示X轴
          zeroline: this.ruleForm1.Xshow,  // 是否显示X轴
          color: this.ruleForm1.axisColor,  // 坐标轴颜色
          showticklabels: this.ruleForm1.showticklabels, // 是否显示刻度标记
          showgrid: false,
          showline: this.ruleForm1.Yshow, // 是否显示Y轴
        },
        xaxis: { title: '' },
        xaxis2: {
          showgrid: false,
          // title: { text: '' }, // 第二个x轴的标题
          overlaying: 'x', // 指定这是第二个x轴，并且它应该覆盖第一个x轴
          // side: 'top', // 将第二个x轴放置在图表的顶部
          showticklabels: false,
          visible: false
        },
      };
      this.layout2 = {
        grid: {
          rows: 1,
          columns: 1,
          pattern: 'independent',
        },
        // y: 0.5,
        showlegend: false, // 设置不显示图例
        hovermode: this.ruleForm2.hovermode,  // 隐藏悬浮显示
        hoverinfo: 'none', //'x'、‌'y'、‌'text'、‌'name'和'all'
        scattermode: "overlay",
        title: this.ruleForm2.titleName,  // 是否显示标题
        scattergap: 0.8,
        violingap: 0,
        violingroupgap: 0,
        yaxis: {
          // zeroline: true,  // 是否显示X轴
          zeroline: this.ruleForm2.Xshow,  // 是否显示X轴
          color: this.ruleForm2.axisColor,  // 坐标轴颜色
          showticklabels: this.ruleForm2.showticklabels, // 是否显示刻度标记
          showgrid: false,
          showline: this.ruleForm2.Yshow, // 是否显示Y轴
        },
        xaxis: { title: '' },
        xaxis2: {
          showgrid: false,
          // title: { text: '' }, // 第二个x轴的标题
          overlaying: 'x', // 指定这是第二个x轴，并且它应该覆盖第一个x轴
          // side: 'top', // 将第二个x轴放置在图表的顶部
          showticklabels: false,
          visible: false
        },
      };
      this.layout3 = {
        grid: {
          rows: 1,
          columns: 1,
          pattern: 'independent',
        },
        // y: 0.5,
        showlegend: false, // 设置不显示图例
        hovermode: this.ruleForm3.hovermode,  // 隐藏悬浮显示
        hoverinfo: 'none', //'x'、‌'y'、‌'text'、‌'name'和'all'
        scattermode: "overlay",
        title: this.ruleForm3.titleName,  // 是否显示标题
        scattergap: 0.8,
        violingap: 0,
        violingroupgap: 0,
        yaxis: {
          // zeroline: true,  // 是否显示X轴
          zeroline: this.ruleForm3.Xshow,  // 是否显示X轴
          color: this.ruleForm3.axisColor,  // 坐标轴颜色
          showticklabels: this.ruleForm3.showticklabels, // 是否显示刻度标记
          showgrid: false,
          showline: this.ruleForm3.Yshow, // 是否显示Y轴
        },
        xaxis: { title: '' },
        xaxis2: {
          showgrid: false,
          // title: { text: '' }, // 第二个x轴的标题
          overlaying: 'x', // 指定这是第二个x轴，并且它应该覆盖第一个x轴
          // side: 'top', // 将第二个x轴放置在图表的顶部
          showticklabels: false,
          visible: false
        },
      };
      this.layout4 = {
        grid: {
          rows: 1,
          columns: 1,
          pattern: 'independent',
        },
        // y: 0.5,
        showlegend: false, // 设置不显示图例
        hovermode: this.ruleForm4.hovermode,  // 隐藏悬浮显示
        hoverinfo: 'none', //'x'、‌'y'、‌'text'、‌'name'和'all'
        scattermode: "overlay",
        title: this.ruleForm4.titleName,  // 是否显示标题
        scattergap: 0.8,
        violingap: 0,
        violingroupgap: 0,
        yaxis: {
          // zeroline: true,  // 是否显示X轴
          zeroline: this.ruleForm4.Xshow,  // 是否显示X轴
          color: this.ruleForm4.axisColor,  // 坐标轴颜色
          showticklabels: this.ruleForm4.showticklabels, // 是否显示刻度标记
          showgrid: false,
          showline: this.ruleForm4.Yshow, // 是否显示Y轴
        },
        xaxis: { title: '' },
        xaxis2: {
          showgrid: false,
          // title: { text: '' }, // 第二个x轴的标题
          overlaying: 'x', // 指定这是第二个x轴，并且它应该覆盖第一个x轴
          // side: 'top', // 将第二个x轴放置在图表的顶部
          showticklabels: false,
          visible: false
        },
      };
      this.config1 = {
        displayModeBar: false,
      }
      this.config2 = {
        displayModeBar: false,
      }
      this.config3 = {
        displayModeBar: false,
      }
      this.config4 = {
        displayModeBar: false,
      }
      if (this.ruleForm1.titleShow) { //显示标题
        this.layout1.title = this.ruleForm1.titleName
      } else {
        delete this.layout1.title
      }
      if (this.ruleForm2.titleShow) { //显示标题
        this.layout2.title = this.ruleForm2.titleName
      } else {
        delete this.layout2.title
      }
      if (this.ruleForm3.titleShow) { //显示标题
        this.layout3.title = this.ruleForm3.titleName
      } else {
        delete this.layout3.title
      }
      if (this.ruleForm4.titleShow) { //显示标题
        this.layout4.title = this.ruleForm4.titleName
      } else {
        delete this.layout4.title
      }
      Plotly.newPlot("myDiv1", traces1, this.layout1, this.config1)
      Plotly.newPlot("myDiv2", traces2, this.layout2, this.config2)
      if (this.formTop.mt) {
        Plotly.newPlot("myDiv3", traces3, this.layout3, this.config3)
      }
      if (this.formTop.pt) {
        Plotly.newPlot("myDiv4", traces4, this.layout4, this.config4)
      }

    },
    init2() {
      // 准备数据
      const traces5 = [{
        type: 'violin',
        y: this.parentMsg.data2.nCount_RNA,
        name: '',
        line: {
          color: this.ruleForm5.violinColor
        },
      }]
      const traces6 = [{
        type: 'violin',
        y: this.parentMsg.data2.nFeature_RNA,
        name: '',
        line: {
          color: this.ruleForm6.violinColor
        },
      }]
      const traces7 = [{
        type: 'violin',
        y: this.parentMsg.data2.percent_mt,
        name: '',
        line: {
          color: this.ruleForm7.violinColor
        },
      }]
      const traces8 = [{
        type: 'violin',
        y: this.parentMsg.data2.percent_pt,
        name: '',
        line: {
          color: this.ruleForm8.violinColor
        },
      }]
      traces5.push({
        y: this.parentMsg.data2.nCount_RNA,
        name: "nCount_RNA",
        type: "scatter",
        mode: "markers",
        xaxis: 'x2', // 指定使用第二个x轴
        marker: {
          size: this.ruleForm5.plotSize, // 散点大小
          color: this.ruleForm5.plotColor,// 散点颜色
        },
      });
      traces6.push({
        y: this.parentMsg.data2.nFeature_RNA,
        name: "nFeature_RNA",
        type: "scatter",
        mode: "markers",
        xaxis: 'x2', // 指定使用第二个x轴
        marker: {
          size: this.ruleForm6.plotSize, // 散点大小
          color: this.ruleForm6.plotColor,// 散点颜色
        },
      });
      traces7.push({
        y: this.parentMsg.data2.percent_mt,
        name: "percent.mt",
        type: "scatter",
        mode: "markers",
        xaxis: 'x2', // 指定使用第二个x轴
        marker: {
          size: this.ruleForm7.plotSize, // 散点大小
          color: this.ruleForm7.plotColor,// 散点颜色
        },
      });
      traces8.push({
        y: this.parentMsg.data2.percent_pt,
        name: "percent.pt",
        type: "scatter",
        mode: "markers",
        xaxis: 'x2', // 指定使用第二个x轴
        marker: {
          size: this.ruleForm8.plotSize, // 散点大小
          color: this.ruleForm8.plotColor,// 散点颜色
        },
      });
      this.layout5 = {
        grid: {
          rows: 1,
          columns: 1,
          pattern: 'independent',
        },
        // y: 0.5,
        showlegend: false, // 设置不显示图例
        hovermode: this.ruleForm5.hovermode,  // 隐藏悬浮显示
        hoverinfo: 'none', //'x'、‌'y'、‌'text'、‌'name'和'all'
        scattermode: "overlay",
        title: this.ruleForm5.titleName,  // 是否显示标题
        scattergap: 0.8,
        violingap: 0,
        violingroupgap: 0,
        yaxis: {
          // zeroline: true,  // 是否显示X轴
          zeroline: this.ruleForm5.Xshow,  // 是否显示X轴
          color: this.ruleForm5.axisColor,  // 坐标轴颜色
          showticklabels: this.ruleForm5.showticklabels, // 是否显示刻度标记
          showgrid: false,
          showline: this.ruleForm5.Yshow, // 是否显示Y轴
        },
        xaxis: { title: '' },
        xaxis2: {
          showgrid: false,
          // title: { text: '' }, // 第二个x轴的标题
          overlaying: 'x', // 指定这是第二个x轴，并且它应该覆盖第一个x轴
          // side: 'top', // 将第二个x轴放置在图表的顶部
          showticklabels: false,
          visible: false
        },
      };
      this.layout6 = {
        grid: {
          rows: 1,
          columns: 1,
          pattern: 'independent',
        },
        // y: 0.5,
        showlegend: false, // 设置不显示图例
        hovermode: this.ruleForm6.hovermode,  // 隐藏悬浮显示
        hoverinfo: 'none', //'x'、‌'y'、‌'text'、‌'name'和'all'
        scattermode: "overlay",
        title: this.ruleForm6.titleName,  // 是否显示标题
        scattergap: 0.8,
        violingap: 0,
        violingroupgap: 0,
        yaxis: {
          // zeroline: true,  // 是否显示X轴
          zeroline: this.ruleForm6.Xshow,  // 是否显示X轴
          color: this.ruleForm6.axisColor,  // 坐标轴颜色
          showticklabels: this.ruleForm6.showticklabels, // 是否显示刻度标记
          showgrid: false,
          showline: this.ruleForm6.Yshow, // 是否显示Y轴
        },
        xaxis: { title: '' },
        xaxis2: {
          showgrid: false,
          // title: { text: '' }, // 第二个x轴的标题
          overlaying: 'x', // 指定这是第二个x轴，并且它应该覆盖第一个x轴
          // side: 'top', // 将第二个x轴放置在图表的顶部
          showticklabels: false,
          visible: false
        },
      };
      this.layout7 = {
        grid: {
          rows: 1,
          columns: 1,
          pattern: 'independent',
        },
        // y: 0.5,
        showlegend: false, // 设置不显示图例
        hovermode: this.ruleForm7.hovermode,  // 隐藏悬浮显示
        hoverinfo: 'none', //'x'、‌'y'、‌'text'、‌'name'和'all'
        scattermode: "overlay",
        title: this.ruleForm7.titleName,  // 是否显示标题
        scattergap: 0.8,
        violingap: 0,
        violingroupgap: 0,
        yaxis: {
          // zeroline: true,  // 是否显示X轴
          zeroline: this.ruleForm7.Xshow,  // 是否显示X轴
          color: this.ruleForm7.axisColor,  // 坐标轴颜色
          showticklabels: this.ruleForm7.showticklabels, // 是否显示刻度标记
          showgrid: false,
          showline: this.ruleForm7.Yshow, // 是否显示Y轴
        },
        xaxis: { title: '' },
        xaxis2: {
          showgrid: false,
          // title: { text: '' }, // 第二个x轴的标题
          overlaying: 'x', // 指定这是第二个x轴，并且它应该覆盖第一个x轴
          // side: 'top', // 将第二个x轴放置在图表的顶部
          showticklabels: false,
          visible: false
        },
      };
      this.layout8 = {
        grid: {
          rows: 1,
          columns: 1,
          pattern: 'independent',
        },
        // y: 0.5,
        showlegend: false, // 设置不显示图例
        hovermode: this.ruleForm8.hovermode,  // 隐藏悬浮显示
        hoverinfo: 'none', //'x'、‌'y'、‌'text'、‌'name'和'all'
        scattermode: "overlay",
        title: this.ruleForm8.titleName,  // 是否显示标题
        scattergap: 0.8,
        violingap: 0,
        violingroupgap: 0,
        yaxis: {
          // zeroline: true,  // 是否显示X轴
          zeroline: this.ruleForm8.Xshow,  // 是否显示X轴
          color: this.ruleForm8.axisColor,  // 坐标轴颜色
          showticklabels: this.ruleForm8.showticklabels, // 是否显示刻度标记
          showgrid: false,
          showline: this.ruleForm8.Yshow, // 是否显示Y轴
        },
        xaxis: { title: '' },
        xaxis2: {
          showgrid: false,
          // title: { text: '' }, // 第二个x轴的标题
          overlaying: 'x', // 指定这是第二个x轴，并且它应该覆盖第一个x轴
          // side: 'top', // 将第二个x轴放置在图表的顶部
          showticklabels: false,
          visible: false
        },
      };
      this.config5 = {
        displayModeBar: false,
      }
      this.config6 = {
        displayModeBar: false,
      }
      this.config7 = {
        displayModeBar: false,
      }
      this.config8 = {
        displayModeBar: false,
      }
      if (this.ruleForm5.titleShow) { //显示标题
        this.layout5.title = this.ruleForm5.titleName
      } else {
        delete this.layout5.title
      }
      if (this.ruleForm6.titleShow) { //显示标题
        this.layout6.title = this.ruleForm6.titleName
      } else {
        delete this.layout6.title
      }
      if (this.ruleForm7.titleShow) { //显示标题
        this.layout7.title = this.ruleForm7.titleName
      } else {
        delete this.layout7.title
      }
      if (this.ruleForm8.titleShow) { //显示标题
        this.layout8.title = this.ruleForm8.titleName
      } else {
        delete this.layout8.title
      }
      Plotly.newPlot("myDiv5", traces5, this.layout5, this.config5)
      Plotly.newPlot("myDiv6", traces6, this.layout6, this.config6)


      if (this.formTop.mt) {
        Plotly.newPlot("myDiv7", traces7, this.layout7, this.config7)
      }
      if (this.formTop.pt) {
        Plotly.newPlot("myDiv8", traces8, this.layout8, this.config8)
      }
    },
    submitForm1(param) {
      this.ruleForm1 = param
      this.init()
      this.ruleForm1.isShowTitle = false
    },
    submitForm2(param) {
      this.ruleForm2 = param
      this.init()
      this.ruleForm2.isShowTitle = false
    },
    submitForm3(param) {
      this.ruleForm3 = param
      this.init()
      this.ruleForm3.isShowTitle = false
    },
    submitForm4(param) {
      this.ruleForm4 = param
      this.init()
      this.ruleForm4.isShowTitle = false
    },
    submitForm5(param) {
      this.ruleForm5 = param
      this.init2()
      this.ruleForm5.isShowTitle = false
    },
    submitForm6(param) {
      this.ruleForm6 = param
      this.init2()
      this.ruleForm6.isShowTitle = false
    },
    submitForm7(param) {
      this.ruleForm7 = param
      this.init2()
      this.ruleForm7.isShowTitle = false
    },
    submitForm8(param) {
      this.ruleForm8 = param
      this.init2()
      this.ruleForm8.isShowTitle = false
    },
    jumpSampleQC() {
      if (this.$route.query.uuid) {
        this.$router.push({
          path: '/DataProcess',
          query: {
            uuid: this.$route.query.uuid,
            id: this.$route.query.id,
            step: this.$route.query.step == 'sample_qc' ? 'data_process' : this.$route.query.step,
            from: this.$route.query.from
          }
        })
      } else {

        analysisCellrangerList({
          uuid: this.parentMsg.uuid,
          email: '', // 
          analysis_name: '',
          source: this.parentMsg.source,
          page: 1,
          page_size: 10
        }).then((res) => {
          if (res.code == 200) {

            this.$router.push({
              path: '/DataProcess',
              query: {
                uuid: this.parentMsg.uuid,
                id: res.data.results[0].id,
                step: res.data.results[0].current_step,
                from: res.data.results[0].source
              }
            })
          }
        })
      }

    },
    handleClick() {

    },
    download() {
      window.open(this.parentMsg.data1.h5ad_file_download, '_blank')
    },
    download2() {
      window.open(this.parentMsg.data2.h5ad_file_download, '_blank')
    },
    chartDownload(refName, idx, name) {
      this.downloadLoading[idx].loading = true
      html2canvas(this.$refs[refName], {
        useCORS: true,
        scale: 2,
        quality: 0.7,
        // 忽略无用节点（主要是这个）
        ignoreElements: e => {
          if (
            e.contains(this.$refs[refName]) ||
            this.$refs[refName].contains(e) ||
            e.tagName === 'STYLE' ||
            e.tagName === 'LINK' ||
            e.getAttribute('data-html2canvas') != null // header里面的样式不能筛掉
          ) {
            return false;
          }
          return true;
        }
      }).then((canvas) => {
        let dataURL = canvas.toDataURL("image/png"); //base64格式的图片 url
        const blobUrl = this.dataURLtoBlob(dataURL); //转化成blob格式的图片 Blob{size:xx,type:xx}
        var fileUrl = URL.createObjectURL(blobUrl); //URL.createObjectURL()创建一个指向File或Blob对象的URL。这个URL可以被用于指定一个HTML标签的href属性

        // 创建a标签下载图片
        var addElement = document.createElement('a')
        addElement.href = fileUrl
        addElement.download = name + ".png"

        document.body.appendChild(addElement)
        addElement.click();
        document.body.removeChild(addElement);
        this.downloadLoading[idx].loading = false
      });
    },
    dataURLtoBlob(dataurl) {
      var arr = dataurl.split(','); //分割为数组，分割到第一个逗号
      let bstr = window.atob(arr[1]);
      let n = bstr.length;
      let u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new Blob([u8arr], { type: "png" });
    }
  }
}
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
