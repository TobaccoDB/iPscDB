<template>
  <div class="homepage">
    <!-- <div style="width:100%;height:300px;background:#ccc;">banner
    </div> -->
    <!-- 图片部分 -->
    <div class="homepage_img">

      <el-row :gutter="20">
        <el-col :span="16">
          <div class="homepage_img_left" v-loading="leftLoading" v-show="isShow">
            <div ref='barChart2' id="barChart2" :style="{width:'100%',height: '100%'}"></div>
          </div>
          <div class="homepage_img_left" v-loading="leftLoading" v-show="!isShow">
            <div style="width:100%;height:512px;overflow:hidden;line-height:512px;font-size:12px;color:#999;text-align:center;" v-loading="leftLoading">
              No data
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="homepage_img_right">
            <dl :class="{active:cur==index}" v-for="(item, index) in itemsList" :key="index" @click="imgClick(index)">
              <dt></dt>
              <dd>{{item.name}}</dd>
            </dl>
          </div>
        </el-col>
      </el-row>
    </div>
    <!-- 统计 -->
    <div class="homepage_statistics">
      <div class="statistics_content">
        <div class="homepage_statistics_left">
          <h3>Atlas</h3>
          <div class="sta_left_content" ref="sta_left">
            <ul>
              <li v-for="(item, index) in itemAtlasList" :key="index" :class="`${item.name}_li`">{{item.label.replace(/_/g, ' ')}}</li>
            </ul>
            <dl v-for="(item, index) in AtlasListDetail" :key="index" @click="jumpList(item)" :class="`${item.name}_dlStyle`">
              <dt>{{item.tissue_label}}</dt>
              <dd>Cell types({{item.cell_count}})</dd>
              <dd>samples({{item.sample_count}})</dd>
            </dl>
          </div>
        </div>
        <div class="homepage_statistics_right">
          <h3>Statistics</h3>
          <div class="sta_right_content" :style="{ height: leftHeight + 'px' }">
            <dl v-for="(item, index) in AtlasListRight" :key="index">
              <dt></dt>
              <dd>{{item.value}}</dd>
              <dd>{{item.name}}</dd>
            </dl>
          </div>
        </div>
        <!-- <dl v-for="(item, index) in statisticsList" :key="index">
          <dt>{{item.count}}</dt>
          <dd>{{item.name}}</dd>
        </dl> -->
      </div>
    </div>
    <!-- 文字叙述部分 -->
    <div class="homepage_introduce">
      <div class="introduce_content">
        <el-row :gutter="20">
          <el-col :span="12">
            <dl>
              <dt>Introduction</dt>
              <dd>Single-cell sequencing has revolutionized biological research, and enables the characterization of cell types
                across multiple species, tissues and cells. Recently, there has been an exponential growth in single-cell
                transcriptomic studies for plants. The growing availability of scRNA-seq data offers opportunities for data
                integration to create comprehensive cell atlas and enhance the power of downstream analyses. Integrating
                scRNA-seq studies for specific tissues or specific plant species as consensus reference atlas is highly useful
                and will enhance downstream analyses. However, such specific database, especially for plant research community,
                is still very limited. Here, we tried to develop the Integrated Plant Single-Cell Database (iPscDB), aiming
                to provide a comprehensive and relative accurate atlas of cell integration for different tissues of different
                plants. </dd>
            </dl>
          </el-col>
          <el-col :span="12">
            <dl>
              <dt>Overview</dt>
              <dd>
                iPscDB has already integrated 1,118,601 cells from 182 samples of 9 plants, covering 12 tissues and 6 sequencing platforms.
                The scRNA-seq data from different studies were analyzed and integrated on study, tissue, and species levels
                with a standardized pipeline. iPscDB provides three different levels of atlas for the collected six plant
                species: whole plant level, tissue level and study level. iPscDB is hierarchical and user-friendly and has
                three built-in search engines. Users can browse all data by shortcuts and multiple layers of webpages. The
                integrated atlases can be visualized by UMAP/TSNE and all datasets can be downloaded freely. For quality
                checking of user-own scRNA-seq dataset, Sample QC tool was developed. Except the current available functions,
                we developed more online analysis tools. For example, trajectory visualization for different tissues, supporting
                marker gene visualization for specific clusters selected by users, CellProjection which could map user-own
                scRNA-seq data onto the available atlas.
              </dd>
            </dl>
          </el-col>
        </el-row>
      </div>
    </div>
    <!-- 日志部分 -->
    <div class="homepage_journal">
      <div class="journal_content">
        <el-row :gutter="20">
          <el-col :span="12">
            <dl>
              <dt>Update log</dt>
              <dd>
                <ul>
                  <li v-for="(item, index) in logsList" :key="index">{{item.title}}
                    <span>{{item.updated_at}}</span>
                  </li>
                </ul>
              </dd>
            </dl>
          </el-col>
          <el-col :span="12">
            <dl>
              <dt>Citation</dt>
              <dd>
                <ul>
                  <!-- <li v-for="(item, index) in logsList" :key="index">{{item.content}} -->
                  <li style="text-align: justify;">iPscDB v1.0: a Integrated Plant Single-Cell Database.
                  </li>
                </ul>
              </dd>
            </dl>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
import echarts from 'echarts';
import { statisticsList, option2 } from "./config";
import { cell_home_specie_tissue_count, specie_list, home_count, home_update_logs, home_umap_polt, atlas_tissue_cell_sample_count, species_relation_statistics } from "@/api/api";
// import { home_umap_polt } from "@/api/search";
import Plotly from 'plotly.js-dist-min'
let barChart2 = null
export default {
  name: "homePage",
  components: {
  },
  data() {
    return {
      leftLoading: false,
      option2,
      itemAtlasList: [
        // 'Arabidopsis thaliana',
        // 'Solanum lycopersicum',
        // 'Glycine max',
        // 'Oryza sativa',
        // 'mays',
        // 'Populus',
        // 'peanut'
      ],
      AtlasListDetail: [
        // { name: 'Adipose1', cells: 18, samples: 123 },
        // { name: 'Adipose2', cells: 28, samples: 223 },
        // { name: 'Adipose3', cells: 38, samples: 323 },
        // { name: 'Adipose4', cells: 58, samples: 523 },
        // { name: 'Adipose112321', cells: 18, samples: 123 },
        // { name: 'Adipose24545666', cells: 28, samples: 223 },
        // { name: 'Adi3', cells: 38, samples: 323 },
        // { name: 'Adipos45e4', cells: 58, samples: 523 },
      ],
      AtlasListRight: [
        { name: 'Species', value: 0 },
        { name: 'Tissues', value: 0 },
        { name: 'Atlases', value: 0 },
        { name: 'Samples', value: 0 },
        { name: 'Cells', value: 0 },
      ],
      leftHeight: 420,
      marker_resource: 'Experimental',
      smallList: [
        {
          tissue_type: 'stem',
          cell_type: [],
          cell_type_title: []
        }, {
          tissue_type: 'root',
          cell_type: [],
          cell_type_title: []
        }, {
          tissue_type: 'seed',
          cell_type: [],
          cell_type_title: []
        }, {
          tissue_type: 'leaf',
          cell_type: [],
          cell_type_title: []
        },
        {
          tissue_type: 'flower',
          cell_type: [],
          cell_type_title: []
        }
      ],
      itemsList: [
        { name: 'Arabidopsis thaliana', value: 'Arabidopsis_thaliana' },
        { name: 'Oryza sativa', value: 'Oryza_sativa' },
        { name: 'Zea mays', value: 'Zea_mays' },
        // { name: 'Peanut', value: 'peanut' },

        { name: 'Solanum lycopersicum', value: 'Solanum_lycopersicum' },
        { name: 'Nicotiana attenuate', value: 'Nicotiana_tabacum' },
        { name: 'Populus alba var.pyramidalis', value: 'Popular_alba' },
        // { name: 'Populus alba', value: 'Populus' },
        { name: 'Populus tremula × alba', value: 'Hybrid_poplar' },
        { name: 'Fragaria vesca', value: 'Fragaria_vesca' },
        { name: 'Phalaenopsis aphrodite', value: 'Phalaenopsis_aphrodite' },
        // { name: 'Eggplant', value: 'Eggplant' },
        // { name: 'Cotton', value: 'Cotton' },
      ],
      statisticsList,
      experimental_count: 0,
      transcriptome_count: 0,
      single_cell_count: 0,
      cur: 0, //默认选中第一个
      logsList: [
        {
          content: "",
          title: "iPscDB v1.0 released",
          updated_at: "2023/04/09"
        },
        {
          content: "",
          title: "iPscDB v1.0 Beta Online",
          updated_at: "2023/01/14"
        }
      ],
      visible: true,
      isShow: true
    };
  },
  watch: {
    AtlasListDetail() {
      this.$nextTick(() => {
        this.leftHeight = this.$refs.sta_left.offsetHeight
      });
    }
  },
  mounted() {
    this.init()
    atlas_tissue_cell_sample_count().then(res => {
      if (res.code == 200) {
        if (res.data.length > 0) {

          this.itemAtlasList = []
          this.AtlasListDetail = []
          res.data.forEach((items, index) => {
            items.data.forEach((item, i) => {
              if (item.is_show == '1') {
                // if ((items.name == 'Nicotiana_tabacum' || items.name == 'Popular_alba' || items.name == 'Hybrid_poplar') && item.Tissue == 'WholePlant') {

                // } else {
                this.itemAtlasList[index] = items
                let obj = Object.assign({}, item, { name: items.name })
                this.AtlasListDetail.push(obj)
                // }

              }
            })
          })
          this.itemAtlasList = this.itemAtlasList.filter(Boolean)
        }
      }
    });
    species_relation_statistics().then(res => {
      if (res.code == 200) {
        if (res.data.length > 0) {
          this.AtlasListRight = [
            { name: 'Species', value: res.data[0].Species },
            { name: 'Tissues', value: res.data[0].Tissue },
            { name: 'Atlases', value: res.data[0].Atlas },
            { name: 'Samples', value: res.data[0].Sample },
            { name: 'Cells', value: res.data[0].cells },
          ]
        }
      }
    });
    this.showEcharts('Arabidopsis_thaliana')

  },
  beforeDestory() {
    // echarts.dispose(barChart2);
    barChart2.dispose && barChart2.dispose();
    barChart2 = null;
  },
  methods: {
    init() {
      // this.cell_home_specie_tissue_count()
      // specie_list({}).then(res => {

      // });
      // home_count({}).then(res => {
      //   this.statisticsList[0].count = res.data.species
      //   this.statisticsList[1].count = res.data.tissue_type_count
      //   this.statisticsList[2].count = res.data.cell_type_count
      //   this.statisticsList[3].count = res.data.gene_ids_count
      //   this.statisticsList[4].count = res.data.records_count
      //   this.experimental_count = res.data.experimental_count
      //   this.transcriptome_count = res.data.transcriptome_count
      //   this.single_cell_count = res.data.single_cell_count
      // });
      home_update_logs({}).then(res => {
        this.logsList = res.data.results
      });
    },
    showEcharts(species_name) {
      this.leftLoading = true
      barChart2 = this.$refs.barChart2

      let tissue = 'Root'
      if (species_name == 'Arabidopsis_thaliana') {
        tissue = 'Root'
      } else if (species_name == 'Oryza_sativa') {
        tissue = 'Root'
      } else if (species_name == 'Solanum_lycopersicum') {
        tissue = 'Root'
      } else if (species_name == 'Nicotiana_tabacum') {
        tissue = 'Flower'
      } else if (species_name == 'Zea_mays') {
        tissue = 'Leaf'
      } else if (species_name == 'Popular_alba') {
        tissue = 'Stem'
      } else if (species_name == 'Hybrid_poplar') {
        tissue = 'Shoot'
      } else if (species_name == 'Phalaenopsis_aphrodite') {
        tissue = 'Flower'
      } else if (species_name == 'Fragaria_vesca') {
        tissue = 'Leaf'
      }
      let params = {
        tissue: 'WholePlant',
        // tissue: tissue,
        species_name: species_name
      }
      home_umap_polt(params).then(res => {
        if (res.code == 200) {
          if (res.data.cell_type_data && res.data.cell_type_data.length > 0) {
            this.isShow = true
            // if (barChart2) {
            //   this.option2.legend.data = []
            //   this.option2.series = []
            //   res.data.cell_type_data.forEach(item => {
            //     this.option2.legend.data.push(item.name)
            //     this.option2.series.push({
            //       symbolSize: 2,
            //       name: item.name,
            //       type: 'scattergl',
            //       data: item.data,
            //       large: true,
            //       largeThreshold: 500
            //     })
            //   })
            // }

          } else {
            this.isShow = false
          }
          // this.Echarts = echarts.init(barChart2);
          // this.Echarts.setOption(this.option2, true)


          //scattergl.js
          let plotlyData = [];
          let trace0 = []
          let trace1 = []
          let trace2 = []
          let trace3 = []
          let trace4 = []
          let trace5 = []
          let trace6 = []
          res.data.cell_type_data.forEach(item => {
            let xData = []
            let yData = []
            let size = []
            item.data.forEach(element => {
              xData.push(element[0])
              yData.push(element[1])
              // size.push(10)
            });
            // if (item.name == 'Epidermal cell' || item.name == 'Epidermis') {
            //   let xData = []
            //   let yData = []
            //   item.data.forEach(element => {
            //     xData.push(element[0])
            //     yData.push(element[1])
            //   });
            //   trace1.push({
            //     type: 'scattergl',  //确定类型为折线图 
            //     mode: 'markers',
            //     name: item.name,
            //     marker: {
            //       size: 3,
            //       // color: 'rgb(31,119,180)',
            //       color: 'rgb(188,189,34)',
            //     },
            //     //轨迹的坐标
            //     x: xData,      //横坐标值  
            //     y: yData  //纵坐标值
            //   })
            // } else if (item.name == 'Lateral root cap' || item.name == 'Lateral root cap/Columella') {
            //   let xData = []
            //   let yData = []
            //   item.data.forEach(element => {
            //     xData.push(element[0])
            //     yData.push(element[1])
            //   });
            //   trace2.push({
            //     type: 'scattergl',  //确定类型为折线图 
            //     mode: 'markers',
            //     name: item.name,
            //     marker: {
            //       size: 3,
            //       color: 'rgb(255,127,14)',
            //     },
            //     //轨迹的坐标
            //     x: xData,      //横坐标值  
            //     y: yData  //纵坐标值
            //   })
            // } else if (item.name == 'Vascular cell' || item.name == 'Vasculature' || item.name == 'Stele') {
            //   let xData = []
            //   let yData = []
            //   item.data.forEach(element => {
            //     xData.push(element[0])
            //     yData.push(element[1])
            //   });
            //   trace3.push({
            //     type: 'scattergl',  //确定类型为折线图 
            //     mode: 'markers',
            //     name: item.name,
            //     marker: {
            //       size: 3,
            //       color: 'rgb(44,160,44)',
            //     },
            //     //轨迹的坐标
            //     x: xData,      //横坐标值  
            //     y: yData  //纵坐标值
            //   })
            // } else if (item.name == 'Phloem parenchyma' || item.name == 'Xylem parenchyma' || item.name == 'Procambium' || item.name == 'Pericycle') {
            //   let xData = []
            //   let yData = []
            //   item.data.forEach(element => {
            //     xData.push(element[0])
            //     yData.push(element[1])
            //   });
            //   trace4.push({
            //     type: 'scattergl',  //确定类型为折线图 
            //     mode: 'markers',
            //     name: item.name,
            //     marker: {
            //       size: 3,
            //       color: 'rgb(214,39,40)',
            //       // color: 'rgb(227,119,194)',
            //     },
            //     //轨迹的坐标
            //     x: xData,      //横坐标值  
            //     y: yData  //纵坐标值
            //   })
            // } else if (item.name == 'Mesophyll' || item.name == 'Mesophyll cell' || item.name == 'Pavement cell' || item.name == 'Shoot endodermis/Mesophyll cell') {
            //   let xData = []
            //   let yData = []
            //   item.data.forEach(element => {
            //     xData.push(element[0])
            //     yData.push(element[1])
            //   });
            //   trace5.push({
            //     type: 'scattergl',  //确定类型为折线图 
            //     mode: 'markers',
            //     name: item.name,
            //     marker: {
            //       size: 3,
            //       color: 'rgb(148,103,189)',
            //     },
            //     //轨迹的坐标
            //     x: xData,      //横坐标值  
            //     y: yData  //纵坐标值
            //   })
            // } else if (item.name == 'Dividing cell' || item.name == 'Proliferating cell' || item.name == 'Quiescent center' || item.name == 'Stem cell niche' || item.name == 'Floral meristem' || item.name == 'Shoot meristematic cell') {
            //   let xData = []
            //   let yData = []
            //   item.data.forEach(element => {
            //     xData.push(element[0])
            //     yData.push(element[1])
            //   });
            //   trace6.push({
            //     type: 'scattergl',  //确定类型为折线图 
            //     mode: 'markers',
            //     name: item.name,
            //     marker: {
            //       size: 3,
            //       color: 'rgb(31,119,180)',
            //       // color: 'rgb(188,189,34)',
            //       // color: 'rgb(140,86,75)',
            //       // 'rgb(23,190,207)'
            //     },
            //     //轨迹的坐标
            //     x: xData,      //横坐标值  
            //     y: yData  //纵坐标值
            //   })
            // } else {
            //   let xData = []
            //   let yData = []
            //   item.data.forEach(element => {
            //     xData.push(element[0])
            //     yData.push(element[1])
            //   });
            //   trace0.push({
            //     type: 'scattergl',  //确定类型为折线图 
            //     mode: 'markers',
            //     name: item.name,
            //     marker: {
            //       size: 3,
            //       color: ['#f00', '#0f0', '#00f'],
            //     },
            //     //轨迹的坐标
            //     x: xData,      //横坐标值  
            //     y: yData  //纵坐标值
            //   })
            // }
            plotlyData.push({
              type: 'scattergl',  //确定类型为折线图 
              mode: 'markers',
              name: item.name,
              marker: {
                size: 3,
              },
              //轨迹的坐标
              x: xData,      //横坐标值  
              y: yData  //纵坐标值
            })
          })

          let layout = {
            // font: {
            //   size: 15,
            //   color: '#000'
            // },
            margin: { "t": 20, "b": 20, "l": 20, "r": 20 }, //饼图边缘距离画布上下左右边界的距离，单位px
            showlegend: true,
            boxmode: 'group',
            legend: {
              font: {
                size: 12,
                color: '#565644'
              },
              itemsizing: 'constant' //trace 和constant两种设置
            }
          }
          // plotlyData = [...trace0, ...trace1, ...trace2, ...trace3, ...trace4, ...trace5, ...trace6]
          plotlyData.forEach(item => {
            if (item.name == 'Atrichoblast') {  // 1
              item.marker.color = '#E5E5E5'
            } else if (item.name == 'Trichoblast') {
              item.marker.color = '#ACCDDC'
            } else if (item.name == 'Hydathode') {  // 2
              item.marker.color = '#8B5A2B'
            } else if (item.name == 'Guard cell') {
              item.marker.color = '#CD853F'
            } else if (item.name == 'Xylem') {
              item.marker.color = '#FFA54F'
            } else if (item.name == 'Cortex') {  // 3
              item.marker.color = '#117777'
            } else if (item.name == 'Root endodermis') {
              item.marker.color = '#44AAAA'
            } else if (item.name == 'Cambium') {
              item.marker.color = '#77CCCC'
            } else if (item.name == 'Companion cell') {  // 4
              item.marker.color = '#771155'
            } else if (item.name == 'Phloem') {
              item.marker.color = '#AA4488'
            } else if (item.name == 'S-phase cell') {
              item.marker.color = '#CC99BB'
            } else if (item.name == 'Senescing cell/stress') {
              item.marker.color = '#8B8B00'
            } else if (item.name == 'Epidermal cell') {  // 5
              item.marker.color = '#FFC535'
            } else if (item.name == 'Epidermis') {
              item.marker.color = '#C1DFA5'
            } else if (item.name == 'Lateral root cap') { // 6
              item.marker.color = '#621E1F'
            } else if (item.name == 'Lateral root cap/Columella') {
              item.marker.color = '#CC4434'
            } else if (item.name == 'Vascular cell') { // 7
              item.marker.color = '#FDBFB4'
            } else if (item.name == 'Vasculature') {
              item.marker.color = '#CF5B44'
            } else if (item.name == 'Stele') {
              item.marker.color = '#F8A6B5'
            } else if (item.name == 'Phloem parenchyma') { // 8
              item.marker.color = '#304047'
            } else if (item.name == 'Xylem parenchyma') {
              item.marker.color = '#326659'
            } else if (item.name == 'Procambium') {
              item.marker.color = '#5EA69B'
            } else if (item.name == 'Pericycle') {
              item.marker.color = '#C0CFA4'
            } else if (item.name == 'Mesophyll') { // 9
              item.marker.color = '#91C953'
            } else if (item.name == 'Mesophyll cell') {
              item.marker.color = '#94B2D7'
            } else if (item.name == 'Pavement cell') {
              item.marker.color = '#2FACC9'
            } else if (item.name == 'Shoot endodermis/Mesophyll cell') {
              item.marker.color = '#356195'
            } else if (item.name == 'Dividing cell') { // 10
              item.marker.color = '#B6D8FE'
            } else if (item.name == 'Proliferating cell') {
              item.marker.color = '#7CACEE'
            } else if (item.name == 'Quiescent center') {
              item.marker.color = '#427DD3'
            } else if (item.name == 'Stem cell niche') {
              item.marker.color = '#81B875'
            } else if (item.name == 'Floral meristem') {
              item.marker.color = '#EFE45E'
            } else if (item.name == 'Shoot meristematic cell') {
              item.marker.color = '#42707D'
            }
          });
          Plotly.newPlot('barChart2', plotlyData, layout);


          this.leftLoading = false
        }
      });
    },
    jumpList(item) { // 跳转列表页
      this.$router.push({
        path: '/searchResult',
        query: {
          Tissue: item.Tissue,
          tissue_label: item.tissue_label,
          cell_count: item.cell_num,
          // cell_count: item.cell_count,
          name: item.name,
          sample_count: item.sample_count
        }
      })

    },
    cell_home_specie_tissue_count(type) {
      let params = {
        species_type: this.itemsList[this.cur].value,
        marker_resource: this.marker_resource,
        tissue_type: type
      }
      cell_home_specie_tissue_count(params).then(res => {
        if (res.code == 200) {
          res.data.forEach(item => {
            if (item.tissue_type == 'stem') {
              if (type == '' || type == undefined) {
                this.smallList[0].cell_type = item.cell_type
              } else {
                this.smallList[0].cell_type_title = item.cell_type
              }
            } else if (item.tissue_type == 'root') {
              if (type == '' || type == undefined) {
                this.smallList[1].cell_type = item.cell_type
              } else {
                this.smallList[1].cell_type_title = item.cell_type
              }
            } else if (item.tissue_type == 'seed') {
              if (type == '' || type == undefined) {
                this.smallList[2].cell_type = item.cell_type
              } else {
                this.smallList[2].cell_type_title = item.cell_type
              }
            } else if (item.tissue_type == 'leaf') {
              if (type == '' || type == undefined) {
                this.smallList[3].cell_type = item.cell_type
              } else {
                this.smallList[3].cell_type_title = item.cell_type
              }
            } else if (item.tissue_type == 'flower') {
              if (type == '' || type == undefined) {
                this.smallList[4].cell_type = item.cell_type
              } else {
                this.smallList[4].cell_type_title = item.cell_type
              }
            }
          });
        }
      });
    },
    imgClick(index) {
      let specieAll = ['Arabidopsis_thaliana', 'Oryza_sativa', 'Zea_mays', 'Solanum_lycopersicum', 'Nicotiana_tabacum', 'Popular_alba', 'Hybrid_poplar', 'Fragaria_vesca', 'Phalaenopsis_aphrodite']
      this.cur = Number(index)
      this.showEcharts(specieAll[this.cur])
      this.smallList = [
        {
          tissue_type: 'stem',
          cell_type: [],
          cell_type_title: []
        }, {
          tissue_type: 'root',
          cell_type: [],
          cell_type_title: []
        }, {
          tissue_type: 'seed',
          cell_type: [],
          cell_type_title: []
        }, {
          tissue_type: 'leaf',
          cell_type: [],
          cell_type_title: []
        },
        {
          tissue_type: 'flower',
          cell_type: [],
          cell_type_title: []
        }
      ]
      if (this.cur == 0 || this.cur == 1 || this.cur == 2 || this.cur == 3 || this.cur == 4 || this.cur == 5 || this.cur == 6) {
        // this.cell_home_specie_tissue_count()
      }
    }
  }
};
</script>


<style lang="scss" scoped>
@import "./style.scss";
</style>
