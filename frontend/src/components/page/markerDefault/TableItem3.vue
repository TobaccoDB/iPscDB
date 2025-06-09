<template>
    <div class="tableItem">
        <div class="TableItemHeader">
            <el-input v-model="searchVal" placeholder="Search.." @keyup.enter.native="keydown"
                style="width: 210px; margin-right: 10px" suffix-icon="el-icon-search"></el-input>
            <el-button icon="el-icon-download" type="success"> <span style="font-size: 12px" :loading="loadingButton"
                    @click="getDownload">CSV</span></el-button>
        </div>
        <el-table :data="tableData" style="width: 100%" v-loading="loading">
            <el-table-column prop="gene" label="Gene ID" width="140px" align="center">
                <template slot-scope="scope">
                    <span style="color: #24a461; text-decoration: underline; cursor: pointer; font-size: 12px"
                        @click="goMarkerCell(scope.row.gene)">{{ scope.row.gene }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="name" label="Gene Name" width="140px" align="center"> </el-table-column>
            <el-table-column prop="tissue" v-if="type && type == 'searchResult'" label="Tissue" width="140px"
                align="center">
            </el-table-column>
            <el-table-column prop="clusterName" v-if="type && type == 'searchResult'" label="Celltype" width="140px"
                align="center">
            </el-table-column>
            <el-table-column prop="cellType_id" label="Celltype ID" width="140px" align="center"> </el-table-column>
            <el-table-column prop="source_no" label="Classic Marker" width="120px" align="center">
                <template slot-scope="scope">
                    <span class="tableItemTableIcon"
                        :class="scope.row.classic_marker == '1' ? 'el-icon-star-on tableItemTableIconActive' : 'el-icon-star-off '"></span>
                </template>
            </el-table-column>
            <el-table-column prop="source_no" label="Source No." width="100px" align="center"> </el-table-column>
            <el-table-column prop="dataset" label="Source Dataset" align="center"> </el-table-column>
        </el-table>
        <div class="TableItemBody">
            <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                :current-page="queryInfo.page" :page-sizes="[10, 20, 30, 50]" :page-size="queryInfo.page_size"
                layout="total, sizes, prev, pager, next" :total="count" background>
            </el-pagination>
        </div>
    </div>
</template>

<script>
import { marker_summary_list, marker_summary_download } from '@/api/api'
export default {
    props: ['type'],
    data() {
        return {
            searchVal: '',
            searchValue: '',
            currentPage4: 4,
            tableData: [],
            queryInfo: {
                page: 1,
                page_size: 10
            },
            count: 0,
            loading: false,
            loadingButton: false,
            baseUrl: process.env.VUE_APP_BASE_URL,
            defaultData:{
                "arabidopsisthalianainflorescence": "AT1G09200",
                "zeamayswholeplant": 'Zm00001d000316',
                "oryzasativawholeplant": "Os04g0599650",
                "zeamaysroottip": "Zm00001d017508",
                "populusalbaxglandulosawholeplant": "Pop-A02G065604",
                "populusalbaxglandulosastem": "Pop-A02G065604",
                "medicagotruncatulawholeplant": "MtrunA17Chr2g0319211",
                "medicagotruncatularoot": "MtrunA17Chr2g0319211",
                "glycinemaxwholeplant": "Glyma.08G131900",
                "glycinemaxroot": "Glyma.08G131900"
            }
        }
    },
    mounted() {
        this.getTable(true)
    },
    methods: {
        goMarkerCell(val) {
            this.$router.push({
                path: '/markerCell',
                query: {
                    gene_id: val,
                    species_name: this.$route.query.name
                }
            })
        },
        keydown(e) {
            this.searchValue = this.searchVal
            this.queryInfo.page = 1
            this.queryInfo.page_size = 10
            this.getTable()
        },
        getTable(bool) {
            let infoData = {
                species_name: this.$route.query.nameLabel
            }
            infoData.tissue_name = this.$route.query.tissue_label

            this.loading = true
            marker_summary_list({
                ...infoData,
                ...this.queryInfo,
                search_gene: this.searchValue,
                query_type: 'home'
            })
                .then((res) => {
                    if (res.code === 200) {
                        this.count = res.data.count
                        this.tableData = res.data.results
                    
                        if(bool){
                            if(this.tableData.length > 0){
                                // console.log(this.tableData[0].gene)
                                // props.setVal( this.tableData[0].gene)
                                let key = this.$route.query.nameLabel.replace(/\s+/g, '').toLocaleLowerCase() + this.$route.query.tissue_label.replace(/\s+/g, '').toLocaleLowerCase()

                              

                                if(this.defaultData[key]){

                                    // console.log(this.defaultData[key], '-----------key')


                                    this.$emit('setVal', this.defaultData[key]);
                                }else {
                                    this.$emit('setVal', this.tableData[0].gene);
                                }   
                               
                            }
                            // props.setVal() gene
                        }
                    } else {
                        this.tableData = []
                    }
                    this.loading = false
                })
                .catch((err) => {
                    this.tableData = []
                    this.loading = false
                })
        },
        getDownload() {
            let url = `${this.baseUrl}/api/v1/marker_summary_list/marker_summary_download?species_name=${this.$route.query.nameLabel}&tissue_name=${this.$route.query.tissue_label}&search_gene=${this.searchValue}`
            // if (this.selectValue.level > 2) {
            //     url = url + `&cell_name=${this.selectValue.name}`
            // }
            window.open(url)
            // let fileName = new Date().getTime() + '.csv'
            // const a = document.createElement('a')
            // a.href = url
            // a.download = fileName
            // a.target = '_blank'
            // a.style.display = 'none'
            // document.body.appendChild(a)
            // a.click()
            // document.body.removeChild(a)
        },
        handleSizeChange(val) {
            this.queryInfo.page = 1
            this.queryInfo.page_size = val
            this.getTable()
        },
        handleCurrentChange(val) {
            this.queryInfo.page = val
            this.getTable()
        }
    }
}
</script>

<style scoped lang="scss">
.tableItem {
    width: 100%;
    height: auto;
    padding: 12px 0;
    box-sizing: border-box;

    .TableItemHeader {
        width: 100%;
        height: 40px;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }

    .TableItemBody {
        height: 50px;
        width: 100%;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }

    .tableItemTableIcon {
        font-size: 30px;
    }

    .tableItemTableIconActive {
        color: #f7af04;
        font-size: 38px;
    }
}
</style>

<style lang="scss">
.TableItemBody {
    .el-pagination.is-background .el-pager li:not(.disabled).active {
        background-color: #24a461 !important;
    }

    .el-radio__input.is-checked+.el-radio__label {
        color: #24a461 !important;
    }

    .el-radio__input.is-checked .el-radio__inner {
        background: #24a461 !important;
        color: #24a461 !important;
        border-color: #24a461 !important;
    }

    .el-button--primary {
        background: #24a461 !important;
        border-color: #24a461 !important;
        font-size: 16px;
    }
}

.TableItemHeader .el-button--success {
    background: #24a461;
}
</style>
