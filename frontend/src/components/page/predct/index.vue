<template>
    <div class="cellAnnotation">
        <div class="cellAnnotationMain">
            <el-header>scPlantDB </el-header>
            <div class="cellAnnotationMainContent">
                <div class="cellAnnotationMainContentLeft">
                    <div class="cellAnnotationMainContentLeftHeader">
                        <span>Gene list</span>
                        <el-button type="info">Clear</el-button>
                    </div>
                    <el-input type="textarea" :rows="15" placeholder="Input Genes...One gene per line" v-model="textarea" style="margin-bottom: 10px"> </el-input>
                    <el-upload class="predctUpload-demo" drag action="https://jsonplaceholder.typicode.com/posts/" multiple>
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">Drag file here,or<em>click to upload</em></div>
                    </el-upload>
                    <div class="cellAnnotationMainContentLeftText">Can only upload txt format</div>
                    <div class="cellAnnotationMainContentLeftFooter">
                        <el-button type="success" plain>Run</el-button>
                        <el-button type="primary" plain>Example</el-button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            textarea: ''
        }
    }
}
</script>

<style scoped lang="scss">
.cellAnnotation {
    width: 100%;
    height: 100%;
    min-height: 700px;
    background: #fff;
    .cellAnnotationMain {
        width: 1240px;
        height: auto;
        margin: 0 auto;
        padding: 20px 0;
        .el-header {
            padding: 0;
            height: 40px !important;
            font-size: 18px;
            font-family: PingFang SC, PingFang SC-Bold;
            font-weight: 700;
            color: #333333;
            line-height: 40px;
        }
        .cellAnnotationMainContent {
            width: 100%;
            height: auto;
            .cellAnnotationMainContentLeft {
                width: 260px;
                height: auto;
                span {
                    font-size: 16px;
                    color: rgb(33, 37, 41);
                }
                .cellAnnotationMainContentLeftHeader {
                    width: 100%;
                    height: 50px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                .predctUpload-demo {
                    margin-bottom: 10px;
                    width: 260px;
                }
                .cellAnnotationMainContentLeftText {
                    width: 100%;
                    height: 20px;
                    line-height: 20px;
                    font-size: 12px;
                    color: rgb(96, 98, 102);
                    margin-bottom: 10px;
                }
                .cellAnnotationMainContentLeftFooter {
                    width: 100%;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
            }
        }
    }
}
</style>

<style>
.predctUpload-demo .el-upload-dragger {
    width: 260px;
}
.predctUpload-demo .el-upload--text {
    width: 260px;
    border: none;
}
</style>
