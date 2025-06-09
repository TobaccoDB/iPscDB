import csv
import os, django
import pandas as pd

django.setup()

from django.core.management import BaseCommand
from plant_marker.apps.plant_home.models import *


class Command(BaseCommand):
    """补充gene_details_info表数据"""
    def handle(self, *args, **options):
        gene_queryset = GeneDetailsInfo.objects.all()
        base_dir = 'F:/data/基因数据'
        file_name = "Fragaria vesca.csv"
        file_path = os.path.join(base_dir, file_name)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            reader = pd.read_csv(file)
            for index, row in reader.iterrows():
                gene_id = row['Gene_ID']
                gene_count = gene_queryset.filter(gene_id=gene_id).count()
                description = row["Description"] if str(row["Description"]) != "nan" else ""
                if gene_count > 0:
                    gene_data = gene_queryset.get(gene_id=gene_id)
                    gene_data.description = description
                    gene_data.save()
                    print("重复数据：{}，第{}行，基因符号:{}".format(file_name, index + 1, gene_id))
                else:
                    kwargs_dict = {
                        'scaffold': row["Location"],
                        'start': row["Start"],
                        'end': row["End"],
                        'strand': row["Strand"],
                        'gene_id': row["Gene_ID"],
                        'gene_symbol': row["Gene_Symbol"],
                        'description': description,
                    }
                    species_post = GeneDetailsInfo.objects.create(**kwargs_dict)
                    species_post.save()
                    print("新增数据：{}，第{}行，基因符号:{}".format(file_name, index + 1, gene_id))
        print("读取文件完成！")


if __name__ == '__main__':
    Command().handle()
