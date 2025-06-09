<template>
    <div class="markerTree">
        <div class="MarkerTree-search">
            <el-input v-model="searchVal" placeholder="Search.." suffix-icon="el-icon-search"></el-input>
        </div>
        <div class="MarkerTree-tag">
            <span>Classic Markers</span>
            <span>Marker genes</span>
        </div>
        <!--  v-loading="loading" -->
        <div class="MarkerTree-content">
            <div class="MarkerTree-content-main">
                <ThreeItem :infoData="treeList" :zIndex="0" :treeActive="treeActive" @selectValParent="selectVal"></ThreeItem>
            </div>
        </div>
    </div>
</template>

<script>
import ThreeItem from './ThreeItem.vue'
import { TreeData } from './markerTree'
import { marker_tree_data_list } from '@/api/api'
export default {
    props: {
        selectValue: {
            type: String,
            default: null
        },
        treeActive: {
            required: false,
            type: Object,
            default: {}
        }
    },
    data() {
        return {
            searchVal: '',
            TreeData,
            treeList: {},
            loading: false,
            // treeActive: null,
            searctValue: {}
        }
    },
    methods: {
        getVal(data, name) {
            let item = {}
            for (let i = 0; i < data.length; i++) {
                if (data[i].name == name) {
                    this.searctValue = data[i]
                    break
                }
                if (data[i].children) {
                    this.getVal(data[i].children, name)
                }
            }
            return item
        },
        getValInfo(data) {
            for (let i = 0; i < data.length; i++) {
                data[i].uuid = Math.random().toString(36).substr(3, 8)
                if (data[i].children) {
                    data[i].children = this.getValInfo(data[i].children)
                }
            }

            return data
        },
        getSelectInfo(data) {
            let name = this.$route.query.tissue || this.$route.query.cell
            let searchValue = this.$route.query.searchValue

            if (name && (searchValue == 2 || searchValue == 3)) {
                this.getVal([data], name)
                if (this.searctValue.name) {
                    this.searctValue.children = null
                    this.selectVal(this.searctValue)
                }
            }
        },
        getDataInfo(val) {
            this.$emit('loadingLeft', true)
            marker_tree_data_list({
                species_name: val
            })
                .then((res) => {
                    if (res.code === 200) {
                        this.treeList = res.data.name ? this.getValInfo([res.data])[0] : {}
                        if (this.$route.query.species == this.selectValue) {
                            this.getSelectInfo(this.treeList)
                        }
                    }
                    this.$emit('loadingLeft', false)
                })
                .catch((err) => {
                    this.$emit('loadingLeft', false)
                })
        },
        selectVal(val) {
            if (val.level == 2) {
                val.parent = val.name
            }
            // this.treeActive = val
            this.$emit('selectTreeValue', val)
        }
    },
    components: {
        ThreeItem
    },
    watch: {
        selectValue: {
            handler(newVal, oldVal) {
                if (newVal) {
                    this.getDataInfo(newVal)
                }
            },
            immediate: true
        }
    }
}
</script>

<style scoped lang="scss">
.markerTree {
    width: auto;
    height: 100%;
    padding: 12px;
    .MarkerTree-search {
        width: 288px;
        margin-bottom: 10px;
    }
    .MarkerTree-tag {
        width: 288px;
        height: 20px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        span {
            width: 138px;
            height: 20px;
            display: inline-block;
            text-align: center;
            border-radius: 5px;
            line-height: 20px;
            font-size: 12px;
        }
        span:nth-child(1) {
            background: #edf5ff;
            border: 1px solid #daecff;
            color: #409eff;
        }
        span:nth-child(2) {
            background: #f0faeb;
            border: 1px solid #e1f3d8;
            color: #67c23a;
        }
    }
    .MarkerTree-content {
        width: 100%;
        height: calc(100% - 86px);
        .MarkerTree-content-main {
            min-width: 100%;
            height: 100%;
            // overflow: auto;
        }
    }
}
</style>
