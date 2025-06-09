<template>
  <div class="atlas" :style="{ minHeight: '390px'}">
    <div class="atlas-inner">
      <div class="scsa" v-loading="loading">
        <el-row :gutter="20" style="width:100%;height:auto;overflow:hidden;">
          <el-col :span="8" v-for="(item, index) in listItem" :key="index">
            <div class="grid-content">
              <div class="title">{{item.label}}</div>
              <ul class="ul-content">
                <li><img :src="item.species_whole_plant" /></li>
                <li style="width:30%;">
                  <img v-if="tissue.Tissue != 'WholePlant'" :class="{active: cur[index] == i}" :style="tissue.is_show == '1' ? 'cursor: pointer;' : 'filter: grayscale(100%) opacity(40%);'"
                    :src="tissue.tissue_head_link" v-for="(tissue, i) in item.data" :key="i" @click="imgClick(item.name, tissue, index,i)"
                  />
                </li>
              </ul>
              <!-- <ul class="ul-content">
                <li>
                  <span>Tissue:</span>
                  <span>{{item.Tissue}} </span>
                </li>
                <li>
                  <span>Cell:</span>{{item.cell_count}}</li>
              </ul> -->
              <div class="btn-content">
                <p>
                  <el-button size="medium" class="btn" type="text" @click="jumpProjectResult(item, index)">Explore</el-button>
                </p>
                <p>
                  <el-button size="medium" class="btn" type="text" @click="Download(item)">Download</el-button>
                </p>

              </div>
            </div>
          </el-col>
        </el-row>
        <!-- 下载组织选择框 -->
        <el-dialog title="Organization selection" :close-on-click-modal="false" width="500px" :visible.sync="dialogFormVisible">
          <el-form :model="form" :inline="true">
            <el-form-item label="Tissue">
              <el-select style="width:395px;" v-model="form.tissue" placeholder="choose">
                <el-option v-for="(item, index) in tissueOptions" :key="index" :label="item.tissue_label" :value="item.Tissue"></el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">Cancel</el-button>
            <el-button type="primary" @click="submitDownLoad">Submit</el-button>
          </div>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script>
import { atlas_tissue_cell_sample_count, cell_atlas_download, project_lit_down } from "@/api/api";
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
      listItem: [],
      cur: [100, 100, 100, 100, 100],
      tempData: [],
      form: {
        tissue: 'WholePlant'
      },
      tissueOptions: [],
      dialogFormVisible: false
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
      atlas_tissue_cell_sample_count().then(res => {
        if (res.code == 200) {
          if (res.data.length > 0) {
            this.listItem = res.data
          }
        }
      });

      //   atlas_tissue_cell_sample_count().then(res => {
      //   if (res.code == 200) {
      //     if (res.data.length > 0) {
      //       this.menuList = res.data
      //     }
      //   }
      // });
    },
    imgClick(name, item, index, i) {
      if (item.is_show == '1') {
        // this.cur[index] = Number(i)
        this.tempData[index] = item
        this.$set(this.cur, index, Number(i))
        this.$router.push({
          path: '/searchResult',
          query: {
            Tissue: this.tempData[index].Tissue,
            tissue_label: this.tempData[index].tissue_label,
            cell_count: this.tempData[index].cell_num,
            // cell_count: this.tempData[index].cell_count,
            name: name,
            sample_count: this.tempData[index].sample_count
          }
        })
      }
    },
    jumpProjectResult(item, index) {
      if (this.tempData.length == 0) {
        // 整株
        item.data.forEach(element => {
          if (element.Tissue == 'WholePlant') {
            this.$router.push({
              path: '/searchResult',
              query: {
                Tissue: element.Tissue,
                tissue_label: element.tissue_label,
                cell_count: element.cell_num,
                // cell_count: element.cell_count,
                name: item.name,
                sample_count: element.sample_count
              }
            })
          }
        });
      } else {
        if (this.tempData[index] && this.tempData[index].is_show == '1') {
          this.$router.push({
            path: '/searchResult',
            query: {
              Tissue: this.tempData[index].Tissue,
              tissue_label: this.tempData[index].tissue_label,
              cell_count: this.tempData[index].cell_num,
              // cell_count: this.tempData[index].cell_count,
              name: item.name,
              sample_count: this.tempData[index].sample_count
            }
          })
        }
      }


    },
    Download(item) {
      // Download(index) {
      // if (this.tempData[index] && this.tempData[index].is_show == '1') {
      //   window.open(this.tempData[index].download_rds_link, '_blank')
      // } else {
      //   this.$message('
      this.tissueOptions = item.data.filter(element => {
        return element.is_show == '1'
      })
      this.form.tissue = 'WholePlant'
      this.form.species_name = item.name
      this.dialogFormVisible = true
    },
    submitDownLoad() {
      if (this.form.tissue != '') {
        this.dialogFormVisible = false
        cell_atlas_download(this.form).then(res => {
          if (res.code == 200) {
            window.open(res.data.rds_download_url, '_blank')
          }
        });
      } else {
        this.$message('Please select an Organization!');
      }

    }
  }
};
</script>
<style lang="scss" scoped>
@import "./style.scss";
</style>
