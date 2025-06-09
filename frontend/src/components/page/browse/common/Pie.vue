<!--
作者: nodebook@qq.com
组件名称: 饼图
-->
<template>
    <div class="pie-chart" ref="pieChart"></div>
</template>

<script>
import * as echarts from 'echarts'
export default {
    props: {
        infoData: {
            type: Array,
            default: () => [],
            required: true
        }
    },
    data() {
        return {}
    },
    methods: {
        getInfo(data) {
            let myChart = echarts.init(this.$refs.pieChart)
            let option
            option = {
                tooltip: {
                    trigger: 'item',
                    position: 'insideTop'
                },
                series: [
                    {
                        type: 'pie',
                        radius: '60%',
                        data: data,
                        label: {
                            show: false,
                            position: 'center'
                        },
                        labelLine: {
                            show: false
                        },
                        itemStyle: {
                            color: function (params) {
                                var colorList = ['#37AC6F', '#FF9828', '#1F88CA', 'yellow', 'orange'] // 定义颜色列表
                                return colorList[params.dataIndex % colorList.length] // 根据数据索引返回对应的颜色
                            }
                        },
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            }

            option && myChart.setOption(option)
        }
    },
    watch: {
        infoData: {
            handler(news) {
                this.$nextTick(() => {
                    this.getInfo(news)
                })
            },
            deep: true,
            immediate: true
        }
    }
}
</script>

<style scoped>
.pie-chart {
    width: 140px;
    height: 60px;
}
</style>
