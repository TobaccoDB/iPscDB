import os
import xlrd
import csv
import uuid
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from plant_marker.apps.plant_home.models import *
import time
import random
import django
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            path = os.path.join(settings.EXCEL_FILE, 'create_cluster_marker_22_09.xlsx')
            data1 = xlrd.open_workbook(path)
            sheet1 = data1.sheet_by_name('Sheet1')
            nrows1 = sheet1.nrows
            for r1 in range(1, nrows1):
                print(r1)
                row1 = sheet1.row_values(r1)
                kwargs_dict = {
                    'species_name': str(row1[0]).replace(' ', '_'),
                    'tissue_id': row1[1],
                    'cell_type': row1[2],
                    'gene_id': row1[3],
                    'cluster_marker': row1[4],
                    'gene_id_other': row1[5],
                    'lit_id': row1[6],
                }
                print(kwargs_dict)
                species_post = ClusterMarkerInfo.objects.create(**kwargs_dict)
                species_post.save()
            print('done')


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
