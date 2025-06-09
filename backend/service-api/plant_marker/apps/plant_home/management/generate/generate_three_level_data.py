import os, django


django.setup()

from django.core.management import BaseCommand
from plant_marker.apps.plant_home.models import *

'''
仅用于生成search页面--cellType搜索项---下拉框三级联动数据
'''
class Command(BaseCommand):



    def handle_from_cellType(self, *args, **options):
        """
        物种、组织、细胞三级联动数据来自：cell_type_relations
        """
        queryset = CellTypeRelations.objects.all()

        # 获取所有的物种数据
        species_data = queryset.values("species_name").distinct().exclude(species_name=None)
        # 获取物种+组织数据
        tissue_data = queryset.values("species_name", "tissue_name").distinct()\
            .exclude(species_name=None).exclude(tissue_name=None)

        # 当前物种当前组织下的所有细胞：（去重+排空）三级节点+四级节点+五级节点
        # l1数据
        l1_cell_data = queryset.values("species_name", "tissue_name", "l1").distinct()\
            .exclude(species_name=None).exclude(tissue_name=None).exclude(l1=None)

        # l2数据
        l2_cell_data = queryset.values("species_name", "tissue_name", "l2").distinct() \
            .exclude(species_name=None).exclude(tissue_name=None).exclude(l1=None).exclude(l2=None)

        # l3数据
        l3_cell_data = queryset.values("species_name", "tissue_name", "l3").distinct()\
            .exclude(species_name=None).exclude(tissue_name=None).exclude(l1=None).exclude(l2=None).exclude(l3=None)

        #结果集
        data = []
        for species in species_data:
            #组装物种数据
            species_dict = {
                'species_name': species['species_name'],
                'child': []
            }
            for tissue in tissue_data:
                if species['species_name'] == tissue['species_name']:
                    #组装组织数据
                    tissue_dict = {
                        'tissue_name': tissue['tissue_name'],
                        'child': []
                    }

                    for l1 in l1_cell_data:
                        if tissue['tissue_name'] == l1['tissue_name']:
                            # 组装l1节点细胞数据
                            l1_cell_dict = {
                                'cell_name': l1['l1']
                            }
                            #将每一个l1节点细胞添加到当前组织中
                            tissue_dict['child'].append(l1_cell_dict)

                    for l2 in l2_cell_data:
                        if tissue['tissue_name'] == l2['tissue_name']:
                            # 组装l2节点细胞数据
                            l2_cell_dict = {
                                'cell_name': l2['l2']
                            }
                            # 将每一个l2节点细胞添加到当前组织中
                            tissue_dict['child'].append(l2_cell_dict)

                    for l3 in l3_cell_data:
                        if tissue['tissue_name'] == l3['tissue_name']:
                            # 组装l3节点细胞数据
                            l3_cell_dict = {
                                'cell_name': l3['l3']
                            }
                            # 将每一个l2节点细胞添加到当前组织中
                            tissue_dict['child'].append(l3_cell_dict)

                    # 将每个组织数据添加到当前物种中
                    species_dict['child'].append(tissue_dict)

            # 将每一个物种数据添加结果集中
            data.append(species_dict)
        print(data)



    def handle_from_gene(self, *args, **options):
        '''
        物种、组织、细胞三级联动数据来自：marker_genes_info表
        '''
        queryset = MarkerGenesInfo.objects.all()
        # 获取所有物种数据
        species_data = queryset.values("species").distinct().exclude(species=None)
        # 获取物种+组织数据
        tissue_data = queryset.values("species","tissue").distinct().exclude(species=None).exclude(tissue=None)
        # 获取物种+组织+细胞数据
        cell_data = queryset.values("species","tissue","clusterName").distinct().exclude(species=None).exclude(tissue=None).exclude(clusterName=None)
        # 结果集
        res = []
        # 整理结果集
        for species in species_data:
            # 组装一级节点物种数据
            if species['species'] == 'Unknow': continue
            specie_dict = {
                'specie_name': species['species'],
                'child': []
            }

            for tissue in tissue_data:
                if species['species'] == tissue['species']:
                    # 组装二级节点组织数据
                    if tissue['tissue'] == 'Unknow': continue
                    tissue_dict = {
                        'tissue_name': tissue['tissue'],
                        'child': []
                    }

                    for cell in cell_data:
                        if cell['tissue'] == tissue['tissue'] and cell['species'] == species['species']:
                            # 组装三级节点细胞数据
                            if cell['clusterName'] == 'Unknow': continue
                            cell_dict = {
                                'cell_name': cell['clusterName']
                            }

                            #向当前组织中添加细胞数据
                            tissue_dict['child'].append(cell_dict)

                    #向当前物种中添加组织数据
                    specie_dict['child'].append(tissue_dict)

            # 向结果集添加当前物种数据
            res.append(specie_dict)

        print(res)



if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_marker.settings')
    # Command().handle_from_cellType()
    Command().handle_from_gene()