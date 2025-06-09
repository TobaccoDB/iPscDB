import os, django

from django.db.models import Q, Sum, Count

from plant_marker import settings

django.setup()

from django.core.management import BaseCommand
from plant_marker.apps.plant_home.models import *


# 生成Atlas页面数据
class Command(BaseCommand):
    def handle(self, *args, **options):
        cell_type_relations_queryset = CellTypeRelations.objects.all()
        sra_information_queryset = SraInformation.objects.all()
        marker_queryset = MarkerGenesInfo.objects.all()

        species_list = sra_information_queryset.values('species').annotate(
            cell_total=Sum('cells'),dataset_count=Count('dataset', distinct=True)
        ).order_by('species')
        # 物种数据
        species_data = []
        for species_item in species_list:
            species_name = str(species_item['species']).replace(" ", "_").replace(".","").replace("×", "x")
            cells_count = '{:,.0f}'.format(species_item['cell_total']) if species_item['cell_total'] else 'Processing'
            dataset_count = species_item['dataset_count'] if species_item['dataset_count'] else 0
            species = {
                "name": species_name,
                "label": species_item['species'],
                "Tissue": "WholePlant",
                "tissue_label": "Whole Plant",
                "cell": cells_count,
                "dataset": dataset_count,
                'species_whole_plant': settings.BASE_URL + 'source_material/{}/{}.png'.format(species_name, species_name),
                "download_rds_link": settings.BASE_URL + 'source_material/{}/{}.rds'.format(species_name, species_name),
            }
            species_data.append(species)

        # 组织数据
        tissue_list = cell_type_relations_queryset.values('species_name', 'tissue_name').distinct().order_by("species_name")

        tissue_data = []
        for tissue_item in tissue_list:
            if tissue_item["tissue_name"] == "Unknown" or tissue_item["tissue_name"] == "Unknow" or tissue_item["tissue_name"] == "Uknown":
                continue

            species_name = str(tissue_item['species_name']).replace(" ", "_").replace(".","").replace("×", "x")
            tissue_name = str(tissue_item['tissue_name']).replace(" ", "_").replace(";", "_")
            # 获取对应物种对应组织下面的Cell数量
            cells = sra_information_queryset.filter(
                species=tissue_item['species_name'], tissue=tissue_item['tissue_name']
            ).aggregate(cell_total=Sum('cells'))
            cells_count = '{:,.0f}'.format(cells['cell_total']) if cells['cell_total'] else 'Processing'
            # Cell Type 数量
            tissue_sub_node_total = cell_type_relations_queryset.filter(
                species_name=tissue_item['species_name'], tissue_name=tissue_item['tissue_name']
            ).exclude(Q(l1__isnull=True) | Q(l1='')).count()

            tissue = {
                "name": species_name,
                "label": tissue_item['species_name'],
                "Tissue": tissue_name,
                "tissue_label": tissue_item['tissue_name'],
                "cell": cells_count,
                "cell_type": tissue_sub_node_total,
                "tissue_head_link": settings.BASE_URL + 'source_material/{}/{}/{}.png'.format(species_name, tissue_name, tissue_name),
                "download_rds_link": settings.BASE_URL + 'source_material/{}/{}/{}.rds'.format(species_name, tissue_name, tissue_name),
            }
            tissue_data.append(tissue)
        result_data = {
            'species_data': species_data,
            'tissue_data': tissue_data
        }
        print(result_data)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_marker.settings')
    Command().handle()
