import os

import requests
from requests_toolbelt import MultipartEncoder
from requests.adapters import HTTPAdapter


def get_cell_type(file_path, species_name, tissue):
    try:
        url = "http://172.16.17.7:80/server_plant_marker/api/v1/get_cell_id_data/"
        print(file_path, species_name, tissue)
        m = MultipartEncoder(
            fields={
                'species': str(species_name).replace('_', ' '),
                'tissue': tissue if tissue else "Root",
                'file': ('filename', open(file_path, 'rb'), 'text/plain')
            }
        )

        s = requests.Session()
        # 设置重试次数
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))

        response = s.request("POST", url, data=m, headers={'Content-Type': m.content_type}, timeout=600)
        print(response)
        if response.status_code == 200:
            # 获取原始数据
            table_data = response.json().get('data', {}).get('table_data', {})
            cluster_to_celltype = {
                str(data['input_index']): data['predicted_cell_type_1'] for data in table_data
            }
        else:
            # cluster_to_celltype = {
            #     '0': 'Xylem pole pericycle',
            #     '1': 'Root hair',
            #     '2': 'Metaxylem',
            #     '3': 'Lateral root cap',
            #     '4': 'Root cap',
            #     '5': 'Root endodermis',
            #     '6': 'Xylem pole pericycle',
            #     '7': 'Phloem pole pericycle',
            #     '8': 'Non-hair',
            #     '9': 'Phloem pole pericycle',
            #     '10': 'Lateral root cap',
            #     '11': 'Protoxylem',
            #     '12': 'Metaxylem',
            #     '13': 'Root cortex',
            #     '14': 'Non-hair',
            #     '15': 'Phloem pole pericycle',
            #     '16': 'Phloem pole pericycle',
            #     '17': 'Lateral root cap',
            #     '18': 'S phase',
            #     '19': 'Root cortex',
            #     '20': 'Phloem pole pericycle',
            #     '21': 'Root hair',
            #     '22': 'Phloem pole pericycle',
            #     '23': 'Protoxylem'
            # }
            cluster_to_celltype = {
                '0': 'No Cell',
                '1': 'No Cell',
                '2': 'No Cell',
                '3': 'No Cell',
                '4': 'No Cell',
                '5': 'No Cell',
                '6': 'No Cell',
                '7': 'No Cell',
                '8': 'No Cell',
                '9': 'No Cell',
                '10': 'No Cell',
                '11': 'No Cell',
                '12': 'No Cell',
                '13': 'No Cell',
                '14': 'No Cell',
                '15': 'No Cell',
                '16': 'No Cell',
                '17': 'No Cell',
                '18': 'No Cell',
                '19': 'No Cell',
                '20': 'No Cell',
                '21': 'No Cell',
                '22': 'No Cell',
                '23': 'No Cell'
            }
    except Exception as e:
        print('eeeeeeeeee',e)
        cluster_to_celltype = {
            '0': 'No Cell',
            '1': 'No Cell',
            '2': 'No Cell',
            '3': 'No Cell',
            '4': 'No Cell',
            '5': 'No Cell',
            '6': 'No Cell',
            '7': 'No Cell',
            '8': 'No Cell',
            '9': 'No Cell',
            '10': 'No Cell',
            '11': 'No Cell',
            '12': 'No Cell',
            '13': 'No Cell',
            '14': 'No Cell',
            '15': 'No Cell',
            '16': 'No Cell',
            '17': 'No Cell',
            '18': 'No Cell',
            '19': 'No Cell',
            '20': 'No Cell',
            '21': 'No Cell',
            '22': 'No Cell',
            '23': 'No Cell'
        }

    return cluster_to_celltype
