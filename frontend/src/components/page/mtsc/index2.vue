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
                    <span style="color: #e6ef82">C</span>ell
                    <span style="color: #e6ef82">T</span>ype
                    <span style="color: #e6ef82">A</span>nnotation (
                    <span style="color: #e6ef82">P</span>lant
                    <span style="color: #e6ef82">C</span>t
                    <span style="color: #e6ef82">A</span>nnotation) With Multiple References
                </span>
                is a ﬂexible single-cell assignment toolkit that integrates multiple references based on multitask deep metric learning designed
                speciﬁcally for cell type annotation within tissues with multiple single-cell sequencing data as references.
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
                            <span style="font-size: 12px" :title="fileName">{{ fileName }}</span>
                        </p>
                        <i class="el-icon-download pointer" @click="downloadFIle">
                            <span>Download Example File</span>
                        </i>
                    </div>
                    <div class="cellidMainContentText">Reference Dataset:</div>
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
                            <el-select v-model="fileList.select1" @change="changeSpecies" placeholder="Please select species" size="large" style="width: 100%">
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
                <el-main style="background: #fff; padding: 20px 20px" v-show="!infoData.file_size">
                    <h3>Input file explain</h3>
                    <p>*Raw counts DGE requirement: Gene (row) * Cell (column);</p>
                    <p>Gene ID: gene symbol only;</p>
                    <p>File size:
                        <=200mb;</p>
                            <p>File format: txt/csv (comma or tab separated);</p>
                            <p>File name: no space or other special character.</p>
                            <p>* Input file format as follows:</p>
                            <ul>
                                <li v-for="(item, index) in itemList" :key="index">{{ item }}</li>
                            </ul>
                </el-main>
                <div class="cellidMainRightInfo" v-show="infoData.file_size">
                    <span style="color: #24a461">File Size </span>
                    <span style="margin-right: 50px">{{ infoData.file_size }} </span>
                    <span style="color: #24a461">Number of Cells</span>
                    <span style="margin-right: 50px">{{ infoData.column_num }}</span>
                    <span style="color: #24a461">Number of Genes</span>
                    <span>{{ infoData.row_num }}</span>
                </div>
                <div class="cellidMainTitle" v-show="infoData.file_size">Result</div>
                <div class="cellidMainRightContent cellidMainRightContentChar" v-loading="form2Loading">
                    <div class="cellidMainRightContentCharLeft" ref="cellidMainRightContentCharLeft"></div>
                    <div class="cellidMainRightContentCharRight" ref="cellidMainRightContentCharRight"></div>
                </div>

                <div class="cellidMainTitle" v-show="tableData.length > 0">
                    <span>Detail</span>
                    <el-button type="primary" size="small" @click="download">Download</el-button>
                </div>
                <div class="cellidMainRightContent" v-show="tableData.length > 0">
                    <!-- <div class="cellidMainRightContentText1">
                        Plant cell type annotation with multiple references(Plant CtAmr) is a ﬂexible single-cell assignment toolkit that integrates multiple references based on multitask deep metric
                        learning designed speciﬁcally for cell type annotation within tissues with multiple single-cell sequencing data as references.
                    </div> -->

                    <!-- <div class="cellidMainRightContentTitle">Format of input data</div>
                    <div class="cellidMainRightContentText1">
                        A routine normalization and quality control should be performed. For example, there are three commonly used cell quality criteria, namely, the number of genes detected (default
                        >500), the number of unique molecular identifiers induced (default >1500), and the percentage of mitochondrial genes detected (default < 10% among all genes). Then, datasets
                        should be normalized, i.e., scaling to 10,000 and then with log(counts+1). The format of training data should be a csv or tab-delimited txt or h5ad(scanpy) format where the
                        columns correspond to genes and the rows correspond to cells. The column of cell types should be the last column and named as "cell_label". In a word, the format of training
                        data is a transposed normalized dataset with a cell type column in the right. A sample file looks something like:
                    </div> -->
                    <!-- <div class="cellidMainRightContentText2">
                        * We noticed some people uploaded mouse data, we now also support mouse data. But we don't recommend to do this as there are significant differences in gene expxression
                        profiles between mouse and human.
                    </div> -->

                    <!-- <table class="cellidMainRightContentTextTable" border="0" style="border-collapse: collapse; border: 1px solid #d1d8df; text-align: center; font-size: 14px; margin-bottom: 20px">
                        <tbody>
                            <tr style="border: 1px solid #d1d8df">
                                <td style="border: 1px solid #d1d8df; width: 250px">cell</td>
                                <td style="border: 1px solid #d1d8df; width: 150px; text-align: center" v-for="(item, index) in tableData" :key="index">{{ item.cell }}</td>
                            </tr>
                            <tr style="border: 1px solid #d1d8df">
                                <td style="border: 1px solid #d1d8df">cell_type</td>
                                <td style="border: 1px solid #d1d8df; width: 150px; text-align: center" v-for="(item, index) in tableData" :key="index">{{ item.cell_type }}</td>
                            </tr>
                        </tbody>
                    </table> -->
                    <el-table :data="tableData" border style="width: 100%" v-loading="form2Loading">
                        <el-table-column type="index" label="Input_ID" align="center" width="80">
                            <template slot-scope="scope">
                                <span>{{ scope.$index + 1 + (currentPage - 1) * 10 }}</span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="cell" label="Cell" align="center"> </el-table-column>
                        <el-table-column prop="cell_type" label="Cell_Type" align="center"> </el-table-column>
                    </el-table>
                    <div class="cell_pages">
                        <el-pagination background hide-on-single-page layout="prev, pager, next" :total="total" :current-page="currentPage" @current-change="
                                (val) => {
                                    currentPage = val;
                                }
                            ">
                        </el-pagination>
                    </div>
                    <!-- <div class="cellidMainRightContentText1">
                        The format of test data is the format of training data without the column of "cell_label". We also provide a script preprocess.py to handle the cell quality control and
                        normalization of origin counts matrix dataset. The processed file will end up with "_treated.h5" in its name and can read through pandas package's read_hdf function. After
                        processing by the script, you just need to add the cell type column in the right of the processed matrix. The origin counts matrix dataset should be a csv or tab-delimited txt
                        or h5ad(scanpy) format where the columns correspond to cells and the rows correspond to genes looks like:
                    </div> -->
                    <!-- <table class="cellidMainRightContentTextTable" border="0" style="border-collapse: collapse; border: 1px solid #d1d8df; text-align: center; font-size: 14px; margin-bottom: 20px">
                        <tbody>
                            <tr style="border: 1px solid #d1d8df">
                                <td style="border: 1px solid #d1d8df; width: 150px"></td>
                                <td style="border: 1px solid #d1d8df; width: 250px; text-align: center">pbmc1_SM2_Cell_133</td>
                                <td style="border: 1px solid #d1d8df; width: 250px; text-align: center">pbmc1_SM2_Cell_142</td>
                            </tr>
                            <tr style="border: 1px solid #d1d8df">
                                <td style="border: 1px solid #d1d8df">tspan6</td>
                                <td style="border: 1px solid #d1d8df">4</td>
                                <td style="border: 1px solid #d1d8df">0</td>
                            </tr>
                            <tr style="border: 1px solid #d1d8df">
                                <td style="border: 1px solid #d1d8df">dpm1</td>
                                <td style="border: 1px solid #d1d8df">0</td>
                                <td style="border: 1px solid #d1d8df">9</td>
                            </tr>
                        </tbody>
                    </table> -->
                </div>
            </div>
        </div>
        <!-- <div class="cellidMainTitleFooter">
            <div class="cellidMainTitleFooterMain">
                The first column is the gene name and other columns are the gene expression data for each cluster. The column can split by Tab(\t), Comma(,) or Space( )
            </div>
        </div> -->
    </div>
</template>

<script>
import { get_train_species, get_train_tissue, get_mtsc_data, mtsc_example } from "@/api/api";
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
            infoData: {
                column_num: 0,
                file_size: 0,
                row_num: 0,
            },
            itemList: ["", "Cell01", "Cell02", "Cell03", "Gene1", "1.33", "0", "0", "Gene2", "0", "0.75", "0", "Gene3", "0", "1", "0.43", "Gene4", "0", "0", "3.17"],
        };
    },
    methods: {
        async download() {
            // const a = document.createElement('a')
            // a.href = 'http://172.16.1.88/source_material/result_file/cell_id_result.txt' //process.env.VUE_APP_BASE_URL + '/source_material/result_file/cell_id_result.txt'
            // a.download = 'cell_id_result.txt'
            // a.target = '_blank'
            // a.style.display = 'none'
            // document.body.appendChild(a)
            // a.click()
            // document.body.removeChild(a)

            var url = process.env.VUE_APP_BASE_URL + "/source_material/result_file/CtAnnotation_result.csv";
            var xhr = new XMLHttpRequest();
            xhr.open("GET", url, true); //get请求，请求地址，是否异步
            xhr.responseType = "blob"; // 返回类型blob
            xhr.onload = function () {
                // 请求完成处理函数
                if (this.status === 200) {
                    var blob = this.response; // 获取返回值
                    var a = document.createElement("a");
                    a.download = "CtAnnotation_result.csv";
                    a.href = window.URL.createObjectURL(blob);
                    a.click();
                }
            };
            // 发送ajax请求
            xhr.send();
        },
        getExampleButton() {
            this.fileList.select1 = "Arabidopsis thaliana";
            this.fileName = "Arabidopsis_thaliana_Root_SRP182008.csv";
            this.getList2(1);
            this.getExample();
        },
        handleUpdate(event) {
            if (event.target.files[0].name.split(".")[event.target.files[0].name.split(".").length - 1] != "csv") {
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
            }
            if (!this.fileList.select1) {
                this.$message.warning("Please select a species！");
                return;
            }
            if (!this.fileList.select2) {
                this.$message.warning("Please select an tissue！");
                return;
            }
            this.form2Loading = true;
            formData.append("species", this.fileList.select1);
            formData.append("tissue", this.fileList.select2);
            this.tableDataAll = [];
            this.tableData = [];
            this.currentPage = 0;

            get_mtsc_data(formData)
                .then((res) => {
                    console.log(res.data.code);
                    if (res.data.code == 200) {
                        // this.tableData = res.data.data
                        this.tableDataAll = res.data.data.table_data;
                        this.total = res.data.data.table_data.length;
                        this.currentPage = 1;
                        let chart_data = res.data.data.chart_data;
                        this.infoData = {
                            column_num: res.data.data.column_num,
                            file_size: res.data.data.file_size,
                            row_num: res.data.data.row_num,
                        };
                        let chartData = [];
                        for (let item in chart_data) {
                            chartData.push({
                                name: item,
                                value: chart_data[item],
                            });
                        }
                        this.getEcharts(chartData);
                    }
                    this.form2Loading = false;
                })
                .catch(() => {
                    this.form2Loading = false;
                });
        },
        downloadFIle() {
            window.open(`${process.env.VUE_APP_BASE_URL}/source_material/Example_File/mtsc/Arabidopsis_thaliana_Root_SRP182008.csv`, "_blank");
        },
        getExample() {
            this.tableDataAll = [];
            this.tableData = [];
            this.currentPage = 0;
            this.form2Loading = true;
            mtsc_example().then((res) => {
                console.log(res.data);
                console.log(res.code);
                if (res.code == 200) {
                    // this.tableData = res.data.data
                    this.tableDataAll = res.data.table_data;
                    this.total = res.data.table_data.length;
                    console.log(this.total, res.data.length);
                    this.currentPage = 1;
                    let chart_data = res.data.chart_data;
                    this.infoData = {
                        column_num: res.data.column_num,
                        file_size: res.data.file_size,
                        row_num: res.data.row_num,
                    };
                    let chartData = [];
                    for (let item in chart_data) {
                        chartData.push({
                            name: item,
                            value: chart_data[item],
                        });
                    }
                    this.getEcharts(chartData);
                }
                this.form2Loading = false;
            });
        },
        getEcharts(data) {
            var myChart = echarts.init(this.$refs.cellidMainRightContentCharLeft);
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

            var myChart2 = echarts.init(this.$refs.cellidMainRightContentCharRight);
            const option2 = {
                color: ["#21C85D", "#EF8839", "#2AD4AD", "#41C1E9", "#7CB518", "#FFD23F"],
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
      display: flex;
      justify-content: space-between;
      align-items: center;
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
            // padding: 0 30px;
            position: relative;
            padding: 0 10px;
            box-sizing: border-box;
            // top: -19px;
            // width: 150px;
            // height: 30px;
            width: 200px;
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
      padding: 30px 20px;
      box-sizing: border-box;
      background: #fff;
      .el-main {
        padding: 0;
        border: 1px solid #09b07a;
        padding: 20px;
        border-radius: 5px;
        position: relative;
        overflow: visible;
        h3 {
          width: 470px;
          height: 30px;
          font-size: 18px;
          font-family: PingFang SC, PingFang SC-Medium;
          font-weight: 500;
          color: #333333;
          line-height: 30px;
          position: absolute;
          top: -15px;
          left: 20px;
          background: #09b07a;
          color: #fff;
          padding-left: 45px;
          box-sizing: border-box;
          border-radius: 3px;
        }
        ul {
          width: 100%;
          height: auto;
          overflow: hidden;
          margin: 10px 0;
          li {
            width: 25%;
            float: left;
            height: 32px;
            line-height: 32px;
            text-align: center;
            font-size: 16px;
            font-family: PingFang SC, PingFang SC-Medium;
            font-weight: 500;
            color: #666666;
            border: 1px solid #999999;
            box-sizing: border-box;
          }
        }
        .ReferenceTable {
          width: 100%;
          height: auto;
          overflow: hidden;
          margin: 10px 0;
          .grid-Reference {
            width: 100%;
            float: left;
            height: 32px;
            line-height: 32px;
            text-align: left;
            font-size: 16px;
            font-family: PingFang SC, PingFang SC-Medium;
            font-weight: 500;
            color: #666666;
            border: 1px solid #999999;
            box-sizing: border-box;
            word-wrap: break-word;
            padding: 0 5px;
          }
        }
        p {
          width: 100%;
          height: auto;
          font-size: 16px;
          font-family: PingFang SC, PingFang SC-Medium;
          font-weight: 500;
          color: #666666;
          line-height: 32px;
        }
        .bottom_p {
          width: 100%;
          margin-top: 10px;
          height: auto;
          overflow: hidden;
          background: rgba(169, 169, 169, 0.2);
          padding: 10px 20px;
          box-sizing: border-box;
        }
      }

      .cellidMainRightInfo {
        width: 100%;
        height: 35px;
        border-top: 1px solid #24a461;
        border-bottom: 1px solid #24a461;
        line-height: 35px;
        padding-left: 20px;
        box-sizing: border-box;

        span:nth-child(2n-1) {
          margin-right: 10px;
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
  margin-bottom: 10px;

  // background: #24a461;
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
</style>
