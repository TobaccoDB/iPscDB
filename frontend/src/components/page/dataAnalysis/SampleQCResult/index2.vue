<template>
  <div class="SampleQCResult">
    <div class="SampleQCResult-inner">
      <div class="blast">
        <el-header>Sample QC Result</el-header>
        <el-tabs type="border-card">
          <el-tab-pane label="Data1">
            <p class="title1">Cells uploaded</p>
            <div style="" class="UMAP">
              <img src='http://47.96.22.63/Sample_QC/qc_picture/example.svg' width="100%" />
            </div>
            <el-button type="text" icon="el-icon-edit" @click="editChart">redact</el-button>
            <div id="myDiv" style="width: 300px; height: 400px"></div>
            <div id="nCount_RNA_plot" style="width: 600px; height: 400px;"></div>
            <ul class="scsa_bottom_ul" style="position:relative;top:-42px;background:#fff;padding-top:30px;">
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
            <el-button type="text" class="textBtn" icon="el-icon-download">h5ad</el-button>
          </el-tab-pane>
          <el-tab-pane label="Data2">Data2</el-tab-pane>
        </el-tabs>
        <!-- 修改图表配置弹窗 -->
        <el-dialog title="配置修改" :visible.sync="isShowTitle" width="400px" v-dialogDrag :close-on-click-modal="false">
          <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="基本设置" name="first">
              <el-form :model="ruleForm" ref="ruleForm" label-width="95px" class="demo-ruleForm">
                <el-form-item label='标题名称'>
                  <el-input v-model="ruleForm.titleName"></el-input>
                </el-form-item>
                <el-form-item label='标题显示'>
                  <el-switch v-model="ruleForm.titleShow"></el-switch>
                </el-form-item>
                <el-form-item label='X轴显示'>
                  <el-switch v-model="ruleForm.Xshow"></el-switch>
                </el-form-item>
                <el-form-item label='Y轴显示'>
                  <el-switch v-model="ruleForm.Yshow"></el-switch>
                </el-form-item>
                <el-form-item label='坐标轴颜色'>
                  <el-color-picker v-model="ruleForm.axisColor"></el-color-picker>
                </el-form-item>
                <el-form-item label='刻度标记'>
                  <el-switch v-model="ruleForm.showticklabels"></el-switch>
                </el-form-item>
              </el-form>
            </el-tab-pane>
            <el-tab-pane label="图形设置" name="second">
              <el-form :model="ruleForm" ref="ruleForm" label-width="95px" class="demo-ruleForm">
                <el-form-item label='悬浮显示'>
                  <el-switch v-model="ruleForm.hovermode"></el-switch>
                </el-form-item>
                <el-form-item label='散点颜色'>
                  <el-color-picker v-model="ruleForm.plotColor"></el-color-picker>
                </el-form-item>
                <el-form-item label='小提琴颜色'>
                  <el-color-picker v-model="ruleForm.violinColor"></el-color-picker>
                </el-form-item>
                <el-form-item label='散点大小'>
                  <el-input-number v-model="ruleForm.plotSize" :min="1" :max="10"></el-input-number>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
          <span slot="footer" class="dialog-footer">
            <el-button @click="isShowTitle = false">取 消</el-button>
            <el-button type="primary" @click="submitForm">确 定</el-button>
          </span>
        </el-dialog>
        <el-button style="margin-top:20px;" class="btnSearch" @click="jumpSampleQC">Data process</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { sample_qc } from '@/api/analysis'
import Plotly from 'plotly.js-dist'
import * as echarts from 'echarts'

export default {
  name: 'SampleQCResult',
  components: {
  },
  data() {
    return {
      isShowTitle: false,
      activeName: 'first',
      ruleForm: {
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
      backVal1: '20563',
      backVal2: '1249',
      chartData1: [],
      layout1: {},
      config1: {}
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    editChart() {
      this.isShowTitle = true
    },
    createViolinPlot(divId, data, title) {
      const chartDom = document.getElementById(divId);
      const myChart = echarts.init(chartDom);

      // 准备数据：这里模拟小提琴图，通过上下四分位数来模拟箱线图形态
      const boxData = this.prepareBoxData(data);

      const option = {
        title: {
          text: title
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        yAxis: {
          type: 'value',
          name: 'Value'
        },
        xAxis: {
          type: 'category',
          name: 'Distribution'
        },
        series: [
          // 箱线图（用作小提琴图的轮廓）
          {
            name: 'Violin',
            type: 'boxplot',
            data: [boxData], // 只有一组数据
            boxWidth: [30, 80] // 控制箱线图的宽度
          },
          // 散点图
          {
            name: 'Scatter',
            type: 'scatter',
            data: data.map(value => [value, 0]), // 所有点集中在同一行
            symbolSize: 3, // 点的大小
            itemStyle: {
              color: 'purple'
            },
            jitter: 0.3 // 控制点的散布
          }
        ]
      };

      myChart.setOption(option);
    },
    prepareBoxData(data) {
      data.sort((a, b) => a - b);
      const q1 = this.quantile(data, 0.25);
      const q2 = this.quantile(data, 0.5); // median
      const q3 = this.quantile(data, 0.75);
      const min = data[0];
      const max = data[data.length - 1];
      return [min, q1, q2, q3, max];
    },
    quantile(arr, p) {
      const idx = (arr.length - 1) * p;
      const lower = Math.floor(idx);
      const upper = lower + 1;
      const weight = idx % 1;
      if (upper >= arr.length) return arr[lower];
      return arr[lower] * (1 - weight) + arr[upper] * weight;
    },
    init() {
      sample_qc({
        uuid: '4070cd12-9c9f-eabf-f332-b5adfba8e208',
        data_type: 'data1',
      }).then((res) => {
        if (res.code == 200) {
          this.createViolinPlot('nCount_RNA_plot', res.data.nCount_RNA, 'nCount_RNA');
          // this.isImplement = false
          // 假设从后端获得的数据如下：
          const responseData = {
            // labels: ["nCount_RNA", "nFeature_RNA", "percent.mt", "percent.pt"],
            labels: ["nCount_RNA"],
            datasets: {
              "nCount_RNA": res.data.nCount_RNA,
              // "nFeature_RNA": res.data.nFeature_RNA,
              // "percent.mt": res.data.percent_mt,
              // "percent.pt": res.data.percent_pt
            }
          };

          // 准备数据
          const traces = responseData.labels.map(label => ({
            type: 'violin',
            y: responseData.datasets[label],
            name: label,
            box: {
              visible: true
            },
            line: {
              // color: 'purple'
              color: this.ruleForm.violinColor
            },
            meanline: {
              // visible: true,
              // line: {
              //   color: 'red'
              // }
            },
            marker: {
              color: 'rgba(0, 0, 0, 0.6)',
              size: 3
            },
            // orientation: 'h', // 旋转图形使其水平
            points: 'all', // 添加点图
            jitter: 1, // 控制点的散布
            scattergap: 0.1,
            violingap: 0,
            violingroupgap: 0,
          }));

          // 绘制图表
          Plotly.newPlot('myDiv', traces, {
            title: 'Violin Plots with Scatter Plots',
            yaxis: { title: 'Distribution' },
            xaxis: { title: 'Value' }
          });
        }
      })
      // let x = []
      // let y = []
      // this.chartData1 = [{
      //   y: [65, 465, 838, 442, 492, 4442, 9235],
      //   x: x,
      //   name: 'Greens FC',
      //   marker: {
      //     color: this.ruleForm.violinColor, //小提琴颜色
      //   },
      //   type: 'violin',
      //   fill: 'tozero',
      //   side: 'top', // negative、positive
      //   sizeref: 2
      // }]

      // for (let i = 0; i < 90; i++) {
      //   let arr = [];
      //   for (let j = 0; j < 9; j++) {
      //     let item = Math.floor(Math.random() * 10000 + 1);
      //     arr.push(item);
      //   }
      //   x.push('GSM4626005')
      //   this.chartData1.push({
      //     x: x,
      //     y: arr,
      //     name: "GSM4626005",
      //     type: "scatter",
      //     mode: "markers",
      //     marker: {
      //       size: this.ruleForm.plotSize, // 散点大小
      //       color: this.ruleForm.plotColor,// 散点颜色
      //     },
      //   });
      // }
      // this.layout1 = {
      //   grid: {
      //     rows: 1,
      //     columns: 1,
      //     pattern: 'independent',
      //   },
      //   y: 0.5,
      //   showlegend: false, // 设置不显示图例
      //   hovermode: this.ruleForm.hovermode,  // 隐藏悬浮显示
      //   hoverinfo: 'none', //'x'、‌'y'、‌'text'、‌'name'和'all'
      //   scattermode: "group",
      //   title: this.ruleForm.titleName,  // 是否显示标题
      //   scattergap: 0.1,
      //   violingap: 0,
      //   violingroupgap: 0,
      //   yaxis: {
      //     zeroline: this.ruleForm.Xshow,  // 是否显示X轴
      //     color: this.ruleForm.axisColor,  // 坐标轴颜色
      //     showticklabels: this.ruleForm.showticklabels, // 是否显示刻度标记
      //     showgrid: false,
      //     showline: this.ruleForm.Yshow, // 是否显示Y轴
      //   },
      //   xaxis: {
      //     zeroline: true
      //   }
      // };
      // this.config1 = {
      //   displayModeBar: false,
      // }
      // if (this.ruleForm.titleShow) { //显示标题
      //   this.layout1.title = this.ruleForm.titleName
      // } else {
      //   delete this.layout1.title
      // }
      // console.log(111, this.chartData1)
      // Plotly.newPlot("myDiv", this.chartData1, this.layout1, this.config1)



    },
    submitForm() {
      // this.layout1.title = this.ruleForm.titleName  // 是否显示标题
      // this.layout1.yaxis.zeroline = this.ruleForm.Xshow // 是否显示X轴
      // this.layout1.yaxis.showline = this.ruleForm.Yshow // 是否显示Y轴
      // this.layout1.yaxis.color = this.ruleForm.axisColor // 坐标轴颜色
      // this.layout1.yaxis.showticklabels = this.ruleForm.showticklabels // 刻度标记
      // Plotly.newPlot("myDiv", this.chartData1, this.layout1, this.config1)
      this.init()
      this.isShowTitle = false
      // 重新渲染，必须词步骤，否则无效果
      // this.option1.title.text = this.ruleForm.name
      // this.option1.title.show = this.ruleForm.delivery
      // this.Echarts = echarts.init(barChart1);
      // this.Echarts.setOption(this.option1, true)
      // this.isShowTitle = false
    },
    jumpSampleQC() {
      this.$router.push({
        path: '/DataProcess',
        query: {

        }
      })
    },
    handleClick() {

    },
  }
}
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
