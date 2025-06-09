# import warnings
# import anndata
# import Cell_BLAST as cb
# import os
#
# from plant_marker import settings
#
# DATA_PATH = '/root/data/05_Atlas_H5/'
# SAVE_PATH = '/data/Tools/mtSC/checkpoints/'
# cb.config.N_JOBS = 4
# cb.config.RANDOM_SEED = 0
# epoch = 4
# warnings.filterwarnings("ignore")
#
#
# def run_cell_blast(reference_data, test_data):
#     save_path = os.path.join(SAVE_PATH, reference_data)
#     blast = cb.blast.BLAST.load(save_path)
#     test_hits = blast.query(test_data)
#     print(test_hits)
#     test_hits = test_hits.reconcile_models().filter(by="pval", cutoff=0.05)
#     test_predictions = test_hits.annotate("Celltype")
#     return test_predictions
#
#
# if __name__ == '__main__':
#     # train('Dt_061_SRP339472.h5ad')
#     # train('Dt_024_SRP279055')
#     test_data = anndata.read_h5ad("/root/data/05_Atlas_H5/D5_Atha_Inflorescence.h5ad")
#
#     data = run_cell_blast('Dt_024_SRP279055', test_data)
#     data["cele_name"] = data.index
#     print(data)
#     data.to_csv("Cell_Blast_Result.txt", sep="\t")
