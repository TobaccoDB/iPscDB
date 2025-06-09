<template>
  <div class="cellIdentification" :style="{ minHeight: '390px'}">
    <div class="cellIdentification-inner" v-loading="loading">
      <div class="scsa">
        <el-row :gutter="20" style="width:100%;height:auto;overflow:hidden;">
          <el-col :span="6" v-for="(item, index) in listItem" :key="index">
            <div class="grid-content">
              <div class="title" @click="jumpRefrence(item.lit_id, item.project_id)">{{item.label}}</div>
              <div class="pic_content">
                <div class="pic" @click="jumpRefrence(item.lit_id, item.project_id)"><img :src="item.cell_identification_pdf" /></div>
                <el-button size="medium" class="btn" @click="jumpClick" type="primary">SCope</el-button>
                <el-button size="medium" class="btn" type="primary" @click="jumpQc(item.lit_id)">Sample QC</el-button>
                <el-button size="medium" class="btn" type="primary" @click="jumpCellIdent(item)">Cell ident</el-button>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
import { cell_identification_pdf_title } from "@/api/api";
export default {
  name: "cellIdentification",
  components: {

  },
  data() {
    return {
      contentHeight: (window.innerHeight - 100 - 60 - 120) + 'px',
      loading: false,
      screenHeight: document.body.clientHeight,
      timer: false,
      listItem: []
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
    this.init()
  },
  methods: {
    init() {
      cell_identification_pdf_title({}).then(res => {
        if (res.code == 200) {
          this.listItem = res.data
        }
      });
    },
    jumpRefrence(id, project_id) {
      this.$router.push({
        path: '/Refrence',
        query: {
          lit_id: id,
          project_id: project_id
        }
      })
    },
    jumpClick() {
      this.$router.push({
        path: '/cellIdentificationScope',
        query: {
        }
      })
      // window.open(`http://159.138.151.49:55850/#/iPscDB/*/welcome/`, '_blank')
    },
    jumpQc(id) {
      this.$router.push({
        path: '/sampleQC',
        query: {
          lit_id: id,
        }
      })
    },
    jumpCellIdent(item) {
      this.$router.push({
        path: '/cellIdent',
        query: {
          lit_id: item.lit_id,
          species_name: item.value.split('-')[0],
          tissue: item.value.split('-')[1],
        }
      })
    }
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
