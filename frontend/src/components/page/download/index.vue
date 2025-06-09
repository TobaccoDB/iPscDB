<template>
    <div class="download">
        <div class="download-inner">
            <div class="blast">
                <div class="radioType">
                    <el-radio-group v-model="radioType" @change="typeChange">
                        <el-radio label="Atlas">Atlas</el-radio>
                        <el-radio label="CellMarker">Cell Marker</el-radio>
                        <el-radio label="ClusterMarker">Cluster Marker</el-radio>
                    </el-radio-group>
                </div>
                <el-form ref="form1" :inline="true" :model="download_form">
                    <el-form-item label="Species" prop="species_name">
                        <el-select clearable style="width: 200px" size="large" @change="species_nameChange" v-model="download_form.species_name_value" placeholder="Choose">
                            <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.name"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item :label="radioType == 'Atlas' ? 'Atlas name' : 'Tissue'" prop="tissue">
                        <el-select clearable style="width: 200px" size="large" v-model="download_form.tissue" placeholder="Choose">
                            <el-option v-for="(item, index) in tissueOptions" :key="index" :label="item.label" :value="item.name"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="">
                        <el-button type="primary" size="lager" @click="search" :loading="loading">GO</el-button>
                    </el-form-item>
                </el-form>
            </div>
            <el-table
                v-show="radioType == 'Atlas'"
                size="small"
                :data="tableData"
                :header-cell-style="headerStyle"
                v-loading="loading"
                element-loading-text="running"
                :cell-style="cellstyle"
                @cell-click="handlecell"
                border
                style="width: 100%"
            >
                <el-table-column
                    v-for="(item, index) in column"
                    :key="index"
                    :label="item.label"
                    :width="item.width"
                    :align="item.align === undefined ? 'center' : item.align"
                    :fixed="item.fixed === undefined ? false : item.fixed"
                    :sortable="item.sortable === undefined ? false : item.sortable"
                    :prop="item.key"
                >
                    <template slot-scope="scope">
                        <span v-if="item.label == 'Souce'"
                            >{{ scope.row[item.key].split(':')[0] }} <i class="downloadIcon" @click="AtlasDownload(scope.row, 'RDS')"></i><br />{{
                                scope.row[item.key].split(':')[1].replace(/_/g, ' ')
                            }}
                            <i class="downloadIcon" @click="AtlasDownload(scope.row, 'GE_Matrix')"></i>
                        </span>
                        <span v-else-if="item.label == 'Size'">{{ scope.row[item.key].split(':')[0] }}<br />{{ scope.row[item.key].split(':')[1] }} </span>
                        <span v-else-if="item.label == 'MD5'">{{ scope.row[item.key].split(':')[0] }}<br />{{ scope.row[item.key].split(':')[1] }} </span>
                        <span v-else>{{ scope.row[item.key] }}</span>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
                v-show="radioType == 'Atlas'"
                style="text-align: right; padding: 10px 5px"
                background
                :current-page="paginationConfig.page"
                :page-sizes="paginationConfig.sizes"
                :page-size="paginationConfig.size"
                :pager-count="7"
                :total="paginationConfig.total"
                @current-change="handleCurrentChange"
                @size-change="handleSizeChange"
                layout="total, sizes, prev, pager, next"
            >
            </el-pagination>
            <!-- Cell Marker表格 -->
            <el-table
                v-show="radioType == 'CellMarker'"
                size="small"
                :data="tableData2"
                :header-cell-style="headerStyle"
                v-loading="loading2"
                element-loading-text="running"
                :cell-style="cellstyle"
                @cell-click="handlecell"
                border
                style="width: 100%"
            >
                <el-table-column
                    v-for="(item, index) in column2"
                    :key="index"
                    :label="item.label"
                    :width="item.width"
                    :align="item.align === undefined ? 'center' : item.align"
                    :fixed="item.fixed === undefined ? false : item.fixed"
                    :sortable="item.sortable === undefined ? false : item.sortable"
                    :prop="item.key"
                >
                    <template slot-scope="scope">
                        <span v-if="item.label == 'Souce'"
                            >{{ scope.row[item.key] }}
                            <i class="downloadIcon" @click="CellMarkerDownload(scope.row)"></i>
                        </span>
                        <span v-else>{{ scope.row[item.key] }}</span>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
                v-show="radioType == 'CellMarker'"
                style="text-align: right; padding: 10px 5px"
                background
                :current-page="paginationConfig2.page"
                :page-sizes="paginationConfig2.sizes"
                :page-size="paginationConfig2.size"
                :pager-count="7"
                :total="paginationConfig2.total"
                @current-change="handleCurrentChange2"
                @size-change="handleSizeChange2"
                layout="total, sizes, prev, pager, next"
            >
            </el-pagination>
            <!-- Cluster Marker表格 -->
            <el-table
                v-show="radioType == 'ClusterMarker'"
                size="small"
                :data="tableData3"
                :header-cell-style="headerStyle"
                v-loading="loading3"
                element-loading-text="running"
                :cell-style="cellstyle"
                @cell-click="handlecell"
                border
                style="width: 100%"
            >
                <el-table-column
                    v-for="(item, index) in column3"
                    :key="index"
                    :label="item.label"
                    :width="item.width"
                    :align="item.align === undefined ? 'center' : item.align"
                    :fixed="item.fixed === undefined ? false : item.fixed"
                    :sortable="item.sortable === undefined ? false : item.sortable"
                    :prop="item.key"
                >
                    <template slot-scope="scope">
                        <span v-if="item.label == 'Souce'"
                            >{{ scope.row[item.key] }}
                            <i class="downloadIcon" @click="ClusterMarkerDownload(scope.row)"></i>
                        </span>
                        <span v-else>{{ scope.row[item.key] }}</span>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
                v-show="radioType == 'ClusterMarker'"
                style="text-align: right; padding: 10px 5px"
                background
                :current-page="paginationConfig3.page"
                :page-sizes="paginationConfig3.sizes"
                :page-size="paginationConfig3.size"
                :pager-count="7"
                :total="paginationConfig3.total"
                @current-change="handleCurrentChange3"
                @size-change="handleSizeChange3"
                layout="total, sizes, prev, pager, next"
            >
            </el-pagination>
            <div class="genomicLocation">
                <p class="keyword_p1">Data Backup</p>
                <div class="keyword_p2">
                    All of the data above has been uploaded to the Zenodo and can be downloaded by visiting website
                    <a href="https://doi.org/10.5281/zenodo.8041092" target="_blank">https://doi.org/10.5281/zenodo.8041092</a>, DOI:10.5281/zenodo.8041092
                    <!-- <a href="https://zenodo.org/record/4017591" target="_blank">https://zenodo.org/record/4017591</a>, DOI:10.5281/zenodo.4017591 -->
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {
    atlas_specis_download_down,
    atlas_name_download_down,
    atlas_download_list,
    cell_marker_download_list,
    cell_cluster_download_list,
    atlas_download,
    cell_marker_download,
    cell_cluster_download,
    cell_specie_download_down,
    cell_tissue_download_down
} from '@/api/api'
import jgTable from '@/components/jgTable/index'

export default {
    name: 'search',
    components: {
        jgTable
    },
    data() {
        return {
            download_form: {
                species_name_value: '',
                tissue: ''
            },
            speciesOptions: [],
            tissueOptions: [],
            tableData: [],
            column: [
                { key: 'species_name', label: 'Species', width: 200 },
                { key: 'version', label: 'Version', width: 80 },
                { key: 'atlas_type', label: 'Atlas type', width: 100 },
                { key: 'atlas_name', label: 'Atlas name', width: 120 },
                { key: 'source', label: 'Souce', width: 120 },
                { key: 'size', label: 'Size', width: 100 },
                { key: 'md5', label: 'MD5' },
                { key: 'last_update', label: 'LastUpdate', width: 120 }
            ],
            paginationConfig: {
                page: 1,
                size: 10,
                sizes: [10, 20, 30],
                total: 0
            },
            loading: false,
            headerStyle: {
                color: '#fff',
                fontSize: '14px',
                background: '#24A461',
                fontFamily: 'Source Han Sans CN'
            },
            radioType: 'Atlas',
            // Cell Marker
            loading2: false,
            tableData2: [],
            column2: [
                { key: 'species_name', label: 'Species', width: 200 },
                { key: 'tissue', label: 'Tissue', width: 180 },
                { key: 'source', label: 'Souce', width: 120 },
                { key: 'size', label: 'Size', width: 120 },
                { key: 'md5', label: 'MD5' },
                { key: 'last_update', label: 'LastUpdate', width: 120 }
            ],
            paginationConfig2: {
                page: 1,
                size: 10,
                sizes: [10, 20, 30],
                total: 0
            },
            // Cluster Marker
            loading3: false,
            tableData3: [],
            column3: [
                { key: 'species_name', label: 'Species', width: 200 },
                { key: 'tissue', label: 'Tissue', width: 180 },
                { key: 'source', label: 'Souce', width: 120 },
                { key: 'size', label: 'Size', width: 120 },
                { key: 'md5', label: 'MD5' },
                { key: 'last_update', label: 'LastUpdate', width: 120 }
            ],
            paginationConfig3: {
                page: 1,
                size: 10,
                sizes: [10, 20, 30],
                total: 0
            }
        }
    },
    mounted() {
        this.init()
        this.getTableData()
        this.getTableData2()
        this.getTableData3()
    },
    methods: {
        init() {
            atlas_specis_download_down({}).then((res) => {
                if (res.code == 200) {
                    this.speciesOptions = res.data
                }
            })
        },
        typeChange(val) {
            this.download_form = {
                species_name_value: '',
                tissue: ''
            }
            this.tissueOptions = []
            if (val == 'Atlas') {
                atlas_specis_download_down({}).then((res) => {
                    if (res.code == 200) {
                        this.speciesOptions = res.data
                        this.getTableData()
                    }
                })
            } else {
                cell_specie_download_down({}).then((res) => {
                    if (res.code == 200) {
                        this.speciesOptions = res.data
                    }
                })
                if (this.radioType == 'CellMarker') {
                    this.getTableData2()
                } else {
                    this.getTableData3()
                }
            }
        },
        species_nameChange() {
            if (this.radioType == 'Atlas') {
                atlas_name_download_down({ species_name_value: this.download_form.species_name_value }).then((res) => {
                    if (res.code == 200) {
                        this.download_form.tissue = ''
                        this.tissueOptions = res.data
                    }
                })
            } else {
                cell_tissue_download_down({ species_name_value: this.download_form.species_name_value }).then((res) => {
                    if (res.code == 200) {
                        this.download_form.tissue = ''
                        this.tissueOptions = res.data
                    }
                })
            }
        },
        search(param) {
            if (this.radioType == 'Atlas') {
                this.paginationConfig.page = 1
                this.getTableData()
            } else if (this.radioType == 'CellMarker') {
                this.paginationConfig2.page = 1
                this.getTableData2()
            } else if (this.radioType == 'ClusterMarker') {
                this.paginationConfig3.page = 1
                this.getTableData3()
            }
        },
        // 表格部分
        getTableData() {
            this.loading = true
            atlas_download_list({
                ...this.download_form,
                ...{
                    page: this.paginationConfig.page,
                    page_size: this.paginationConfig.size
                }
            }).then((res) => {
                if (res.code == 200) {
                    this.tableData = res.data.results
                    this.paginationConfig.total = res.data.count
                    this.loading = false
                }
            })
        },
        handleCurrentChange(val) {
            this.paginationConfig.page = val
            this.getTableData()
        },
        handleSizeChange(val) {
            this.paginationConfig.page = 1
            this.paginationConfig.size = val
            this.getTableData()
        },
        cellstyle({ row, column, rowIndex, columnIndex }) {
            // if (column.label === 'Lit ID') {
            //   return { color: "#0a9daa", cursor: "pointer" }
            // }
            return { fontSize: '14px' }
        },
        handlecell(row, col) {
            if (col.label == 'Lit ID') {
                // window.open(`https://pubmed.ncbi.nlm.nih.gov/${params.row.pmid}/`, '_blank')
            }
        },
        AtlasDownload(row, type) {
            atlas_download({
                species_name_value: row.species_name_value,
                atlas_type: row.atlas_type,
                atlas_name_value: row.atlas_name_value,
                download_type: type
            }).then((res) => {
                if (res.code == 200) {
                    window.open(res.data.atlas_download, '_blank')
                }
            })
        },
        // Cell Marker-----------------------------------------
        getTableData2() {
            cell_marker_download_list({
                ...this.download_form,
                ...{
                    page: this.paginationConfig2.page,
                    page_size: this.paginationConfig2.size
                }
            }).then((res) => {
                if (res.code == 200) {
                    this.tableData2 = res.data.results
                    this.paginationConfig2.total = res.data.count
                }
            })
        },
        handleCurrentChange2(val) {
            console.log(123, val)
            this.paginationConfig2.page = val
            this.getTableData2()
        },
        handleSizeChange2(val) {
            console.log(456, val)
            this.paginationConfig2.page = 1
            this.paginationConfig2.size = val
            this.getTableData2()
        },
        CellMarkerDownload(row) {
            cell_marker_download({
                species_name_value: row.species_name_value,
                tissue: row.tissue
            }).then((res) => {
                if (res.code == 200) {
                    window.open(res.data.atlas_download, '_blank')
                }
            })
        },
        // Cluster Marker-----------------------------------------
        getTableData3() {
            cell_cluster_download_list({
                ...this.download_form,
                ...{
                    page: this.paginationConfig3.page,
                    page_size: this.paginationConfig3.size
                }
            }).then((res) => {
                if (res.code == 200) {
                    res.data.results.forEach((item) => {
                        if (item.marker_resource == 'all') {
                            item.marker_resource = 'All'
                        }
                    })
                    this.tableData3 = res.data.results
                    this.paginationConfig3.total = res.data.count
                }
            })
        },
        handleCurrentChange3(val) {
            this.paginationConfig3.page = val
            this.getTableData3()
        },
        handleSizeChange3(val) {
            this.paginationConfig3.page = 1
            this.paginationConfig3.size = val
            this.getTableData3()
        },
        ClusterMarkerDownload(row) {
            cell_cluster_download({
                species_name_value: row.species_name_value,
                tissue: row.tissue
            }).then((res) => {
                if (res.code == 200) {
                    window.open(res.data.atlas_download, '_blank')
                }
            })
        }
    }
}
</script>
<style lang="scss" scoped>
@import './style.scss';
</style>
