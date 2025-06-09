<template>
    <div class="searchForm">
        <div class="searchFormMain">
            <div class="searchFormMainItem">
                <h1 class="searchFormMainItemName">By marker gene (identifier or keyword)</h1>
                <div class="searchFormMainItemContent">
                    <span style="margin-right: 10px">Species</span>
                    <el-select v-model="form1.searchValue" placeholder="choose" style="width: 217px; margin-right: 10px">
                        <el-option :label="item" :value="item" v-for="(item, index) in formOption" :key="index"> </el-option>
                    </el-select>
                    <el-input v-model="form1.value"></el-input>
                </div>
                <div class="searchFormMainItemButton">
                    <el-button type="success" style="width: 100px" @click="Example1">Example</el-button>
                    <el-button type="success" style="width: 100px" @click="Search1">Search</el-button>
                    <el-button type="info" style="width: 100px" @click="reset1">Reset</el-button>
                </div>
            </div>
            <div class="searchFormMainItem" v-loading="form2Loading">
                <h1 class="searchFormMainItemName">By sequence (Blast)</h1>
                <div class="searchFormMainItemTextarea">
                    <el-input type="textarea" placeholder="Input a FASTA sequence here" v-model="form2.textarea" resize="none" style="height: 92px; resize: none"> </el-input>
                </div>
                <div class="searchFormMainItemContent">
                    <span style="margin-right: 10px">Program</span>
                    <el-select v-model="form2.program" placeholder="choose" style="width: 200px; margin-right: 20px">
                        <el-option :label="item" :value="item" v-for="(item, index) in formOption2.program" :key="index"> </el-option>
                    </el-select>
                    <span style="margin-right: 10px">Species</span>
                    <el-select v-model="form2.species" placeholder="choose" style="width: 200px; margin-right: 20px">
                        <el-option :label="item.name" :value="item.value" v-for="(item, index) in formOption2.species" :key="index"> </el-option>
                    </el-select>
                    <span style="margin-right: 10px">Database</span>
                    <el-select v-model="form2.database" placeholder="choose" style="width: 200px; margin-right: 20px">
                        <el-option :label="item.name" :value="item.value" v-for="(item, index) in formOption2.database" :key="index"> </el-option>
                    </el-select>
                    <span style="margin-right: 10px">E-value</span>
                    <el-select v-model="form2.Evalue" placeholder="choose" style="width: 200px">
                        <el-option :label="item" :value="item" v-for="(item, index) in formOption2.EValue" :key="index"> </el-option>
                    </el-select>
                </div>
                <div class="searchFormMainItemFile">
                    <span>or upload sequence FASTA file</span>
                    <a href="javascript:;" class="file" style="margin-right: 20px"
                        >Browse
                        <input type="file" name="file" ref="file" @change="handleUpdate($event)" />
                    </a>
                    <span>{{ fileName }}</span>
                </div>
                <div class="searchFormMainItemButton">
                    <el-button type="success" style="width: 100px" @click="ExampleButton2">Example</el-button>
                    <el-button type="success" style="width: 100px" @click="SearchButton2">Search</el-button>
                    <el-button type="info" style="width: 100px" @click="ResetButton2">Reset</el-button>
                </div>
            </div>
            <div class="searchFormMainItem">
                <h1 class="searchFormMainItemName">By cell type</h1>
                <div class="searchFormMainItemContent">
                    <span style="margin-right: 10px">Species</span>
                    <el-select v-model="form3.species" placeholder="choose" style="width: 200px; margin-right: 20px" @change="change31" ref="select31">
                        <el-option :label="item.specie_name" :value="item.specie_name" v-for="(item, index) in formOption3" :key="index"> </el-option>
                    </el-select>
                    <span style="margin-right: 10px">Tissue</span>
                    <el-select v-model="form3.tissue" placeholder="choose" style="width: 200px; margin-right: 20px" @change="change32" ref="select32">
                        <el-option :label="item.tissue_name" :value="item.tissue_name" v-for="(item, index) in formOption32" :key="index"> </el-option>
                    </el-select>
                    <span style="margin-right: 10px">Cell type</span>
                    <el-select v-model="form3.cell_type" placeholder="choose" style="width: 200px; margin-right: 20px">
                        <el-option :label="item.cell_name" :value="item.cell_name" v-for="(item, index) in formOption33" :key="index"> </el-option>
                    </el-select>
                </div>
                <div class="searchFormMainItemButton">
                    <el-button type="success" style="width: 100px" @click="Example3">Example</el-button>
                    <el-button type="success" style="width: 100px" @click="Search3">Search</el-button>
                    <el-button type="info" style="width: 100px" @click="Reset3">Reset</el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { marker_list, search_cell_select_data, blast_list, blast_data } from '@/api/api'
export default {
    data() {
        return {
            form1: {
                searchValue: '',
                value: ''
            },
            formOption: [],
            form2: {
                textarea: '',
                program: '',
                species: '',
                database: '',
                Evalue: ''
            },
            form2Loading: false,
            formOption2: {
                program: [],
                database: [],
                EValue: [],
                species: []
            },
            formOption3: [],
            formOption32: [],
            formOption33: [],
            form3: {
                species: '',
                tissue: '',
                cell_type: ''
            },
            fileName: '',
            file: null
        }
    },
    mounted() {
        this.getForm1Option()
        this.getSelection2()
        this.getSelection3()
    },
    methods: {
        handleUpdate(event) {
            if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'fa') {
                this.$message.warning('Please upload .fa file！')
            } else {
                this.fileName = event.target.files[0].name
                this.file = event.target.files[0]
                console.log(this.file, event.target.files)
                // sessionStorage.setItem('files', JSON.stringify(event.target.files[0]))
            }
        },
        getInfo() {
            this.form2Loading = true

            // 添加其他字段到 FormData 对象中（可选）

            let formData = new FormData()
            if (this.file) {
                formData.append('file', this.file)
            }

            formData.append('search_method', this.form2.program)
            formData.append('species', this.form2.species)
            formData.append('database', this.form2.database)
            formData.append('evalue', this.form2.Evalue)
            formData.append('query_sequence', this.form2.textarea)

            blast_data(formData)
                .then((res) => {
                    if (res.data.code == 200) {
                        sessionStorage.setItem('tableData', JSON.stringify(res.data.data.data))
                        this.$router.push({
                            path: '/searchBlast'
                        })
                    }
                    this.form2Loading = false
                })
                .catch(() => {
                    this.form2Loading = false
                })
        },
        getForm1Option() {
            marker_list().then((res) => {
                if (res.code == 200) {
                    this.formOption = res.data
                }
            })
        },
        getSelection2() {
            blast_list().then((res) => {
                if (res.code == 200) {
                    console.log(res.data)
                    this.formOption2 = {
                        program: res.data.program,
                        database: res.data.database,
                        EValue: res.data['e-value'],
                        species: res.data.species
                    }
                }
            })
        },
        getSelection3() {
            search_cell_select_data().then((res) => {
                if (res.code == 200) {
                    this.formOption3 = res.data
                }
            })
        },
        change31(item) {
            for (let i = 0; i < this.formOption3.length; i++) {
                if (this.formOption3[i].specie_name == item) {
                    this.formOption32 = this.formOption3[i].child
                }
            }
            this.formOption33 = []
            this.form3.tissue = ''
            this.form3.cell_type = ''
        },
        change32(item) {
            for (let i = 0; i < this.formOption32.length; i++) {
                if (this.formOption32[i].tissue_name == item) {
                    this.formOption33 = this.formOption32[i].child
                }
            }
            this.form3.cell_type = ''
        },
        Example1() {
            this.form1.searchValue = this.formOption.length > 0 ? this.formOption[0] : ''
            this.form1.value = 'RBB1'
        },
        Search1() {
            if (this.form1.searchValue == '') {
                this.$message.error('Please select search criteria')
                return
            }
            if (this.form1.value == '') {
                this.$message.error('Please enter search content')
                return
            }
            this.$router.push({
                path: '/searchMarker',
                query: {
                    species_name: this.form1.searchValue,
                    search_gene: this.form1.value
                }
            })
        },
        reset1() {
            this.form1.searchValue = ''
            this.form1.value = ''
        },
        Search3() {
            if (!this.form3.species) {
                this.$message.error('Please select Species')
                return
            }
            if (!this.form3.tissue) {
                this.$message.error('Please select Tissue')
                return
            }
            if (!this.form3.cell_type) {
                this.$message.error('Please select Cell type')
                return
            }
            this.$router.push({
                path: '/searchCellType',
                query: {
                    species_name: this.form3.species,
                    tissue_name: this.form3.tissue,
                    cell_name: this.form3.cell_type
                }
            })
        },
        Example3() {
            this.form3.species = this.formOption3[0].specie_name
            this.formOption32 = this.formOption3[0].child
            this.form3.tissue = this.formOption32[0].tissue_name
            this.formOption33 = this.formOption32[0].child
            this.form3.cell_type = this.formOption33[0].cell_name
        },
        Reset3() {
            this.form3.species = ''
            this.formOption32 = []
            this.form3.tissue = ''
            this.formOption33 = []
            this.form3.cell_type = ''
        },
        ExampleButton2() {
            this.form2.program = 'blastn'
            this.form2.species = 'Arabidopsis_thaliana'
            this.form2.database = 'cds'
            this.form2.Evalue = '1e-5'
            this.form2.textarea = `>Test_seq
ATGCAGATCTTTGTTAAGACTCTCACCGGAAAGACTATCACCCTCGAGGTGGAAAGCTCTGACACCATCGACAACGTTAA
GGCCAAGATCCAGGATAAGGAAGGCATTCCTCCGGATCAGCAGAGGTTGATCTTCGCTGGAAAGCAGTTGGAGGATGGCA
GAACTCTTGCTGACTACAACATCCAGAAGGAGTCCACACTTCATCTTGTTCTCAGGCTCCGTGGTGGTATGCAGATCTTT
GTCAAGACGTTGACTGGAAAGACTATCACTTTGGAGGTGGAGAGCTCTGACACTATCGACAATGTCAAAGCCAAGATCCA
GGACAAAGAGGGTATCCCACCGGACCAGCAGAGATTGATCTTCGCCGGAAAACAACTTGAAGATGGTAGAACTTTGGCTG
ACTACAACATTCAGAAGGAGTCTACACTTCACTTGGTGTTGCGTCTCCGTGGAGGTATGCAGATTTTCGTGAAGACTCTC
ACTGGAAAGACCATTACTCTTGAAGTTGAGAGCTCCGACACCATTGACAACGTGAAGGCTAAGATCCAGGACAAGGAAGG
TATCCCTCCGGACCAGCAGCGTCTCATCTTCGCTGGAAAACAGCTTGAGGATGGTCGTACTTTGGCCGACTACAACATCC
AGAAGGAGTCTACCCTTCACTTGGTGCTAAGGCTCCGTGGTGGTTTCTAA`
        },
        SearchButton2() {
            // console.log(this.form2)
            // let queryInfo = {
            //     search_method: this.form2.program,
            //     species: this.form2.species,
            //     database: this.form2.database,
            //     evalue: this.form2.Evalue,
            //     query_sequence: this.form2.textarea
            // }
            if (!this.form2.program) {
                this.$message.error('Please select Program')
                return
            }
            if (!this.form2.species) {
                this.$message.error('Please select Species')
                return
            }
            if (!this.form2.database) {
                this.$message.error('Please select Database')
                return
            }
            if (!this.form2.Evalue) {
                this.$message.error('Please select E-value')
                return
            }
            this.getInfo()
        },
        ResetButton2() {
            this.form2 = {
                textarea: '',
                program: '',
                species: '',
                database: '',
                Evalue: ''
            }
        }
    }
}
</script>

<style scoped lang="scss">
.searchForm {
    width: 100%;
    height: 100%;

    .searchFormMain {
        width: 1240px;
        height: auto;
        min-height: 800px;
        background: #fff;
        padding: 0 20px;
        box-sizing: border-box;
        margin: 0 auto;

        .searchFormMainItem {
            width: 100%;
            height: auto;
            border-bottom: 1px solid #24a461;

            &:last-child {
                border-color: transparent;
            }

            .searchFormMainItemName {
                width: 100%;
                height: 70px;
                line-height: 70px;
                font-weight: 700;
                font-size: 18px;
                color: #000;
            }

            .searchFormMainItemContent {
                width: 100%;
                height: 40px;
                display: flex;
                align-items: center;
                margin-bottom: 10px;
            }

            .searchFormMainItemFile {
                width: 100%;
                height: 50px;

                // background: yellowgreen;
                span {
                    display: inline-block;
                    // padding-left: 30px;
                }

                .file {
                    position: relative;
                    display: inline-block;
                    background: #24a461;
                    border-radius: 4px;
                    overflow: hidden;
                    color: #fff;
                    text-decoration: none;
                    text-indent: 0;
                    line-height: 30px;
                    cursor: pointer;
                    width: 100px;
                    height: 30px;
                    text-align: center;
                    top: 8px;
                    left: 15px;

                    input {
                        position: absolute;
                        font-size: 100px;
                        right: 0;
                        top: 0;
                        opacity: 0;
                        cursor: pointer;
                    }
                }
            }

            .searchFormMainItemTextarea {
                width: 100%;
                height: 92px;
                margin-bottom: 10px;
            }

            .searchFormMainItemButton {
                width: 100%;
                height: 40px;
                display: flex;
                align-items: center;
                margin-bottom: 40px;
            }
        }
    }
}
</style>

<style>
.searchFormMainItemTextarea textarea {
    height: 92px !important;
}

.searchFormMainItemButton .el-button--success {
    background: #24a461;
}
</style>
