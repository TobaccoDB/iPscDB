<template>
  <div class="monocleExpressed">
    <div class="crumbs">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/monocle' }">Developmental trajectory</el-breadcrumb-item>
        <el-breadcrumb-item>Differential expressed genes</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="monocleExpressed-inner" :style="{minHeight: contentHeight}" element-loading-text="loading" element-loading-background="#fff">
      <div class="searchJump">
        <span>Genes:</span>
        <!-- <el-select v-model="searchJump" size="large" style="width:250px;" collapse-tags filterable multiple placeholder="Choose">
          <el-option v-for="item in genesOptions" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select> -->
        <el-select v-model="searchJump" size="large" style="width:250px;" multiple filterable remote reserve-keyword placeholder="Please enter keywords"
          :remote-method="remoteMethod" :loading="selectLoading">
          <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
        <el-button type="primary" size="lager" style="margin-left:20px;" @click="search">GO</el-button>
      </div>
      <el-radio-group style="margin:20px 0;" v-model="radioType" @change="search">
        <el-radio label="Pseudotime">Pseudotime</el-radio>
        <el-radio label="State">State</el-radio>
        <el-radio label="cell_type">Cell type</el-radio>
        <el-radio label="seurat_clusters">Cluster</el-radio>
      </el-radio-group>
      <!-- 图片 -->
      <div class="static_img" style="text-align:center;" v-loading="loading" element-loading-text="running" element-loading-background="#fff">
        <img style=" max-width: 100%;max-height: 95%;margin-top:10px;" :src="staticUrl" v-loading="loading" element-loading-text="running"
          element-loading-background="#fff">
        <div style="width:100%;height:212px;overflow:hidden;line-height:212px;font-size:14px;color:#999;text-align:center;" v-if="!staticUrl"
          v-loading="loading" element-loading-text="running" element-loading-background="#fff">
          No data
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { monocle_expressed_down, monocle_expressed_png } from "@/api/api";
import jgTable from '@/components/jgTable/index'

export default {
  name: "monocleExpressed",
  components: {
    jgTable
  },
  data() {
    return {
      contentHeight: (window.innerHeight - 330) + 'px',
      radioType: 'State',
      staticUrl: '',
      genesOptions: [],
      loading: false,
      searchJump: '',
      selectLoading: false,
      options: []

    };
  },
  mounted() {
    this.radioType = this.$route.query.type
    this.searchJump = this.$route.query.gene.split(',')
    this.init()
    this.search()
  },
  methods: {
    init() {
      monocle_expressed_down({
        species_name: this.$route.query.species_name,
        tissue: this.$route.query.tissue,
        cell_type: this.$route.query.cell_type,
        page: 1,
        page_size: 10000
      }).then(res => {
        if (res.code == 200) {
          this.genesOptions = []
          res.data && res.data.forEach(item => {
            this.genesOptions.push({
              label: Object.entries(item)[0][1],
              value: Object.entries(item)[0][1]
            })
          });
        }
      });
    },
    remoteMethod(query) {
      if (query !== '') {
        this.selectLoading = true;
        setTimeout(() => {
          this.selectLoading = false;
          this.options = this.genesOptions.filter(item => {
            return item.label.toLowerCase()
              .indexOf(query.toLowerCase()) > -1;
          }).slice(0, 20);
        }, 200);
      } else {
        this.options = [];
      }
    },
    search() {
      this.loading = true
      monocle_expressed_png({
        species_name: this.$route.query.species_name,
        tissue: this.$route.query.tissue,
        cell_type: this.$route.query.cell_type,
        gene: this.searchJump.join(),
        type: this.radioType
      }).then(res => {
        if (res.code == 200) {
          this.staticUrl = res.data.expression_png
          this.loading = false
        }
      });
    }
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
