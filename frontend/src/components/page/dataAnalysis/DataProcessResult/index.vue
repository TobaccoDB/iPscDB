<template>
  <div class="DataProcessResult">
    <div class="DataProcessResult-inner">
      <div class="blast">
        <el-header>Data Process Result</el-header>

        <div :style="{width:'100%',height: 'auto'}" v-loading="umapLoading1">
          <div id="barChart1" ref='barChart1' :style="{width:'100%',height: '600px'}"></div>
        </div>
        <el-button style="margin-top:20px;" class="btnSearch" @click="jumpCluster">Next</el-button>
        <!-- 修改图表配置弹窗 -->
        <el-dialog title="Configuration modification" :visible.sync="isShowTitle" width="400px" :close-on-click-modal="false">
          <el-tabs v-model="activeName">
            <el-tab-pane label="Basic Settings" name="first">
              <el-form :model="ruleForm" ref="ruleForm" label-width="110px" class="demo-ruleForm">
                <el-collapse v-model="activeNames" accordion>
                  <el-collapse-item title="Text Style" name="1">
                    <el-form-item label='Title Display'>
                      <el-switch v-model="ruleForm.title"></el-switch>
                    </el-form-item>
                    <el-form-item label='Title Name'>
                      <el-input v-model="ruleForm.titleText"></el-input>
                    </el-form-item>
                    <el-form-item label='Font size'>
                      <el-slider v-model="ruleForm.textFontsize" :min='10' :max="50" show-input></el-slider>
                    </el-form-item>
                    <el-form-item label='Text Style'>
                      <el-color-picker v-model="ruleForm.textColor"></el-color-picker>
                    </el-form-item>
                    <el-form-item label='X-axis Title'>
                      <el-input v-model="ruleForm.xName"></el-input>
                    </el-form-item>
                    <el-form-item label='Y-axis title'>
                      <el-input v-model="ruleForm.yName"></el-input>
                    </el-form-item>
                  </el-collapse-item>
                  <el-collapse-item title="Coordinate axis system" name="2">
                    <el-form-item label='X-axis display'>
                      <el-switch v-model="ruleForm.Xshow"></el-switch>
                    </el-form-item>
                    <el-form-item label='Y-axis display'>
                      <el-switch v-model="ruleForm.Yshow"></el-switch>
                    </el-form-item>
                    <el-form-item label='Axis color'>
                      <el-color-picker v-model="ruleForm.axisColor"></el-color-picker>
                    </el-form-item>
                    <el-form-item label='Grid lines'>
                      <el-switch v-model="ruleForm.showticklabels"></el-switch>
                    </el-form-item>
                    <el-form-item label='Axis scale line'>
                      <el-switch v-model="ruleForm.axisLineTick"></el-switch>
                    </el-form-item>
                  </el-collapse-item>
                  <el-collapse-item title="Legend" name="3">
                    <el-form-item label='Legend display'>
                      <el-switch v-model="ruleForm.showLegend"></el-switch>
                    </el-form-item>
                    <el-form-item label='Legend size'>
                      <el-slider v-model="ruleForm.legendSize" :min='10' :max="50" show-input></el-slider>
                    </el-form-item>
                    <el-form-item label='Font size'>
                      <el-slider v-model="ruleForm.legendFontsize" :min='10' :max="50" show-input></el-slider>
                    </el-form-item>
                    <el-form-item label='Text Style'>
                      <el-color-picker v-model="ruleForm.legendColor"></el-color-picker>
                    </el-form-item>
                  </el-collapse-item>
                </el-collapse>

              </el-form>
            </el-tab-pane>
            <el-tab-pane label="Graphic Settings" name="second">
              <el-form :model="ruleForm" ref="ruleForm" label-width="110px" class="demo-ruleForm">
                <el-form-item label='Scatter color'>
                  <el-color-picker v-model="ruleForm.plotColor"></el-color-picker>
                </el-form-item>
                <el-form-item label='Scatter size'>
                  <el-input-number v-model="ruleForm.plotSize" :min="1" :max="10"></el-input-number>
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
          <span slot="footer" class="dialog-footer">
            <el-button @click="isShowTitle = false">Cancel</el-button>
            <el-button type="primary" @click="submitForm">OK</el-button>
          </span>
        </el-dialog>
        <el-dialog title="Download Settings" :visible.sync="isShowDownload" width="500px" :close-on-click-modal="false">
          <el-form :model="ruleForm" ref="ruleForm" label-width="auto" class="demo-ruleForm">
            <el-form-item label='Proportional locking'>
              <el-switch v-model="ruleForm.lockRatio"></el-switch>
            </el-form-item>
            <el-form-item label='Image size'>
              <!-- <el-slider v-model="ruleForm.imgSize" :min='1' :max="10" show-input></el-slider> -->
              <el-input style="width:130px;" @change="widthChange" v-model="ruleForm.imgWidth">
                <template slot="append">W</template>
              </el-input> X
              <el-input style="width:130px;" @change="heightChange" v-model="ruleForm.imgHeight">
                <template slot="append">H</template>
              </el-input>
            </el-form-item>
            <el-form-item label='Image format'>
              <el-radio v-model="ruleForm.imgType" label="png">png</el-radio>
              <el-radio v-model="ruleForm.imgType" label="jpeg">jpg</el-radio>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="isShowDownload = false">Cancel</el-button>
            <el-button type="primary" @click="downloadChart">OK</el-button>
          </span>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script>
import echarts from 'echarts';

export default {
  name: 'DataProcessResult',
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
        showticklabels: true,
        xName: 'UMAP_1',
        yName: 'UMAP_2',
        textColor: '#333',
        textFontsize: 16,
        axisLineTick: true,
        showLegend: false,
        legendSize: 12,
        legendFontsize: 12,
        legendColor: '#333',
        imgSize: 1,
        imgType: 'png',
        imgWidth: 1200,
        imgHeight: 600,
        lockRatio: true
      },
      option1: {},
      activeName: 'first',
      isShowTitle: false,
      activeNames: ['1'],
      isShowDownload: false
    }
  },
  mounted() {
    this.init()
    this.showUMAP()
  },
  methods: {
    init() {
      let that = this
      this.option1 = {
        title: {
          left: 'center',
          text: this.ruleForm.titleText,
          show: this.ruleForm.title,
          textStyle: {
            color: this.ruleForm.textColor,
            fontSize: this.ruleForm.textFontsize
          }
        },
        // color: ['#eb5e28', '#f27f34', '#f9a03f', '#f6b049', '#f3c053', '#a1c349', '#94b33d', '#87a330', '#799431',
        //     '#6a8532', '#ff0000', '#ff8700', '#ffd300', '#deff0a', '#a1ff0a', '#0aff99', '#0aefff', '#147df5', '#580aff', '#be0aff'
        // ],
        color: ['#ef8839', '#21c85d', '#fbb02d', '#ff0054', '#ff5400', '#f72585', '#41c1e9', '#7cb518', '#c46cfd', '#4cbcaf', '#3f9fe0', '#fb5607', '#8338ec', '#3a86ff', '#ffd23f', '#2ad4ad', '#0ead69', '#427aa1', '#679436'],
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
                // 重新渲染，必须词步骤，否则无效果
                // var echartsItem = echarts.init(document.getElementById('barChart1'));
                // echartsItem.setOption(e.getOption());
              }
            },
            myTool2: {
              show: true,
              title: ' ',
              icon: 'image://' + require('../../../../assets/img/echrtsDownload.png'),
              onclick: function (e) {
                that.isShowDownload = true
              }
            },
            // saveAsImage: {
            //   title: 'jpg',
            //   type: 'jpg'
            // },
          }
        },
        legend: {
          show: this.ruleForm.showLegend,
          data: [],
          top: 'middle',
          right: 'left',
          orient: 'vertical',
          type: 'scroll',
          itemWidth: this.ruleForm.legendSize,
          itemHeight: this.ruleForm.legendSize,
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
            fontSize: this.ruleForm.legendFontsize,
            color: this.ruleForm.legendColor
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
          name: this.ruleForm.xName,
          nameLocation: 'center',
          nameGap: 20,
          nameTextStyle: {
            fontWeight: 'bolder',
            fontSize: this.ruleForm.textFontsize,
            color: this.ruleForm.textColor
          },
          axisLine: {
            // onZero: false
            lineStyle: {
              color: this.ruleForm.axisColor
            }
          },
          axisTick: {
            show: this.ruleForm.axisLineTick
          }
        },
        yAxis: {
          show: this.ruleForm.Yshow,
          // type: 'value',
          // scale: true,
          splitLine: {
            show: this.ruleForm.showticklabels
          },
          name: this.ruleForm.yName,
          nameLocation: 'center',
          nameGap: 20,
          nameTextStyle: {
            fontWeight: 'bolder',
            fontSize: this.ruleForm.textFontsize,
            color: this.ruleForm.textColor
          },
          axisLine: {
            // onZero: false,
            lineStyle: {
              color: this.ruleForm.axisColor
            }
          },
          axisTick: {
            show: this.ruleForm.axisLineTick
          }
        },
        series: []
      }
    },
    submitForm() {
      // 重新渲染，必须词步骤，否则无效果
      // this.option1.title.text = this.ruleForm.titleText
      // this.option1.title.show = this.ruleForm.title
      this.init()
      // this.option1.legend.data = []
      // this.option1.series = []
      // this.poitData.specice_umap_data && this.poitData.specice_umap_data.forEach(item => {
      //   this.species_name1 = item.specie
      //   this.option1.legend.data.push(item.name)
      //   this.option1.series.push({
      //     symbolSize: this.ruleForm.plotSize,
      //     name: item.name,
      //     type: 'scatter',
      //     data: item.data
      //   })
      // })
      this.option1.legend.data = ['1']
      this.option1.series = [{
        symbolSize: this.ruleForm.plotSize,
        name: '1',
        type: 'scatter',
        data: this.parentMsg.result_data,
        itemStyle: {
          normal: {
            color: this.ruleForm.plotColor
          }
        }
      }]
      this.Echarts = echarts.init(barChart1);
      this.Echarts.setOption(this.option1, true)
      this.isShowTitle = false
    },
    showUMAP() {
      let barChart1 = this.$refs.barChart1
      this.umapLoading1 = true
      if (barChart1) {
        this.option1.legend.data = ['1']
        this.option1.series = [{
          symbolSize: this.ruleForm.plotSize,
          name: '1',
          type: 'scatter',
          data: this.parentMsg.result_data,
          itemStyle: {
            normal: {
              color: this.ruleForm.plotColor
            }
          }
        }]
        // this.parentMsg.result_data.forEach(item => {
        // this.species_name1 = item.specie
        // this.option1.legend.data.push(item.name)
        // this.option1.series.push({
        //   symbolSize: this.ruleForm.plotSize,
        //   name: item.name,
        //   type: 'scatter',
        //   data: item.data
        // })
        // })
      }

      this.Echarts = echarts.init(barChart1);
      this.Echarts.setOption(this.option1, true)
      this.umapLoading1 = false
    },
    jumpCluster() {
      this.$router.push({
        path: '/Cluster',
        query: {
          uuid: this.$route.query.uuid,
          id: this.$route.query.id,
          step: this.$route.query.step == 'data_process' ? 'cluster' : this.$route.query.step,
          from: this.$route.query.from
        }
      })
    },
    downloadChart() {
      const img = new Image();
      // let mapChart = this.$echarts.init(document.getElementById("echarts"));
      img.src = this.Echarts.getDataURL({
        type: this.ruleForm.imgType,
        pixelRatio: this.ruleForm.imgSize,
        backgroundColor: '#fff',
      });
      img.onload = () => {
        const canvas = document.createElement("canvas");
        canvas.width = this.ruleForm.imgWidth;
        canvas.height = this.ruleForm.imgHeight;
        const ctx = canvas.getContext("2d");
        if (ctx) {
          ctx.drawImage(img, 0, 0, this.ruleForm.imgWidth, this.ruleForm.imgHeight);
          const link = document.createElement("a");
          // link.download = `业绩柱状图.png`;
          link.download = this.ruleForm.titleText || 'UMAP'
          link.href = canvas.toDataURL("image/" + this.ruleForm.imgType, 0.9);
          document.body.appendChild(link);
          link.click();
          link.remove();
        }
      };
      this.isShowDownload = false

      // // 获取base64图片
      // const chartImgUrl = this.Echarts.getDataURL({
      //   type: this.ruleForm.imgType,
      //   pixelRatio: this.ruleForm.imgSize,
      //   backgroundColor: '#fff',
      // })
      // // 下载base64图片
      // const a = document.createElement('a')
      // document.body.appendChild(a)
      // a.style = 'display: none'
      // a.href = chartImgUrl
      // a.download = this.ruleForm.titleText || 'UMAP'
      // a.click()
      // window.URL.revokeObjectURL(chartImgUrl)
      // this.isShowDownload = false
    },
    widthChange(val) {
      if (this.ruleForm.lockRatio) {
        this.ruleForm.imgHeight = val / 2
      }
    },
    heightChange(val) {
      if (this.ruleForm.lockRatio) {
        this.ruleForm.imgWidth = val * 2
      }
    }
  }
}
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
