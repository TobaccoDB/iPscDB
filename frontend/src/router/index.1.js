import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
    mode: 'history',
    // base: '/pcmdb/',
    base: '/ipscdb/',
    // base: 'test',
    routes: [{
            path: '/',
            redirect: '/homePage'
        },
        {
            path: '/',
            component: (resolve) => require(['../components/common/Home.vue'], resolve),
            meta: {
                title: '系统首页'
            },
            children: [{
                    path: '/homePage',
                    component: (resolve) => require(['../components/page/homePage/index.vue'], resolve),
                    meta: {
                        title: '系统首页'
                    }
                },
                {
                    path: '/searchTable',
                    name: 'searchTable',
                    component: (resolve) => require(['../components/page/searchTable/index.vue'], resolve),
                    meta: {
                        title: '搜索结果'
                    }
                },
                {
                    path: '/searchForm',
                    name: 'searchForm',
                    component: (resolve) => require(['../components/page/searchForm/index.vue'], resolve),
                    meta: {
                        title: 'Search'
                    }
                },
                {
                    path: '/searchMarker',
                    name: 'searchMarker',
                    component: (resolve) => require(['../components/page/searchForm/marker.vue'], resolve),
                    meta: {
                        title: 'Search'
                    }
                },
                {
                    path: '/searchBlast',
                    name: 'searchBlast',
                    component: (resolve) => require(['../components/page/searchForm/blast/index.vue'], resolve),
                    meta: {
                        title: 'Search'
                    }
                },
                {
                    path: '/searchCellType',
                    name: 'searchCellType',
                    component: (resolve) => require(['../components/page/searchForm/CellType.vue'], resolve),
                    meta: {
                        title: 'Search'
                    }
                },
                // {
                //     path: '/searchBlast',
                //     name: 'searchBlast',
                //     component: (resolve) => require(['../components/page/searchForm/Blast.vue'], resolve),
                //     meta: {
                //         title: 'Search'
                //     }
                // },
                {
                    path: '/homePage100',
                    component: (resolve) => require(['../components/page/homePage/index-100.vue'], resolve),
                    meta: {
                        title: '系统首页'
                    }
                },
                {
                    path: '/browse',
                    component: (resolve) => require(['../components/page/browse/index.vue'], resolve),
                    meta: {
                        keepAlive: true, // 需要缓存
                        title: 'browse'
                    }
                },
                {
                    path: '/Integration',
                    component: (resolve) => require(['../components/page/search/index.vue'], resolve),
                    meta: {
                        // keepAlive: true, // 需要缓存
                        title: 'Integration'
                    }
                },
                {
                    path: '/integrationDetails',
                    component: (resolve) => require(['../components/page/integrationDetails/index.vue'], resolve),
                    meta: {
                        title: 'integrationDetails'
                    }
                },
                {
                    path: '/integrationNewDetails',
                    component: (resolve) => require(['../components/page/integrationNewDetails/index.vue'], resolve),
                    meta: {
                        title: 'integrationNewDetails'
                    }
                },
                {
                    path: '/searchResult',
                    component: (resolve) => require(['../components/page/searchResult/index.vue'], resolve),
                    meta: {
                        title: 'searchResult'
                    }
                },
                {
                    path: '/projectResult',
                    component: (resolve) => require(['../components/page/projectResult/index.vue'], resolve),
                    meta: {
                        title: 'projectResult'
                    }
                },
                {
                    path: '/searchList',
                    component: (resolve) => require(['../components/page/searchList/index.vue'], resolve),
                    meta: {
                        title: 'searchList'
                    }
                },
                {
                    path: '/searchDetails',
                    component: (resolve) => require(['../components/page/searchDetails/index.vue'], resolve),
                    meta: {
                        title: 'searchDetails'
                    }
                },
                {
                    path: '/scsa',
                    component: (resolve) => require(['../components/page/scsa/index.vue'], resolve),
                    meta: {
                        keepAlive: true, // 需要缓存
                        title: 'scsa'
                    }
                },
                {
                    path: '/sampleDetails',
                    component: (resolve) => require(['../components/page/sampleDetails/index.vue'], resolve),
                    meta: {
                        title: 'sampleDetails'
                    }
                },
                {
                    path: '/sampleQCNew',
                    component: (resolve) => require(['../components/page/sampleQCNew/index.vue'], resolve),
                    meta: {
                        title: 'sampleQCNew'
                    }
                },
                {
                    path: '/sampleQCFilter',
                    component: (resolve) => require(['../components/page/sampleQCFilter/index.vue'], resolve),
                    meta: {
                        title: 'sampleQCFilter'
                    }
                },
                {
                    path: '/sampleQC',
                    component: (resolve) => require(['../components/page/sampleQC/index.vue'], resolve),
                    meta: {
                        // keepAlive: true, // 需要缓存
                        title: 'sampleQC'
                    }
                },
                {
                    path: '/cellIdentification',
                    component: (resolve) => require(['../components/page/cellIdentification/index.vue'], resolve),
                    meta: {
                        title: 'cellIdentification'
                    }
                },
                {
                    path: '/cellIdentificationScope',
                    component: (resolve) => require(['../components/page/cellIdentificationScope/index.vue'], resolve),
                    meta: {
                        title: 'cellIdentificationScope'
                    }
                },
                {
                    path: '/atlas',
                    component: (resolve) => require(['../components/page/atlas/index.vue'], resolve),
                    meta: {
                        title: 'atlas'
                    }
                },
                {
                    path: '/projectAtlas',
                    component: (resolve) => require(['../components/page/projectAtlas/index.vue'], resolve),
                    meta: {
                        title: 'projectAtlas'
                    }
                },
                {
                    path: '/marker',
                    component: (resolve) => require(['../components/page/marker/index.vue'], resolve),
                    meta: {
                        title: 'marker'
                    }
                },
                {
                    path: '/markerCell',
                    component: (resolve) => require(['../components/page/markerCell/index.vue'], resolve),
                    meta: {
                        title: 'marker'
                    }
                },
                {
                    path: '/markerDefault',
                    component: (resolve) => require(['../components/page/markerDefault/index.vue'], resolve),
                    meta: {
                        title: 'markerDefault'
                    }
                },
                {
                    path: '/Refrence',
                    component: (resolve) => require(['../components/page/Refrence/index.vue'], resolve),
                    meta: {
                        title: 'Refrence'
                    }
                },
                {
                    path: '/cellIdent',
                    component: (resolve) => require(['../components/page/cellIdent/index.vue'], resolve),
                    meta: {
                        title: 'cellIdent'
                    }
                },
                {
                    path: '/cellIdentResult',
                    component: (resolve) => require(['../components/page/cellIdentResult/index.vue'], resolve),
                    meta: {
                        title: 'cellIdentResult'
                    }
                },
                {
                    path: '/identificationDetails',
                    component: (resolve) => require(['../components/page/identificationDetails/index.vue'], resolve),
                    meta: {
                        title: 'identificationDetails'
                    }
                },
                {
                    path: '/geneExpression',
                    component: (resolve) => require(['../components/page/geneExpression/index.vue'], resolve),
                    meta: {
                        // keepAlive: true, // 需要缓存
                        title: 'geneExpression'
                    }
                },
                {
                    path: '/singleRDetails',
                    component: (resolve) => require(['../components/page/singleRDetails/index.vue'], resolve),
                    meta: {
                        title: 'singleRDetails'
                    }
                },
                // {
                //     path: '/CMPredictor',
                //     component: resolve => require(['../components/page/CMPredictor/index.vue'], resolve),
                //     meta: {
                //         keepAlive: true, // 需要缓存
                //         title: 'CMPredictor'
                //     }
                // },
                {
                    path: '/CMPredictorDetails',
                    component: (resolve) => require(['../components/page/CMPredictorDetails/index.vue'], resolve),
                    meta: {
                        title: 'CMPredictorRDetails'
                    }
                },
                {
                    path: '/blast',
                    component: (resolve) => require(['../components/page/blast/index.vue'], resolve),
                    meta: {
                        keepAlive: true, // 需要缓存
                        title: 'blast'
                    }
                },
                {
                    path: '/documentDetails',
                    component: (resolve) => require(['../components/page/documentDetails/index.vue'], resolve),
                    meta: {
                        title: 'documentDetails'
                    }
                },
                {
                    path: '/submit',
                    component: (resolve) => require(['../components/page/submit/index.vue'], resolve),
                    meta: {
                        title: 'submit'
                    }
                },
                {
                    path: '/download',
                    component: (resolve) => require(['../components/page/download/index.vue'], resolve),
                    meta: {
                        title: 'download'
                    }
                },
                {
                    path: '/tissueStructure',
                    component: (resolve) => require(['../components/page/tissueStructure/index.vue'], resolve),
                    meta: {
                        title: 'tissueStructure'
                    }
                },
                {
                    path: '/eSCP',
                    component: (resolve) => require(['../components/page/eSCP/index.vue'], resolve),
                    meta: {
                        title: 'eSCP'
                    }
                },
                {
                    path: '/monocle',
                    component: (resolve) => require(['../components/page/monocle/index.vue'], resolve),
                    meta: {
                        title: 'monocle'
                    }
                },
                {
                    path: '/monocleExpressed',
                    component: (resolve) => require(['../components/page/monocleExpressed/index.vue'], resolve),
                    meta: {
                        title: 'monocleExpressed'
                    }
                },
                {
                    path: '/monocleDifferential',
                    component: (resolve) => require(['../components/page/monocleDifferential/index.vue'], resolve),
                    meta: {
                        title: 'monocleDifferential'
                    }
                },
                {
                    path: '/tools',
                    component: (resolve) => require(['../components/page/tools/index.vue'], resolve),
                    meta: {
                        title: 'tools'
                    }
                },
                // {
                //     path: '/cellAnnotation',
                //     component: (resolve) => require(['../components/page/cellAnnotation/index.vue'], resolve),
                //     meta: {
                //         title: 'cellAnnotation'
                //     }
                // },
                {
                    path: '/cellid',
                    component: (resolve) => require(['../components/page/cellid/index2.vue'], resolve),
                    meta: {
                        title: 'cellid'
                    },
                    children: [{
                            path: '',
                            component: (resolve) => require(['../components/page/cellid/index.vue'], resolve),
                            meta: {
                                title: 'cellid'
                            }
                        },
                        {
                            path: '/cellAnnotation',
                            component: (resolve) => require(['../components/page/cellAnnotation/index.vue'], resolve),
                            meta: {
                                title: 'cellAnnotation'
                            }
                        }
                    ]
                },
                {
                    path: '/cellblast2',
                    component: (resolve) => require(['../components/page/cellBlast/index.vue'], resolve),
                    meta: {
                        title: 'cellBlast'
                    }
                },
                {
                    path: '/cellblast',
                    component: (resolve) => require(['../components/page/cellBlast/index2.vue'], resolve),
                    meta: {
                        title: 'cellBlast'
                    }
                },
                {
                    path: '/mtsc',
                    component: (resolve) => require(['../components/page/mtsc/index2.vue'], resolve),
                    meta: {
                        title: 'mtsc'
                    }
                },
                {
                    path: '/downLoadFile',
                    component: (resolve) => require(['../components/page/downLoadFile/index.vue'], resolve),
                    meta: {
                        title: 'downLoadFile'
                    }
                },
                {
                    path: '/mtsc1',
                    component: (resolve) => require(['../components/page/mtsc/index.vue'], resolve),
                    meta: {
                        title: 'mtsc1'
                    }
                },
                {
                    path: '/cellAnnotationResult',
                    component: (resolve) => require(['../components/page/cellAnnotationResult/index.vue'], resolve),
                    meta: {
                        title: 'cellAnnotationResult'
                    }
                },
                {
                    path: '/cellCellInteractions',
                    component: (resolve) => require(['../components/page/cellCellInteractions/index.vue'], resolve),
                    meta: {
                        title: 'cellCellInteractions'
                    }
                },
                {
                    path: '/Contact',
                    component: (resolve) => require(['../components/page/Contact/index.vue'], resolve),
                    meta: {
                        title: 'Contact'
                    }
                },
                {
                    path: '/UpdateLog',
                    component: (resolve) => require(['../components/page/UpdateLog/index.vue'], resolve),
                    meta: {
                        title: 'UpdateLog'
                    }
                },
                {
                    path: '/predct1',
                    component: (resolve) => require(['../components/page/predct/index.vue'], resolve),
                    meta: {
                        title: 'UpdateLog'
                    }
                },
                {
                    path: '/predct2',
                    component: (resolve) => require(['../components/page/predct/index.vue'], resolve),
                    meta: {
                        title: 'UpdateLog'
                    }
                },
                {
                    path: '/predct3',
                    component: (resolve) => require(['../components/page/predct/index.vue'], resolve),
                    meta: {
                        title: 'UpdateLog'
                    }
                },
                {
                    path: '/documentation',
                    component: (resolve) => require(['../components/page/documentation/index.vue'], resolve),
                    meta: {
                        title: 'documentation'
                    },
                    children: [{
                            path: '',
                            component: (resolve) => require(['../components/page/documentation/index1.vue'], resolve),
                            meta: {
                                title: 'documentation1'
                            }
                        },
                        {
                            path: '/documentation2',
                            component: (resolve) => require(['../components/page/documentation/index2.vue'], resolve),
                            meta: {
                                title: 'documentation2'
                            }
                        },
                        {
                            path: '/documentation3',
                            component: (resolve) => require(['../components/page/documentation/index3.vue'], resolve),
                            meta: {
                                title: 'documentation3'
                            }
                        },
                        {
                            path: '/documentation4',
                            component: (resolve) => require(['../components/page/documentation/index4.vue'], resolve),
                            meta: {
                                title: 'documentation4'
                            }
                        },
                    ]
                },
                {
                    path: '/analysisFromCellranger',
                    component: (resolve) => require(['../components/page/dataAnalysis/analysisFromCellranger/index.vue'], resolve),
                    meta: {
                        title: 'analysisFromCellranger'
                    }
                },
                {
                    path: '/CellRanger',
                    component: (resolve) => require(['../components/page/dataAnalysis/CellRanger/index.vue'], resolve),
                    meta: {
                        title: 'CellRanger'
                    }
                },
                {
                    path: '/DataAnalysisSampleQC',
                    component: (resolve) => require(['../components/page/dataAnalysis/SampleQC/index.vue'], resolve),
                    meta: {
                        title: 'SampleQC'
                    }
                },
                {
                    path: '/DataProcess',
                    component: (resolve) => require(['../components/page/dataAnalysis/DataProcess/index.vue'], resolve),
                    meta: {
                        title: 'DataProcess'
                    }
                },
                {
                    path: '/Cluster',
                    component: (resolve) => require(['../components/page/dataAnalysis/Cluster/index.vue'], resolve),
                    meta: {
                        title: 'Cluster'
                    }
                },
                {
                    path: '/DataAnalysisCellAnnotation',
                    component: (resolve) => require(['../components/page/dataAnalysis/CellAnnotation/index.vue'], resolve),
                    meta: {
                        title: 'CellAnnotation'
                    }
                },
                {
                    path: '/analysisFromSampleQC',
                    component: (resolve) => require(['../components/page/dataAnalysis/analysisFromSampleQC/index.vue'], resolve),
                    meta: {
                        title: 'analysisFromSampleQC'
                    }
                },
                {
                    path: '/SampleSampleQC',
                    component: (resolve) => require(['../components/page/dataAnalysis/SampleSampleQC/index.vue'], resolve),
                    meta: {
                        title: 'SampleSampleQC'
                    }
                },

            ]
        },
        {
            path: '/detailInfo',
            component: (resolve) => require(['../components/page/searchDetails/detailInfo.vue'], resolve),
            meta: {
                title: 'detailInfo'
            }
        },
        {
            path: '/403',
            component: (resolve) => require(['../components/page/403.vue'], resolve),
            meta: {
                title: '403'
            }
        },
        {
            path: '*',
            component: (resolve) => require(['../components/page/404.vue'], resolve),
            meta: {
                title: '404'
            }
        }
    ]
})

const VueRouterPush = Router.prototype.push

Router.prototype.push = function push(to) {

    return VueRouterPush.call(this, to).catch(err => err)

}