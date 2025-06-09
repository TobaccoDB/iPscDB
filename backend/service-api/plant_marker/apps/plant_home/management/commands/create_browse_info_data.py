import os
import xlrd
from plant_marker.apps.plant_home.models import *
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        literature_queryset = LiteratureInfo.objects.all()
        sample_queryset = Sample.objects.all()
        with transaction.atomic():
            for obj in literature_queryset:
                if obj.lit_id == 'LT22':
                    lit_id = 'LT22, LT24'
                elif obj.lit_id == 'LT24':
                    lit_id = 'LT22, LT24'
                else:
                    lit_id = obj.lit_id
                project_id = ','.join(
                    set(list(sample_queryset.filter(lit_id=lit_id).values_list('project_id',
                                                                               flat=True))))
                tissue = ','.join(
                    set(list(sample_queryset.filter(lit_id=lit_id).values_list('tissue',
                                                                               flat=True))))
                chemistry = ','.join(
                    set(list(sample_queryset.filter(lit_id=lit_id).values_list('chemistry',
                                                                               flat=True))))
                qc_cells = sum([int(i) for i in
                                list(sample_queryset.filter(lit_id=lit_id).values_list('qc_cells',
                                                                                       flat=True))])
                kwargs_dict = {
                    'lit_id': obj.lit_id,
                    'species_name': obj.species_name,
                    'pmid': obj.pmid,
                    'doi': obj.doi,
                    'title': obj.title,
                    'project_id': project_id,
                    'tissue': tissue,
                    'chemistry': chemistry,
                    'qc_cells': qc_cells
                    ,
                }
                print(kwargs_dict)
                species_post = BrowseInfo.objects.create(**kwargs_dict)
                species_post.save()
