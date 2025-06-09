<template>
  <div class="searchResult">
    <div class="crumbs">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item style="color:#666;" :to="{ path: '/search' }">Search</el-breadcrumb-item>
        <el-breadcrumb-item>searchList</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="search-inner">
      <jg-table :tableData="tableData" :column='column' :loading='loading' :cellstyle="cellstyle" :paginationConfig="paginationConfig"
        @handleCurrentChange="handleCurrentChange" @handleSizeChange="handleSizeChange" @handlecell='handlecell'></jg-table>
    </div>
  </div>
</template>

<script>
import { sample_plant_search, search_cluster_marker, search_cell_marker } from "@/api/api";
import jgTable from '@/components/jgTable/index'

export default {
  name: "searchList",
  components: {
    jgTable
  },
  data() {
    return {
      // tableHeight: (window.innerHeight - 416),
      tableData: [],
      column: [],
      paginationConfig: {
        page: 1,
        size: 10,
        sizes: [10, 20, 30],
        total: 0
      },
      loading: false
    };
  },
  mounted() {
    this.getTableData()
  },
  methods: {
    getTableData() {
      this.loading = true
      if (this.$route.query.type == 'sample_form') {
        this.column = [
          { key: 'sam_id', label: 'Sam ID' },
          { key: 'sample_id', label: 'Sample ID' },
          { key: 'project_id', label: 'Project ID' },
          { key: 'species_name', label: 'Species Name' },
          { key: 'sample_type', label: 'Sample Type' },
          { key: 'tissue', label: 'Tissue', width: 90 },
          { key: 'chemistry', label: 'Chemistry' },
          { key: 'pmid', label: 'Lit ID', width: 80 }
        ]
        sample_plant_search({
          ...this.$route.query,
          ...{
            page: this.paginationConfig.page,
            page_size: this.paginationConfig.size
          }
        }).then(res => {
          if (res.code == 200) {
            this.tableData = res.data.results
            this.paginationConfig.total = res.data.count
            this.loading = false
          }
        });
      } else if (this.$route.query.type == 'clusterMarker_form') {
        this.column = [
          { key: 'cluster_marker_id', label: 'ClMark ID' },
          { key: 'species_name', label: 'Species Name' },
          { key: 'tissue_id', label: 'Tissue ID', width: 90 },
          { key: 'cluster_name', label: 'Cluster Name' },
          { key: 'cluster_marker', label: 'Cluster Marker' },
          { key: 'gene_id', label: 'Gene ID' },
          { key: 'gene_id_other', label: 'GeneID Other' },
          { key: 'pmid', label: 'Lit ID', width: 80 },
        ]
        search_cluster_marker({
          ...this.$route.query,
          ...{
            page: this.paginationConfig.page,
            page_size: this.paginationConfig.size
          }
        }).then(res => {
          if (res.code == 200) {
            this.tableData = res.data.results
            this.paginationConfig.total = res.data.count
            this.loading = false
          }
        });
      } else if (this.$route.query.type == 'cellMarker_form') {
        this.column = [
          { key: 'mar_id', label: 'Mar ID', width: 100 },
          { key: 'species_name', label: 'Species Name' },
          { key: 'tissue_id', label: 'Tissue ID', width: 90 },
          { key: 'cell_id', label: 'Cell ID' },
          { key: 'gene_symbol', label: 'Gene Symbol' },
          { key: 'gene_id', label: 'Gene ID', width: 120 },
          { key: 'gene_id_other', label: 'GeneID Other' },
          { key: 'source_id', label: 'Source ID' },
          { key: 'pmid', label: 'Lit ID', width: 80 },
        ]
        search_cell_marker({
          ...this.$route.query,
          ...{
            page: this.paginationConfig.page,
            page_size: this.paginationConfig.size
          }
        }).then(res => {
          if (res.code == 200) {
            this.tableData = res.data.results
            this.paginationConfig.total = res.data.count
            this.loading = false
          }
        });
      }

    },
    handleCurrentChange(val) {
      this.paginationConfig.page = val;
      this.getTableData()
    },
    handleSizeChange(val) {
      this.paginationConfig.page = 1
      this.paginationConfig.size = val
      this.getTableData()
    },
    cellstyle({ row, column, rowIndex, columnIndex }) {
      if (column.label === 'Lit ID') {
        return { color: "#0a9daa", cursor: "pointer" }
      }
      return { fontSize: '14px' }
    },
    handlecell(params) {
      if (params.col.label == 'Lit ID') {
        window.open(`https://pubmed.ncbi.nlm.nih.gov/${params.row.pmid}/`, '_blank')
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.searchResult {
  width: 100%;
  height: 100%;
  margin: 0 auto;
  background: #fafafa;
  padding: 0 0 30px 0;
  .crumbs {
    width: 1200px;
    margin: 0 auto;
    height: 28px;
    padding-top: 12px;
  }
  .search-inner {
    width: 1200px;
    padding: 20px;
    margin: 0 auto;
    overflow: hidden;
    background: rgba(255, 255, 255, 1);
  }
}
</style>
