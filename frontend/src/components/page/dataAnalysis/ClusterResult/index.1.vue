<template>
  <div class="ClusterResult">
    <div class="ClusterResult-inner">
      <div class="blast">
        <el-header>Cluster Result</el-header>
        <div :style="{width:'100%',height: 'auto'}" v-loading="umapLoading1">
          <div id="barChart1" ref='barChart1' :style="{width:'100%',height: '600px'}"></div>
        </div>
        <el-button style="margin-top:20px;" class="btnSearch" @click="jumpCellAnnotation">Cell Annotation</el-button>
        <!-- 修改图表配置弹窗 -->
        <el-dialog title="配置修改" :visible.sync="isShowTitle" width="440px" :close-on-click-modal="false">
          <el-tabs v-model="activeName">
            <el-tab-pane label="基本设置" name="first">
              <el-form :model="ruleForm" ref="ruleForm" label-width="100px" class="demo-ruleForm">
                <el-form-item label='标题显示'>
                  <el-switch v-model="ruleForm.title"></el-switch>
                </el-form-item>
                <el-form-item label='标题名称'>
                  <el-input v-model="ruleForm.titleText"></el-input>
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
              <el-form :model="ruleForm" ref="ruleForm" label-width="80px" class="demo-ruleForm">
                <el-form-item label='散点颜色'>
                  <el-color-picker v-for="(item, index) in colorList" @change="colorChange($event, index)" v-model="colorList[index]"></el-color-picker>
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
      </div>
    </div>
  </div>
</template>

<script>
import echarts from 'echarts';

export default {
  name: 'ClusterResult',
  components: {
  },
  props: {
    parentMsg: {
      type: Object
    }
  },
  data() {
    return {
      umapLoading1: false,
      ruleForm: {
        title: true,
        titleText: "UMAP",
        plotSize: 2,
        plotColor: '#ccc',
        Xshow: true,
        Yshow: true,
        axisColor: '#333',
        showticklabels: true
      },
      option1: {},
      activeName: 'first',
      isShowTitle: false,
      colorList: ['#ef8839', '#21c85d', '#fbb02d', '#ff0054', '#ff5400', '#f72585', '#41c1e9', '#7cb518', '#c46cfd', '#4cbcaf'],
      temSaveColor: ['#ef8839', '#21c85d', '#fbb02d', '#ff0054', '#ff5400', '#f72585', '#41c1e9', '#7cb518', '#c46cfd', '#4cbcaf']
    }
  },
  mounted() {
    this.init()
    this.showUMAP()
  },
  methods: {
    colorChange(val, index) {
      this.temSaveColor[index] = val
    },
    init() {
      let that = this
      this.option1 = {
        title: {
          left: 'center',
          text: this.ruleForm.titleText,
          show: this.ruleForm.title
        },
        // color: ['#eb5e28', '#f27f34', '#f9a03f', '#f6b049', '#f3c053', '#a1c349', '#94b33d', '#87a330', '#799431',
        //     '#6a8532', '#ff0000', '#ff8700', '#ffd300', '#deff0a', '#a1ff0a', '#0aff99', '#0aefff', '#147df5', '#580aff', '#be0aff'
        // ],
        // color: ['#ef8839', '#21c85d', '#fbb02d', '#ff0054', '#ff5400', '#f72585', '#41c1e9', '#7cb518', '#c46cfd', '#4cbcaf', '#3f9fe0', '#fb5607', '#8338ec', '#3a86ff', '#ffd23f', '#2ad4ad', '#0ead69', '#427aa1', '#679436'],
        color: this.colorList,
        toolbox: {
          show: true,
          feature: {
            //   dataZoom: {
            //     yAxisIndex: 'none'
            //   },
            //   dataView: { readOnly: false },
            //   magicType: { type: ['line', 'bar'] },
            //   restore: {},
            /*自定义事件,注意:自定义事件必须以my开头*/
            myTool1: {
              show: true,
              title: ' ',
              /*鼠标停留时的提示文字*/
              icon: 'image://' + require('../../../../assets/img/set.png'),
              /*显示图标,必须以image://为开头显示后面是图表的路径*/
              /*点击时触发的事件*/
              onclick: function (e) {
                console.log(that)
                that.isShowTitle = true
                that.temSaveColor = that.colorList
                // 重新渲染，必须词步骤，否则无效果
                // var echartsItem = echarts.init(document.getElementById('barChart1'));
                // echartsItem.setOption(e.getOption());
              }
            },
            saveAsImage: {
              title: ' ',
            },
          }
        },
        legend: {
          data: [],
          top: 'center',
          right: 30,
          orient: 'vertical',
          type: 'scroll',
          formatter: function (name) {
            // if (!name) return '';
            // if (name.length > 5) {
            //     name = name.slice(0, 5) + '...';
            //     return name
            // }
            let strs = name.split(''); //字符串数组
            let str = ''
            for (let i = 0, s; s = strs[i++];) { //遍历字符串数组
              str += s;
              if (!(i % 10)) str += '\n'; //按需要求余
            }
            return str
          },
          textStyle: {
            fontSize: 12
          }
        },
        grid: {
          // top: '3%',
          // left: '3%',
          // right: '28%',
          // bottom: '3%',
          containLabel: true
        },
        tooltip: {
          trigger: 'item',
          axisPointer: {
            type: 'cross'
          },
          formatter: function (params) {
            if (params.value.length > 1) {
              return params.seriesName + ' :<br/>' +
                params.value[0] + ' , ' +
                params.value[1] + '';
            } else {
              return params.seriesName + ' :<br/>' +
                params.name + ' , ' +
                params.value + '';
            }
          },
        },
        xAxis: {
          show: this.ruleForm.Xshow,
          // type: 'value',
          // scale: true,
          splitLine: {
            show: this.ruleForm.showticklabels
          },
          // name: 'umap1',
          // nameLocation: 'center',
          // nameGap: 20,
          // nameTextStyle: {
          //     fontWeight: 'bolder',
          //     fontSize: 16
          // },
          axisLine: {
            // onZero: false
            lineStyle: {
              color: this.ruleForm.axisColor
            }
          }
        },
        yAxis: {
          show: this.ruleForm.Yshow,
          // type: 'value',
          // scale: true,
          splitLine: {
            show: this.ruleForm.showticklabels
          },
          // name: 'umap2',
          // nameLocation: 'center',
          // nameGap: 20,
          // nameTextStyle: {
          //     fontWeight: 'bolder',
          //     fontSize: 16
          // },
          axisLine: {
            // onZero: false,
            lineStyle: {
              color: this.ruleForm.axisColor
            }
          }
        },
        series: []
      }
    },
    submitForm() {
      this.colorList = this.temSaveColor
      this.init()
      this.option1.legend.data = []
      this.option1.series = []
      this.parentMsg.result_data.forEach(item => {
        this.option1.series.push({
          symbolSize: this.ruleForm.plotSize,
          name: item.sort,
          type: 'scatter',
          data: item.data,
        })
        this.option1.legend.data.push(item.sort.toString())
      });
      this.Echarts = echarts.init(barChart1);
      this.Echarts.setOption(this.option1, true)
      this.isShowTitle = false
    },
    showUMAP() {
      let barChart1 = this.$refs.barChart1
      this.umapLoading1 = true
      if (barChart1) {
        this.option1.legend.data = []
        this.option1.series = []
        this.parentMsg.result_data.forEach(item => {
          this.option1.series.push({
            symbolSize: this.ruleForm.plotSize,
            name: item.sort,
            type: 'scatter',
            data: item.data,
          })
          this.option1.legend.data.push(item.sort.toString())
        });
      }
      this.Echarts = echarts.init(barChart1);
      this.Echarts.setOption(this.option1, true)
      this.umapLoading1 = false
    },
    jumpCellAnnotation() {
      this.$router.push({
        path: '/DataAnalysisCellAnnotation',
        query: {
          uuid: this.$route.query.uuid,
          id: this.$route.query.id,
          step: this.$route.query.step == 'cluster' ? 'cell_annotation' : this.$route.query.step,
          from: this.$route.query.from,
        }
      })
    }
  }
}
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
