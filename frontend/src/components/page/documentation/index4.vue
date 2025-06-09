<!--
作者: nodebook@qq.com
组件名称: 第一个
-->
<template>
    <div class="documentation-index1"  id="submit">
        <h3 class="documentation-index1-h3">Submit data</h3>
        <div class="documentation-index1-title-line">
            <div class="documentation-index1-title">Welcome to submit single-cell data to the iPscDB</div>
            <div class="documentation-index1-title">
                If you have a group of single-cell data in plants and would like to submit them to iPscDB.Please email your expression matrix data to penglu2004@hotmail.com, peijiancao@163.com with
                the following format:
            </div>
            <div class="documentation-index1-title">1.RDS file</div>
            <div class="documentation-index1-title">2. Barcodes, Features, and Matrix files</div>
            <div class="documentation-index1-title">3.H5 file</div>
            <div class="documentation-index1-title">4.Reference genome version</div>
            <div class="documentation-index1-title">Sinale-cell data will be uploaded after manuscript acceptance. All submissions will be really appreciated!</div>
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
