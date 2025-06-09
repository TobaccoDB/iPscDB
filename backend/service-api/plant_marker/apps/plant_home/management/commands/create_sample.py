import os
import xlrd
from plant_marker.apps.plant_home.models import *
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            path = os.path.join(settings.EXCEL_FILE, 'sample_data_23-02.xlsx')
            data1 = xlrd.open_workbook(path)
            sheet1 = data1.sheet_by_name('Sheet1')
            nrows1 = sheet1.nrows
            for r1 in range(1, nrows1):
                print(r1)
                row1 = sheet1.row_values(r1)
                kwargs_dict = {
                    'sam_id': row1[0],
                    'species_name': str(row1[1]).replace(' ', '_') if ' ' in str(row1[1]) else row1[1],
                    'project_id': row1[2],
                    'sample_id': row1[3],
                    'sample_name': row1[4],
                    'geno_type': row1[5],
                    'treament': row1[6] if row1[6] != 'None' else '',
                    'ecotype': row1[7],
                    'age': row1[8],
                    'tissue': row1[9],
                    'chemistry': row1[10],
                    'lit_id': row1[11],
                    'qc_check': row1[12],
                    'qc_cells': int(row1[13]) if row1[13] else 0,
                }
                print(kwargs_dict)
                species_post = Sample.objects.create(**kwargs_dict)
                species_post.save()
