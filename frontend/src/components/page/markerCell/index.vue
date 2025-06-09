<!--
作者: nodebook@qq.com
组件名称: 
-->
<template>
    <div class="markerCell">
        <div class="markerCellInfo">
            <div class="markerCellInfoName">{{ $route.query.gene_id }}</div>
            <div class="markerCellInfoItem">
                <div class="markerCellInfoL1">
                    <span>Species:</span>
                    <!-- <span>{{ info.scaffold }}</span> -->
                    <span>{{ $route.query.species_name.replace(/_/g, " ") }}</span>
                </div>
                <div class="markerCellInfoL1">
                    <span>Gene Symbol:</span>
                    <span>{{ info.gene_symbol || info.gene_id }}</span>
                </div>
                <div class="markerCellInfoL1">
                    <span>Gene Strand:</span>
                    <span class="markerCellInfoL1Icon" :style="{ background: info.strand == '+' ? '#24A461' : 'red' }">{{ info.strand }}</span>
                </div>
            </div>
            <div class="markerCellInfoItem">
                <div class="markerCellInfoL1">
                    <span>Gene Location:</span>
                    <!-- <span>{{ info.gene_id }}</span> -->
                    <span>{{ info.scaffold }}</span>
                </div>
                <div class="markerCellInfoL1">
                    <span>Start Location:</span>
                    <span>{{ info.start }}</span>
                </div>
                <div class="markerCellInfoL1">
                    <span>End Location:</span>
                    <span>{{ info.end }}</span>
                </div>
            </div>
            <div class="markerCellInfoItem">
                <div class="markerCellInfoL2">
                    <span>Gene Description:</span>
                    <span>{{ info.description }}</span>
                </div>
            </div>
        </div>
        <div class="markerCellEcharts">
            <div class="markerCellEchartsName">Cell Type</div>
            <div class="markerCellEchartsContent">
                <div class="markerCellEchartsContentLeft" ref="markerCellEchartsContentLeft" style="margin-bottom: 10px"></div>
                <div class="markerCellEchartsContentTable">
                    <el-table :data="tableList" border style="width: 100%">
                        <el-table-column prop="clusterName" label="Cell Type" align="center" width="160"> </el-table-column>
                        <el-table-column prop="dataset" label="Dataset" align="center" width="340">
                            <template slot-scope="scope">
                                <el-tooltip class="item" effect="dark" :content="scope.row.dataset" placement="top">
                                    <div class="markerCellEchartsContentTableText">{{ scope.row.dataset }}</div>
                                </el-tooltip>
                            </template>
                        </el-table-column>
                        <el-table-column prop="dataset_no" label="Dataset No." align="center" width="120"> </el-table-column>
                        <el-table-column prop="dataset_no" label="PMID" align="center">
                            <template slot-scope="scope">
                                <a class="markerCellEchartsContentTableLink" v-for="(item, index) in scope.row.pmid" :key="index" :href="item.label" target="_blank">{{ item.name }};</a>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { gene_details_info, gene_details_cell_type } from '@/api/api'
import * as echarts from 'echarts'
export default {
    data() {
        return {
            info: {},
            tableList: []
        }
    },
    created() {
        if (!this.$route.query.species_name || !this.$route.query.gene_id) {
            this.$router.back()
        }
        this.getInfo()
    },
    mounted() {
        this.getTable()
    },
    methods: {
        getTable() {
            gene_details_cell_type({
                species_name: this.$route.query.species_name,
                gene_id: this.$route.query.gene_id
            }).then((res) => {
                if (res.code == 200) {
                    this.tableList = res.data
                    this.getEcharts(res.data)
                }
            })
        },
        getInfo() {
            gene_details_info({
                gene_id: this.$route.query.gene_id
            }).then((res) => {
                if (res.code == 200) {
                    this.info = res.data
                    console.log(this.info)
                }
            })
        },
        getEcharts(data) {
            var myChart = echarts.init(this.$refs.markerCellEchartsContentLeft)
            var option
            option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                xAxis: {
                    type: 'category',
                    data: data.map((item) => item.clusterName),
                    axisLabel: {
                        interval: 0,
                        rotate: 25,
                        textStyle: {
                            color: '#6E7079' // 设置 Y 轴刻度标签的颜色
                        }
                    }
                },
                yAxis: {
                    type: 'value',
                    axisLine: {
                        show: false
                    },
                    axisLabel: {
                        textStyle: {
                            color: '#6E7079' // 设置 Y 轴刻度标签的颜色
                        }
                    }
                },
                series: [
                    {
                        data: data.map((item) => item.dataset_no),
                        type: 'bar',
                        // barWidth: 45,
                        itemStyle: {
                            color: 'rgba(40,186,112, 0.8)', // 设置柱状图的颜色
                            barBorderRadius: [20, 20, 0, 0] // 设置顶部圆角
                        },
                        barBorderRadius: [20, 20, 20, 20]
                    }
                ]
            }

            option && myChart.setOption(option)
        }
    }
}
</script>

<style scoped lang="scss">
.markerCell {
    width: 1240px;
    margin: 0 auto;
    height: auto;
    padding: 40px 20px;
    box-sizing: border-box;
    background: #fff;
    .markerCellInfo {
        width: 100%;
        height: auto;
        background: #41ae7644;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        padding: 30px 20px 30px;
        box-sizing: border-box;
        border-radius: 10px;
        margin-bottom: 30px;

        .markerCellInfoName {
            width: 100%;
            height: 35px;
            font-size: 30px;
            line-height: 35px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #303133;
        }
        .markerCellInfoItem {
            width: 100%;
            height: 40px;
            line-height: 40px;
            display: flex;
            font-size: 18px;
            .markerCellInfoL1 {
                width: 30%;
                height: 100%;
                span {
                    font-size: 18px;
                    &:nth-child(1) {
                        font-weight: bold;
                        color: #555555;
                        margin-right: 10px;
                        font-size: 18px;
                    }
                }
                .markerCellInfoL1Icon {
                    width: 30px;
                    height: 30px;
                    display: inline-block;
                    text-align: center;
                    line-height: 30px;
                    color: #fff;
                    border-radius: 5px;
                }
            }
            .markerCellInfoL2 {
                width: 100%;
                height: 100%;
                span {
                    font-size: 18px;
                    &:nth-child(1) {
                        font-weight: bold;
                        color: #555555;
                        margin-right: 10px;
                        font-size: 18px;
                    }
                }
            }
        }
    }
    .markerCellEcharts {
        width: 100%;
        height: auto;
        .markerCellEchartsName {
            width: 100%;
            height: 35px;
            font-weight: bold;
            color: rgb(49, 163, 84);
            font-size: 30px;
            line-height: 35px;
        }
        .markerCellEchartsContent {
            width: 100%;
            // height: 350px;
            // display: flex;
            // justify-content: space-between;
            .markerCellEchartsContentLeft {
                width: 100%;
                height: 350px;
                // background: yellow;
            }
            .markerCellEchartsContentTable {
                width: 100%;
                height: auto;
                background: goldenrod;
                .markerCellEchartsContentTableText {
                    width: 320px;
                    height: auto;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                    text-align: center;
                    cursor: pointer;
                }
                .markerCellEchartsContentTableLink {
                    font-size: 14px;
                    margin-right: 5px;
                    color: #0d6efd;
                }
            }
        }
    }
}
</style>
