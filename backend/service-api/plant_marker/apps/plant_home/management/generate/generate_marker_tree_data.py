import os, django

from django.db.models import Q
from plant_marker import settings

django.setup()

from django.core.management import BaseCommand
from plant_marker.apps.plant_home.models import *


# 生成MarkerTree数据
class Command(BaseCommand):
    def handle(self, *args, **options):
        cell_type_relations_queryset = CellTypeRelations.objects.all()
        classic_markers_queryset = ClassicMarkersInfo.objects.all()
        marker_genes_queryset = MarkerGenesInfo.objects.all()

        species_list = cell_type_relations_queryset.values('species_name').exclude(
            Q(species_name__isnull=True) | Q(species_name='')
        ).distinct()
        tree_list = []
        # Tree数据
        for species_item in species_list:
            # 格式化物种名称
            icon_species = str(species_item['species_name']).replace(" ", "_").replace(";", "_").replace(".","").replace("×", "x")
            # 二级数据
            tissue_node_list = []
            # 获取二级节点名称集合
            tissue_list = cell_type_relations_queryset.filter(species_name=species_item['species_name']).values(
                'tissue_name').distinct()
            for tissue_item in tissue_list:
                # 三级节点数据
                l1_node_list = []
                # 获取三级节点名称集合
                l1_list = cell_type_relations_queryset.filter(
                    species_name=species_item['species_name'], tissue_name=tissue_item['tissue_name']
                ).exclude(Q(l1__isnull=True) | Q(l1='')).values('l1').distinct()
                # 存在三级节点数据
                if l1_list:
                    for l1_item in l1_list:
                        # 四级节点数据
                        l2_node_list = []
                        l2_list = cell_type_relations_queryset.filter(
                            species_name=species_item['species_name'], tissue_name=tissue_item['tissue_name'],
                            l1=l1_item['l1']
                        ).exclude(Q(l2__isnull=True) | Q(l2='')).values('l2').distinct()
                        # 存在四级节点数据
                        if l2_list:
                            for l2_item in l2_list:
                                # 五级节点数据
                                l3_node_list = []
                                l3_list = cell_type_relations_queryset.filter(
                                    species_name=species_item['species_name'], tissue_name=tissue_item['tissue_name'],
                                    l1=l1_item['l1'], l2=l2_item['l2']
                                ).exclude(Q(l3__isnull=True) | Q(l3='')).values('l3').distinct()
                                # 存在五级节点数据
                                if l3_list:
                                    for l3_item in l3_list:
                                        # 五级节点的 Marker gene数量
                                        l3_gene_number = marker_genes_queryset.filter(
                                            species=species_item['species_name'], tissue=tissue_item['tissue_name'],
                                            clusterName=l3_item['l3']
                                        ).count()
                                        # 五级节点的 Classic Marker 数量
                                        l3_classic_number = classic_markers_queryset.filter(
                                            species_name=species_item['species_name'],
                                            tissue_id=tissue_item['tissue_name'],
                                            cell_id=l3_item['l3']
                                        ).count()
                                        # 单个五级节点数据
                                        l3_data = {
                                            "name": l3_item['l3'],
                                            "level": "5",
                                            "icon_url": settings.BASE_URL + "source_material/other/{}.png".format("Unknow"),
                                            "gene_number": l3_gene_number,
                                            "classic_number": l3_classic_number,
                                            "node_number": 0,
                                        }
                                        l3_node_list.append(l3_data)
                                # 四级节点的 Marker gene数量
                                l2_gene_number = marker_genes_queryset.filter(
                                    species=species_item['species_name'], tissue=tissue_item['tissue_name'],
                                    clusterName=l2_item['l2']
                                ).count()
                                # 四级节点的 Classic Marker 数量
                                l2_classic_number = classic_markers_queryset.filter(
                                    species_name=species_item['species_name'], tissue_id=tissue_item['tissue_name'],
                                    cell_id=l2_item['l2']
                                ).count()
                                # 四级节点的子节点总数
                                l2_sub_node_total = cell_type_relations_queryset.filter(
                                    species_name=species_item['species_name'], tissue_name=tissue_item['tissue_name'],
                                    l1=l1_item['l1'], l2=l2_item['l2']
                                ).exclude(Q(l3__isnull=True) | Q(l3='')).count()
                                # 单个四级节点数据
                                l2_data = {
                                    "name": l2_item['l2'],
                                    "level": "4",
                                    "icon_url": settings.BASE_URL + "source_material/other/{}.png".format("Unknow"),
                                    "gene_number": l2_gene_number,
                                    "classic_number": l2_classic_number,
                                    "node_number": l2_sub_node_total,
                                    "children": l3_node_list
                                }
                                l2_node_list.append(l2_data)
                        # 三级节点的 Marker gene数量
                        l1_gene_number = marker_genes_queryset.filter(
                            species=species_item['species_name'], tissue=tissue_item['tissue_name'],
                            clusterName=l1_item['l1']
                        ).count()
                        # 三级节点的 Classic Marker 数量
                        l1_classic_number = classic_markers_queryset.filter(
                            species_name=species_item['species_name'], tissue_id=tissue_item['tissue_name'],
                            cell_id=l1_item['l1']
                        ).count()
                        # 三级节点的子节点总数
                        l1_sub_node_total = cell_type_relations_queryset.filter(
                            species_name=species_item['species_name'], tissue_name=tissue_item['tissue_name'],
                            l1=l1_item['l1']
                        ).exclude(Q(l2__isnull=True) | Q(l2='')).count()
                        # 单个三级节点数据
                        l1_data = {
                            "name": l1_item['l1'],
                            "level": "3",
                            "icon_url": settings.BASE_URL + "source_material/other/{}.png".format("Unknow"),
                            "gene_number": l1_gene_number,
                            "classic_number": l1_classic_number,
                            "node_number": l1_sub_node_total,
                            "children": l2_node_list
                        }
                        l1_node_list.append(l1_data)
                # 二级节点的 Marker gene数量
                tissue_gene_number = marker_genes_queryset.filter(
                    species=species_item['species_name'], tissue=tissue_item['tissue_name']
                ).count()
                # 二级节点的 Classic Marker 数量
                tissue_classic_number = classic_markers_queryset.filter(
                    species_name=species_item['species_name'], tissue_id=tissue_item['tissue_name']
                ).count()
                # 二级节点的子节点总数
                tissue_sub_node_total = cell_type_relations_queryset.filter(
                    species_name=species_item['species_name'], tissue_name=tissue_item['tissue_name']
                ).exclude(Q(l1__isnull=True) | Q(l1='')).count()

                icon_tissue = str(tissue_item['tissue_name']).replace(" ", "_").replace(";", "_")
                if tissue_item['tissue_name'] == "Unknown":
                    icon_url = "source_material/other/Unknown.png"
                else:
                    icon_url = "source_material/{}/{}/{}.png".format(icon_species, icon_tissue, icon_tissue)
                # 单个二级节点数据
                tissue_data = {
                    "name": tissue_item['tissue_name'],
                    "level": "2",
                    "icon_url": settings.BASE_URL + icon_url,
                    "gene_number": tissue_gene_number,
                    "classic_number": tissue_classic_number,
                    "node_number": tissue_sub_node_total,
                    "children": l1_node_list
                }
                tissue_node_list.append(tissue_data)

            # 一级节点的 Marker gene数量
            species_gene_number = marker_genes_queryset.filter(species=species_item['species_name']).count()
            # 一级节点的 Classic Marker 数量
            species_classic_number = classic_markers_queryset.filter(species_name=species_item['species_name']).count()
            # 一级节点的子节点总数，排除Unknow节点
            species_sub_node_total = cell_type_relations_queryset.filter(
                species_name=species_item['species_name']
            ).exclude(tissue_name='Unknow').count()

            # 单个一级节点数据
            species_data = {
                "name": species_item['species_name'],
                "level": "1",
                "icon_url": settings.BASE_URL + "source_material/{}/{}.png".format(icon_species, icon_species),
                "gene_number": species_gene_number,
                "classic_number": species_classic_number,
                "node_number": species_sub_node_total,
                "children": tissue_node_list
            }
            tree_list.append(species_data)
        print(tree_list)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_marker.settings')
    Command().handle()
