export const option1 = {
    color: ['#21C85D', '#EF8839', '#2AD4AD', '#41C1E9', '#7CB518', '#FFD23F'],
    title: {
        text: 'Cells',
        left: 'center',
        bottom: 0,
        textStyle: {
            color: '#333',
            fontSize: 16
        }
    },
    tooltip: {
        trigger: 'item',
        formatter: '{b} : {c} ({d}%)'
    },
    series: [
        {
            name: 'Cells',
            type: 'pie',
            radius: '50%',
            data: [],
            label: {
                color: '#333333',
                fontSize: 11
                // formatter(v) {
                //     let text = v.name
                //     let count = text.indexOf(' ')
                //     console.log()
                //     return text.length < count ?
                //         text :
                //         `${text.slice(0,count)}\n${text.slice(count)}`
                // }
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
export const option2 = {
    color: ['#21C85D', '#EF8839', '#2AD4AD', '#41C1E9', '#7CB518', '#FFD23F'],
    title: {
        text: 'Sequencing technology',
        left: 'center',
        bottom: 0,
        textStyle: {
            color: '#333',
            fontSize: 16
        }
    },
    tooltip: {
        trigger: 'item',
        formatter: '{b} : {c} ({d}%)'
    },
    series: [
        {
            name: 'Sequencing technology',
            type: 'pie',
            radius: '50%',
            data: [],
            label: {
                color: '#333333',
                fontSize: 11
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

export const option3 = {
    color: ['#21C85D', '#EF8839', '#2AD4AD', '#41C1E9', '#7CB518', '#FFD23F'],
    title: {
        text: 'Markers',
        left: 'center',
        bottom: 0,
        textStyle: {
            color: '#333',
            fontSize: 16
        }
    },
    tooltip: {
        trigger: 'item',
        formatter: '{b} : {c} ({d}%)'
    },
    series: [
        {
            name: 'Markers',
            type: 'pie',
            radius: '50%',
            data: [],
            label: {
                color: '#333333',
                fontSize: 11
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

export const column = [
    // {
    //     key: 'lit_id',
    //     label: 'Lit ID',
    //     width: 80
    // },
    {
        key: 'species_name',
        label: 'Species',
        width: 160
    },
    // {
    //     key: 'doi',
    //     label: 'DOI',
    //     width: 300
    // },
    {
        key: 'title',
        label: 'Title'
    },
    {
        key: 'pmid',
        label: 'PMID',
        width: 100
    },
    {
        key: 'project_id',
        label: 'Project ID',
        width: 120
    },
    {
        key: 'tissue',
        label: 'Tissue',
        width: 100
    },
    {
        key: 'chemistry',
        label: 'Platform',
        width: 100
    },
    {
        key: 'qc_cells',
        label: 'Cell Number',
        width: 110
    }
]
