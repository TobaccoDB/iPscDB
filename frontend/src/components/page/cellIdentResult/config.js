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