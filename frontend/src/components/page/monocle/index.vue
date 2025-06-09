<template>
    <div class="monocle">
        <div class="monocle-inner">
            <div class="blast">
                <el-header>Developmental trajectory</el-header>
                <el-form ref="form1" :inline="true" :model="monocleForm">
                    <el-form-item label="Species" prop="species_name">
                        <el-select style="width: 200px" size="large" @change="species_nameChange" v-model="monocleForm.species_name" placeholder="Choose">
                            <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Tissue" prop="tissue">
                        <el-select clearable style="width: 200px" @change="tissueChange" size="large" v-model="monocleForm.tissue" placeholder="Choose">
                            <el-option v-for="(item, index) in monocleForm_option.tissueOptions" :key="index" :label="item.label" :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Cell type" prop="cell_type">
                        <el-select filterable clearable style="width: 200px" size="large" v-model="monocleForm.cell_type" placeholder="Choose">
                            <el-option v-for="item in monocleForm_option.cellTypeOptions" :key="item.label" :label="item.label" :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="">
                        <el-button class="btnSearch" @click="search" :loading="loading">GO</el-button>
                    </el-form-item>
                </el-form>
                <el-radio-group v-model="radioType" @change="radioChange">
                    <el-radio label="Pseudotime">Pseudotime</el-radio>
                    <el-radio label="State">State</el-radio>
                    <el-radio label="cell_type">Cell type</el-radio>
                    <el-radio label="seurat_clusters">Cluster</el-radio>
                </el-radio-group>
            </div>
            <!-- 图片 -->
            <div class="static_img" style="text-align: center" v-loading="loadingImg" element-loading-text="running">
                <img style="max-width: 100%; max-height: 95%; margin-top: 10px" :src="staticUrl" />
                <div style="width: 100%; height: 512px; overflow: hidden; line-height: 512px; font-size: 14px; color: #999; text-align: center"
                    v-if="!staticUrl">No data</div>
            </div>
            <!-- Differential expressed genes表格 -->
            <div class="firstTable" v-if="false">
                <div class="centerTable">
                    <p class="table1Title">Differential expressed genes</p>
                    <jg-table :tableData="tableData" :column="column" :loading="loading" :cellstyle="cellstyle" :paginationConfig="paginationConfig"
                        @handleCurrentChange="handleCurrentChange" @handleSizeChange="handleSizeChange" @handlecell="handlecell"></jg-table>
                    <div class="searchJump">
                        <span>Genes:</span>
                        <!-- <el-select v-model="searchJump" size="large" style="width:250px;" collapse-tags filterable multiple placeholder="Choose">
              <el-option v-for="item in genesOptions" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select> -->

                        <el-select v-model="searchJump" size="large" multiple filterable remote reserve-keyword placeholder="Please enter keywords"
                            :remote-method="remoteMethod" :loading="selectLoading">
                            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                        <el-button type="primary" size="lager" style="margin-left: 20px" @click="goDetail">GO</el-button>
                        <el-button type="primary" size="lager" style="margin-left: 20px" @click="goExampleDetail">Example</el-button>
                    </div>
                </div>
            </div>
            <div class="centerTable" v-if="false">
                <p class="table1Title">Differential genes</p>
                <jg-table :tableData="tableData2" :column="column2" :loading="loading2" :cellstyle="cellstyle" :paginationConfig="paginationConfig2"
                    @handleCurrentChange="handleCurrentChange2" @handleSizeChange="handleSizeChange2" @handlecell="handlecell2"></jg-table>
                <div class="searchJump">
                    <span>Genes:</span>
                    <!-- <el-select v-model="searchJump2" size="large" style="width:250px;" collapse-tags filterable multiple placeholder="Choose">
            <el-option v-for="item in genesOptions2" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select> -->
                    <el-select v-model="searchJump2" size="large" multiple filterable remote reserve-keyword placeholder="Please enter keywords"
                        :remote-method="remoteMethod2" :loading="selectLoading2">
                        <el-option v-for="item in options2" :key="item.value" :label="item.label" :value="item.value"> </el-option>
                    </el-select>
                    <el-button type="primary" size="lager" style="margin-left: 20px" @click="goDetail2">GO</el-button>
                    <el-button type="primary" size="lager" style="margin-left: 20px" @click="goExampleDetail2">Example</el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { species_down, species_tissue_down, species_cell_type_down, monocle_expressed_list, monocle_heatmap_list, monocle_expressed_down, monocle_heatmap_down, monocle_heat_png } from '@/api/api'
import jgTable from '@/components/jgTable/index'

export default {
    name: 'monocle',
    components: {
        jgTable
    },
    data() {
        return {
            loadingImg: false,
            monocleForm: {
                species_name: 'Arabidopsis_thaliana',
                tissue: 'Root',
                cell_type: 'Atrichoblast'
            },
            radioType: 'Pseudotime',
            staticUrl: '',
            speciesOptions: [],
            monocleForm_option: {
                tissueOptions: [],
                cellTypeOptions: []
            },
            options: [],
            options2: [],
            genesOptions: [],
            genesOptions2: [],
            tableData: [],
            column: [
                { key: 'gene_id', label: 'Gene ID' },
                { key: 'status', label: 'status' },
                { key: 'family', label: 'family' },
                { key: 'pval', label: 'pval' },
                { key: 'qval', label: 'qval' },
                { key: 'gene_short_name', label: 'gene short name' },
                { key: 'num_cells_expressed', label: 'num cells expressed' }
            ],
            paginationConfig: {
                page: 1,
                size: 10,
                sizes: [10, 20, 30],
                total: 0
            },
            loading: false,
            searchJump: '',
            // 第二部分
            tableData2: [],
            column2: [
                { key: 'gene_id', label: 'Gene ID' },
                { key: 'status', label: 'status' },
                { key: 'family', label: 'family' },
                { key: 'pval', label: 'pval' },
                { key: 'qval', label: 'qval' },
                { key: 'gene_short_name', label: 'gene short name' },
                { key: 'num_cells_expressed', label: 'num cells expressed', width: 170 },
                { key: 'use_for_ordering', label: 'use for ordering' }
            ],
            paginationConfig2: {
                page: 1,
                size: 10,
                sizes: [10, 20, 30],
                total: 0
            },
            loading2: false,
            searchJump2: '',
            selectLoading: false,
            selectLoading2: false
        }
    },
    mounted() {
        this.init()
        this.getGeneoption()
        this.getTableData()
        this.getTableData2()
        this.radioChange()
        species_tissue_down({ species_name: this.monocleForm.species_name }).then((res) => {
            if (res.code == 200) {
                this.monocleForm_option.tissueOptions = res.data
            }
        })
        species_cell_type_down({ species_name: this.monocleForm.species_name, tissue: this.monocleForm.tissue }).then((res) => {
            if (res.code == 200) {
                this.monocleForm_option.cellTypeOptions = res.data
            }
        })
    },
    methods: {
        init() {
            species_down({}).then((res) => {
                if (res.code == 200) {
                    this.speciesOptions = res.data
                }
            })
        },
        radioChange() {
            this.loadingImg = true
            monocle_heat_png({
                ...this.monocleForm,
                ...{
                    type: this.radioType
                }
            }).then((res) => {
                if (res.code == 200) {
                    this.staticUrl = res.data.monocle_heat_png
                    this.loadingImg = false
                }
            })
        },
        getGeneoption() {
            monocle_expressed_down({
                ...this.monocleForm,
                ...{
                    page: 1,
                    page_size: 10000
                }
            }).then((res) => {
                if (res.code == 200) {
                    this.genesOptions = []
                    res.data &&
                        res.data.forEach((item) => {
                            this.genesOptions.push({
                                label: Object.entries(item)[0][1],
                                value: Object.entries(item)[0][1]
                            })
                        })
                }
            })
            monocle_heatmap_down({
                ...this.monocleForm,
                ...{
                    page: 1,
                    page_size: 10000
                }
            }).then((res) => {
                if (res.code == 200) {
                    this.genesOptions2 = []
                    res.data &&
                        res.data.forEach((item) => {
                            this.genesOptions2.push({
                                label: Object.entries(item)[0][1],
                                value: Object.entries(item)[0][1]
                            })
                        })
                }
            })
        },
        remoteMethod(query) {
            if (query !== '') {
                this.selectLoading = true
                setTimeout(() => {
                    this.selectLoading = false
                    this.options = this.genesOptions
                        .filter((item) => {
                            return item.label.toLowerCase().indexOf(query.toLowerCase()) > -1
                        })
                        .slice(0, 20)
                }, 200)
            } else {
                this.options = []
            }
        },
        remoteMethod2(query) {
            if (query !== '') {
                this.selectLoading2 = true
                setTimeout(() => {
                    this.selectLoading2 = false
                    this.options2 = this.genesOptions2
                        .filter((item) => {
                            return item.label.toLowerCase().indexOf(query.toLowerCase()) > -1
                        })
                        .slice(0, 20)
                }, 200)
            } else {
                this.options2 = []
            }
        },
        species_nameChange() {
            species_tissue_down({ species_name: this.monocleForm.species_name }).then((res) => {
                if (res.code == 200) {
                    this.monocleForm.cell_type = ''
                    this.monocleForm.tissue = ''
                    this.monocleForm_option.cellTypeOptions = []
                    this.monocleForm_option.tissueOptions = res.data
                }
            })
        },
        tissueChange() {
            species_cell_type_down({ species_name: this.monocleForm.species_name, tissue: this.monocleForm.tissue }).then((res) => {
                if (res.code == 200) {
                    this.monocleForm.cell_type = ''
                    this.monocleForm_option.cellTypeOptions = res.data
                }
            })
        },
        search() {
            if (this.monocleForm.tissue == '') {
                this.$message('Please select Tissue!')
            } else if (this.monocleForm.cell_type == '') {
                this.$message('Please select Cell type!')
            } else {
                this.paginationConfig.page = 1
                this.paginationConfig2.page = 1
                this.getTableData()
                this.getTableData2()
                this.getGeneoption()
                this.radioChange()
            }
        },
        // 表格部分
        getTableData() {
            this.loading = true
            monocle_expressed_list({
                ...this.monocleForm,
                ...{
                    page: this.paginationConfig.page,
                    page_size: this.paginationConfig.size
                }
            }).then((res) => {
                if (res.code == 200) {
                    if (res.count) {
                        this.tableData = res.data
                        this.paginationConfig.total = res.count
                    } else {
                        this.tableData = []
                        this.paginationConfig.total = 0
                    }
                    this.loading = false
                }
            })
        },
        goDetail() {
            this.$router.push({
                path: '/monocleExpressed',
                query: {
                    ...this.monocleForm,
                    ...{
                        gene: this.searchJump.join(),
                        type: this.radioType
                    }
                }
            })
            // if (this.multipleSelection.length < 2 || this.multipleSelection.length > 5) {
            //   this.$message('Please select 2 to 5 pieces of data!')
            //   return
            // }
        },
        goExampleDetail() {
            let genes = ''
            if (this.monocleForm.species_name == 'Oryza_sativa') {
                genes = 'Os01g0169900'
            } else if (this.monocleForm.species_name == 'Zea_mays') {
                genes = 'Zm00001d027230'
            } else if (this.monocleForm.species_name == 'Arabidopsis_thaliana') {
                genes = 'AT1G01050'
            }
            this.$router.push({
                path: '/monocleExpressed',
                query: {
                    ...this.monocleForm,
                    ...{
                        gene: genes,
                        type: this.radioType
                    }
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
            if (column.label === 'Gene ID') {
                return { color: '#0a9daa', cursor: 'pointer' }
            }
            // 针对Safari表格width与showOverflowTooltip暂不能共存异常
            const tempWidth = column.realWidth || column.width
            if (column.showOVerflowTooltip) {
                return {
                    minWidth: tempWidth + 'px',
                    maxWidth: tempWidth + 'px'
                }
            }
            return { fontSize: '14px' }
        },
        // 第二部分
        getTableData2() {
            this.loading2 = true
            monocle_heatmap_list({
                ...this.monocleForm,
                ...{
                    page: this.paginationConfig2.page,
                    page_size: this.paginationConfig2.size
                }
            }).then((res) => {
                if (res.code == 200) {
                    if (res.count) {
                        this.tableData2 = res.data
                        this.paginationConfig2.total = res.count
                    } else {
                        this.tableData2 = []
                        this.paginationConfig2.total = 0
                    }
                    this.loading2 = false
                }
            })
        },
        goDetail2() {
            this.$router.push({
                path: '/monocleDifferential',
                query: {
                    ...this.monocleForm,
                    ...{
                        gene: this.searchJump2.join(),
                        type: this.radioType
                    }
                }
            })
        },
        goExampleDetail2() {
            let genes = ''
            if (this.monocleForm.species_name == 'Oryza_sativa') {
                genes = 'Os01g0816100,Os01g0323600'
            } else if (this.monocleForm.species_name == 'Zea_mays') {
                genes = 'Zm00001d027290,Zm00001d027330'
            } else if (this.monocleForm.species_name == 'Arabidopsis_thaliana') {
                genes = 'AT2G16005,AT2G37130'
            }
            this.$router.push({
                path: '/monocleDifferential',
                query: {
                    ...this.monocleForm,
                    ...{
                        gene: genes,
                        type: this.radioType
                    }
                }
            })
        },
        handleCurrentChange2(val) {
            this.paginationConfig2.page = val
            this.getTableData2()
        },
        handleSizeChange2(val) {
            this.paginationConfig2.page = 1
            this.paginationConfig2.size = val
            this.getTableData2()
        },
        handlecell(params) {
            if (params.col.label == 'Gene ID') {
                if (this.searchJump.indexOf(params.row.gene_id) == -1) {
                    this.searchJump.push(params.row.gene_id)
                }
            }
        },
        handlecell2(params) {
            if (params.col.label == 'Gene ID') {
                if (this.searchJump2.indexOf(params.row.gene_id) == -1) {
                    this.searchJump2.push(params.row.gene_id)
                }
            }
        }
    }
}
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
