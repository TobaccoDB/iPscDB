import os
import xlrd
from plant_marker.apps.plant_home.models import *
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            path = os.path.join('D:\免疫单细胞数据库\sample_ click_rds\sample_ click_rds')
            for root, dirs, files in os.walk(path):
                pass
            l = list(set(files))
            lst = [i.split('.')[0] for i in l]
            for i in lst:
                kwargs_dict = {
                    'sample_id': i,
                }
                print(kwargs_dict)
                species_post = SampleRdsDownload.objects.create(**kwargs_dict)
                species_post.save()
