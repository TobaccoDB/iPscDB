import scanpy as sc


def cluster_fun(adata, **kwargs):
    # 获取参数
    resolution = kwargs.get('resolution', 0.2)

    # 定制cluster
    sc.tl.leiden(adata, resolution=resolution, key_added='cluster')

    return adata
