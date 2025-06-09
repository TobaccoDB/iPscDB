<!--
作者: nodebook@qq.com
组件名称: 
-->
<template>
    <div class="downLoadFile">
        <div class="downLoadFileMain">
            <h2>Integration Result</h2>
            <h3>The script execution takes a long time. You can download the data and run it on your PC</h3>
            <h3>How to use?</h3>
            <p>1. Click the Download button</p>
            <p>2. Unzip data.zip</p>
            <p>3. Open terminal in the folder</p>
            <p>4. Run command: Rscript Harmony,R -a SAMC200945.rds -b SAMC200944.rds -c SAMC200943.rds -d SAMC200942.rds</p>
            <el-button type="primary" style="width: 120px" :loading="searchIng" @click="download">Download results</el-button>
        </div>
        <!-- <el-button type="primary" style="width: 120px" :loading="searchIng" @click="download">点击下载文件</el-button> -->
    </div>
</template>

<script>
import { integration_zip_download } from '@/api/api'
export default {
    data() {
        return {
            searchIng: false
        }
    },
    methods: {
        download() {
            this.searchIng = true
            integration_zip_download({
                integration_type: this.$route.query.integration_type,
                sample_id: this.$route.query.sample_id
            })
                .then((res) => {
                    if (res.code == 200) {
                        console.log(res.data.integration_zip)
                        window.open(res.data.integration_zip)
                        // const a = document.createElement('a')
                        // a.href = res.data.integration_zip
                        // a.target = '_blank'
                        // a.style.display = 'none'
                        // document.body.appendChild(a)
                        // a.click()
                        // document.body.removeChild(a)
                    }
                    this.searchIng = false
                })
                .catch((err) => {
                    this.searchIng = false
                })
        }
    }
}
</script>

<style scoped lang="scss">
.downLoadFile {
    width: 100%;
    height: 100%;
    /* background: #fff; */
    min-height: 500px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.downLoadFileMain {
    width: 1240px;
    height: 700px;
    margin: 0 auto;
    background: #fff;
    padding: 25px;
    box-sizing: border-box;
    h2 {
        font-size: 36px;
        margin-bottom: 20px;
    }
    h3 {
        font-size: 24px;
        margin-bottom: 20px;
    }
    p {
        font-size: 20px;
        color: #333333;
        margin-bottom: 15px;
    }
}
</style>
