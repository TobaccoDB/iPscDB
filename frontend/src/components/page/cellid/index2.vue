<template>
    <div class="cellid">
        <div class="cellidMainTitleInfo">
            <div class="cellidMainTitleInfoMain">
                <span style="font-weight: bold">
                    <span style="color: #e6ef82">P</span>lant <span style="color: #e6ef82">C</span>ell <span style="color: #e6ef82">i</span>Dentification(<span style="color: #e6ef82">P</span>lant
                    <span style="color: #e6ef82">C</span>ell<span style="color: #e6ef82">i</span>D)
                </span>
                is an atlas guided automatic cell type identification method which utilize massive public single-cell annotation to predict the cell type quickly and accurately.
            </div>
        </div>

        <div class="cellidMain">
            <!-- <div class="cellidTitle">
                <el-button :type="$route.path.includes('cellid') ? 'primary' : ''" size="small" @click="$router.push('/cellid')">Single specie</el-button>
                <el-button :type="$route.path.includes('cellAnnotation') ? 'primary' : ''" size="small" @click="$router.push('/cellAnnotation')">Cross species</el-button>
            </div> -->
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
export default {
    name: 'index2'
}
</script>

<style scoped lang="scss">
.cellid {
    width: 100%;
    height: 100%;
    // background: #fff;
    .cellidMain {
        width: 1200px;
        min-height: 70px;
        margin: 0 auto;
        padding-bottom: 20px;
        // border-bottom: 1px solid #f0f0f0;
        .cellidTitle {
            width: 1200px;
            height: 47px;
            // background: yellowgreen;
            padding-top: 15px;
            margin-bottom: 10px;
            box-sizing: border-box;
        }
    }
    .cellidMainTitleInfo {
        width: 100%;
        height: auto;
        margin-bottom: 10px;
        // background: #24a461;
        .cellidMainTitleInfoMain {
            width: 1240px;
            height: 100%;
            background: #24a461;
            margin: 0 auto;
            padding: 20px;
            box-sizing: border-box;
            color: #fff;
            font-size: 16px;
            line-height: 30px;
            border-radius: 5px;
        }
    }
}
</style>
