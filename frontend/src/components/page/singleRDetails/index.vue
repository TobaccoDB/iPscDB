<template>
    <div class="singleRDetails">
        <div class="crumbs">
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-breadcrumb-item :to="{ path: '/singleR' }">Single R</el-breadcrumb-item>
                <el-breadcrumb-item>Single R Results</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="singleRDetails-inner">
            <p class="title1">Single R Results</p>
            <div class="UMAP">
                <i class="el-icon-download pointer" style="padding: 20px 5px; color: #24a461; float: right; cursor: pointer" @click="download">{{ single_name }}</i>
                <p class="title" style="margin-top: 26px">The label score distribution for each cell for your input data:</p>
                <img :src="single_svg1" width="100%" />
                <p class="title">The box plot for each label score is shown as following:</p>
                <img :src="single_svg2" width="100%" />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'singleRDetails',
    components: {},
    data() {
        return {
            single_svg1: '',
            single_svg2: '',
            single_name: '',
            text: ''
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        init() {
            this.single_svg1 = JSON.parse(sessionStorage.getItem('singleR')).single_svg1
            this.single_svg2 = JSON.parse(sessionStorage.getItem('singleR')).single_svg2
            this.text = JSON.parse(sessionStorage.getItem('singleR')).single_txt
            this.single_name = JSON.parse(sessionStorage.getItem('singleR')).single_name
        },
        download() {
            this.jg_downloadFile('api/v1/cell_single_file/single_r_download', { name: this.text })
        }
    }
}
</script>
<style lang="scss" scoped>
@import './style.scss';
</style>
