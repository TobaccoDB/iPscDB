import os
import xlrd
from plant_marker.apps.plant_home.models import *
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            path = os.path.join(settings.EXCEL_FILE, 'cell_identification_datas.xlsx')
            data1 = xlrd.open_workbook(path)
            sheet1 = data1.sheet_by_name('Sheet1')
            nrows1 = sheet1.nrows
            for r1 in range(1, nrows1):
                row1 = sheet1.row_values(r1)
                kwargs_dict = {
                    'species_name': row1[0],
                    'title': row1[1],
                    'pdf_name': row1[2],
                    'scope_url': row1[3],
                    'project_id': row1[4],
                    'lit_id': row1[5],
                    'rds_name': row1[6]
                }
                print(kwargs_dict)
                species_post = CellIdentificationInfo.objects.create(**kwargs_dict)
                species_post.save()
