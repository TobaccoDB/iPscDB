export const option1 = {
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
        max: 5,
        text: ['5', '0'],
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
            // return params.seriesName + ' : ' +
            //     params.value[2];
            return params.value[2];
        },
    },
    xAxis: [{
        type: 'value',
        scale: true,
        splitLine: {
            show: false
        },
        name: '',
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
        name: '',
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
        name: '',
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