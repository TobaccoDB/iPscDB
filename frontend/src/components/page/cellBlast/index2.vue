<!--
作者: nodebook@qq.com
组件名称: 
-->
<template>
  <div class="cellid">
    <div class="cellidMainTitleInfo">
      <div class="cellidMainTitleInfoMain">
        <span style="font-weight: bold">
          <span style="color: #e6ef82">P</span>lant
          <span style="color: #e6ef82">C</span>ell-
          <span style="color: #e6ef82">B</span>last</span>
        is a BLAST-like toolkit for scRNA-seq data querying and annotation, which was built on a neural network-based generative
        model and a customized cell-to-cell similarity metric.
      </div>
    </div>
    <div class="cellidMain">
      <div class="cellidMainLeft">
        <div class="cellidMainTitle">Input Data</div>
        <div class="cellidMainContent">
          <div class="cellidMainContentName">Input File</div>
          <div class="cellidMainContentFile">
            <p class="file_p">
              <a href="javascript:;" class="file">Choose File
                <input type="file" name="file" ref="file" @change="handleUpdate($event)" />
              </a>
              <span style="font-size: 12px" :title="fileName">{{ fileName }}
              </span>
            </p>
            <i class="el-icon-download pointer" @click="downloadFIle">
              <span>Download Example File</span>
            </i>
          </div>
          <div class="cellidMainContentText">
            Reference Dataset:
          </div>
          <!-- <div class="cellidMainContentDefault">
                        <el-select v-model="fileList.select2" placeholder="Please select Tissue" size="large" style="width: 100%">
                            <el-option v-for="(item, index) in optionsFile2" :key="index" :label="item" :value="item" />
                        </el-select>
                    </div> -->
          <div class="cellidMainContentSelect">
            <div class="cellidMainContentSelectName">Tissue</div>
            <div class="cellidMainContentSelectFile">
              <el-select v-model="fileList.select2" placeholder="Please select Tissue" size="large" style="width: 100%">
                <el-option v-for="(item, index) in optionsFile2" :key="index" :label="item" :value="item" />
              </el-select>
            </div>
          </div>
          <div class="cellidMainContentSelect">
            <div class="cellidMainContentSelectName">Species</div>
            <div class="cellidMainContentSelectFile">
              <el-select v-model="fileList.select1" placeholder="Please select species" @change="changeSpecies" size="large" style="width: 100%">
                <el-option v-for="(item, index) in optionsFile" :key="index" :label="item" :value="item" />
              </el-select>
            </div>
          </div>

          <div class="cellidMainContentButton">
            <el-button type="primary" style="width: 100px" @click="getExampleButton" :loading="form2Loading">Example</el-button>
            <el-button type="primary" style="width: 100px" @click="getData" :loading="form2Loading" :disabled="!fileList.select2 || !fileList.select1">Run</el-button>
          </div>
          <div class="cellidMainContentButton">
            <span>*About 1 minute for each job</span>
          </div>
        </div>
      </div>
      <div class="cellidMainRight">
        <!-- <div class="cellidMainTitle">Result</div> -->
        <template v-if="seep <= 0">
          <div class="cellBlastMainContent">
            <div class="cellBlastMainContentTitle">
              Upload Plant Data For Query or Fetch Previous Results
            </div>
            <div class="cellBlastMainContentName">Note:</div>
            <div class="cellBlastMainContentText">
              ✓ Supported Format of Single-cell Expression Matrix File Includes CSV, h5ad .
            </div>
            <div class="cellBlastMainContentText">
              ✓ CSV Files Should Include Both Cell Names and Gene IDs (e.g. AT1G05260 ，NOT Gene Names Like RCI3).

            </div>
            <div class="cellBlastMainContentText">
              ✓ Gene Expression Matrix Contains UMI Counts or TPM/FPKM, with All Genes Detected.
            </div>
            <div class="cellBlastMainContentText" style="margin-bottom: 10px">
              ✓ The Number of Querying Cells is Currently Limited to 20,000 in the Web Interface.
            </div>
          </div>
        </template>
        <div class="cellidMainRightButton">
          <div>
            <el-button v-if="seep > 0" type="primary" @click="() => {
              seepActive = 1;
            }
              " :plain="seepActive != 1">START</el-button>
            <el-button v-if="seep > 1" type="primary" @click="() => {
              seepActive = 2;
            }
              " :plain="seepActive != 2">HITS</el-button>
            <el-button v-if="seep > 2" type="primary" @click="() => {
              seepActive = 3;
            }
              " :plain="seepActive != 3">PREDICT</el-button>
            <el-button v-if="seep > 3" type="primary" @click="() => {
              seepActive = 4;
            }
              " :plain="seepActive != 4">PREDICTIONS</el-button>
          </div>
          <div>
            <el-button type="danger" v-if="seep > 0" @click="resetAllTitle">RESET ALL</el-button>
          </div>
        </div>
        <div class="cellidMainRightContent" v-show="seepActive == 1">
          <!-- <el-table :data="tableData" border style="width: 100%">
                        <el-table-column prop="Celltype" label="Celltype" align="center"> </el-table-column>
                        <el-table-column prop="cele_name" label="Cell_Name" align="center"> </el-table-column>
                    </el-table>
                    <div class="cell_pages">
                        <el-pagination
                            background
                            hide-on-single-page
                            layout="prev, pager, next"
                            :total="total"
                            :current-page="currentPage"
                            @current-change="
                                (val) => {
                                    currentPage = val
                                }
                            "
                        >
                        </el-pagination>
                    </div> -->
          <div class="cellBlastMainInfo" v-loading="tableLoading1">
            <div class="cellBlastMainInfoItem">
              <span>File Name:</span>
              <span>{{ result1.file_name }}</span>
            </div>
            <div class="cellBlastMainInfoItem">
              <span>File Size:</span>
              <span>{{ result1.file_size }}</span>
            </div>
            <div class="cellBlastMainInfoItem">
              <span>Number of Cells:</span>
              <span>{{ result1.cells_number }}</span>
            </div>
            <div class="cellBlastMainInfoItem">
              <span>Number of Genes:</span>
              <span>{{ result1.genes_number }}</span>
            </div>
          </div>
          <table v-loading="tableLoading1" class="cellidMainRightContentTextTable" border="0" style="
              border-collapse: collapse;
              border: 1px solid #d1d8df;
              text-align: center;
              font-size: 14px;
              margin-bottom: 20px;
            ">
            <thead>
              <tr style="height: 60px; background: #09b07a; color: #fff">
                <th style="width: 200px">
                  <div class="cellidMainRightContentTextTableTop">
                    <span class="cellidMainRightContentTextTableTopRight">Cells</span>
                    <span class="cellidMainRightContentTextTableTopLeft"> {{ column_names.length > 0 ? column_names[0] : "Genes" }}
                    </span>
                    <span class="cellidMainRightContentTextTableTopLine"></span>
                  </div>
                </th>
                <template v-for="(item, index) in column_names">
                  <th style="text-align: center" v-if="index > 0" :key="index">
                    <span class="cellidMainRightContentTextTableHeaderName">{{ item }}</span>
                  </th>
                </template>
              </tr>
            </thead>
            <tbody>
              <tr style="border: 1px solid #d1d8df" v-for="(item, index) in tableData" :key="index">
                <td v-for="(items, indexs) in column_names" :key="indexs">
                  {{ item[items] }}
                </td>
              </tr>
            </tbody>
          </table>
          <div class="cellidMainRightContentFooter2">
            <el-button type="primary" @click="getTable2" v-loading="tableLoading2 || tableLoading1">CONFIRM</el-button>
          </div>
        </div>
        <div class="cellidMainRightContent cellidMainRightContent2" v-show="seepActive == 2">
          <div class="cellidMainRightContent2Left">
            <div class="cellidMainRightContent2LeftName">
              Query Cell Name ({{ tableData2All.length }})
            </div>
            <div class="cellidMainRightContent2LeftList">
              <div class="cellidMainRightContent2LeftListItem" :class="tableDataActive == index
                ? 'cellidMainRightContent2LeftListItemActive'
                : ''
                " v-for="(item, index) in tableData2All" :key="index" @click="tagTable2(item, index)">
                {{ item.query_cell_name }}
              </div>
            </div>
          </div>
          <div class="cellidMainRightContent2Right">
            <el-table :data="tableData2" stripe style="width: 100%" size="mini" border v-loading="tableLoading2" max-height="300">
              <el-table-column prop="Celltype" label="Celltype" width="300" align="center">
              </el-table-column>
              <el-table-column prop="PercentMt" label="Percent.mt" width="160" align="center">
              </el-table-column>
              <el-table-column prop="Seurat_clusters" label="Seurat_clusters" width="160" align="center">
              </el-table-column>
              <el-table-column prop="cid" label="cid" width="180" align="center">
              </el-table-column>
              <el-table-column prop="dist" label="dist" width="120" align="center">
              </el-table-column>
              <el-table-column prop="hits" label="hits" width="120" align="center">
              </el-table-column>
              <el-table-column prop="nCount_RNA" label="nCount_RNA" width="120" align="center">
              </el-table-column>
              <el-table-column prop="nCount_SCT" label="nCount_SCT" width="120" align="center">
              </el-table-column>
              <el-table-column prop="nFeature_RNA" label="nFeature_RNA" width="120" align="center">
              </el-table-column>
              <el-table-column prop="nFeature_SCT" label="nFeature_SCT" width="120" align="center">
              </el-table-column>
              <el-table-column prop="pval" label="pval" width="100" align="center">
              </el-table-column>
              <el-table-column prop="qid" label="qid" width="180" align="center">
              </el-table-column>
              <el-table-column prop="__libsize__" label="__libsize__" width="100" align="center">
              </el-table-column>
            </el-table>
          </div>
        </div>
        <div class="cellidMainRightContentFooter2" v-show="seepActive == 2">
          <el-button type="primary" :disabled="disabled2" @click="getTable3" plain v-loading="tableLoading2">PREDICT</el-button>
          <el-button type="primary" :disabled="!downloadFIle2Url" @click="downloadFIle2" plain v-loading="tableLoading1">DOWNLOAD PREDICTION</el-button>
        </div>
        <div class="cellidMainRightContent" v-show="seepActive == 3">
          <div class="cellBlastMainBlast1">
            <div class="cellBlastMainBlast1Title">Choose Reference Panel</div>
            <div class="cellBlastMainBlast1Item">
              <div class="cellBlastMainBlast1ItemLeft">
                <div class="cellBlastMainBlast1ItemLeftName" title="Features that can be predicted based on significant hits">
                  Predictions:
                </div>
                <div class="cellBlastMainBlast1ItemLeftValue" style="border: none">
                  <el-checkbox v-model="tableForm2.data1">cell_type1</el-checkbox>
                </div>
              </div>
            </div>
            <div class="cellBlastMainBlast1Item">
              <div class="cellBlastMainBlast1ItemLeft">
                <div class="cellBlastMainBlast1ItemLeftName" title="The minimal fraction of majority votes for a confident prediction to be made, otherwise the prediction will be 'ambiguous' (only relevant when predicting discrete features)">
                  Majority Threshold:
                </div>
                <div class="cellBlastMainBlast1ItemLeftValue">
                  <input type="number" v-model="tableForm2.data2" :step="1" />
                </div>
              </div>
            </div>
            <div class="cellBlastMainBlast1Item">
              <div class="cellBlastMainBlast1ItemLeft">
                <div class="cellBlastMainBlast1ItemLeftName" title="Minimal number of significant hits required for a query cell to be accepted for prediction, otherwise the query cell will be rejected">
                  Min Hits:
                </div>
                <div class="cellBlastMainBlast1ItemLeftValue">
                  <input type="number" v-model="tableForm2.data3" />
                </div>
              </div>
            </div>
            <div class="cellBlastMainBlast1Item">
              <div class="cellBlastMainBlast1ItemLeft">
                <div class="cellBlastMainBlast1ItemLeftName" title="Minimal number of significant hits required for a query cell to be accepted for prediction, otherwise the query cell will be rejected">
                  Pval Cutoff:
                </div>
                <div class="cellBlastMainBlast1ItemLeftValue">
                  <input type="number" v-model="tableForm2.data4" />
                </div>
              </div>
              <div class="cellBlastMainBlast1ItemRight">
                <el-button type="danger" plain style="width: 120px" @click="clearBtn">CLEAR</el-button>
              </div>
            </div>
          </div>
          <div class="cellidMainRightContentFooter2">
            <el-button type="primary" @click="tableData3" plain v-loading="tableLoading3">PREDICT</el-button>
          </div>
        </div>
        <div class="cellidMainRightContent" v-show="seepActive == 4">
          <div class="cellidMainRightContent cellidMainRightContentChar" v-loading="form2Loading">
            <div class="cellidMainRightContentCharLeft" ref="cellidMainRightContentCharLeft2"></div>
            <div class="cellidMainRightContentCharRight" ref="cellidMainRightContentCharRight2"></div>
          </div>
          <el-table :data="tableData3List" stripe style="width: 100%; margin-bottom: 20px" size="mini" border v-loading="tableLoading3"
            max-height="700">
            <el-table-column prop="query_cell_name" label="Query_Cell_Name" width="200" align="center">
            </el-table-column>
            <el-table-column prop="cell_type" label="Cell_Type" align="center">
            </el-table-column>
            <el-table-column prop="hits_number" label="Hits_Number" width="100" align="center">
            </el-table-column>
          </el-table>
          <div class="cellidMainRightContentFooter2">
            <el-button type="primary" :disabled="!downloadFIle4Url" @click="downloadFIle4" plain>DOWNLOAD PREDICTION
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  get_train_species,
  get_train_tissue,
  get_cell_blast_data,
  cell_blast_example,
  get_cell_blast_hits,
  get_cell_blast_predictions,
} from "@/api/api";
import * as echarts from "echarts";
export default {
  data() {
    return {
      optionsFile: [],
      optionsFile2: [],
      fileList: {
        select1: "",
        select2: "",
      },
      fileName: "",
      file: null,
      form2Loading: false,
      tableData: [],
      tableDataAll: [],
      total: 0,
      currentPage: 0,
      column_names: [],
      tableLoading1: false,
      result1: {},
      tableLoading2: false,
      tableData2: [],
      tableData2All: [],
      tableDataActive: "",
      tableForm2: {
        data1: true,
        data2: 0.5,
        data3: 2,
        data4: 0.05,
      },
      tableLoading3: false,
      tableData3List: [],
      downloadFIle4Url: null,
      seep: 0,
      seepActive: 0,
      downloadFIle2Url: null,
      errMessage:
        "Sorry, there was an error in the job you submitted. Please confirm the format of the input data and submit it again.",
      disabled2: false,
    };
  },
  methods: {
    clearBtn() {
      this.tableForm2 = {
        data1: true,
        data2: 0.5,
        data3: 2,
        data4: 0.05,
      };
    },
    resetAllTitle() {
      this.seep = 0;
      this.seepActive = 0;
    },
    getExampleButton() {
      this.fileList.select1 = "Arabidopsis thaliana";
      this.fileName = "Arabidopsis_thaliana_Root_SRP182008.csv";
      this.getList2(1);
      this.getExample();
    },
    handleUpdate(event) {
      if (
        event.target.files[0].name.split(".")[
        event.target.files[0].name.split(".").length - 1
        ] != "csv"
      ) {
        this.$message.warning("Please upload .csv file！");
      } else {
        this.fileName = event.target.files[0].name;
        this.file = event.target.files[0];
        console.log(this.file, event.target.files);
      }
    },
    getList1() {
      get_train_species()
        .then((res) => {
          if (res.code == 200) {
            this.optionsFile = res.data;
          }
        })
        .catch((err) => { });
    },
    getList2(num = 0) {
      get_train_tissue({
        species: this.fileList.select1,
      })
        .then((res) => {
          if (res.code == 200) {
            this.optionsFile2 = res.data;
          }
          if (num) {
            this.fileList.select2 = "Root";
          } else {
            this.fileList.select2 = null;
          }
        })
        .catch((err) => { });
    },
    changeSpecies() {
      this.getList2();
    },
    getData() {
      // 添加其他字段到 FormData 对象中（可选）

      let formData = new FormData();
      if (this.file) {
        formData.append("file", this.file);
      } else {
        this.$message.warning("Please select a file！");
        return;
      }
      if (!this.fileList.select1) {
        this.$message.warning("Please select a species！");
        return;
      }
      if (!this.fileList.select2) {
        this.$message.warning("Please select an tissue！");
        return;
      }
      this.seep = 1;
      this.seepActive = 1;
      this.form2Loading = true;
      this.tableLoading1 = true;
      formData.append("species", this.fileList.select1);
      formData.append("tissue", this.fileList.select2);
      this.tableDataAll = [];
      this.tableData = [];
      this.currentPage = 0;
      get_cell_blast_data(formData)
        .then((res) => {
          console.log(res);
          if (res.data.code == 200) {
            this.tableData = res.data.data.table_data;
            this.column_names = res.data.data.column_names
              ? res.data.data.column_names
              : (() => {
                if (this.tableData.length > 0) {
                  return Object.keys(this.tableData[0]);
                } else {
                  return [];
                }
              })();
            // this.tableDataAll = res.data.data
            // this.total = res.data.data.length
            // this.currentPage = 1
            this.result1 = res.data.data;
          } else {
            this.result1 = {};
            this.tableData = [];
            this.column_names = [];
          }
          this.form2Loading = false;
          this.tableLoading1 = false;
        })
        .catch(() => {
          this.result1 = {};
          this.tableData = [];
          this.column_names = [];
          this.form2Loading = false;
          this.tableLoading1 = false;
        });
    },
    downloadFIle() {
      window.open(
        `${process.env.VUE_APP_BASE_URL}/source_material/Example_File/cell_blast/Arabidopsis_thaliana_Root_SRP182008.csv`,
        "_blank"
      );
    },
    downloadFIle2() {
      window.open(this.downloadFIle2Url, "_blank");
    },
    getExample() {
      this.tableDataAll = [];
      this.tableData = [];
      this.currentPage = 0;
      this.tableLoading1 = true;
      this.seepActive = 1;
      this.seep = 1;
      cell_blast_example()
        .then((res) => {
          console.log(res);
          this.tableLoading1 = false;
          if (res.code == 200) {
            this.tableData = res.data.table_data;
            this.column_names = res.data.column_names;
            // this.tableDataAll = res.data
            // this.total = res.data.length
            // console.log(this.total, res.data.length)
            // this.currentPage = 1

            this.result1 = res.data;
          } else {
            this.result1 = {};
            this.tableData = [];
            this.column_names = [];

            this.$message.error(res.data.msg || this.errMessage);
          }
        })
        .catch(() => {
          this.result1 = {};
          this.tableData = [];
          this.column_names = [];
          this.tableLoading1 = false;
          this.$message.error(this.errMessage);
        });
    },
    getTable3() {
      this.seepActive = 3;
      this.seep = this.seep > 3 ? this.seep : 3;
    },
    getTable2() {
      this.tableLoading2 = true;
      this.seepActive = 2;
      this.seep = this.seep > 2 ? this.seep : 2;
      get_cell_blast_hits({
        species: this.fileList.select1,
        tissue: this.fileList.select2,
        file_name: this.result1.file_name,
        query_type: this.result1.query_type,
      })
        .then((res) => {
          if (res.code == 200) {
            this.disabled2 = false;
            this.downloadFIle2Url = res.data.download_url;
            if (res.data.result_data && res.data.result_data.length > 0) {
              this.tableData2 = res.data.result_data[0].hits_table.map(
                (item) => {
                  item["PercentMt"] = item["Percent.mt"];
                  return item;
                }
              );
              this.tableDataActive = 0;
              this.tableData2All = res.data.result_data;
            } else {
              this.tableData2 = [];
            }
          } else {
            this.downloadFIle2Url = null;
            this.disabled2 = true;
            this.tableData2 = [];
            this.tableData2All = [];
            this.$message.error(res.data.msg || this.errMessage);
          }
          this.tableLoading2 = false;
        })
        .catch(() => {
          this.downloadFIle2Url = null;
          this.disabled2 = true;
          this.tableData2 = [];
          this.tableData2All = [];
          this.tableLoading2 = false;
          this.$message.error(this.errMessage);
        });
    },
    tagTable2(item, index) {
      this.tableData2 = item.hits_table.map((item) => {
        item["PercentMt"] = item["Percent.mt"];
        return item;
      });
      this.tableDataActive = index;
    },
    tableData3() {
      this.tableLoading3 = true;
      this.seepActive = 4;
      this.seep = this.seep > 4 ? this.seep : 4;
      get_cell_blast_predictions({
        pval_cutoff: this.tableForm2.data4,
        min_hits: this.tableForm2.data3,
        majority_threshold: this.tableForm2.data2,
        query_type: this.result1.query_type,
      })
        .then((res) => {
          this.tableLoading3 = false;
          if (res.code == 200) {
            this.downloadFIle4Url = res.data.download_url;
            this.tableData3List = res.data.table_data;
            let chart_data = res.data.chart_data || [];
            let chartData = [];
            // for (let i = 0; i < chart_data.length; i++) {
            //   chartData.push({
            //     name: chart_data[i].query_cell_name,
            //     value: chart_data[i].hits_number,
            //   });
            // }
            for (let item in chart_data) {
              chartData.push({
                name: item,
                value: chart_data[item],
              });
            }
            this.getEcharts(chartData);
          } else {
            this.downloadFIle4Url = null;
            this.tableData3List = [];
            let chart_data = [];

            this.$message.error(res.data.msg || this.errMessage);
          }
        })
        .catch(() => {
          this.downloadFIle4Url = null;
          this.tableData3List = [];
          let chart_data = [];
          this.tableLoading3 = false;
          this.$message.error(this.errMessage);
        });
    },
    getEcharts(data) {
      console.log(data);
      var myChart = echarts.init(this.$refs.cellidMainRightContentCharLeft2);
      var option;
      option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
        },
        xAxis: {
          type: "category",
          data: data.map((item) => item.name),
          axisLabel: {
            interval: 0,
            rotate: 20,
            textStyle: {
              color: "#6E7079", // 设置 Y 轴刻度标签的颜色
              fontSize: 10,
            },
            formatter: function (value) {
              // 假设超过5个字符的名称显示省略号
              if (value.length > 10) {
                return value.substring(0, 10) + "...";
              }
              return value;
            },
          },
        },
        yAxis: {
          type: "value",
          axisLine: {
            show: false,
          },
          axisLabel: {
            textStyle: {
              color: "#6E7079", // 设置 Y 轴刻度标签的颜色
            },
          },
        },
        series: [
          {
            data: data.map((item) => item.value),
            type: "bar",
            // barWidth: 45,
            itemStyle: {
              color: "rgba(40,186,112, 0.8)", // 设置柱状图的颜色
              barBorderRadius: [20, 20, 0, 0], // 设置顶部圆角
            },
            barBorderRadius: [20, 20, 20, 20],
          },
        ],
      };

      option && myChart.setOption(option);

      var myChart2 = echarts.init(this.$refs.cellidMainRightContentCharRight2);
      const option2 = {
        color: [
          "#21C85D",
          "#EF8839",
          "#2AD4AD",
          "#41C1E9",
          "#7CB518",
          "#FFD23F",
        ],
        title: {
          text: "Sequencing technology",
          left: "center",
          bottom: 0,
          textStyle: {
            color: "#333",
            fontSize: 16,
          },
          show: false,
        },
        tooltip: {
          trigger: "item",
          formatter: "{b} : {c} ({d}%)",
        },
        series: [
          {
            name: "Sequencing technology",
            type: "pie",
            radius: "50%",
            data: data,
            label: {
              color: "#333333",
              fontSize: 11,
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      };
      option2 && myChart2.setOption(option2);
    },
    downloadFIle4() {
      window.open(this.downloadFIle4Url, "_blank");
    },
  },
  mounted() {
    this.getList1();
    this.getList2();
  },
  watch: {
    currentPage: {
      handler(news) {
        if (this.tableDataAll.length > (news - 1) * 10) {
          this.tableData = this.tableDataAll.filter((item, index) => {
            return index >= (news - 1) * 10 && index < news * 10;
          });
        }
      },
      immediate: true,
    },
  },
};
</script>

<style scoped lang="scss">
.cellid {
  width: 100%;
  height: 100%;

  // background: #fff;
  .cellidMain {
    width: 1200px;
    min-height: 70px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    padding-bottom: 20px;

    // border-bottom: 1px solid #f0f0f0;
    .cellidMainTitle {
      width: 100%;
      height: 56px;
      line-height: 56px;
      font-weight: bold;
      font-size: 18px;
      color: #333;
    }

    .cellidMainLeft {
      width: 360px;
      height: auto;
      padding: 0 20px;
      box-sizing: border-box;
      background: #fff;

      .cellidMainContent {
        width: 100%;
        height: auto;
        padding: 30px 0 0 0;
        box-sizing: border-box;
        color: #666;

        .cellidMainContentName {
          margin-bottom: 20px;
        }

        .file_p {
          margin-top: 0;
          margin-bottom: 10px;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          display: flex;
          justify-content: space-between;
          align-items: center;

          span {
            display: inline-block;
            padding: 0 10px;
            box-sizing: border-box;
            position: relative;
            // top: -19px;
            width: 180px;
            height: 30px;
            line-height: 30px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
          }

          .file {
            position: relative;
            display: inline-block;
            background: #24a461;
            border-radius: 4px;
            overflow: hidden;
            color: #fff;
            text-decoration: none;
            text-indent: 0;
            line-height: 30px;
            cursor: pointer;
            width: 125px;
            height: 40px;
            line-height: 40px;
            text-align: center;
            top: 0;
            left: 0;

            input {
              position: absolute;
              font-size: 100px;
              right: 0;
              top: 0;
              opacity: 0;
              cursor: pointer;
            }
          }
        }

        .pointer {
          color: #0a9daa;
          cursor: pointer;
          margin-bottom: 20px;

          span {
            text-decoration: underline;
            padding-left: 10px;
          }
        }

        .cellidMainContentSelect {
          width: 100%;
          display: flex;
          justify-content: space-between;
          height: 40px;
          line-height: 40px;
          margin-bottom: 30px;

          .cellidMainContentSelectName {
            width: 70px;
            height: 100%;
          }

          .cellidMainContentSelectFile {
            width: calc(100% - 90px);
          }
        }

        .cellidMainContentText {
          width: 100%;
          height: 32px;
          color: #666;
          font-size: 14px;
        }

        .cellidMainContentDefault {
          width: 100%;
          margin-bottom: 20px;
        }

        .cellidMainContentButton {
          width: 100%;
          height: 40px;
          display: flex;
          justify-content: space-between;
          align-items: center;

          span {
            font-size: 14px;
            color: red;
          }
        }
      }
    }

    .cellidMainRight {
      width: calc(100% - 380px);
      height: auto;
      padding: 0 20px;
      box-sizing: border-box;
      background: #fff;

      .cellidMainRightContent {
        width: 100%;
        height: auto;

        .cellidMainRightContentTitle {
          width: 100%;
          height: 40px;
          font-size: 32px;
          line-height: 40px;
          font-weight: bold;
          margin-bottom: 20px;
        }

        .cellidMainRightContentText1 {
          color: #333333;
          font-size: 14px;
          line-height: 20px;
          margin-bottom: 20px;
        }

        .cellidMainRightContentText2 {
          color: #ff0000;
          font-size: 14px;
          line-height: 20px;
          margin-bottom: 20px;
        }

        .cellidMainRightContentText3 {
          width: 100%;
          height: auto;
          padding: 10px;
          box-sizing: border-box;
          background: #f4f4f4;
          border: 1px solid hsla(0, 0%, 39.2%, 0.2);
        }

        .cellidMainRightContentTextTable {
          tr {
            height: 36px;
          }
        }

        .cellBlastMainContentText {
          width: 100%;
          height: auto;
          line-height: 26px;
          color: #555;
          font-size: 14px;
          padding-left: 20px;
          box-sizing: border-box;
        }
      }
    }
  }

  .cell_pages {
    width: 100%;
    height: 50px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
}

.cellidMainTitleInfo {
  width: 100%;
  height: auto;
  // background: #24a461;
  margin-bottom: 10px;

  .cellidMainTitleInfoMain {
    width: 1240px;
    height: 100%;
    background: #24a461;
    margin: 0 auto;
    padding: 20px;
    box-sizing: border-box;
    color: #fff;
    font-size: 16px;
    line-height: 30px;
    border-radius: 5px;
  }
}

.cellidMainTitleFooter {
  width: 100%;
  height: 70px;

  .cellidMainTitleFooterMain {
    width: 1240px;
    height: 100%;
    // background: #24a461;
    margin: 0 auto;
    padding: 20px;
    box-sizing: border-box;
    // color: #fff;
    font-size: 16px;
    line-height: 30px;
    border-radius: 5px;
    text-align: center;
  }
}

.cellBlastMainInfo {
  width: 100%;
  height: 40px;
  display: flex;
  justify-content: space-between;
  line-height: 40px;
  font-weight: bold;
  font-size: 12px;

  .cellBlastMainInfoItem {
    color: #555555;

    span:nth-child(1) {
      color: #78c269;
    }
  }
}

.cellidMainRightContentTextTable {
  width: 100%;

  .cellidMainRightContentTextTableTop {
    width: 200px;
    height: 60px;
    position: relative;

    .cellidMainRightContentTextTableTopRight {
      position: absolute;
      right: 10px;
      top: 10px;
    }

    .cellidMainRightContentTextTableTopLeft {
      position: absolute;
      left: 10px;
      bottom: 10px;
      color: #555555;
    }

    .cellidMainRightContentTextTableTopLine {
      width: 220px;
      height: 2px;
      position: absolute;
      background: #fff;
      display: inline-block;
      left: 0;
      top: 0;
      transform-origin: 0 0;
      transform: rotate(15deg);
    }
  }

  tr {
    height: 36px;
  }

  tr:nth-child(2n) {
    background: #f2f2f2;
  }
}

.cellidMainRightContentFooter1 {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.cellidMainRightContentFooter2 {
  width: 100%;
  display: flex;
  // justify-content: center;
  align-items: center;
  margin-bottom: 20px;
  justify-content: space-between;
}

.cellidMainRightContent2 {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.cellidMainRightContent2Left {
  width: 220px;
  height: 300px;
  color: #fff;
  text-align: center;
  line-height: 35px;
  font-size: 14px;

  .cellidMainRightContent2LeftName {
    width: 100%;
    height: 35px;
    background: #09b07a;
    margin-bottom: 10px;
  }

  .cellidMainRightContent2LeftList {
    width: 100%;
    height: calc(100% - 45px);
    overflow-y: auto;
    overflow-x: hidden;

    .cellidMainRightContent2LeftListItem {
      width: 100%;
      height: 35px;
      color: #555555;
      cursor: pointer;
    }

    .cellidMainRightContent2LeftListItem:nth-child(2n) {
      background: #f2f2f2;
    }

    .cellidMainRightContent2LeftListItemActive {
      background: #fda543 !important;
      color: #fff !important;
    }
  }
}

.cellidMainRightContent2Right {
  width: calc(100% - 230px);
  height: 300px;
}

.cellBlastMainBlast1 {
  width: 100%;
  height: auto;
  border: 1px solid #09b07a;
  border-radius: 3px;
  position: relative;
  padding: 22px 100px 10px 20px;
  box-sizing: border-box;
  margin-bottom: 20px;

  .cellBlastMainBlast1Title {
    width: 210px;
    height: 30px;
    background: #09b07a;
    position: absolute;
    left: 20px;
    top: -15px;
    border-radius: 3px;
    color: #fff;
    text-align: center;
    line-height: 30px;
    font-size: 16px;
  }

  .cellBlastMainBlast1Item {
    width: 100%;
    height: 40px;
    line-height: 40px;
    color: #09b07a;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;

    .cellBlastMainBlast1ItemLeft {
      display: flex;
      justify-content: flex-start;
    }

    .cellBlastMainBlast1ItemLeftName {
      width: 180px;
      height: 100%;
      font-weight: bold;
      text-align: left;
    }

    .cellBlastMainBlast1ItemLeftValue {
      width: 268px;
      height: 100%;
      border: 1px solid #dcdfe6;
      border-radius: 0px;

      input {
        border: none;
        outline: none;
        width: 100%;
        height: 100%;
        background: #fff;
        color: #09b07a;
        font-size: 14px;
        text-align: left;
        padding-left: 10px;
        box-sizing: border-box;
      }
    }

    .cellBlastMainBlast1ItemRight {
      // width: calc(100% - 650px);
      width: 100%;
      height: 100%;
      text-align: right;
    }
  }
}

.cellidMainRightContentChar {
  display: flex;
  justify-content: space-between;

  .cellidMainRightContentCharLeft {
    width: 50%;
    height: 300px;
  }

  .cellidMainRightContentCharRight {
    width: 50%;
    height: 300px;
  }
}

.cellidMainRightButton {
  width: 100%;
  height: 60px;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
}

.cellBlastMainContent {
  width: 100%;
  height: 220px;
  border: 1px solid #09b07a;
  border-radius: 3px;
  position: relative;
  padding: 22px 50px 0;
  box-sizing: border-box;
  margin-top: 30px;

  .cellBlastMainContentTitle {
    width: 470px;
    height: 30px;
    background: #09b07a;
    position: absolute;
    left: 20px;
    top: -15px;
    border-radius: 3px;
    color: #fff;
    text-align: center;
    line-height: 30px;
    font-size: 16px;
  }

  .cellBlastMainContentName {
    width: 100%;
    height: 28px;
    line-height: 28px;
    font-weight: bold;
  }

  .cellBlastMainContentText {
    width: 100%;
    //   height: 26px;
    line-height: 26px;
    color: #555;
    font-size: 14px;
    padding-left: 20px;
    box-sizing: border-box;
  }

  .cellBlastMainContentInput {
    width: 100%;
    height: 134px;
    border: 1px dashed #09b07a;
    border-radius: 3px;
    position: relative;

    .cellBlastMainContentInputMain {
      width: calc(100% - 160px);
      height: 30px;
      position: absolute;
      left: 80px;
      top: 52px;
      display: flex;
      justify-content: space-between;

      .cellBlastMainContentInputMainInput {
        width: calc(100% - 160px);
        height: 100%;
      }
    }
  }

  .cellBlastMainContentDia {
    width: 100%;
    height: 28px;
    line-height: 28px;
    color: #555;
    font-size: 14px;
    text-align: center;
    margin-bottom: 20px;
  }

  .cellBlastMainContentFooter {
    width: 100%;
    height: 30px;
    display: flex;
    justify-content: space-between;
  }
}

.cellidMainRightContentTextTableHeaderName {
  display: inline-block;
  width: 100%;
  // max-width: 160px;
  line-height: 20px;
  padding: 0 10px;
  box-sizing: border-box;
  word-break: break-all;
}
</style>
