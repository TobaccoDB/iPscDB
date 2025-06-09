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
import pymysql
import pandas as pd
import math
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            path = os.path.join(settings.EXCEL_FILE, 'create_cell_type_22_09.xlsx')
            data1 = xlrd.open_workbook(path)
            sheet1 = data1.sheet_by_name('Sheet1')
            nrows1 = sheet1.nrows
            for r1 in range(1, nrows1):
                row1 = sheet1.row_values(r1)
                kwargs_dict = {
                    'cell_id': row1[0],
                    'cell_name_lit': row1[1],
                    'cell_name': row1[2],
                    'cell_po': row1[3],
                    'tiss_id':str( row1[4]).split('.')[0],
                }
                print(kwargs_dict)
                species_post = CellType.objects.create(**kwargs_dict)
                species_post.save()
