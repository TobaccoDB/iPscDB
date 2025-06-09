<template>
    <div class="marker">
        <div class="marker-header">
            <el-select v-model="headerValue" placeholder="Please select" style="width: 244px; height: 40px" @change="headerChange">
                <el-option v-for="item in options" :key="item" :label="item" :value="item"> </el-option>
            </el-select>
        </div>
        <div class="marker-body">
            <div class="marker-body-left" v-loading="leftLoading">
                <div class="marker-body-left-main">
                    <MarkerTree :selectValue="headerValue" :treeActive="treeActive" @loadingLeft="loadingLeft" @selectTreeValue="selectTreeValue"></MarkerTree>
                </div>
            </div>
            <div class="marker-body-right">
                <!-- <Histogram :selectValue="headerValue"></Histogram> -->
                <MarkerDefault v-if="treeActive.level && treeActive.level > 1" :selectValue="treeActive"></MarkerDefault>
                <Histogram v-else :selectValue="headerValue"></Histogram>
            </div>
        </div>
    </div>
</template>

<script>
import MarkerTree from './common/markerTree.vue'
import Histogram from './common/histogram.vue'
import MarkerDefault from '../markerDefault/index.vue'
import { marker_list } from '@/api/api'
export default {
    data() {
        return {
            headerValue: null,
            options: [],
            leftLoading: false,
            treeActive: {}
        }
    },
    components: {
        MarkerTree,
        Histogram,
        MarkerDefault
    },
    mounted() {
        this.getTreeData()
    },
    methods: {
        headerChange() {
            this.treeActive = {}
        },
        getTreeData() {
            marker_list().then((res) => {
                if (res.code === 200) {
                    this.options = res.data
                    this.headerValue = this.$route.query.species ? this.$route.query.species : res.data && res.data.length > 0 ? res.data[0] : null
                }
            })
        },
        loadingLeft(val) {
            this.leftLoading = val
        },
        selectTreeValue(item) {
            this.treeActive = item
        }
    },
    computed: {
        species() {
            return this.$route.query.species
        }
    }
}
</script>

<style scoped lang="scss">
.marker {
    width: 100%;
    height: auto;
    padding-top: 20px;
    background: #fff;
    .marker-header {
        width: 1240px;
        margin: 0 auto;
        height: 40px;
        margin-bottom: 12px;
        overflow: auto;
    }
    .marker-body {
        width: 1240px;
        margin: 0 auto;
        height: auto;
        padding-bottom: 47px;
        display: flex;
        .marker-body-left {
            width: 308px;
            height: 915px;
            background: #ffffff;
            border: 1px solid #dddddd;
            border-radius: 1px;
            overflow: auto;
            box-sizing: border-box;
            margin-right: 10px;
            // background: yellowgreen;
            .marker-body-left-main {
                width: auto;
                height: auto;
            }
        }
        .marker-body-right {
            width: calc(100% - 318px);
            border: 1px solid #dddddd;
            // height: 915px;
            background: #ffff;
        }
    }
}
</style>
