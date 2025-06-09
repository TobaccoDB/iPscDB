export const option1 = {
    // color: ['#eb5e28', '#f27f34', '#f9a03f', '#f6b049', '#f3c053', '#a1c349', '#94b33d', '#87a330', '#799431',
    //     '#6a8532', '#ff0000', '#ff8700', '#ffd300', '#deff0a', '#a1ff0a', '#0aff99', '#0aefff', '#147df5', '#580aff', '#be0aff'
    // ],
    color: [
        '#ef8839',
        '#21c85d',
        '#fbb02d',
        '#ff0054',
        '#ff5400',
        '#f72585',
        '#41c1e9',
        '#7cb518',
        '#c46cfd',
        '#4cbcaf',
        '#3f9fe0',
        '#fb5607',
        '#8338ec',
        '#3a86ff',
        '#ffd23f',
        '#2ad4ad',
        '#0ead69',
        '#427aa1',
        '#679436'
    ],
    title: {
        left: 'center',
        textStyle: {
            fontSize: 24,
            fontWeight: 400,
            color: '#666666'
        },
        text: ''
    },
    legend: {
        data: [],
        top: 'center',
        right: 'left',
        orient: 'vertical',
        type: 'scroll',
        formatter: function (name) {
            // if (!name) return '';
            // if (name.length > 5) {
            //     name = name.slice(0, 5) + '...';
            //     return name
            // }
            let strs = name.split('') //字符串数组
            let str = ''
            for (let i = 0, s; (s = strs[i++]); ) {
                //遍历字符串数组
                str += s
                if (!(i % 10)) str += '\n' //按需要求余
            }
            return str
        },
        textStyle: {
            fontSize: 12
        }
    },
    grid: {
        top: '6%',
        left: '3%',
        right: '19%',
        bottom: 23,
        containLabel: true
    },
    tooltip: {
        trigger: 'item',
        axisPointer: {
            type: 'cross'
        },
        formatter: function (params) {
            if (params.value.length > 1) {
                return params.seriesName + ' :<br/>' + params.value[0] + ' , ' + params.value[1] + ''
            } else {
                return params.seriesName + ' :<br/>' + params.name + ' , ' + params.value + ''
            }
        }
    },
    xAxis: {
        // type: 'value',
        // scale: true,
        // splitLine: {
        //     show: false
        // },
        // name: 'umap1',
        // nameLocation: 'center',
        // nameGap: 20,
        // nameTextStyle: {
        //     fontWeight: 'bolder',
        //     fontSize: 16
        // },
        // axisLine: {
        //     onZero: false
        // }
    },
    yAxis: {
        // type: 'value',
        // scale: true,
        // splitLine: {
        //     show: false
        // },
        // name: 'umap2',
        // nameLocation: 'center',
        // nameGap: 20,
        // nameTextStyle: {
        //     fontWeight: 'bolder',
        //     fontSize: 16
        // },
        // axisLine: {
        //     onZero: false
        // }
    },
    series: []
}

export const option1Left = {
    // color: ['#eb5e28', '#f27f34', '#f9a03f', '#f6b049', '#f3c053', '#a1c349', '#94b33d', '#87a330', '#799431',
    //     '#6a8532', '#ff0000', '#ff8700', '#ffd300', '#deff0a', '#a1ff0a', '#0aff99', '#0aefff', '#147df5', '#580aff', '#be0aff'
    // ],
    color: [
        '#ef8839',
        '#21c85d',
        '#fbb02d',
        '#ff0054',
        '#ff5400',
        '#f72585',
        '#41c1e9',
        '#7cb518',
        '#c46cfd',
        '#4cbcaf',
        '#3f9fe0',
        '#fb5607',
        '#8338ec',
        '#3a86ff',
        '#ffd23f',
        '#2ad4ad',
        '#0ead69',
        '#427aa1',
        '#679436'
    ],
    title: {
        left: 'center',
        textStyle: {
            fontSize: 24,
            fontWeight: 400,
            color: '#666666'
        },
        text: ''
    },
    legend: {
        data: [],
        top: 'center',
        right: 'left',
        orient: 'vertical',
        type: 'scroll',
        formatter: function (name) {
            // if (!name) return '';
            // if (name.length > 5) {
            //     name = name.slice(0, 5) + '...';
            //     return name
            // }
            let strs = name.split('') //字符串数组
            let str = ''
            for (let i = 0, s; (s = strs[i++]); ) {
                //遍历字符串数组
                str += s
                if (!(i % 10)) str += '\n' //按需要求余
            }
            return str
        },
        textStyle: {
            fontSize: 12
        }
    },
    grid: {
        top: '6%',
        left: '3%',
        right: '19%',
        bottom: 23,
        containLabel: true
    },
    tooltip: {
        trigger: 'item',
        axisPointer: {
            type: 'cross'
        },
        formatter: function (params) {
            if (params.value.length > 1) {
                return params.seriesName + ' :<br/>' + params.value[0] + ' , ' + params.value[1] + ''
            } else {
                return params.seriesName + ' :<br/>' + params.name + ' , ' + params.value + ''
            }
        }
    },
    xAxis: {
        // type: 'value',
        // scale: true,
        // splitLine: {
        //     show: false
        // },
        // name: 'umap1',
        // nameLocation: 'center',
        // nameGap: 20,
        // nameTextStyle: {
        //     fontWeight: 'bolder',
        //     fontSize: 16
        // },
        // axisLine: {
        //     onZero: false
        // }
    },
    yAxis: {
        // type: 'value',
        // scale: true,
        // splitLine: {
        //     show: false
        // },
        // name: 'umap2',
        // nameLocation: 'center',
        // nameGap: 20,
        // nameTextStyle: {
        //     fontWeight: 'bolder',
        //     fontSize: 16
        // },
        // axisLine: {
        //     onZero: false
        // }
    },
    series: []
}
export const optionRight1 = {
    title: {
        left: 'center',
        textStyle: {
            fontSize: 14,
            fontWeight: 400,
            color: '#666666'
        },
        text: 'Cell Number in Each Cell Type'
    },
    tooltip: {
        // trigger: 'axis',
        // axisPointer: {
        //     type: "shadow",
        // },
    },
    grid: {
        left: '2%',
        right: '2%',
        bottom: 0,
        top: '10%',
        containLabel: true
    },
    xAxis: {
        type: 'category',
        data: [],
        // axisTick: {
        //     show: false,
        // },
        axisLabel: {
            // interval: 0,
            rotate: 45
        }
        // splitArea: {
        //     show: true
        // },
    },
    yAxis: {
        // type: 'category',
        // splitArea: {
        //     show: true
        // },
        // type: 'value',
    },
    // dataZoom: {
    //     type: "inside",
    //     show: true,
    //     height: 10,
    //     start: 0,
    //     end: 100,
    // },
    series: [
        {
            // name: 'Cell Number in Each Cell Type',
            type: 'bar',
            data: [],
            barMaxWidth: 20
        }
    ]
}

export const optionBoxplot = {
    title: {
        left: 'center',
        textStyle: {
            fontSize: 14,
            fontWeight: 400,
            color: '#666666'
        },
        text: 'Cell Number in Each Cell Type'
    },
    tooltip: {
        // trigger: 'item',
        // axisPointer: {
        //     type: 'shadow'
        // }
    },
    grid: {
        left: '6%',
        right: '2%',
        bottom: 0,
        top: '10%',
        containLabel: true
    },
    xAxis: {
        type: 'category',
        data: [],
        // boundaryGap: true,
        // nameGap: 30,
        // splitArea: {
        //     show: false
        // },
        // axisLabel: {
        //     formatter: 'expr {value}'
        // },
        // splitLine: {
        //     show: false
        // }
        axisLabel: {
            // interval: 0,
            rotate: 45
        }
    },
    yAxis: {
        // type: 'value',
        // name: 'km/s minus 299,000',
        // splitArea: {
        //     show: true
        // }
    },
    series: [
        {
            name: 'boxplot',
            type: 'boxplot',
            data: [],
            // itemStyle: {
            //     normal: {
            //         borderColor: '#666',
            //         // borderColor: '#4B96F3',
            //         borderWidth: 1,
            //         color: '#D9EAFF',
            //     }
            // },
            tooltip: {
                formatter: function (param) {
                    return [
                        'Experiment ' + param.name + ': ',
                        'upper: ' + param.data.value[5],
                        'Q3: ' + param.data.value[4],
                        'median: ' + param.data.value[3],
                        'Q1: ' + param.data.value[2],
                        'lower: ' + param.data.value[1]
                    ].join('<br/>')
                }
            }
        }
        // {
        //     name: 'outlier',
        //     type: 'scatter',
        //     data: []
        // }
    ]
}
export const option1_2 = {
    // color: ['#eb5e28', '#f27f34', '#f9a03f', '#f6b049', '#f3c053', '#a1c349', '#94b33d', '#87a330', '#799431',
    //     '#6a8532', '#ff0000', '#ff8700', '#ffd300', '#deff0a', '#a1ff0a', '#0aff99', '#0aefff', '#147df5', '#580aff', '#be0aff'
    // ],
    color: [
        '#ef8839',
        '#21c85d',
        '#fbb02d',
        '#ff0054',
        '#ff5400',
        '#f72585',
        '#41c1e9',
        '#7cb518',
        '#c46cfd',
        '#4cbcaf',
        '#3f9fe0',
        '#fb5607',
        '#8338ec',
        '#3a86ff',
        '#ffd23f',
        '#2ad4ad',
        '#0ead69',
        '#427aa1',
        '#679436'
    ],
    title: {
        left: 'center',
        textStyle: {
            fontSize: 24,
            fontWeight: 400,
            color: '#666666'
        },
        text: ''
    },
    legend: {
        data: [],
        top: 'center',
        right: 'left',
        orient: 'vertical',
        type: 'scroll',
        formatter: function (name) {
            // if (!name) return '';
            // if (name.length > 5) {
            //     name = name.slice(0, 5) + '...';
            //     return name
            // }
            let strs = name.split('') //字符串数组
            let str = ''
            for (let i = 0, s; (s = strs[i++]); ) {
                //遍历字符串数组
                str += s
                if (!(i % 10)) str += '\n' //按需要求余
            }
            return str
        },
        textStyle: {
            fontSize: 12
        }
    },
    grid: {
        top: '6%',
        left: '3%',
        right: '19%',
        bottom: 24,
        containLabel: true
    },
    tooltip: {
        trigger: 'item',
        axisPointer: {
            type: 'cross'
        },
        formatter: function (params) {
            if (params.value.length > 1 && params.value.length < 3) {
                return params.seriesName + ' :<br/>' + params.value[0] + ' , ' + params.value[1] + ''
            } else if (params.value.length > 2) {
                return params.seriesName + ' :' + params.value[2]
            } else {
                return params.seriesName + ' :<br/>' + params.name + ' , ' + params.value + ''
            }
        }
    },
    xAxis: {
        // type: 'value',
        // scale: true,
        // splitLine: {
        //     show: false
        // },
        // name: 'umap1',
        // nameLocation: 'center',
        // nameGap: 20,
        // nameTextStyle: {
        //     fontWeight: 'bolder',
        //     fontSize: 16
        // },
        // axisLine: {
        //     onZero: false
        // }
    },
    yAxis: {
        // type: 'value',
        // scale: true,
        // splitLine: {
        //     show: false
        // },
        // name: 'umap2',
        // nameLocation: 'center',
        // nameGap: 20,
        // nameTextStyle: {
        //     fontWeight: 'bolder',
        //     fontSize: 16
        // },
        // axisLine: {
        //     onZero: false
        // }
    },
    series: []
}
const hours = ['12a', '1a', '2a', '3a', '4a', '5a', '6a', '7a', '8a', '9a', '10a', '11a', '12p', '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p', '10p', '11p']
// prettier-ignore
const days = [
    'Saturday', 'Friday', 'Thursday',
    'Wednesday', 'Tuesday', 'Monday', 'Sunday'
];
const data2 = [
    [0, 0, 5],
    [0, 1, 1],
    [0, 2, 0],
    [0, 3, 0],
    [0, 4, 0],
    [0, 5, 0],
    [0, 6, 0],
    [0, 7, 0],
    [0, 8, 0],
    [0, 9, 0],
    [0, 10, 0],
    [0, 11, 2],
    [0, 12, 4],
    [0, 13, 1],
    [0, 14, 1],
    [0, 15, 3],
    [0, 16, 4],
    [0, 17, 6],
    [0, 18, 4],
    [0, 19, 4],
    [0, 20, 3],
    [0, 21, 3],
    [0, 22, 2],
    [0, 23, 5],
    [1, 0, 7],
    [1, 1, 0],
    [1, 2, 0],
    [1, 3, 0],
    [1, 4, 0],
    [1, 5, 0],
    [1, 6, 0],
    [1, 7, 0],
    [1, 8, 0],
    [1, 9, 0],
    [1, 10, 5],
    [1, 11, 2],
    [1, 12, 2],
    [1, 13, 6],
    [1, 14, 9],
    [1, 15, 11],
    [1, 16, 6],
    [1, 17, 7],
    [1, 18, 8],
    [1, 19, 12],
    [1, 20, 5],
    [1, 21, 5],
    [1, 22, 7],
    [1, 23, 2],
    [2, 0, 1],
    [2, 1, 1],
    [2, 2, 0],
    [2, 3, 0],
    [2, 4, 0],
    [2, 5, 0],
    [2, 6, 0],
    [2, 7, 0],
    [2, 8, 0],
    [2, 9, 0],
    [2, 10, 3],
    [2, 11, 2],
    [2, 12, 1],
    [2, 13, 9],
    [2, 14, 8],
    [2, 15, 10],
    [2, 16, 6],
    [2, 17, 5],
    [2, 18, 5],
    [2, 19, 5],
    [2, 20, 7],
    [2, 21, 4],
    [2, 22, 2],
    [2, 23, 4],
    [3, 0, 7],
    [3, 1, 3],
    [3, 2, 0],
    [3, 3, 0],
    [3, 4, 0],
    [3, 5, 0],
    [3, 6, 0],
    [3, 7, 0],
    [3, 8, 1],
    [3, 9, 0],
    [3, 10, 5],
    [3, 11, 4],
    [3, 12, 7],
    [3, 13, 14],
    [3, 14, 13],
    [3, 15, 12],
    [3, 16, 9],
    [3, 17, 5],
    [3, 18, 5],
    [3, 19, 10],
    [3, 20, 6],
    [3, 21, 4],
    [3, 22, 4],
    [3, 23, 1],
    [4, 0, 1],
    [4, 1, 3],
    [4, 2, 0],
    [4, 3, 0],
    [4, 4, 0],
    [4, 5, 1],
    [4, 6, 0],
    [4, 7, 0],
    [4, 8, 0],
    [4, 9, 2],
    [4, 10, 4],
    [4, 11, 4],
    [4, 12, 2],
    [4, 13, 4],
    [4, 14, 4],
    [4, 15, 14],
    [4, 16, 12],
    [4, 17, 1],
    [4, 18, 8],
    [4, 19, 5],
    [4, 20, 3],
    [4, 21, 7],
    [4, 22, 3],
    [4, 23, 0],
    [5, 0, 2],
    [5, 1, 1],
    [5, 2, 0],
    [5, 3, 3],
    [5, 4, 0],
    [5, 5, 0],
    [5, 6, 0],
    [5, 7, 0],
    [5, 8, 2],
    [5, 9, 0],
    [5, 10, 4],
    [5, 11, 1],
    [5, 12, 5],
    [5, 13, 10],
    [5, 14, 5],
    [5, 15, 7],
    [5, 16, 11],
    [5, 17, 6],
    [5, 18, 0],
    [5, 19, 5],
    [5, 20, 3],
    [5, 21, 4],
    [5, 22, 2],
    [5, 23, 0],
    [6, 0, 1],
    [6, 1, 0],
    [6, 2, 0],
    [6, 3, 0],
    [6, 4, 0],
    [6, 5, 0],
    [6, 6, 0],
    [6, 7, 0],
    [6, 8, 0],
    [6, 9, 0],
    [6, 10, 1],
    [6, 11, 0],
    [6, 12, 2],
    [6, 13, 1],
    [6, 14, 3],
    [6, 15, 4],
    [6, 16, 0],
    [6, 17, 0],
    [6, 18, 0],
    [6, 19, 0],
    [6, 20, 1],
    [6, 21, 2],
    [6, 22, 2],
    [6, 23, 6]
].map(function (item) {
    return [item[1], item[0], item[2] || '-']
})
export const option2 = {
    tooltip: {
        position: 'top'
    },
    grid: {
        height: '50%',
        top: '10%'
    },
    xAxis: {
        type: 'category',
        data: hours,
        splitArea: {
            show: true
        }
    },
    yAxis: {
        type: 'category',
        data: days,
        splitArea: {
            show: true
        }
    },
    visualMap: {
        min: 0,
        max: 10,
        calculable: true,
        orient: 'vertical',
        top: 'center',
        right: 10
    },
    series: [
        {
            name: 'Punch Card',
            type: 'heatmap',
            data: data2,
            label: {
                show: false
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
}

export const option3 = {
    tooltip: {
        position: 'top'
    },
    grid: {
        height: '50%',
        top: '10%'
    },
    xAxis: {
        type: 'category',
        data: hours,
        splitArea: {
            show: true
        }
    },
    yAxis: {
        type: 'category',
        data: days,
        splitArea: {
            show: true
        }
    },
    visualMap: {
        min: 0,
        max: 10,
        calculable: true,
        orient: 'vertical',
        top: 'center',
        right: 10
    },
    series: [
        {
            name: 'Punch Card',
            type: 'heatmap',
            data: data2,
            label: {
                show: false
            },
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
}

export const optionBar = {
    color: ['#f4a364'],
    title: {
        text: 'Number of expressed Gene',
        bottom: 10,
        left: 250
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: 45,
        containLabel: true
    },
    xAxis: {
        type: 'value'
    },
    yAxis: {
        type: 'category',
        data: ['Brazil', 'Indonesia', 'USA', 'India', 'China', 'World']
    },
    series: [
        {
            name: 'Expressed Gene',
            type: 'bar',
            barMaxWidth: 30,
            data: [18203, 23489, 29034, 104970, 131744, 630230]
        }
    ]
}
