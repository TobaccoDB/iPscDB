<template>
    <div class="PTable">
        <div class="PTable-header">
            <el-form label-position="top" label-width="0" :model="queryInfo" :inline="true">
                <el-form-item label="Species" style="width: 248px">
                    <!-- <el-input v-model="queryInfo.species" @change="change('species')"></el-input> -->
                    <el-select
                        v-model="queryInfo.species"
                        placeholder="Select Species"
                        @change="changeSpecies"
                        clearable
                        >
                        <el-option
                            v-for="item in option1"
                            :key="item"
                            :label="item"
                            :value="item"
                        />
                        </el-select>
                </el-form-item>
                <el-form-item label="Tissue" style="width: 248px">
                    <!-- <el-input v-model="queryInfo.tissue" @change="change('tissue')"></el-input> -->
                    <el-select
                        v-model="queryInfo.tissue"
                        placeholder="Select Tissue"
                        @change="changeTissue"
                        clearable
                        >
                        <el-option
                            v-for="item in option2"
                            :key="item"
                            :label="item"
                            :value="item"
                        />
                        </el-select>
                </el-form-item>
                <el-form-item label="BioProject" style="width: 248px">
                    <!-- <el-input v-model="queryInfo.bioProject" @change="change('bioProject')"></el-input> -->
                    <el-select
                        v-model="queryInfo.bioProject"
                        placeholder="Select BioProject"
                        @change="changeBioProject"
                        clearable
                        >
                        <el-option
                            v-for="item in option3"
                            :key="item"
                            :label="item"
                            :value="item"
                        />
                        </el-select>
                </el-form-item>
                <el-form-item label="Dataset" style="width: 248px">
                    <!-- <el-input v-model="queryInfo.dataset" @change="change('dataset')"></el-input> -->
                    <el-select
                        v-model="queryInfo.dataset"
                        placeholder="Select Dataset"
                        clearable
                        >
                        <el-option
                            v-for="item in option4"
                            :key="item"
                            :label="item"
                            :value="item"
                        />
                        </el-select>
                </el-form-item>
                <el-form-item style="width: calc(100% - 1032px); margin-right: 0; ">
                    <div style="width: 100%; height: 65px; display: flex; align-items: flex-end; justify-content: flex-end;">
                        <el-button type="primary"  @click="change" style="width: 100px;">
                            Search
                        </el-button>
                    </div>
                   
                    <!-- <el-input v-model="queryInfo.dataset" @change="change('dataset')"></el-input> -->
                </el-form-item>
            </el-form>
        </div>
        <div class="PTable-main">
            <el-table :data="tableData" ref="multipleTable" style="width: 100%" border stripe @selection-change="handleSelectionChange">
                <el-table-column type="selection" width="55" align="center"> </el-table-column>
                <!-- :filters="[
                        { text: 'Arabidopsis thaliana', value: '1' },
                        { text: 'Oryza sativa', value: '2' }
                    ]"
                    :filter-method="filterHandler" -->
                <el-table-column prop="species" label="Species" align="center" width="168"> </el-table-column>
                <el-table-column prop="tissue" label="Tissue" align="center" width="120"> </el-table-column>
                <el-table-column prop="bio_project" label="BioProject" align="center" width="129"> </el-table-column>
                <el-table-column prop="dataset" label="Dataset" align="center" width="129" sortable> </el-table-column>
                <el-table-column prop="name" label="Condition" align="center" width="140">
                    <template slot-scope="scope">
                        <Pie :infoData="scope.row.condition"></Pie>
                    </template>
                </el-table-column>
                <el-table-column prop="address" label="Genotype" align="center" width="140">
                    <template slot-scope="scope">
                        <Pie :infoData="scope.row.genotype"></Pie>
                    </template>
                </el-table-column>
                <el-table-column prop="libraries" label="Libraries" align="center" width="115"> </el-table-column>
                <el-table-column prop="age" label="AGE" align="center" width="149"> </el-table-column>
                <el-table-column prop="experiments" label="Experiments" align="center" width="168"> </el-table-column>
                <el-table-column prop="cells" label="Cells" align="center" width="91"> 
                    <template slot-scope="scope">
                        <span>{{ scope.row.cells ? scope.row.cells : 'Under processing' }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="dataset" label="Dataset" align="center" width="115"> </el-table-column>
                <el-table-column prop="pmid" label="PMID" align="center" width="115"> </el-table-column>
                <el-table-column label="Explore" align="center" width="144" fixed="right">
                    <template slot-scope="scope">
                      <el-button @click.native.prevent="download(scope.row, tableData)" :disabled="!scope.row.cells" plain size="small"> Download </el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="PTable-main-page">
                <el-pagination
                    background
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[10, 20, 30, 50]"
                    :page-size="queryInfo.page_size"
                    layout="total, sizes, prev, pager, next"
                    :total="total"
                >
                </el-pagination>
            </div>
<!--            <div class="PTable-main-go">-->
<!--                <div>-->
<!--                    <span style="margin-right: 30px">Integration Type</span>-->
<!--                    <el-radio-group v-model="radio" style="margin-right: 32px">-->
<!--                        <el-radio label="Harmony">Harmony</el-radio>-->
<!--                        <el-radio label="Seurat">Seurat</el-radio>-->
<!--                        <el-radio label="Liger">Liger</el-radio>-->
<!--                    </el-radio-group>-->
<!--                    <el-button type="primary" style="width: 76px" @click="goSearch" :loading="searchIng">GO</el-button>-->
<!--                    <el-button type="primary" style="width: 105px" @click="goExample">Example</el-button>-->
<!--                </div>-->
<!--                <el-button type="primary" style="width: 138px" @click="goQC">Sample QC</el-button>-->
<!--            </div>-->
<!--            <div class="PTable-main-footer">-->
<!--                Due to limited server resources, we only support online integration of three samples. If more than t three samples are integrated, they occupy a lot of resources or take a long time to-->
<!--                run. You are advised to download the generated script and run it locally. <br />-->
<!--                If your required data was not contained in the above, please let us know the specific data you need c or send us the data via email.-->
<!--            </div>-->
        </div>
    </div>
</template>

<script>
import { sra_information_list, integration_zip_download, information_drop_down } from '@/api/api'
import Pie from './Pie.vue'
export default {
    data() {
        return {
            // queryInfo: {
            //     species: '',
            //     tissue: '',
            //     bioProject: '',
            //     dataset: ''
            // },
            tableData: [],
            currentPage: 1,
            multipleSelection: [],
            radio: 'Harmony',
            queryInfo: {
                page: 1,
                page_size: 10,
                species: '',
                tissue: '',
                bioProject: '',
                dataset: ''
            },
            total: 0,
            defaultSelected: [],
            searchIng: false,
            option1: [],
            option2: [],
            option3: [],
            option4: []
        }
    },
    mounted() {
        this.getTableList()
        this.getOptions1()
    },
    methods: {
        searchs(){

        },
        getOptions1(){
            information_drop_down({
                drop_type: 'species'
            })
            .then((res) => {
                if(res.code == 200){
                    this.option1 = res.data
                }
            })
        },
        changeSpecies(val){
                this.option2 = []
                this.option3 = []
                this.option4 = []
                this.queryInfo.tissue = ''
                this.queryInfo.bioProject = ''
                this.queryInfo.dataset = ''
            if(val){
                this.getOptions2()
            }
            
        },
        getOptions2(){
            
            information_drop_down({
                drop_type: 'tissue',
                species: this.queryInfo.species
            })
            .then((res) => {
                if(res.code == 200){
                    this.option2 = res.data
                }
            })
        },
        changeTissue(val){
            this.option3 = []
            this.option4 = []
            this.queryInfo.bioProject = ''
            this.queryInfo.dataset = ''
            if(val){
                this.getOptions3()
            }
            
        },
        getOptions3(){
            information_drop_down({
                drop_type: 'bioProject',
                species: this.queryInfo.species,
                tissue: this.queryInfo.tissue
            })
            .then((res) => {
                if(res.code == 200){
                    this.option3 = res.data
                    
                }
            })
        },
        changeBioProject(val){
            
            this.option4 = []
            this.queryInfo.dataset = ''
            if(val){
                this.getOptions4()
            }
            
        },
        getOptions4(){
            information_drop_down({
                drop_type: 'dataset',
                species: this.queryInfo.species,
                tissue: this.queryInfo.tissue,
                bioProject: this.queryInfo.bioProject
            })
            .then((res) => {
                if(res.code == 200){
                    this.option4 = res.data
                }
            })
        },
        change() {
            // this.queryInfo[filed] = this.queryInfo[filed]
      

            this.queryInfo.page_size = 10
            this.queryInfo.page = 1
            this.getTableList()
        },
        handleSelectionChange(val) {
            this.multipleSelection = val
        },
        goSearch() {
            if (this.multipleSelection.length < 3 || this.multipleSelection.length > 5) {
                this.$message({
                    message: 'Please select 3 to 5 pieces of data!'
                })
                return
            }
            let searchValue = this.multipleSelection.map((item) => item.sample_id)
            this.$router.push({
                path: '/downLoadFile',
                query: {
                    sample_id: searchValue.join(','),
                    integration_type: this.radio
                }
            })
            // this.searchIng = true
            // integration_zip_download({
            //     integration_type: this.radio,
            //     sample_id: searchValue.join(',')
            // })
            //     .then((res) => {
            //         if (res.code == 200) {
            //             console.log(res.data.integration_zip, 'res.data.integration_zip')
            //             const a = document.createElement('a')
            //             a.href = res.data.integration_zip
            //             a.target = '_blank'
            //             a.style.display = 'none'
            //             document.body.appendChild(a)
            //             a.click()
            //             document.body.removeChild(a)
            //         }
            //         this.searchIng = false
            //     })
            //     .catch((err) => {
            //         this.searchIng = false
            //     })
        },
        goExample() {
            // if (this.defaultSelected.length < 3 || this.defaultSelected.length > 5) {
            //     this.$message({
            //         message: 'Please select 3 to 5 pieces of data!'
            //     })
            //     return
            // }
            // let searchValue = this.defaultSelected.map((item) => item.sample_id)
            // this.$router.push({
            //     path: '/integrationDetails',
            //     query: {
            //         sample_id: searchValue.join(','),
            //         integration_type: this.radio
            //     }
            // })
            this.$router.push({
                path: '/integrationDetails',
                query: {
                    integration_type: this.radio
                }
            })
        },
        download(item) {
            if (item.browser_download) {
                const a = document.createElement('a')
                a.href = item.browser_download
                a.target = '_blank'
                a.style.display = 'none'
                document.body.appendChild(a)
                a.click()
                document.body.removeChild(a)
            }
        },
        handleSizeChange(val) {
            this.queryInfo.page_size = val
            this.queryInfo.page = 1
            this.getTableList()
        },
        handleCurrentChange(val) {
            this.queryInfo.page = val
            this.getTableList()
        },
        filterHandler(value, row, column) {
            const property = column['property']
            return row[property] === value
        },
        getTableList() {
            sra_information_list({
                ...this.queryInfo
            }).then((res) => {
                if (res.code === 200) {
                    this.tableData = res.data.results
                    this.total = res.data.count
                    this.$nextTick(() => {
                        // 默认选中第一页的前三个
                        // if (this.tableData.length >= 3 && this.queryInfo.page === 1) {
                        //     let defaultSelect = this.tableData.filter((item, index) => index < 3)
                        //     defaultSelect.forEach((row) => {
                        //         this.$refs.multipleTable.toggleRowSelection(row)
                        //     })
                        //     this.defaultSelected = defaultSelect
                        // }
                    })
                }
            })
        },
        goQC() {
            // this.$router.push('/sampleQCNew')
            if (this.multipleSelection.length <= 0 || this.multipleSelection.length > 1) {
                this.$message({
                    message: 'Please select 1 pieces of data!'
                })
                return
            }

            this.$router.push({
                path: '/sampleQCNew',
                query: {
                    species: this.multipleSelection[0].species,
                    dataset: this.multipleSelection[0].dataset
                }
            })
        }
    },
    components: {
        Pie
    }
}
</script>

<style scoped lang="scss">
.PTable {
    width: 100%;
    height: auto;
    .PTable-header {
        width: 100%;
        height: auto;
        .el-form-item--small.el-form-item {
            margin-bottom: 0;
        }
    }
    .PTable-main {
        width: 100%;
        height: auto;
        padding-top: 10px;
        .PTable-main-page {
            width: 100%;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            // background: yellow;
        }
        .PTable-main-go {
            width: 100%;
            height: 40px;
            font-size: 16px;
            color: #333333;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            span {
                font-weight: bold;
            }
        }
        .PTable-main-footer {
            width: 100%;
            padding: 16px 22px 16px 24px;
            box-sizing: border-box;
            background: #f9fffc;
            border: 1px solid #24a461;
            font-size: 16px;
            color: #0d4126;
            line-height: 24px;
            font-family: PingFangSC-Regular;
        }
    }
}
</style>
<style lang="scss">
.PTable {
    .PTable-header {
        .el-form-item__label {
            padding: 0 !important;
        }
    }
    .PTable-main {
        .el-table td.el-table__cell,
        .el-table th.el-table__cell.is-leaf {
            border-bottom: 1px solid #ebeef5 !important;
            border-top: 1px solid #ebeef5 !important;
        }
        .el-table td,
        .el-table th.is-leaf {
            border-color: #ebeef5 !important;
        }
        .el-table--border,
        .el-table--group {
            border-color: #ebeef5 !important;
        }
        .el-table:before {
            background-color: #ebeef5 !important;
        }
        .el-table--border:after,
        .el-table--group:after,
        .el-table:before {
            background-color: #ebeef5 !important;
        }
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
}
</style>
