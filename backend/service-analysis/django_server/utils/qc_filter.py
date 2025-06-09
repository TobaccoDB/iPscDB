import scanpy as sc


def qc_filter(adata, **kwargs):
    # adata=sc.read('./combined_adata.h5ad')
    # 基本过滤设置
    # 去除表达基因200以下的细胞；去除在3个细胞以下表达的基因。这也是通常Seurat通常用的默认过滤标准
    #sc.pp.filter_cells(adata, min_genes=200)
    #sc.pp.filter_genes(adata, min_cells=3)

    # sc.pp.calculate_qc_metrics(adata, qc_vars=['mt', 'pt'], percent_top=None, log1p=False, inplace=True)

    max_n_genes_by_counts = kwargs.get('max_n_genes_by_counts', 0)
    min_n_genes_by_counts = kwargs.get('min_n_genes_by_counts', 0)
    max_total_counts = kwargs.get('max_total_counts', 0)
    min_total_counts = kwargs.get('min_total_counts', 0)
    max_pct_counts_mt = kwargs.get('max_pct_counts_mt', None)
    min_pct_counts_mt = kwargs.get('min_pct_counts_mt', None)
    max_pct_counts_pt = kwargs.get('max_pct_counts_pt', None)
    min_pct_counts_pt = kwargs.get('min_pct_counts_pt', None)
    # adata = adata[
    #     (adata.obs.n_genes_by_counts <= max_n_genes_by_counts) & (adata.obs.n_genes_by_counts >= min_n_genes_by_counts)]
    # adata = adata[(adata.obs.total_counts <= max_total_counts) & (adata.obs.total_counts >= min_total_counts)]
    # adata = adata[(adata.obs.pct_counts_mt <= max_pct_counts_mt) & (adata.obs.pct_counts_mt >= min_pct_counts_mt)]
    # adata = adata[(adata.obs.pct_counts_pt <= max_pct_counts_pt) & (adata.obs.pct_counts_pt >= min_pct_counts_pt)]

    adata = adata[
        (adata.obs.n_genes_by_counts <= max_n_genes_by_counts) &
        (adata.obs.n_genes_by_counts >= min_n_genes_by_counts)
        ]
    adata = adata[
        (adata.obs.total_counts <= max_total_counts) &
        (adata.obs.total_counts >= min_total_counts)
        ]

    # 如果提供了 max_pct_counts_mt 和 min_pct_counts_mt，就执行筛选
    if max_pct_counts_mt is not None and min_pct_counts_mt is not None:
        adata = adata[
            (adata.obs.pct_counts_mt <= max_pct_counts_mt) &
            (adata.obs.pct_counts_mt >= min_pct_counts_mt)
            ]

    # 如果提供了 max_pct_counts_pt 和 min_pct_counts_pt，就执行筛选
    if max_pct_counts_pt is not None and min_pct_counts_pt is not None:
        adata = adata[
            (adata.obs.pct_counts_pt <= max_pct_counts_pt) &
            (adata.obs.pct_counts_pt >= min_pct_counts_pt)
            ]

    return adata

