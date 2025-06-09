import os
import xlrd
from plant_marker.apps.plant_home.models import *
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from xlrd import xldate_as_datetime, xldate_as_tuple
import calendar

dat = {
    '01': 'Jan',
    '02': 'Feb',
    '03': 'Mar',
    '04': 'Apr',
    '05': 'May',
    '06': 'Jun',
    '07': 'Jul',
    '08': 'Aug',
    '09': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec',
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            path = os.path.join(settings.EXCEL_FILE, 'gene_symbol_gene_id.xlsx')
            data1 = xlrd.open_workbook(path)
            sheet1 = data1.sheet_by_name('Sheet1')
            nrows1 = sheet1.nrows
            for r1 in range(1, nrows1):
                print(r1)
                row1 = sheet1.row_values(r1)
                try:
                    kwargs_dict = {
                        'gene_id': row1[0],
                        'gene_symbol': str(
                            str(xldate_as_datetime(row1[1], 0).strftime('%m/%d')).split('/')[1] + '-' + dat.get(
                                str(xldate_as_datetime(row1[1], 0).strftime('%m/%d')).split('/')[0])).replace('0',
                                                                                                              '') if str(
                            xldate_as_datetime(row1[1], 0).strftime('%m/%d')).startswith(
                            str(xldate_as_datetime(row1[1], 0).strftime('%m/%d')).split('/')[0]) else str(
                            xldate_as_datetime(row1[1], 0).strftime('%m/%d')),
                    }
                except Exception as e:
                    kwargs_dict = {
                        'gene_id': row1[0],
                        'gene_symbol': row1[1],
                    }
                print(kwargs_dict)
                species_post = GeneSymbolToGeneIdInfo.objects.create(**kwargs_dict)
                species_post.save()
