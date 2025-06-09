<template>
    <div>
        <!-- 
            :header-cell-style="headerStyle" -->
        <el-table
            ref="jgTable"
            size="small"
            :data="tableData"
            :height="tableHeight"
            :max-height="tableHeight"
            v-loading="loading"
            element-loading-text="running"
            :cell-style="cellstyle"
            @selection-change="handleSelectionChange"
            @expand-change="handleExpandChange"
            @sort-change="sortChange"
            @row-click="rowClick"
            @cell-click="handlecell"
            :span-method="tableSpanMethod"
            :border="ifhavborder"
        >
            <!-- 是否多选 -->
            <el-table-column type="selection" width="55" fixed v-if="ifHaveCheckBox" align="center"> </el-table-column>
            <!-- 是否单选 -->
            <el-table-column lable="" width="40" v-if="ifHaveRadio">
                <template slot-scope="scope">
                    <el-radio @change.native="getRadio(scope.row)" :label="scope.$index" v-model="radio">&nbsp;</el-radio>
                </template>
            </el-table-column>
            <!-- 是否显示序列 -->
            <el-table-column type="index" fixed width="55" label="序号" v-if="ifHaveIndex" align="center"> </el-table-column>
            <!-- 是否展开 -->
            <el-table-column width="55" type="expand" v-if="ifIsExpand" align="center">
                <template slot-scope="props">
                    <!-- 展开内容 -->
                    <slot></slot>
                </template>
            </el-table-column>
            <!-- table数据 -->
            <el-table-column
                v-for="(item, index) in column"
                :key="index"
                :label="item.label"
                :width="item.width"
                show-overflow-tooltip
                :align="item.align === undefined ? 'center' : item.align"
                :fixed="item.fixed === undefined ? false : item.fixed"
                :sortable="item.sortable === undefined ? false : item.sortable"
                :prop="item.key"
            >
                <template slot-scope="scope">
                    <span v-if="scope.row[item.key] === undefined || scope.row[item.key] === null || scope.row[item.key] === '' || scope.row[item.key].toString().trim() == ''"></span>
                    <el-popover
                        placement="top"
                        trigger="hover"
                        v-else-if="scope.row[item.key].toString().trim().length > showLen && showLen > 0 && showLen != 0"
                        :content="scope.row[item.key].toString()"
                    >
                        <span slot="reference">{{ `${scope.row[item.key].toString().trim().slice(0, showLen)}...` }}</span>
                    </el-popover>
                    <span v-else>{{ scope.row[item.key] }}</span>
                </template>
            </el-table-column>
            <!-- 操作 -->
            <el-table-column :label="operationText" align="center" width="140" fixed="right" v-if="isHaveView || isHaveEdit || isHaveDelete || isHaveDownload">
                <template slot-scope="scope">
                    <i class="el-icon-view pointer" style="padding: 0 5px; color: #24a461" v-if="isHaveView" @click="viewHandle(scope)"></i>
                    <i class="el-icon-edit pointer" style="padding: 0 5px; color: #24a461" v-if="isHaveEdit" @click="editHandle(scope)"></i>
                    <i class="el-icon-delete pointer" style="padding: 0 5px; color: #24a461" v-if="isHaveDelete" @click="deleteHandle(scope)"></i>
                    <i class="el-icon-download pointer" style="padding: 0 5px; color: #24a461" v-if="isHaveDownload" @click="downloadHandle(scope, 'csv')">csv</i>
                    <i class="el-icon-download pointer" style="padding: 0 5px; color: #24a461" v-if="isHaveDownload" @click="downloadHandle(scope, 'txt')">txt</i>
                    <!-- <span class="pointer" style="padding:0 5px;color:#24A461;" v-if='isHaveDownload' @click='downloadHandle(scope)'>Excel</span> -->
                </template>
            </el-table-column>
        </el-table>
        <el-pagination
            style="text-align: right; padding: 10px 5px"
            background
            v-if="hasPagination"
            :current-page="paginationConfig.page"
            :page-sizes="paginationConfig.sizes"
            :page-size="paginationConfig.size"
            :pager-count="pagerCount"
            :total="paginationConfig.total"
            @current-change="handleCurrentChange"
            @size-change="handleSizeChange"
            :layout="layout"
        >
        </el-pagination>
    </div>
</template>

<script>
/**
 * 必填
 * @param {tableData} 表格数据
 * @param {column} 表格头数据{key:'',label:''} key代表唯一ID值,label代表名称
 */

/**
 * 选填
 * @param {showLen} 表格内容显示多长(超过改长度的显示...)
 * @param {isHaveView} 是否有查看
 * @function viewHandle(scope) 查看事件,scope为修改行数据
 * @param {isHaveEdit} 是否有修改
 * @function editHandle(scope) 修改事件,scope为修改行数据
 * @param {isHaveDelete} 是否有删除
 * @function deleteHandle(scope) 删除事件,scope为删除行数据
 * @param {ifHaveCheckBox} 是否显示多选
 * @function handleSelectionChange(val) 多选事件 val为选中项数据
 * @param {ifIsExpand} 是否可以展开
 * @function handleExpandChange(val) 展开事件 val为展开项数据
 * @function sortChange(val) 排序事件
 * @function rowClick(row,event,column) 点击行
 * @param {ifHaveIndex} 是否显示序列号
 */
export default {
    name: 'jgTable',
    props: {
        tableData: {
            type: Array,
            default() {
                return []
            }
        },
        column: {
            type: Array,
            default() {
                return []
            }
        },
        isHaveView: {
            type: Boolean,
            default() {
                return false
            }
        },
        isHaveEdit: {
            type: Boolean,
            default() {
                return false
            }
        },
        isHaveDelete: {
            type: Boolean,
            default() {
                return false
            }
        },
        isHaveDownload: {
            type: Boolean,
            default() {
                return false
            }
        },
        showLen: {
            type: Number,
            default() {
                return 0
            }
        },
        ifHaveCheckBox: {
            type: Boolean,
            default() {
                return false
            }
        },
        ifIsExpand: {
            type: Boolean,
            default() {
                return false
            }
        },
        ifHaveIndex: {
            type: Boolean,
            default() {
                return false
            }
        },
        ifHaveRadio: {
            type: Boolean,
            default: () => false
        },
        ifhavborder: {
            type: Boolean,
            default: () => true
        },
        tableSpanArr: {
            type: Array,
            default: () => []
        },
        spanColumnArr: {
            type: Array,
            default: () => []
        },
        tableHeight: {
            // type: Number,
            // default() {
            //   return 440
            // }
        },
        paginationConfig: {
            type: Object,
            default() {
                return {}
            }
        },
        pagerCount: {
            type: Number,
            default() {
                return 7
            }
        },
        hasPagination: {
            type: Boolean,
            default() {
                return true
            }
        },
        layout: {
            type: String,
            default() {
                return 'total, sizes, prev, pager, next'
            }
        },
        loading: {
            type: Boolean,
            default() {
                return false
            }
        },
        operationText: {
            type: String,
            default() {
                return '操作'
            }
        },
        cellstyle: {
            default() {
                return {
                    fontSize: '14px'
                }
            }
        },
        headerStyle: {
            default() {
                return {
                    color: '#fff',
                    fontSize: '14px',
                    background: '#24A461',
                    fontFamily: 'Source Han Sans CN'
                }
            }
        }
    },
    data() {
        return {
            radio: ''
        }
    },
    watch: {
        tableData() {
            this.radio = ''
        }
    },
    methods: {
        viewHandle(scope) {
            this.$emit('viewHandle', scope)
        },
        editHandle(scope) {
            this.$emit('editHandle', scope)
        },
        deleteHandle(scope) {
            this.$emit('deleteHandle', scope)
        },
        downloadHandle(scope, type) {
            this.$emit('downloadHandle', scope, type)
        },
        handleSelectionChange(val) {
            this.$emit('handleSelectionChange', val)
        },
        handleExpandChange(val) {
            this.$emit('handleExpandChange', val)
        },
        sortChange(val) {
            this.$emit('sortChange', val)
        },
        rowClick(row, event, column) {
            this.$emit('rowClick', row)
        },
        getRadio(row) {
            this.$emit('getRadio', row)
        },
        tableSpanMethod({ row, column, rowIndex, columnIndex }) {
            if (this.tableSpanArr.length) {
                if (this.spanColumnArr.indexOf(columnIndex) > -1) {
                    if (this.tableSpanArr[rowIndex]) {
                        return {
                            rowspan: this.tableSpanArr[rowIndex],
                            colspan: 1
                        }
                    } else {
                        return {
                            rowspan: 0,
                            colspan: 0
                        }
                    }
                }
            }
        },
        handleCurrentChange(val) {
            this.$emit('handleCurrentChange', val)
        },
        handleSizeChange(val) {
            this.$emit('handleSizeChange', val)
        },
        handlecell(row, col) {
            let param = { row, col }
            this.$emit('handlecell', param)
        }
    }
}
</script>

<style scoped>
@import './index.css';
</style>
