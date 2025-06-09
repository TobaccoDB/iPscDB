<!--
作者: nodebook@qq.com
组件名称: 
-->
<template>
    <div class="cellBlast">
        <div class="cellBlastMain">
            <div class="cellBlastMainTitle">Welcome to Cell BLAST</div>
            <div class="cellBlastMaintext">A BLAST-like Toolkit for scRNA-seq Data Querying and Annotation</div>
            <!-- Start -->
            <div class="cellBlastMainContent">
                <div class="cellBlastMainContentTitle">Upload scRNA-seq Data For Query or Fetch Previous Results</div>
                <div class="cellBlastMainContentName">Note:</div>
                <div class="cellBlastMainContentText">✓ Supported Format of Single-cell Expression Matrix File Includes CSV, TSV, h5ad and loom.</div>
                <div class="cellBlastMainContentText">✓ CSV and TSV Files Should Include Both Cell Names and Gene Names (e.g. TP53, NOT IDs Like ENSG00000141510).</div>
                <div class="cellBlastMainContentText">✓ Gene Expression Matrix Contains UMI Counts or TPM/FPKM, with All Genes Detected.</div>
                <div class="cellBlastMainContentText" style="margin-bottom: 10px">✓ The Number of Querying Cells is Currently Limited to 20,000 in the Web Interface.</div>
                <div class="cellBlastMainContentInput">
                    <div class="cellBlastMainContentInputMain">
                        <el-input class="cellBlastMainContentInputMainInput" placeholder="Type or paste a task Id to fetch Cell BLAST result within a week." />
                        <el-button type="success">CHOOSE FILE</el-button>
                    </div>
                </div>
                <div class="cellBlastMainContentDia">or Drag And Drop a Single-cell Expression Matrix File into the Dash-box Area</div>
                <div class="cellBlastMainContentFooter">
                    <el-button type="success" plain>DOWNLOAD A SAMPLE</el-button>
                    <el-button type="success" plain>RUN A DEMO</el-button>
                    <el-button type="success" plain>TRY A TASK ID</el-button>
                </div>
            </div>
            <div class="cellBlastMainInfo">
                <div class="cellBlastMainInfoItem">
                    <span>File Name:</span>
                    <span>segerstolpe_disease_gc.tsv.gz</span>
                </div>
                <div class="cellBlastMainInfoItem">
                    <span>File Type:</span>
                    <span>application/gzip</span>
                </div>
                <div class="cellBlastMainInfoItem">
                    <span>File Size:</span>
                    <span>655.38 KB</span>
                </div>
                <div class="cellBlastMainInfoItem">
                    <span>Number of Cells:</span>
                    <span>50</span>
                </div>
                <div class="cellBlastMainInfoItem">
                    <span>Number of Genes:</span>
                    <span>21882</span>
                </div>
            </div>
            <table class="cellidMainRightContentTextTable" border="0" style="border-collapse: collapse; border: 1px solid #d1d8df; text-align: center; font-size: 14px; margin-bottom: 20px">
                <thead>
                    <tr style="height: 60px; background: #09b07a; color: #fff">
                        <th style="width: 200px">
                            <div class="cellidMainRightContentTextTableTop">
                                <span class="cellidMainRightContentTextTableTopRight">Genes</span>
                                <span class="cellidMainRightContentTextTableTopLeft">Cells</span>
                                <span class="cellidMainRightContentTextTableTopLine"></span>
                            </div>
                        </th>
                        <th style="text-align: center">SGIP1</th>
                        <th style="text-align: center">AZIN2</th>
                        <th style="text-align: center">CLIC4</th>
                        <th style="text-align: center">AGBL5</th>
                        <th style="text-align: center">NECAP2</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border: 1px solid #d1d8df">
                        <td>HP1526901T2D_H3</td>
                        <td>0</td>
                        <td>0</td>
                        <td>0</td>
                        <td>0</td>
                        <td>0</td>
                    </tr>
                    <tr style="border: 1px solid #d1d8df">
                        <td>HP1504101T2D_B6</td>
                        <td>0</td>
                        <td>0</td>
                        <td>0</td>
                        <td>0</td>
                        <td>0</td>
                    </tr>
                </tbody>
            </table>
            <!-- Blast -->
            <div class="cellBlastMainBlast1">
                <div class="cellBlastMainBlast1Title">Choose Reference Panel</div>
                <div class="cellBlastMainBlast1Item">
                    <div class="cellBlastMainBlast1ItemLeft">
                        <div class="cellBlastMainBlast1ItemLeftName">Species:</div>
                        <div class="cellBlastMainBlast1ItemLeftValue">
                            <el-select v-model="value" placeholder="Select" style="width: 100%">
                                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                            </el-select>
                        </div>
                    </div>
                </div>
                <div class="cellBlastMainBlast1Item">
                    <div class="cellBlastMainBlast1ItemLeft">
                        <div class="cellBlastMainBlast1ItemLeftName">Organ:</div>
                        <div class="cellBlastMainBlast1ItemLeftValue">
                            <el-select v-model="value" placeholder="Select" style="width: 100%">
                                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                            </el-select>
                        </div>
                    </div>
                </div>
                <div class="cellBlastMainBlast1Item">
                    <div class="cellBlastMainBlast1ItemLeft">
                        <div class="cellBlastMainBlast1ItemLeftName">Reference Panel:</div>
                        <div class="cellBlastMainBlast1ItemLeftValue">
                            <el-select v-model="value" placeholder="Select" style="width: 100%">
                                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                            </el-select>
                        </div>
                    </div>
                    <div class="cellBlastMainBlast1ItemRight">
                        <el-button type="danger" plain style="width: 120px">CLEAR</el-button>
                    </div>
                </div>
            </div>
            <div class="cellBlastMainBlast1">
                <div class="cellBlastMainBlast1Title" style="background: #fda543">Send Email with Results</div>
                <div class="cellBlastMainBlast1Item">
                    <div class="cellBlastMainBlast1ItemLeft">
                        <div class="cellBlastMainBlast1ItemLeftName" style="color: #fda543">Email Address:</div>
                        <div class="cellBlastMainBlast1ItemLeftValue">
                            <el-select v-model="value" placeholder="Select" style="width: 100%">
                                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                            </el-select>
                        </div>
                    </div>
                    <div class="cellBlastMainBlast1ItemRight">
                        <el-button type="danger" plain style="width: 120px">CLEAR</el-button>
                    </div>
                </div>
            </div>
            <div class="cellBlastMainBlast1">
                <div class="cellBlastMainBlast1Title" style="background: #fda543">Set Query Parameters</div>
                <div class="cellBlastMainBlast1Item">
                    <div class="cellBlastMainBlast1ItemLeft">
                        <div class="cellBlastMainBlast1ItemLeftName" style="color: #fda543; width: 350px">Number of Models:</div>
                        <div class="cellBlastMainBlast1ItemLeftValue">
                            <el-select v-model="value" placeholder="Select" style="width: 100%">
                                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                            </el-select>
                        </div>
                    </div>
                    <div class="cellBlastMainBlast1ItemRight">
                        <!-- <el-button type="danger" plain style="width: 120px">CLEAR</el-button> -->
                    </div>
                </div>
                <div class="cellBlastMainBlast1Item">
                    <div class="cellBlastMainBlast1ItemLeft">
                        <div class="cellBlastMainBlast1ItemLeftName" style="color: #fda543; width: 350px">Number of Hits Reported for Each Model:</div>
                        <div class="cellBlastMainBlast1ItemLeftValue">
                            <el-select v-model="value" placeholder="Select" style="width: 100%">
                                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                            </el-select>
                        </div>
                    </div>
                    <div class="cellBlastMainBlast1ItemRight">
                        <el-button type="danger" plain style="width: 120px">CLEAR</el-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const value = ref('')
let options = [
    {
        value: 'Option1',
        label: 'Option1'
    }
]
</script>

<style scoped lang="scss">
.cellBlast {
    width: 100%;
    min-height: 700px;
    .cellBlastMain {
        width: 1240px;
        height: auto;
        margin: 0 auto;
        padding-top: 20px;
        .cellBlastMainTitle {
            width: 100%;
            height: 38px;
            font-size: 30px;
            font-weight: bold;
            color: #09b07a;
            text-align: center;
            line-height: 38px;
            margin-bottom: 20px;
        }
        .cellBlastMaintext {
            width: 100%;
            text-align: center;
            height: 20px;
            line-height: 20px;
            color: rgb(85, 85, 85);
            font-size: 16px;
            margin-bottom: 30px;
        }
        .cellBlastMainContent {
            width: 100%;
            height: 420px;
            border: 1px solid #09b07a;
            border-radius: 3px;
            position: relative;
            padding: 22px 100px 0;
            box-sizing: border-box;
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
                height: 26px;
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
        .cellBlastMainInfo {
            width: 100%;
            height: 40px;
            display: flex;
            justify-content: space-between;
            line-height: 40px;
            font-weight: bold;
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
                    width: 140px;
                    height: 100%;
                    font-weight: bold;
                    text-align: left;
                }
                .cellBlastMainBlast1ItemLeftValue {
                    width: 268px;
                    height: 100%;
                }
                .cellBlastMainBlast1ItemRight {
                    width: calc(100% - 650px);
                    height: 100%;
                    text-align: right;
                }
            }
        }
    }
}
</style>
