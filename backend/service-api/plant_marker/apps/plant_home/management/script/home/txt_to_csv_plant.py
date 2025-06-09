import os
from collections import Counter

import pandas as pd

base_dir = 'F:/脚本20240227'


# Gene 这一列去除冒号
def gene_replace(x):
    return x.replace('"', '')


def cell_id_format(x):
    x = x.replace('@', '.')
    return x


# 生成 Umap_data
# 读取 Umap_location 数据
umap_location_path = os.path.join(base_dir, "D1_umap_location.txt")
umap_location_data = pd.read_csv(umap_location_path, sep=r"\t", engine='python')

umap_location_rename_columns_data = {
    '"UMAP_1"': 'UMAP_1',
    '"UMAP_2"': 'UMAP_2',
}
umap_location_data = umap_location_data.rename(columns=umap_location_rename_columns_data)

# 将索引转换成 Cell_ID 列
umap_location_data['Cell_ID'] = umap_location_data.index
umap_location_data['Cell_ID'] = umap_location_data['Cell_ID'].apply(cell_id_format)
# print(umap_location_data)


# 读取 D3_cell_type 数据
cell_cluster_path = os.path.join(base_dir, "D3_cell_type.txt")
cell_cluster_data = pd.read_csv(cell_cluster_path, sep=r"\t", engine='python')

cell_cluster_rename_columns_data = {
    '"Orig.ident"': 'Project_ID',
    '"Seurat_clusters"': 'Clusters',
    '"Celltype"': 'Cell_type',
}
cell_cluster_data = cell_cluster_data.rename(columns=cell_cluster_rename_columns_data)
# 去除 Clusters 的冒号
cell_cluster_data['Clusters'] = cell_cluster_data['Clusters'].apply(gene_replace)
# 去除 Project_ID 的冒号
cell_cluster_data['Project_ID'] = cell_cluster_data['Project_ID'].apply(gene_replace)
# 去除 Cell_type 的冒号
cell_cluster_data['Cell_type'] = cell_cluster_data['Cell_type'].apply(gene_replace)

# 将索引转换成 Cell_ID 列
cell_cluster_data['Cell_ID'] = cell_cluster_data.index
cell_cluster_data['Cell_ID'] = cell_cluster_data['Cell_ID'].apply(cell_id_format)


umap_data = pd.merge(umap_location_data, cell_cluster_data, how='left', on='Cell_ID')


# 去除 Cell_ID 的冒号并转换 - 为 .
def to_point(x):
    x = x.replace('"', '').replace('-', '.')
    return x


umap_data['Cell_ID'] = umap_data['Cell_ID'].apply(to_point)
umap_data.to_csv('./umap_data_old.csv', index=False)

umap_cluster_list = list(umap_data['Clusters'].values.tolist())
umap_cluster_data = dict(Counter(umap_cluster_list))
with open('umap_gene_count_Clusters.txt', 'w') as op:
    op.write(str(umap_cluster_data))

umap_cell_type_list = list(umap_data['Cell_type'].values.tolist())
umap_cell_type_data = dict(Counter(umap_cell_type_list))
with open('umap_gene_count_Cell_type.txt', 'w') as op:
    op.write(str(umap_cell_type_data))

umap_sample_list = list(umap_data['Project_ID'].values.tolist())
umap_sample_data = dict(Counter(umap_sample_list))
with open('umap_gene_count_Project_ID.txt', 'w') as op:
    op.write(str(umap_sample_data))

# 生成 tSNE_data
# 读取 tsne_location 数据
tsne_location_path = os.path.join(base_dir, "D2_tsne_location.txt")
tsne_location_data = pd.read_csv(tsne_location_path, sep=r"\t", engine='python')

tsne_location_rename_columns_data = {
    '"tSNE_1"': 'tSNE_1',
    '"tSNE_2"': 'tSNE_2',
}
tsne_location_data = tsne_location_data.rename(columns=tsne_location_rename_columns_data)

# 将索引转换成 Cell_ID 列
tsne_location_data['Cell_ID'] = tsne_location_data.index
tsne_location_data['Cell_ID'] = tsne_location_data['Cell_ID'].apply(cell_id_format)
# 根据 Cell_ID 合并 Umap_location 和 Cell_cluster
tsne_data = pd.merge(tsne_location_data, cell_cluster_data, how='left', on='Cell_ID')

# 去除 Cell_ID 的冒号
tsne_data['Cell_ID'] = tsne_data['Cell_ID'].apply(to_point)
tsne_data.to_csv('./tsne_data_old.csv', index=False)

tsne_cluster_list = list(tsne_data['Clusters'].values.tolist())
tsne_cluster_data = dict(Counter(tsne_cluster_list))
with open('tsne_gene_count_Clusters.txt', 'w') as op:
    op.write(str(tsne_cluster_data))

tsne_cell_type_list = list(tsne_data['Cell_type'].values.tolist())
tsne_cell_type_data = dict(Counter(tsne_cell_type_list))
with open('tsne_gene_count_Cell_type.txt', 'w') as op:
    op.write(str(tsne_cell_type_data))

tsne_sample_list = list(tsne_data['Project_ID'].values.tolist())
tsne_sample_data = dict(Counter(tsne_sample_list))
with open('tsne_gene_count_Project_ID.txt', 'w') as op:
    op.write(str(tsne_sample_data))

cell_cluster_data['Cell_ID'] = cell_cluster_data['Cell_ID'].apply(to_point)

cell_cluster_data = cell_cluster_data.set_index("Cell_ID")

print(cell_cluster_data)
cell_cluster_data.to_csv("cell_cluster.csv")
