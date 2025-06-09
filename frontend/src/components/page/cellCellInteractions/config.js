export const option1 = {
    // color: ['#eb5e28', '#f27f34', '#f9a03f', '#f6b049', '#f3c053', '#a1c349', '#94b33d', '#87a330', '#799431',
    //     '#6a8532', '#ff0000', '#ff8700', '#ffd300', '#deff0a', '#a1ff0a', '#0aff99', '#0aefff', '#147df5', '#580aff', '#be0aff'
    // ],
    title: {
        left: 'center',
        textStyle: {
            fontSize: 14,
            fontWeight: 400,
            color: '#666666'
        },
        bottom: 0,
        text: 'Reference atlas'
    },
    color: ['#ef8839', '#21c85d', '#fbb02d', '#ff0054', '#ff5400', '#f72585', '#41c1e9', '#7cb518', '#c46cfd', '#4cbcaf', '#3f9fe0', '#fb5607', '#8338ec', '#3a86ff', '#ffd23f', '#2ad4ad', '#0ead69', '#427aa1', '#679436'],
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
            let strs = name.split(''); //字符串数组
            let str = ''
            for (let i = 0, s; s = strs[i++];) { //遍历字符串数组
                str += s;
                if (!(i % 10)) str += '\n'; //按需要求余
            }
            return str
        },
        textStyle: {
            fontSize: 12
        }
    },
    grid: {
        top: '3%',
        left: '3%',
        right: '28%',
        bottom: '10%',
        containLabel: true
    },
    // tooltip: {
    //     trigger: 'item',
    //     axisPointer: {
    //         type: 'cross'
    //     },
    //     formatter: function (params) {
    //         if (params.value.length > 1) {
    //             return params.seriesName + ' :<br/>' +
    //                 params.value[0] + ' , ' +
    //                 params.value[1] + '';
    //         } else {
    //             return params.seriesName + ' :<br/>' +
    //                 params.name + ' , ' +
    //                 params.value + '';
    //         }
    //     },
    // },
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
};
export const option2 = {
    // color: ['#eb5e28', '#f27f34', '#f9a03f', '#f6b049', '#f3c053', '#a1c349', '#94b33d', '#87a330', '#799431',
    //     '#6a8532', '#ff0000', '#ff8700', '#ffd300', '#deff0a', '#a1ff0a', '#0aff99', '#0aefff', '#147df5', '#580aff', '#be0aff'
    // ],
    title: {
        left: 'center',
        textStyle: {
            fontSize: 14,
            fontWeight: 400,
            color: '#666666'
        },
        bottom: 0,
        text: 'Ligand gene'
    },
    color: ['#ef8839', '#21c85d', '#fbb02d', '#ff0054', '#ff5400', '#f72585', '#41c1e9', '#7cb518', '#c46cfd', '#4cbcaf', '#3f9fe0', '#fb5607', '#8338ec', '#3a86ff', '#ffd23f', '#2ad4ad', '#0ead69', '#427aa1', '#679436'],
    legend: {
        show: false,
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
            let strs = name.split(''); //字符串数组
            let str = ''
            for (let i = 0, s; s = strs[i++];) { //遍历字符串数组
                str += s;
                if (!(i % 10)) str += '\n'; //按需要求余
            }
            return str
        },
        textStyle: {
            fontSize: 12
        }
    },
    visualMap: {
        show: true,
        top: 'center',
        right: 'left',
        orient: 'vertical',
        min: 0,
        max: 2,
        text: ['2', '0'],
        dimension: 2,
        inRange: {
            color: ['#ccc', '#E15457']
        },
        itemGap: 0,
    },
    grid: {
        top: '3%',
        left: '3%',
        right: '28%',
        bottom: '10%',
        containLabel: true
    },
    // tooltip: {
    //     trigger: 'item',
    //     axisPointer: {
    //         type: 'cross'
    //     },
    //     formatter: function (params) {
    //         if (params.value.length > 1 && params.value.length < 3) {
    //             return params.seriesName + ' :<br/>' +
    //                 params.value[0] + ' , ' +
    //                 params.value[1] + '';
    //         } else if (params.value.length > 2) {
    //             return params.seriesName + ' :' + params.value[2];
    //         } else {
    //             return params.seriesName + ' :<br/>' +
    //                 params.name + ' , ' +
    //                 params.value + '';
    //         }
    //     },
    // },
    xAxis: {},
    yAxis: {},
    series: []
};
export const option3 = {
    // color: ['#eb5e28', '#f27f34', '#f9a03f', '#f6b049', '#f3c053', '#a1c349', '#94b33d', '#87a330', '#799431',
    //     '#6a8532', '#ff0000', '#ff8700', '#ffd300', '#deff0a', '#a1ff0a', '#0aff99', '#0aefff', '#147df5', '#580aff', '#be0aff'
    // ],
    title: {
        left: 'center',
        textStyle: {
            fontSize: 14,
            fontWeight: 400,
            color: '#666666'
        },
        bottom: 0,
        text: 'Receptor gene'
    },
    color: ['#ef8839', '#21c85d', '#fbb02d', '#ff0054', '#ff5400', '#f72585', '#41c1e9', '#7cb518', '#c46cfd', '#4cbcaf', '#3f9fe0', '#fb5607', '#8338ec', '#3a86ff', '#ffd23f', '#2ad4ad', '#0ead69', '#427aa1', '#679436'],
    legend: {
        show: false,
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
            let strs = name.split(''); //字符串数组
            let str = ''
            for (let i = 0, s; s = strs[i++];) { //遍历字符串数组
                str += s;
                if (!(i % 10)) str += '\n'; //按需要求余
            }
            return str
        },
        textStyle: {
            fontSize: 12
        }
    },
    visualMap: {
        show: true,
        top: 'center',
        right: 'left',
        orient: 'vertical',
        min: 0,
        max: 2,
        text: ['2', '0'],
        dimension: 2,
        inRange: {
            color: ['#ccc', '#E15457']
        },
        itemGap: 0,
    },
    grid: {
        top: '3%',
        left: '3%',
        right: '28%',
        bottom: '10%',
        containLabel: true
    },
    // tooltip: {
    //     trigger: 'item',
    //     axisPointer: {
    //         type: 'cross'
    //     },
    //     formatter: function (params) {
    //         if (params.value.length > 1 && params.value.length < 3) {
    //             return params.seriesName + ' :<br/>' +
    //                 params.value[0] + ' , ' +
    //                 params.value[1] + '';
    //         } else if (params.value.length > 2) {
    //             return params.seriesName + ' :' + params.value[2];
    //         } else {
    //             return params.seriesName + ' :<br/>' +
    //                 params.name + ' , ' +
    //                 params.value + '';
    //         }
    //     },
    // },
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
};
export const column = [{
        key: 'Ligands',
        label: 'Ligands'
    },
    {
        key: 'Receptors',
        label: 'Receptors'
    },
    {
        key: 'Ligands_cell',
        label: 'Ligands Cell'
    },
    {
        key: 'Receptors_cell',
        label: 'Receptors Cell'
    },
    {
        key: 'Ligands_expr',
        label: 'Ligands Expr'
    },
    {
        key: 'Receptors_expr',
        label: 'Receptors Expr'
    },
    {
        key: 'Score',
        label: 'Score',
        sortable: 'custom'
    },
    // {
    //     key: 'Pvalue',
    //     label: 'Pvalue'
    // },
    // {
    //     key: 'Type',
    //     label: 'Type'
    // },
]

export const optionRight1 = {
    title: {
        left: 'center',
        textStyle: {
            fontSize: 14,
            fontWeight: 400,
            color: '#666666'
        },
        top: 8,
        text: 'LR-Pairs number in cell type'
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
        bottom: '0',
        top: '15%',
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
        },
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
    series: [{
        // name: 'Cell Number in Each Cell Type',
        type: 'bar',
        data: [],
        barMaxWidth: 20,
    }]
};