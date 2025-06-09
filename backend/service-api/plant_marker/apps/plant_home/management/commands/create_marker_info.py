import os
import xlrd
from plant_marker.apps.plant_home.models import *
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            path = os.path.join(settings.EXCEL_FILE, 'marker_info_leaf.xlsx')
            data1 = xlrd.open_workbook(path)
            sheet1 = data1.sheet_by_name('Sheet1')
            nrows1 = sheet1.nrows
            for r1 in range(1, nrows1):
                row1 = sheet1.row_values(r1)
                kwargs_dict = {
                    'p_va1': 0 if float(row1[0]) == 0.0 else float(row1[0]),
                    'log_2fc': float(row1[1]),
                    'pct1': float(row1[2]),
                    'pct2': float(row1[3]),
                    'p_val_adj': 0 if float(row1[4]) == 0.0 else float(row1[4]),
                    'cluster_id': int(row1[5]),
                    'gene_id': row1[6],
                    'cell_type': row1[7],
                    'tissue': 'Leaf',

                }
                print(kwargs_dict)
                species_post = MarkerInfo.objects.create(**kwargs_dict)
                species_post.save()


"""
[{
  name: 'Female1',
 data:[[172.5, 55.2], [170.9, 54.2]]
},
{
  name: 'Female2',
 data:[[1.5, 5.2], [17.9, 5.2]]
}]

"""
