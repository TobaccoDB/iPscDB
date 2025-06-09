<!--
作者: nodebook@qq.com
组件名称: 
-->
<template>
    <div class="cellid">
        <div class="cellidMain">
            <div class="cellidMainLeft">
                <div class="cellidMainTitle">Input Data</div>
                <div class="cellidMainContent">
                    <div class="cellidMainContentName">Input File</div>
                    <div class="cellidMainContentFile">
                        <p class="file_p">
                            <a href="javascript:;" class="file"
                                >Choose File
                                <input type="file" name="file" ref="file" />
                            </a>
                            <span>a.png</span>
                        </p>
                        <i class="el-icon-download pointer">
                            <span>Download Example File</span>
                        </i>
                    </div>

                    <div class="cellidMainContentButton">
                        <span></span>
                        <el-button type="success" style="width: 100px">Run</el-button>
                    </div>
                </div>
            </div>
            <div class="cellidMainRight">
                <div class="cellidMainTitle">Result</div>
                <div class="cellidMainRightContent">
                    <div class="cellidMainRightContentTitle">Format of input data</div>
                    <div class="cellidMainRightContentText1">
                        A routine normalization and quality control should be performed. For example, there are three commonly used cell quality criteria, namely, the number of genes detected (default
                        >500), the number of unique molecular identifiers induced (default >1500), and the percentage of mitochondrial genes detected (default < 10% among all genes). Then, datasets
                        should be normalized, i.e., scaling to 10,000 and then with log(counts+1). The format of training data should be a csv or tab-delimited txt or h5ad(scanpy) format where the
                        columns correspond to genes and the rows correspond to cells. The column of cell types should be the last column and named as "cell_label". In a word, the format of training
                        data is a transposed normalized dataset with a cell type column in the right. A sample file looks something like:
                    </div>
                    <!-- <div class="cellidMainRightContentText2">
                        * We noticed some people uploaded mouse data, we now also support mouse data. But we don't recommend to do this as there are significant differences in gene expxression
                        profiles between mouse and human.
                    </div> -->

                    <table class="cellidMainRightContentTextTable" border="0" style="border-collapse: collapse; border: 1px solid #d1d8df; text-align: center; font-size: 14px; margin-bottom: 20px">
                        <tbody>
                            <tr style="border: 1px solid #d1d8df">
                                <td style="border: 1px solid #d1d8df; width: 250px"></td>
                                <td style="border: 1px solid #d1d8df; width: 150px; text-align: center">tspan6</td>
                                <td style="border: 1px solid #d1d8df; width: 150px; text-align: center">dpm1</td>
                                <td style="border: 1px solid #d1d8df; width: 150px; text-align: center">cell_label</td>
                            </tr>
                            <tr style="border: 1px solid #d1d8df">
                                <td style="border: 1px solid #d1d8df">pbmc1_SM2_Cell_133</td>
                                <td style="border: 1px solid #d1d8df">0.745639</td>
                                <td style="border: 1px solid #d1d8df">0.0</td>
                                <td style="border: 1px solid #d1d8df">CD4+_T_cell</td>
                            </tr>
                            <tr style="border: 1px solid #d1d8df">
                                <td style="border: 1px solid #d1d8df">pbmc1_SM2_Cell_142</td>
                                <td style="border: 1px solid #d1d8df">0.0</td>
                                <td style="border: 1px solid #d1d8df">0.778851</td>
                                <td style="border: 1px solid #d1d8df">B_Cell</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="cellidMainRightContentText1">
                        The format of test data is the format of training data without the column of "cell_label". We also provide a script preprocess.py to handle the cell quality control and
                        normalization of origin counts matrix dataset. The processed file will end up with "_treated.h5" in its name and can read through pandas package's read_hdf function. After
                        processing by the script, you just need to add the cell type column in the right of the processed matrix. The origin counts matrix dataset should be a csv or tab-delimited txt
                        or h5ad(scanpy) format where the columns correspond to cells and the rows correspond to genes looks like:
                    </div>
                    <table class="cellidMainRightContentTextTable" border="0" style="border-collapse: collapse; border: 1px solid #d1d8df; text-align: center; font-size: 14px; margin-bottom: 20px">
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
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const fileList = ref({
    select: ''
})
const optionsFile = ref([
    {
        label: '',
        value: ''
    }
])
</script>

<style scoped lang="scss">
.cellid {
    width: 100%;
    height: 100%;
    background: #fff;
    .cellidMain {
        width: 1200px;
        min-height: 70px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        padding-bottom: 20px;
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
                    white-space: nowrap;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    span {
                        display: inline-block;
                        // padding: 0 30px;
                        position: relative;
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
                    line-height: 24px;
                    margin-bottom: 20px;
                }
                .cellidMainRightContentText2 {
                    color: #ff0000;
                    font-size: 14px;
                    line-height: 24px;
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
}
</style>
