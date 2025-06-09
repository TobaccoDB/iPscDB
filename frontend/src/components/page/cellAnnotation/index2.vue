<template>
    <div class="cellAnnotation">
        <!-- <div class="crumbs">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/tools' }">Tools</el-breadcrumb-item>
        <el-breadcrumb-item>Cross-species cell annotation</el-breadcrumb-item>
      </el-breadcrumb>
    </div> -->
        <div class="cellAnnotation-inner" style="width: 100%; background: #fff; padding: 30px 0 0 0">
            <el-container>
                <el-container>
                    <el-main>
                        <h3 class="cellAnnotation-inner-title">Input file explain</h3>
                        <p>*Raw counts DGE requirement: Gene (row) * Cell (column);</p>
                        <p>Gene ID: gene symbol only;</p>
                        <p>File size: <=200mb;</p>
                        <p>File format: txt/csv (comma or tab separated);</p>
                        <p>File name: no space or other special character.</p>
                        <p>* Input file format as follows:</p>
                        <ul>
                            <li v-for="(item, index) in itemList" :key="index">{{ item }}</li>
                        </ul>

                        <p>
                            * If you paste your data to Excel, please format the cell as text before pasting data on it. Otherwise, some gene names will be converted to Date and will introduce
                            redundant gene names.
                        </p>
                        <p>* If you use Seurat in R, you can run these scripts to generate input:</p>
                        <div class="bottom_p">
                            <p>rna.data.average = AverageExpression(rna.data)</p>
                            <p># This will generate average expression for each cluster</p>
                            <p>write.table(rna.data.average, "Cell_ident_input.csv", quote = F, col.names = T, row.names = T, sep="\t")</p>
                            <p># Then, you can upload this file to predict cell types</p>
                        </div>
                        <h3>Reference genome information：</h3>
                        <div class="ReferenceTable">
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Species</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">Refrence Genome</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">Download information</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Arabidopsis thaliana                                    </div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">TAIR10</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">https://www.arabidopsis.org/</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference" style="height: 64px;">Bombax ceiba
                                    </div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference" style="height: 64px;">Bombax ceiba L.
                                    </div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference" style="height: 64px">https://academic.oup.com/gigascience/article/7/5/giy051/4994837
                                    </div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference" style="height: 64px;">Brassica rapa
                                    </div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference" style="height: 64px;">A03 v1
                                    </div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference" style="height: 64px">http://www.bioinformaticslab.cn/EMSmutation/home
                                    </div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference" style="height: 64px">Catharanthus roseus</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference" style="height: 64px">C. roseus genome v3.0</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference" style="height: 64px">https://www.ncbi.nlm.nih.gov/nuccore/NC_021423.1</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference" style="height: 64px;">Fragaria vesca</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference" style="height: 64px;">F. vesca v4.0.a1</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference" style="height: 64px">https://www.rosaceae.org/</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference" style="height: 64px;">Glycine max</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference" style="height: 64px;">Wm82 ISU-01 v2.1</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference"  style="height: 64px">https://phytozome-next.jgi.doe.gov/info/GmaxWm82ISU_01_v2_1</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference" style="height: 64px;">Gossypium bickii</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference" style="height: 64px;">FGossypium bickii (G1) genome JZU_v1</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference"  style="height: 64px">https://www.cottongen.org/Analysis/8018111</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Gossypium hirsutum</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">Gossypium hirsutum (AD1) TM-1</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">https://www.cottongen.org/species/Gossypium_hirsutum/bgi-AD1_genome_v1.0</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Manihot esculenta</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">Manihot esculenta v8.1</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">https://phytozome-next.jgi.doe.gov/info/Mesculenta_v8_1</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Marchantia polymorpha</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">Marchantia Tak-1 V5.1</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">https://marchantia.info/</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Medicago truncatula</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">MtrunA17r5.0</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">https://medicago.toulouse.inra.fr/MtrunA17r5.0-ANR/</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Nicotiana attenuata</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">NIATTr2</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">https://www.ncbi.nlm.nih.gov/assembly/GCF_001879085.1/</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Nicotiana tabacum</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">NtaSR1v1.0</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">http://lifenglab.hzau.edu.cn/Nicomics/Download/NtaSR1/</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Oryza sativa</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">IRGSP-1.0</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">https://rapdb.dna.affrc.go.jp/</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Phalaenopsis big chili</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">Orchidstra 2.0</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">http://orchidstra2.abrc.sinica.edu.tw</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Phyllostachys edulis</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">Moso genome</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">https://gigadb.org/dataset/100498</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Populus alba var. pyramidalis</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">P. alba var. pyramidalis reference genome</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">https://doi.org/10.1038/s41438-021-00494-2</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Populus alba × glandulosa</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">P. alba×glandulosa reference genome</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">https://onlinelibrary.wiley.com/doi/10.1111/jipb.13159</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Populus tremula × alba</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">Populus tremula × alba refrence genome</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">https://doi.org/10.1242/dev.200632</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Populus trichocarpa</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">Populus trichocarpa refrence genome</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">https://genomebiology.biomedcentral.com/articles/10.1186/s13059-022-02845-1</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Solanum lycopersicum</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">ITAG4.0</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">ftp://ftp.solgenomics.net/tomato_genome/annotation/ITAG4.0_release</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Triticum aestivum</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">IWGSC RefSeq v1.0</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">https://www.wheatgenome.org/projects/reference-genome-project/refseq-v1.0</div>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="6">
                                    <div class="grid-Reference">Zea mays</div>
                                </el-col>
                                <el-col :span="8">
                                    <div class="grid-Reference">B73 V4</div>
                                </el-col>
                                <el-col :span="10">
                                    <div class="grid-Reference">https://plants.ensembl.org/index.html</div>
                                </el-col>
                            </el-row>
                        </div>
                    </el-main>
                </el-container>
            </el-container>
        </div>
    </div>
</template>

<script>
import axios from '@/api/http.js'
import Axios from 'axios'
import { cell_identification_reference_detail, cell_identification_csv_zip_download, cross_reference_specie_down, cross_reference_species_down } from '@/api/api'
export default {
    name: 'cellAnnotation',
    components: {},
    data() {
        return {
            contentHeight: window.innerHeight - 330 + 'px',
            goLoading: false,
            cellAnnotation_form: {
                species_name: 'Oryza_sativa',
                reference: 'Arabidopsis_thaliana',
                tissue: 'Root',
                num_top: 2,
                fileName: '',
                file: ''
            },
            speciesOptions: [
                { label: 'Arabidopsis thaliana', value: 'Arabidopsis_thaliana' },
                { label: 'Oryza sativa', value: 'Oryza_sativa' },
                { label: 'Zea mays', value: 'Zea_mays' }
            ],
            referenceOptions: [],
            tissueOptions: [
                // { label: "Root", value: "Root" },
                // { label: "Leaf", value: "Leaf" }
            ],
            file_name: '',
            fileLoading: false,
            itemList: ['', 'Cell01', 'Cell02', 'Cell03', 'Gene1', '1.33', '0', '0', 'Gene2', '0', '0.75', '0', 'Gene3', '0', '1', '0.43', 'Gene4', '0', '0', '3.17']
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        init() {
            // let params = {
            //   lit_id: this.$route.query.lit_id
            // }
            // this.goLoading = true
            // cell_identification_reference_detail(params).then(res => {
            //   if (res.code == 200) {
            //     this.detailData = res.data.results[0]
            //     this.goLoading = false
            //   }
            // });
            cross_reference_specie_down({ species_name: this.cellAnnotation_form.species_name }).then((res) => {
                if (res.code == 200) {
                    this.referenceOptions = res.data
                }
            })
            cross_reference_species_down({ reference_name: this.cellAnnotation_form.reference }).then((res) => {
                if (res.code == 200) {
                    this.tissueOptions = res.data
                }
            })
        },
        species_nameChange() {
            cross_reference_specie_down({ species_name: this.cellAnnotation_form.species_name }).then((res) => {
                if (res.code == 200) {
                    this.cellAnnotation_form.reference = ''
                    this.referenceOptions = res.data
                    this.cellAnnotation_form.tissue = ''
                    this.tissueOptions = []
                }
            })
        },
        referenceChange() {
            cross_reference_species_down({ reference_name: this.cellAnnotation_form.reference }).then((res) => {
                if (res.code == 200) {
                    this.cellAnnotation_form.tissue = ''
                    this.tissueOptions = res.data
                }
            })
        },
        download() {
            cell_identification_csv_zip_download({
                file_name: '',
                file_type: 'example'
            }).then((res) => {
                if (res.code == 200) {
                    window.open(res.data.cell_identification_csv_zip, '_blank')
                }
            })
        },
        search() {
            if (this.cellAnnotation_form.fileName == '') {
                this.$message.warning('Please upload a file！')
                return
            } else if (this.cellAnnotation_form.reference == '') {
                this.$message.warning('Please Choose Reference！')
                return
            } else if (this.cellAnnotation_form.tissue == '') {
                this.$message.warning('Please Choose tissue')
                return
            }
            this.$router.push({
                path: '/cellAnnotationResult',
                query: {
                    file_name: this.cellAnnotation_form.fileName,
                    reference_name: this.cellAnnotation_form.reference,
                    tissue: this.cellAnnotation_form.tissue,
                    num_top: this.cellAnnotation_form.num_top
                }
            })
        },
        reset() {
            this.file_name = ''
            this.cellAnnotation_form = {
                species_name: 'Oryza_sativa',
                reference: 'Arabidopsis_thaliana',
                tissue: 'Root',
                num_top: 2,
                fileName: '',
                file: ''
            }
            this.$refs.file.value = ''
        },
        handleUpdate(event) {
            // if (event.target.files[0].name.split('.')[event.target.files[0].name.split('.').length - 1] != 'csv') {
            //   this.$message.warning('Please upload .csv file！');
            // } else {
            if (this.cellAnnotation_form.reference == '') {
                this.$message.warning('Please Choose Reference！')
                return
            }
            this.cellAnnotation_form.fileName = event.target.files[0].name
            this.fileLoading = true

            let formData = new FormData()
            formData.append('myfile', event.target.files[0])
            formData.append('reference_name', this.cellAnnotation_form.reference)
            formData.append('species_name', this.cellAnnotation_form.species_name)
            let config = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
            const $axios = Axios.create({
                baseURL: axios.defaults.baseURL,
                timeout: 1000000
            })

            $axios
                .post('/api/v1/cross_species_annotation_upload/', formData, config)
                .then((res) => {
                    if (res.data.code == 200) {
                        this.cellAnnotation_form.file = event.target.files[0]
                        this.file_name = res.data.data.file_name
                        this.$message.success(res.data.data.msg)
                    } else {
                        this.$message.warning(res.data.msg)
                    }
                    this.fileLoading = false
                })
                .catch((err) => {
                    this.$message.warning(err.data.msg)
                })
            // }
        }
    }
}
</script>
<style lang="scss" scoped>
@import './style.scss';
</style>
