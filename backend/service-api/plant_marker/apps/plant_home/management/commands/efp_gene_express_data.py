import os
import xlrd
from plant_marker.apps.plant_home.models import *
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            path = os.path.join(settings.EXCEL_FILE, 'efp_gene_express_data.xlsx')
            data1 = xlrd.open_workbook(path)
            sheet1 = data1.sheet_by_name('Sheet1')
            nrows1 = sheet1.nrows
            for r1 in range(1, nrows1):
                row1 = sheet1.row_values(r1)
                kwargs_dict = {
                    'class_name': row1[0],
                    'tissue': row1[1],
                    'value': int(row1[2]),
                    'species_name': 'Arabidopsis_thaliana',
                    'gene_id': 'AT1G01070',
                }
                print(kwargs_dict)
                species_post = EfpGeneExpress.objects.create(**kwargs_dict)
                species_post.save()
