import axios from './analysisHttp.js';
import qs from 'qs'
let baseUrl = '';

// analysisFromCellranger页面 ----------------------------------------------------------------------------
// analysis分析列表页接口
export const analysisCellrangerList = params => {
    return axios.get(`${baseUrl}/v1/analysis/`, {
        params: params
    })
}
// -----------------------------------------第一步----------------------------
// cellRanger  # analysis New Job接口
export const analysis_new_job = (params) => {
    const param = qs.stringify(params) //序列化post 参数
    return axios.post(`${baseUrl}/v1/analysis_new_job/`, {
        data: param
    })
}
// cellRanger  大文件上传
export const analysis_file_upload = params => {
    return axios.get(`${baseUrl}/v1/analysis_file_upload/`, {
        params: params
    })
}
// cellRanger  # analysis物种和转录组下拉框接口
export const specie_down_box = params => {
    return axios.get(`${baseUrl}/v1/specie_down_box/`, {
        params: params
    })
}
// cellRanger  # analysis组织下拉框接口
export const specie_tissue_down_box = params => {
    return axios.get(`${baseUrl}/v1/specie_tissue_down_box/`, {
        params: params
    })
}
// cellRanger  analysis分析接口
export const analysisCellranger = (params) => {
    const param = qs.stringify(params) //序列化post 参数
    return axios.post(`${baseUrl}/v1/analysis/cellranger/`, {
        data: param
    })
}
// # analysis分析详情页接口
export const analysisInfo = params => {
    return axios.get(`${baseUrl}/v1/analysis/${params}/`)
}
// # analysis删除接口
export const analysisDelete = params => {
    return axios.delete(`${baseUrl}/v1/analysis/${params}/`)
}
// cellRanger  第一步cellranger gz文件下载和展示接口
export const analysis_file_download = params => {
    return axios.get(`${baseUrl}/v1/analysis_file_download/`, {
        params: params
    })
}
// # analysis删除上传文件
export const upload_file_delete = params => {
    return axios.get(`${baseUrl}/v1/upload_file_delete/`, {
        params: params
    })
}

// ---------------------------------第二步-------------------------------
// Samlpe QC mt  pt 默认数据
export const sample_qc_pt_mt = params => {
    return axios.get(`${baseUrl}/v1/sample_qc_pt_mt/`, {
        params: params
    })
}
// Samlpe QC表格数据接口
export const sqmple_qc_data_show = params => {
    return axios.get(`${baseUrl}/v1/sqmple_qc_data_show/`, {
        params: params
    })
}
//  QC Filter表格数据接口
export const qc_filter_data_show = params => {
    return axios.get(`${baseUrl}/v1/qc_filter_data_show/`, {
        params: params
    })
}
// Run QC
export const sample_qc = (params) => {
    const param = qs.stringify(params) //序列化post 参数
    return axios.post(`${baseUrl}/v1/analysis/sample_qc/`, {
        data: param
    })
}
//  analysis QC Filter小提琴图和点图展示数据接口
export const qc_filter_data_result = params => {
    return axios.get(`${baseUrl}/v1/qc_filter_data_result/`, {
        params: params
    })
}
// ---------------------------------第三步-------------------------------
//  获取默认值
export const data_process_show = params => {
    return axios.get(`${baseUrl}/v1/data_process_show/`, {
        params: params
    })
}
// Run data process接口
export const data_process = (params) => {
    const param = qs.stringify(params) //序列化post 参数
    return axios.post(`${baseUrl}/v1/analysis/data_process/`, {
        data: param
    })
}
//  data process结果展示接口
export const data_process_result = params => {
    return axios.get(`${baseUrl}/v1/data_process_result/`, {
        params: params
    })
}
// ---------------------------------第四步-------------------------------
//  获取默认值
export const cluster_resolution = params => {
    return axios.get(`${baseUrl}/v1/cluster_resolution/`, {
        params: params
    })
}
// Run cluster接口
export const cluster = (params) => {
    const param = qs.stringify(params) //序列化post 参数
    return axios.post(`${baseUrl}/v1/analysis/cluster/`, {
        data: param
    })
}
//  cluster结果展示接口
export const cluster_result = params => {
    return axios.get(`${baseUrl}/v1/cluster_result/`, {
        params: params
    })
}
// ---------------------------------第五步-------------------------------
//  CellAnnotation  结果展示接口
export const cell_annotation_result = params => {
    return axios.get(`${baseUrl}/v1/cell_annotation_result/`, {
        params: params
    })
}
//  CellAnnotation  表格展示接口
export const cluster_result_list = params => {
    return axios.get(`${baseUrl}/v1/cluster_result_list/`, {
        params: params
    })
}

// ---------------------------------第二个流程-------------------------------
//  analysis Samlpe QC表格数据接口
export const sqmpleQcDataShow = params => {
    return axios.get(`${baseUrl}/v1/sqmple_qc_data_show/`, {
        params: params
    })
}
//  analysis Samlpe QC 回显详细信息
export const sample_qc_upload_show = params => {
    return axios.get(`${baseUrl}/v1/sample_qc_upload_show/`, {
        params: params
    })
}

//  run之后获取进度条进度
export const analysis_step_progress = params => {
    return axios.get(`${baseUrl}/v1/analysis_step_progress/`, {
        params: params
    })
}
//  # sample_qc 一键生成 接口
export const from_sample_qc_one_step = (params) => {
    const param = qs.stringify(params) //序列化post 参数
    return axios.post(`${baseUrl}/v1/analysis/from_sample_qc_one_step/`, {
        data: param
    })
}
//  # cellranger 一键生成 接口
export const from_cell_ranger_one_step = params => {
    const param = qs.stringify(params) //序列化post 参数
    return axios.post(`${baseUrl}/v1/analysis/from_cell_ranger_one_step/`, {
        data: param
    })
}