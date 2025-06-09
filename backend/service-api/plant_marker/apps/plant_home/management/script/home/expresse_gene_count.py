import pandas as pd
import os


def cell_type_data():
    # 读取 total_mean_Cell_type 数据 
    cell_type_data = pd.read_csv("total_mean_Cell_type.csv")
    cell_type_list = list(cell_type_data.columns.tolist())
    cell_type_expresse_gene_count_list = []
    for cell_type in cell_type_list:
        cell_type_mean_data = cell_type_data[[cell_type]]
        cell_type_mean_data = cell_type_mean_data[cell_type_mean_data[cell_type] > 0]
        cell_type_dict = {
           cell_type: cell_type_mean_data.shape[0]
        }
        cell_type_expresse_gene_count_list.append(cell_type_dict)
    print(cell_type_expresse_gene_count_list)
    with open('expresse_gene_count_Cell_type.txt', 'w') as op:
        op.write(str(cell_type_expresse_gene_count_list))


def cluster_data():
    # 读取 total_mean_Clusters 数据 
    cluster_data = pd.read_csv("total_mean_Clusters.csv")
    cluster_list = list(cluster_data.columns.tolist())
    cluster_expresse_gene_count_list = []
    for cluster in cluster_list:
        cluster_mean_data = cluster_data[[cluster]]
        cluster_mean_data = cluster_mean_data[cluster_mean_data[cluster] > 0]
        cluster_dict = {
           cluster: cluster_mean_data.shape[0]
        }
        cluster_expresse_gene_count_list.append(cluster_dict)
    print(cluster_expresse_gene_count_list)
    with open('expresse_gene_count_Clusters.txt', 'w') as op:
        op.write(str(cluster_expresse_gene_count_list))


def sample_data():
    # 读取 total_mean_Project_ID 数据 
    sample_data = pd.read_csv("total_mean_Project_ID.csv")
    sample_list = list(sample_data.columns.tolist())
    sample_expresse_gene_count_list = []
    for sample in sample_list:
        sample_mean_data = sample_data[[sample]]
        sample_mean_data = sample_mean_data[sample_mean_data[sample] > 0]
        sample_dict = {
           sample: sample_mean_data.shape[0]
        }
        sample_expresse_gene_count_list.append(sample_dict)
    print(sample_expresse_gene_count_list)
    with open('expresse_gene_count_Project_ID.txt', 'w') as op:
        op.write(str(sample_expresse_gene_count_list))


if __name__ == "__main__":

    cell_type_data()
    cluster_data()
    sample_data()
