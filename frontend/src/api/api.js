import axios from "./http";
import qs from "qs";
import Axios from "axios";
let baseUrl = "";

// 首页 home----------------------------------------------------------------------------
// umap expression接口
export const umap_expression = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_home_umap/umap_dataset/`, {
        params: params,
    });
};
export const home_umap_polt = (params) => {
    return axios.get(`${baseUrl}/api/v1/home_umap_polt/`, {
        params: params,
    });
};
// atlas  tsne_umap_dataset
export const tsne_umap_dataset = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_home_umap/tsne_umap_dataset/`, {
        params: params,
    });
};
// 首页Atlas物种组织cell和sample统计接口
export const atlas_tissue_cell_sample_count = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_home_umap/atlas_tissue_cell_sample_count/`, {
        params: params,
    });
};
//  首页下面 statistics 统计接口
export const species_relation_statistics = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_home_umap/species_relation_statistics/`, {
        params: params,
    });
};
// 搜索结果页面 atlas----------------------------------------------------------------------------
export const plant_atlas_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_atlas_list/`, {
        params: params,
    });
};
export const cell_atlas_download = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_atlas_download/`, {
        params: params,
    });
};
// search 页面---------------------------------------------
// Search物种下拉框接口
export const plant_search_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_search_down/`, {
        params: params,
    });
};
// Search Tissue组织下拉框接口
export const tissue_type_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_search_down/tissue_type_down/`, {
        params: params,
    });
};
// Search Project_ID下拉框接口
export const project_id_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_search_down/project_id_down/`, {
        params: params,
    });
};
// Search sample_id_down下拉框接口
export const sample_id_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_search_down/sample_id_down/`, {
        params: params,
    });
};
// Search Cluster_Name下拉框接口
export const cluster_name_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_search_down/cluster_name_down/`, {
        params: params,
    });
};
// Search Cluster_Marker下拉框接口
export const cluster_marker_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_search_down/cluster_marker_down/`, {
        params: params,
    });
};
// Search Cell_ID下拉框接口
export const cell_id_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_search_down/cell_id_down/`, {
        params: params,
    });
};
// Search Gene_Symbol下拉框接口
export const gene_symbol_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_search_down/gene_symbol_down/`, {
        params: params,
    });
};
// 需求变更  新增下拉框接口
// Search Sample_Name下拉框接口
export const sample_name_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_search_down/sample_name_down/`, {
        params: params,
    });
};
// Search Process_Status下拉框接口
export const process_status_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_search_down/process_status_down/`, {
        params: params,
    });
};

// ## Project 导航栏下拉框接口
export const project_lit_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/project_atlas_list/project_lit_down/`, {
        params: params,
    });
};
//  Project  umap接口
export const project_umap_dataset = (params) => {
    return axios.get(`${baseUrl}/api/v1/project_atlas_list/project_umap_dataset/`, {
        params: params,
    });
};
// Project  CellType列表页接口
export const project_atlas_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/project_atlas_list/`, {
        params: params,
    });
};
// Project  Marker列表页接口
export const cluster_marker = (params) => {
    return axios.get(`${baseUrl}/api/v1/project_atlas_list/cluster_marker/`, {
        params: params,
    });
};
// Project  Sample列表页接口
export const sample_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/project_atlas_list/sample_list/`, {
        params: params,
    });
};
// GeneExpression ------------------------------
// 物种下拉框接口
export const gene_expression_species_name = (params) => {
    return axios.get(`${baseUrl}/api/v1/gene_express_umap/gene_expression_species_name/`, {
        params: params,
    });
};
// 物种reference下拉框接口
export const cross_reference_specie_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/cross_reference_specie_down/`, {
        params: params,
    });
};
// 组织下拉框接口
export const gene_expression_tissue = (params) => {
    return axios.get(`${baseUrl}/api/v1/gene_express_umap/gene_expression_tissue/`, {
        params: params,
    });
};
// GeneExpression  gene_id下拉框接口
// export const gene_id_express_down = params => {
//     return axios.get(`${baseUrl}/api/v1/plant_search_down/gene_id_express_down/`, {
//         params: params
//     })
// }
export const cross_specie_gene_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/cross_specie_gene_down/`, {
        params: params,
    });
};
// GeneExpression  图形接口
// export const gene_express_umap = params => {
//     return axios.get(`${baseUrl}/api/v1/gene_express_umap/`, {
//         params: params
//     })
// }
// # 物种和对比目标物种组织的表达值图
export const cross_specie_expression = (params) => {
    return axios.get(`${baseUrl}/api/v1/cross_specie_expression/`, {
        params: params,
    });
};
//  物种和对比目标物种gene的表达值图
export const cross_specie_gene_expression = (params) => {
    return axios.get(`${baseUrl}/api/v1/cross_specie_gene_expression/`, {
        params: params,
    });
};
//  物种和对比目标物种gene的小提琴图接口
export const cross_specie_violin_box_plot = (params) => {
    return axios.get(`${baseUrl}/api/v1/cross_specie_violin_box_plot/`, {
        params: params,
    });
};

// searchList ------------------------------
// Search Sample列表页接口
export const sample_plant_search = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_search/`, {
        params: params,
    });
};
// Search  ClusterMarker列表页接口
export const search_cluster_marker = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_search/search_cluster_marker/`, {
        params: params,
    });
};
// Search  CellMarker列表页接口
export const search_cell_marker = (params) => {
    return axios.get(`${baseUrl}/api/v1/plant_search/search_cell_marker/`, {
        params: params,
    });
};
// ---------------------  sample_QC 页面--------------------------------------------------
// Sample_QC获取UUID文件名接口
export const sample_qc_uuid = (params) => {
    return axios.get(`${baseUrl}/api/v1/sample_qc_upload/sample_qc_uuid/`, {
        params: params,
    });
};
//  Sample_QC  功能展示接口
export const sample_qc_upload = (params) => {
    return axios.get(`${baseUrl}/api/v1/sample_qc_upload/`, {
        params: params,
    });
};
//  Sample_QC  文件上传接口
export const sample_qc_upload_picture = (params) => {
    return axios.get(`${baseUrl}/api/v1/sample_qc_upload_picture/`, {
        params: params,
    });
};

// Integration SVG图片生成和RDS文件下载接口
export const integration_svg_show = (params) => {
    return axios.get(`${baseUrl}/api/v1/integration_svg_show/`, {
        params: params,
    });
};
// Integration Example动态生成 SVG图片
export const integration_example_svg_show = (params) => {
    return axios.get(`${baseUrl}/api/v1/integration_example_svg_show/`, {
        params: params,
    });
};
//  Integration Download csv 下载接口
export const integration_download = (params) => {
    return axios.get(`${baseUrl}/api/v1/integration_download/`, {
        params: params,
    });
};
// 0721优化后相关接口-------------------------
//  Integration详情 展示示例图片接口
export const integration_example_show = (params) => {
    return axios.get(`${baseUrl}/api/v1/integration_example_show/`, {
        params: params,
    });
};
//  Integration详情 脚本zip下载接口
export const integration_zip_download = (params) => {
    return axios.get(`${baseUrl}/api/v1/integration_zip_download/`, {
        params: params,
    });
};

// -------------------------CellIdentification 页面---------------------------------------------
// CellIdentificationSpecies物种下拉框接口
export const cell_identification_species_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_species_down/`, {
        params: params,
    });
};
//  CellIdentificationTissue组织下拉框接口
export const cell_tissue_type_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_species_down/tissue_type_down/`, {
        params: params,
    });
};
//  CellIdentification RDS文件上传接口
export const cell_identification_upload = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_upload/`, {
        params: params,
    });
};
//  CellIdentification SVG展示和三种格式图片下载接口
export const cell_identification_svg_show = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_svg_show/`, {
        params: params,
    });
};
//  CellIdentification Example SVG展示和三种格式图片下载接口
export const cell_identification_example_svg_show = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_example_svg_show/`, {
        params: params,
    });
};
// -------------------------CellIdentification 页面  2022-9-21 新页面
//  CellIdentification Refrence  图片标题接口
export const cell_identification_pdf_title = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_pdf_title/`, {
        params: params,
    });
};
//  CellIdentification Refrence  详情接口
export const cell_identification_reference_detail = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_reference_detail/`, {
        params: params,
    });
};
//  CellIdentification Refrence   Sample列表页接口
export const cell_identification_reference_sample = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_reference_sample/`, {
        params: params,
    });
};
// ## CellIdentification submit提交接口
export const cell_identification_create_csv = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_create_csv/`, {
        params: params,
    });
};
//  ## CellIdentification  Cell_type列表页接口
export const cell_identification_cell_type_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_cell_type_list/`, {
        params: params,
    });
};
// ## CellIdentification  Cors_matrix列表页接口
export const cell_identification_cors_matrix_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_cors_matrix_list/`, {
        params: params,
    });
};
// ## CellIdentification 下载接口
export const cell_identification_csv_zip_download = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_csv_zip_download/`, {
        params: params,
    });
};
// ## CellIdentification 下载接口
export const cell_identification_cell_type_map = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_cell_type_map/`, {
        params: params,
    });
};
export const cell_identification_csv_download = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_csv_download/`, {
        params: params,
    });
};

// ## Filter submit提交接口
export const cell_identification_filter_csv = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_filter_csv/`, {
        params: params,
    });
};
// -------------------------cellAnnotationResult 页面  2023-4-11 新页面
// ##   生成进入详情提供下载和列表的文件接口
export const cell_identification_csv = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_identification_csv/`, {
        params: params,
    });
};
//Cross-species cell annotation动态返回组织接口
export const cross_reference_species_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/cross_reference_species_down/`, {
        params: params,
    });
};

// 首页 Browse----------------------------------------------------------------------------
// Browse Statistics饼图接口
export const cell_browse_statistics = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_browse_statistics/`, {
        params: params,
    });
};
// ## Browse列表页接口
export const browse_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/browse_list/`, {
        params: params,
    });
};
// ## QC Filter下面物种组织下拉框接口----------------------------------------------------------------------------

export const cell_species_tissues = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_species_tissues/`, {
        params: params,
    });
};
// ## 柱状图和热力图接口
export const expressed_gene_cell_type_count = (params) => {
    return axios.get(`${baseUrl}/api/v1/expressed_gene_cell_type_count/`, {
        params: params,
    });
};

// ## 手风琴和箱图接口
export const expressed_gene_violin_box_plot = (params) => {
    return axios.get(`${baseUrl}/api/v1/expressed_gene_violin_box_plot/`, {
        params: params,
    });
};
// ## umap散点图接口
export const expressed_gene_umap_dataset = (params) => {
    return axios.get(`${baseUrl}/api/v1/expressed_gene_umap_dataset/`, {
        params: params,
    });
};

// ## Tissue structure接口
export const tissue_structure = (params) => {
    return axios.get(`${baseUrl}/api/v1/tissue_structure/`, {
        params: params,
    });
};
// ## reference_cell_type_list接口
export const reference_cell_type_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/reference_cell_type_list/`, {
        params: params,
    });
};
// ## efp接口
export const species_efp = (params) => {
    return axios.get(`${baseUrl}/api/v1/species_efp/`, {
        params: params,
    });
};

// ## atlas  热力图和柱状图接口
export const atlas_expressed_gene_cell_type_count = (params) => {
    return axios.get(`${baseUrl}/api/v1/atlas_expressed_gene_cell_type_count/`, {
        params: params,
    });
};
// ## atlas  手风琴接口
export const atlas_expressed_gene_violin_box_plot = (params) => {
    return axios.get(`${baseUrl}/api/v1/atlas_expressed_gene_violin_box_plot/`, {
        params: params,
    });
};
// ## Atlas详情最上面新增的柱状图接口
export const atlas_gene_cell_type_count = (params) => {
    return axios.get(`${baseUrl}/api/v1/atlas_gene_cell_type_count/`, {
        params: params,
    });
};
// ## Atlas箱图接口
export const atlas_total_mean_count = (params) => {
    return axios.get(`${baseUrl}/api/v1/atlas_total_mean_count/`, {
        params: params,
    });
};
export const cell_atlas_detail_diagram_map = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_atlas_detail_diagram_map/`, {
        params: params,
    });
};
// 获取geni列表
export const cell_atlas_gene_symbol_download = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_atlas_gene_symbol_download/`, {
        params: params,
    });
};

// 获取geni列表
export const sra_information_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/sra_information_list/`, {
        params: params,
    });
};

export const information_drop_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/sra_information_list/information_drop_down/`, {
        params: params,
    });
};

// monocle页面接口-----------------------------------------

// ## species下拉框
export const species_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/species_down/`, {
        params: params,
    });
};
// ## Tissue下拉框
export const species_tissue_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/species_tissue_down/`, {
        params: params,
    });
};
// ## CellType下拉框
export const species_cell_type_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/species_cell_type_down/`, {
        params: params,
    });
};
// ## EXPRESSION 列表接口
export const monocle_expressed_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/monocle_expressed_list/`, {
        params: params,
    });
};
// ##Heatmap列表接口
export const monocle_heatmap_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/monocle_heatmap_list/`, {
        params: params,
    });
};
// EXPRESSION 基因下拉框
export const monocle_expressed_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/monocle_expressed_down/`, {
        params: params,
    });
};
// Heatmap基因下拉框
export const monocle_heatmap_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/monocle_heatmap_down/`, {
        params: params,
    });
};

//  EXPRESSION 图
export const monocle_expressed_png = (params) => {
    return axios.get(`${baseUrl}/api/v1/monocle_expressed_png/`, {
        params: params,
    });
};
//  Heatmap 图
export const monocle_heatmap_png = (params) => {
    return axios.get(`${baseUrl}/api/v1/monocle_heatmap_png/`, {
        params: params,
    });
};
// monocle 最上面的图
export const monocle_heat_png = (params) => {
    return axios.get(`${baseUrl}/api/v1/monocle_heat_png/`, {
        params: params,
    });
};

// 国旗
export const cell_country_visiter = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_country_visiter/`, {
        params: params,
    });
};
// 物种组织部位统计
export const cell_home_specie_tissue_count = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_home_specie_tissue_count/`, {
        params: params,
    });
};
// 首页所有物种
export const specie_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_browse_cell_type_count/specie_list/`, {
        params: params,
    });
};

// 中间组织统计接口
export const home_count = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_browse_cell_type_count/home_count/`, {
        params: params,
    });
};
// 首页底部日志接口
// export const home_update_logs = params => {
//     return axios.get(`${baseUrl}/api/v1/cell_browse_cell_type_count/home_update_logs/`, {
//         params: params
//     })
// }
export const home_update_logs = (params) => {
    return axios.get(`${baseUrl}/api/v1/home_update_logs/`, {
        params: params,
    });
};
// 日志详情页
export const home_update_logs_detail = (params) => {
    return axios.get(`${baseUrl}/api/v1/home_update_logs/${params}/`);
};

// 首页 Download----------------------------------------------------------------------------
// 物种下拉框
export const atlas_specis_download_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/atlas_specis_download_down/`, {
        params: params,
    });
};
// Atlas name下拉框
export const atlas_name_download_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/atlas_name_download_down/`, {
        params: params,
    });
};
// CellMarker ClusterMarker物种下拉框
export const cell_specie_download_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_specie_download_down/`, {
        params: params,
    });
};
// 组织下拉框
export const cell_tissue_download_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_tissue_download_down/`, {
        params: params,
    });
};
// 文件名下拉框
export const cell_download = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_download/`, {
        params: params,
    });
};
// Atlas列表页接口
export const atlas_download_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/atlas_download_list/`, {
        params: params,
    });
};
// Atlas下载接口
export const atlas_download = (params) => {
    return axios.get(`${baseUrl}/api/v1/atlas_download/`, {
        params: params,
    });
};
// CellMarker列表页接口
export const cell_marker_download_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_marker_download_list/`, {
        params: params,
    });
};
// CellMarker下载接口
export const cell_marker_download = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_marker_download/`, {
        params: params,
    });
};
// CellCluster列表页接口
export const cell_cluster_download_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_cluster_download_list/`, {
        params: params,
    });
};
// ClusterMarker下载接口
export const cell_cluster_download = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_cluster_download/`, {
        params: params,
    });
};

// tools----------------------------------------------------------------------------
// query specie 下拉框
export const query_specie_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_browse_cell_type_count/query_specie_list/`, {
        params: params,
    });
};
// tissue_type下拉框
export const tissue_type_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_browse_cell_type_count/tissue_type_list/`, {
        params: params,
    });
};
// 列表页
export const cell_search_cmpredictor = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_search_cmpredictor/`, {
        params: params,
    });
};
// tools  Cell-Cell interactions----------------------------------------------------------------------------
// 十二个物种(geneExpression页面的)
export const cross_specie_name_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/cross_specie_name_down/`, {
        params: params,
    });
};
// Cell-Cell interactions物种下拉框接口
export const cell_iteraction_species_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_iteraction_species_down/`, {
        params: params,
    });
};
// Cell-Cell interactions组织下拉框接口
export const cell_iteraction_species_tissue_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_iteraction_species_tissue_down/`, {
        params: params,
    });
};
// Cell-Cell interactions三个图展示接口
export const cell_iteraction_png = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_iteraction_png/`, {
        params: params,
    });
};
// Cell-Cell interactions列表页接口
export const cell_iteraction_csv_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_iteraction_csv_list/`, {
        params: params,
    });
};
export const interactions_ligands_receptors_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/interactions_ligands_receptors_list/`, {
        params: params,
    });
};
// Tool的Cell-Cell interactions三个散点图的下拉框接口（填充一个基因接口后请求这个接口展示下拉列表）
export const cell_interactions_ligands_receptors_gene_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_interactions_ligands_receptors_gene_down/`, {
        params: params,
    });
};
// 新页面Cell-Cell interactions lr_pair下拉框接口
export const cross_lr_pair_gene_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/cross_lr_pair_gene_down/`, {
        params: params,
    });
};
// 新页面Cell-Cell interactions 新增cellType下拉框接口
export const interaction_cell_type = (params) => {
    return axios.get(`${baseUrl}/api/v1/interaction_cell_type/`, {
        params: params,
    });
};
export const cell_interactions_ligands_receptors_down = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_interactions_ligands_receptors_down/`, {
        params: params,
    });
};
//  新页面Cell-Cell interactions获取柱形图
export const interactions_ligands_receptors_histogram = (params) => {
    return axios.get(`${baseUrl}/api/v1/interactions_ligands_receptors_histogram/`, {
        params: params,
    });
};
//  新页面Cell-Cell interactions 三个umap散点图接口
export const cell_iteraction_gene_expression = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_iteraction_gene_expression/`, {
        params: params,
    });
};
//  Cell-Cell interactionsTXT下载接口
export const cell_iteraction_txt = (params) => {
    return axios.get(`${baseUrl}/api/v1/cell_iteraction_txt/`, {
        params: params,
    });
};

// 育种大数据登录接口
export const login = (params) => {
    const param = qs.stringify(params); //序列化post 参数
    return axios.post(`${baseUrl}/api/v1/account/login/`, {
        data: param,
    });
};

export const menu_select_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/menu_select_list`, {
        params: params,
    });
};

// ! marker

// marker 页面  下拉框
export const marker_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/marker_list`, {
        params: params,
    });
};

// marker 页面  树状结构
export const marker_tree_data_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/marker_tree_data_list`, {
        params: params,
    });
};

// marker 页面  柱状图
export const marker_histogram_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/marker_histogram_list`, {
        params: params,
    });
};

// marker 页面  头部展示信息
export const marker_node_desc = (params) => {
    return axios.get(`${baseUrl}/api/v1/marker_node_desc`, {
        params: params,
    });
};

// marker 页面  词云
export const marker_word_data = (params) => {
    return axios.get(`${baseUrl}/api/v1/marker_word_data`, {
        params: params,
    });
};

// Marker Table Summary列表数据接口
export const marker_summary_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/marker_summary_list`, {
        params: params,
    });
};

// Marker Table Summary列表CSV文件下载接口
export const marker_summary_download = (params) => {
    return axios.get(`${baseUrl}/api/v1/marker_summary_list/marker_summary_download`, {
        params: params,
    });
};

// 八、Marker Table Details列表筛选条件数据接口
export const marker_details_search_data = (params) => {
    return axios.get(`${baseUrl}/api/v1/marker_details_search_data`, {
        params: params,
    });
};

// 九、Marker Table Details列表数据接口
export const marker_details_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/marker_details_list`, {
        params: params,
    });
};

// 十、Marker Table Details列表 CSV下载接口
export const marker_details_download = (params) => {
    return axios.get(`${baseUrl}/api/v1/marker_details_list/marker_details_download`, {
        params: params,
    });
};

// 搜素
export const menu_search_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/menu_search_list`, {
        params: params,
    });
};

// 二、By cell type下拉框数据接口
export const search_cell_select_data = (params) => {
    return axios.get(`${baseUrl}/api/v1/search_cell_select_data`, {
        params: params,
    });
};

// // 二、By cell type下拉框数据接口
export const search_word_cloud_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/marker_word_data/search_word_cloud_list`, {
        params: params,
    });
};

export const search_marker_gene_table = (params) => {
    return axios.get(`${baseUrl}/api/v1/search_marker_gene_table`, {
        params: params,
    });
};

export const search_cell_type_table = (params) => {
    return axios.get(`${baseUrl}/api/v1/search_cell_type_table`, {
        params: params,
    });
};

export const gene_details_info = (params) => {
    return axios.get(`${baseUrl}/api/v1/gene_details_info`, {
        params: params,
    });
};

export const gene_details_cell_type = (params) => {
    return axios.get(`${baseUrl}/api/v1/gene_details_info/gene_details_cell_type`, {
        params: params,
    });
};

export const blast_list = (params) => {
    return axios.get(`${baseUrl}/api/v1/blast_list`, {
        params: params,
    });
};

// export const blast_data = (params) => {
//     return axios.get(`${baseUrl}/api/v1/blast_data`, {
//         params: params
//     })
// }

export const blast_data = (formData) => {
    let config = {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    };
    return Axios.post(`${process.env.VUE_APP_BASE_URL}/api/v1/blast_data/`, formData, config);
    // return Axios.post(`https://www.tobaccodb.org/server_pcmdb/api/v1/blast_data/`, formData, config)
};

export const get_train_species = (params) => {
    return axios.get(`${baseUrl}/api/v1/get_train_species/`, {
        params: params,
    });
};

export const get_train_tissue = (params) => {
    return axios.get(`${baseUrl}/api/v1/get_train_tissue/`, {
        params: params,
    });
};

export const get_cell_id_data = (formData) => {
    let config = {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    };
    return Axios.post(`${process.env.VUE_APP_BASE_URL}/api/v1/get_cell_id_data/`, formData, config);
    // return Axios.post(`https://www.tobaccodb.org/server_pcmdb/api/v1/blast_data/`, formData, config)
};

export const cell_id_example = (params) => {
    return axios.get(`${baseUrl}/api/v1/get_cell_id_data/cell_id_example`, {
        params: params,
    });
};

export const mtsc_example = (params) => {
    return axios.get(`${baseUrl}/api/v1/get_mtsc_data/mtsc_example/`, {
        params: params,
    });
};

export const cell_blast_example = (params) => {
    return axios.get(`${baseUrl}/api/v1/get_cell_blast_data/cell_blast_example/`, {
        params: params,
    });
};

export const get_cell_blast_hits = (params) => {
    return axios.get(`${baseUrl}/api/v1/get_cell_blast_data/get_cell_blast_hits/`, {
        params: params,
    });
};

export const get_cell_blast_predictions = (params) => {
    return axios.get(`${baseUrl}/api/v1/get_cell_blast_data/get_cell_blast_predictions/`, {
        params: params,
    });
};

export const get_mtsc_data = (formData) => {
    let config = {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    };
    return Axios.post(`${process.env.VUE_APP_BASE_URL}/api/v1/get_mtsc_data/`, formData, config);
    // return Axios.post(`https://www.tobaccodb.org/server_pcmdb/api/v1/blast_data/`, formData, config)
};

export const get_cell_blast_data = (formData) => {
    let config = {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    };
    return Axios.post(`${process.env.VUE_APP_BASE_URL}/api/v1/get_cell_blast_data/`, formData, config);
    // return Axios.post(`https://www.tobaccodb.org/server_pcmdb/api/v1/blast_data/`, formData, config)
};
