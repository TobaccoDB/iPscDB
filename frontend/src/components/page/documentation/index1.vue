<!--
作者: nodebook@qq.com
组件名称: 第一个
-->
<template>
    <div class="documentation-index1" id="overview">
        <!-- <div class="documentation-index1-title">
            Plant Cell iDentification(Plant CelliD) is an atlas guided automatic cell type identification method which utilize massive public single-cell annotation to predict the cell type quickly
            and accurately.
        </div>

        <div class="documentation-index1-title">
            Plant Cell-Blast is a BLAST-like toolkit for scRNA-seq data querying and annotation, which was built on a neural network-based generative model and a customized cell-to-cell similarity
            metric.
        </div>

        <div class="documentation-index1-title">
            Plant cell type annotation with multiple references(Plant CtAmr) is a ﬂexible single-cell assignment toolkit that integrates multiple references based on multitask deep metric learning
            designed speciﬁcally for cell type annotation within tissues with multiple single-cell sequencing data as references.
        </div> -->
        <h3 class="documentation-index1-h3">Overview</h3>
        <div class="documentation-index1-title-line">
            <h6 class="documentation-index1-h4">Welcome to iPscDB</h6>
            <div class="documentation-index1-title">
                iPscDB is a single cell transcriptomic data resource that includes cell markers, single cell maps, and a
                wealth of data analysis tools. At present, data from 23 species of model
                plants, including Arabidopsis thaliana, rice, corn, tomato, and tobacco, including more than 270,480
                marker genes and more than 3 million single cell data, have been collected,
                providing comprehensive and relatively accurate cell markers and cell maps for cell integration and
                single cell research in different plants and tissues.
            </div>
        </div>
    </div>
</template>

<script setup></script>

<style scoped lang="scss">
.documentation-index1 {
    width: 100%;
    height: auto;

    .documentation-index1-title {
        width: 100%;
        line-height: 20px;
        font-size: 14px;
        // text-indent: 2em;
        margin-bottom: 10px;
        color: #666;
    }

    .documentation-index1-h3 {
        width: 100%;
        margin: 20px 0;
        font-size: 44px;
    }

    .documentation-index1-h4 {
        width: 100%;
        margin: 10px 0;
        font-size: 24px;
    }

    .documentation-index1-title-line {
        border-left: 2px solid #dadde1;
        padding: 10px 20px;
        box-sizing: border-box;
    }
}
</style>
