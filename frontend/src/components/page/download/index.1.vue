<template>
    <div class="download">
        <div class="download-inner">
            <div style="background: #fff; height: 52px; padding: 13px 0 0 0; margin-bottom: 5px">
                <el-form ref="form1" :inline="true">
                    <el-form-item label="Species">
                        <el-select size="large" v-model="download_form.species_type" @change="SpecieChange" placeholder="Choose">
                            <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Tissue">
                        <el-select clearable size="large" v-model="download_form.tissue_type" placeholder="Choose">
                            <el-option v-for="(item, index) in tissueOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Type">
                        <el-select size="large" clearable v-model="download_form.marker_resource" placeholder="Choose">
                            <el-option v-for="(item, index) in resourceOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="">
                        <el-button class="btnSearch" style="width: 80px" @click="search">GO</el-button>
                    </el-form-item>
                </el-form>
            </div>
            <!-- 表格 -->
            <jg-table
                :tableData="tableData"
                :column="column"
                :tableHeight="tableHeight"
                operationText="Download"
                :paginationConfig="paginationConfig"
                @handleCurrentChange="handleCurrentChange"
                @handleSizeChange="handleSizeChange"
                :isHaveDownload="true"
                @downloadHandle="downloadHandle"
            ></jg-table>
        </div>
    </div>
</template>

<script>
import { specie_list, cell_download } from '@/api/api'
import { cell_search_down } from '@/api/search'
import jgTable from '@/components/jgTable/index'
export default {
    name: 'download',
    components: {
        jgTable
    },
    data() {
        return {
            resourceOptions: [
                {
                    label: 'Project RDS',
                    value: 'Project RDS'
                },
                {
                    label: 'Cell Marker',
                    value: 'Cell Marker'
                }
            ],
            download_form: {
                marker_resource: 'Project RDS',
                species_type: 'Arabidopsis_thaliana',
                tissue_type: ''
            },
            speciesOptions: [],
            tissueOptions: [],
            tableHeight: window.innerHeight - 381,
            tableData: [],
            column: [
                { key: 'species_type', label: 'Spacies' },
                { key: 'tissue_type', label: 'Tissue' },
                { key: 'Type', label: 'Type' }
            ],
            paginationConfig: {
                page: 1,
                size: 10,
                sizes: [10, 20, 30],
                total: 0
            }
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        init() {
            specie_list({}).then((res) => {
                if (res.code == 200) {
                    this.speciesOptions = res.data
                    this.getTableData()
                }
            })
            // this.SpecieChange()
        },
        SpecieChange() {
            cell_search_down({
                species_type: this.download_form.species_type
            }).then((res) => {
                if (res.code == 200) {
                    this.download_form.tissue_type = ''
                    this.tissueOptions = res.data
                }
            })
        },
        getTableData() {
            cell_download({
                ...this.download_form,
                ...{
                    page: this.paginationConfig.page,
                    page_size: this.paginationConfig.size
                }
            }).then((res) => {
                if (res.code == 200) {
                    res.data.results.forEach((item) => {
                        if (item.marker_resource == 'all') {
                            item.marker_resource = 'All'
                        }
                    })
                    this.tableData = res.data.results
                    this.paginationConfig.total = res.data.count
                }
            })
        },
        search() {
            this.getTableData()
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
        downloadHandle(params, type) {
            this.jg_downloadFile('api/v1/cell_download/cell_marker_download/', { id: params.row.id, type: type })
        }
    }
}
</script>
<style lang="scss" scoped>
.download {
    width: 1240px;
    height: 100%;
    margin: 0 auto;
    background: #fafafa;
    padding: 30px 0;
    .download-inner {
        width: 1200px;
        padding: 20px;
        margin: 0 auto;
        overflow: hidden;
        background: rgba(255, 255, 255, 1);
        .btnSearch {
            width: 125px;
            height: 40px;
            background: #24a461;
            font-size: 18px;
            font-family: PingFang SC;
            color: #fff;
            outline: none;
            border: none;
            cursor: pointer;
        }
    }
}
</style>
