<!--
作者: nodebook@qq.com
组件名称: 第一个
-->
<template>
    <div class="documentation-index1"  id="datasets">
        <h3 class="documentation-index1-h3">Datasets and usage</h3>
        <div class="documentation-index1-title-line">
            <div class="documentation-index1-title">iPscDB mainly provides five modules:</div>
            <div class="documentation-index1-title">Browser - Including meta information, sample QC, sanmple intergration, and download options for both .rds file formats for our datasets.</div>
            <div class="documentation-index1-title">Atlas - Including 23 species atlases and 33 tissue atlaese, each of which can be viewed and downloaded, and contains a variety of displays。</div>
            <div class="documentation-index1-title">Marker - Including general and classic two types of markers, and the data can be found in the summary and details marker tables .</div>
            <div class="documentation-index1-title">Search - Three seacrch methods, include marker gene search, cell type search and sequence search using Blast.</div>
            <div class="documentation-index1-title">
                Tools - Including seven tools: Cross-species cell annotation, Cell-Cell interactions, Developmental trajectory, eSCP, Plant CelliD, Plant Cell-Blast, and Plant CtAmr.
            </div>
        </div>
        <h6 class="documentation-index1-h4">A.Datasets</h6>
        <div class="documentation-index1-title-line">
            <div class="documentation-index1-title">
                PscDB downloaded SRA data from databases such as NCBI, ENI and GSA for 691 experiments in 41 projects, covering 23 plant species (including model plants such as Arabidopsis, rice,
                maize, soybean, tomato and tobacco), and we aligned the original data with reference genomes. At the same time, two different types of cell markers were collected: experimentally
                validated marker genes, and differentially expressed genes of specific cells identified by scRNA-seq. In order to ensure the unity of tissue and cell types, we normalized tissue and
                cell type names into standard bibliographies based on the Plant Ontology database.
            </div>
            <div class="documentation-index1-image">
                <img src="../../../assets/img/wps1.png" />
            </div>
        </div>
        <h6 class="documentation-index1-h4">B.Usage</h6>
        <div class="documentation-index1-title-line">
            <div class="documentation-index1-title">
                <span style="font-size: 20px">Home</span><br />
                The home page provides a global view of 23 plant tissue maps, and by clicking on hyperlinks embedded in web images, you can quickly explore the cell maps of entire plants and tissues.
                The tissue chart of different plants can be switched by clicking on the picture in the upper right corner. The Tissue chart makes it easy to quickly browse the map of listed cell
                types, and a detailed interface for painting the map can be accessed by clicking the tissue icon.
            </div>
            <div class="documentation-index1-image">
                <img src="../../../assets/img/wps2.jpg" />
            </div>
            <div class="documentation-index1-title">
                <span style="font-size: 20px">Browser</span><br />
                In this module, iPscDB provides all data statistics, details of each data set, and data integration operations. The data statistics show the number of species, data sets, cell maps,
                number of genes, number of cell markers and so on.
            </div>
            <div class="documentation-index1-image">
                <img src="../../../assets/img/wps3.png" />
            </div>
            <div class="documentation-index1-title">
                In addition, meta information is provided for each data set, Information includes dataset, BioProject, Species, Tissue, Treatment, Genotype, Libraries, AGE, Samples, Cells and
                Publication, Users can use browser buttons or download datasets.
            </div>
            <div class="documentation-index1-image">
                <img src="../../../assets/img/wps4.png" />
            </div>
            <div class="documentation-index1-title">
                Finally, we provide online Sample quality control and data integration analysis. After selecting the above data set, click the Sample QC button, you can enter the cell quality control
                interface, submit relevant parameters for operation, and download the rds file after quality control.
            </div>
            <div class="documentation-index1-image">
                <img src="../../../assets/img/wps5.png" />
            </div>
            <div class="documentation-index1-title">
                <span style="font-size: 20px">Atlas</span><br />
                In this module, we provide two types of Atlas：Species atlas and Tissue atlas. The interface provides browsing and downloading functions, and the data displays species name, tissue
                name, number of data sets, number of cell types and number of cells.
            </div>
            <div class="documentation-index1-image">
                <img src="../../../assets/img/wps6.png" />
            </div>
            <div class="documentation-index1-image">
                <img src="../../../assets/img/wps7.png" />
            </div>
            <div class="documentation-index1-title">
                In the explore interface, the gene retrieval function could be found in the upper part, the Umap infographic of Atlas, a variety of information was displayed diagrams, and the cell
                markers and sample tables were displayed below.
            </div>
            <div class="documentation-index1-image">
                <img src="../../../assets/img/wps8.png" />
            </div>
            <div class="documentation-index1-title">
                <span style="font-size: 20px">Marker</span><br />
                Here, iPscDB offers an informative module that provides marker gene information for each cell type across various species. Users can easily select a cell type using either the Bar
                chart or the Tree list. In the specific cell type panel, scPlantDB offers informative visualizations in the form of word clouds that display the number of source datasets for each
                marker gene. Additionally, users can access meta-information about the cell type, including the number of plant species and tissues that share this cell type.
            </div>
            <div class="documentation-index1-image">
                <img src="../../../assets/img/wps9.png" />
            </div>
            <div class="documentation-index1-image">
                <img src="../../../assets/img/wps10.png" />
            </div>
            <div class="documentation-index1-title">
                In the tables of marker genes, the times of the gene are displayed, which has been reported in a certain cell type, and whether the gene has been validated experimentally. If it is a
                classic gene, its pentagram will light up. At the same time, in the details table, the P-value and fold-change value of each marker gene are displayed.
            </div>
            <div class="documentation-index1-image">
                <img src="../../../assets/img/wps11.png" />
            </div>
            <div class="documentation-index1-image">
                <img src="../../../assets/img/wps12.png" />
            </div>
            <div class="documentation-index1-title">
                <span style="font-size: 20px">Search</span><br />
                Users can easily access the search panel in iPscDB by simply clicking on the search icon in the navigation bar. The search panel offers two efficient methods to help users quickly find
                the desired information: marker/cell type name searching and sequence searching. The marker/cell type name search allows users to enter keywords related to the cell type or marker they
                are looking for, including both exact matches and partial matches of markers description. On the other hand, the sequence search mainly relies on BLAST algorithm, allowing users to
                input a nucleotide or amino acid sequence and compare it against sequences of species in the database. Both searching methods offer convenient and precise results to meet users’
                various research needs.
            </div>
            <div class="documentation-index1-image">
                <img src="../../../assets/img/wps13.png" />
            </div>
            <div class="documentation-index1-title">
                <span style="font-size: 20px">Tools</span><br />
                iPscDB provides a wealth of online single-cell data analysis capabilities, includes Cross-species gene expression, Cell-Cell interaction, Developmental trajectory analysis, electronic
                Single-Cell Pictograph, Plant Cell iDentification, Plant Cell Blast and Plant cell type annotation with multiple references tools, users can choose the appropriate tools according to
                the needs of data analysis for analysis. Among these 7 tools, we provide 3 cell type annotation and classification analysis tools, enabling accurate and rapid annotation of cell types
                across species and within species.
            </div>
            <div class="documentation-index1-image">
                <img src="../../../assets/img/wps14.png" />
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
        margin-bottom: 20px;
    }
    .documentation-index1-image {
        width: 100%;
        height: auto;
        img {
            width: 100%;
        }
    }
}
</style>
