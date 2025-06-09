import os
import xlrd
from plant_marker.apps.plant_home.models import *
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        cell_type_queryset = CellType.objects.all()
        tissue_queryset = TissueType.objects.all()
        cell_marker_queryset = CellMarkerInfo.objects.all()
        literature_queryset = LiteratureInfo.objects.all()
        with transaction.atomic():
            # lit_list = ['Root', 'Leaf', 'Shoot']
            # lit_list = ['Embryos']
            lit_list = ['LT58']
            for lit in lit_list:
                path = os.path.join(settings.EXCEL_FILE, '{}_umap_infos.xlsx'.format(lit))
                data1 = xlrd.open_workbook(path)
                sheet1 = data1.sheet_by_name('Sheet1')
                nrows1 = sheet1.nrows
                for r1 in range(1, nrows1):
                    row1 = sheet1.row_values(r1)
                    cell_type_obj = cell_type_queryset.filter(cell_name_lit=row1[1]).first()
                    if cell_type_obj:
                        cell_name = cell_type_obj.cell_name
                        cell_po = cell_type_obj.cell_po
                        if tissue_queryset.filter(tiss_name_lit=cell_type_obj.tiss_id):
                            po_num = tissue_queryset.filter(tiss_name_lit=cell_type_obj.tiss_id).first().po_num
                        else:
                            po_num = ''
                    else:
                        cell_name = ''
                        cell_po = ''
                        po_num = ''
                    if cell_marker_queryset.filter(cell_id=row1[1]):
                        if literature_queryset.filter(
                                lit_id=cell_marker_queryset.filter(cell_id=row1[1]).first().lit_id):
                            doi = literature_queryset.filter(
                                lit_id=cell_marker_queryset.filter(cell_id=row1[1]).first().lit_id).first().doi
                    else:
                        doi = ''
                    gene_id_obj_list = list(
                        set(cell_marker_queryset.filter(cell_id=row1[1],
                                                        species_name='Arabidopsis_thaliana').values_list('gene_id',
                                                                                                         flat=True)))[
                                       0:6]
                    kwargs_dict = {
                        'lit_id': lit,
                        'clusters': int(row1[0]),
                        'cluster_name': row1[1],
                        'cell_name': cell_name,
                        'cell_po': cell_po,
                        'po_num': po_num,
                        'gene_id': ','.join(gene_id_obj_list),
                        'doi': doi,
                        'tissue_id': 'Root',
                        'species_name': "Arabidopsis_thaliana"
                    }
                    print(kwargs_dict)
                    species_post = ProjrctAtlasCellType.objects.create(**kwargs_dict)
                    species_post.save()
