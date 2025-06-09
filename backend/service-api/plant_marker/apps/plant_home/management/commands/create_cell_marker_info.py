import os
import xlrd

from django.core.management.base import BaseCommand
from django.db import transaction

from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            path = os.path.join(settings.EXCEL_FILE, 'cell_marker_data_22_09.xlsx')
            data1 = xlrd.open_workbook(path)
            sheet1 = data1.sheet_by_name('Sheet1')
            nrows1 = sheet1.nrows
            for r1 in range(1, nrows1):
                row1 = sheet1.row_values(r1)
                kwargs_dict = {
                    'mar_id': row1[0],
                    'species_name': str(row1[1]).replace(' ', '_'),
                    'tissue_id': row1[2],
                    'cell_id': row1[3],
                    'gene_symbol': row1[4],
                    'gene_id': row1[5],
                    'gene_id_other': row1[6],
                    'lit_id': row1[7],
                    'source_id': row1[8],

                }
                print(kwargs_dict)
                # species_post = CellMarkerInfo.objects.create(**kwargs_dict)
                # species_post.save()


"""
[{
  name: 'Female1',
 data:[[172.5, 55.2], [170.9, 54.2]]
},
{
  name: 'Female2',
 data:[[1.5, 5.2], [17.9, 5.2]]
}]

"""
# if __name__ == '__main__':
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_marker.settings')
#     Command().handle()