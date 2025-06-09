<template>
  <div class="progressResult">
    <el-dialog :visible.sync="visible" :close-on-click-modal="false" custom-class="no-header-dialog" width="500px" center>
      <span style="color: rgb(51, 51, 51);font-family: 思源黑体;font-size: 14px;line-height: 20px;">The task has been submitted to the background for execution. You can wait for the completion of the task here to view
        the result, or click close go to the home page to wait for the result.</span>
      <el-progress style="margin:29px 0 15px 0;font-size: 14px;" define-back-color="#E7EFEA" text-color="#fff" :text-inside="true"
        color="#24A461" :stroke-width="20" :percentage="percentage" status="success"></el-progress>
      <p style="color: rgb(0, 0, 0);font-family: 思源黑体;font-size: 14px;line-height: 20px;text-align:center;">Task is runing
        <i style="color:#000;" class="el-icon-loading"></i>
      </p>
      <span slot="footer" class="dialog-footer">
        <el-button style="color: rgb(36, 164, 97);font-family: 思源黑体;font-size: 14px;line-height: 20px;" type="text" @click="dialogClose">close</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>

export default {
  name: 'progressBar',
  components: {
  },
  props: {
    progressVisible: {
      type: Boolean,
      default() {
        return false
      }
    },
    percentage: {
      type: Number,
      default() {
        return 0
      }
    },
  },
  watch: {
    progressVisible(val1, val2) {
      this.visible = this.progressVisible
    }
  },
  data() {
    return {
      visible: false
    }
  },
  mounted() {

  },
  methods: {
    dialogClose() {
      this.$emit('dialogClose', false)
      this.$router.push({
        path: '/browseResult',
        query: {}
      })
      // if (this.$route.query.from == 'cell_ranger') {
      //   this.$router.push({
      //     path: '/analysisFromCellranger',
      //     query: {}
      //   })
      // } else {
      //   this.$router.push({
      //     path: '/analysisFromSampleQC',
      //     query: {}
      //   })
      // }
    },
  }
}
</script>
<style lang="scss" scoped>
.progressResult {
  width: 1240px;
  height: 100%;
  margin: 0 auto;
}
</style>
<style>
.no-header-dialog .el-dialog__header {
  display: none;
}
.no-header-dialog .el-dialog__footer {
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  padding: 10px;
}
.no-header-dialog {
  border-radius: 8px;
}
</style>
