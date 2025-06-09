# import scanpy as sc

# df = sc.read_h5ad("/root/data/05_Atlas_H5/D5_Atha_Hypocotyl_callus.h5ad")
# df = df.to_df()
# print(df)
# print(df.columns)

import anndata
from mtsc import mtSC
import os
import warnings
import pandas as pd
import numpy as np
import torch
from plant_marker import settings

warnings.filterwarnings("ignore")

SAVE_PATH = '/data/Tools/mtSC/checkpoints/'
DATA_PATH = '/root/data/05_Atlas_H5/'


def test(model, test_data, metrics_list, labels_list):
    test_data = torch.tensor(test_data.values,
                             dtype=torch.float32)
    max_likelihood_lists = []
    max_likelihood_classes = []
    for l in range(len(metrics_list)):
        max_likelihood_list, max_likelihood_class = mtSC.one_model_predict(
            test_data, model, metrics_list[l], labels_list[l])
        max_likelihood_lists.append(max_likelihood_list)
        max_likelihood_classes.append(max_likelihood_class)
        # calculate f1_score
    pred_class = []
    max_likelihood_indices = np.argmax(max_likelihood_lists, axis=0)
    for k in range(len(max_likelihood_indices)):
        max_likelihood_indice = max_likelihood_indices[k]
        pred_class.append(max_likelihood_classes[max_likelihood_indice][k])
    return pred_class


def transfer(adata):
    x = adata.to_df()
    obs = adata.obs
    var = adata.var
    df = x.merge(obs[['Celltype']], left_index=True, right_index=True)
    return df.rename(columns=str.lower)


def run_mtsc(reference_data, test_adata):
    # 数据处理
    save_dir = os.path.join(SAVE_PATH, reference_data)
    gene_path = 'gene_list.txt'
    with open(os.path.join(save_dir, gene_path), 'r') as file:
        gene_list = [line.strip() for line in file]
    # print('gene list shape:', len(gene_list))
    feature_num = len(gene_list)

    test_df = transfer(test_adata)

    test_genes = test_df.columns
    # print(test_genes)
    add_gene = []
    for gene_ in gene_list:
        if gene_ not in test_genes:
            add_gene.append(gene_)
    # print('add gene shape:', list(add_gene))

    add_df = pd.DataFrame(np.zeros((test_df.shape[0], len(add_gene))), index=test_df.index, columns=add_gene)
    processed_df = pd.concat([test_df, add_df], axis=1)
    processed_df = processed_df.loc[processed_df.index.tolist(), gene_list]

    # test_dataset_list = [processed_df]

    # 加载模型
    model = mtSC.Net(feature_num)
    model.load_state_dict(torch.load(os.path.join(save_dir, 'model.pth')))

    # 加载metric
    metrics_list = []
    labels_list = []
    npzfile = np.load(os.path.join(save_dir, 'metrics_and_labels.npz'), allow_pickle=True)
    metrics_list.append(npzfile['metrics'])
    labels_list.append(npzfile['labels'])

    pred_class = test(model, processed_df, metrics_list, labels_list)
    # print('len(index)',len(processed_df.index))
    # print('pred_class',len(pred_class))
    result = pd.DataFrame({'cell': processed_df.index, 'cell_type': pred_class})
    result.set_index('cell', inplace=True)
    # print(result.columns)

    return result

    # for test_data in range(test_dataset_list):
    #     pred_class = test(model, test_data, metrics_list, labels_list)

    #     with open('result.txt','a') as result_file:
    #         for pred_class_indice in range(len(pred_class)):
    #             result_file.write(str(test_data.index[pred_class_indice])+'\t'+str(pred_class[pred_class_indice])+'\n')


if __name__ == '__main__':
    # train('Dt_061_SRP339472')
    # train('Dt_024_SRP279055')
    # train('D5_Atha_Hypocotyl_callus')
    test_adata = anndata.read_h5ad("/root/data/05_Atlas_H5/Dt_061_SRP339472.h5ad")
    print(run_mtsc('Dt_061_SRP339472', test_adata))
