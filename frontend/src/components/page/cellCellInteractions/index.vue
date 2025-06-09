<template>
  <div class="cellCellInteractions">
    <div class="cellCellInteractions-inner">
      <div class="blast">
        <div class="title_header">Cell-Cell interactions</div>
        <el-form ref="form1" :inline="true" :model="cellCellInteractions_form" :rules="rules">
          <el-form-item label="Specie" prop="species_name">
            <el-select size="large" @change="species_nameChange" v-model="cellCellInteractions_form.species_name" placeholder="Choose">
              <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Tissue" prop="tissue">
            <el-select size="large" @change="tissueChange" v-model="cellCellInteractions_form.tissue" placeholder="Choose">
              <el-option v-for="(item, index) in tissueOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <!-- <el-form-item label="Treatment" prop="gene_id">
            <el-select filterable size="large" v-model="cellCellInteractions_form.gene_id" placeholder="Choose">
              <el-option v-for="item in gene_idOptions" :key="item.label" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item> -->
        </el-form>
        <!-- Expression in cell types -->
        <el-row :gutter="20" v-loading="chartLoading3" style="margin:30px 0;">
          <el-col :span="8" v-if="ExpressionUrl1">
            <div class="homepage_img_left" style="text-align:center;">
              <img style=" max-width: 100%;max-height: 100%;" :src="ExpressionUrl1">
            </div>
          </el-col>
          <el-col :span="8" v-if="ExpressionUrl2">
            <div class="homepage_img_left" style="text-align:center;">
              <img style=" max-width: 100%;max-height: 100%;" :src="ExpressionUrl2">
            </div>
          </el-col>
          <el-col :span="8" v-if="ExpressionUrl3">
            <div class="homepage_img_left" style="text-align:center;">
              <img style=" max-width: 100%;max-height: 100%;" :src="ExpressionUrl3">
            </div>
          </el-col>
          <el-col :span="24" v-if="!ExpressionUrl1">
            <div style="width:100%;height:110px;overflow:hidden;line-height:110px;font-size:14px;color:#999;text-align:center;">
              No Data
            </div>
          </el-col>
        </el-row>

        <!-- 表格 -->
        <el-form ref="form2" :inline="true" :model="table_form">
          <el-form-item label="Interaction" prop="Interaction">
            <el-select size="large" @change="InteractionChange" v-model="table_form.Interaction" placeholder="Choose">
              <el-option v-for="(item, index) in InteractionOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Cell type" prop="Celltype">
            <el-select size="large" clearable v-model="table_form.Celltype" placeholder="Choose">
              <el-option v-for="(item, index) in CelltypeOptions" :key="index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="">
            <el-button type="primary" size="lager" @click="table_formSearch">GO</el-button>
          </el-form-item>
        </el-form>
        <el-row :gutter="20">
          <el-col :span="12">
            <!-- 柱形图 -->
            <div ref='barChartRight1' style="width: 100%;height: 520px;"></div>
          </el-col>
          <el-col :span="12">
            <div style="overflow:hidden;">
              <span style="color:#666;float:left;font-size:14px;line-height:34px;padding-left:200px;">LR-Pairs in {{histogram_cell_type ? histogram_cell_type : 'all cell types'}}</span>
              <el-button type="text" @click="downloadTable" style="color:#0a9daa;float:right;margin-right:20px;font-size:14px;">
                <i class="el-icon-download el-icon--right"></i>Download
              </el-button>
            </div>
            <jg-table :tableData="tableData" :column='column' :loading="tableLoading" :cellstyle="cellstyle" layout="total, prev, pager, next"
              :paginationConfig="paginationConfig" @sortChange="sortChange" @handleCurrentChange="handleCurrentChange" @handleSizeChange="handleSizeChange"
              @handlecell='handlecell'></jg-table>
          </el-col>
        </el-row>

        <el-form ref="form2" :inline="true" :model="cellCellInteractions_form2" style="margin-top:30px;">
          <el-form-item label="Ligand" prop="Ligand">
            <el-autocomplete size="large" clearable v-model="state1" :fetch-suggestions="querySearchAsync1" placeholder="please enter"
              @select="handleSelect1" @blur="LigandBlur"></el-autocomplete>
          </el-form-item>
          <el-form-item label="Receptor" prop="Receptor">
            <el-autocomplete size="large" clearable v-model="state2" @blur="ReceptorBlur" :fetch-suggestions="querySearchAsync2" placeholder="please enter"
              @select="handleSelect2"></el-autocomplete>
          </el-form-item>
          <el-form-item label="">
            <el-button type="primary" size="lager" @click="cellCellInteractions_form2Search">GO</el-button>
          </el-form-item>
        </el-form>
        <div :style="{width:'100%',height: 'auto'}">
          <el-row :gutter="20" v-loading="umapLoading" element-loading-background="#fff">
            <el-col :span="8">
              <div ref='barChart1' v-show="umapHeight == '300px'" :style="{width:'400px',height: '300px'}"></div>
            </el-col>
            <el-col :span="8">
              <div ref='barChart2' v-show="umapHeight == '300px'" :style="{width:'400px',height: '300px'}"></div>
            </el-col>
            <el-col :span="8">
              <div ref='barChart3' v-show="umapHeight == '300px'" :style="{width:'400px',height: '300px'}"></div>
            </el-col>
            <el-col :span="24" v-if="umapHeight == '100px'">
              <div style="width:100%;height:110px;background:#fff;font-size:14px;color:#999;line-height:100px;text-align:center;z-index:100;">
                No Data
              </div>
            </el-col>
          </el-row>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import echarts from 'echarts';
import { cell_iteraction_species_down, cell_iteraction_species_tissue_down, cell_iteraction_png, cross_specie_gene_down, cell_iteraction_gene_expression, cell_iteraction_txt, cell_interactions_ligands_receptors_down, interactions_ligands_receptors_histogram, interactions_ligands_receptors_list, cell_interactions_ligands_receptors_gene_down } from "@/api/api";
import { option1, option2, option3, column, optionRight1 } from "./config";
import jgTable from '@/components/jgTable/index'
export default {
  name: "cellCellInteractions",
  components: {
    jgTable
  },
  data() {
    return {
      option1,
      option2,
      option3,
      optionRight1,
      cellCellInteractions_form: {
        species_name: "Arabidopsis_thaliana",
        tissue: "Root",
        gene_id: "",
      },
      cellCellInteractions_form2: {
        Ligand: "AT3G49780",
        Receptor: 'AT5G40730'
      },
      rules: {
      },
      speciesOptions: [
        // { label: "Arabidopsis thaliana", value: "Arabidopsis_thaliana" },
        // { label: "Oryza sativa", value: "Oryza_sativa" },
        // { label: "Zea mays", value: "Zea_mays" }
      ],
      tissueOptions: [
        // { label: "Root", value: "Root" },
        // { label: "Leaf", value: "Leaf" }
      ],
      gene_idOptions: [],
      CelltypeOptions: [],
      umapHeight: '100px',
      umapLoading: false,
      // Expression in cell types
      chartLoading3: false,
      ExpressionUrl1: '',
      ExpressionUrl2: '',
      ExpressionUrl3: '',
      // 表格
      tableData: [],
      column,
      paginationConfig: {
        page: 1,
        size: 10,
        sizes: [10, 20, 30],
        total: 0
      },
      tableLoading: false,
      option2MinMax: [],
      option3MinMax: [],
      table_form: {
        Interaction: 'Ligands_cell',
        Celltype: 'Stele'
      },
      InteractionOptions: [
        { label: "Ligands", value: "Ligands_cell" },
        { label: "Receptors", value: "Receptors_cell" },
      ],
      // 
      restaurants1: [],
      restaurants2: [],
      state1: 'AT3G49780',
      timeout1: null,
      state2: 'AT5G40730',
      timeout2: null,
      sorted_type: '',
      histogram_cell_type: ''
    };
  },
  mounted() {
    this.init()
    this.showViolin_box_plot()
    this.getTableData()
    this.getBarData()
    this.showUMAP()
  },
  methods: {
    querySearchAsync1(queryString, cb) {
      var restaurants = this.restaurants1;
      var results = queryString ? restaurants.filter(this.createStateFilter1(queryString)) : restaurants;

      clearTimeout(this.timeout);
      this.timeout = setTimeout(() => {
        cb(results);
      }, 300 * Math.random());
    },
    createStateFilter1(queryString) {
      return (state) => {
        return (state.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
      };
    },
    handleSelect1(item) {
      this.state1 = item.value
    },
    querySearchAsync2(queryString, cb) {
      var restaurants = this.restaurants2;
      var results = queryString ? restaurants.filter(this.createStateFilter2(queryString)) : restaurants;

      clearTimeout(this.timeout);
      this.timeout = setTimeout(() => {
        cb(results);
      }, 300 * Math.random());
    },
    createStateFilter2(queryString) {
      return (state) => {
        return (state.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
      };
    },
    handleSelect2(item) {
      this.state2 = item.value
    },
    init() {
      cell_iteraction_species_down().then(res => {
        if (res.code == 200) {
          this.speciesOptions = res.data
        }
      });
      cell_iteraction_species_tissue_down({
        species_name: this.cellCellInteractions_form.species_name
      }).then(res => {
        if (res.code == 200) {
          this.tissueOptions = res.data
        }
      });
      cell_interactions_ligands_receptors_down({
        species_name: this.cellCellInteractions_form.species_name,
        tissue: this.cellCellInteractions_form.tissue,
        ligands_receptors_type: this.table_form.Interaction
      }).then(res => {
        if (res.code == 200) {
          this.CelltypeOptions = res.data
        }
      });
    },
    species_nameChange() {
      // cross_specie_gene_down({ species_name: this.cellCellInteractions_form.species_name }).then(res => {
      //   if (res.code == 200) {
      //     this.cellCellInteractions_form.gene_id = ''
      //     this.gene_idOptions = res.data
      //   }
      // });
      cell_iteraction_species_tissue_down({
        species_name: this.cellCellInteractions_form.species_name
      }).then(res => {
        if (res.code == 200) {
          this.cellCellInteractions_form.tissue = ''
          this.tissueOptions = res.data
        }
      });
      cell_interactions_ligands_receptors_down({
        species_name: this.cellCellInteractions_form.species_name,
        tissue: this.cellCellInteractions_form.tissue,
        ligands_receptors_type: this.table_form.Interaction
      }).then(res => {
        if (res.code == 200) {
          this.table_form.Celltype = res.data[0].value || ''
          this.CelltypeOptions = res.data
          this.showViolin_box_plot()
          this.paginationConfig.page = 1
          this.histogram_cell_type = ''
          this.getBarData()
          this.getTableData()
          this.showUMAP()
        }
      });

    },
    tissueChange() {
      cell_interactions_ligands_receptors_down({
        species_name: this.cellCellInteractions_form.species_name,
        tissue: this.cellCellInteractions_form.tissue,
        ligands_receptors_type: this.table_form.Interaction
      }).then(res => {
        if (res.code == 200) {
          this.table_form.Celltype = res.data[0].value || ''
          this.CelltypeOptions = res.data
          this.showViolin_box_plot()
          this.paginationConfig.page = 1
          this.histogram_cell_type = ''
          this.getBarData()
          this.getTableData()
          this.showUMAP()
        }
      });

    },
    InteractionChange() {
      cell_interactions_ligands_receptors_down({
        species_name: this.cellCellInteractions_form.species_name,
        tissue: this.cellCellInteractions_form.tissue,
        ligands_receptors_type: this.table_form.Interaction
      }).then(res => {
        if (res.code == 200) {
          this.table_form.Celltype = res.data[0].value || ''
          this.CelltypeOptions = res.data
        }
      });
    },
    // UMAP visualization of cell types
    showUMAP() {
      let barChart1 = this.$refs.barChart1
      let barChart2 = this.$refs.barChart2
      let barChart3 = this.$refs.barChart3
      this.umapLoading = true
      cell_iteraction_gene_expression({
        species_name: this.cellCellInteractions_form.species_name,
        tissue: this.cellCellInteractions_form.tissue,
        ligand_gene: this.state1,
        receptor_gene: this.state2,
      }).then(res => {
        if (res.code == 200) {
          if (res.data) {
            this.umapHeight = '300px'
            if (barChart2) {
              this.option2.legend.data = []
              this.option2.series = []
              let option2visualMapData = []
              res.data.species_gene_one_umap_data && res.data.species_gene_one_umap_data.forEach(item => {
                this.option2.legend.data.push(item.name)
                this.option2.series.push({
                  symbolSize: 2,
                  name: item.name,
                  type: 'scatter',
                  data: item.data
                })
                option2visualMapData = [...option2visualMapData, ...item.data]
              })
              this.option2MinMax = []
              option2visualMapData.forEach(item => {
                this.option2MinMax.push(item[2])
              })
            }
            if (barChart1) {
              this.option1.legend.data = []
              this.option1.series = []
              res.data.species_umap_data && res.data.species_umap_data.forEach(item => {
                this.option1.legend.data.push(item.name)
                this.option1.series.push({
                  symbolSize: 2,
                  name: item.name,
                  type: 'scatter',
                  data: item.data
                })
              })
            }
            if (barChart3) {
              this.option3.legend.data = []
              this.option3.series = []
              let option3visualMapData = []
              res.data.species_gene_second_umap_data && res.data.species_gene_second_umap_data.forEach(item => {
                this.option3.legend.data.push(item.name)
                this.option3.series.push({
                  symbolSize: 2,
                  name: item.name,
                  type: 'scatter',
                  data: item.data
                })
                option3visualMapData = [...option3visualMapData, ...item.data]
              })
              this.option3MinMax = []
              option3visualMapData.forEach(item => {
                this.option3MinMax.push(item[2])
              })
            }
          } else {
            this.umapHeight = '100px'
          }
          this.option2.visualMap = {
            show: true,
            top: 'center',
            right: 'left',
            orient: 'vertical',
            min: Number(Math.min.apply(null, this.option2MinMax)),
            max: Number(Math.max.apply(null, this.option2MinMax)) || 1,
            text: [Math.max.apply(null, this.option2MinMax).toString(), Math.min.apply(null, this.option2MinMax).toString()],
            dimension: 2,
            inRange: {
              color: ['#ccc', '#E15457']
            },
            itemGap: 0,
          }
          this.option3.visualMap = {
            show: true,
            top: 'center',
            right: 'left',
            orient: 'vertical',
            min: Number(Math.min.apply(null, this.option3MinMax)),
            max: Number(Math.max.apply(null, this.option3MinMax)) || 1,
            text: [Math.max.apply(null, this.option3MinMax).toString(), Math.min.apply(null, this.option3MinMax).toString()],
            dimension: 2,
            inRange: {
              color: ['#ccc', '#E15457']
            },
            itemGap: 0,
          }
          this.Echarts = echarts.init(barChart1);
          this.Echarts.setOption(this.option1, true)
          this.Echarts = echarts.init(barChart2);
          this.Echarts.setOption(this.option2, true)
          this.Echarts = echarts.init(barChart3);
          this.Echarts.setOption(this.option3, true)
          this.umapLoading = false
        }
      });
    },
    // 第一行三个图
    showViolin_box_plot() {
      let params = {
        species_name: this.cellCellInteractions_form.species_name,
        tissue: this.cellCellInteractions_form.tissue,
        // gene_id: this.cellCellInteractions_form.gene_id
      }
      this.chartLoading3 = true
      cell_iteraction_png(params).then(res => {
        if (res.code == 200) {
          this.ExpressionUrl1 = res.data.cell_iteraction_first_png
          this.ExpressionUrl2 = res.data.cell_iteraction_second_png
          this.ExpressionUrl3 = res.data.cell_iteraction_thired_png

          this.chartLoading3 = false
        }
      });
    },
    // 表格
    getTableData() {
      this.tableLoading = true
      interactions_ligands_receptors_list({
        species_name: this.cellCellInteractions_form.species_name,
        tissue: this.cellCellInteractions_form.tissue,
        ligands_receptors_type: this.table_form.Interaction,
        cell_type: this.table_form.Celltype,
        histogram_cell_type: this.histogram_cell_type,
        sorted_type: this.sorted_type,          //1正排    2：倒排 
        page: this.paginationConfig.page,
        page_size: this.paginationConfig.size
      }).then(res => {
        if (res.code == 200) {
          if (this.table_form.Interaction == 'Ligands_cell') {
            this.column = [{
              key: 'Ligands',
              label: 'Ligands'
            },
            {
              key: 'Receptors',
              label: 'Receptors'
            },
            // {
            //     key: 'Ligands_cell',
            //     label: 'Ligands Cell'
            // },
            {
              key: 'Receptors_cell',
              label: 'Receptors Cell'
            },
            {
              key: 'Ligands_expr',
              label: 'Ligands Expr'
            },
            {
              key: 'Receptors_expr',
              label: 'Receptors Expr'
            },
            {
              key: 'Score',
              label: 'Score',
              sortable: 'custom'
            },
            ]
          } else {
            this.column = [{
              key: 'Ligands',
              label: 'Ligands'
            },
            {
              key: 'Receptors',
              label: 'Receptors'
            },
            {
              key: 'Ligands_cell',
              label: 'Ligands Cell'
            },
            // {
            //     key: 'Receptors_cell',
            //     label: 'Receptors Cell'
            // },
            {
              key: 'Ligands_expr',
              label: 'Ligands Expr'
            },
            {
              key: 'Receptors_expr',
              label: 'Receptors Expr'
            },
            {
              key: 'Score',
              label: 'Score',
              sortable: 'custom'
            },
            ]
          }
          this.tableData = res.data.results
          this.paginationConfig.total = res.data.count
          this.tableLoading = false
        }
      });
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
    cellstyle({ row, column, rowIndex, columnIndex }) {
      if (column.label === 'Ligands' || column.label === 'Receptors') {
        return { color: "#0a9daa", cursor: "pointer" }
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
      if (params.col.label == 'Title') {
        window.open(`${params.row.doi}`, '_blank')
      }
      if (params.col.label == 'Ligands' || params.col.label == 'Receptors') {
        this.state1 = params.row.Ligands
        this.state2 = params.row.Receptors
      }
    },
    downloadTable() {
      cell_iteraction_txt({
        species_name: this.cellCellInteractions_form.species_name,
        tissue: this.cellCellInteractions_form.tissue
      }).then(res => {
        if (res.code == 200) {
          window.open(res.data.cell_iteraction_download_txt, '_blank')
        }
      });
    },
    sortChange(val) {
      if (val.order == "ascending") {
        this.sorted_type = 1
      } else if (val.order == "descending") {
        this.sorted_type = 2
      } else {
        this.sorted_type = ''
      }
      this.getTableData()
    },
    // 新增柱形图
    getBarData() {
      interactions_ligands_receptors_histogram({
        species_name: this.cellCellInteractions_form.species_name,
        tissue: this.cellCellInteractions_form.tissue,
        ligands_receptors_type: this.table_form.Interaction,
        cell_type: this.table_form.Celltype
      }).then(res => {
        if (res.code == 200) {
          let barChartRight1 = this.$refs.barChartRight1
          if (barChartRight1) {
            this.optionRight1.xAxis.data = []
            this.optionRight1.series[0].data = []
            res.data.forEach(item => {
              this.optionRight1.xAxis.data.push(item.label)
              this.optionRight1.series[0].data.push({ name: item.label, value: item.value })
            });

            const color10 = ['#ee724c', '#b69d78', '#4faf51', '#367cb3', '#faa851', '#98cd96', '#ea9352', '#eb5753', '#a8cde1', '#835c96', '#af5d31', '#f5f39a', '#b393c4', '#ee724c', '#b69d78', '#4faf51', '#367cb3', '#faa851', '#98cd96', '#ea9352', '#eb5753', '#a8cde1', '#835c96', '#af5d31', '#f5f39a', '#b393c4', '#ee724c', '#b69d78', '#4faf51', '#367cb3', '#faa851', '#98cd96', '#ea9352', '#eb5753', '#a8cde1', '#835c96', '#af5d31', '#f5f39a', '#b393c4', '#ee724c', '#b69d78', '#4faf51', '#367cb3', '#faa851', '#98cd96', '#ea9352', '#eb5753', '#a8cde1', '#835c96', '#af5d31', '#f5f39a', '#b393c4']
            this.optionRight1.series[0].data.forEach((item, index) => {
              item.itemStyle = {
                color: color10[index],
              }

            })
          }

          this.Echarts = echarts.init(barChartRight1);
          this.Echarts.setOption(this.optionRight1, true)
          this.Echarts.on('click', (event) => {
            this.paginationConfig.page = 1
            this.histogram_cell_type = event.data.name
            this.getTableData()
          });
        }
      });

    },
    cellCellInteractions_form2Search() {
      this.showUMAP()
    },
    table_formSearch() {
      this.getBarData()
      this.paginationConfig.page = 1
      this.histogram_cell_type = ''
      this.getTableData()
    },
    LigandBlur(val) {
      cell_interactions_ligands_receptors_gene_down({
        species_name: this.cellCellInteractions_form.species_name,
        tissue: this.cellCellInteractions_form.tissue,
        ligands_receptors_type: 'Ligands',
        gene_id: this.state1
      }).then(res => {
        if (res.code == 200) {
          this.restaurants2 = res.data
        }
      });
    },
    ReceptorBlur(val) {
      cell_interactions_ligands_receptors_gene_down({
        species_name: this.cellCellInteractions_form.species_name,
        tissue: this.cellCellInteractions_form.tissue,
        ligands_receptors_type: 'Receptors',
        gene_id: this.state2
      }).then(res => {
        if (res.code == 200) {
          this.restaurants1 = res.data
        }
      });
    }
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
