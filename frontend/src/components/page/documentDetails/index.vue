<template>
    <div class="searchDetails">
        <!-- 文献详情 -->
        <div class="searchDetails-inner">
            <dl class="mainDl">
                <dd><span>Title：</span>{{ detailMsg.title }}</dd>
                <dd><span>Author：</span>{{ detailMsg.author }}</dd>
                <dd><span>Source：</span>{{ detailMsg.source }}</dd>
                <dd>
                    <span>PMID：</span>
                    <span v-if="/^(10\.|DOI:)/.test(detailMsg.pmid)" style="color: rgb(36, 164, 97); font-weight: 400; cursor: pointer" @click="jumpPMIDDIO(detailMsg.pmid)">{{ detailMsg.pmid }}</span>
                    <span v-else style="color: rgb(36, 164, 97); font-weight: 400; cursor: pointer" @click="jumpPMID(detailMsg.pmid)">{{ detailMsg.pmid }}</span>
                </dd>
                <dd><span>Abstract：</span>{{ detailMsg.description }}</dd>
            </dl>
        </div>
    </div>
</template>

<script>
import { cell_search_public_detail } from '@/api/search'
export default {
    name: 'searchDetails',
    components: {},
    data() {
        return {
            detailMsg: {
                title: '',
                author: '',
                source: '',
                pmid: '',
                description: ''
            }
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        init() {
            cell_search_public_detail(this.$route.query.id).then((res) => {
                if (res.code == 200) {
                    this.detailMsg = res.data.data
                }
            })
        },
        jumpPMID(id) {
            window.open(`https://pubmed.ncbi.nlm.nih.gov/${id}/`, '_blank')
        },
        jumpPMIDDIO(id) {
            window.open(`https://doi.org/${id}/`, '_blank')
        }
    }
}
</script>
<style lang="scss" scoped>
.searchDetails {
    width: 1240px;
    height: 100%;
    margin: 0 auto;
    background: #fafafa;
    padding: 30px 0;
    .searchDetails-inner {
        width: 1240px;
        margin: 0 auto;
        overflow: hidden;
        background: rgba(255, 255, 255, 1);
        .title1 {
            font-size: 20px;
            font-family: PingFang SC;
            font-weight: bold;
            color: #fff;
            height: 40px;
            line-height: 40px;
            background: #24a461;
            padding-left: 20px;
        }
        .content_detail {
            width: 1200px;
            padding: 10px 20px;
            box-sizing: border-box;
            height: auto;
            overflow: hidden;
            .grid-content {
                min-width: 33.3%;
                float: left;
                height: 38px;
                font-size: 16px;
                font-family: PingFang SC Medium, PingFang SC Medium-Medium;
                font-weight: 500;
                color: #333;
                line-height: 38px;
                span {
                    color: #666;
                    font-weight: 200;
                }
            }
            .grid-content:nth-child(10) span {
                color: #24a461;
                cursor: pointer;
            }
        }
        .content_efp {
            width: 1200px;
            padding: 10px 20px;
            box-sizing: border-box;
            height: auto;
            overflow: hidden;
        }
        .content_document {
            width: 1200px;
            padding: 10px 20px;
            box-sizing: border-box;
            height: auto;
            overflow: hidden;
            .retrieval_pub_ul {
                width: 100%;
                height: auto;
                overflow: hidden;
                box-sizing: border-box;
                li {
                    height: auto;
                    padding: 10px 0;
                    width: 100%;
                    border-bottom: 1px solid #f0f0f0;
                    p {
                        font-size: 16px;
                        height: 30px;
                        line-height: 30px;
                        color: #333;
                        width: 100%;
                        white-space: nowrap;
                        text-overflow: ellipsis;
                        overflow: hidden;
                        word-break: break-all;
                    }
                }
                li p:nth-child(1) {
                    color: #24a461;
                    cursor: pointer;
                }
            }
        }
        // 文献详情
        .mainDl {
            width: 100%;
            float: left;
            height: auto;
            background: #fff;
            padding: 20px;
            box-sizing: border-box;
            padding-top: 10px;
            dd {
                float: left;
                min-height: 30px;
                width: 100%;
                font-size: 14px;
                font-family: Source Han Sans CN;
                font-weight: 400;
                color: #666;
                line-height: 30px;
                text-align: justify;
                display: flex;
                white-space: normal;
                align-items: stretch;
                span {
                    float: left;
                    width: auto;
                    min-height: 30px;
                    font-size: 14px;
                    font-family: Source Han Sans CN;
                    font-weight: 600;
                    color: #333;
                    line-height: 30px;
                }
            }
        }
    }
}
</style>
