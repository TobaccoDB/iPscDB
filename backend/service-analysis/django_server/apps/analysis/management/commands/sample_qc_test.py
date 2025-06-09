from django.core.management.base import BaseCommand
import scanpy as sc
 
class Command(BaseCommand):

    def handle(self, *args, **options):
        
        filtered_dir_name = '/opt/Data_analyse/test_data1/data1/outs/outs/filtered_feature_bc_matrix.h5'
        try:
            adata = sc.read_h5ad(filtered_dir_name)
        except Exception as e:
            adata = sc.read_10x_h5(filtered_dir_name)
            
        print(adata)
    