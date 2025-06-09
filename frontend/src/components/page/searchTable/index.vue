<template>
    <div class="searchTable">
        <div class="searchTable-title">
            <!-- for {{ searchTitle }} -->
            <h2>Search Results : {{ $route.query.inputValue }}</h2>
        </div>
        <div class="searchTable-content">
            <el-table :data="tableData" style="width: 100%" v-loading="loading">
                <el-table-column :prop="item.prop" :label="item.label" align="center" v-for="(item, index) in searchColumn" :key="index">
                    <template slot-scope="scope">
                        <span v-if="item.color" v-html="highlightLetters(scope.row[item.prop], item.color)"></span>
                        <span v-else-if="item.prop == 'examine'" class="searchTable-content-details" @click="goMarker(scope.row)"> Details </span>
                        <span v-else>{{ scope.row[item.prop] }}</span>
                    </template>
                </el-table-column>
            </el-table>
            <div class="searchTable-content-footer">
                <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="queryInfo.page"
                    :page-sizes="[10, 20, 30, 50]"
                    :page-size="queryInfo.page_size"
                    layout="total, sizes, prev, pager, next"
                    :total="total"
                    background
                >
                </el-pagination>
            </div>
        </div>
    </div>
</template>

<script>
import { menu_search_list } from '@/api/api'

export default {
    data() {
        return {
            searchTitle: '',
            searchColumn: [],
            tableColumnSpecies: [
                { prop: 'species', label: 'Species', color: '#24A461' },
                { prop: 'examine', label: 'Examine' }
            ],
            titleSpecies: 'Species',
            tableColumnTissue: [
                { prop: 'tissue', label: 'Tissue', color: '#24A461' },
                { prop: 'species', label: 'Species' },
                { prop: 'examine', label: 'Examine' }
            ],
            titleTissue: 'Tissue',
            tableColumnCellType: [
                { prop: 'clusterName', label: 'Cell Type', color: '#24A461' },
                { prop: 'species', label: 'Species' },
                { prop: 'examine', label: 'Examine' }
            ],
            titleCellType: 'Cell Type',
            tableColumnMarker: [
                { prop: 'gene', label: 'Marker', color: '#24A461' },
                { prop: 'species', label: 'Species Name' },
                { prop: 'description', label: 'Description' },
                { prop: 'examine', label: 'Examine' }
            ],
            titleCellMarker: 'Marker',
            tableData: [],
            queryInfo: {
                page_size: 10,
                page: 1
            },
            total: 0,
            loading: false
        }
    },
    created() {},
    methods: {
        removeSpacesAndDuplicates(str) {
            return str
                .replace(/\s+/g, '')
                .split('')
                .filter((item, index, self) => {
                    return self.indexOf(item) === index
                })
                .join('')
        },
        highlightLetters(str, color) {
            let inputValue = this.$route.query.inputValue
            let replacedStr = ''
            if (inputValue) {
                let inputValueTiem = this.removeSpacesAndDuplicates(this.$route.query.inputValue.toLowerCase())

                let regex = new RegExp(`([${inputValueTiem}${inputValueTiem.toLocaleUpperCase()}])`, 'g')
                replacedStr = str.replace(regex, `<span style="color: ${color};">$1</span>`)
            }
            return replacedStr
        },
        goMarker(val) {
            if (this.$route.query.searchValue < 4) {
                this.$router.push({
                    path: '/marker',
                    query: {
                        species: val.species,
                        searchValue: this.$route.query.searchValue,
                        tissue: val.tissue,
                        cell: val.clusterName,
                        detail: val.gene
                    }
                })
            } else {
                this.$router.push({
                    path: '/markerCell',
                    query: {
                        species_name: val.species,
                        gene_id: val.gene
                    }
                })
            }
        },
        getColorString(val) {},
        infoPage() {
            this.queryInfo.page = 1
            this.queryInfo.page_size = 10
            let searchValue = this.$route.query.searchValue
            // let inputValue = this.$route.query.inputValue
            if (searchValue == '1') {
                this.searchTitle = this.titleSpecies
                this.searchColumn = this.tableColumnSpecies
            } else if (searchValue == '2') {
                this.searchTitle = this.titleTissue
                this.searchColumn = this.tableColumnTissue
            } else if (searchValue == '3') {
                this.searchTitle = this.titleCellType
                this.searchColumn = this.tableColumnCellType
            } else if (searchValue == '4') {
                this.searchTitle = this.titleCellMarker
                this.searchColumn = this.tableColumnMarker
            }
            this.tableData = []
            this.getDataList()
        },
        getDataList() {
            this.loading = true
            menu_search_list({
                ...this.queryInfo,
                opt_num: this.$route.query.searchValue,
                key_word: this.$route.query.inputValue
            })
                .then((res) => {
                    if (res.code == 200) {
                        this.total = res.data.count
                        this.tableData = res.data.results
                    }
                })
                .finally(() => {
                    this.loading = false
                })
        },
        handleSizeChange(val) {
            this.queryInfo.page = 1
            this.queryInfo.page_size = val
            this.getDataList()
        },
        handleCurrentChange(val) {
            this.queryInfo.page = val
            this.getDataList()
        }
    },
    computed: {
        searchValue() {
            return this.$route.query.searchValue
        },
        inputValue() {
            return this.$route.query.inputValue
        }
    },
    watch: {
        searchValue: {
            handler(news) {
                this.infoPage()
            },
            immediate: true
        },
        inputValue: {
            handler(news) {
                this.infoPage()
            },
            immediate: true
        }
    }
}
</script>

<style scoped lang="scss">
.searchTable {
    width: 100%;
    height: auto;
    min-height: 800px;
    background: #fff;
    .searchTable-title {
        width: 100%;
        height: 60px;
        line-height: 60px;
        text-align: center;
    }
    .searchTable-content {
        width: 1240px;
        margin: 0 auto;
        .searchTable-content-details {
            cursor: pointer;
            color: rgb(10, 157, 170);
            text-decoration: underline;
        }
        .searchTable-content-footer {
            width: 100%;
            height: 60px;
            display: flex;
            justify-content: flex-end;
            align-items: center;
        }
    }
}
</style>

<style lang="scss">
.searchTable {
    .el-pagination.is-background .el-pager li:not(.disabled).active {
        background-color: #24a461 !important;
    }
    .el-radio__input.is-checked + .el-radio__label {
        color: #24a461 !important;
    }
    .el-radio__input.is-checked .el-radio__inner {
        background: #24a461 !important;
        color: #24a461 !important;
        border-color: #24a461 !important;
    }
    .el-button--primary {
        background: #24a461 !important;
        border-color: #24a461 !important;
        font-size: 16px;
    }
}
</style>
