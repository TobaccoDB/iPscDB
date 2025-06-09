import os

import requests
from requests_toolbelt import MultipartEncoder
from requests.adapters import HTTPAdapter
import pandas as pd
import discotoolkit as dt


REF_PATH = '/home/Data_analyse/Cellid_REF/'

def get_cell_type(file_path,speices_name, tissue):
    count_cmd_path = '/home/Data_analyse/ref_data/Default'   
    df = pd.read_csv(file_path, index_col=0)
    try:
        cell_type_df = dt.CELLiD_cluster(rna = df, n_predict = 2, ref_path = count_cmd_path)
        cell_type = cell_type_df['predicted_cell_type_1'].to_dict()

        cell_type = {key: value.replace("\\", "") for key, value in cell_type.items()}
        
        
    except Exception as e:
        print(e)
        cell_type = {}
    
    
    return cell_type
    
    


    
