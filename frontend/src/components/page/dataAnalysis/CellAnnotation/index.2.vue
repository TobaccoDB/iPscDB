<template>
  <div class="CellAnnotation">
    <div class="CellAnnotation-inner">
      <div class="stepBar">
        <el-steps :active="stepActive + 1" finish-status="success" :align-center="true">
          <el-step :style="{ cursor: index <= stepActive ? 'pointer' : 'auto' }" @click.native="setpClick(item, index)" :title="item.name"
            v-for="(item, index) in stepList"></el-step>
        </el-steps>
      </div>
      <div class="blast">
        <el-header>CellAnnotation</el-header>
        <div :style="{width:'100%',height: 'auto'}" v-loading="umapLoading1">
          <div id="barChart1" ref='barChart1' :style="{width:'100%',height: '600px'}"></div>
        </div>
        <!-- 修改图表配置弹窗 -->
        <el-dialog title="配置修改" :visible.sync="isShowTitle" width="440px" :close-on-click-modal="false">
          <el-tabs v-model="activeName" @tab-click="handleClick">
            <el-tab-pane label="基本设置" name="first">
              <el-form :model="ruleForm" ref="ruleForm" label-width="100px" class="demo-ruleForm">
                <el-collapse v-model="activeNames" accordion>
                  <el-collapse-item title="文本样式" name="1">
                    <el-form-item label='标题显示'>
                      <el-switch v-model="ruleForm.title"></el-switch>
                    </el-form-item>
                    <el-form-item label='标题名称'>
                      <el-input v-model="ruleForm.titleText"></el-input>
                    </el-form-item>
                    <el-form-item label='字号选择'>
                      <el-slider v-model="ruleForm.textFontsize" :min='10' :max="50" show-input></el-slider>
                    </el-form-item>
                    <el-form-item label='文本样式'>
                      <el-color-picker v-model="ruleForm.textColor"></el-color-picker>
                    </el-form-item>
                    <el-form-item label='X轴标题'>
                      <el-input v-model="ruleForm.xName"></el-input>
                    </el-form-item>
                    <el-form-item label='Y轴标题'>
                      <el-input v-model="ruleForm.yName"></el-input>
                    </el-form-item>
                  </el-collapse-item>
                  <el-collapse-item title="坐标轴系" name="2">
                    <el-form-item label='X轴显示'>
                      <el-switch v-model="ruleForm.Xshow"></el-switch>
                    </el-form-item>
                    <el-form-item label='Y轴显示'>
                      <el-switch v-model="ruleForm.Yshow"></el-switch>
                    </el-form-item>
                    <el-form-item label='坐标轴颜色'>
                      <el-color-picker v-model="ruleForm.axisColor"></el-color-picker>
                    </el-form-item>
                    <el-form-item label='网格线'>
                      <el-switch v-model="ruleForm.showticklabels"></el-switch>
                    </el-form-item>
                    <el-form-item label='轴刻度线'>
                      <el-switch v-model="ruleForm.axisLineTick"></el-switch>
                    </el-form-item>
                  </el-collapse-item>
                  <el-collapse-item title="图例" name="3">
                    <el-form-item label='图例显示'>
                      <el-switch v-model="ruleForm.showLegend"></el-switch>
                    </el-form-item>
                    <el-form-item label='图例尺寸'>
                      <el-slider v-model="ruleForm.legendSize" :min='10' :max="50" show-input></el-slider>
                    </el-form-item>
                    <el-form-item label='字号选择'>
                      <el-slider v-model="ruleForm.legendFontsize" :min='10' :max="50" show-input></el-slider>
                    </el-form-item>
                    <el-form-item label='文本样式'>
                      <el-color-picker v-model="ruleForm.legendColor"></el-color-picker>
                    </el-form-item>
                  </el-collapse-item>
                </el-collapse>
              </el-form>
            </el-tab-pane>
            <el-tab-pane label="图形设置" name="second">
              <el-form :model="ruleForm" ref="ruleForm" label-width="100px" class="demo-ruleForm">
                <el-form-item label='散点颜色'>
                  <el-select ref="colorSelect" placeholder="" v-model="myColor" style="width: 100%" @change="handleChange">
                    <el-option v-for="(item, index) in colorList" :key="index" label=" " :value="item">
                      <div v-for="color in item" :style="{backgroundColor:color,width: '5.6%',marginRight:'1%',height: '80%',float: 'left'}"></div>
                    </el-option>
                  </el-select>
                  <!-- <el-color-picker v-for="(item, index) in colorList" @change="colorChange($event, index)" v-model="colorList[index]"></el-color-picker> -->
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
        <el-dialog title="下载修改" :visible.sync="isShowDownload" width="400px" :close-on-click-modal="false">
          <el-form :model="ruleForm" ref="ruleForm" label-width="auto" class="demo-ruleForm">
            <el-form-item label='比例锁定'>
              <el-switch v-model="ruleForm.lockRatio"></el-switch>
            </el-form-item>
            <el-form-item label='图片尺寸'>
              <el-input style="width:130px;" @change="widthChange" v-model="ruleForm.imgWidth">
                <template slot="append">W</template>
              </el-input> X
              <el-input style="width:130px;" @change="heightChange" v-model="ruleForm.imgHeight">
                <template slot="append">H</template>
              </el-input>
            </el-form-item>
            <el-form-item label='图片格式'>
              <el-radio v-model="ruleForm.imgType" label="png">png</el-radio>
              <el-radio v-model="ruleForm.imgType" label="jpeg">jpg</el-radio>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="isShowDownload = false">取 消</el-button>
            <el-button type="primary" @click="downloadChart">确 定</el-button>
          </span>
        </el-dialog>
        <el-header>All markers
          <el-button @click="download" type="text" style="float:right;font-size:16px;">
            <i class="el-icon-download"></i>download</el-button>
        </el-header>
        <!-- 表格 -->
        <div class="firstTable">
          <jg-table :tableData="tableData" :column="column" :loading="loading" :cellstyle="cellstyle" :paginationConfig="paginationConfig"
            @handleCurrentChange="handleCurrentChange" @handleSizeChange="handleSizeChange" @handlecell="handlecell"></jg-table>
        </div>
        <!-- svg图 -->
        <el-header style="height:40px;margin-top:20px;">Heatmap
          <el-button @click="downloadImg('heatmap_svg')" type="text" style="float:right;font-size:16px;">
            <i class="el-icon-download"></i>download</el-button>
        </el-header>
        <div class="UMAP" ref="imageTofile">
          <img :src="heatmap_svg" width="100%" height="auto">
        </div>
        <el-header style="height:40px;margin-top:20px;">Dotplot
          <el-button @click="downloadImg('dotplot_svg')" type="text" style="float:right;font-size:16px;">
            <i class="el-icon-download"></i>download</el-button>
        </el-header>
        <div class="UMAP" ref="imageTofile">
          <img :src="dotplot_svg" width="100%" height="auto">
        </div>
        <el-header style="height:40px;margin-top:20px;">Tracksplot
          <el-button @click="downloadImg('tracksplot_svg')" type="text" style="float:right;font-size:16px;">
            <i class="el-icon-download"></i>download</el-button>
        </el-header>
        <div class="UMAP" ref="imageTofile">
          <img :src="tracksplot_svg" width="100%" height="auto">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { cell_annotation_result, cluster_result_list } from "@/api/analysis";
import jgTable from '@/components/jgTable/index'
import echarts from 'echarts';
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
        { key: 'group', label: 'Cluster ID', width: 80 },
        { key: 'cell_type', label: 'Cell type' },
        { key: 'names', label: 'Gene name' },
        { key: 'scores', label: 'Scores' },
        { key: 'logfoldchanges', label: 'Logfoldchanges' },
        { key: 'pvals', label: 'Pvals', width: 200 },
        { key: 'pvals_adj', label: 'Pvals adj', width: 200 }
      ],
      paginationConfig: {
        page: 1,
        size: 10,
        sizes: [10, 20, 30],
        total: 0
      },
      loading: false,
      isShowResult: false,
      activeName: 'first',
      ruleForm: {
        title: true,
        titleText: "UMAP",
        plotSize: 2,
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
      geneExpression_form: {
        species_name: "Arabidopsis_thaliana",
        // reference: 'Oryza_sativa',
        tissue: "Root",
        gene_id: "AT5G50850",
      },
      umapLoading1: false,
      isShowTitle: false,
      poitData: {},
      tableUrl: '',
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
      temSaveColor: ['#ef8839', '#21c85d', '#fbb02d', '#ff0054', '#ff5400', '#f72585', '#41c1e9', '#7cb518', '#c46cfd', '#4cbcaf'],
      heatmap_svg: '',
      dotplot_svg: '',
      tracksplot_svg: '',
      // tracksplot_svg: require('@/assets/img/heatmap.svg'),
      stepActive: 4,
      activeNames: ['1'],
      isShowDownload: false,
      myColor: ['#007A87', '#2B9CA0', '#7CB3B0', '#A5C6BB', '#DCE9E2', '#FFF6ED', '#F4DCC0', '#C7A47E', '#7B684A', '#332D15', '#304047', '#326659', '#5EA69B', '#C0CFA4', '#A2789C']
    }
  },
  mounted() {
    if (this.$route.query.from == 'sample_qc') {
      this.stepList = [
        { name: 'Sample QC', link: 'SampleSampleQC', step: 'sample_qc' },
        { name: 'Data Process', link: 'DataProcess', step: 'data_process' },
        { name: 'Cluster', link: 'Cluster', step: 'cluster' },
        { name: 'Cell Annotation', link: 'DataAnalysisCellAnnotation', step: 'cell_annotation' },
      ]
    } else {
      this.stepList = [
        { name: 'Cell Ranger', link: 'CellRanger', step: 'cell_ranger' },
        { name: 'Sample QC', link: 'DataAnalysisSampleQC', step: 'sample_qc' },
        { name: 'Data Process', link: 'DataProcess', step: 'data_process' },
        { name: 'Cluster', link: 'Cluster', step: 'cluster' },
        { name: 'Cell Annotation', link: 'DataAnalysisCellAnnotation', step: 'cell_annotation' },
      ]
    }
    this.stepList.forEach((item, index) => {
      if (this.$route.query.step == item.step) {
        this.stepActive = index
      }
    });
    this.getTableData()
    this.init()
    this.showUMAP()
  },
  methods: {
    //设置颜色选择框中颜色
    setSelectColor(color) {
      //通过操作dom节点改变样式
      this.$nextTick(() => {
        let dom = this.$refs.colorSelect;
        if (dom) {
          dom = dom.$el.children[0];
          let inputDom = dom.querySelectorAll(".el-input__inner");
          let icon = dom.querySelectorAll(".el-input__icon");
          // inputDom[0].style["background-color"] = color;
          inputDom[0].style["background"] = `linear-gradient(to right, ${color[0]} 0 6%, ${color[1]} 6% 12%, ${color[2]} 12% 18%, ${color[3]} 18% 24%, ${color[4]} 24% 30%, ${color[5]} 30% 36%, ${color[6]} 36% 42%, ${color[7]} 42% 48%, ${color[8]} 48% 54%, ${color[9]} 54% 60%, ${color[10]} 60% 66%, ${color[11]} 66% 72%, ${color[12]} 72% 78%, ${color[13]} 78% 84%, ${color[14]} 84% 90%, #fff 90% 100%)`;
          // inputDom[0].style["background"] = `linear-gradient(to right, ${color[0]} 0 6.6%, ${color[1]} 6.6% 13.2%, ${color[2]} 13.2% 19.8%, ${color[3]} 19.8% 26.4%, ${color[4]} 26.4% 33%, ${color[5]} 33% 39.6%, ${color[6]} 39.6% 46.2%, ${color[7]} 46.2% 52.8%, ${color[8]} 52.8% 59.4%, ${color[9]} 59.4% 66%, ${color[10]} 66% 72.6%, ${color[11]} 72.6% 79.2%, ${color[12]} 79.2% 85.8%, ${color[13]} 85.8% 92.4%, ${color[14]} 92.4% 99%, #fff 99% 100%)`;
          icon[0].style["color"] = "black";
        }
      })
    },
    handleChange(val) {
      this.setSelectColor(val);
      //触发update事件更新父组件绑定值
      // this.$emit('update', val);
    },
    colorChange(val, index) {
      this.temSaveColor[index] = val
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
        color: this.myColor,
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
                that.setSelectColor(that.myColor);
                that.temSaveColor = that.myColor
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
          right: 'left',
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
      this.init()
      this.option1.legend.data = []
      this.option1.series = []
      this.poitData && this.poitData.forEach(item => {
        this.species_name1 = item.specie
        this.option1.legend.data.push(item.name)
        this.option1.series.push({
          symbolSize: this.ruleForm.plotSize,
          name: item.name,
          type: 'scatter',
          data: item.data
        })
      })
      this.Echarts = echarts.init(barChart1);
      this.Echarts.setOption(this.option1, true)
      this.isShowTitle = false
    },
    setpClick(item, index) {
      if (index < this.stepActive || index == this.stepActive) {
        this.$router.push({
          path: '/' + item.link,
          query: {
            uuid: this.$route.query.uuid,
            id: this.$route.query.id,
            step: this.$route.query.step,
            from: this.$route.query.from,
          }
        })
        this.isShowResult = false
      }
    },
    // 表格部分
    getTableData() {
      this.loading = true
      cluster_result_list({
        uuid: this.$route.query.uuid,
        page: this.paginationConfig.page,
        page_size: this.paginationConfig.size
      }).then((res) => {
        if (res.code == 200) {
          if (res.data.count) {
            this.tableData = res.data.results
            this.paginationConfig.total = res.data.count
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
    handleClick() {

    },

    // UMAP visualization of cell types
    showUMAP() {
      let barChart1 = this.$refs.barChart1
      this.umapLoading1 = true
      cell_annotation_result({
        uuid: this.$route.query.uuid
      }).then(res => {
        if (res.code == 200) {
          if (res.data.results && res.data.results.length > 0) {
            this.poitData = res.data.results[0].result_data
            if (barChart1) {
              this.option1.legend.data = []
              this.option1.series = []
              res.data.results[0].result_data && res.data.results[0].result_data.forEach(item => {
                this.species_name1 = item.specie
                this.option1.legend.data.push(item.name)
                this.option1.series.push({
                  symbolSize: this.ruleForm.plotSize,
                  name: item.name,
                  type: 'scatter',
                  data: item.data
                })
              })
            }

            this.tableUrl = res.data.results[0].download_cluster_csv
            this.heatmap_svg = res.data.results[0].heatmap_svg
            this.dotplot_svg = res.data.results[0].dotplot_svg
            this.tracksplot_svg = res.data.results[0].tracksplot_svg

          }
          this.Echarts = echarts.init(barChart1);
          this.Echarts.setOption(this.option1, true)
          this.umapLoading1 = false
        }
      });
    },
    download() {
      window.open(this.tableUrl, "_blank");
    },
    downloadImg(name) {
      const link = document.createElement("a"); //自己创建的a标签
      link.href = this[name];
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(imgUrl);
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
