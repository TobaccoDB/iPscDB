export const option1 = {
    // color: ['#ec6841', '#f19149', '#f7b551', '#ea68a2', '#eb6877', '#7fc269', '#31b16c', '#12b4b1', '#448ac9', '#556fb5'],
    // color: ['#eb5e28', '#f27f34', '#f9a03f', '#f6b049', '#f3c053', '#a1c349', '#94b33d', '#87a330', '#799431',
    //     '#6a8532', '#ff0000', '#ff8700', '#ffd300', '#deff0a', '#a1ff0a', '#0aff99', '#0aefff', '#147df5', '#580aff', '#be0aff'
    // ],
    color: ['#7089d8', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#5bc393', '#fc8452', '#ea7ccc', '#ff7cb1', '#8e8cd8', '#00b7c3', '#20bba1', '#40cb88', '#ce7cdb', '#ffb75f', '#38aae1', '#00bcd4', '#66bb6a', '#4abbb0', '#ee805d'],
    // legend: {
    //     type: 'scroll',
    //     data: [],
    //     top: 'center',
    //     right: 'left',
    //     orient: 'vertical',
    // },
    tooltip: {},
    grid: {
        top: '3%',
        left: '3%',
        right: '3%',
        // right: '20%',
        bottom: '3%',
        containLabel: true
    },
    yAxis: {
        data: [],
        splitLine: {
            lineStyle: {
                color: '#666'
            }
        },
        axisLine: {
            show: false,
            lineStyle: {
                color: '#666'
            }
        },
        axisLabel: {
            color: '#666',
            show: false
        },
        axisTick: {
            lineStyle: {
                color: '#666'
            }
        },
    },
    xAxis: {
        // type: 'value',
        axisLine: {
            show: false
        },
        axisTick: {
            show: false
        },
        axisLabel: {
            color: '#666'
        }
    },
    series: []
};

export const option2 = {
    // color: ['#eb5e28', '#f27f34', '#f9a03f', '#f6b049', '#f3c053', '#a1c349', '#94b33d', '#87a330', '#799431',
    //     '#6a8532', '#ff0000', '#ff8700', '#ffd300', '#deff0a', '#a1ff0a', '#0aff99', '#0aefff', '#147df5', '#580aff', '#be0aff'
    // ],
    color: ['#ef8839', '#21c85d', '#fbb02d', '#ff0054', '#ff5400', '#f72585', '#41c1e9', '#7cb518', '#c46cfd', '#4cbcaf', '#3f9fe0', '#fb5607', '#8338ec', '#3a86ff', '#ffd23f', '#2ad4ad', '#0ead69', '#427aa1', '#679436'],
    legend: {
        data: [],
        top: 'center',
        right: 'left',
        orient: 'vertical',
        formatter: function (name) {
            // if (!name) return '';
            // if (name.length > 5) {
            //     name = name.slice(0, 5) + '...';
            //     return name
            // }
            let strs = name.split(''); //字符串数组
            let str = ''
            for (let i = 0, s; s = strs[i++];) { //遍历字符串数组
                str += s;
                if (!(i % 20)) str += '\n'; //按需要求余
            }
            return str
        },
        textStyle: {
            fontSize: 9
        }
    },
    grid: {
        top: '3%',
        left: '3%',
        right: '20%',
        bottom: '3%',
        containLabel: true
    },
    tooltip: {
        trigger: 'item',
        axisPointer: {
            type: 'cross'
        },
        formatter: function (params) {
            if (params.value.length > 1) {
                return params.seriesName + ' :<br/>' +
                    params.value[0] + ' , ' +
                    params.value[1] + '';
            } else {
                return params.seriesName + ' :<br/>' +
                    params.name + ' , ' +
                    params.value + '';
            }
        },
    },
    xAxis: {
        type: 'value',
        scale: true,
        splitLine: {
            show: false
        },
        name: 'umap1',
        nameLocation: 'center',
        nameGap: 20,
        nameTextStyle: {
            fontWeight: 'bolder',
            fontSize: 16
        },
        axisLine: {
            onZero: false
        }
    },
    yAxis: {
        type: 'value',
        scale: true,
        splitLine: {
            show: false
        },
        name: 'umap2',
        nameLocation: 'center',
        nameGap: 20,
        nameTextStyle: {
            fontWeight: 'bolder',
            fontSize: 16
        },
        axisLine: {
            onZero: false
        }
    },
    series: []
};
export const option3 = {
    color: ['#eb5e28', '#f27f34', '#f9a03f', '#f6b049', '#f3c053', '#a1c349', '#94b33d', '#87a330', '#799431',
        '#6a8532', '#ff0000', '#ff8700', '#ffd300', '#deff0a', '#a1ff0a', '#0aff99', '#0aefff', '#147df5', '#580aff', '#be0aff'
    ],
    // title: {
    //     text: 'Dispersion of house price based on the area',
    //     left: 'center',
    //     top: 0
    // },
    visualMap: {
        top: 'center',
        right: 'left',
        orient: 'vertical',
        min: 0,
        max: 20,
        text: ['20', '0'],
        dimension: 2,
        // inRange: {
        //     color: ['#D7DA8B', '#E15457']
        // },
        itemGap: 0,
        // itemSymbol: 'circle',
        pieces: [{
                symbol: 'rect',
                gte: 20,
                color: '#E15457'
            },
            {
                symbol: 'rect',
                gte: 20,
                lt: 18,
                color: '#e1655e'
            },
            {
                symbol: 'rect',
                gte: 18,
                lt: 16,
                color: '#df7463'
            },
            {
                symbol: 'rect',
                gte: 16,
                lt: 14,
                color: '#de8369'
            },
            {
                symbol: 'rect',
                gte: 14,
                lt: 12,
                color: '#dd8e6d'
            },
            {
                symbol: 'rect',
                gte: 12,
                lt: 10,
                color: '#dc9d74'
            },
            {
                symbol: 'rect',
                gte: 10,
                lt: 8,
                color: '#daac79'
            },
            {
                symbol: 'rect',
                gte: 8,
                lt: 6,
                color: '#dab77d'
            },
            {
                symbol: 'rect',
                gte: 6,
                lt: 4,
                color: '#d9c583'
            },
            {
                symbol: 'rect',
                gte: 4,
                lt: 2,
                color: '#D7DA8B'
            },
            {
                symbol: 'rect',
                gte: 2,
                lt: 0,
                color: '#dddeb0'
            },
            {
                symbol: 'rect',
                value: 0,
                color: '#ccc'
            },
        ]
    },
    grid: {
        left: '3%',
        right: '20%',
        bottom: '3%',
        containLabel: true
    },
    tooltip: {
        trigger: 'item',
        axisPointer: {
            type: 'cross'
        },
        formatter: function (params) {
            return params.seriesName + ' : ' +
                params.value[2];
        },
    },
    xAxis: [{
        type: 'value',
        scale: true,
        splitLine: {
            show: false
        },
        name: 'umap1',
        nameLocation: 'center',
        nameGap: 20,
        nameTextStyle: {
            fontWeight: 'bolder',
            fontSize: 16
        },
        axisLine: {
            onZero: false
        }
    }],
    yAxis: [{
        type: 'value',
        scale: true,
        splitLine: {
            show: false
        },
        name: 'umap2',
        nameLocation: 'center',
        nameGap: 20,
        nameTextStyle: {
            fontWeight: 'bolder',
            fontSize: 16
        },
        axisLine: {
            onZero: false
        }
    }],
    series: [{
        name: 'umap',
        type: 'scatter',
        symbolSize: 2,
        // itemStyle: {
        //     normal: {
        //         borderWidth: 0.2,
        //         borderColor: '#fff'
        //     }
        // },
        data: []
    }]
};

export const option4 = {
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
        '#8980f5',
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
    legend: {
        data: [],
        top: 'center',
        right: 'left',
        orient: 'vertical',
        textStyle: {
            fontSize: 9,
        }
    },
    grid: {
        top: '3%',
        left: '3%',
        right: '20%',
        bottom: '3%',
        containLabel: true
    },
    tooltip: {
        trigger: 'item',
        axisPointer: {
            type: 'cross'
        },
        formatter: function (params) {
            if (params.value.length > 1) {
                return params.seriesName + ' :<br/>' +
                    params.value[0] + ' , ' +
                    params.value[1] + '';
            } else {
                return params.seriesName + ' :<br/>' +
                    params.name + ' , ' +
                    params.value + '';
            }
        },
    },
    xAxis: {
        type: 'value',
        scale: true,
        splitLine: {
            show: false
        },
        name: 'tsne1',
        nameLocation: 'center',
        nameGap: 20,
        nameTextStyle: {
            fontWeight: 'bolder',
            fontSize: 16
        },
        axisLine: {
            onZero: false
        }
    },
    yAxis: {
        type: 'value',
        scale: true,
        splitLine: {
            show: false
        },
        name: 'tsne2',
        nameLocation: 'center',
        nameGap: 20,
        nameTextStyle: {
            fontWeight: 'bolder',
            fontSize: 16
        },
        axisLine: {
            onZero: false
        }
    },
    series: []
};
export const option5 = {
    color: ['#eb5e28', '#f27f34', '#f9a03f', '#f6b049', '#f3c053', '#a1c349', '#94b33d', '#87a330', '#799431',
        '#6a8532', '#ff0000', '#ff8700', '#ffd300', '#deff0a', '#a1ff0a', '#0aff99', '#0aefff', '#147df5', '#580aff', '#be0aff'
    ],
    // title: {
    //     text: 'Dispersion of house price based on the area',
    //     left: 'center',
    //     top: 0
    // },
    visualMap: {
        top: 'center',
        right: 'left',
        orient: 'vertical',
        min: 0,
        max: 20,
        text: ['20', '0'],
        dimension: 2,
        // inRange: {
        //     color: ['#D7DA8B', '#E15457']
        // }
        itemGap: 0,
        pieces: [{
                symbol: 'rect',
                gte: 20,
                color: '#E15457'
            },
            {
                symbol: 'rect',
                gte: 20,
                lt: 18,
                color: '#e1655e'
            },
            {
                symbol: 'rect',
                gte: 18,
                lt: 16,
                color: '#df7463'
            },
            {
                symbol: 'rect',
                gte: 16,
                lt: 14,
                color: '#de8369'
            },
            {
                symbol: 'rect',
                gte: 14,
                lt: 12,
                color: '#dd8e6d'
            },
            {
                symbol: 'rect',
                gte: 12,
                lt: 10,
                color: '#dc9d74'
            },
            {
                symbol: 'rect',
                gte: 10,
                lt: 8,
                color: '#daac79'
            },
            {
                symbol: 'rect',
                gte: 8,
                lt: 6,
                color: '#dab77d'
            },
            {
                symbol: 'rect',
                gte: 6,
                lt: 4,
                color: '#d9c583'
            },
            {
                symbol: 'rect',
                gte: 4,
                lt: 2,
                color: '#D7DA8B'
            },
            {
                symbol: 'rect',
                gte: 2,
                lt: 0,
                color: '#dddeb0'
            },
            {
                symbol: 'rect',
                value: 0,
                color: '#ccc'
            },
        ]
    },
    grid: {
        left: '3%',
        right: '20%',
        bottom: '3%',
        containLabel: true
    },
    tooltip: {
        trigger: 'item',
        axisPointer: {
            type: 'cross'
        },
        formatter: function (params) {
            return params.seriesName + ' : ' +
                params.value[2];
        },
    },
    xAxis: [{
        type: 'value',
        scale: true,
        splitLine: {
            show: false
        },
        name: 'tsne1',
        nameLocation: 'center',
        nameGap: 20,
        nameTextStyle: {
            fontWeight: 'bolder',
            fontSize: 16
        },
        axisLine: {
            onZero: false
        }
    }],
    yAxis: [{
        type: 'value',
        scale: true,
        splitLine: {
            show: false
        },
        name: 'tsne2',
        nameLocation: 'center',
        nameGap: 20,
        nameTextStyle: {
            fontWeight: 'bolder',
            fontSize: 16
        },
        axisLine: {
            onZero: false
        }
    }],
    series: [{
        name: 'tsne',
        type: 'scatter',
        symbolSize: 2,
        // itemStyle: {
        //     normal: {
        //         borderWidth: 0.2,
        //         borderColor: '#fff'
        //     }
        // },
        data: []
    }]
};