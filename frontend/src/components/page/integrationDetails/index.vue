<template>
    <div class="integrationDetails">
        <div class="crumbs">
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <!-- <el-breadcrumb-item :to="{ path: '/Integration' }">Integration</el-breadcrumb-item> -->
                <el-breadcrumb-item :to="{ path: '/browse' }">Browse</el-breadcrumb-item>
                <el-breadcrumb-item>Detail</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="integrationDetails-inner" :style="{ minHeight: contentHeight }" v-loading="goLoading" element-loading-text="loading" element-loading-background="#fff">
            <p class="topTitle">
                Integratied by Harmony
                <el-button type="text" @click="downloadImg('jpg')" style="float: right; color: #0a9daa; margin-left: 10px"> <i class="el-icon-download"></i> jpg</el-button>
                <el-button type="text" @click="downloadImg('png')" style="float: right; color: #0a9daa; margin-left: 10px"> <i class="el-icon-download"></i> png</el-button>
                <el-button type="text" @click="downloadImg('svg')" style="float: right; color: #0a9daa; margin-left: 10px"> <i class="el-icon-download"></i> svg</el-button>
            </p>
            <el-row :gutter="20" v-if="$route.query.sample_id">
                <el-col :span="12">
                    <div class="grid-content" style="padding-left: 145px">Samples</div>
                </el-col>
                <el-col :span="12">
                    <div class="grid-content" style="padding-left: 55px">Clusters</div>
                </el-col>
            </el-row>
            <div class="UMAP" ref="imageTofile">
                <img :src="url" width="100%" height="560px" />
                <!-- <div class="detailUrl"></div> -->
                <!-- <p class="secondTitle">Integration Result</p>
        <p class="thirdTitle">The script execution takes a long time. You can download the data and run it on your PC</p>
        <p class="thirdTitle">How to use?</p>
        <ul>
          <li>1. Click the Download button</li>
          <li>2. Unzip data.zip</li>
          <li>3. Open terminal in the folder</li>
          <li>4. Run command: Rscript {{backText}}</li>
        </ul> -->
                <el-button v-if="this.$route.query.sample_id" type="primary" @click="download" :loading="downloadLoading"> <i class="el-icon-download"></i> Download results</el-button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from '@/api/http.js'
import Axios from 'axios'
import html2canvas from 'html2canvas'
//顶部页面加载条
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
NProgress.configure({
    easing: 'ease',
    speed: 500,
    showSpinner: false,
    trickleSpeed: 200,
    minimum: 0.3
})
import { integration_svg_show, integration_example_svg_show, integration_download, integration_example_show } from '@/api/api'
export default {
    name: 'integrationDetails',
    components: {},
    data() {
        return {
            contentHeight: window.innerHeight - 330 + 'px',
            goLoading: false,
            downloadLoading: false,
            url: '',
            integration_zip: '',
            integration_download_png: '',
            integration_download_svg: '',
            integration_download_jpg: '',
            backText: 'Seurat.R -a ERR6908267.rds -b GSM4809928.rds'
        }
    },
    mounted() {
        // this.init()
        // let typeArr = ['-a', '-b', '-c', '-d', '-e']
        // let str = ''
        // this.$route.query.sample_id.split(',').forEach((item, index) => {
        //   str = str + ` ${typeArr[index]} ${item}.rds`
        // });
        // this.backText = `${this.$route.query.integration_type}.R ${str}`
        if (this.$route.query.sample_id) {
            this.init()
        } else {
            this.example()
        }
    },
    methods: {
        example() {
            let params = {
                integration_type: this.$route.query.integration_type
            }
            this.goLoading = true
            integration_example_show(params).then((res) => {
                if (res.code == 200) {
                    this.url = res.data.integration_example_svg
                    this.integration_download_svg = res.data.integration_download_svg
                    this.integration_download_png = res.data.integration_download_png
                    this.integration_download_jpg = res.data.integration_download_jpg
                    this.goLoading = false
                }
            })
        },
        init() {
            NProgress.start()
            let params = {
                integration_type: this.$route.query.integration_type,
                sample_id: this.$route.query.sample_id
            }
            this.goLoading = true
            // integration_example_svg_show(params).then(res => {
            //   if (res.code == 200) {
            //     this.url = res.data.integration_svg
            //     this.goLoading = false
            //   }
            // });
            integration_svg_show(params).then((res) => {
                if (res.code == 200) {
                    // this.integration_zip = res.data.integration_zip
                    this.url = res.data.integration_svg
                    this.integration_download_svg = res.data.integration_download_svg
                    this.integration_download_png = res.data.integration_download_png
                    this.integration_download_jpg = res.data.integration_download_jpg
                    this.goLoading = false
                    NProgress.done()
                }
            })
        },
        download() {
            let params = {
                integration_type: this.$route.query.integration_type,
                sample_id: this.$route.query.sample_id
            }
            this.downloadLoading = true
            integration_download(params).then((res) => {
                if (res.code == 200) {
                    this.downloadLoading = false
                    window.open(res.data.integration_cell_cluster, '_blank')
                    window.location.href = res.data.integration_umap_location
                }
            })
        },
        downloadImg(name) {
            let imgUrl = ''
            if (name == 'svg') {
                imgUrl = this.integration_download_svg
            } else if (name == 'png') {
                imgUrl = this.integration_download_png
            } else {
                imgUrl = this.integration_download_jpg
            }
            const link = document.createElement('a') //自己创建的a标签
            link.href = imgUrl
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
            window.URL.revokeObjectURL(imgUrl)
        }
    }
}
</script>
<style lang="scss" scoped>
@import './style.scss';
</style>
