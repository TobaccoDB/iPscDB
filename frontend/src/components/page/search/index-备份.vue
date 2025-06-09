<template>
    <div class="search">
        <div class="search-inner">
            <div class="blast">
                <el-form ref="form1" :inline="true" :model="sample_form">
                    <el-form-item label="Species" prop="species_name">
                        <el-select clearable style="width: 200px" size="large" @change="species_nameChange" v-model="sample_form.species_name" placeholder="Choose">
                            <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Tissue" prop="tissue">
                        <el-select clearable style="width: 200px" @change="tissueChange" size="large" v-model="sample_form.tissue" placeholder="Choose">
                            <el-option v-for="(item, index) in sample_form_option.tissueOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Project ID" prop="project_id">
                        <el-select filterable clearable style="width: 200px" @change="project_idChange" size="large" v-model="sample_form.project_id" placeholder="Choose">
                            <el-option v-for="item in sample_form_option.project_idOptions" :key="item.label" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Sample ID">
                        <el-select filterable clearable style="width: 200px" size="large" @change="sample_idChange" v-model="sample_form.sample_id" placeholder="Choose">
                            <el-option v-for="(item, index) in sample_form_option.sample_idOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <!-- <el-form-item label="Sample Name" prop="sample_name">
            <el-select filterable clearable style="width:200px;" @change="sample_nameChange" size="large" v-model="sample_form.sample_name"
              placeholder="Choose">
              <el-option v-for="item in sample_form_option.sample_nameOptions" :key="item.label" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item> -->
                    <el-form-item label="Process Status">
                        <el-select filterable clearable style="width: 200px" size="large" v-model="sample_form.process_status" placeholder="Choose">
                            <el-option v-for="(item, index) in sample_form_option.process_statusOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="">
                        <el-button class="btnSearch" @click="search" :loading="loading">GO</el-button>
                    </el-form-item>
                </el-form>
            </div>
            <el-table
                size="small"
                :data="tableData"
                :header-cell-style="headerStyle"
                :header-cell-class-name="cellClass"
                @selection-change="handleSelectionChange"
                v-loading="loading"
                element-loading-text="running"
                :cell-style="cellstyle"
                @cell-click="handlecell"
                border
                style="width: 100%"
            >
                <el-table-column type="selection" width="55" align="center" :selectable="selected"> </el-table-column>
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
                        <span v-if="item.label == 'Sample ID' && scope.row['is_sample_rds'] == '1'"
                            >{{ scope.row[item.key] }}
                            <i class="downloadIcon" @click="rdsDownload(scope.row.sample_id)"></i>
                        </span>
                        <span v-else-if="item.label == 'Process Status' && scope.row[item.key] == 'QC Fail'" class="statusSpan1">{{ scope.row[item.key] }} </span>
                        <span v-else-if="item.label == 'Process Status' && scope.row[item.key] == 'QC Pass'" class="statusSpan2">{{ scope.row[item.key] }} </span>
                        <span v-else-if="item.label == 'Process Status' && scope.row[item.key] == 'Under process'" class="statusSpan3">{{ scope.row[item.key] }} </span>
                        <span v-else>{{ scope.row[item.key] }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="Publication" prop="lit_id" align="center" width="120">
                    <template slot-scope="scope">
                        <span v-for="(item, index) in scope.row.lit_id" :key="index">
                            <!-- <span v-if="/^(10\.|DOI:)/.test(item)" style="float:left;width:50%;">{{item}}</span> -->
                            <el-popover placement="top" trigger="hover" :content="item.value.toString()">
                                <!-- <span slot="reference">{{ `${scope.row[item.key].toString().trim().slice(0,showLen)}...` }}</span> -->
                                <span slot="reference" class="litClass" @click="jumpLink(item.value)">
                                    <i class="el-icon-document" style="font-size: 16px; color: #0a9daa"></i>
                                </span>
                            </el-popover>
                            <!-- <span class="litClass" @click="jumpLink(item.value)">
                <i class="el-icon-document"></i>
              </span> -->
                        </span>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination
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
            <div class="radioType">
                <span>Integration Type:</span>
                <el-radio-group v-model="radioType">
                    <el-radio label="Harmony">Harmony</el-radio>
                    <el-radio label="Seurat">Seurat</el-radio>
                    <el-radio label="Liger">Liger</el-radio>
                </el-radio-group>
                <el-button type="primary" size="lager" style="margin-left: 20px" @click="goDetail">GO</el-button>
                <el-button type="primary" size="lager" style="margin-left: 20px" @click="goExampleDetail">Example</el-button>
            </div>
            <p class="tips">
                Due to limited server resources, we only support online integration of two samples. If more than two samples are integrated, they occupy a lot of resources or take a long time to run.
                You are advised to download the generated script and run it locally.<br />If your required data was not contained in the above, please let us know the specific data you need or send us
                the data via email.
            </p>
        </div>
    </div>
</template>

<script>
import { plant_search_down, tissue_type_down, project_id_down, sample_id_down, sample_name_down, process_status_down, sample_plant_search } from '@/api/api'
import jgTable from '@/components/jgTable/index'

export default {
    name: 'search',
    components: {
        jgTable
    },
    data() {
        return {
            sample_form: {
                species_name: '',
                tissue: '',
                project_id: '',
                sample_id: '',
                sample_name: '',
                process_status: ''
            },
            speciesOptions: [],
            sample_form_option: {
                tissueOptions: [],
                project_idOptions: [],
                sample_idOptions: [],
                sample_nameOptions: [],
                process_statusOptions: []
            },
            tableData: [],
            column: [
                { key: 'species_name', label: 'Specie Name', width: 200 },
                { key: 'project_id', label: 'Project ID', width: 150 },
                { key: 'sample_id', label: 'Sample ID', width: 180 },
                { key: 'tissue', label: 'Tissue', width: 100 },
                { key: 'process_status', label: 'Process Status', width: 150 },
                { key: 'sample_name', label: 'Sample Name', width: 260 },
                { key: 'geno_type', label: 'Genotype', width: 150 },
                { key: 'treament', label: 'Treament', width: 200 },
                { key: 'ecotype', label: 'Ecotype', width: 250 },
                { key: 'age', label: 'Age', width: 100 },
                { key: 'chemistry', label: 'Chemistry', width: 100 }
                // { key: 'species_name', label: 'Specie Name', width: 154 },
                // { key: 'project_id', label: 'Project ID', width: 114 },
                // { key: 'sample_id', label: 'Sample ID', width: 130 },
                // { key: 'tissue', label: 'Tissue', width: 80 },
                // { key: 'process_status', label: 'Process Status', width: 100 },
                // { key: 'sample_name', label: 'Sample Name' },
                // { key: 'geno_type', label: 'Genotype' },
                // { key: 'treament', label: 'Treament' },
                // { key: 'ecotype', label: 'Ecotype' },
                // { key: 'age', label: 'Age', width: 68 },
                // { key: 'chemistry', label: 'Chemistry', width: 94 },
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
            multipleSelection: [],
            radioType: 'Harmony'
        }
    },
    mounted() {
        this.init()
        this.getTableData()
    },
    methods: {
        init() {
            plant_search_down({}).then((res) => {
                if (res.code == 200) {
                    this.speciesOptions = res.data
                }
            })
        },
        species_nameChange() {
            tissue_type_down({ species_name: this.sample_form.species_name }).then((res) => {
                if (res.code == 200) {
                    this.sample_form.tissue = ''
                    this.sample_form.project_id = ''
                    this.sample_form.sample_id = ''
                    this.sample_form.sample_name = ''
                    this.sample_form.process_status = ''
                    this.sample_form_option.project_idOptions = []
                    this.sample_form_option.sample_idOptions = []
                    this.sample_form_option.sample_nameOptions = []
                    this.sample_form_option.process_statusOptions = []
                    this.sample_form_option.tissueOptions = res.data
                }
            })
        },
        tissueChange() {
            project_id_down({ species_name: this.sample_form.species_name, tissue: this.sample_form.tissue }).then((res) => {
                if (res.code == 200) {
                    this.sample_form.project_id = ''
                    this.sample_form.sample_id = ''
                    this.sample_form.sample_name = ''
                    this.sample_form.process_status = ''
                    this.sample_form_option.sample_idOptions = []
                    this.sample_form_option.sample_nameOptions = []
                    this.sample_form_option.process_statusOptions = []
                    this.sample_form_option.project_idOptions = res.data
                }
            })
        },
        project_idChange(val) {
            sample_id_down({
                species_name: this.sample_form.species_name,
                tissue: this.sample_form.tissue,
                project_id: val
            }).then((res) => {
                if (res.code == 200) {
                    this.sample_form.sample_id = ''
                    this.sample_form.sample_name = ''
                    this.sample_form.process_status = ''
                    this.sample_form_option.sample_nameOptions = []
                    this.sample_form_option.process_statusOptions = []
                    this.sample_form_option.sample_idOptions = res.data
                }
            })
        },
        sample_idChange(val) {
            // sample_name_down({
            //   species_name: this.sample_form.species_name,
            //   tissue: this.sample_form.tissue,
            //   project_id: this.sample_form.project_id,
            //   sample_id: val
            // }).then(res => {
            //   if (res.code == 200) {
            //     this.sample_form.sample_name = ''
            //     this.sample_form.process_status = ''
            //     this.sample_form_option.process_statusOptions = []
            //     this.sample_form_option.sample_nameOptions = res.data
            //   }
            // });
            process_status_down({
                species_name: this.sample_form.species_name,
                tissue: this.sample_form.tissue,
                project_id: this.sample_form.project_id,
                sample_id: this.sample_form.sample_id,
                sample_name: val
            }).then((res) => {
                if (res.code == 200) {
                    this.sample_form.process_status = ''
                    this.sample_form_option.process_statusOptions = res.data
                }
            })
        },
        sample_nameChange(val) {
            process_status_down({
                species_name: this.sample_form.species_name,
                tissue: this.sample_form.tissue,
                project_id: this.sample_form.project_id,
                sample_id: this.sample_form.sample_id,
                sample_name: val
            }).then((res) => {
                if (res.code == 200) {
                    this.sample_form.process_status = ''
                    this.sample_form_option.process_statusOptions = res.data
                }
            })
        },
        search(param) {
            this.paginationConfig.page = 1
            this.getTableData()
        },
        // 表格部分
        getTableData() {
            this.loading = true
            sample_plant_search({
                ...this.sample_form,
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
        handleSelectionChange(val) {
            this.multipleSelection = val
        },
        //判断后台给返回的状态码
        selected(row, index) {
            if (row.is_sample_rds == 1) {
                return true //不可勾选
            } else {
                return false //可勾选
            }
        },
        goDetail() {
            if (this.multipleSelection.length < 2 || this.multipleSelection.length > 5) {
                this.$message('Please select 2 to 5 pieces of data!')
                return
            }

            let sample_id = []
            this.multipleSelection.forEach((item) => {
                sample_id.push(item.sample_id)
            })
            if (sample_id.length > 2) {
                this.$confirm('The script can be downloaded if the script occupies a large number of resources and takes a long time to run', 'Tips', {
                    confirmButtonText: 'Confirm',
                    cancelButtonText: 'Cancel',
                    type: 'warning'
                })
                    .then(() => {
                        // console.log('进入下载脚本的页面(新增页面)')
                        this.$router.push({
                            path: '/integrationNewDetails',
                            query: {
                                integration_type: this.radioType,
                                sample_id: sample_id.join(',')
                            }
                        })
                    })
                    .catch(() => {
                        // console.log('直接进入现在的详情页')
                        this.$router.push({
                            path: '/integrationDetails',
                            query: {
                                integration_type: this.radioType,
                                sample_id: sample_id.join(',')
                            }
                        })
                    })
            } else {
                this.$router.push({
                    path: '/integrationDetails',
                    query: {
                        integration_type: this.radioType,
                        sample_id: sample_id.join(',')
                    }
                })
            }
        },
        goExampleDetail() {
            this.$router.push({
                path: '/integrationDetails',
                query: {
                    integration_type: this.radioType
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
        cellClass(row) {
            if (row.columnIndex === 0) {
                return 'DisableSelection'
            }
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
        rdsDownload(sample_id) {
            this.jg_downloadFile('api/v1/plant_sample_rds_download/', {
                sample_id: sample_id
            })
        },
        jumpLink(url) {
            window.open(url, '_blank')
        }
    }
}
</script>
<style lang="scss" scoped>
@import './style.scss';
</style>
