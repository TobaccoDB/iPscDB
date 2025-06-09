<template>
  <div>
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="Basic Settings" name="first">
        <el-form :model="ruleForm" ref="ruleForm" label-width="110px" class="demo-ruleForm">
          <el-form-item label='Title Name'>
            <el-input v-model="ruleForm.titleName"></el-input>
          </el-form-item>
          <el-form-item label='Title Display'>
            <el-switch v-model="ruleForm.titleShow"></el-switch>
          </el-form-item>
          <el-form-item label='X-axis display'>
            <el-switch v-model="ruleForm.Xshow"></el-switch>
          </el-form-item>
          <el-form-item label='Y-axis display'>
            <el-switch v-model="ruleForm.Yshow"></el-switch>
          </el-form-item>
          <el-form-item label='Axis color'>
            <el-color-picker v-model="ruleForm.axisColor"></el-color-picker>
          </el-form-item>
          <el-form-item label='Tick marks'>
            <el-switch v-model="ruleForm.showticklabels"></el-switch>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="Graphic Settings" name="second">
        <el-form :model="ruleForm" ref="ruleForm" label-width="110px" class="demo-ruleForm">
          <!-- <el-form-item label='悬浮显示'>
            <el-switch v-model="ruleForm.hovermode"></el-switch>
          </el-form-item> -->
          <el-form-item label='Scatter color'>
            <el-color-picker v-model="ruleForm.plotColor"></el-color-picker>
          </el-form-item>
          <el-form-item label='Violin color'>
            <el-color-picker v-model="ruleForm.violinColor"></el-color-picker>
          </el-form-item>
          <el-form-item label='Scatter size'>
            <el-input-number v-model="ruleForm.plotSize" :min="1" :max="10"></el-input-number>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
    <div slot="footer" class="dialog-footer" style="text-align:right;">
      <el-button @click="ruleForm.isShowTitle = false">cancel</el-button>
      <el-button type="primary" @click="submitForm">sure</el-button>
    </div>
  </div>
</template>

<script>

export default {
  name: 'chartSet',
  components: {
  },
  props: {
    chartForm: {
      type: Object
    }
  },
  data() {
    return {
      activeName: 'first',
      ruleForm: {
        titleName: "nFeature_RNA",  // 标题名称
        isShowTitle: false, // 
        titleShow: true, //标题显示
        Xshow: true, //  x轴显示
        Yshow: true, //  y轴显示
        hovermode: true, // 悬浮显示
        axisColor: '#333', // 坐标轴颜色
        plotColor: '#333', //  散点颜色
        violinColor: '#F8766D', //  小提琴颜色
        plotSize: 2, //  散点大小
        showticklabels: true //  刻度显示
      },
    }
  },
  mounted() {
    this.ruleForm = this.chartForm
  },
  methods: {
    handleClick() {

    },
    submitForm() {
      this.$emit('submitForm', this.ruleForm);
    }
  }
}
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
