export const option = {
    tooltip: {
        trigger: 'item',
        triggerOn: 'mousemove'
    },
    series: [
        {
            type: 'tree',
            data: [],
            top: '1%',
            left: '10%',
            bottom: '1%',
            right: '12%',
            symbolSize: 7,
            itemStyle: {
                borderColor: '#24A461'
            },
            label: {
                position: 'left',
                verticalAlign: 'middle',
                align: 'right',
                fontSize: 12
            },
            leaves: {
                label: {
                    position: 'right',
                    verticalAlign: 'middle',
                    align: 'left'
                }
            },
            emphasis: {
                focus: 'descendant'
            },
            initialTreeDepth: -1,
            expandAndCollapse: true,
            animationDuration: 550,
            animationDurationUpdate: 750
        }
    ]
}

export const column = [
    {
        key: 'cell_type',
        label: 'Cell Type'
    },
    {
        key: 'type',
        label: 'Type'
    },
    {
        key: 'parent',
        label: 'Parent'
    }
]
