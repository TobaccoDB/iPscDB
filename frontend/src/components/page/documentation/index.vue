<template>
    <div class="documentation">
        <div class="documentationLeft">
            <div class="documentationLeftItem" :class="{ active: active === '#overview' }" @click="goPage('#overview')">Overview</div>
            <div class="documentationLeftItem" :class="{ active: active === '#datasets' }" @click="goPage('#datasets')">Datasets and usage</div>
            <div class="documentationLeftItem" :class="{ active: active === '#contact' }" @click="goPage('#contact')">Contact us</div>
            <div class="documentationLeftItem" :class="{ active: active === '#submit' }" @click="goPage('#submit')">Submit data</div>
        </div>
        <div class="documentationRight">
            <!-- <router-view></router-view> -->
             <div  class="documentationRightMain">
                <Index1></Index1>
                <Index2></Index2>
                <Index3></Index3>
                <Index4></Index4>
             </div>
        </div>
    </div>
</template>

<script>
import Index1 from './index1'
import Index2 from './index2'
import Index3 from './index3'
import Index4 from './index4'
export default {
    name: 'documentation',
    data() {
        return {
            active: '#overview'
        }
    },
    methods: {
        goPage(name) {
            this.active = name
            // this.$router.push({
            //     path: name
            // })

            const target = document.querySelector(name);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
        }
    },
    components: {
        Index1,
        Index2,
        Index3,
        Index4
    }
}
</script>
<!-- D:\gaige\yancao\src\assets\img -->
<style lang="scss" scoped>
.documentation {
    width: 1240px;
    height: 100%;
    margin: 0 auto;
    // background: #fff;
    padding: 30px;
    box-sizing: border-box;
    position: relative;
    display: flex;
    justify-content: space-between;
    .documentationLeft {
        width: 300px;
        // height: 100%;
        // position: absolute;
        // left: -320px;
        // top: 0;
        height: 500px;
        background: #fff;
        padding-top: 20px;

        .documentationLeftItem {
            font-size: 16px;
            font-weight: 500;
            color: #333333;
            line-height: 22px;
            cursor: pointer;
            padding: 10px 20px;
            box-sizing: border-box;
            &:hover {
                color: #24a461;
                // background: #cccccc;
            }
        }
        .active {
            color: #24a461;
            background: #cccccc;
        }
    }
    .documentationRight {
        width: calc(100% - 320px);
        height: calc(100vh - 460px);
        box-sizing: border-box;
        overflow-y: auto;
    }
}
</style>
