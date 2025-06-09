<template>
    <div class="markerDefault">
        <!-- <div class="markerDefault-header">
            <el-select v-model="headerValue" placeholder="请选择" style="width: 244px; height: 40px">
                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
            </el-select>
        </div> -->
        <div class="markerDefault-body">
            <!-- <div class="markerDefault-body-left">
                <div class="markerDefault-body-left-main">
                    <MarkerTree></MarkerTree>
                </div>
            </div> -->
            <div class="markerDefault-body-right">
                <div class="markerDefault-body-right-name">{{ selectValue.name }}</div>
                <div class="markerDefault-body-right-number">
                    <div class="markerDefault-body-right-number-item" v-for="(item, index) in titleData" :key="index">
                        <div class="markerDefault-body-right-number-item-name">{{ item.name }}</div>
                        <div class="markerDefault-body-right-number-item-value">
                            <span :style="{ borderColor: item.color }">{{ index == 0 ? selectValue.classic_number : index == 1 ? selectValue.gene_number : selectValue.node_number }}</span>
                        </div>
                    </div>
                </div>
                <div class="markerDefault-body-right-title" style="margin-bottom: 8px">{{ selectValue.level == 2 ? 'Tissue ID' : 'Celltype ID' }}</div>
                <div class="markerDefault-body-right-content" style="margin-bottom: 18px">
                    <span style="color: #333; font-weight: bold; font-size: 14px; margin-right: 12px">{{ info.po_id }}</span>
                    <span>{{ info.celltype_id }}</span>
                </div>
                <div class="markerDefault-body-right-title">Description</div>
                <div class="markerDefault-body-right-content" style="margin-bottom: 16px">
                    <span style="font-size: 14px">{{ info.description }}</span>
                </div>
                <div class="markerDefault-body-right-WordCloud">
                    <WordCloud :infoData="workData"></WordCloud>
                </div>
                <div class="markerDefault-body-right-title" style="margin-bottom: 10px">Marker Table</div>
                <el-tabs v-model="activeName">
                    <el-tab-pane label="Summary" name="first">
                        <TableItem :selectValue="selectValue"></TableItem>
                    </el-tab-pane>
                    <el-tab-pane label="Details" name="second">
                        <TableItem2 :selectValue="selectValue"></TableItem2>
                    </el-tab-pane>
                </el-tabs>
            </div>
        </div>
    </div>
</template>

<script>
import MarkerTree from '../marker/common/markerTree.vue'
import WordCloud from './WordCloud.vue'
import TableItem from './TableItem.vue'
import TableItem2 from './TableItem2.vue'
import { marker_node_desc, marker_word_data } from '@/api/api'

export default {
    props: {
        selectValue: {
            type: Object,
            default: () => {},
            required: true
        }
    },
    data() {
        return {
            titleData: [
                {
                    name: '#Classic Markers',
                    value: '',
                    color: '#A6CEE3'
                },
                {
                    name: '#Marker genes',
                    value: '',
                    color: '#B2DF8A'
                },
                {
                    name: '#Sub',
                    value: '',
                    color: '#FB9B9A'
                }
            ],
            activeName: 'first',
            info: {},
            workData: []
        }
    },
    methods: {
        // 头部信息
        getInfo(val) {
            marker_node_desc({
                ...val
            })
                .then((res) => {
                    if (res.code == 200) {
                        this.info = res.data
                    } else {
                        this.info = {}
                    }
                })
                .catch((err) => {
                    this.info = {}
                })
        },
        getWord(val) {
            marker_word_data({
                ...val
            })
                .then((res) => {
                    if (res.code == 200) {
                        this.workData = res.data
                    } else {
                        this.info = []
                    }
                })
                .catch((err) => {
                    this.info = []
                })
        }
    },
    components: {
        MarkerTree,
        WordCloud,
        TableItem,
        TableItem2
    },
    watch: {
        selectValue: {
            handler(newVal, oldVal) {
                let infoData = {
                    species_name: newVal.root
                }
                if (newVal.level > 1) {
                    infoData.tissue_name = newVal.parent
                }
                if (newVal.level > 2) {
                    infoData.cell_name = newVal.name
                }
                this.getInfo(infoData)
                this.getWord(infoData)
            },
            deep: true,
            immediate: true
        }
    }
}
</script>

<style scoped lang="scss">
.markerDefault {
    width: 100%;
    // height: 1231px;
    padding-top: 20px;
    background: #fff;
    box-sizing: border-box;
    .markerDefault-header {
        // width: 1240px;
        width: auto;
        margin: 0 auto;
        height: 40px;
        margin-bottom: 12px;
        overflow: auto;
    }
    .markerDefault-body {
        width: auto;
        margin: 0 auto;
        height: auto;
        padding-bottom: 47px;
        display: flex;
        .markerDefault-body-left {
            width: 308px;
            height: 915px;
            background: #ffffff;
            // border: 1px solid #dddddd;
            border-radius: 1px;
            overflow: auto;
            box-sizing: border-box;
            margin-right: 10px;
            // background: yellowgreen;
            .markerDefault-body-left-main {
                width: 500px;
                height: auto;
            }
        }
        .markerDefault-body-right {
            // width: calc(100% - 318px);
            width: 100%;
            // border: 1px solid #dddddd;
            // height: 1231px;
            padding: 27px 24px;
            box-sizing: border-box;
            background: #ffff;
            .markerDefault-body-right-name {
                width: 100%;
                line-height: 40px;
                height: 40px;
                font-family: PingFangSC-Semibold;
                font-size: 28px;
                color: #212121;
                letter-spacing: 0;
                font-weight: 600;
                margin-bottom: 20px;
            }
            .markerDefault-body-right-number {
                height: 78px;
                width: 100%;
                margin-bottom: 23px;
                .markerDefault-body-right-number-item {
                    display: inline-block;
                    width: auto;
                    height: 100%;
                    padding: 0 14px;
                    .markerDefault-body-right-number-item-name {
                        width: auto;
                        height: 22px;
                        line-height: 22px;
                        font-size: 16px;
                        color: #212121;
                        letter-spacing: 0;
                        font-weight: 400;
                        margin-bottom: 16px;
                    }
                    .markerDefault-body-right-number-item-value {
                        width: auto;
                        height: 60px;
                        text-align: center;
                        span {
                            display: inline-block;
                            width: 60px;
                            height: 60px;
                            border: 2px solid #212121;
                            border-radius: 50%;
                            text-align: center;
                            line-height: 60px;
                            font-size: 16px;
                            color: #212121;
                            letter-spacing: 0;
                            font-weight: 400;
                            box-sizing: border-box;
                        }
                    }
                }
            }
            .markerDefault-body-right-title {
                width: 100%;
                height: 28px;
                font-size: 20px;
                color: #333333;
                letter-spacing: 0;
                font-weight: bold;
                line-height: 28px;
            }
            .markerDefault-body-right-content {
                width: 100%;
                height: auto;
                padding-right: 60px;
                box-sizing: border-box;
                font-size: 12px;
                color: #333333;
                line-height: 20px;
                word-wrap: break-word;
            }
            .markerDefault-body-right-WordCloud {
                height: 337px;
                width: 100%;
                margin-bottom: 26px;
            }
        }
    }
}
</style>

<style>
.markerDefault-body-right .el-tabs__item {
    font-size: 16px;
}
.markerDefault-body-right .el-tabs__item.is-active {
    color: #24a461 !important;
}
.markerDefault-body-right .el-tabs__active-bar {
    background-color: #24a461 !important;
}
</style>
