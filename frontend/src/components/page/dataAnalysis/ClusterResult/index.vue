<template>
  <div class="ClusterResult">
    <div class="ClusterResult-inner">
      <div class="blast">
        <el-header>Cluster Result</el-header>
        <div :style="{width:'100%',height: 'auto'}" v-loading="umapLoading1">
          <div id="barChart1" ref='barChart1' :style="{width:'100%',height: '600px'}"></div>
        </div>
        <el-button style="margin-top:20px;" class="btnSearch" @click="jumpCellAnnotation">Next</el-button>
        <!-- 修改图表配置弹窗 -->
        <el-dialog title="Configuration" :visible.sync="isShowTitle" width="440px" :close-on-click-modal="false">
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
                <el-form-item label='Scatter size'>
                  <el-input-number v-model="ruleForm.plotSize" :min="1" :max="10"></el-input-number>
                </el-form-item>
                <el-form-item label='Color scheme'>
                  <el-select ref="colorSelect" placeholder="" v-model="myColor" style="width: 100%" @change="handleChange">
                    <el-option v-for="(item, index) in colorList" :key="index" label=" " :value="item">
                      <div v-if="cellType[i]" v-for="(color, i) in item" :style="{backgroundColor:color,width: '5.6%',marginRight:'1%',height: '80%',float: 'left'}"></div>
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label='Scatter color'>
                  <div v-for="(item, index) in colorList[0]">
                    <span v-if='cellType[index]'>{{cellType[index]}}</span>
                    <div class="psfa" v-if='cellType[index]'>
                      <el-color-picker @change="colorChange($event, index)" v-model="temSaveColor[index]"></el-color-picker>
                      <span>{{temSaveColor[index]}}</span>
                    </div>
                  </div>
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
        showticklabels: true,
        xName: 'UMAP_1',
        yName: 'UMAP_2',
        textColor: '#333',
        textFontsize: 16,
        axisLineTick: true,
        showLegend: true,
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
      colorList: [
        ['#007A87', '#2B9CA0', '#7CB3B0', '#A5C6BB', '#DCE9E2', '#FFF6ED', '#F4DCC0', '#C7A47E', '#7B684A', '#332D15', '#304047', '#326659', '#5EA69B', '#C0CFA4', '#A2789C'],
        ['#12467F', '#317CB6', '#6EADD0', '#B8D8E5', '#E8F4F4', '#FAE4D7', '#F7B092', '#DE7059', '#B52330', '#6F011C', '#F4A460', '#5E2612', '#C76114', '#BC8F8F', '#FFD700'],
        ['#E5E5E5', '#479E9B', '#EE4A25', '#DD5F60', '#4169B2', '#FFA54F', '#DD5F60', '#FDDC7B', '#A087B2', '#27408B', '#ACCDDC', '#E5E5E5', '#479E9B', '#EE4A25', '#DD5F60'],
        ['#AD964A', '#DBE5CA', '#5B8361', '#CEE89E', '#7E7E7C', '#F6768D', '#FBA3A2', '#FDDAC4', '#25A4CF', '#B4C6AC', '#F9C269', '#AD964A', '#DBE5CA', '#5B8361', '#CEE89E'],
        ['#E5E5E5', '#ACCDDC', '#8B5A2B', '#CD853F', '#FFA54F', '#117777', '#44AAAA', '#77CCCC', '#771155', '#AA4488', '#CC99BB', '#8B8B00', '#CDCD00', '#FAD23F', '#E5E5E5'],
        ['#007A87', '#2EA4CA', '#DEA85E', '#A3212B', '#EE4A25', '#C76114', '#308014', '#3459A9', '#AD964A', '#77B17B', '#FFD700', '#6A5ACD', '#DA70D6', '#DDA0DD', '#CDCD00'],
        ['#DDA0DD', '#DA70D6', '#A066D3', '#872657', '#FFC0CB', '#0000FF', '#3D59AB', '#1E90FF', '#03A89E', '#191970', '#33A1C9', '#20BA87', '#4169E1', '#6A5ACD', '#00FFFF'],
      ],
      // colorList: ['#ef8839', '#21c85d', '#fbb02d', '#ff0054', '#ff5400', '#f72585', '#41c1e9', '#7cb518', '#c46cfd', '#4cbcaf'],
      temSaveColor: ['#007A87', '#2B9CA0', '#7CB3B0', '#A5C6BB', '#DCE9E2', '#FFF6ED', '#F4DCC0', '#C7A47E', '#7B684A', '#332D15', '#304047', '#326659', '#5EA69B', '#C0CFA4', '#A2789C'],
      activeNames: ['1'],
      isShowDownload: false,
      myColor: ['#007A87', '#2B9CA0', '#7CB3B0', '#A5C6BB', '#DCE9E2', '#FFF6ED', '#F4DCC0', '#C7A47E', '#7B684A', '#332D15', '#304047', '#326659', '#5EA69B', '#C0CFA4', '#A2789C'],
      cellType: []
    }
  },
  mounted() {
    this.init()
    this.showUMAP()
  },
  methods: {
    //设置颜色选择框中颜色
    setSelectColor(colors) {
      let color = colors.slice(0, this.cellType.length)
      //通过操作dom节点改变样式
      this.$nextTick(() => {
        let dom = this.$refs.colorSelect;
        if (dom) {
          dom = dom.$el.children[0];
          let inputDom = dom.querySelectorAll(".el-input__inner");
          let icon = dom.querySelectorAll(".el-input__icon");
          // inputDom[0].style["background-color"] = color;
          inputDom[0].style["background"] = `linear-gradient(to right, ${color[0] || '#fff'} 0 6%, ${color[1] || '#fff'} 6% 12%, ${color[2] || '#fff'} 12% 18%, ${color[3] || '#fff'} 18% 24%, ${color[4] || '#fff'} 24% 30%, ${color[5] || '#fff'} 30% 36%, ${color[6] || '#fff'} 36% 42%, ${color[7] || '#fff'} 42% 48%, ${color[8] || '#fff'} 48% 54%, ${color[9] || '#fff'} 54% 60%, ${color[10] || '#fff'} 60% 66%, ${color[11] || '#fff'} 66% 72%, ${color[12] || '#fff'} 72% 78%, ${color[13] || '#fff'} 78% 84%, ${color[14] || '#fff'} 84% 90%, #fff 90% 100%)`;
          // inputDom[0].style["background"] = `linear-gradient(to right, ${color[0]} 0 6.6%, ${color[1]} 6.6% 13.2%, ${color[2]} 13.2% 19.8%, ${color[3]} 19.8% 26.4%, ${color[4]} 26.4% 33%, ${color[5]} 33% 39.6%, ${color[6]} 39.6% 46.2%, ${color[7]} 46.2% 52.8%, ${color[8]} 52.8% 59.4%, ${color[9]} 59.4% 66%, ${color[10]} 66% 72.6%, ${color[11]} 72.6% 79.2%, ${color[12]} 79.2% 85.8%, ${color[13]} 85.8% 92.4%, ${color[14]} 92.4% 99%, #fff 99% 100%)`;
          icon[0].style["color"] = "black";
        }
      })
    },
    handleChange(val) {
      this.setSelectColor(val);
      this.temSaveColor = val
      //触发update事件更新父组件绑定值
      // this.$emit('update', val);
    },
    colorChange(val, index) {
      this.temSaveColor[index] = val
      this.setSelectColor(this.temSaveColor);
    },
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
        // color: ['#ef8839', '#21c85d', '#fbb02d', '#ff0054', '#ff5400', '#f72585', '#41c1e9', '#7cb518', '#c46cfd', '#4cbcaf', '#3f9fe0', '#fb5607', '#8338ec', '#3a86ff', '#ffd23f', '#2ad4ad', '#0ead69', '#427aa1', '#679436'],
        color: this.temSaveColor,
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
                that.setSelectColor(that.temSaveColor);
                // that.temSaveColor = that.myColor
                // that.setSelectColor(that.myColor);
                // that.temSaveColor = that.myColor
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
            //   title: ' ',
            // },
          }
        },
        legend: {
          show: this.ruleForm.showLegend,
          itemWidth: this.ruleForm.legendSize,
          itemHeight: this.ruleForm.legendSize,
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
      // this.myColor = this.temSaveColor
      this.option1.color = this.temSaveColor
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
      this.cellType = this.option1.legend.data
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
        this.parentMsg.result_data.forEach((item, index) => {
          this.option1.series.push({
            symbolSize: this.ruleForm.plotSize,
            name: item.sort,
            type: 'scatter',
            data: item.data,
          })
          this.option1.legend.data.push(item.sort.toString())
        });
        this.cellType = this.option1.legend.data
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
    },
    downloadChart() {
      const img = new Image();
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
          link.download = this.ruleForm.titleText || 'UMAP'
          link.href = canvas.toDataURL("image/" + this.ruleForm.imgType, 0.9);
          document.body.appendChild(link);
          link.click();
          link.remove();
        }
      };
      this.isShowDownload = false
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
