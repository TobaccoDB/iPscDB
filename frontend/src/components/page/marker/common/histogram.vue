<template>
    <div class="HistogramMain">
        <div class="Histogram" ref="HistogramDom"></div>
        <div class="HistogramFooter">number of markers</div>
    </div>
</template>

<script>
import * as echarts from 'echarts'
import { histogramData } from './charData'
import { marker_histogram_list } from '@/api/api'
export default {
    props: {
        selectValue: {
            type: String,
            default: null
        }
    },
    data() {
        return {}
    },
    mounted() {},
    methods: {
        getInfoData(val) {
            marker_histogram_list({
                species_name: val
            }).then((res) => {
                if (res.code == 200) {
                    if (res.data.children) {
                        // this.$refs.HistogramDom.innerHTML = ''
                        this.initChart(res.data.children)
                    }
                }
            })
        },
        initChart(data) {
            let myChart = echarts.init(this.$refs.HistogramDom)
            let option = {
                title: {
                    text: 'Distribution of cell markers in each tissue',
                    textStyle: {
                        color: '#212121', // 设置标题文字颜色
                        fontSize: 16, // 设置标题文字大小
                        fontWeight: '400' // 设置标题文字加粗
                    }
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    },
                    textStyle: {
                        color: '#fff' // 设置 Tooltip 文字颜色为黑色
                    },
                    backgroundColor: 'rgba(255,255,255,0.9)',
                    formatter: function (params) {
                        let title = ''
                        let data1 = {
                            color: '',
                            name: '',
                            value: ''
                        }
                        let data2 = {
                            color: '',
                            name: '',
                            value: ''
                        }
                        for (let i = 0; i < params.length; i++) {
                            if (i == 0 && params[i].name) {
                                title = params[i].name
                                data1.color = params[i].color
                                data1.value = params[i].value
                                data1.name = params[i].seriesName
                            }
                            if (i == 2 && params[i].name) {
                                data2.color = params[i].color
                                data2.value = params[i].value
                                data2.name = params[i].seriesName
                            }
                        }
                        let tooltipHTML = `
                            <div class='tooltipMarker'>
                                <div class='tooltipMarkerTitle'>${title}</div>
                                <div class='tooltipMarkerContent'>
                                    <span style='background: ${data1.color}'></span>
                                    <span>${data1.name}</span>
                                    <span>${data1.value}</span>
                                </div>
                                <div class='tooltipMarkerContent'>
                                    <span style='background: ${data2.color}'></span>
                                    <span>${data2.name}</span>
                                    <span>${data2.value}</span>
                                </div>
                            </div>
                        `

                        return tooltipHTML
                    }
                },
                legend: {
                    show: false
                },
                grid: {
                    left: '2%',
                    right: '4%',
                    bottom: '1%',
                    containLabel: true
                },
                xAxis: {
                    type: 'value',
                    axisLabel: {
                        show: true,
                        color: '#666666',
                        formatter: function (value, index) {
                            if (value > 1000) {
                                return value / 1000 + 'K' // 如果 x 轴坐标大于 1000，则显示为 K
                            } else {
                                return value
                            }
                        }
                    },
                    axisLine: false
                },
                yAxis: {
                    type: 'category',
                    axisLabel: {
                        show: true,
                        color: '#666666',
                        rotate: 10,
                        fontSize: 10
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#CCD6EB' // 设置轴线颜色为红色
                        }
                    },
                    data: data.map((item) => item.name).reverse()
                },
                series: [
                    {
                        name: 'Marker genes',
                        type: 'bar',
                        stack: 'total',
                        data: data.map((item) => item.gene_number).reverse(),
                        itemStyle: {
                            color: '#26B082' // 设置柱状图颜色为蓝色
                        }
                    },
                    {
                        name: 'transparent',
                        type: 'bar',
                        stack: 'total',
                        data: data.map((item) => 20),
                        itemStyle: {
                            color: 'transparent' // 设置柱状图颜色为蓝色
                        }
                    },
                    {
                        name: 'Classic Markers',
                        type: 'bar',
                        stack: 'total',
                        data: data.map((item) => item.classic_number).reverse(),
                        itemStyle: {
                            color: '#1CA1E3' // 设置柱状图颜色为蓝色
                        }
                    }
                ]
            }

            option && myChart.setOption(option)
        }
    },
    watch: {
        selectValue: {
            handler(news) {
                this.$nextTick(() => {
                    this.getInfoData(news)
                })
            },
            immediate: true
        }
    }
}
</script>

<style scoped lang="scss">
.HistogramMain {
    width: 100%;
    height: 100%;
    padding: 20px;
    box-sizing: border-box;
    text-align: center;
}
.HistogramFooter {
    width: 100%;
    height: 50px;
    font-family: PingFangSC-Regular;
    font-size: 14px;
    color: #212121;
    letter-spacing: 0;
    font-weight: 400;
}
.Histogram {
    width: 100%;
    height: calc(100% - 50px);
}
</style>

<style lang="scss">
.tooltipMarker {
    width: auto;
    // height: 915px;
    padding: 5px 10px;
}
.tooltipMarkerTitle {
    color: #666666;
    font-size: 12px;
    height: 16px;
    line-height: 16px;
}
.tooltipMarkerContent {
    height: 24px;
    font-size: 12px;
    color: #212121;
    line-height: 24px;
    text-align: left;
    span:nth-child(1) {
        display: inline-block;
        width: 12px;
        height: 12px;
        margin-right: 10px;
    }
    span:nth-child(2) {
        display: inline-block;
        width: auto;
        height: 16px;
        margin-right: 10px;
    }
}
</style>
