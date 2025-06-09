import os
import scanpy as sc

from django_server.utils.sqmple_qc import sample_qc_fun


def collect_data(base_path, request_data):
    """私有方法来收集数据，减少重复代码"""
    all_data = []
    for dir_name in ['data1', 'data2']:
        try:
            # 自动检测文件类型
            file_path_gz = get_file_path(base_path, dir_name, 'gz')
            file_path_h5 = get_file_path(base_path, dir_name, 'h5')

            if os.path.exists(file_path_gz):
                adata = sc.read_10x_mtx(file_path_gz, var_names='gene_symbols')
                qc_data = sample_qc_fun(adata, dir_name, **request_data)
            elif os.path.exists(file_path_h5):
                # adata = sc.read_h5ad(file_path_h5)
                try:
                    adata = sc.read_h5ad(file_path_h5)
                except Exception as e:
                    adata = sc.read_10x_h5(file_path_h5)
                qc_data = sample_qc_fun(adata, dir_name, **request_data)
            else:
                qc_data = default_qc_data()

            all_data.append({dir_name: qc_data})
        except Exception as e:
            # 捕获收集数据过程中的异常
            qc_data = default_qc_data()
            error_message = f"数据收集错误 ({dir_name}): {str(e)}"
            all_data.append({"error": error_message})
    return all_data


def get_file_path(base_path, dir_name, run_type):
    """根据运行类型获取文件路径"""
    if run_type == 'gz':
        return f"{base_path}/{dir_name}/outs/outs/filtered_feature_bc_matrix"
    return f"{base_path}/{dir_name}/outs/outs/filtered_feature_bc_matrix.h5"


def load_data(file_path, run_type):
    """根据运行类型加载数据"""
    try:
        if run_type == 'gz':
            return sc.read_10x_mtx(file_path, var_names='gene_symbols')
        # 读取h5
        return sc.read_h5ad(file_path)
    except Exception as e:
        return sc.read_10x_h5(file_path)


def default_qc_data():
    """返回默认的QC数据字典"""
    return {
        "max_n_genes_by_counts": 0,
        "min_n_genes_by_counts": 0,
        "max_total_counts": 0,
        "min_total_counts": 0,
        "max_pct_counts_mt": 0,
        "min_pct_counts_mt": 0,
        "max_pct_counts_pt": 0,
        "min_pct_counts_pt": 0
    }