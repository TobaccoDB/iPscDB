<template>
    <div class="ThreeItem" :style="{ marginLeft: zIndex > 0 ? '-10px' : '' }">
        <!-- :class="uuid == treeActive.uuid ? 'ThreeItem-title-main-active' : ''" -->
        <div class="ThreeItem-title-main" :class="treeActive && infoData.uuid == treeActive.uuid ? 'ThreeItem-title-main-active' : ''">
            <div class="ThreeItem-title" :style="{ paddingLeft: zIndex == 0 ? '10px' : '' }">
                <div class="ThreeItem-content-main-item-line" v-show="zIndex > 0" @click="selectVal(infoData)">
                    <div class="ThreeItem-content-main-item-line-footer" v-show="footerLine" :style="{ height: isShow ? parentLength * 34 + 17 + 'px' : 17 + 'px' }"></div>
                </div>
                <div class="ThreeItem-content-main-item-name">
                    <span
                        class="ThreeItem-titleIcon"
                        v-if="infoData.children && infoData.children.length > 0"
                        :class="!isShow ? 'el-icon-circle-plus-outline' : 'el-icon-remove-outline'"
                        v-show="infoData.children"
                        @click="tagExpand"
                    ></span>
                    <span @click="selectVal(infoData)" class="ThreeItem-content-main-item-name-name">
                        <!-- <img src="https://biobigdata.nju.edu.cn/scplantdb/img/plant_color.ab5174ae.png" /> -->
                        <img
                            class="ThreeItem-content-main-item-name-name-image"
                            :src="infoData.icon_url ? infoData.icon_url : 'https://biobigdata.nju.edu.cn/scplantdb/img/plant_color.ab5174ae.png'"
                        />
                        <!-- <span class="ThreeItem-content-main-item-name-name-image"></span> -->
                        <span class="ThreeItem-title-name">{{ infoData.name }}</span>
                        <span class="ThreeItem-title-tag" style="background: #409eff" v-if="infoData.classic_number">{{ infoData.classic_number }}</span>
                        <span class="ThreeItem-title-tag" style="background: #67c23a" v-if="infoData.gene_number">{{ infoData.gene_number }}</span>
                    </span>
                </div>
            </div>
        </div>
        <el-collapse-transition v-if="infoData.children">
            <div class="ThreeItem-content" v-show="isShow">
                <div class="ThreeItem-content-main" :class="footerLine && parentLength ? 'borderActive' : 'borderActive'">
                    <ThreeItem
                        :infoData="item"
                        v-for="(item, index) in infoData.children"
                        :key="index"
                        :zIndex="zIndex + 1"
                        :footerLine="infoData.children.length - 1 == index"
                        :parentLength="item.children ? item.children.length : 0"
                        @selectValParent="selectValParent"
                        :treeActive="treeActive"
                        :root="zIndex == 0 ? infoData.name : root"
                        :parent="zIndex == 1 ? infoData.name : parent"
                    ></ThreeItem>
                </div>
            </div>
        </el-collapse-transition>
    </div>
</template>

<script>
import 'element-ui/lib/theme-chalk/base.css'
import CollapseTransition from 'element-ui/lib/transitions/collapse-transition'
export default {
    name: 'ThreeItem',
    props: {
        parent: {
            type: String,
            default: null
        },
        root: {
            type: String,
            default: null
        },
        footerLine: {
            required: false,
            type: Boolean,
            default: false
        },
        infoData: {
            required: true,
            type: Object
        },
        zIndex: {
            required: true,
            type: Number,
            default: 0
        },
        parentLength: {
            required: false,
            type: Number,
            default: 0
        },
        treeActive: {
            required: false,
            type: Object,
            default: null
        }
    },
    data() {
        return {
            isShow: true
            // uuid: Math.random().toString(36).substr(3, 8)
        }
    },
    created() {},
    methods: {
        tagExpand() {
            this.isShow = !this.isShow
        },
        selectVal(item) {
            this.$emit('selectValParent', {
                ...item,
                // uuid: this.uuid,
                children: null,
                parent: this.parent,
                root: this.root
            })
        },
        selectValParent(item) {
            this.$emit('selectValParent', item)
        }
    },
    components: {
        CollapseTransition
    }
}
</script>

<style lang="scss">
// .ThreeItem {
//     margin-left: -10px;
// }
.ThreeItem-title-main {
    width: 400px;
    &:hover {
        background: #f5f7fa;
    }
}
.ThreeItem-title-main-active {
    background: #f0f7ff !important;
}
.ThreeItem-title {
    width: auto;
    min-width: 100%;
    height: 34px;
    line-height: 34px;
    display: flex;
    flex-wrap: nowrap;
    align-items: center;
    // padding-right: 100px;
    white-space: nowrap;
    cursor: pointer;
    .ThreeItem-content-main-item-name {
        display: inline-block;
        user-select: none;
        white-space: nowrap;
        display: block;
        .ThreeItem-content-main-item-name-name {
            display: inline-block;
            width: auto;
            height: 100%;
            padding-top: 7px;
            box-sizing: border-box;
            position: relative;
            padding-left: 25px;

            .ThreeItem-content-main-item-name-name-image {
                position: absolute;
                left: 0;
                top: 13px;
            }
        }
    }
    .ThreeItem-content-main-item-line {
        display: inline-block;
        width: 10px;
        height: 0px;
        border-top: 1px dashed #666666;
        position: relative;
        margin-right: 2px;
        .ThreeItem-content-main-item-line-footer {
            display: inline-block;
            width: 1px;
            height: 12px;
            background: #fff;
            // background: #666666;
            position: absolute;
            top: 0px;
            left: -1px;
            transition: all 0.4s;
        }
    }
    .ThreeItem-titleIcon {
        flex-shrink: 0;
        width: 14px;
        height: 14px;
        font-size: 14px;
        margin-right: 6px;
    }
    img {
        width: 20px;
        margin-right: 6px;
        flex-shrink: 0;
    }
    .ThreeItem-title-name {
        font-size: 12px;
        color: #333;
        margin-right: 6px;
        flex-shrink: 0;
    }
    .ThreeItem-title-tag {
        flex-shrink: 0;
        color: #fff;
        font-size: 12px;
        padding: 0 6px;
        display: inline-block;
        height: 18px;
        line-height: 18px;
        transform: scale(0.83);
        border-radius: 3px;
    }
}
.ThreeItem-content {
    width: 100%;
    min-width: 100%;
    height: auto;
    padding-left: 15px;
    box-sizing: border-box;
    font-size: 12px;
    .borderActive {
        border-left: 1px dashed #666666;
    }
    .ThreeItem-content-main {
        width: auto;
        min-width: 100%;

        padding-left: 10px;
        box-sizing: border-box;
        .ThreeItem-content-main-item {
            height: auto;
            width: auto;
            min-width: 100%;
            display: flex;

            .ThreeItem-content-main-item-line {
                display: inline-block;
                width: 12px;
                height: 0px;
                border-top: 1px dashed #666666;
            }
            .ThreeItem-content-main-item-children {
                width: auto;
                min-width: 100%;
            }
        }
    }
}
</style>
