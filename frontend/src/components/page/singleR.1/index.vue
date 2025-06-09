<template>
    <div class="singleR">
        <div class="singleR-inner">
            <div class="scsa" v-loading="loading" element-loading-text="The program is running and may take 1-2 minutes.">
                <p class="keyword_p1">
                    SingleR:
                    <span style="font-size: 16px">Reference data-based cell-type prediction</span>
                </p>
                <el-form ref="form1" :model="singler_form">
                    <el-form-item label="Reference database" prop="species">
                        <el-select size="large" style="width: 300px" v-model="singler_form.species" placeholder="Choose">
                            <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="Cluster" style="width: 100%" class="firstItem">
                        <el-input type="textarea" :autosize="{ minRows: 4, maxRows: 6 }" placeholder="Please enter the contents" v-model="singler_form.custer" style="width: calc(100% - 80px)">
                        </el-input>
                    </el-form-item>
                </el-form>
                <p class="file_p">
                    <span style="padding: 0 12px 0 0">Or cluster file</span>
                    <a href="javascript:;" class="file"
                        >Open File
                        <input type="file" name="file" ref="file" @change="handleUpdate($event)" />
                    </a>
                    <span>{{ fileName }}</span>
                    <i class="el-icon-download pointer" style="padding: 0 5px; color: #24a461; cursor: pointer" @click="download"> Download Cluster sample file </i>
                </p>
                <p class="file_p">
                    <el-radio-group v-model="radio">
                        <el-radio label="h5">H5</el-radio>
                        <el-radio label="tar">Tar</el-radio>
                    </el-radio-group>
                    <span style="padding: 0 12px">CellRanger Matrix</span>
                    <a href="javascript:;" class="file"
                        >Open File
                        <input type="file" name="file" ref="file2" @change="handleUpdate2($event)" />
                    </a>
                    <span>{{ fileName2 }}</span>
                    <i class="el-icon-download pointer" style="padding: 0 5px; color: #24a461; cursor: pointer" @click="download2"> Download Matrix sample file </i>
                </p>
                <el-row style="margin: 20px 0px 20px 0">
                    <el-button class="btnSearch" @click="example">Example</el-button>
                    <el-button class="btnSearch" style="width: 80px" @click="search">GO</el-button>
                    <el-button class="btnReset" @click="reset">Reset</el-button>
                </el-row>
                <ul class="scsa_bottom_ul">
                    <li>Input format description</li>
                    <li style="font-weight: 700; font-size: 16px">Cluster file (TXT, split by Tab):</li>
                    <li>Column1: index for cell</li>
                    <li>Column2: cluster ID for cell</li>
                    <li style="font-weight: 700; font-size: 16px">Matrix file (Output of Cellranger):</li>
                    <li>1. H5 format</li>
                    <li>Or 2. Tar format (barcodes.tsv.gz, features.tsv.gz, matrix.mtx.gz)</li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
import axios from '@/api/http.js'
import Axios from 'axios'
import { specie_list } from '@/api/api'
export default {
    name: 'singleR',
    components: {},
    data() {
        return {
            speciesOptions: [
                { label: 'Arabidopsis.Leaf.33955487', value: 'Arabidopsis.leaf.33955487.ref.Rdata' },
                { label: 'Arabidopsis.Root.31004836', value: 'Arabidopsis.Root.31004836.ref.Rdata' },
                { label: 'Maize.Ear.33400914', value: 'maize.ear.33400914.ref.Rdata' },
                { label: 'Maize.Leaf.33955497', value: 'maize.leaf.33955497.ref.Rdata' },
                { label: 'Maize.SAM.33400914', value: 'maize.SAM.33400914.ref.Rdata' },
                { label: 'Rice.Root.33352304', value: 'rice.root.33352304.ref.Rdata' }
            ],
            singler_form: {
                custer: '',
                species: 'Arabidopsis.leaf.33955487.ref.Rdata'
            },
            rules: {
                custer: [{ required: true, message: 'Please enter', trigger: 'blur' }],
                species: [{ required: true, message: 'Please select', trigger: 'change' }]
            },
            file: '',
            fileName: '',
            file2: '',
            fileName2: '',
            loading: false,
            radio: 'h5'
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        init() {
            // specie_list({}).then(res => {
            //   if (res.code == 200) {
            //     this.speciesOptions = res.data
            //   }
            // });
        },
        example() {
            this.singler_form = {
                custer: '1	1\n2	6\n3	11\n4	13\n5	3\n6	10\n7	13\n8	6\n9	1\n10	1\n11	14\n12	3\n13	2\n14	8\n15	4\n16	0\n17	5\n18	8',
                species: 'Arabidopsis.leaf.33955487.ref.Rdata'
            }
        },
        search() {
            if (this.file == '' && this.file2 == '' && this.singler_form.custer == '') {
                this.$message.warning('Please input or select a file！')
                return
            }
            this.loading = true
            let formData = new FormData()
            formData.append('reference_database', this.singler_form.species)
            formData.append('custer_file', this.file)
            formData.append('cell_range', this.file2)
            formData.append('custer', this.singler_form.custer)
            formData.append('type', this.radio)
            let config = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
            sessionStorage.removeItem('singleR')
            const $axios = Axios.create({
                baseURL: axios.defaults.baseURL,
                timeout: 1000000
            })

            $axios
                .post('/api/v1/cell_single_file/', formData, config)
                .then((res) => {
                    if (res.data.code == 200) {
                        sessionStorage.setItem('singleR', JSON.stringify(res.data.data))
                        this.loading = false
                        this.$router.push('/singleRDetails')
                    } else {
                        this.$message.warning(res.data.msg)
                    }
                })
                .catch((err) => {
                    this.$message.warning(err.data.msg)
                })
        },
        reset() {
            this.fileName = ''
            this.file = ''
            this.fileName2 = ''
            this.file2 = ''
            this.singler_form = {
                custer: '',
                species: 'Arabidopsis.leaf.33955487.ref.Rdata'
            }
            this.loading = false
            this.$refs['form1'].resetFields()
        },
        handleUpdate(event) {
            if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'txt') {
                this.$message.warning('Please upload .txt file！')
            } else {
                this.fileName = event.target.files[0].name
                this.file = event.target.files[0]
                sessionStorage.setItem('files', JSON.stringify(event.target.files[0]))
            }
        },
        handleUpdate2(event) {
            if (this.radio == 'h5' && event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'h5') {
                this.$message.warning('Please upload .h5 file！')
            } else if (this.radio == 'tar' && event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'tar') {
                this.$message.warning('Please upload .tar file！')
            } else {
                this.fileName2 = event.target.files[0].name
                this.file2 = event.target.files[0]
                sessionStorage.setItem('files2', JSON.stringify(event.target.files[0]))
            }
        },
        download() {
            this.jg_downloadFile('api/v1/cell_single_file/single_r_download', { name: 'test_clusters.txt' })
        },
        download2() {
            if (this.radio == 'h5') {
                this.jg_downloadFile('api/v1/cell_single_file/single_r_download', { name: 'filtered_feature_bc_matrix.h5' })
            } else {
                this.jg_downloadFile('api/v1/cell_single_file/single_r_download', { name: 'filtered_feature_bc_matrix_test.tar' })
            }
        }
    }
}
</script>
<style lang="scss" scoped>
@import './style.scss';
</style>
