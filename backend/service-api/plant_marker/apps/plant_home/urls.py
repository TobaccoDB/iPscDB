from rest_framework import routers

from . import views

router = routers.DefaultRouter()

# 首页物种umap散点图接口
router.register(r'plant_home_umap', views.PlantHomeUmaptViewSet, base_name='plant_home_umap')
# 2023-618 首页但是写个接口
router.register(r'home_umap_polt', views.HomeUmaptPoltViewSet, base_name='home_umap_polt')
# Atlas下面三种检索列表 1：cellType  2：marker 3：sample
router.register(r'plant_atlas_list', views.PlantAtlasListViewSet, base_name='plant_atlas_list')
router.register(r'plant_search_down', views.PlantSearchDownViewSet, base_name='plant_search_down')
# Search 检索功能接口
router.register(r'plant_search', views.PlantSearchViewSet, base_name='plant_search')
# .rds下载接口
router.register(r'plant_sample_rds_download', views.PlantSampleRdsDownloadViewSet,
                base_name='plant_sample_rds_download')
# Project下面三种检索列表 1：cellType  2：marker 3：sample
router.register(r'project_atlas_list', views.ProjrctAtlasListViewSet, base_name='project_atlas_list')
# Sample_QC
router.register(r'sample_qc_upload', views.SampleQcUploadViewSet, base_name='sample_qc_upload')
# GeneExpression
router.register(r'gene_express_umap', views.GeneExpressionUmapViewSet, base_name='gene_express_umap')
# 获取国家访问量列表接口
router.register(r'cell_country_visiter', views.CellCountryVisiterViewSet, base_name='cell_country_visiter')
# Sample_QC
router.register(r'sample_qc_upload_picture', views.SampleQcUploadPictureViewSet, base_name='sample_qc_upload_picture')
# Integration SVG图片生成和RDS文件下载
router.register(r'integration_svg_show', views.IntegrationSvgShowViewSet, base_name='integration_svg_show')
# Integration csv文件下载
router.register(r'integration_download', views.IntegrationDownloadViewSet, base_name='integration_download')
# Integration zip下载脚本接口
router.register(r'integration_zip_download', views.IntegrationZipDownloadViewSet, base_name='integration_zip_download')
# Integration  Example示例图片展示接口
router.register(r'integration_example_show', views.IntegrationExampleShowViewSet, base_name='integration_example_show')
'===================Cell Identification相关接口===================='
# 物种、组织下拉框
router.register(r'cell_identification_species_down', views.CellIdentificationSpeciesDownViewSet,
                base_name='cell_identification_species_down')
# cell_identification文件上传接口
router.register(r'cell_identification_upload', views.CellIdentificationUploadViewSet,
                base_name='cell_identification_upload')
# Cell Identification SVG图片返回展示
router.register(r'cell_identification_svg_show', views.CellIdentificationSvgShowViewSet,
                base_name='cell_identification_svg_show')
# Cell Identification Example SVG图片返回展示
router.register(r'cell_identification_example_svg_show', views.CellIdentificationExampleSvgShowViewSet,
                base_name='cell_identification_example_svg_show')

# 新页面Cell Identification PDF title ---------- 2022/09/14沟通功能接口如下
router.register(r'cell_identification_pdf_title', views.CellIdentificationPdftitleViewSet,
                base_name='cell_identification_pdf_title')
# reference详情
router.register(r'cell_identification_reference_detail', views.CellIdentificationReferenceDetailViewSet,
                base_name='cell_identification_reference_detail')
# reference sample
router.register(r'cell_identification_reference_sample', views.CellIdentificationReferenceSampleViewSet,
                base_name='cell_identification_reference_sample')
'''=====================Cell_Idetification相关功能如下======================'''
# 文件上传接口
router.register(r'cell_reference_identification_upload', views.CellIdentificationReferenceUploadViewSet,
                base_name='cell_reference_identification_upload')
# csv数据生成接口
# cell_identification_create_csv
router.register(r'cell_identification_create_csv', views.CellIdentificationCreateCsvViewSet,
                base_name='cell_identification_create_csv')
# Cell_Idetification 操作生成的文件 进行列表展示
# cell_type
router.register(r'cell_identification_cell_type_list', views.CellIdentificationCellTypeCsvViewSet,
                base_name='cell_identification_cell_type_list')
router.register(r'cell_identification_cell_type_map', views.CellIdentificationCellTypemapViewSet,
                base_name='cell_identification_cell_type_map')
# cors_matrix
router.register(r'cell_identification_cors_matrix_list', views.CellIdentificationCorsMatrixCsvViewSet,
                base_name='cell_identification_cors_matrix_csv')
#
# Integration zip下载脚本接口
router.register(r'cell_identification_csv_zip_download', views.CellIdentificationCsvZipDownloadViewSet,
                base_name='cell_identification_csv_zip_download')
# Browse Statistics饼图统计
router.register(r'cell_browse_statistics', views.CellBrowseStatisticsViewSet,
                base_name='cell_browse_statistics')
# cell Identification 物种和组织下拉框
router.register(r'cell_species_tissues', views.CellSpeciesTissuesViewSet,
                base_name='cell_species_tissues')
# csv数据生成接口
router.register(r'cell_identification_filter_csv', views.CellIdentificationFilterCsvViewSet,
                base_name='cell_identification_filter_csv')
# 2022-10-23 Browse列表页
router.register(r'browse_list', views.BrowseListViewSet, base_name='browse_list')

# 2022-12-20
# Atlas 热力图和柱状图统计接口
router.register(r'atlas_expressed_gene_cell_type_count', views.AtlasExpressedGeneCellTypeCountViewSet,
                base_name='atlas_expressed_gene_cell_type_count')
# Atlas 20230424新增上面柱状图统计接口
router.register(r'atlas_gene_cell_type_count', views.AtlasGeneCellTypeCountViewSet,
                base_name='atlas_gene_cell_type_count')
# Atlas 手风琴和箱图接口
router.register(r'atlas_expressed_gene_violin_box_plot', views.AtlasExpressedGeneViolinBoxPlotViewSet,
                base_name='atlas_expressed_gene_violin_box_plot')
# 2022-10-31
# 热力图和柱状图统计接口
router.register(r'expressed_gene_cell_type_count', views.ExpressedGeneCellTypeCountViewSet,
                base_name='expressed_gene_cell_type_count')

# 手风琴和箱图接口
router.register(r'expressed_gene_violin_box_plot', views.ExpressedGeneViolinBoxPlotViewSet,
                base_name='expressed_gene_violin_box_plot')
# Project Atlas umap散点图接口
router.register(r'expressed_gene_umap_dataset', views.ExpressedUmapDatasetViewSet,
                base_name='expressed_gene_umap_dataset')
# Tissue structure
router.register(r'tissue_structure', views.TissueStructureViewSet,
                base_name='tissue_structure')
# #EFP接口
router.register(r'species_efp', views.SpeciesEfpViewSet, base_name='species_efp')
# #ReferenceCellType列表页接口
router.register(r'reference_cell_type_list', views.ReferenceCellTypeListViewSet,
                base_name='reference_cell_type_list')
# Project static umap 静态图
router.register(r'project_static_umap_png', views.ProjectStaticUmapPngtViewSet,
                base_name='project_static_umap_png')
# Atlas static umap 静态图
router.register(r'atlas_static_umap_png', views.AtlasStaticUmapPngtViewSet,
                base_name='atlas_static_umap_png')
# ====================Monocle相关功能=============================
router.register(r'monocle_expressed_list', views.MonocleExpressedGenesListViewSet,
                base_name='monocle_expressed_list')
router.register(r'monocle_heatmap_list', views.MonocleHeatMapGenesListViewSet,
                base_name='monocle_heatmap_list')
# expressed 图
router.register(r'monocle_expressed_png', views.MonocleExpressedGenesPngViewSet,
                base_name='monocle_expressed_png')
# # expressed 图
router.register(r'monocle_heatmap_png', views.MonocleHeatMapGenesPngViewSet,
                base_name='monocle_heatmap_png')
# gene下拉框
router.register(r'monocle_expressed_down', views.MonocleExpressedGenesDownViewSet,
                base_name='monocle_expressed_down')
# gene下拉框
router.register(r'monocle_heatmap_down', views.MonocleHeatMapGenesDownViewSet,
                base_name='monocle_heatmap_down')
# species_down下拉框
router.register(r'species_down', views.SpeciesDownViewSet,
                base_name='species_down')
# species_tissue下拉框
router.register(r'species_tissue_down', views.SpeciesTissueDownViewSet,
                base_name='species_tissue_down')
# cell_type_down下拉框
router.register(r'species_cell_type_down', views.SpeciesCellTypeDownViewSet,
                base_name='species_cell_type_down')
# monocle最上面的图
# expressed 图
router.register(r'monocle_heat_png', views.MonocleHeatPngViewSet,
                base_name='monocle_heat_png')
##################################################
# Download页面
# 1：Atlas
router.register(r'atlas_download_list', views.AtlasDownloadListViewSet, base_name='atlas_download_list')
# 2：cell_marker
router.register(r'cell_marker_download_list', views.CellMarkerDownloadListViewSet,
                base_name='cell_marker_download_list')
# 3：cell_cluster
router.register(r'cell_cluster_download_list', views.CellClusterDownloadListViewSet,
                base_name='cell_cluster_download_list')
# 4：Atlas下载
router.register(r'atlas_download', views.AtlasDownloadViewSet, base_name='atlas_download')
# 5：cell_marker下载
router.register(r'cell_marker_download', views.CellMarkerDownloadViewSet, base_name='cell_marker_download')
# 6：cluster_marker下载
router.register(r'cell_cluster_download', views.CellClusterDownloadViewSet, base_name='cell_cluster_download')

router.register(r'atlas_specis_download_down', views.AtalsSpeciesDownViewSet,
                base_name='atlas_specis_download_down')
router.register(r'atlas_name_download_down', views.AtalsnameDownViewSet,
                base_name='atlas_name_download_down')

router.register(r'cell_specie_download_down', views.CellSpecieDownViewSet,
                base_name='cell_specie_download_down')
router.register(r'cell_tissue_download_down', views.CellTissueDownViewSet,
                base_name='cell_tissue_download_down')
############################################################新增810
router.register(r'cluster_marker_specie_download_down', views.ClusterMarkerDownViewSet,
                base_name='cluster_marker_specie_download_down')
router.register(r'cluster_marker_tissue_download_down', views.ClusterMarkerTissueDownViewSet,
                base_name='cluster_marker_tissue_download_down')
########################################################
# Cross-species gene expression
router.register(r'cross_specie_expression', views.CrossSpecieExpressionViewSet,
                base_name='cross_specie_expression')
# gene
router.register(r'cross_specie_gene_expression', views.CrossSpecieGeneExpressionViewSet,
                base_name='cross_specie_gene_expression')
# 物种和目标物种的小提琴图
router.register(r'cross_specie_violin_box_plot', views.CrossSpecieViolinBoxPlotViewSet,
                base_name='cross_specie_violin_box_plot')
# 物种下拉框
router.register(r'cross_specie_name_down', views.CrossSpecieNameDownViewSet,
                base_name='cross_specie_name_down')
# 物种下拉框
router.register(r'cross_reference_specie_down', views.CrossReferenceSpecieDownViewSet,
                base_name='cross_specie_down')
# 物种gene下拉框
router.register(r'cross_specie_gene_down', views.CrossSpecieGeneDownViewSet,
                base_name='cross_specie_gene_down')
#####################################
# 文件上传接口
router.register(r'cross_species_annotation_upload', views.CrossSpeciesAnnotationUploadViewSet,
                base_name='cross_species_annotation_upload')
# csv数据生成接口
router.register(r'cell_identification_csv', views.CellIdentificationCsvViewSet,
                base_name='cell_identification_csv')
###############Cell-Cell interactions
# png展示
router.register(r'cell_iteraction_png', views.CellInteractionPngViewSet,
                base_name='cell_iteraction_png')
# Ligands和Receptors
router.register(r'cell_interactions_ligands_receptors_down', views.CrossInteractionsLigandsReceptorsDownViewSet,
                base_name='cell_interactions_ligands_receptors_down')
# Ligands和Receptors筛选柱状图接口
router.register(r'interactions_ligands_receptors_histogram', views.CrossInteractionsLigandsReceptorsHistogramViewSet,
                base_name='interactions_ligands_receptors_histogram')
# Ligands和Receptors筛选列表页接口
router.register(r'interactions_ligands_receptors_list', views.CrossInteractionsLigandsReceptorsListViewSet,
                base_name='interactions_ligands_receptors_list')
# 列表分页
router.register(r'cell_iteraction_csv_list', views.CellInteractionCsvListViewSet,
                base_name='cell_iteraction_csv_list')
router.register(r'cross_reference_species_down', views.CrossReferenceSpeciesDownViewSet,
                base_name='cross_reference_species_down')
#########2023-05-22 柱状图统计的是表里面符合条件的各类型基因数量
router.register(r'cell_histogram_png', views.CellHistogramPngViewSet,
                base_name='cell_histogram_png')

# Cell-Cell interactions散点图
router.register(r'cell_iteraction_gene_expression', views.CellInteractionSpecieGeneExpressionViewSet,
                base_name='cell_iteraction_gene_expression')
# Ligands和Receptors Gene_id下拉框接口
router.register(r'cell_interactions_ligands_receptors_gene_down',
                views.CrossInteractionsLigandsReceptorsGeneDownViewSet,
                base_name='cell_interactions_ligands_receptors_gene_down')
# txt下载
router.register(r'cell_iteraction_txt', views.CellInteractionTxtDownloadViewSet,
                base_name='cell_iteraction_txt')
# lr_pair下拉框
router.register(r'cross_lr_pair_gene_down', views.CrossLrPairGeneDownViewSet,
                base_name='cross_lr_pair_gene_down')
# 新增cellType下拉框接口

router.register(r'interaction_cell_type', views.InteractionCellTypeViewSet,
                base_name='interaction_cell_type')

# Cell-Cell interactions species_down下拉框
router.register(r'cell_iteraction_species_down', views.CellInteractionSpeciesDownViewSet,
                base_name='cell_iteraction_species_down')
# species_tissue下拉框
router.register(r'cell_iteraction_species_tissue_down', views.CellInteractionSpeciesTissueDownViewSet,
                base_name='cell_iteraction_species_tissue_down')
# #首页Update log
router.register(r'home_update_logs', views.HomeUpdateLogsViewSet,
                base_name='home_update_logs')

router.register(r'home_atlas_static', views.HomeAtlasStaticViewSet,
                base_name='home_atlas_static')
# Atlas gene_id 下载接口
router.register(r'atlas_gene_id_download', views.AtlasGeneDonloadViewSet,
                base_name='atlas_gene_id_download')
# Atlas 箱图接口2023-4-24
router.register(r'atlas_total_mean_count', views.AtlasTotalMeanCountViewSet,
                base_name='atlas_total_mean_count')
# 2023-05-22示例下载
# Integration zip下载脚本接口
router.register(r'cell_identification_csv_download', views.CellIdentificationCsvDownloadViewSet,
                base_name='cell_identification_csv_download')

# 2023-06-17 Atlas Download下载rds文件
router.register(r'cell_atlas_download', views.CellAtlasRdsDownloadViewSet,
                base_name='cell_atlas_download')

# 2023-06-17 Atlas详情箱图数据
router.register(r'cell_atlas_detail_diagram_map', views.CellAtlasDetailDiagramMapViewSet,
                base_name='cell_atlas_detail_diagram_map')
# 202232-07-15Atlas
router.register(r'cell_atlas_gene_symbol_download', views.CellAtlasGeneSymbolDownloadViewSet,
                base_name='cell_atlas_gene_symbol_download')
# 2024-01-04
# gene_id统计计数接口
router.register(r'classic_markers_info_count', views.ClassicMarkersInfoCountGene, base_name='classic_markers_info_count')

# 2024-01-02 Browse页面 Project information列表
router.register(r'sra_information_list', views.SraInformationViewSet, base_name='sra_information_list')
# 2024-01-03 Markker页面 下拉框数据
router.register(r'marker_list', views.MarkerViewSet, base_name='marker_list')
# 2024-01-04 菜单栏下拉框数据
router.register(r'menu_select_list', views.MenuViewSet, base_name='menu_select_list')
# 2024-01-08 菜单栏搜索结果列表数据
router.register(r'menu_search_list', views.MenuSearchViewSet, base_name='menu_search_list')
# 2024-01-04 Marker页面 树状图数据
router.register(r'marker_tree_data_list', views.MarkerTreeDataViewSet, base_name='marker_tree_data_list')
# 2024-01-08 Marker Details 筛选条件接口
router.register(r'marker_details_search_data', views.MarkerDetailsSearchData, base_name='marker_details_search_data')
# 2024-01-04 Marker页面点击树状图节点右侧列表部分Summary列表数据接口
router.register(r'marker_details_list', views.MarkerDetailsListViewSet, base_name='marker_details_list')
# 2024-01-04 Marker页面点击树状图节点右侧列表部分Details列表数据接口
router.register(r'marker_summary_list', views.MarkerSummaryListViewSet, base_name='marker_summary_list')
# 2024-01-08 Marker页面点击树状图一级节点的柱状图接口
router.register(r'marker_histogram_list', views.MarkerHistogramViewSet, base_name='marker_histogram_list')
# 2023-01-16 基因详情页面接口
router.register(r'gene_details_info', views.GeneDetailsInfoViewSet, base_name='gene_details_info')
# 2024-01-09 Search页面 通过细胞类型搜索项---下拉框三级联动数据
router.register(r'search_cell_select_data', views.SearchCellSelectViewSet, base_name='search_cell_select_data')

# 2024-01-06 marker页面 词云图数据。
router.register(r'marker_word_data', views.WordCloudViewSet, base_name='marker_word_data')
# 2024-01-06 marker页面 树状图子节点信息数据
router.register(r'marker_node_desc', views.NodeDesViewSet, base_name='marker_node_desc')

# 2024-01-16 Search页面-By marker gene-搜索结果列表
router.register(r'search_marker_gene_table', views.SearchMarkerGeneTable, base_name='search_marker_gene_table')
# 2024-01-16 Search页面-By cell type-搜索结果列表
router.register(r'search_cell_type_table', views.SearchCellTypeTable, base_name='search_cell_type_table')
# 2024-01-31 Search页面-blast数据
router.register(r'blast_data', views.BlastData, base_name='blast_data')
# 2024-02-01 Search页面-blast下拉框数据
router.register(r'blast_list', views.BlastList, base_name='blast_list')

# 调用浙大接口
router.register(r'get_cell_blast_data', views.GetCellBlastData, base_name='get_cell_blast_data')
router.register(r'get_cell_id_data', views.GetCellIdData, base_name='get_cell_id_data')
router.register(r'get_mtsc_data', views.GetMtscData, base_name='get_mtsc_data')

router.register(r'get_train_species', views.GetTrainSpeciesList, base_name='get_train_species')
router.register(r'get_train_tissue', views.GetTrainTissueList, base_name='get_train_tissue')