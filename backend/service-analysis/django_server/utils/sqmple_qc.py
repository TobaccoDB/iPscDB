## 通过 h5ad 读取 Anndata
import scanpy as sc


def sample_qc_fun(adata, dir_name, **kwargs):
    # 索引去重复
    adata.var_names_make_unique()
    adata.obs_names_make_unique()
    # 增加基本过滤条件0901
    sc.pp.filter_cells(adata, min_genes=200)
    sc.pp.filter_genes(adata, min_cells=3)

    mt = kwargs.get('mt', None)
    pt = kwargs.get('pt', None)
    base_path = kwargs.get('base_path', None)
    qc_vars_list = []
    if mt:
        # 进行线粒体和叶绿体的基因过滤
        adata.var['mt'] = adata.var_names.str.startswith(mt)
        qc_vars_list.append('mt')
    if pt:
        adata.var['pt'] = adata.var_names.str.startswith(pt)
        qc_vars_list.append('pt')
    # # 进行线粒体和叶绿体的基因过滤0901
    sc.pp.calculate_qc_metrics(adata, qc_vars=qc_vars_list, percent_top=None, log1p=False, inplace=True)

    # 生成结果数据，确保所有数值转换为 int 类型
    data = {
        "max_n_genes_by_counts": int(
            adata.obs['n_genes_by_counts'].max()) if 'n_genes_by_counts' in adata.obs.columns else 0,
        "min_n_genes_by_counts": int(
            adata.obs['n_genes_by_counts'].min()) if 'n_genes_by_counts' in adata.obs.columns else 0,
        "max_total_counts": int(adata.obs['total_counts'].max()) if 'total_counts' in adata.obs.columns else 0,
        "min_total_counts": int(adata.obs['total_counts'].min()) if 'total_counts' in adata.obs.columns else 0,
        "max_pct_counts_mt": int(adata.obs['pct_counts_mt'].max()) if 'pct_counts_mt' in adata.obs.columns else 0,
        "min_pct_counts_mt": int(adata.obs['pct_counts_mt'].min()) if 'pct_counts_mt' in adata.obs.columns else 0,
        "max_pct_counts_pt": int(adata.obs['pct_counts_pt'].max()) if 'pct_counts_pt' in adata.obs.columns else 0,
        "min_pct_counts_pt": int(adata.obs['pct_counts_pt'].min()) if 'pct_counts_pt' in adata.obs.columns else 0,
    }
    path = f'{base_path}/{dir_name}/outs/outs/filtered_feature_bc_matrix.h5'
    adata.write_h5ad(filename=path)

    return data
