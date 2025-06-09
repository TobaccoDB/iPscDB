import os, django

from django.db.models import Q

from plant_marker import settings

django.setup()

from django.core.management import BaseCommand
from plant_marker.apps.plant_home.models import *


# 生成首页物种数据
class Command(BaseCommand):
    def handle(self, *args, **options):
        cell_type_relations_queryset = CellTypeRelations.objects.all()

        species_list = cell_type_relations_queryset.values('species_name').exclude(
            Q(species_name__isnull=True) | Q(species_name='')
        ).distinct()

        result_data = []
        for species_item in species_list:
            species_name = str(species_item['species_name']).replace(" ", "_").replace(".","").replace("×", "x")
            tissue_data = []
            species_whole_plant = {
                # 整株数据
                "Tissue": "WholePlant",
                "tissue_label": "Whole Plant",
                "tissue_head_link": '',
                # "download_rds_link": '',
                'is_show': '1'
            }
            tissue_data.append(species_whole_plant)
            # 获取二级节点名称集合
            tissue_list = cell_type_relations_queryset.filter(species_name=species_item['species_name']).values(
                'tissue_name').distinct()
            for tissue_item in tissue_list:
                if tissue_item['tissue_name'] == 'Unknown':
                    continue
                tissue_name = str(tissue_item['tissue_name']).replace(" ", "_").replace(";", "_")
                tissue = {
                        "Tissue": tissue_name,
                        "tissue_label": tissue_item['tissue_name'],
                        "tissue_head_link": settings.BASE_URL + 'source_material/'+species_name+'/'+tissue_name+'/'+tissue_name+'.png',
                        # "download_rds_link": settings.PROJECT_DOWNLOAD_RDS+species_name+'/'+tissue_name+'/'+tissue_name+'.rds',
                        'is_show': '1'
                    }

                tissue_data.append(tissue)
            species = {
                "name": species_name,
                "label": species_item['species_name'],
                'species_whole_plant': settings.BASE_URL + 'source_material/{}/{}.png'.format(species_name, species_name),
                "data": tissue_data
            }
            result_data.append(species)
        print(result_data)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_marker.settings')
    Command().handle()