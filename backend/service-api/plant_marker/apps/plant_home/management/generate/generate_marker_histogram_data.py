import os, django
django.setup()

from django.core.management import BaseCommand
from plant_marker.apps.plant_home.models import *


# 生成Marker 柱状图数据
class Command(BaseCommand):
    def handle(self, *args, **options):
        cell_type_relations_queryset = CellTypeRelations.objects.all()
        classic_markers_queryset = ClassicMarkersInfo.objects.all()
        marker_genes_queryset = MarkerGenesInfo.objects.all()

        species_list = cell_type_relations_queryset.values('species_name').distinct()
        histogram_data = []
        for species in species_list:
            # 根据物种获取物种下面的Cell
            dict_list = marker_genes_queryset.filter(species=species['species_name']).values('clusterName').distinct()
            cell_list = []
            for cell in dict_list:
                # Marker gene 数量
                marker_number = marker_genes_queryset.filter(
                    species=species['species_name'], clusterName=cell['clusterName'],
                ).count()
                # Classic Marker 数量
                classic_number = classic_markers_queryset.filter(
                    species_name=species['species_name'], cell_id=cell['clusterName']
                ).count()
                total = marker_number + classic_number
                cell_data = {
                    "name": cell['clusterName'],
                    "gene_number": marker_number,
                    "classic_number": classic_number,
                    "total": total
                }
                cell_list.append(cell_data)

            cell_list = sorted(cell_list, key=lambda x: x['total'], reverse=True)

            species_data = {
                "species_name": species['species_name'],
                "children": cell_list,
            }
            histogram_data.append(species_data)
        print(histogram_data)


if __name__ == '__main__':
    Command().handle()
