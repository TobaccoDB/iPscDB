<template>
    <div class="eSCP">
        <div class="eSCP-inner">
            <div class="efpTitle">electronic Single-Cell Pictograph</div>
            <el-form ref="form1" class="efp_form" :inline="true" :model="sample_form">
                <el-form-item label="Species" prop="species_name">
                    <el-select clearable style="width: 200px" size="large" @change="species_nameChange" v-model="sample_form.species_name" placeholder="Choose">
                        <el-option v-for="(item, index) in speciesOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="Tissue" prop="tissue">
                    <el-select clearable style="width: 200px" size="large" v-model="sample_form.tissue" placeholder="Choose">
                        <el-option v-for="(item, index) in tissueOptions" :key="index" :label="item.label" :value="item.value"> </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="Gene">
                    <!-- <el-input clearable style="width:200px;" size="large" v-model="sample_form.gene_id"></el-input> -->
                    <el-select
                        v-model="sample_form.gene_id"
                        style="width: 200px"
                        size="large"
                        filterable
                        remote
                        reserve-keyword
                        placeholder="Please enter"
                        :remote-method="remoteMethod"
                        :loading="GeneLoading"
                    >
                        <el-option v-for="item in GeneOptions" :key="item.value" :label="item.name" :value="item.value"> </el-option>
                    </el-select>
                </el-form-item>
                <el-button type="primary" size="lager" style="margin-left: 20px" @click="Example">Example</el-button>
                <el-button type="primary" size="lager" style="margin-left: 20px" @click="svgData">GO</el-button>
            </el-form>
            <div v-show="stage_svg" class="svgClass" ref="efpPlant" v-loading="loading" v-html="stage_svg"></div>
            <p v-if="stage_svg == ''" v-loading="loading" style="width: 1200px; height: 300px; position: absolute; font-size: 16px; color: #666; line-height: 300px; text-align: center; z-index: 100">
                No Data
            </p>
        </div>
    </div>
</template>

<script>
import { plant_search_down, tissue_type_down, species_efp, cell_atlas_gene_symbol_download } from '@/api/api'
export default {
    data() {
        return {
            sample_form: {
                species_name: 'Arabidopsis_thaliana',
                tissue: 'Root',
                gene_id: ''
            },
            speciesOptions: [
                { label: 'Arabidopsis thaliana', value: 'Arabidopsis_thaliana' },
                { label: 'Oryza sativa', value: 'Oryza_sativa' },
                { label: 'Zea mays', value: 'Zea_mays' }
            ],
            tissueOptions: [
                {
                    label: 'Root',
                    value: 'Root'
                },
                {
                    label: 'Leaf',
                    value: 'Leaf'
                }
            ],
            stage_svg: '',
            loading: false,
            GeneOptions: [],
            GeneLoading: false,
            list: []
        }
    },
    mounted() {
        this.svgData()
        this.init()
    },
    methods: {
        init() {
            // plant_search_down({}).then(res => {
            //   if (res.code == 200) {
            //     this.speciesOptions = res.data
            //   }
            // });
            // tissue_type_down({ species_name: this.sample_form.species_name }).then(res => {
            //   if (res.code == 200) {
            //     this.tissueOptions = res.data
            //   }
            // });
        },
        species_nameChange() {
            // tissue_type_down({ species_name: this.sample_form.species_name }).then(res => {
            //   if (res.code == 200) {
            //     this.sample_form.tissue = ''
            //     this.tissueOptions = res.data
            //   }
            // });
        },
        Example() {
            this.sample_form = {
                species_name: 'Arabidopsis_thaliana',
                tissue: 'Root',
                gene_id: 'AT1G01160'
            }
        },
        svgData() {
            let params = {
                species: this.sample_form.species_name,
                tissue: this.sample_form.tissue,
                gene_id: this.sample_form.gene_id
            }
            this.loading = true
            this.stage_svg = ''

            species_efp(params).then((res) => {
                if (res.code == 200) {
                    this.loading = false
                    this.stage_svg = res.data.stage_svg
                    // debugger
                    Object.keys(res.data.stage_plant).forEach((clsItem) => {
                        // 每个中有多少个部位
                        this.$nextTick(function () {
                            // this.$refs.efpPlant.style.height = Number(this.$refs.efpPlant.querySelector('svg').clientHeight) + 'px'
                            this.$refs.efpPlant.querySelectorAll(`.${clsItem}`).forEach((item) => {
                                item.style.fill = res.data.stage_plant[clsItem]
                            })
                        })
                    })
                }
            })
        },
        remoteMethod(query) {
            if (query !== '') {
                this.GeneLoading = true
                cell_atlas_gene_symbol_download({
                    species_name: this.$route.query.name,
                    gene_id: query
                    // gene_id: this.formInline.gene_id
                }).then((res) => {
                    if (res.code == 200) {
                        // this.list = res.data
                        this.GeneOptions = res.data
                        this.GeneLoading = false
                    }
                })
                // this.GeneLoading = true;
                // setTimeout(() => {
                //   this.GeneLoading = false;
                //   this.GeneOptions = this.list.filter(item => {
                //     return item.name.toLowerCase()
                //       .indexOf(query.toLowerCase()) > -1;
                //   });
                // }, 200);
            } else {
                this.GeneOptions = []
            }
        }
    }
}
</script>

<style lang="scss" scoped>
@import './style.scss';
</style>
