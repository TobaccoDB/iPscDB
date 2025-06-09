import axios from './http';
import qs from 'qs'
let baseUrl = '';

// search页面 ----------------------------------------------------------------------------
// tissue_type下拉框
export const cell_search_down = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search_down/`, {
        params: params
    })
}
// cell_type下拉框
export const cell_type_down = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search_down/cell_type_down/`, {
        params: params
    })
}
// cell_marker_name下拉框
// export const cell_marker_name_down = params => {
//     return axios.get(`${baseUrl}/api/v1/cell_search_down/cell_marker_name_down`, { params: params })
// }

// search关键字检索接口
export const cell_search = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search/`, {
        params: params
    })
}
// Search_by_Marker
export const cell_search_marker = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search/cell_search_marker/`, {
        params: params
    })
}
// serach_marker
export const search_marker = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search/search_marker/`, {
        params: params
    })
}

// search列表详情页
export const cell_search_detail = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search_detail/${params}/`)
}

// search文献列表页
export const cell_search_public_list = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search_public_list/`, {
        params: params
    })
}

// search列表详情页
export const cell_search_public_detail = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search_public_detail/${params}/`)
}

// efp 图片动态返回
export const cell_search_efp = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search_efp/`, {
        params: params
    })
}
// 烟草EFP
export const nicotiana_tabacum_efp = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search_efp/nicotiana_tabacum_efp/`, {
        params: params
    })
}


// Transcriptome 下拉框
export const pmid_dataset = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search_detail/${params}/pmid_dataset/`)
}
// Transcriptome
export const transcriptome = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search_detail/transcriptome/`, {
        params: params
    })
}
// 单细胞详情supported_evidences列表页展示接口
export const supported_evidences = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search/${params}/supported_evidences/`)
}

// umap dataset接口
export const umap_dataset = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search_detail/${params}/umap_dataset/`)
}
// umap expression接口
export const umap_expression = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search_detail/umap_expression/`, {
        params: params
    })
}
// umap tsne接口
export const tsne_expression = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search_detail/tsne_expression/`, {
        params: params
    })
}

// search result
export const page_search_heat_map = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search/page_search_heat_map/`, {
        params: params
    })
}
// search result chart
export const all_search_heat_map = params => {
    return axios.get(`${baseUrl}/api/v1/cell_search/all_search_heat_map/`, {
        params: params
    })
}
// 详情序列接口
export const cell_detail_seq = params => {
    return axios.get(`${baseUrl}/api/v1/cell_detail_seq/`, {
        params: params
    })
}
// 获取静态图片
export const project_static_umap_png = params => {
    return axios.get(`${baseUrl}/api/v1/project_static_umap_png/`, {
        params: params
    })
}
// atlas 获取静态图片
export const atlas_static_umap_png = params => {
    return axios.get(`${baseUrl}/api/v1/atlas_static_umap_png/`, {
        params: params
    })
}
// 动态返回静态图接口
export const home_atlas_static = params => {
    return axios.get(`${baseUrl}/api/v1/home_atlas_static/`, {
        params: params
    })
}








// 育种大数据登录接口
export const login = params => {
    const param = qs.stringify(params) //序列化post 参数
    return axios.post(`${baseUrl}/api/v1/account/login/`, {
        data: param
    })
}