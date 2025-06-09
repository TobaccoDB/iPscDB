<template>
  <div class="submit">
    <div class="submit-inner">
      <div class="keyword">
        <p class="keyword_p1">Welcome to submit new data to iPscDB</p>
        <el-row :gutter="20">
          <el-col :span="12" v-for="(item, index) in itemList" :key="index">
            <div class="grid-content">
              {{1 + index}}）{{item}}
            </div>
          </el-col>
        </el-row>
        <p class="keyword_p2">Please send your iPscDB to tobaccodb@gmail.com, and provide the above information.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { specie_list } from "@/api/api";
export default {
  name: "submit",
  components: {
  },
  data() {
    return {
      itemList: ['Species', 'Tissue Type', 'Cell Type', 'CellMarker Name', 'Gene Symbol', 'Gene ID', 'Protein Name', 'Marker Resource', 'PMID', 'Note Gene Type', 'Description']
    };
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      specie_list({}).then(res => {
        if (res.code == 200) {

        }
      });
    },
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
