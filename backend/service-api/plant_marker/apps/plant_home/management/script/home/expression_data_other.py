import pandas as pd
import os
from datetime import datetime

base_dir = 'D:/项目文档/基因检测/源数据/Oryza_sativa_Root/Root'

# 读取 Cell_cluster 数据
# cell_cluster_path = os.path.join(base_dir, "cell_cluster.txt")
# cell_cluster_data = pd.read_csv(cell_cluster_path, sep=r"\t", usecols=['"cell_type"', '"seurat_clusters"'])


# 格式化数据
def gene_replace(x):
    return str(x).replace('"', '')


def Cell_Id_Format(cell_id):
    return str(cell_id).replace("@", ".")


# cell_cluster_rename_columns_data = {
#     '"cell_type"': 'Cell_type',
#     '"seurat_clusters"': 'Clusters',
# }
# cell_cluster_data = cell_cluster_data.rename(columns=cell_cluster_rename_columns_data)
# cell_cluster_data['Clusters'] = cell_cluster_data['Clusters'].apply(gene_replace)
# cell_cluster_data['Cell_type'] = cell_cluster_data['Cell_type'].apply(gene_replace)
# # 将索引转换成 Cell_ID 列
# cell_cluster_data['Cell_ID'] = cell_cluster_data.index
# print(cell_cluster_data)


# 读取表达值
expression_path = os.path.join(base_dir, "D4_GEMatrix.txt")
# expression = pd.read_csv(expression_path, sep=r"\t")
expression = pd.read_csv(expression_path, sep=r"\t", chunksize=100, engine='python')
print(expression)
save_dir = './expression_data/'

for chunk in expression:
    try:
        expression_data = chunk.T
        expression_data['index'] = expression_data.index
        expression_data['index'] = expression_data['index'].apply(gene_replace)
        # expression_data = expression_data.reset_index()
        print(expression_data)
        column_name_list = expression_data.columns.values.tolist()
        column_name_list.remove('index')
        for column_name in column_name_list:
            save_name = column_name.replace('"', '') + '.csv'
            save_name = os.path.join(save_dir, save_name)
            print(save_name)
            if not os.path.exists(save_name):
                rename_columns_data = {
                    'index': 'Cell_ID',
                    column_name: 'value',
                }
                column_expression_data = expression_data[["index", column_name]]
                column_expression_data = column_expression_data.rename(columns=rename_columns_data)
                column_expression_data['Cell_ID'] = column_expression_data['Cell_ID'].apply(Cell_Id_Format)
                # 根据 Cell_ID 合并 expression_data 和 cell_cluster_data
                # expression_data = pd.merge(expression_data, cell_cluster_data, how='left', on='Cell_ID')
            
                column_expression_data.to_csv(save_name, index=False)

    except Exception as e:
        print(e)
        continue
