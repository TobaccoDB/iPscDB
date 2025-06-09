export const option1 = {
    // color: ['#eb5e28', '#f27f34', '#f9a03f', '#f6b049', '#f3c053', '#a1c349', '#94b33d', '#87a330', '#799431',
    //     '#6a8532', '#ff0000', '#ff8700', '#ffd300', '#deff0a', '#a1ff0a', '#0aff99', '#0aefff', '#147df5', '#580aff', '#be0aff'
    // ],
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
export const option3 = {
    // color: ['#eb5e28', '#f27f34', '#f9a03f', '#f6b049', '#f3c053', '#a1c349', '#94b33d', '#87a330', '#799431',
    //     '#6a8532', '#ff0000', '#ff8700', '#ffd300', '#deff0a', '#a1ff0a', '#0aff99', '#0aefff', '#147df5', '#580aff', '#be0aff'
    // ],
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
export const option2_2 = {
    color: ['#ef8839', '#21c85d', '#fbb02d', '#ff0054', '#ff5400', '#f72585', '#41c1e9', '#7cb518', '#c46cfd', '#4cbcaf', '#3f9fe0', '#fb5607', '#8338ec', '#3a86ff', '#ffd23f', '#2ad4ad', '#0ead69', '#427aa1', '#679436'],
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
        top: '6%',
        left: '3%',
        right: '19%',
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
    xAxis: {},
    yAxis: {},
    series: []
};
export const option2_1 = {
    color: ['#ef8839', '#21c85d', '#fbb02d', '#ff0054', '#ff5400', '#f72585', '#41c1e9', '#7cb518', '#c46cfd', '#4cbcaf', '#3f9fe0', '#fb5607', '#8338ec', '#3a86ff', '#ffd23f', '#2ad4ad', '#0ead69', '#427aa1', '#679436'],
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
        right: 100,
        orient: 'vertical',
        type: 'scroll',
        formatter: function (name) {
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
        top: '6%',
        left: '3%',
        right: '19%',
        bottom: '3%',
        containLabel: true
    },
    tooltip: {
        trigger: 'item',
        axisPointer: {
            type: 'cross'
        },
        formatter: function (params) {
            if (params.value.length > 1 && params.value.length < 3) {
                return params.seriesName + ' :<br/>' +
                    params.value[0] + ' , ' +
                    params.value[1] + '';
            } else if (params.value.length > 2) {
                return params.seriesName + ' :' + params.value[2];
            } else {
                return params.seriesName + ' :<br/>' +
                    params.name + ' , ' +
                    params.value + '';
            }
        },
    },
    xAxis: {},
    yAxis: {},
    series: []
};
export const option2_3 = {
    // color: ['#eb5e28', '#f27f34', '#f9a03f', '#f6b049', '#f3c053', '#a1c349', '#94b33d', '#87a330', '#799431',
    //     '#6a8532', '#ff0000', '#ff8700', '#ffd300', '#deff0a', '#a1ff0a', '#0aff99', '#0aefff', '#147df5', '#580aff', '#be0aff'
    // ],
    color: ['#ef8839', '#21c85d', '#fbb02d', '#ff0054', '#ff5400', '#f72585', '#41c1e9', '#7cb518', '#c46cfd', '#4cbcaf', '#3f9fe0', '#fb5607', '#8338ec', '#3a86ff', '#ffd23f', '#2ad4ad', '#0ead69', '#427aa1', '#679436'],
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
        right: 100,
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
        top: '6%',
        left: '3%',
        right: '19%',
        bottom: '3%',
        containLabel: true
    },
    tooltip: {
        trigger: 'item',
        axisPointer: {
            type: 'cross'
        },
        formatter: function (params) {
            if (params.value.length > 1 && params.value.length < 3) {
                return params.seriesName + ' :<br/>' +
                    params.value[0] + ' , ' +
                    params.value[1] + '';
            } else if (params.value.length > 2) {
                return params.seriesName + ' :' + params.value[2];
            } else {
                return params.seriesName + ' :<br/>' +
                    params.name + ' , ' +
                    params.value + '';
            }
        },
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
};