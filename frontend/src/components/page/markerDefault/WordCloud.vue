<template>
    <div class="wordCloud" ref="wordCloud"></div>
</template>

<script>
import * as echarts from 'echarts'
import 'echarts-wordcloud'
export default {
    props: {
        infoData: {
            type: Array,
            default: [],
            required: true
        }
    },
    data() {
        return {
            loading: false
        }
    },
    mounted() {},
    methods: {
        getRandomInt(min, max) {
            min = Math.ceil(min)
            max = Math.floor(max)
            return Math.floor(Math.random() * (max - min + 1)) + min
        },
        infoWordCloud(words) {
            let This = this
            let keywords = words.map((item) => {
                item.value = item.source_no
                return item
            })
            let myChart = echarts.init(this.$refs.wordCloud)
            let option = {
                series: [
                    {
                        type: 'wordCloud',
                        //maskImage: maskImage,
                        sizeRange: [30, 40],
                        rotationRange: [-45, 45],
                        rotationStep: 45,
                        gridSize: 8,
                        shape: 'pentagon',
                        width: '100%',
                        height: '100%',
                        textStyle: {
                            normal: {
                                color: function () {
                                    return 'rgb(' + [This.getRandomInt(0, 255), This.getRandomInt(0, 255), This.getRandomInt(0, 255)].join(',') + ')'
                                },
                                fontFamily: 'sans-serif',
                                fontWeight: 'normal'
                            },
                            emphasis: {
                                shadowBlur: 10,
                                shadowColor: '#333'
                            }
                        },
                        data: keywords
                    }
                ]
            }
            option && myChart.setOption(option)
        }
    },
    watch: {
        infoData: {
            handler(newVal, oldVal) {
                this.infoWordCloud(newVal)
            },
            deep: true
            // immediate: true
        }
    }
}
</script>
<style lang="scss" scoped>
.wordCloud {
    width: 100%;
    height: 100%;
}
</style>
