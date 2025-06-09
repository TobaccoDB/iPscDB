import os
import xlrd
from plant_marker.apps.plant_home.models import *
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            path = os.path.join(settings.EXCEL_FILE, 'literature_data_22_10.xlsx')
            data1 = xlrd.open_workbook(path)
            sheet1 = data1.sheet_by_name('Sheet1')
            nrows1 = sheet1.nrows
            for r1 in range(1, nrows1):
                row1 = sheet1.row_values(r1)
                kwargs_dict = {
                    'lit_id': row1[0],
                    'species_name': str(row1[1]).replace(' ', '_') if ' ' in str(row1[1]) else row1[1],
                    'pmid': int(row1[2]) if row1[2] else '',
                    'doi': row1[3],
                    'title': row1[4],
                    'year': str(row1[5]).split('.')[0],
                    # 'data_type': row1[6],
                    # 'download': row1[7],
                    # 'unzip': row1[8],
                    # 'cell_ranger': row1[9],
                    # 'qc': row1[10],
                }
                print(kwargs_dict)
                species_post = LiteratureInfo.objects.create(**kwargs_dict)
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
