import scanpy as sc
import scanpy.external as sce

def data_process(adata, **kwargs):
    """
    # 数据预处理
    """
    # 提取参数
    min_mean = kwargs.get('min_mean', 0.0125)
    max_mean = kwargs.get('max_mean', 3)
    min_disp = kwargs.get('min_disp', 0.25)
    n_jobs = kwargs.get('n_jobs', 10)
    max_value = kwargs.get('max_value', 10)
    n_neighbors = kwargs.get('n_neighbors', 10)
    n_pcs = kwargs.get('n_pcs', 50)
    # 开始数据预处理
    adata.var['mt'] = adata.var_names.str.startswith('MT-')
    sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, min_mean=min_mean, max_mean=max_mean, min_disp=min_disp)
    adata.raw = adata
    adata = adata[:, adata.var.highly_variable]
    sc.pp.regress_out(adata, ['total_counts'], n_jobs=n_jobs)
    sc.pp.scale(adata, max_value=max_value)
    sc.tl.pca(adata, svd_solver='arpack')
    sc.pp.neighbors(adata, n_neighbors=n_neighbors, n_pcs=n_pcs)
    sc.tl.umap(adata)
    sce.pp.harmony_integrate(adata, 'sample')
    adata.obsm['X_pca'] = adata.obsm['X_pca_harmony']

    return adata