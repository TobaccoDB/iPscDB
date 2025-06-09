<template>
    <div class="search-list">
        <div class="crumbs">
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-breadcrumb-item :to="{ path: '/searchForm' }">Search</el-breadcrumb-item>
                <el-breadcrumb-item>Blast Results</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="search-list-inner">
            <div class="firstChild">Blast Results</div>
            <div class="search-list-table">
                <!--  @cell-click="handlecell" -->
                <el-table
                    :data="tableData"
                    class="table"
                    ref="multipleTable"
                    stripe
                    header-cell-class-name="table-header"
                    :header-cell-style="headerStyle"
                    :row-style="rowStyle"
                    :row-class-name="tableRowClassName"
                    :cell-style="cellstyle"
                    @cell-click="cellClick"
                >
                    >
                    <el-table-column v-for="(item, index) in tableDataItem" :width="item.width" :key="index" :prop="item.prop" align="center" :show-overflow-tooltip="true" :label="item.label">
                    </el-table-column>
                </el-table>
            </div>
            <div style="margin-top: 20px">
                <dl class="ruler_dl">
                    <dt>{{ titleH1 }}</dt>
                    <dd>
                        <div class="ruler">
                            <div class="cm" v-for="(items, indexs) in itemCm" :v-for="indexs">
                                <div class="mm" v-for="(item, index) in 4" :key="index"></div>
                                <span>{{ items }}</span>
                            </div>
                            <div class="cm">
                                <span>{{ alignLength }}</span>
                            </div>
                        </div>
                    </dd>
                </dl>
                <dl class="ruler_dl ruler_dl1" v-for="(item, index) in itemContent" :key="index">
                    <dt>{{ item.hits }}</dt>
                    <dd v-if="(Number(item.score) > 0 && Number(item.score) < 50) || Number(item.score) == 50" style="background: #305db7"></dd>
                    <dd v-if="(Number(item.score) > 50 && Number(item.score) < 100) || Number(item.score) == 100" style="background: #868ba3"></dd>
                    <dd v-if="(Number(item.score) > 100 && Number(item.score) < 150) || Number(item.score) == 150" style="background: #c59c49"></dd>
                    <dd v-if="(Number(item.score) > 150 && Number(item.score) < 200) || Number(item.score) == 200" style="background: #3b9c25"></dd>
                    <dd v-if="Number(item.score) > 200" style="background: #bc423b"></dd>
                </dl>
                <dl class="ruler_dl" style="margin-top: 30px">
                    <dt>{{ titleH1 }}</dt>
                    <dd>
                        <div class="ruler ruler1">
                            <div class="cm" v-for="(items, indexs) in itemCm" :key="indexs">
                                <div class="mm" v-for="(item, index) in 4" :key="index"></div>
                                <span>{{ items }}</span>
                            </div>
                            <div class="cm">
                                <span>{{ alignLength }}</span>
                            </div>
                        </div>
                    </dd>
                </dl>
                <dl class="ruler_dl ruler_dl3">
                    <dt>Scoring <br />colors</dt>
                    <dd>
                        <ul>
                            <li style="background: #305db7"></li>
                            <li style="background: #868ba3"></li>
                            <li style="background: #c59c49"></li>
                            <li style="background: #3b9c25"></li>
                            <li style="background: #bc423b"></li>
                        </ul>
                        <ul style="margin-top: 5px">
                            <li>S>0</li>
                            <li>S>50</li>
                            <li>S>100</li>
                            <li>S>150</li>
                            <li>S>200</li>
                        </ul>
                    </dd>
                </dl>
                <div v-for="(item, index) in itemsBottom" :key="item.hits + index" style="color: #666; font-size: 14px">
                    <p class="bottom_p">
                        <!-- <span style="cursor: pointer; color: rgb(34, 173, 99); padding-right: 10px" @click="jump(item.id)">>{{ item.hits }}</span> -->
                        <span style="color: rgb(34, 173, 99); padding-right: 10px">>{{ item.hits }}</span>
                        {{ item.description }}
                    </p>
                    <p class="bottom_p">Score = {{ item.score1 }} bits ({{ item.bits1 }})， Expect = {{ item.Expect1 }},Method: Compositional matrix adjus</p>
                    <p>Identities = {{ item.IdentitiesFz }}/{{ item.IdentitiesFm }}({{ item.IdentitiesBfb }}%)，Positives= {{ item.PositivesFz }}/{{ item.PositivesFm }}({{ item.PositivesBfb }}%)</p>
                    <div v-for="(que_sbj, idx) in querySbjct" :key="idx">
                        <p class="bottom_p">
                            <span v-html="que_sbj.query"></span>
                        </p>
                        <p style="margin-left: 3em">
                            <span v-html="que_sbj.match"></span>
                        </p>
                        <p class="bottom_p">
                            <span v-html="que_sbj.sbjct"></span>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { tableDataItem } from './config'
import { tableData } from './index'
export default {
    data() {
        return {
            tableDataItem,
            tableData: [],
            pageTotal: 0,
            query: {
                page: 1,
                size: 10
            },
            headerStyle: {
                background: '#F5F9FC',
                fontSize: '16px',
                fontFamily: 'PingFang SC',
                fontWeight: 'bold',
                color: '#333'
            },
            rowStyle: {
                fontSize: '14px',
                fontFamily: 'PingFang SC',
                fontWeight: '400',
                color: '#666'
            },
            itemCm: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
            itemContent: [],
            str: '',
            titleH1: '',
            alignLength: 0,
            itemsBottom: [],
            querySbjct: []
        }
    },
    created() {
        this.getData()
    },
    methods: {
        tableRowClassName({ row, rowIndex }) {
            if (rowIndex === 1) {
                return 'warning-row'
            } else if (rowIndex === 3) {
                return 'success-row'
            }
            return ''
        },
        getData() {
            this.tableData = JSON.parse(sessionStorage.getItem('tableData'))
            if (!this.tableData) {
                return
            }

            this.titleH1 = (this.tableData && this.tableData[0] && this.tableData[0].query_id) || ''
            this.itemContent = this.tableData
            this.itemsBottom = JSON.parse(JSON.stringify(this.tableData))
            this.itemCm = []
            for (let i = 0; i < 10; i++) {
                this.itemCm.push(`${Math.floor(this.tableData[0].align_length / 10) * i}`)
            }
            this.alignLength = this.tableData[0].align_length
            this.itemsBottom.forEach((item) => {
                item.score1 = item.bits
                item.bits1 = item.alignment_length
                item.Expect1 = item.expect
                item.IdentitiesFz = item.identities
                item.IdentitiesFm = item.align_length
                item.IdentitiesBfb = (Number(item.identities) / Number(item.align_length)).toFixed(2) * 100
                item.PositivesFz = item.positives
                item.PositivesFm = item.align_length
                item.PositivesBfb = (Number(item.positives) / Number(item.align_length)).toFixed(2) * 100
                this.querySbjct = []
                for (let i = 0; i < Math.ceil(item.query.length / 60); i++) {
                    this.querySbjct.push({
                        query:
                            `<span style="display:inline-block;width:90px;">Query:${Number(1) + i * 60}</span>` +
                            `<span style="display:inline-block;text-align:justify;width:auto;">${item.query.substr(i * 60, 60)}</span>` +
                            `<span style="display:inline-block;padding-left:10px;">${i < Math.ceil(item.query.length / 60) - 1 ? (i + 1) * 60 : item.query.length}</span><br />`,
                        // match: `${item.match} <br />`,
                        sbjct:
                            `<span style="display:inline-block;width:90px;">Sbjct:${Number(1) + i * 60}</span>` +
                            `<span style="display:inline-block;text-align:justify;width:auto;">${item.sbjct.substr(i * 60, 60)}</span>` +
                            `<span style="display:inline-block;padding-left:10px;">${i < Math.ceil(item.query.length / 60) - 1 ? (i + 1) * 60 : item.query.length}</span><br />`
                    })
                }
            })
        },
        handlecell(row, col) {
            if (col.label === 'Subject') {
                if (row.lnc_or_isform == 'isform') {
                    sessionStorage.removeItem('isoform_id')
                    sessionStorage.setItem('isoform_id', row.hit_id)
                    this.$router.push('/nunMirGene')
                } else {
                    sessionStorage.removeItem('lncRNA_id')
                    sessionStorage.setItem('lncRNA_id', row.hit_id)

                    //   sessionStorage.removeItem("blastQuery");
                    // sessionStorage.setItem("blastQuery", JSON.stringify(this.$route.query));
                    this.$router.push({
                        path: '/searchDetails',
                        query: {
                            from: 'blast',
                            id: row.id
                        }
                    })
                }
            }
        },
        jump(id) {
            this.$router.push({
                path: '/searchDetails',
                query: {
                    from: 'blast',
                    id: id
                }
            })
        },
        cellstyle({ row, column, rowIndex, columnIndex }) {
            if (columnIndex === 1) {
                // cursor: 'pointer'
                // return { color: 'rgb(34, 173, 99)' }
                return { color: 'rgb(34, 173, 99)', cursor: 'pointer', textDecoration: 'underline' }
            }
            if (column.label === 'Species') {
                return {
                    fontStyle: 'italic'
                }
            }
        },
        cellClick(row, column, cell, event) {
            console.log(row.hits.substr(0, row.hits.lastIndexOf('.')))
            this.$router.push({
                path: '/markerCell',
                query: {
                    gene_id: row.hits.substr(0, row.hits.lastIndexOf('.')),
                    species_name: row.species_name
                }
            })
        }
    }
}
</script>

<style lang="scss" scoped>
@import './style.scss';
</style>
