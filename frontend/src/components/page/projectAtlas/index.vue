<template>
    <div class="projectAtlas" :style="{ minHeight: '390px' }">
        <div class="projectAtlas-inner" style="margin-bottom: 20px">
            <div class="projectAtlas-inner-name">Species Atlas</div>
            <div class="scsa" v-loading="loading" style="min-height: 300px">
                <el-row :gutter="20" style="width: 100%; height: auto; overflow: hidden">
                    <el-col :span="6" v-for="(item, index) in listItem" :key="index">
                        <div class="grid-content">
                            <div class="grid-content-top">
                                <div class="grid-content-top-left">
                                    <img :src="item.species_whole_plant" />
                                </div>
                                <div class="grid-content-top-right">
                                    <div class="title">
                                        <span class="titleOverflow2" :title="item.label">
                                            {{ item.label }}
                                           
                                        </span>
                                    </div>
                                    <!-- <div class="content">
                                        <span>Project:</span>
                                        <span style="color: #24A461; cursor: pointer" @click="jumpPMIDDIO(item.dio_link)">{{ item.label }} </span>
                                    </div>
                                    <div class="contentFooter">
                                        <span>Cell:</span><span>{{ item.cell_count }}</span>
                                    </div> -->
                                    <div class="contentBox">
                                        <div class="contentBoxLeft">
                                            <p>DataSet</p>
                                            <p style="color: #24a461">{{ item.dataset }}</p>
                                        </div>
                                        <div class="contentBoxLeft">
                                            <p>Cell</p>
                                            <p>{{ item.cell }}</p>
                                        </div>
                                    </div>
                                </div>
                                <!-- <div class="title"><img :src="item.tissue_head_link" />{{ item.title }}</div> -->
                                <!-- <ul class="ul-content">
                                    <li>
                                        <span>Project:</span>
                                        <span style="color: #24A461; cursor: pointer" @click="jumpPMIDDIO(item.dio_link)">{{ item.label }} </span>
                                    </li>
                                    <li><span>Cell:</span>{{ item.cell_count }}</li>
                                </ul> -->
                            </div>
                            <div class="btn-content">
                                <p>
                                    <el-button size="medium" class="btn" type="text" @click="jumpProjectResult(item)">Explore</el-button>
                                </p>
                                <p>
                                    <el-button size="medium" class="btn" type="text" @click="Download(item.download_rds_link)">Download</el-button>
                                </p>
                            </div>
                        </div>
                    </el-col>
                </el-row>
            </div>
        </div>
        <div class="projectAtlas-inner">
            <div class="projectAtlas-inner-name">Tissue Atlas</div>
            <div class="scsa" v-loading="loading" style="min-height: 300px">
                <el-row :gutter="20" style="width: 100%; height: auto; overflow: hidden">
                    <el-col :span="6" v-for="(item, index) in listItem1" :key="index">
                        <div class="grid-content">
                            <div class="grid-content-top">
                                <!-- <div class="grid-content-top-left">
                                    <img :src="item.tissue_head_link" />
                                </div> -->
                                <div class="grid-content-top-right" style="width: 100%">
                                    <div class="title">
                                        <img :src="item.tissue_head_link" />
                                        <span class="titleOverflow" :title="item.label">
                                            {{ item.label }}
                                           
                                        </span>
                                        <span class="titleOverflowDetial">{{ item.tissue_label }}</span>
                                    </div>
                                    <!-- <div class="content">
                                        <span>Project:</span>
                                        <span style="color: #24A461; cursor: pointer" @click="jumpPMIDDIO(item.dio_link)">{{ item.label }} </span>
                                    </div>
                                    <div class="contentFooter">
                                        <span>Cell:</span><span>{{ item.cell_count }}</span>
                                    </div> -->
                                    <div class="contentBox">
                                        <div class="contentBoxLeft" style="width: 50%">
                                            <p>Cell Type</p>
                                            <p>{{ item.cell_type }}</p>
                                            <!-- @click="jumpPMIDDIO(item.dio_link)" -->
                                        </div>
                                        <div class="contentBoxLeft">
                                            <p>Cell</p>
                                            <p>{{ item.cell }}</p>
                                        </div>
                                    </div>
                                </div>
                                <!-- <div class="title"><img :src="item.tissue_head_link" />{{ item.title }}</div> -->
                                <!-- <ul class="ul-content">
                                    <li>
                                        <span>Project:</span>
                                        <span style="color: #24A461; cursor: pointer" @click="jumpPMIDDIO(item.dio_link)">{{ item.label }} </span>
                                    </li>
                                    <li><span>Cell:</span>{{ item.cell_count }}</li>
                                </ul> -->
                            </div>
                            <div class="btn-content">
                                <p>
                                    <el-button size="medium" class="btn" type="text" @click="jumpProjectResult(item)">Explore</el-button>
                                </p>
                                <p>
                                    <el-button size="medium" class="btn" type="text" @click="Download(item.download_rds_link)">Download</el-button>
                                </p>
                            </div>
                        </div>
                    </el-col>
                </el-row>
            </div>
        </div>
    </div>
</template>

<script>
import { cell_identification_pdf_title, project_lit_down } from '@/api/api'
export default {
    name: 'projectAtlas',
    components: {},
    data() {
        return {
            contentHeight: window.innerHeight - 100 - 60 - 120 + 'px',
            loading: false,
            screenHeight: document.body.clientHeight,
            timer: false,
            listItem: [],
            listItem1: []
        }
    },
    watch: {
        screenHeight(val) {
            // 为了避免频繁触发resize函数导致页面卡顿，使用定时器
            if (!this.timer) {
                // 一旦监听到的screenHeight值改变，就将其重新赋给data里的screenHeight
                this.contentHeight = val - 100 - 60 - 120 + 'px'
                this.timer = true
                let that = this
                setTimeout(function () {
                    that.timer = false
                }, 400)
            }
        }
    },
    mounted() {
        const that = this
        let firstFire = null
        window.addEventListener('resize', () => {
            if (firstFire === null) {
                firstFire = setTimeout(function () {
                    firstFire = null
                    return (() => {
                        window.screenHeight = window.innerHeight
                        that.screenHeight = window.screenHeight
                    })()
                }, 100)
            }
        })

        this.init()
    },
    methods: {
        init() {
            this.loading = true
            project_lit_down()
                .then((res) => {
                    if (res.code == 200) {
                        if (res.data) {
                            this.listItem = res.data.species_data
                            this.listItem1 = res.data.tissue_data
                            // res.data.species_data.forEach((item) => {
                            //     item.project.forEach((element) => {
                            //         element.title = item.label
                            //         element.species_name = item.species_name
                            //         this.listItem.push(element)
                            //     })
                            // })
                        }
                    }
                    this.loading = false
                })
                .catch(() => {
                    this.loading = false
                })
            // cell_identification_pdf_title({}).then(res => {
            //   if (res.code == 200) {
            //     this.listItem = res.data
            //   }
            // });
        },
        jumpProjectResult(item) {
            // this.$router.push({
            //     path: '/projectResult',
            //     query: {
            //         lit_id: item.value,
            //         species_name: item.species_name,
            //         tissue: item.tissue,
            //         project_id: item.label,
            //         sample_count: item.sample_count,
            //         cell_count: item.cell_count
            //     }
            // })
            this.$router.push({
                path: '/searchResult',
                query: {
                    Tissue: item.Tissue,
                    tissue_label: item.tissue_label,
                    name: item.name,
                    nameLabel: item.label
                }
            })
        },
        Download(url) {
            window.open(url, '_blank')
            // let fileName = url.substr(url.lastIndexOf('/') + 1, url.length)
            // console.log(fileName)
            // console.log(url)
            // const a = document.createElement('a')
            // a.href = url
            // a.download = fileName
            // a.target = '_blank'
            // a.style.display = 'none'
            // document.body.appendChild(a)
            // a.click()
            // document.body.removeChild(a)
        },
        jumpPMIDDIO(id) {
            window.open(`${id}`, '_blank')
        }
    }
}
</script>
<style lang="scss" scoped>
@import './style.scss';
</style>
