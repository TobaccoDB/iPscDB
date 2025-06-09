import csv
import os, django

django.setup()

from django.core.management import BaseCommand
from plant_marker.apps.plant_home.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        gene_queryset = GeneDetailsInfo.objects.all()
        base_dir = 'D:/svn/玥琨项目管理/基因数据库/基因数据/20基因详情'
        file_name = "EVMCDS.txt"
        file_path = os.path.join(base_dir, file_name)
        with open(file_path, 'r', errors='ignore') as file:
            reader = csv.reader(file, delimiter='\t')

            for i, row in enumerate(reader):
                gene_id = ""
                gene_symbol = ""
                description_list = []

                details = row[-1]
                details_list = str(details).split(";")
                for details_item in details_list:
                    key_value_pairs = details_item.split("=")  # 根据等号进行切片
                    key = key_value_pairs[0].strip()
                    if key == 'gene_id':
                        gene_id = key_value_pairs[1]
                    if key == 'symbol':
                        gene_symbol = key_value_pairs[1]
                    if key == 'description':
                        description_list.append(key_value_pairs[1])

                gene_id = str(gene_id).replace('"')
                if not gene_id:
                    print("无效数据，无基因ID：{}，第{}行".format(file_name, i+1))
                    continue

                count = gene_queryset.filter(gene_id=gene_id).count()
                if count > 0:
                    print("重复数据：{}，第{}行，基因ID:{}".format(file_name, i+1,gene_id))
                    continue

                kwargs_dict = {
                    'scaffold': row[0],
                    'start': row[3],
                    'end': row[4],
                    'strand': row[6],
                    'gene_id': gene_id,
                    'gene_symbol': gene_symbol,
                    'description': ';'.join(description_list),
                }
                print("读取文件：{}，第{}行:{}".format(file_name, i+1, kwargs_dict))
                species_post = GeneDetailsInfo.objects.create(**kwargs_dict)
                species_post.save()


if __name__ == '__main__':
    Command().handle()
