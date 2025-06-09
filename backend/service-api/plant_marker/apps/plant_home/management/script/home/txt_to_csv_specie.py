import os
from collections import Counter

import pandas as pd

base_dir = 'D:/项目文档/基因检测/源数据/Oryza_sativa_Root/Root'

# cluster_annotation 数据
cluster_annotation_path = os.path.join(base_dir, "Cluster_annt.txt")
# print(cluster_annotation_path)
cluster_annotation_data = pd.read_csv(cluster_annotation_path, sep=r"\t", engine='python')

dict_data = cluster_annotation_data.to_dict('list')
Cluster_data = dict_data.get('Cluster', {})
Cell_type_data = dict_data.get('Cell_type', {})
cluster_name_data = dict(zip(Cluster_data, Cell_type_data))
print(cluster_name_data)
# cluster_name_data = cluster_annotation_data.to_dict('dict').get('Cell_type', {})

# 保存为 Cluster_annotation.csv

cluster_annotation_rename_columns_data = {
    'Cluster': 'Clusters',
    'Cell_type': 'Cluster_Name'
}
cluster_annotation_data = cluster_annotation_data.rename(columns=cluster_annotation_rename_columns_data)
cluster_annotation_data.to_csv('./Cluster_annotation.csv', index=False)

# 生成 cluster_markers.csv
cluster_markers_path = os.path.join(base_dir, "clustermarker.txt")

cluster_markers_data = pd.read_csv(cluster_markers_path, sep=r"\t", engine='python')
rename_columns_data = {
    '"cluster"': 'cluster_id',
    '"p_val"': 'p_val',
    '"avg_log2FC"': 'log_2fc',
    '"pct.1"': 'pct1',
    '"pct.2"': 'pct2',
    '"p_val_adj"': 'p_val_adj',
    '"gene"': 'gene_id',
}
cluster_markers_data = cluster_markers_data.rename(columns=rename_columns_data)


# 先把 Cluster ID 这一列转换成 数字
def cluster_id_to_int(x):
    return int(x.replace('"', ''))
    # return x


cluster_markers_data['cluster_id'] = cluster_markers_data['cluster_id'].apply(cluster_id_to_int)


# 再生成一列 Cell Type
def cluster_id_to_cluster_name(x):
    return cluster_name_data.get(x, '')


cluster_markers_data['cell_type'] = cluster_markers_data['cluster_id'].apply(cluster_id_to_cluster_name)


# Gene 这一列去除冒号
def gene_replace(x):
    return x.replace('"', '')

# 逗号转换下划线
def convert_comma(x):
    x = x.replace('.', '-')
    return x


def to_point(x):
    x = x.replace('"', '').replace('-', '.')
    return x


cluster_markers_data['gene_id'] = cluster_markers_data['gene_id'].apply(gene_replace)

cluster_markers_data.to_csv('cluster_markers.csv', index=False)

# 生成 Umap_data
# 读取 Umap_location 数据
umap_location_path = os.path.join(base_dir, "umap_location.txt")
umap_location_data = pd.read_csv(umap_location_path, sep=r"\t", engine='python')

umap_location_rename_columns_data = {
    '"UMAP_1"': 'UMAP_1',
    '"UMAP_2"': 'UMAP_2',
}
umap_location_data = umap_location_data.rename(columns=umap_location_rename_columns_data)

# 将索引转换成 Cell_ID 列
umap_location_data['Cell_ID'] = umap_location_data.index
print(umap_location_data)

# 读取 Cell_cluster 数据
cell_cluster_path = os.path.join(base_dir, "cell_cluster.txt")
cell_cluster_data = pd.read_csv(cell_cluster_path, sep=r"\t", engine='python')

cell_cluster_rename_columns_data = {
    '"orig.ident"': 'Project_ID',
    '"seurat_clusters"': 'Clusters',
}
cell_cluster_data = cell_cluster_data.rename(columns=cell_cluster_rename_columns_data)
# print(cell_cluster_data)
# 将 Clusters 转换成 整数
cell_cluster_data['Clusters'] = cell_cluster_data['Clusters'].apply(cluster_id_to_int)

# 去除 Project_ID 的冒号
cell_cluster_data['Project_ID'] = cell_cluster_data['Project_ID'].apply(gene_replace)

# 将索引转换成 Cell_ID 列
cell_cluster_data['Cell_ID'] = cell_cluster_data.index
cell_cluster_data['Cell_ID'] = cell_cluster_data['Cell_ID'].apply(convert_comma)
print(cell_cluster_data)
# 根据 Cell_ID 合并 Umap_location 和 Cell_cluster
umap_data = pd.merge(umap_location_data, cell_cluster_data, how='left', on='Cell_ID')
print(umap_data)


# umap_data 的 Clusters 转换为 cluster_id：cluster_name

def clusters_to_clusters_name(x):
    clusters_name = cluster_name_data.get(int(x))
    # clusters_name_data = f'{x}:{clusters_name}'
    return clusters_name


# umap_data['Clusters'] = umap_data['Clusters'].apply(gene_replace)
umap_data['Cell_type'] = umap_data['Clusters'].apply(clusters_to_clusters_name)

# 去除 Cell_ID 的冒号
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
# 读取 Umap_location 数据
tsne_location_path = os.path.join(base_dir, "tsne_location.txt")
tsne_location_data = pd.read_csv(tsne_location_path, sep=r"\t", engine='python')

tsne_location_rename_columns_data = {
    '"tSNE_1"': 'tSNE_1',
    '"tSNE_2"': 'tSNE_2',
}
tsne_location_data = tsne_location_data.rename(columns=tsne_location_rename_columns_data)

# 将索引转换成 Cell_ID 列
tsne_location_data['Cell_ID'] = tsne_location_data.index

# 读取 Cell_cluster 数据
cell_cluster_path = os.path.join(base_dir, "cell_cluster.txt")
cell_cluster_data = pd.read_csv(cell_cluster_path, sep=r"\t", engine='python')

cell_cluster_rename_columns_data = {
    '"orig.ident"': 'Project_ID',
    '"seurat_clusters"': 'Clusters',
}
cell_cluster_data = cell_cluster_data.rename(columns=cell_cluster_rename_columns_data)
# 将 Clusters 转换成 整数
cell_cluster_data['Clusters'] = cell_cluster_data['Clusters'].apply(cluster_id_to_int)

# 去除 Project_ID 的冒号
cell_cluster_data['Project_ID'] = cell_cluster_data['Project_ID'].apply(gene_replace)

# 将索引转换成 Cell_ID 列
cell_cluster_data['Cell_ID'] = cell_cluster_data.index
cell_cluster_data['Cell_ID'] = cell_cluster_data['Cell_ID'].apply(convert_comma)
# 根据 Cell_ID 合并 Umap_location 和 Cell_cluster
tsne_data = pd.merge(tsne_location_data, cell_cluster_data, how='left', on='Cell_ID')


# umap_data 的 Clusters 转换为 cluster_id：cluster_name
def clusters_to_clusters_name(x):
    clusters_name = cluster_name_data.get(int(x))
    # clusters_name_data = f'{x}:{clusters_name}'
    return clusters_name


# tsne_data['Clusters'] = tsne_data['Clusters'].apply(gene_replace)
print(tsne_data)
tsne_data['Cell_type'] = tsne_data['Clusters'].apply(clusters_to_clusters_name)

# 去除 Cell_ID 的冒号

tsne_data['Cell_ID'] = tsne_data['Cell_ID'].apply(to_point)
tsne_data.to_csv('./tsne_data_old.csv', index=False)

tsne_cluster_list = list(tsne_data['Clusters'].values.tolist())
tsne_cluster_data = dict(Counter(tsne_cluster_list))
with open('tsne_gene_count_cluster.txt', 'w') as op:
    op.write(str(tsne_cluster_data))

tsne_cell_type_list = list(tsne_data['Cell_type'].values.tolist())
tsne_cell_type_data = dict(Counter(tsne_cell_type_list))
with open('tsne_gene_count_cell_type.txt', 'w') as op:
    op.write(str(tsne_cell_type_data))

tsne_sample_list = list(tsne_data['Project_ID'].values.tolist())
tsne_sample_data = dict(Counter(tsne_sample_list))
with open('tsne_gene_count_sample.txt', 'w') as op:
    op.write(str(tsne_sample_data))
