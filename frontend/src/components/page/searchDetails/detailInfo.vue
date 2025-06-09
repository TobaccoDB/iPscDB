
<template>
    <div class="detail-page">
        <div class="content" v-html="message"></div>
    </div>
</template>

<script>
import { cell_detail_seq } from "@/api/search";

export default {
    name: "detailInfo",
    components: {
    },
    data() {
        return {
            message: ''
        };
    },
    mounted() {
        this.init()
    },
    methods: {
        init() {
            cell_detail_seq({ gene_id: this.$route.query.id }).then(res => {
                if (res.code == 200) {
                    if (this.$route.query.name == 'pep') {
                        this.message = ''
                        res.data.results.forEach(item => {
                            this.message += item.gene_id + '<br />' + item.gene_pep_seq.replace(/\n/g, "<br />");
                        });
                    } else {
                        this.message = ''
                        res.data.results.forEach(item => {
                            this.message += item.gene_id + '<br />' + item.gene_cds_seq.replace(/\n/g, "<br />");
                        });
                    }
                }
            });

        }
    }
};
</script>

<style lang="scss" scoped>
.detail-page {
  width: 100%;
  height: 100%;
  overflow: auto;
  .content {
    width: 100%;
    height: auto;
    margin: 0 auto;
    padding: 10px;
    font-family: serif;
    font-size: 20px;
    box-sizing: border-box;
  }
}
</style>
