import csv
import os, django
import pandas as pd

django.setup()

from django.core.management import BaseCommand
from plant_marker.apps.plant_home.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        cell_type_details_queryset = CellTypeDetails.objects.all()
        marker_gene_queryset = MarkerGenesInfo.objects.all()

        base_dir = 'F:/data/基因数据'
        file_name = "cellTypeId.csv"
        file_path = os.path.join(base_dir, file_name)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            reader = pd.read_csv(file)
            null_list = []
            for index, row in reader.iterrows():
                id = row['id']
                cell_type_id = row['celltype_id']
                if pd.isna(cell_type_id) or not cell_type_id:
                    continue
                species = row['species'].replace(" ", "_")
                cell_type_list = cell_type_id.split('->')
                new_cell_type_id = species.lower()
                for cell_type in cell_type_list:
                    po_id_dict = cell_type_details_queryset.filter(name=cell_type).values("po_id").distinct()
                    if not po_id_dict:
                        po_id = 'PO:@@@@'
                        cell = {
                            'cell_type_id': cell_type
                        }
                        null_list.append(cell)
                    else:
                        po_id = po_id_dict[0]['po_id']
                    new_cell_type_id = new_cell_type_id + "->" + po_id
                print("第{}行，ID：{}，物种：{}，原cell_id：{}，新cell_id：{}".format(index + 1, id, species, cell_type_id, new_cell_type_id))
                marker_data = marker_gene_queryset.get(id=id)
                marker_data.celltype_id = new_cell_type_id
                marker_data.save()

            df = pd.DataFrame(null_list)
            file_path = os.path.join(base_dir, "not_query.csv")
            df.to_csv(file_path)
        print("读取文件完成！")


if __name__ == '__main__':
    Command().handle()
