import os
import re
import discotoolkit as dt
import scanpy as sc
import anndata
import pandas as pd
import numpy as np
from plant_marker import settings
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

SAVE_PATH = '/data/Tools/CelliD/checkpoints/'
DATA_PATH = '/root/data/05_Atlas_H5/'
REF_PATH = '/data/Tools/CelliD/ref/'


def get_integrated_data(cell):
    for col in cell.obs.columns:
        new_col = re.sub(r'\.', '_', col)
        cell.obs.rename(columns={col: new_col}, inplace=True)

    # Rename columns with periods in `.var` attribute
    for col in cell.var.columns:
        new_col = re.sub(r'\.', '_', col)
        cell.var.rename(columns={col: new_col}, inplace=True)

    # apply normalise to the count data gene expression
    ### Ignore this if the data has been normalised
    ### please exponentiate if the data is in log-space
    sc.pp.normalize_total(cell, target_sum=1e4)
    norm_temp = cell.X

    # convert into dataframe for adding metadata
    temp = pd.DataFrame(norm_temp.toarray(), columns=list(cell.var.index))

    temp["cluster"] = np.array(cell.obs["Seurat_clusters"])  # get the cluster metadata from
    integrated_data = temp.groupby("cluster").mean().transpose()  # get the average expression for each cluster

    return integrated_data


def run_cell_id(reference_data):
    cell_adata = anndata.read_h5ad(os.path.join(DATA_PATH, reference_data + '.h5ad'))
    print(f"======== Data {reference_data} loaded successfully. ========")
    # get the integrated data
    integrated_data = get_integrated_data(cell_adata)
    print(f"======== Data {reference_data} integrated successfully.========")
    # cell annotation
    """
    Cell type annotation using reference data and compute the correlation between the user cell gene expression as compare
        to the reference data. The celltype with highest correlation will be concluded as the celltype

    Args:
        rna (Pandas DataFrame | Numpy array): user define dataframe. Need to transpose so that the index is the genes
        ref_data (Pandas DataFrame, optional): Reference dataframe used to compute for the cell type annotation. Defaults to None.
        ref_deg (Pandas DataFrame): reference DEG database. Defaults to None.
        atlas (String, optional): String of atlas that the user want to use as the reference. Defaults to None.
        n_predict (Integer, optional): number of predicted celltype. Defaults to 1.
        ref_path (string, optional): path string to the reference data. Defaults to None.
        ncores (Integer, optional): number of CPU cores used to run the data. Defaults to 10.

    Returns:
        Pandas DataFrame: return the Pandas DataFrame along with the correlation score.
    """
    cell_type = dt.CELLiD_cluster(rna=integrated_data, n_predict=3, ref_path=REF_PATH)
    print(f"======== Data {reference_data} annotated successfully.=======")
    # save the cell type
    annoted_data = 'cell_type.csv'
    save_dir = os.path.join(SAVE_PATH, reference_data)
    os.makedirs(save_dir, exist_ok=True)

    return cell_type


if __name__ == '__main__':
    cell_type = run_cell_id('Dt_004_SRP182008')
    print(cell_type)
    cell_type.to_csv("cell_id_result.txt", sep="\t")
