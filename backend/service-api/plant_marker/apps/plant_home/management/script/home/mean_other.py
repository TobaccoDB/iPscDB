import pandas as pd
import os

base_dir = 'D:/项目文档/基因检测/源数据/Oryza_sativa_Root/Root'

# cluster_annotation 数据
cluster_annotation_path = os.path.join(base_dir, "Cluster_annt.txt")
# print(cluster_annotation_path)
cluster_annotation_data = pd.read_csv(cluster_annotation_path, sep=r"\t", engine='python')
dict_data = cluster_annotation_data.to_dict('list')
Cluster_data = dict_data.get('Cluster', {})
Cell_type_data = dict_data.get('Cell_type', {})
cluster_name_data = dict(zip(Cluster_data, Cell_type_data))


# 去除冒号
def gene_replace(x):
    return x.replace('"', '')


# 读取 Cell_cluster 数据
cell_cluster_path = os.path.join(base_dir, "cell_cluster.txt")
cell_cluster_data = pd.read_csv(cell_cluster_path, sep=r"\t", engine='python')

cell_cluster_rename_columns_data = {
    '"orig.ident"': 'Project_ID',
    '"seurat_clusters"': 'Clusters',
    '"cell_type"': 'Cell_type',
}
cell_cluster_data = cell_cluster_data.rename(columns=cell_cluster_rename_columns_data)
cell_cluster_data['Project_ID'] = cell_cluster_data['Project_ID'].apply(gene_replace)
cell_cluster_data['Clusters'] = cell_cluster_data['Clusters'].apply(gene_replace)


# 再生成一列 Cell Type
def cluster_id_to_cluster_name(x):
    return cluster_name_data.get(int(x), '')


cell_cluster_data['Cell_type'] = cell_cluster_data['Clusters'].apply(cluster_id_to_cluster_name)
print(cell_cluster_data)

# 获取 cluster 数据
cluster_list = list(set(cell_cluster_data["Clusters"].values.tolist()))
print(cluster_list)
# 获取 sample 数据
sample_list = list(set(cell_cluster_data["Project_ID"].values.tolist()))
print(sample_list)
# 获取 cell_type 数据
cell_type_list = list(set(cell_cluster_data["Cell_type"].values.tolist()))
print(cell_type_list)
# 分片读取表达式值
expression_path = os.path.join(base_dir, "scRNA_Matrix.txt")
expression = pd.read_csv(expression_path, sep=r"\t", chunksize=300, engine='python')
print("-----------------文件切片处理开始-----------------------------")
for index, chunk in enumerate(expression):
    print("-----------------------第{}次----------------------------".format(index+1))
    try:
        expression_data = chunk.T
        total_data = pd.merge(expression_data, cell_cluster_data, left_index=True, right_index=True)

        cluster_total_data = total_data.drop(['Project_ID', 'Cell_type'], axis=1)
        for cluster in cluster_list:
            cluster_data = cluster_total_data[cluster_total_data["Clusters"] == cluster]
            cluster_data = cluster_data.set_index('Clusters')
            cluster_data = cluster_data.T
            cluster_data["mean"] = cluster_data.mean(axis=1)
            cluster_name = cluster.replace('/', '_')
            save_name = "./mean_data_cluster/{cluster_name}.csv".format(cluster_name=cluster_name)
            file_data = cluster_data["mean"]

            if os.path.exists(save_name):
                file_data.to_csv(save_name, mode='a', header=False,index=False)
            else:
                file_data.to_csv(save_name, mode='w', header=True, index=False)

        sample_total_data = total_data.drop(['Clusters', 'Cell_type'], axis=1)
        for sample in sample_list:
            sample_data = sample_total_data[sample_total_data["Project_ID"] == sample]
            sample_data = sample_data.set_index('Project_ID')
            sample_data = sample_data.T
            sample_data["mean"] = sample_data.mean(axis=1)
            sample_name = sample.replace('/', '_')
            save_name = "./mean_data_sample/{sample_name}.csv".format(sample_name=sample_name)
            file_data = sample_data["mean"]
            if os.path.exists(save_name):
                file_data.to_csv(save_name, mode='a', header=False, index=False)
            else:
                file_data.to_csv(save_name, mode='w', header=True, index=False)

        cell_type_total_data = total_data.drop(['Clusters', 'Project_ID'], axis=1)
        for cell_type in cell_type_list:
            cell_type_data = cell_type_total_data[cell_type_total_data["Cell_type"] == cell_type]
            cell_type_data = cell_type_data.set_index('Cell_type')
            cell_type_data = cell_type_data.T
            cell_type_data["mean"] = cell_type_data.mean(axis=1)
            cell_type_name = cell_type.replace('/', '_')
            save_name = "./mean_data_cell_type/{cell_type_name}.csv".format(cell_type_name=cell_type_name)
            file_data = cell_type_data["mean"]

            if os.path.exists(save_name):
                file_data.to_csv(save_name, mode='a', header=False, index=False)
            else:
                file_data.to_csv(save_name, mode='w', header=True, index=False)

    except Exception as e:
        print(e)
        continue

print("-----------------文件切片处理完成-----------------------------")
print("-------------------读取文件开始------------------------------")
cluster_expresse_gene_count_list = []
cluster_total_mean_data = pd.DataFrame()
for cluster in cluster_list:
    cluster_name = cluster.replace('/', '_')
    read_name = "./mean_data_cluster/{cluster_name}.csv".format(cluster_name=cluster_name)
    mean_data = pd.read_csv(read_name)
    expresse_data = mean_data[mean_data["mean"] != 0]
    cluster_dict = {
        cluster: expresse_data.shape[0]
    }
    cluster_expresse_gene_count_list.append(cluster_dict)
    mean_data = mean_data.rename(columns={"mean": cluster})
    cluster_total_mean_data = pd.concat([cluster_total_mean_data, mean_data], join='outer', axis=1)
with open('expresse_gene_count_Clusters.txt', 'w') as op:
    op.write(str(cluster_expresse_gene_count_list))
cluster_total_mean_data.to_csv("total_mean_Clusters.csv", index=False)

sample_expresse_gene_count_list = []
sample_total_mean_data = pd.DataFrame()
for sample in sample_list:
    sample_name = sample.replace('/', '_')
    read_name = "./mean_data_sample/{sample_name}.csv".format(sample_name=sample_name)
    mean_data = pd.read_csv(read_name)
    expresse_data = mean_data[mean_data["mean"] != 0]
    sample_dict = {
       sample: expresse_data.shape[0]
    }
    sample_expresse_gene_count_list.append(sample_dict)
    mean_data = mean_data.rename(columns={"mean": sample})
    sample_total_mean_data = pd.concat([sample_total_mean_data, mean_data], join='outer', axis=1)

with open('expresse_gene_count_Project_ID.txt', 'w') as op:
    op.write(str(sample_expresse_gene_count_list))
sample_total_mean_data.to_csv("total_mean_Project_ID.csv", index=False)


cell_type_expresse_gene_count_list = []
cell_type_total_mean_data = pd.DataFrame()
for cell_type in cell_type_list:
    cell_type_name = cell_type.replace('/', '_')
    read_name = "./mean_data_cell_type/{cell_type_name}.csv".format(cell_type_name=cell_type_name)
    mean_data = pd.read_csv(read_name)
    expresse_data = mean_data[mean_data["mean"] != 0]
    cell_type_dict = {
       cell_type: expresse_data.shape[0]
    }
    cell_type_expresse_gene_count_list.append(cell_type_dict)
    mean_data = mean_data.rename(columns={"mean": cell_type})
    cell_type_total_mean_data = pd.concat([cell_type_total_mean_data, mean_data], join='outer', axis=1)

with open('expresse_gene_count_Cell_type.txt', 'w') as op:
    op.write(str(cell_type_expresse_gene_count_list))
cell_type_total_mean_data.to_csv("total_mean_Cell_type.csv", index=False)
