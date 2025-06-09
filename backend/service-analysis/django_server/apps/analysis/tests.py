# import pandas as pd
#
# # 根据物种名称映射文件
# file_path = r'D:\P_三期\analysis_server\django_server\apps\analysis\cluster.csv'
#
# umap_data = pd.read_csv(file_path, usecols=['UMAP1', 'UMAP2', 'cluster', 'cell_type'])
# umap_type = 'cell_type'
#
# # 通过 cell_type 组成的 DataFrame
# umap_data['cluster_cell_type'] = umap_data['cluster'].map(str) + ':' + umap_data[umap_type].map(str)
#
# # 按 cluster 和 cell_type 分组，此时 group_name 是 (cluster, cell_type) 的元组
# clusters_data = umap_data.groupby(['cluster', umap_type])
#
# data_list = []
# for group_name, group_data in clusters_data:
#     # group_name 是一个元组，包含 cluster 和 cell_type
#     cluster_name = str(group_name[0])  # cluster 值
#     cell_type_name = group_name[1]  # cell_type 值
#
#     group_data = group_data[['UMAP1', 'UMAP2']]
#     data = {
#         'name': cell_type_name,
#         'data': group_data.to_dict('split').get('data', []),
#         'sort': int(cluster_name)
#     }
#     data_list.append(data)
#
# # 按 sort 排序
# data_list = sorted(data_list, key=lambda x: x['sort'])
# print(data_list)
# import re
# # 定义前缀
# a = "scDR1"
#
# # 定义正则表达式模式，使用前缀
# pattern = fr'^{re.escape(a)}_S\d+_L\d+_R\d+_\d+\.fastq\.gz$'
#
# # 测试文件名
# filename = "scDR1_S12_L010_R11_010.fastq.gz"
#
# # 使用 re.match() 校验文件名
# if re.match(pattern, filename):
#     print("文件名格式正确且以指定前缀开头")
# else:
#     print("文件名格式不正确或不以指定前缀开头")
from datetime import datetime

import scanpy as sc
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def heatmap(adata, **kwargs):
    print(datetime.now())
    type_ = kwargs.get('type_', "heatmap")
    # 设置图片存放的路径
    sc.settings.figdir = r'D:/P_三期/analysis_server/django_server/apps/analysis/'
    # 设置文件存储的后缀
    sc.settings.file_format_figs = 'svg'

    if type_ == 'heatmap':

        heatmap_data = sc.pl.rank_genes_groups_heatmap(adata, n_genes=5, groupby='cluster', show_gene_labels=True,
                                                       show=False, save=True)

    elif type_ == 'dotplot':

        # 保存 dotplot 图片 名称为 dotplot.svg
        sc.pl.rank_genes_groups_dotplot(adata, n_genes=5, groupby='cluster', show=False, save=True)

    else:
        # 保存 tracksplot 图片 名称为 tracksplot.svg
        sc.pl.rank_genes_groups_tracksplot(adata, n_genes=3, groupby='cluster', show=False, save=True)

    print(datetime.now())


if __name__ == "__main__":
    # 通过 h5ad 读取 Anndata
    adata = sc.read('./cluster.h5ad')
    # 执行方法
    heatmap(adata)
