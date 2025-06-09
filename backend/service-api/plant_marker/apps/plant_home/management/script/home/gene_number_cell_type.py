import pandas as pd
import numpy as np
import os

base_dir = '/root/data/04_Atlases/Gossypium hirsutum/Ovule'

# 格式化
def gene_replace(x):
    # @替换为'.'
    x = x.replace('@', '.')
    # 添加双引号
    x = '"{index}"'.format(index=x)
    return x


# 读取 Cell_cluster 数据
cell_cluster_data = pd.read_csv("./umap_data_old.csv", usecols=['Cell_ID', 'Project_ID', 'Clusters', 'Cell_type'], engine='python')
cell_cluster_data['Cell_ID'] = cell_cluster_data['Cell_ID'].apply(gene_replace)
cell_id_list = cell_cluster_data['Cell_ID'].values.tolist()
column_types = { i:np.float16 for i in cell_id_list}
cell_cluster_data = cell_cluster_data.set_index('Cell_ID')
cell_cluster_data = cell_cluster_data.rename_axis(None)
print(cell_cluster_data)
# 生成 Cell_type 数据
cell_type_umap_data = cell_cluster_data.drop(['Project_ID', 'Clusters'], axis=1)
cell_type_list = list(set(cell_type_umap_data["Cell_type"].values.tolist()))
cell_type_number_data = {}
for cell_type in cell_type_list:
    print(cell_type)
    cluster_data = cell_type_umap_data[cell_type_umap_data["Cell_type"] == cell_type]
    column_list = cluster_data.index.tolist()
    expression_path = os.path.join(base_dir, "D4_GEMatrix.txt")
    expression_data_list = pd.read_csv(expression_path, sep=r"\t", dtype=column_types, usecols=column_list, chunksize=10000, engine='python')
    total_number_list = []
    for expression_chunk_data in expression_data_list:
        expression_chunk_data = expression_chunk_data.T
        expression_chunk_data[cell_type] = expression_chunk_data.gt(0).sum(axis=1)
        total_number_list.extend(expression_chunk_data[cell_type].values.tolist())

    # print(total_number_list)
    cell_type_number_data[cell_type] = total_number_list
# print(cell_type_number_data)
with open('expresse_gene_number_Cell_type.txt', 'w') as op:
    op.write(str(cell_type_number_data))

# 生成 sample 数据
sample_umap_data = cell_cluster_data.drop(['Cell_type', 'Clusters'], axis=1)
sample_list = list(set(sample_umap_data["Project_ID"].values.tolist()))
sample_number_data = {}
for sample in sample_list:
    print(sample)
    sample_data = sample_umap_data[sample_umap_data["Project_ID"] == sample]
    column_list = sample_data.index.tolist()
    expression_path = os.path.join(base_dir, "D4_GEMatrix.txt")
    expression_data_list = pd.read_csv(expression_path, sep=r"\t", dtype=column_types, usecols=column_list, chunksize=10000, engine='python')

    total_number_list = []
    for expression_chunk_data in expression_data_list:
        expression_chunk_data = expression_chunk_data.T
        expression_chunk_data[sample] = expression_chunk_data.gt(0).sum(axis=1)
        total_number_list.extend(expression_chunk_data[sample].values.tolist())

    # print(total_number_list)
    sample_number_data[sample] = total_number_list
# print(sample_number_data)
with open('expresse_gene_number_Project_ID.txt', 'w') as op:
    op.write(str(sample_number_data))

# 生成 Clusters 数据
cluster_umap_data = cell_cluster_data.drop(['Cell_type', 'Project_ID'], axis=1)
cluster_list = list(set(cluster_umap_data["Clusters"].values.tolist()))
cluster_number_data = {}
for cluster in cluster_list:
    if not cluster or str(cluster) == 'nan':
        continue
    cluster = int(cluster)
    print(cluster)
    cluster_data = cluster_umap_data[cluster_umap_data["Clusters"] == cluster]
    column_list = cluster_data.index.tolist()
    expression_path = os.path.join(base_dir, "D4_GEMatrix.txt")
    expression_data_list = pd.read_csv(expression_path, sep=r"\t", dtype=column_types, usecols=column_list, chunksize=10000, engine='python')

    total_number_list = []
    for expression_chunk_data in expression_data_list:
        expression_chunk_data = expression_chunk_data.T
        expression_chunk_data[cluster] = expression_chunk_data.gt(0).sum(axis=1)
        total_number_list.extend(expression_chunk_data[cluster].values.tolist())

    # print(total_number_list)
    cluster_number_data[cluster] = total_number_list
# print(cluster_number_data)
with open('expresse_gene_number_Clusters.txt', 'w') as op:
    op.write(str(cluster_number_data))
