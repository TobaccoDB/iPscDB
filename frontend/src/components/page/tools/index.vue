<template>
  <div class="atlas" :style="{ minHeight: '390px'}">
    <div class="atlas-inner">
      <div class="scsa" v-loading="loading">
        <el-row :gutter="20" style="width:100%;height:auto;overflow:hidden;">
          <el-col :span="8" v-for="(item, index) in listItem" :key="index">
            <div class="grid-content" @click="jumpList(item.routeUrl)">
              <div class="title">{{item.title}}</div>
              <img style="width:100%;height:341px;" :src=item.url alt="">
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
// import { project_lit_down } from "@/api/api";
export default {
  name: "atlas",
  components: {

  },
  data() {
    return {
      contentHeight: (window.innerHeight - 100 - 60 - 120) + 'px',
      loading: false,
      screenHeight: document.body.clientHeight,
      timer: false,
      listItem: [
        { title: 'Cross-species gene expression', url: require("@/assets/img/tools_01.jpg"), routeUrl: 'geneExpression' },
        { title: 'Cross-species cell annotation', url: require("@/assets/img/tools_05.jpg"), routeUrl: 'cellAnnotation' },
        { title: 'Cell-Cell interactions', url: require("@/assets/img/tools_06.jpg"), routeUrl: 'cellCellInteractions' },
        { title: 'Developmental trajectory', url: require("@/assets/img/tools_04.jpg"), routeUrl: 'monocle' },
        { title: 'eSCP', url: require("@/assets/img/tools_03.jpg"), routeUrl: 'eSCP' },
        { title: 'Tissue structure', url: require("@/assets/img/tools_02.jpg"), routeUrl: 'tissueStructure' },
      ]
    };
  },
  watch: {
    screenHeight(val) {
      // 为了避免频繁触发resize函数导致页面卡顿，使用定时器
      if (!this.timer) {
        // 一旦监听到的screenHeight值改变，就将其重新赋给data里的screenHeight
        this.contentHeight = (val - 100 - 60 - 120) + 'px'
        this.timer = true
        let that = this
        setTimeout(function () {
          that.timer = false
        }, 400)
      }
    },
  },
  mounted() {
    const that = this
    let firstFire = null;
    window.addEventListener('resize', () => {
      if (firstFire === null) {
        firstFire = setTimeout(function () {
          firstFire = null;
          return (() => {
            window.screenHeight = window.innerHeight
            that.screenHeight = window.screenHeight
          })()
        }, 100);
      }
    })
  },
  methods: {
    jumpList(item) { // 跳转列表页
      this.$router.push({
        path: `/${item}`,
      })

    }
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
