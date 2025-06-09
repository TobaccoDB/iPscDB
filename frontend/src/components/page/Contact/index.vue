<template>
  <div class="Contact">
    <div class="Contact-inner" :style="{minHeight: contentHeight}" element-loading-text="loading" element-loading-background="#fff">
      <el-container>
        <el-header style="height:40px;">Contact</el-header>
        <el-container>
          <el-main>
            <h3>Comments and suggestions are welcomed</h3>
            <p>If you meet any troubles or find any bugs when you visit iPscDB, please email to
              <span style="color:#0a9daa;">penglu2004@hotmail.com</span>,
              <span style="color:#0a9daa;">peijiancao@163.com</span><br />Address: No.2 Fengyang Street, High-Tech Zone, Zhengzhou, P. R, 450001</p>
          </el-main>
        </el-container>
      </el-container>
      <el-container>
        <el-header style="height:40px;margin-top:20px;">Submit</el-header>
        <el-container>
          <el-main>
            <h3>Welcome to submit single-cell data to the iPscDB</h3>
            <p>If you have a group of single-cell data in plants and would like to submit them to iPscDB.Please email your expression
              matrix data to
              <span style="color:#0a9daa;">penglu2004@hotmail.com</span>,
              <span style="color:#0a9daa;">peijiancao@163.com</span> with the following format:</p>
            <p>1.RDS file</p>
            <p>2. Barcodes, Features, and Matrix files</p>
            <p>3.H5 file</p>
            <p>4.Reference genome version</p>
            <p>Sinale-cell data will be uploaded after manuscript acceptance. All submissions will be really appreciated!</p>
          </el-main>
        </el-container>
      </el-container>
    </div>
  </div>
</template>
<script>
export default {
  name: "Contact",
  components: {
  },
  data() {
    return {
      contentHeight: (window.innerHeight - 330) + 'px'
    };
  },
  mounted() {
  },
  methods: {
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>


