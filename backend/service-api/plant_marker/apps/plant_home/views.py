import ast
import csv
import glob
import hashlib
import operator
import os
import re
import uuid
import zipfile
from collections import Counter
from itertools import chain
from time import strftime, localtime
from io import StringIO
import anndata
import cairosvg
import fitz
import pandas as pd
from PIL import Image
from django.db import connection
from django.db.models import Count
from django.db.models import Q, Min, Max
from django.db.models import Sum
from django.http import FileResponse, HttpResponse
from django.http import StreamingHttpResponse
from django.utils.encoding import escape_uri_path
from rest_framework import status, viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny

from .serializers import *
from ..utils.atlas_data import atlas_list_data
from ..utils.blast_list import blast_list
from ..utils.blast_query import parse_blast_xml
from ..utils.diagram import all_tissue_structure_data, all_tissue_Leaf_structure_data
from ..utils.get_efp_color import color_value_new
from ..utils.get_ip import change_info
from ..utils.group_concat import GroupConcat
from ..utils.home_species_data import home_species_data
from ..utils.marker_histogram_data import marker_histogram_data
from ..utils.markers_tree import markers_tree_data
from ..utils.three_level_data import three_level_data
from ..utils.violin_box_plot import draw_violinplot, draw_atlas_violinplot, draw_atlas_cell_violinplot_new, \
    cell_id_format
from ..utils.get_zju_data import get_api_data, format_cell_type
from ...response import JSONResponse


class PlantHomeUmaptViewSet(viewsets.ModelViewSet):
    """首页物种表达式图"""
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        queryset_values_list = self.paginate_queryset(self.queryset)
        serializer = PlantHomeUmaptSerializer(queryset_values_list, many=True)
        return self.get_paginated_response(serializer.data)

    @list_route(methods=('get',), url_path='umap_dataset')
    def umap_dataset(self, request, *args, **kwargs):
        """
        首页 物种umap接口
        """
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        gene_id = request.GET.get('gene_id', '')
        umap_type = request.GET.get('umap_type', 'Cell_type')
        try:

            if not gene_id:
                # 根据物种名称映射文件
                file_name = 'umap/{}/{}/umap_data'.format(species_name, tissue)
                # 读取物种对应的文件
                file_path = os.path.join(
                    settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(file_name))
                # 1：Sample_ID;2:Clusters;3:Project_ID 筛选相应的列
                # umap_data = pd.read_csv(file_path, usecols=['UMAP_1', 'UMAP_2', 'Clusters', 'Cell_type'])#########20230401##############
                umap_data = pd.read_csv(file_path, usecols=['UMAP_1', 'UMAP_2', 'Clusters', umap_type])
                # 2023-5-16
                # umap_data = umap_data.iloc[1:15000]
                # 通过cell_type组成的df
                cell_type_df = umap_data
                # 将Clusters和Cell_type进行拼接聚合
                # umap_data['Clusters_Cell_type'] = umap_data['Clusters'].map(str) + ':' + umap_data['Cell_type'].map(str)########20230401###############
                umap_data['Clusters_Cell_type'] = umap_data['Clusters'].map(str) + ':' + umap_data[umap_type].map(str)
                clusters_data = umap_data.groupby(['Clusters_Cell_type'])

                data_list = []
                for group_name, group_data in clusters_data:
                    group_data = group_data[['UMAP_1', 'UMAP_2']]
                    group_name = group_name[0]
                    data = {
                        'name': group_name.split(":")[1],
                        'data': group_data.to_dict('split').get('data', []),
                        'sort': int(group_name.split(":")[0]) if tissue != 'WholePlant' else group_name.split(":")[0]
                    }
                    data_list.append(data)
                data_list = sorted(data_list, key=lambda x: x['sort'])
                # 组合cell_type的df
                # cell_type_df = cell_type_df.iloc[1:10000]
                # cell_type_df = cell_type_df.groupby('Cell_type')########20230401###############
                cell_type_df = cell_type_df.groupby(umap_type)
                cell_type_data_list = []
                for group_name, group_data in cell_type_df:
                    group_data = group_data[['UMAP_1', 'UMAP_2']]
                    data = {
                        'name': str(group_name),
                        # 'data': group_data.to_dict('split').get('data', [])[1:15000],#2023-5-16
                        'data': group_data.to_dict('split').get('data', []),
                    }
                    cell_type_data_list.append(data)
                all_data_ = {
                    'clusters_data': data_list,
                    'cell_type_data': cell_type_data_list,
                }
            else:
                # 根据物种名称映射文件
                umap_path = 'umap/{}/{}/umap_data'.format(species_name, tissue)
                # 2023 03 10注
                # file_path = os.path.join(settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(umap_path))
                file_path = os.path.join(settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(umap_path))
                # file_path = 'D:/免疫单细胞数据库/数据/Arabidopsis_thaliana/Root/umap_data.csv'
                # 1：Sample_ID;2:Clusters;3:Project_ID 筛选相应的列
                # 读取基因对应的文件
                file_name = '{}/{}/expression_data'.format(species_name, tissue)
                gene_path = os.path.join(settings.ATLAS_HOT_PNG_DIR, "umap/{}/{}.csv".format(file_name, gene_id))
                # 1：Sample_ID;2:Clusters;3:Project_ID 筛选相应的列
                # expression_data = pd.read_csv(file_path, usecols=['Cell_ID', 'UMAP_1', 'UMAP_2', 'Clusters', 'Cell_type'])
                expression_data = pd.read_csv(file_path, usecols=['Cell_ID', 'UMAP_1', 'UMAP_2', 'Clusters', umap_type])
                # 格式化 Cell_ID
                expression_data['Cell_ID'] = expression_data['Cell_ID'].apply(cell_id_format)
                # 组合cell_type的df
                cell_type_df = expression_data
                if os.path.exists(gene_path):
                    gene_data = pd.read_csv(gene_path, usecols=['Cell_ID', 'value'])
                    gene_data['Cell_ID'] = gene_data['Cell_ID'].apply(cell_id_format)
                    expression_data = pd.merge(expression_data, gene_data, how='left', on='Cell_ID').fillna(0)
                    expression_data['value'] = expression_data['value'].astype(str).str[:4].astype(float)
                    cell_type_df = pd.merge(cell_type_df, gene_data, how='left', on='Cell_ID').fillna(0)
                    cell_type_df['value'] = cell_type_df['value'].astype(str).str[:4].astype(float)
                else:
                    expression_data['value'] = 0
                    cell_type_df['value'] = 0
                expression_data = expression_data.drop('Cell_ID', axis=1)
                cell_type_df = cell_type_df.drop('Cell_ID', axis=1)
                # 2023-5-16
                # expression_data = expression_data.iloc[1:15000]
                # cell_type_df = cell_type_df.iloc[1:15000]
                # expression_data['Clusters_Cell_type'] = expression_data['Clusters'].map(str) + ':' + expression_data['Cell_type'].map(str)
                expression_data['Clusters_Cell_type'] = expression_data['Clusters'].map(str) + ':' + expression_data[
                    umap_type].map(str)
                expression_data = expression_data.groupby(['Clusters_Cell_type'])

                data_list = []
                for group_name, group_data in expression_data:
                    group_data = group_data[['UMAP_1', 'UMAP_2', 'value']]
                    group_name = str(group_name[0])
                    data = {
                        'name': group_name.split(":")[1],
                        'data': group_data.to_dict('split').get('data', []),
                        'sort': group_name.split(":")[0],
                        # 'sort': int(group_name.split(":")[0]) if tissue != 'WholePlant' else group_name.split(":")[0]
                    }
                    data_list.append(data)
                data_list = sorted(data_list, key=lambda x: x['sort'])
                # 组合cell_type的df
                # cell_type_df = cell_type_df.groupby('Cell_type')
                cell_type_df = cell_type_df.groupby(umap_type)
                cell_type_data_list = []
                for group_name, group_data in cell_type_df:
                    group_data = group_data[['UMAP_1', 'UMAP_2', 'value']]
                    data = {
                        'name': str(group_name),
                        # 'data': group_data.to_dict('split').get('data', [])[1:2800],
                        'data': group_data.to_dict('split').get('data', []),
                    }
                    cell_type_data_list.append(data)
                all_data_ = {
                    'clusters_data': data_list,
                    'cell_type_data': cell_type_data_list,
                }

        except Exception as e:
            print(e)
            all_data_ = []
        return JSONResponse(all_data_)

    @list_route(methods=('get',), url_path='tsne_umap_dataset')
    def tsne_umap_dataset(self, request, *args, **kwargs):
        """
        TSNE umap接口
        """
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        gene_id = request.GET.get('gene_id')
        umap_type = request.GET.get('umap_type', 'Cell_type')
        try:
            if not gene_id:
                # 根据物种名称映射文件
                file_name = 'umap/{}/{}/tsne_data'.format(species_name, tissue)
                # 读取物种对应的文件
                file_path = os.path.join(
                    settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(file_name))
                # file_path = 'D:/免疫单细胞数据库/数据/Arabidopsis_thaliana/Root/umap_data.csv'
                # 1：Sample_ID;2:Clusters;3:Project_ID 筛选相应的列
                umap_data = pd.read_csv(
                    file_path, usecols=['tSNE_1', 'tSNE_2', 'Clusters', umap_type])
                # umap_data = umap_data.iloc[1:15000]
                # 通过cell_type组成的df
                cell_type_df = umap_data
                # 将Clusters和Cell_type进行拼接聚合
                umap_data['Clusters_Cell_type'] = umap_data['Clusters'].map(str) + ':' + umap_data[umap_type].map(str)
                clusters_data = umap_data.groupby(['Clusters_Cell_type'])
                # clusters_data = umap_data.groupby(mata_data_type)
                data_list = []
                for group_name, group_data in clusters_data:
                    group_data = group_data[['tSNE_1', 'tSNE_2']]
                    group_name = group_name[0]
                    data = {
                        'name': group_name.split(":")[1],
                        'data': group_data.to_dict('split').get('data', []),
                        'sort': int(group_name.split(":")[0]) if tissue != 'WholePlant' else group_name.split(":")[0]
                    }
                    data_list.append(data)
                data_list = sorted(data_list, key=lambda x: x['sort'])
                # 组合cell_type的df
                cell_type_df = cell_type_df.groupby(umap_type)
                cell_type_data_list = []
                for group_name, group_data in cell_type_df:
                    group_data = group_data[['tSNE_1', 'tSNE_2']]
                    data = {
                        'name': str(group_name),
                        'data': group_data.to_dict('split').get('data', []),
                    }
                    cell_type_data_list.append(data)
                all_data_ = {
                    'clusters_data': data_list,
                    'cell_type_data': cell_type_data_list,
                }
            else:
                # 根据物种名称映射文件
                umap_path = 'umap/{}/{}/tsne_data'.format(species_name, tissue)
                file_path = os.path.join(settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(umap_path))
                # file_path = 'D:/免疫单细胞数据库/数据/Arabidopsis_thaliana/Root/umap_data.csv'
                # 1：Sample_ID;2:Clusters;3:Project_ID 筛选相应的列
                # 读取基因对应的文件
                file_name = 'umap/{}/{}/expression_data'.format(species_name, tissue)
                # # 读取物种对应的文件
                gene_path = os.path.join(settings.ATLAS_HOT_PNG_DIR, "{}/{}.csv".format(file_name, gene_id))
                # 1：Sample_ID;2:Clusters;3:Project_ID 筛选相应的列
                expression_data = pd.read_csv(file_path, usecols=['Cell_ID', 'tSNE_1', 'tSNE_2', 'Clusters', umap_type])
                expression_data['Cell_ID'] = expression_data['Cell_ID'].apply(cell_id_format)
                # 组合cell_type的df
                cell_type_df = expression_data
                if os.path.exists(gene_path):
                    gene_data = pd.read_csv(gene_path, usecols=['Cell_ID', 'value'])
                    gene_data['Cell_ID'] = gene_data['Cell_ID'].apply(cell_id_format)
                    expression_data = pd.merge(expression_data, gene_data, how='left', on='Cell_ID').fillna(0)
                    expression_data['value'] = expression_data['value'].astype(str).str[:4].astype(float)
                    cell_type_df = pd.merge(cell_type_df, gene_data, how='left', on='Cell_ID').fillna(0)
                    cell_type_df['value'] = cell_type_df['value'].astype(str).str[:4].astype(float)
                else:
                    expression_data['value'] = 0
                    cell_type_df['value'] = 0
                expression_data = expression_data.drop('Cell_ID', axis=1)
                cell_type_df = cell_type_df.drop('Cell_ID', axis=1)
                # expression_data = expression_data.iloc[1:15000]
                # cell_type_df = cell_type_df.iloc[1:15000]
                expression_data['Clusters_Cell_type'] = expression_data['Clusters'].map(str) + ':' + expression_data[umap_type].map(str)
                expression_data = expression_data.groupby(['Clusters_Cell_type'])
                data_list = []
                for group_name, group_data in expression_data:
                    group_data = group_data[['tSNE_1', 'tSNE_2', 'value']]
                    group_name = str(group_name[0])
                    data = {
                        'name': group_name.split(":")[1],
                        'data': group_data.to_dict('split').get('data', []),
                        'sort': int(group_name.split(":")[0]) if tissue != 'WholePlant' else group_name.split(":")[0]
                    }
                    data_list.append(data)
                data_list = sorted(data_list, key=lambda x: x['sort'])
                # 组合cell_type的df
                cell_type_df = cell_type_df.groupby(umap_type)
                cell_type_data_list = []
                for group_name, group_data in cell_type_df:
                    group_data = group_data[['tSNE_1', 'tSNE_2', 'value']]
                    data = {
                        'name': str(group_name),
                        'data': group_data.to_dict('split').get('data', []),
                    }
                    cell_type_data_list.append(data)
                all_data_ = {
                    'clusters_data': data_list,
                    'cell_type_data': cell_type_data_list,
                }

        except Exception as e:
            print(e)
            all_data_ = []
        return JSONResponse(all_data_)

    @list_route(methods=('get',), url_path='atlas_tissue_cell_sample_count')
    def atlas_tissue_cell_sample_count(self, request, *args, **kwargs):
        """首页物种相关统计"""
        data = home_species_data
        return JSONResponse(data)

    @list_route(methods=('get',), url_path='species_relation_statistics')
    def species_relation_statistics(self, request, *args, **kwargs):
        """首页物种相关统计"""
        data = [
            {
                "species": "23",
                "datasets": "92",
                "experiments": "789",
                "technologies": "6",
                "atlases": "43",
                "markers": "274,430",
                "classic_markers": "3976",
                "marker_genes": "270,480",
                "cells": "3,537,348",
                "cell_types": "276"
            }
        ]
        return JSONResponse(data)


class HomeUmaptPoltViewSet(viewsets.ModelViewSet):
    """首页物种表达式图"""
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        """20230618:首页 物种umap接口"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        gene_id = request.GET.get('gene_id', '')
        umap_type = request.GET.get('umap_type', 'Cell_type')
        try:
            if not gene_id:
                # 根据物种名称映射文件
                file_name = 'umap/{}/{}/umap_data_old'.format(species_name, tissue)
                # 读取物种对应的文件
                file_path = os.path.join(
                    settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(file_name))
                # 1：Sample_ID;2:Clusters;3:Project_ID 筛选相应的列
                # umap_data = pd.read_csv(file_path, usecols=['UMAP_1', 'UMAP_2', 'Clusters', 'Cell_type'])#########20230401##############
                umap_data = pd.read_csv(file_path, usecols=['UMAP_1', 'UMAP_2', 'Clusters', umap_type])
                cell_type_df = umap_data

                # 将Clusters和Cell_type进行拼接聚合
                # umap_data['Clusters_Cell_type'] = umap_data['Clusters'].map(str) + ':' + umap_data['Cell_type'].map(str)########20230401###############
                umap_data['Clusters_Cell_type'] = umap_data['Clusters'].map(str) + ':' + umap_data[umap_type].map(str)
                clusters_data = umap_data.groupby(['Clusters_Cell_type'])

                # data_list = []
                # for group_name, group_data in clusters_data:
                #     group_data = group_data[['UMAP_1', 'UMAP_2']]
                #     data = {
                #         'name': group_name.split(":")[1],
                #         'data': group_data.to_dict('split').get('data', []),
                #         'sort': int(group_name.split(":")[0]) if tissue != 'WholePlant' else group_name.split(":")[0]
                #     }
                #     data_list.append(data)
                # data_list = sorted(data_list, key=lambda x: x['sort'])
                # 组合cell_type的df
                # cell_type_df = cell_type_df.iloc[1:10000]
                # cell_type_df = cell_type_df.groupby('Cell_type')########20230401###############
                cell_type_df = cell_type_df.groupby(umap_type)
                cell_type_data_list = []
                for group_name, group_data in cell_type_df:
                    group_data = group_data[['UMAP_1', 'UMAP_2']]
                    data = {
                        'name': str(group_name),
                        # 'data': group_data.to_dict('split').get('data', [])[1:15000],#2023-5-16
                        'data': group_data.to_dict('split').get('data', []),
                    }
                    cell_type_data_list.append(data)
                all_data_ = {
                    # 'clusters_data': data_list,
                    'cell_type_data': cell_type_data_list,
                }
            else:
                # 2023-06-06新增基因别名
                if species_name == 'Arabidopsis_thaliana':
                    gene_id_list_1 = GeneInfo.objects.filter(species=species_name).filter(
                        gene_symbol__icontains=gene_id).exclude(gene_symbol='').values_list('gene_id', flat=True)
                    # 查的表数据
                    gene_id_list_2 = ClusterMarkerInfo.objects.filter(species_name__icontains=species_name,
                                                                      tissue_id__icontains=tissue).filter(
                        cluster_marker__icontains=gene_id).exclude(cluster_marker='').values_list('gene_id',
                                                                                                  flat=True)
                    gene_id_3 = list(set(chain(gene_id_list_1, gene_id_list_2)))
                    # 根据物种名称映射文件-------------取指定路径下的文件名
                    file_name = 'umap/{}/{}'.format(species_name, tissue)
                    # 读取物种对应的文件
                    file_path = os.path.join(
                        settings.ATLAS_HOT_PNG_DIR, "{}/expression_data/".format(file_name))
                    matched_files = []
                    # 使用glob模块进行文件名匹配
                    files = glob.glob(os.path.join(file_path, f'*{gene_id}*'))
                    for file_path in files:
                        file_name_without_extension = os.path.splitext(os.path.basename(file_path))[
                            0] if os.path.splitext(os.path.basename(file_path)) else ''
                        # 根据输入的参数动态返回文件名
                        matched_files.append(file_name_without_extension)
                    gene_id_list = list(set(matched_files))
                    gene_id = list(set(chain(gene_id_list, gene_id_3)))[0]
                else:
                    gene_id_list = CellMarkerInfo.objects.filter(species_name=species_name).filter(
                        Q(gene_symbol__icontains=gene_id) | Q(gene_id__icontains=gene_id)).exclude(
                        gene_symbol='').values_list(
                        'gene_id', flat=True)
                    gene_id_list_3 = ClusterMarkerInfo.objects.filter(species_name=species_name).filter(
                        cluster_marker__icontains=gene_id).exclude(cluster_marker='').values_list('gene_id', flat=True)
                    gene_id_ = list(set(chain(gene_id_list, gene_id_list_3)))
                    # 根据物种名称映射文件-------------取指定路径下的文件名
                    file_name = 'umap/{}/{}'.format(species_name, tissue)
                    # 读取物种对应的文件
                    file_path = os.path.join(
                        settings.ATLAS_HOT_PNG_DIR, "{}/expression_data/".format(file_name))
                    matched_files = []
                    # 使用glob模块进行文件名匹配
                    files = glob.glob(os.path.join(file_path, f'*{gene_id}*'))
                    for file_path in files:
                        file_name_without_extension = os.path.splitext(os.path.basename(file_path))[
                            0] if os.path.splitext(os.path.basename(file_path)) else ''
                        # 根据输入的参数动态返回文件名
                        matched_files.append(file_name_without_extension)
                    gene_id_list = list(set(matched_files))
                    gene_id = list(set(chain(gene_id_list, gene_id_)))[0]
                # 根据物种名称映射文件
                umap_path = 'umap/{}/{}/umap_data_old'.format(species_name, tissue)
                # 2023 03 10注
                # file_path = os.path.join(settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(umap_path))
                file_path = os.path.join(settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(umap_path))
                # file_path = 'D:/免疫单细胞数据库/数据/Arabidopsis_thaliana/Root/umap_data.csv'
                # 1：Sample_ID;2:Clusters;3:Project_ID 筛选相应的列
                # 读取物种对应的文件
                file_name = '{}/{}/expression_data'.format(species_name, tissue)
                # # 读取物种对应的文件
                gene_path = os.path.join(settings.ATLAS_HOT_PNG_DIR,
                                         "umap/{file_name}/{gene_id}.csv".format(file_name=file_name, gene_id=gene_id))
                # 1：Sample_ID;2:Clusters;3:Project_ID 筛选相应的列
                # expression_data = pd.read_csv(file_path, usecols=['Cell_ID', 'UMAP_1', 'UMAP_2', 'Clusters', 'Cell_type'])
                expression_data = pd.read_csv(file_path, usecols=['Cell_ID', 'UMAP_1', 'UMAP_2', 'Clusters', umap_type])
                # 组合cell_type的df
                cell_type_df = expression_data
                if os.path.exists(gene_path):
                    gene_data = pd.read_csv(gene_path, usecols=['Cell_ID', 'value'])
                    expression_data = pd.merge(
                        expression_data, gene_data, how='left', on='Cell_ID').fillna(0)
                    expression_data['value'] = expression_data['value'].astype(
                        str).str[:4].astype(float)
                    cell_type_df = pd.merge(
                        cell_type_df, gene_data, how='left', on='Cell_ID').fillna(0)
                    cell_type_df['value'] = cell_type_df['value'].astype(
                        str).str[:4].astype(float)
                else:
                    expression_data['value'] = 0
                    cell_type_df['value'] = 0
                expression_data = expression_data.drop('Cell_ID', axis=1)
                expression_data['Clusters_Cell_type'] = expression_data['Clusters'].map(str) + ':' + expression_data[
                    umap_type].map(str)
                expression_data = expression_data.groupby(['Clusters_Cell_type'])
                # data_list = []
                # for group_name, group_data in expression_data:
                #     group_data = group_data[['UMAP_1', 'UMAP_2', 'value']]
                #     data = {
                #         'name': group_name.split(":")[1],
                #         'data': group_data.to_dict('split').get('data', []),
                #         # 'sort': int(group_name.split(":")[0])
                #         'sort': int(group_name.split(":")[0]) if tissue != 'WholePlant' else group_name.split(":")[0]
                #     }
                #     data_list.append(data)
                # data_list = sorted(data_list, key=lambda x: x['sort'])
                # 组合cell_type的df
                # cell_type_df = cell_type_df.iloc[1:10000]
                # cell_type_df = cell_type_df.groupby('Cell_type')########20230401###############
                cell_type_df = cell_type_df.groupby(umap_type)
                cell_type_data_list = []
                for group_name, group_data in cell_type_df:
                    group_data = group_data[['UMAP_1', 'UMAP_2']]
                    data = {
                        'name': str(group_name),
                        # 'data': group_data.to_dict('split').get('data', [])[1:15000],#2023-5-16
                        'data': group_data.to_dict('split').get('data', []),
                    }
                    cell_type_data_list.append(data)
                all_data_ = {
                    # 'clusters_data': data_list,
                    'cell_type_data': cell_type_data_list,
                }

        except Exception as e:
            print(e)
            all_data_ = []
        return JSONResponse(all_data_)


class ClassicMarkersInfoCountGene(viewsets.ModelViewSet):
    """classic_markers_info表根据gene_id去重计数"""
    queryset = ClassicMarkersInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ClassicMarkersInfoSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name')
        tissue_id = request.GET.get('tissue_id')
        cell_id = request.GET.get('cell_id')
        try:
            data = self.queryset
            # 1.根据条件过滤数据
            if species_name or tissue_id or cell_id:
                # 1.1三个条件至少一个不为空
                if not self.isLegal(species_name, tissue_id, cell_id):
                    # 1.1.1 若三个参数的形式不合法，则数据设置为空
                    data = data.none()
                else:
                    # 1.1.2 若三个参数的形式合法，则依次按条件过滤
                    data = data.filter(species_name=species_name)
                    if tissue_id:
                        data = data.filter(tissue_id=tissue_id)
                        if cell_id:
                            data = data.filter(cell_id=cell_id)
            else:
                # 1.2 三个条件都空则取默认物种数据
                data = data.filter(species_name='Arabidopsis thaliana')
            # 2. 对gene_id数据去重
            distinct_data = data.values('gene_id', 'species_name', 'tissue_id', 'cell_id').distinct()
            # 3. 根据gene_id统计数量并降序排序
            result = distinct_data.values('species_name', 'tissue_id', 'cell_id').annotate(
                gene_id_count=Count('gene_id')).order_by('gene_id_count').reverse()
        except Exception as e:
            print(e)
            result = []
        return JSONResponse(result)

    # 判断三个参数的格式是否合法
    def isLegal(self, species_name, tissue_id, cell_id):
        if (not species_name and tissue_id) or (not tissue_id and cell_id):
            return False
        else:
            return True


class PlantAtlasListViewSet(viewsets.ModelViewSet):
    """Atlas列表页接口"""
    queryset = ProjrctAtlasCellType.objects.all()
    permission_classes = (AllowAny,)
    # serializer_class = MarkerInfoSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        tag_list_type = request.GET.get('tag_list_type', '')
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        page = self.request.GET.get('page', '1')
        page_size = self.request.GET.get('page_size', '1')

        if tag_list_type == 'cell_type':
            if species_name == 'Popular_alba':
                species_name = 'Populus_alba'
            else:
                species_name = species_name
                # paginate_queryset：分页查询器，lit_id__icontains：模糊查询
            queryset_values_list = self.paginate_queryset(
                self.queryset.filter(lit_id__icontains=tissue, species_name=species_name))
            serializer = ProjrctAtlasCellTypeSerializer(
                queryset_values_list, many=True)
        elif tag_list_type == 'marker':
            # Arabidopsis thaliana物种的Root tip组织没有数据，因此获取的Root的数据
            if tissue == "Root_tip" or tissue == "Root tip":
                tissue = "Root"

            query_sql = "SELECT mgi.gene, mgi.`name`, mgi.clusterName, mgi.pct_1, mgi.pct_2, " \
                        "mgi.avg_log2FC, mgi.p_val, mgi.p_val_adj, cmi.gene_symbol " \
                        "FROM marker_genes_info mgi LEFT JOIN classic_markers_info cmi " \
                        "ON mgi.species = cmi.species_name AND mgi.tissue = cmi.tissue_id " \
                        "AND mgi.clusterName = cmi.cell_id AND mgi.gene = cmi.gene_id " \
                        "WHERE mgi.species = '{}'".format(species_name.replace("_", " "))
            if tissue != 'WholePlant' and tissue != 'Whole Plant':
                query_sql += " AND mgi.tissue = '{}'".format(tissue.replace("_", " "))
            cursor = connection.cursor()
            cursor.execute(query_sql)
            results = cursor.fetchall()
            result_data = []
            for dict_item in results:
                # 处理gene_symbol
                if dict_item[8]:
                    gene_symbol = dict_item[8]
                elif dict_item[1]:
                    gene_symbol = dict_item[1]
                else:
                    gene_symbol = dict_item[0]
                # 处理 log_2fc数据
                log_2fc = round(dict_item[5], 3)
                if log_2fc == 999:
                    log_2fc = 'inf'
                dict_data = {
                    'gene_id': dict_item[0],
                    'gene_symbol': gene_symbol,
                    'cell_type': dict_item[2],
                    'pct1': dict_item[3],
                    'pct2': dict_item[4],
                    'log_2fc': log_2fc,
                    'p_va1': '{:.2e}'.format(dict_item[6]),
                    'p_val_adj': '{:.2e}'.format(dict_item[7])
                }
                result_data.append(dict_data)
            page = self.paginate_queryset(result_data)
            return self.get_paginated_response(page)
        else:
            if species_name == 'Oryza_sativa' and tissue == 'Flower':
                tissue = 'Inflorescence'
            elif tissue == 'Root_tip' or tissue == 'Root tip':
                tissue = "Root"
            else:
                tissue = tissue
            if tissue != 'WholePlant' and tissue != 'Whole Plant':
                queryset = Sample.objects.filter(
                    tissue__icontains=tissue,
                    species_name=species_name)
            else:
                queryset = Sample.objects.filter(
                    species_name=species_name)
            queryset_values_list = self.paginate_queryset(queryset)
            serializer = SampleSerializer(queryset_values_list, many=True)
        return self.get_paginated_response(serializer.data)


class PlantSearchDownViewSet(viewsets.ModelViewSet):
    """Search各种下拉框接口"""
    queryset = Sample.objects.all()
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        """tissue_type下拉框接口"""
        try:
            # species_name_type_list = self.queryset.values_list(
            #     'species_name', flat=True).order_by(
            #     'species_name').distinct()
            # specie_data = list()
            # for species in list(set(species_name_type_list)):
            #
            #     if species == 'Nicotiana_tabacum':
            #         data = {
            #             'label': 'Nicotiana attenuate',
            #             'value': species
            #         }
            #
            #     elif species == 'Populus':
            #         data = {
            #             'label': 'Populus alba',
            #             'value': species
            #         }
            #
            #     else:
            #         data = {
            #             'label': str(species).replace('_', ' '),
            #             'value': species
            #         }
            #     specie_data.append(data)
            specie_data = [
                {
                    "label": "Arabidopsis thaliana",
                    "value": "Arabidopsis_thaliana"
                },
                {
                    "label": "Nicotiana attenuata",
                    "value": "Nicotiana_attenuata"
                },
                {
                    "label": "Populus alba var. pyramidalis",
                    # "value": "Populus"
                    "value": "Popular_alba"
                },
                {
                    "label": "Solanum lycopersicum",
                    "value": "Solanum_lycopersicum"
                },
                {
                    "label": "Oryza sativa",
                    "value": "Oryza_sativa"
                },
                {
                    "label": "Arachis hypogaea",
                    "value": "Arachis_hypogaea"
                },
                {
                    "label": "Bombax ceiba",
                    "value": "Bombax_ceiba"
                },
                {
                    "label": "Brassica rapa",
                    "value": "Brassica_rapa"
                },
                # {
                #     "label": "Camellia sinensis",
                #     "value": "Camellia_sinensis"
                # },
                {
                    "label": "Catharanthus roseus",
                    "value": "Catharanthus_roseus"
                },
                {
                    "label": "Fragaria vesca",
                    "value": "Fragaria_vesca"
                },
                {
                    "label": "Glycine max",
                    "value": "Glycine_max"
                },
                {
                    "label": "Gossypium bickii",
                    "value": "Gossypium_bickii"
                },
                {
                    "label": "Gossypium hirsutum",
                    "value": "Gossypium_hirsutum"
                },
                {
                    "label": "Gossypium arboreum",
                    "value": "Gossypium_arboreum"
                },
                {
                    "label": "Manihot esculenta",
                    "value": "Manihot_esculenta"
                },
                {
                    "label": "Marchantia polymorpha",
                    "value": "Marchantia_polymorpha"
                },
                {
                    "label": "Medicago truncatula",
                    "value": "Medicago_truncatula"
                },
                {
                    "label": "Phalaenopsis Big Chili",
                    "value": "Phalaenopsis_Big_Chili"
                },
                {
                    "label": "Phyllostachys edulis",
                    "value": "Phyllostachys_edulis"
                },
                {
                    "label": "Populus trichocarpa",
                    "value": "Populus_trichocarpa"
                },
                {
                    "label": "Populus tremula × alba",
                    "value": "Populus_tremula"
                },
                {
                    "label": "Populus alba",
                    "value": "Populus_alba"
                },
                {
                    "label": "Populus euramericana",
                    "value": "Populus_euramericana"
                },
                {
                    "label": "Triticum aestivum",
                    "value": "Triticum_aestivum"
                }
            ]
        except Exception as e:
            specie_data = []
        return JSONResponse(data=specie_data)

    @list_route(methods=('get',), url_path='tissue_type_down')
    def tissue_type_down(self, request, *args, **kwargs):
        """tissue物种组织"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        try:
            querysets = self.queryset.filter(species_name=species_name)
            tissue_type_list = querysets.exclude(tissue='').values_list('tissue',
                                                                        flat=True).order_by(
                'tissue').distinct()
            tissue_data = list()
            for tissue_one in list(set(tissue_type_list)):
                data = {
                    'label': tissue_one,
                    'value': tissue_one
                }
                tissue_data.append(data)
        except Exception as e:
            tissue_data = []
        return JSONResponse(data=tissue_data)

    @list_route(methods=('get',), url_path='project_id_down')
    def project_id_down(self, request, *args, **kwargs):
        """物种Project_ID下拉框"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        try:
            querysets = self.queryset.filter(
                species_name=species_name, tissue=tissue)
            project_id_type_list = querysets.exclude(project_id='').values_list('project_id',
                                                                                flat=True).order_by(
                'project_id').distinct()
            project_id_data = list()
            for project_id_one in list(set(project_id_type_list)):
                data = {
                    'label': project_id_one,
                    'value': project_id_one
                }
                project_id_data.append(data)
        except Exception as e:
            project_id_data = []
        return JSONResponse(data=project_id_data)

    @list_route(methods=('get',), url_path='sample_id_down')
    def sample_id_down(self, request, *args, **kwargs):
        """物种Sample_ID下拉框"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        project_id = request.GET.get('project_id', '')
        try:
            querysets = self.queryset.filter(
                species_name=species_name, tissue=tissue, project_id=project_id)
            sample_id_type_list = querysets.exclude(sample_id='').values_list('sample_id',
                                                                              flat=True).order_by(
                'sample_id').distinct()
            sample_id_data = list()
            for sample_id_one in list(set(sample_id_type_list)):
                data = {
                    'label': sample_id_one,
                    'value': sample_id_one
                }
                sample_id_data.append(data)
        except Exception as e:
            sample_id_data = []
        return JSONResponse(data=sample_id_data)

    @list_route(methods=('get',), url_path='sample_name_down')
    def sample_name_down(self, request, *args, **kwargs):
        """Sample   Sample_Name下拉框"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        project_id = request.GET.get('project_id', '')
        sample_id = request.GET.get('sample_id', '')
        try:
            querysets = self.queryset.filter(species_name=species_name, tissue=tissue, project_id__icontains=project_id)
            sample_name_type_list = querysets.exclude(sample_name='').values_list('sample_name',
                                                                                  flat=True).order_by(
                'sample_name').distinct()
            sample_name_data = list()
            for sample_name_one in list(set(sample_name_type_list)):
                data = {
                    'label': sample_name_one,
                    'value': sample_name_one
                }
                sample_name_data.append(data)
        except Exception as e:
            sample_name_data = []
        return JSONResponse(data=sample_name_data)

    @list_route(methods=('get',), url_path='process_status_down')
    def process_status_down(self, request, *args, **kwargs):
        """Sample  QC_check下拉框"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        project_id = request.GET.get('project_id', '')
        sample_id = request.GET.get('sample_id', '')
        # sample_name = request.GET.get('sample_name', '')
        try:
            querysets = self.queryset.filter(species_name=species_name, tissue=tissue, project_id__icontains=project_id,
                                             sample_id__icontains=sample_id)
            process_status_type_list = querysets.exclude(qc_check='').values_list('qc_check',
                                                                                  flat=True).order_by(
                'qc_check').distinct()
            process_status_data = list()
            for process_status_one in list(set(process_status_type_list)):
                data = {
                    'label': process_status_one,
                    'value': process_status_one
                }
                process_status_data.append(data)
        except Exception as e:
            process_status_data = []
        return JSONResponse(data=process_status_data)

    @list_route(methods=('get',), url_path='cluster_name_down')
    def cluster_name_down(self, request, *args, **kwargs):
        """物种Cluster_Name下拉框"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        try:
            querysets = ClusterMarkerInfo.objects.filter(
                species_name=species_name, tissue_id=tissue)
            cluster_name_type_list = querysets.exclude(cluster_name='').values_list('cluster_name',
                                                                                    flat=True).order_by(
                'cluster_name').distinct()
            cluster_name_data = list()
            for cluster_name_one in list(set(cluster_name_type_list)):
                data = {
                    'label': cluster_name_one,
                    'value': cluster_name_one
                }
                cluster_name_data.append(data)
        except Exception as e:
            cluster_name_data = []
        return JSONResponse(data=cluster_name_data)

    @list_route(methods=('get',), url_path='cluster_marker_down')
    def cluster_marker_down(self, request, *args, **kwargs):
        """物种Cluster_Marker下拉框"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', '')
        cluster_name = request.GET.get('cluster_name', '')
        try:
            querysets = ClusterMarkerInfo.objects.filter(species_name=species_name, tissue_id=tissue,
                                                         cluster_name=cluster_name)
            cluster_marker_type_list = querysets.exclude(cluster_marker='').values_list('cluster_marker',
                                                                                        flat=True).order_by(
                'cluster_marker').distinct()
            cluster_marker_data = list()
            for cluster_marker_one in list(set(cluster_marker_type_list)):
                data = {
                    'label': cluster_marker_one,
                    'value': cluster_marker_one
                }
                cluster_marker_data.append(data)
        except Exception as e:
            cluster_marker_data = []
        return JSONResponse(data=cluster_marker_data)

    @list_route(methods=('get',), url_path='cell_id_down')
    def cell_id_down(self, request, *args, **kwargs):
        """物种Cell_ID下拉框"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', '')
        try:
            querysets = CellMarkerInfo.objects.filter(
                species_name=species_name, tissue_id=tissue)
            cell_id_type_list = querysets.exclude(cell_id='').values_list('cell_id',
                                                                          flat=True).order_by(
                'cell_id').distinct()
            cell_id_data = list()
            cell_id_type_list = list(set(cell_id_type_list))
            cell_id_type_split_list = []
            cell_id_type_one_list = []
            for one in cell_id_type_list:
                # 括号+号连接的进行分类
                if '+' in one and 'LRC (1st +2nd Outer Layer)' not in one:
                    one_list = one.split('+')
                    cell_id_type_split_list += one_list
                else:
                    cell_id_type_one_list.append(one)
            cell_id_type_all_data = cell_id_type_split_list + cell_id_type_one_list
            cell_id_type_all_data = [i.strip() for i in cell_id_type_all_data]
            # 处理括号里含+号
            if 'Columella (1st Outer Layer) + LRC (1st +2nd Outer Layer)' in cell_id_type_all_data:
                cell_id_type_all_data = cell_id_type_all_data + ['Columella(1st Outer Layer)',
                                                                 'LRC(1st + 2nd Outer Layer)']
                cell_id_type_all_data.remove(
                    'Columella (1st Outer Layer) + LRC (1st +2nd Outer Layer)')
            for cell_id_one in list(set(cell_id_type_all_data)):
                data = {
                    'label': cell_id_one,
                    'value': cell_id_one
                }
                cell_id_data.append(data)
        except Exception as e:
            cell_id_data = []
        return JSONResponse(data=cell_id_data)

    @list_route(methods=('get',), url_path='gene_symbol_down')
    def gene_symbol_down(self, request, *args, **kwargs):
        """物种Gene_Symbol下拉框"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', '')
        cell_id = request.GET.get('cell_id', '')
        try:
            querysets = CellMarkerInfo.objects.filter(species_name=species_name, tissue_id=tissue,
                                                      cell_id__icontains=cell_id)
            gene_symbol_type_list = querysets.exclude(gene_symbol='').values_list('gene_symbol',
                                                                                  flat=True).order_by(
                'gene_symbol').distinct()
            gene_symbol_data = list()
            for gene_symbol_one in list(set(gene_symbol_type_list)):
                data = {
                    'label': gene_symbol_one,
                    'value': gene_symbol_one
                }
                gene_symbol_data.append(data)
        except Exception as e:
            gene_symbol_data = []
        return JSONResponse(data=gene_symbol_data)

    @list_route(methods=('get',), url_path='gene_id_express_down')
    def gene_id_express_down(self, request, *args, **kwargs):
        """GeneExpression gene_id 下拉框"""
        species_name = self.request.GET.get('species_name')
        tissue = self.request.GET.get('tissue')
        try:
            # path = 'D:/免疫单细胞数据库/数据/物种数据/{}/{}'.format(species_name, tissue)
            path = os.path.join(settings.GENE_EXPRESSION_FILE +
                                species_name + '/' + tissue + '/')
            files = os.listdir(path)
            gene_id_list = []
            for gene_id in files:
                data = {
                    'label': gene_id.split('.')[0],
                    'value': gene_id.split('.')[0]
                }
                gene_id_list.append((data))
        except Exception as e:
            gene_id_list = []
        return JSONResponse(data=gene_id_list)


class PlantSearchViewSet(viewsets.ModelViewSet):
    """Search各种检索接口"""
    queryset = Sample.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SampleSearchSerializer
    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        return JSONResponse(data={'msg': '非法操作'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        species_name = self.request.GET.get(
            'species_name', 'Arabidopsis_thaliana')
        tissue = self.request.GET.get('tissue', '')
        project_id = self.request.GET.get('project_id', '')
        sample_id = self.request.GET.get('sample_id', '')
        sample_name = self.request.GET.get('sample_name', '')
        process_status = self.request.GET.get('process_status', '')
        try:
            query_list = []
            if species_name:
                query_list.append(Q(species_name=species_name))
            if tissue:
                query_list.append(Q(tissue=tissue))
            if project_id:
                query_list.append(Q(project_id__icontains=project_id))
            if sample_id:
                query_list.append(Q(sample_id__icontains=sample_id))
            if sample_name:
                query_list.append(Q(sample_name__icontains=sample_name))
            if project_id:
                query_list.append(Q(qc_check__icontains=process_status))
        except Exception as e:
            query_list = []
        queryset = self.queryset.filter(*query_list)
        for obj in queryset:
            try:
                if os.path.lexists(r'/data/Sample_clean_rds/{}'.format(obj.sample_id + '.rds')):
                    obj.is_sample_rds = '1'
                    obj.process_status = 'QC Pass'
                else:
                    obj.is_sample_rds = '0'
                    obj.process_status = 'Under process'
            except Exception as e:
                obj.is_sample_rds = '0'
                obj.process_status = 'Under process'

        sorted_queryset = sorted(queryset, key=lambda obj: obj.is_sample_rds, reverse=True)
        return sorted_queryset

    @list_route(methods=('get',), url_path='search_cluster_marker')
    def search_cluster_marker(self, request, *args, **kwargs):
        species_name = self.request.GET.get(
            'species_name', 'Arabidopsis_thaliana')
        tissue = self.request.GET.get('tissue', '')
        cluster_name = self.request.GET.get('cluster_name', '')
        cluster_marker = self.request.GET.get('cluster_marker', '')
        try:
            query_list = []
            if species_name:
                query_list.append(Q(species_name=species_name))
            if tissue:
                query_list.append(Q(tissue_id=tissue))
            if cluster_name:
                query_list.append(Q(cluster_name__icontains=cluster_name))
            if cluster_marker:
                query_list.append(Q(cluster_marker__icontains=cluster_marker))
        except Exception as e:
            query_list = []
        queryset_values_list = ClusterMarkerInfo.objects.filter(*query_list)
        queryset_values_list = self.paginate_queryset(queryset_values_list)
        serializer = ClusterMarkerSearchSerializer(
            queryset_values_list, many=True)
        return self.get_paginated_response(serializer.data)

    @list_route(methods=('get',), url_path='search_cell_marker')
    def search_cell_marker(self, request, *args, **kwargs):
        species_name = self.request.GET.get(
            'species_name', 'Arabidopsis_thaliana')
        tissue = self.request.GET.get('tissue', '')
        cell_id = self.request.GET.get('cell_id', '')
        gene_symbol = self.request.GET.get('gene_symbol', '')
        try:
            query_list = []
            if species_name:
                query_list.append(Q(species_name=species_name))
            if tissue:
                query_list.append(Q(tissue_id=tissue))
            if cell_id:
                query_list.append(Q(cell_id__icontains=cell_id))
            if gene_symbol:
                query_list.append(Q(gene_symbol__icontains=gene_symbol))
        except Exception as e:
            query_list = []
        queryset_values_list = CellMarkerInfo.objects.filter(*query_list)
        queryset_values_list = self.paginate_queryset(queryset_values_list)
        serializer = CellMarkerInfoSearchSerializer(
            queryset_values_list, many=True)
        return self.get_paginated_response(serializer.data)


class PlantSampleRdsDownloadViewSet(viewsets.ModelViewSet):
    """Search Sample Rds数据下载接口"""
    queryset = Sample.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SampleSearchSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        sample_id = self.request.GET.get('sample_id', '')
        try:
            file_name = sample_id + '.rds'
            file_url = os.path.join(settings.SAMPLE_RDS_DOWNLOAD, file_name)
            file_time = strftime("%Y%m%d%H", localtime())
            response = FileResponse(open(file_url, 'rb'))
            response['Content-Type'] = 'application/msword'
            response['Content-Disposition'] = 'attachment;filename={file_name}'.format(
                file_name=file_name)
            return response
        except Exception as e:
            return JSONResponse({"mas": "非法操作"}, status=status.HTTP_403_FORBIDDEN)


class ProjrctAtlasListViewSet(viewsets.ModelViewSet):
    """ProjrctAtlas各种检索接口"""
    queryset = ProjrctAtlasCellType.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProjrctAtlasCellTypeSerializer
    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        return JSONResponse(data={'msg': '非法操作'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        lit_id = self.request.GET.get('lit_id', '')
        species_name = self.request.GET.get('species_name', '')
        tissue = self.request.GET.get('tissue', '')
        # print()
        if species_name == 'Popular_alba':
            species_name = 'Populus_alba'
        else:
            species_name = species_name
        try:
            query_list = []
            if lit_id:
                query_list.append(Q(lit_id=lit_id))
            if species_name:
                query_list.append(Q(species_name=species_name))
            if tissue:
                query_list.append(Q(tissue_id__icontains=tissue))
        except Exception as e:
            print(e)
            query_list = []
            # print()
        return self.queryset.filter(*query_list).exclude(gene_id='')

    @list_route(methods=('get',), url_path='cluster_marker')
    def cluster_marker(self, request, *args, **kwargs):
        lit_id = self.request.GET.get('lit_id', '')
        project_id = self.request.GET.get('project_id', '')
        species_name = self.request.GET.get('species_name', '')
        page = self.request.GET.get('page', '1')
        page_size = self.request.GET.get('page_size', '1')
        try:
            if species_name == 'Popular_alba':
                species_name = 'Populus'
            else:
                species_name = species_name
            # 根据物种名称映射文件
            file_name = '{}/{}_{}/cluster_markers'.format(species_name, lit_id, project_id)
            # file_name = '{}/{}/cluster_markers'.format(species_name, lit_id)
            # 读取物种对应的文件
            file_path = os.path.join(
                settings.CELL_EXPRESSION_DIR, "{}.csv".format(file_name))
            # file_path = 'D:/免疫单细胞数据库/数据/umap数据/{}/cluster_markers.csv'.format(lit_id)
            # 读取物种对应的文件
            obj_data = pd.read_csv(file_path)

            data = obj_data.to_dict(orient="records")
            # data = eval(obj_data[['cell_type']].to_json(orient='records', force_ascii=False))
            # print(data)
            data_drfm = data[(int(page) - 1) *
                             10: (int(page) - 1) * 10 + int(page_size)]
            data_dic = {
                "code": 200,
                "data": {
                    "page_size": int(page_size),
                    "results": data_drfm,
                    "count": len(data)
                }
            }
        except Exception as e:
            print(e)
            data_dic = {
                "code": 200,
                "data": []
            }
        return JSONResponse(data=data_dic)

    @list_route(methods=('get',), url_path='sample_list')
    def sample_list(self, request, *args, **kwargs):
        # lit_id = self.request.GET.get('lit_id', '')
        species_name = self.request.GET.get('species_name', '')
        project_id = self.request.GET.get('project_id', '')
        try:
            sample_queryset = Sample.objects.filter(
                species_name=species_name, project_id=project_id)
        except Exception as e:
            sample_queryset = []
        queryset_values_list = self.paginate_queryset(sample_queryset)
        serializer = SampleSerializer(queryset_values_list, many=True)
        return self.get_paginated_response(serializer.data)

    @list_route(methods=('get',), url_path='project_umap_dataset')
    def project_umap_dataset(self, request, *args, **kwargs):
        """
         物种umap接口
        """
        lit_id = self.request.GET.get('lit_id', '')
        species_name = self.request.GET.get('species_name', '')
        # 1：Sample_ID;2:Clusters;3:Project_ID
        mata_data_type = request.GET.get('mata_data_type', 'Clusters')
        try:
            # 根据物种名称映射文件
            file_name = '{}/{}/umap_data'.format(species_name, lit_id)
            # 读取物种对应的文件
            file_path = os.path.join(
                settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(file_name))
            # 1：Sample_ID;2:Clusters;3:Project_ID 筛选相应的列
            umap_data = pd.read_csv(
                file_path, usecols=['UMAP_1', 'UMAP_2', mata_data_type])
            umap_data = umap_data.iloc[1:15001]
            clusters_data = umap_data.groupby(mata_data_type)
            data_list = []
            for group_name, group_data in clusters_data:
                group_data = group_data[['UMAP_1', 'UMAP_2']]
                data = {
                    'name': group_name,
                    'data': group_data.to_dict('split').get('data', []),
                    'sort': int(group_name.split(':')[0])
                }
                data_list.append(data)
            data_list = sorted(data_list, key=lambda x: x['sort'])
        except Exception as e:
            data_list = []
        return JSONResponse(data_list)

    @list_route(methods=('get',), url_path='project_lit_down')
    def project_lit_down(self, request, *args, **kwargs):
        """
         Project Atlas导航栏下拉框
        """
        data = atlas_list_data
        return JSONResponse(data)


class SampleQcUploadViewSet(viewsets.ModelViewSet):
    """SampleQc文件上传接口"""
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get']

    # def create(self, request, *args, **kwargs):
    #     '''SampleQc文件上传接口'''
    #     files_uuid = self.request.data.get('files_uuid')  # 创建文件夹名称
    #     file = self.request.FILES.get('myfile')
    #     try:
    #         if file:
    #             file_url = os.path.join(
    #                 settings.SAMPLE_UPLOAD_FILE + files_uuid + '/', file.name)
    #             # 上传文件的话上传的指定的路径下,进行数据的比对
    #             with open(file_url, 'wb+') as f:
    #                 # 分块写入文件
    #                 for chunk in file.chunks():
    #                     f.write(chunk)
    #         return JSONResponse(data={'msg': '文件上传成功！'})
    #     except Exception as e:
    #         print(e)
    #         return JSONResponse(data={'msg': '文件上传失败,请重新上传！'})

    def list(self, request, *args, **kwargs):
        files_uuid = self.request.GET.get('files_uuid')
        if files_uuid:
            f = os.popen(
                'Rscript /data/Sample_QC/Sample_QC.R -d {}'.format(files_uuid))
            result = f.read()
        else:
            result = r"[1] 3228\nAn object of class Seurat \n20563 features across 3025 samples within 1 assay \nActive assay: RNA (20563 features, 0 variable features)\n"

        re_c = re.compile('(\d+)')

        result_list = re_c.findall(result)

        try:
            data = {
                'genes': result_list[2],
                'cells': result_list[3],
                'result': result
            }

        except Exception as e:
            data = {
                'genes': 0,
                'cells': 0,
                'result': result
            }

        return JSONResponse(data=data)

    @list_route(methods=('get',), url_path='sample_qc_uuid')
    def sample_qc_uuid(self, request, *args, **kwargs):
        try:
            uuid_str = uuid.uuid4()
            # 创建文件夹
            # os.system('mkdir {}/{}'.format(settings.SAMPLE_UPLOAD_FILE, uuid_str))
        except Exception as e:
            uuid_str = '67285f07-cff4-4a80-ae3f-0d6277c3d92c'
        return JSONResponse(data=[uuid_str])


class GeneExpressionUmapViewSet(viewsets.ModelViewSet):
    """GeneExpression接口"""
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = self.request.GET.get(
            'species_name', 'Arabidopsis_thaliana')
        tissue = self.request.GET.get('tissue', 'Root')
        gene_id = self.request.GET.get('gene_id', 'AT1G01070')
        # 读取文件
        try:
            umap_path = os.path.join(
                settings.ATLAS_HOT_PNG_DIR, 'umap', species_name, tissue + '/' + 'umap_data.csv')
            file_name = '{}/{}/expression_data'.format(species_name, tissue)
            # # 读取物种对应的文件
            gene_path = os.path.join(settings.ATLAS_HOT_PNG_DIR,
                                     "umap/{file_name}/{gene_id}.csv".format(file_name=file_name, gene_id=gene_id))
            expression_data = pd.read_csv(
                umap_path, usecols=['Cell_ID', 'UMAP_1', 'UMAP_2', 'Clusters'])
            # umpa 数据返回所有的点
            if os.path.exists(gene_path):
                gene_data = pd.read_csv(gene_path)
                expression_data = pd.merge(
                    expression_data, gene_data, how='left', on='Cell_ID').fillna(0)
                expression_data['value'] = expression_data['value'].astype(
                    str).str[:4].astype(float)
            else:
                expression_data['value'] = 0
            expression_data = expression_data.drop('Cell_ID', axis=1)

            # expression_data = expression_data.sort_values(by='value',ascending=False)
            umap_data = expression_data.iloc[1:30000]
            # expression_data = expression_data.drop('Cell_ID', axis=1)
            expression_data_list = eval(
                expression_data.to_json(orient="split")).get('data', '')
            clusters_data = umap_data.groupby('Cell_type')
            data_list = []
            for group_name, group_data in clusters_data:
                group_data = group_data[['UMAP_1', 'UMAP_2']]
                # print('www', group_name)
                data = {
                    'name': group_name,
                    'data': group_data.to_dict('split').get('data', []),
                    # 'sort': int(group_name.split(":")[0])
                }
                data_list.append(data)

            # data_list = sorted(data_list, key=lambda x: x['sort'])
            umap_data = umap_data.drop('Cell_type', axis=1)
            expression_data_list = eval(
                umap_data.to_json(orient="split")).get('data', '')
            data = {
                'umpa_data': data_list,
                'expression_data': expression_data_list,
            }
        except Exception as e:
            print(e)
            data = {
                'expression_data': []
            }

        return JSONResponse(data=data)

    @list_route(methods=('get',), url_path='gene_expression_species_name')
    def gene_expression_species_name(self, request, *args, **kwargs):
        try:
            # path = 'D:/免疫单细胞数据库/数据/物种数据/'
            path = "/data/Gene_expression/"
            files = os.listdir(path)
            species_name_list = []
            for species_name in files:
                if os.path.isdir(path + species_name):
                    data = {
                        'label': species_name.replace('_', ' '),
                        'value': species_name
                    }
                    species_name_list.append((data))
        except Exception as e:
            species_name_list = []
        return JSONResponse(data=species_name_list)

    @list_route(methods=('get',), url_path='gene_expression_tissue')
    def gene_expression_tissue(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name')
        try:
            # path = 'D:/免疫单细胞数据库/数据/物种数据/{}'.format(species_name)
            path = os.path.join(
                settings.GENE_EXPRESSION_FILE + "{}/".format(species_name))
            files = os.listdir(path)
            tissue_list = []
            for tissue in files:
                if os.path.isdir(path):
                    data = {
                        'label': tissue,
                        'value': tissue
                    }
                    tissue_list.append((data))
        except Exception as e:
            tissue_list = []
        return JSONResponse(data=tissue_list)


class CellCountryVisiterViewSet(viewsets.ModelViewSet):
    """底部国家访问量接口"""
    queryset = UserIP.objects.all()
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        change_info(request)  # 调用ip 信息录入方法
        country_queryset_list = UserIP.objects.all().values_list('ip_addr', flat=True).exclude(ip_addr='unknown')
        country_queryset_list = list(set(country_queryset_list))
        dic = {}
        total_count = UserIP.objects.all().values_list('count', flat=True).aggregate(
            Sum('count'))  # 查询网页总访问量
        country_lst = []
        for country in country_queryset_list:
            dic_country = {}
            con = UserIP.objects.filter(ip_addr=country).values_list('count', flat=True).aggregate(
                Sum('count'))
            dic_country['country'] = country
            dic_country['count'] = con['count__sum']
            country_lst.append(dic_country)
        country_lst = sorted(country_lst, key=operator.itemgetter('count'), reverse=True)

        dic['code'] = 200
        dic['meg'] = 'success'
        dic['total_count'] = total_count.get('count__sum')
        dic['data'] = country_lst
        return JSONResponse(dic)


class SampleQcUploadPictureViewSet(viewsets.ModelViewSet):
    """SampleQc文件上传接口"""
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        '''
        Sample QC文件上传接口
        '''
        files_uuid = request.data.get('files_uuid', None)  # 文件夹UUID
        file_type = request.data.get('file_type', None)  # 文件类型
        file_name = request.data.get('file_name', None)
        file = self.request.FILES.get('myfile')

        if file_type == 'rds':
            # 如果上传的是 rds 文件直接存储在 /data/Sample_QC/upload_data 下
            file_name = files_uuid + '.rds'
            file_url = os.path.join(settings.SAMPLE_UPLOAD_RDS_DIR + file_name)
            # 上传文件的话上传的指定的路径下,进行数据的比对
            with open(file_url, 'wb+') as f:
                # 分块写入文件
                for chunk in file.chunks():
                    f.write(chunk)
        elif file_type == 'gz':
            save_path = os.path.join(settings.SAMPLE_UPLOAD_GZ_DIR, files_uuid)
            # 判断保存的文件夹存不存在
            if not os.path.exists(save_path):
                # 如果不存在则创建目录
                os.makedirs(save_path)
            # 上传的名字
            file_name = file_name.lower()
            if file_name == "barcodes":
                file_name_gz = "barcodes.tsv.gz"
            elif file_name == "features":
                file_name_gz = "features.tsv.gz"
            elif file_name == "matrix":
                file_name_gz = 'matrix.mtx.gz'
            else:
                return JSONResponse(data={'msg': 'File upload failed！'})

            file_url = os.path.join(save_path, file_name_gz)
            # 上传文件的话上传的指定的路径下,进行数据的比对
            with open(file_url, 'wb+') as f:
                # 分块写入文件
                for chunk in file.chunks():
                    f.write(chunk)
        else:
            return JSONResponse(data={'msg': 'File upload failed！'})

        return JSONResponse(data={'msg': 'File uploaded successfully！'})

    def list(self, request, *args, **kwargs):
        uuid_str = str(uuid.uuid1())

        files_uuid = self.request.GET.get('files_uuid')
        file_type = self.request.GET.get('file_type')
        sample_id = self.request.GET.get('sample_id')
        filter_min_mt_cutmin = self.request.GET.get('filter_min_mt_cutmin')
        filter_max_mt_cutmax = self.request.GET.get('filter_max_mt_cutmax')
        filter_min_pt_cutmin = self.request.GET.get('filter_min_pt_cutmin')
        filter_max_pt_cutmax = self.request.GET.get('filter_max_pt_cutmax')
        filter_min_Feature_RNA_cutmin = self.request.GET.get('filter_min_Feature_RNA_cutmin')
        filter_max_Feature_RNA_cutax = self.request.GET.get('filter_max_Feature_RNA_cutax')
        if files_uuid and file_type == 'rds':
            f = os.popen(f'Rscript /data/Sample_QC/QC_Upload_Rds.R -d {files_uuid} -s {sample_id}')
            result = f.read()
        elif files_uuid and file_type == 'gz':
            f = os.popen(f'Rscript /data/Sample_QC/QC_Upload.R -d {files_uuid} -s {sample_id}')
            result = f.read()
        # 带着参数请求  读取QC_Filter.R文件
        elif files_uuid and file_type == 'filter':
            a = f"Rscript /data/Sample_QC/QC_Filter.R -d {files_uuid} -a {filter_min_mt_cutmin} -b {filter_max_mt_cutmax} -c {filter_min_pt_cutmin} -e {filter_max_pt_cutmax} -f {filter_min_Feature_RNA_cutmin} -g {filter_max_Feature_RNA_cutax} -u {uuid_str}"

            f = os.popen(a)
            result = f.read()
        elif file_type == 'example':
            f = os.popen(f'Rscript /data/Sample_QC/QC_Upload_Rds.R -d example -s {sample_id}')
            result = f.read()
        else:
            result = ""
        # re_c = '\d+\.\d+|\d+'
        re_c = '-?[0-9]+\.[0-9]*|-?[0-9]+'
        result_list = re.findall(re_c, result)
        try:
            if file_type == 'rds' or file_type == 'example':
                data = {
                    'min_nFeature_RNA': result_list[1],
                    'max_nFeature_RNA': result_list[3],
                    'min_nCount_RNA': result_list[5],
                    'max_nCount_RNA': result_list[7],
                    'min_percent_mt': result_list[9],
                    'max_percent_mt': result_list[11],
                    'min_percent_pt': result_list[13],
                    'max_percent_pt': result_list[15],
                    'filter_min_Feature_RNA_cutmin': result_list[17],
                    'filter_max_Feature_RNA_cutax': result_list[19],
                    'filter_min_nCount_RNA': result_list[21],
                    'filter_max_nCount_RNA': result_list[23],
                    'filter_min_mt_cutmin': result_list[25],
                    'filter_max_mt_cutmax': result_list[27],
                    'filter_min_pt_cutmin': result_list[29],
                    'filter_max_pt_cutmax': result_list[31],
                    # 'genes': result_list[16],
                    # 'cells': result_list[17],
                    'result': result,
                    'picture': settings.BASE_URL + "Sample_QC/qc_picture/" + files_uuid + '.svg'
                }
            elif file_type == 'gz':
                data = {
                    'min_nFeature_RNA': result_list[1],
                    'max_nFeature_RNA': result_list[3],
                    'min_nCount_RNA': result_list[5],
                    'max_nCount_RNA': result_list[7],
                    'min_percent_mt': result_list[9],
                    'max_percent_mt': result_list[11],
                    'min_percent_pt': result_list[13],
                    'max_percent_pt': result_list[15],
                    'filter_min_Feature_RNA_cutmin': result_list[17],
                    'filter_max_Feature_RNA_cutax': result_list[19],
                    'filter_min_nCount_RNA': result_list[21],
                    'filter_max_nCount_RNA': result_list[23],
                    'filter_min_mt_cutmin': result_list[25],
                    'filter_max_mt_cutmax': result_list[27],
                    'filter_min_pt_cutmin': result_list[29],
                    'filter_max_pt_cutmax': result_list[31],
                    # 'genes': result_list[2],
                    # 'cells': result_list[3],
                    'result': result,
                    'picture': settings.BASE_URL + "Sample_QC/qc_picture/" + files_uuid + '.svg'
                }
            elif file_type == 'filter':
                re_c = re.compile('(\d+)')
                result_list = re_c.findall(result)
                data = {
                    'genes': result_list[0] if result_list else 0,
                    'cells': result_list[1] if result_list else 0,
                    'result': result if result_list else 'Error: No cells found',
                    'picture': settings.BASE_URL + "Sample_QC/qc_picture/" + uuid_str + '.svg',
                    'result_rds': settings.BASE_URL + "Sample_QC/filter_rds_data/" + uuid_str + '.rds',
                    'identification_path': settings.SAPMLE_FILTER_RDS_DIR + uuid_str + '.rds'
                }
            else:
                data = {
                    'min_nFeature_RNA': 0,
                    'max_nFeature_RNA': 0,
                    'min_nCount_RNA': 0,
                    'max_nCount_RNA': 0,
                    'min_percent_mt': 0,
                    'max_percent_mt': 0,
                    'min_percent_pt': 0,
                    'max_percent_pt': 0,
                    'genes': 0,
                    'cells': 0,
                    'result': '',
                    'picture': settings.BASE_URL + "Sample_QC/qc_picture/" + files_uuid + '.svg'
                }

        except Exception as e:
            data = {
                'min_nFeature_RNA': 0,
                'max_nFeature_RNA': 0,
                'min_nCount_RNA': 0,
                'max_nCount_RNA': 0,
                'min_percent_mt': 0,
                'max_percent_mt': 0,
                'min_percent_pt': 0,
                'max_percent_pt': 0,
                'genes': 0,
                'cells': 0,
                'result': result,
                'picture': settings.BASE_URL + "Sample_QC/qc_picture/" + files_uuid + '.svg'
            }

        return JSONResponse(data=data)


class IntegrationSvgShowViewSet(viewsets.ModelViewSet):
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """Integration SVG图片生成展示接口"""
        sample_id = self.request.GET.get('sample_id')  # sample_id 传的参数是Integration(列表页中sample_id的数据用,隔开控制在2-5个)
        uuid_str = uuid.uuid4()
        sample_id_list = sample_id.split(',')
        # rds 文件所在的文件夹
        rds_base_path = '/data/browser_download'
        fileMap = {}
        # 选择两个文件比较小的
        for filename in sample_id_list:
            size = os.path.getsize(os.path.join(rds_base_path, filename + '.rds'))
            fileMap.setdefault(os.path.join(rds_base_path, filename + '.rds'), size)
            filelist = sorted(fileMap.items(), key=lambda d: d[1], reverse=False)
        finall_list = filelist[0:3]
        a = [str(list(i)[0]).split('{}/'.format(rds_base_path)) for i in finall_list]
        print(a)
        b = a[0] + a[1] + a[2]
        list_ = [x.strip().split('.')[0] for x in b if x.strip() != '']
        try:
            fun = 'Rscript /data/Integration/Integration.R -a {} -b {} -c {} -u {}'.format(list_[0], list_[1], list_[2],
                                                                                           uuid_str)
            f = os.popen(fun)
            f.read()
            # 去掉orig.ident图片上的标题
            sub_str = 'orig.ident'
            svg_base_path = '/data/Integration/result_picture/{}.svg'.format(uuid_str)
            with open(svg_base_path, 'r') as fr:
                data = fr.read()
                data = re.sub(sub_str, r"", str(data))
            with open(svg_base_path, 'w') as fw:
                fw.write(data)
            # 根据生成展示的svg图片转换成png格式的图片进行返回
            svg_path = '/data/Integration/result_picture/{}.svg'.format(uuid_str)
            png_path = '/data/Integration/result_picture/{}.png'.format(uuid_str)
            cairosvg.svg2png(url=svg_path, write_to=png_path, background_color='#ffffff', output_width=1200,
                             output_height=560)
            # 将生成的png转换成jpg
            jpg_path = '/data/Integration/result_picture/{}.jpg'.format(uuid_str)
            img = Image.open(png_path)
            img.save(jpg_path)
            data = {
                'integration_svg': settings.INTEGRATION_RESULT_PICTURE + str(uuid_str) + '.svg',  # 详情图片展示
                'integration_download_png': settings.INTEGRATION_RESULT_PICTURE + str(uuid_str) + '.png',  # 详情png图片格式下载
                'integration_download_svg': settings.INTEGRATION_RESULT_PICTURE + str(uuid_str) + '.svg',  # 详情svg图片格式下载
                'integration_download_jpg': settings.INTEGRATION_RESULT_PICTURE + str(uuid_str) + '.jpg',  # 详情jpg图片格式下载
            }
        except Exception as e:
            print(e)
            data = {
                'integration_svg': '',
                'integration_download_png': '',
                'integration_download_svg': '',
                'integration_download_jpg': ''
            }
        return JSONResponse(data=data)


class IntegrationDownloadViewSet(viewsets.ModelViewSet):
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """Integration SVG图片生成展示接口"""
        integration_type = self.request.GET.get('integration_type')  # 文件所在文件夹
        sample_id = self.request.GET.get('sample_id')  # sample_id 传的参数是Integration(列表页中sample_id的数据用,隔开控制在2-5个)
        uuid_str = uuid.uuid4()
        sample_id_list = sample_id.split(',')
        sample_id_len = len(sample_id_list)
        try:
            if sample_id_len == 2:
                fun = 'Rscript /data/Integration/{}.R -a {} -b {} -u {}'.format(integration_type, sample_id_list[0],
                                                                                sample_id_list[1], uuid_str)
            elif sample_id_len == 3:
                fun = 'Rscript /data/Integration/{}.R -a {} -b {} -c {} -u {}'.format(integration_type,
                                                                                      sample_id_list[0],
                                                                                      sample_id_list[1],
                                                                                      sample_id_list[2],
                                                                                      uuid_str)
            elif sample_id_len == 4:
                fun = 'Rscript /data/Integration/{}.R -a {} -b {} -c {} -d {} -u {}'.format(integration_type,
                                                                                            sample_id_list[0],
                                                                                            sample_id_list[1],
                                                                                            sample_id_list[2],
                                                                                            sample_id_list[3],
                                                                                            uuid_str)
            else:
                fun = 'Rscript /data/Integration/{}.R -a {} -b {} -c {} -d {} -e {} -u {}'.format(integration_type,
                                                                                                  sample_id_list[0],
                                                                                                  sample_id_list[1],
                                                                                                  sample_id_list[2],
                                                                                                  sample_id_list[3],
                                                                                                  sample_id_list[4],
                                                                                                  uuid_str)

            f = os.popen(fun)
            f.read()
            # 返回example生成的svg图片路径
            data = {
                'integration_cell_cluster': settings.INTEGRATION_SVG_PNG_DOWNLOAD + str(uuid_str) + '_cell_cluster.csv',
                'integration_umap_location': settings.INTEGRATION_SVG_PNG_DOWNLOAD + str(
                    uuid_str) + '_umap_location.csv'
            }
        except Exception as e:
            data = {
                'integration_cell_cluster': '',
                'integration_umap_location': '',
            }
        return JSONResponse(data=data)


class IntegrationZipDownloadViewSet(viewsets.ModelViewSet):
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """Integration zip下载脚本接口"""
        integration_type = self.request.GET.get('integration_type')  # 文件所在文件夹
        sample_id = self.request.GET.get('sample_id')  # sample_id 传的参数是Integration(列表页中sample_id的数据用,隔开控制在2-5个)
        uuid_str = uuid.uuid4()
        sample_id_list = sample_id.split(',')
        rds_base_path = '/data/browser_download'
        try:
            # R 脚本所在的文件夹
            r_script_path = '/data/Integration'
            out_zip_dir = '/data/Integration/result_data'
            out_name = os.path.join(out_zip_dir, '{}.zip'.format(uuid_str))
            zip = zipfile.ZipFile(out_name, "w", zipfile.ZIP_DEFLATED)  # outFullName为压缩文件的完整路径
            for rds_name in sample_id_list:
                # 组合文件路径
                path = os.path.join(rds_base_path, rds_name + '{}'.format('.zip'))
                zip.write(path, rds_name + '.zip')

            if integration_type == 'Seurat':
                r_script_name = os.path.join(r_script_path, 'Seurat.R')
                zip.write(r_script_name, 'Seurat.R')
            elif integration_type == 'Harmony':
                r_script_name = os.path.join(r_script_path, 'Harmony.R')
                zip.write(r_script_name, 'Harmony.R')
            else:
                r_script_name = os.path.join(r_script_path, 'Liger.R')
                zip.write(r_script_name, 'Liger.R')
            zip.close()
            # 返回zip文件压缩包
            data = {
                'integration_zip': settings.BASE_URL + 'Integration/result_data/' + str(uuid_str) + '.zip',
            }
        except Exception as e:
            print(e)
            data = {
                'integration_zip': '',
            }
        return JSONResponse(data=data)


class IntegrationExampleShowViewSet(viewsets.ModelViewSet):
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """Integration Example图片展示接口"""
        integration_type = self.request.GET.get('integration_type')  # 脚本类型
        try:
            uuid_str = 'cf9a0c26-6c12-4690-b5dd-384b6a9f1ab0'
            # 根据生成展示的svg图片转换成png格式的图片进行返回
            svg_path = '/data/Integration/Integration_example_picture/{}_{}.svg'.format(integration_type, uuid_str)
            png_path = '/data/Integration/Integration_example_picture/{}_{}.png'.format(integration_type, uuid_str)
            cairosvg.svg2png(url=svg_path, write_to=png_path, background_color='#ffffff', output_width=1200,
                             output_height=600)
            # 将生成的png转换成jpg
            jpg_path = '/data/Integration/Integration_example_picture/{}_{}.jpg'.format(integration_type, uuid_str)
            img = Image.open(png_path)
            img.save(jpg_path)
            # 返回示例图片地址
            data = {
                'integration_example_svg': settings.INTEGRATION_EXAMPLE_SVG_SHOW + integration_type + '_{}.svg'.format(
                    uuid_str),
                'integration_download_png': settings.INTEGRATION_EXAMPLE_SVG_SHOW + integration_type + '_{}.png'.format(
                    uuid_str),  # 详情png图片格式下载
                'integration_download_svg': settings.INTEGRATION_EXAMPLE_SVG_SHOW + integration_type + '_{}.svg'.format(
                    uuid_str),
                'integration_download_jpg': settings.INTEGRATION_EXAMPLE_SVG_SHOW + integration_type + '_{}.jpg'.format(
                    uuid_str),
                # 详情svg图片格式下载
            }
        except Exception as e:
            print(e)
            data = {
                'integration_example_svg': '',
                'integration_download_png': '',
                'integration_download_svg': '',
                'integration_download_jpg': ''

            }
        return JSONResponse(data=data)


class CellIdentificationSpeciesDownViewSet(viewsets.ModelViewSet):
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """CellIdentificationSpecies物种下拉框接口"""
        species_list = []
        try:
            path = r'/data/Cell_identification/species_classifier_data'
            datanames = os.listdir(path)
            for species in datanames:
                if species == 'Nicotiana_tabacum':
                    data = {
                        'label': 'Nicotiana attenuate',
                        'value': species
                    }

                elif species == 'Populus':
                    data = {
                        # 'label': 'Populus alba',
                        'label': 'Populus alba var. pyramidalis',
                        'value': species
                    }
                else:
                    data = {
                        'label': str(species).replace('_', ' '),
                        'value': species
                    }
                species_list.append(data)
        except Exception as e:
            species_list = []
        return JSONResponse(data=species_list)

    @list_route(methods=('get',), url_path='tissue_type_down')
    def tissue_type_down(self, request, *args, **kwargs):
        """CellIdentificationTissue物种组织下拉框"""
        specie_type = self.request.GET.get('specie_type')  # 物种类型
        species_tissue_list = []
        try:
            path = r'/data/Cell_identification/species_classifier_data/{}'.format(specie_type)
            datanames = os.listdir(path)
            for tissue in datanames:
                data = {
                    'label': str(tissue).split('_')[0],
                    'value': str(tissue).split('_')[0]
                }
                species_tissue_list.append(data)
        except Exception as e:
            species_tissue_list = []
        return JSONResponse(data=species_tissue_list)


class CellIdentificationUploadViewSet(viewsets.ModelViewSet):
    """SampleQc文件上传接口"""
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        '''
        CellIdentification rds文件上传接口
        '''
        file = self.request.FILES.get('myfile')
        try:
            fil_name = str(file.name).split('.')[0]
            files_uuid = uuid.uuid4()
            file_name = fil_name + '_' + str(files_uuid) + '.rds'
            file_url = os.path.join(settings.CELL_IDENTIFICATION_DIR + file_name)
            # 上传文件的话上传的指定的路径下,进行数据的比对
            with open(file_url, 'wb+') as f:
                # 分块写入文件
                for chunk in file.chunks():
                    f.write(chunk)
                data = {
                    'identification_path': file_url
                }
        except Exception as e:
            data = {
                'identification_path': ''
            }
        return JSONResponse(data=data)


class CellIdentificationSvgShowViewSet(viewsets.ModelViewSet):
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """CellIdentification图片展示和下载接口"""
        identification_type = self.request.GET.get('identification_type',
                                                   'Garnnet')  # 脚本类型 总共两个脚本1：Garnnet.R 2:Single.R
        specie_type = self.request.GET.get('specie_type', 'Arabidopsis_thaliana')  # 物种名
        tissue_type = self.request.GET.get('tissue_type', 'root')  # 物种组织
        identification_path = self.request.GET.get('identification_path', '')  # 上传rds文件地址
        try:
            tissue_classifier_rds_path = '/data/Cell_identification/species_classifier_data/{}/{}_classifier.rds'.format(
                specie_type, tissue_type)
            uuid_str = str(uuid.uuid4())
            a = f"Rscript /data/Cell_identification/{identification_type}.R -c {tissue_classifier_rds_path} -h {identification_path} -u {uuid_str}"
            f = os.popen(a)
            f.read()
            path_save = settings.CELL_IDENTIFICATION_PICTURE
            # 根据生成展示的svg图片转换成png格式的图片进行返回
            svg_path = '{}{}.svg'.format(path_save, uuid_str)
            png_path = '{}{}.png'.format(path_save, uuid_str)
            cairosvg.svg2png(url=svg_path, write_to=png_path)
            # 将生成的png转换成jpg
            jpg_path = '{}{}.jpg'.format(path_save, uuid_str)
            img = Image.open(png_path)
            img.save(jpg_path)
            # 返回示例图片地址
            data = {
                'classifier_picture_show_svg': settings.CELL_IDENTIFICATION_PICTURE_SVG + '{}.svg'.format(
                    uuid_str),  # 图片展示
                'classifier_picture_download_png': settings.CELL_IDENTIFICATION_PICTURE_SVG + '{}.png'.format(
                    uuid_str),  # 详情png图片格式下载
                'classifier_picture_download_svg': settings.CELL_IDENTIFICATION_PICTURE_SVG + '{}.svg'.format(
                    uuid_str),  # 详情svg图片格式下载
                'classifier_picture_download_jpg': settings.CELL_IDENTIFICATION_PICTURE_SVG + '{}.jpg'.format(
                    uuid_str),  # 详情jpg图片格式下载
            }
        except Exception as e:
            data = {
                'classifier_picture_show_svg': '',
                'classifier_picture_download_png': '',
                'classifier_picture_download_svg': '',
                'classifier_picture_download_jpg': '',
            }
        return JSONResponse(data=data)


class CellIdentificationExampleSvgShowViewSet(viewsets.ModelViewSet):
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """CellIdentification Example图片展示和下载接口"""
        try:
            # 返回示例图片地址
            data = {
                "classifier_picture_show_svg": settings.CELL_IDENTIFICATION_PICTURE_SVG + "example.svg",
                "classifier_picture_download_png": settings.CELL_IDENTIFICATION_PICTURE_SVG + "example.png",
                "classifier_picture_download_svg": settings.CELL_IDENTIFICATION_PICTURE_SVG + "example.svg",
                "classifier_picture_download_jpg": settings.CELL_IDENTIFICATION_PICTURE_SVG + "example.jpg"
            }
        except Exception as e:
            data = {
                'classifier_picture_show_svg': '',
                'classifier_picture_download_png': '',
                'classifier_picture_download_svg': '',
                'classifier_picture_download_jpg': '',
            }
        return JSONResponse(data=data)


class CellIdentificationPdftitleViewSet(viewsets.ModelViewSet):
    queryset = CellIdentificationInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CellIdentificationPdfTitleSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        '''CellIdentification Refrence  图片标题接口'''
        data_list = []
        for query in self.queryset:
            if query.title == 'Nicotiana_tabacum':
                label = 'Nicotiana attenuate' + '-' + query.cell_type
            elif query.title == 'Populus':
                # label = 'Populus alba' + '-' + query.cell_type
                label = 'Populus alba var. pyramidalis' + '-' + query.cell_type
            else:
                # label = query.title.replace('_', ' ') + ' ' + query.cell_type
                label = query.title.replace('_', ' ') + '-' + query.cell_type
            data = {
                'value': query.title + '-' + str(query.cell_type).replace(' ',
                                                                          '_') if ' ' in query.cell_type else query.title + '-' + str(
                    query.cell_type),
                'lit_id': query.lit_id,
                'project_id': query.project_id,
                'rds_name': query.rds_name,
                'cell_identification_pdf': settings.CELL_IDENTIFICATION_PDF + '{}.png'.format(query.pdf_name),  # 图片展示
            }

            data['label'] = label
            data_list.append(data)
        return JSONResponse(data=data_list)


# a = 'Rscript Cell_ident_for_seuratQC.R -r Arabidopsis_thaliana_Root.rds -q 5e03450a-4782-11ed-ada6-fa163e6dc4d5.rds -u 12345678'


class CellIdentificationReferenceDetailViewSet(viewsets.ModelViewSet):
    queryset = LiteratureInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CellIdentificationReferenceDetaileSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        lit_id = self.request.GET.get('lit_id')
        if lit_id == 'LT9LT29':
            data = {
                "code": 200,
                "data": {
                    "page_size": 15,
                    "results": [
                        {
                            "species_name": "Arabidopsis_thaliana",
                            "cells_reference": 5750,
                            "pmid": "33955487,34687312",
                            "doi": "https://doi.org/10.1093/plcell/koaa060,https://doi.org/10.1093/plphys/kiab489",
                            "data_type": "",
                            "species_name_down": "Arabidopsis thaliana",
                            "title": "Arabidopsis thaliana-Leaf",
                            # "cell_identification_pdf": ["http://159.138.151.49:8080/classifier_png/LT9LT29.png"]
                            # 测试环境地址
                            "cell_identification_pdf": [
                                "https://www.tobaccodb.org/server_ipscdb/classifier_png/LT9LT29.png"]
                            # 烟院地址
                        }
                    ],
                    "count": 1
                }
            }
            return JSONResponse(data=data)
        elif lit_id == 'LT40':
            data = {
                "code": 200,
                "data": {
                    "page_size": 15,
                    "results": [
                        {
                            "species_name": "Popular_alba",
                            "cells_reference": 4610,
                            "pmid": "34809675",
                            "doi": "https://doi.org/10.1186/s13059-021-02537-2",
                            "data_type": "",
                            "species_name_down": "Populus alba var. pyramidalis",
                            "title": "Populus alba var. pyramidalis-Stem",
                            # "cell_identification_pdf": ["http://159.138.151.49:8080/classifier_png/LT40.png"]
                            # 测试环境地址
                            "cell_identification_pdf": [
                                "https://www.tobaccodb.org/server_ipscdb/classifier_png/LT9LT29.png"]
                            # 烟院地址
                        }
                    ],
                    "count": 1
                }
            }
            return JSONResponse(data=data)
        cluster_marker_queryset = LiteratureInfo.objects.filter(lit_id__contains=lit_id)
        queryset_values_list = self.paginate_queryset(cluster_marker_queryset)
        serializer = CellIdentificationReferenceDetaileSerializer(queryset_values_list, many=True)
        return self.get_paginated_response(serializer.data)


class CellIdentificationReferenceSampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SampleSearchSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        project_id = self.request.GET.get('project_id')
        if project_id == 'GSE161482,ERX6530535':
            cluster_marker_queryset = self.queryset.filter(project_id__in=['GSE161482', 'ERX6530535'])
        else:
            cluster_marker_queryset = self.queryset.filter(project_id__contains=project_id)
        queryset_values_list = self.paginate_queryset(cluster_marker_queryset)
        serializer = SampleSearchSerializer(queryset_values_list, many=True)
        return self.get_paginated_response(serializer.data)


class CellIdentificationReferenceUploadViewSet(viewsets.ModelViewSet):
    """Cell_Idetification文件上传接口"""
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        file = self.request.FILES.get('myfile')
        try:
            if file.name:
                files_uuid = uuid.uuid4()
                # 如果上传的是 rds 文件直接存储在 /data/Sample_QC/upload_data 下
                file_name = str(files_uuid) + '_' + file.name
                file_url = os.path.join(settings.CELL_IDENTIFICATION_CSV_UPLOAD + file_name)
                # 上传文件的话上传的指定的路径下,进行数据的比对
                with open(file_url, 'wb+') as f:
                    # 分块写入文件
                    for chunk in file.chunks():
                        f.write(chunk)
            else:
                return JSONResponse(data={'msg': 'File upload failed！', 'file_name': ''})
            return JSONResponse(data={'msg': 'File upload successfully！', 'file_name': file_name})
        except Exception as e:
            return JSONResponse(data={'msg': 'File upload failed！', 'file_name': ''})


class CellIdentificationCreateCsvViewSet(viewsets.ModelViewSet):
    """Cell_Idetification文件上传接口"""
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = self.request.GET.get('tissue', 'Root')
        file_name = self.request.GET.get('file_name')
        num_top = self.request.GET.get('num_top')
        try:
            str_uuid = str(uuid.uuid4())
            f = os.popen(
                f'Rscript /data/Cell_identification/Cell_ident_for_CSV.R -r {species_name}_{tissue}.rds -c {file_name} -n {num_top} -u {str_uuid}'.format(
                    species_name=species_name, tissue=tissue,
                    file_name=file_name, num_top=num_top, str_uuid=str_uuid))
            f.read()
            # 返回生成文件链接供下载时传参使用
            data = {
                "classifier_cell_type_csv": "{str_uuid}_Cell_type.csv".format(
                    str_uuid=str_uuid),
                "classifier_cors_matrix_csv": "{str_uuid}_cors_matrix.csv".format(
                    str_uuid=str_uuid),
            }
        except Exception as e:
            print(e)
            data = {
                "classifier_cell_type_csv": '',
                "classifier_cors_matrix_csv": '',
            }
        return JSONResponse(data=data)


def index_str(x):
    value = x.replace('RNA.', '').replace('.', ' ')
    return value


class CellIdentificationCellTypeCsvViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SampleSearchSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        file_name = self.request.GET.get('file_name')
        top = self.request.GET.get('top', '3')
        cell_type = request.GET.get('cell_type', 'Primary cell type')
        species_name = self.request.GET.get('species_name', 'Arabidopsis_thaliana')
        try:
            file_path = os.path.join(settings.CELL_IDENTIFICATION_ZIP_CSV_DOWNLOAD, "{}".format(file_name))
            # file_path = r'D:\plant_marker_backend\excel\3e7a5523-e9a6-42fc-a1e2-6fb148a3c3ac_cors_matrix.csv'
            # file_path = os.path.join(settings.EXCEL_FILE, 'fa5c478c-e2ea-4e89-a002-60438b8b8699_cors_matrix.csv')
            value_data = pd.read_csv(file_path)
            # print(value_data)
            # 校验
            # res = int(all(value.startswith(SPECIE_GENE_RE.get(species_name)) for value in value_data["Cell Name"]))
            # print(res)
            # if res == 1:
            # 清除 索引中的 RNA. 和 .替换成空格
            value_data['index'] = value_data.index
            value_data['index'] = value_data['index'].apply(index_str)
            value_data = value_data.set_index('index')
            value_data = value_data.T
            last_data_list = []
            valuse_list = []
            coloum_list = ['Quinary cell type', 'Fourth cell type', 'Tertiary cell type', 'Secondary cell type',
                           'Primary cell type']
            coloum_list = coloum_list[::-1][0:int(top)][::-1]
            for index, row in value_data.iterrows():
                row = row.sort_values(ascending=False)
                # 根据 传入的 top 切割
                row_values = row.index.values[:int(top)]
                row_data = dict(zip(coloum_list, row_values))
                row_data['Cell Name'] = index
                last_data_list.append(row_data)
                valuse_list.extend(row_values)
            last_data = pd.DataFrame(last_data_list)
            # #新增
            valuse_list = last_data[cell_type].to_list()
            histogram_count = Counter(valuse_list)
            obj_data = {
                "code": 200,
                "data": {
                    'cellt_ype_data': last_data,
                    'histogram_count': histogram_count,
                    'coloum_list': coloum_list[::-1]

                }
            }
            # else:
            #     obj_data = {
            #         "code": 200,
            #         'message': '您上传的文件格式有问题,请确认后从新上传！！！',
            #         "data": {
            #             'cellt_ype_data': [],
            #             'histogram_count': [],
            #             'coloum_list': []
            #         }
            #     }
        except Exception as e:
            print(e)
            obj_data = {
                "code": 200,
                "data": {
                    'cellt_ype_data': {},
                    'histogram_count': {},
                    'coloum_list': []
                }
            }
        return JSONResponse(data=obj_data)


class CellIdentificationCellTypemapViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SampleSearchSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        file_name = self.request.GET.get('file_name')
        top = self.request.GET.get('top', '3')
        cell_type = request.GET.get('cell_type', 'Primary cell type')
        species_name = self.request.GET.get('species_name', 'Arabidopsis_thaliana')
        try:
            file_path = os.path.join(settings.CELL_IDENTIFICATION_ZIP_CSV_DOWNLOAD, "{}".format(file_name))
            # file_path = r'D:\plant_marker_backend\excel\Arabidopsis_thaliana_Leaf.csv'
            value_data = pd.read_csv(file_path)
            # res = int(all(value.startswith(SPECIE_GENE_RE.get(species_name)) for value in value_data["Cell Name"]))
            # if res == 1:
            # 清除 索引中的 RNA. 和 .替换成空格
            value_data['index'] = value_data.index
            value_data['index'] = value_data['index'].apply(index_str)
            value_data = value_data.set_index('index')
            value_data = value_data.T
            last_data_list = []
            valuse_list = []
            # coloum_list = ['Primary cell type', 'Secondary cell type', 'Tertiary cell type', 'Fourth cell type','Quinary cell type']
            coloum_list = ['Quinary cell type', 'Fourth cell type', 'Tertiary cell type', 'Secondary cell type',
                           'Primary cell type']
            coloum_list = coloum_list[::-1][0:int(top)][::-1]
            for index, row in value_data.iterrows():
                row = row.sort_values(ascending=False)
                # 根据 传入的 top 切割
                row_values = row.index.values[:int(top)]
                row_data = dict(zip(coloum_list, row_values))
                row_data['Cell Name'] = index
                last_data_list.append(row_data)
                valuse_list.extend(row_values)
            last_data = pd.DataFrame(last_data_list)
            # #新增
            valuse_list = last_data[cell_type].to_list()
            histogram_count = Counter(valuse_list)
            obj_data = {
                "code": 200,
                "data": {
                    'histogram_count': histogram_count,

                }
            }
        # else:
        #     obj_data = {
        #         "code": 200,
        #         'message': '您上传的文件格式有问题,请确认后从新上传！！！',
        #         "data": {
        #             'cellt_ype_data': [],
        #             'histogram_count': [],
        #             'coloum_list': []
        #         }
        #     }

        except Exception as e:
            print(e)
            obj_data = {
                "code": 200,
                "data": {
                    'histogram_count': [],
                }
            }
        return JSONResponse(data=obj_data)


class CellIdentificationCorsMatrixCsvViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SampleSearchSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        page = self.request.GET.get('page')
        page_size = self.request.GET.get('page_size')
        file_name = self.request.GET.get('file_name')
        try:
            page = int(page)
            page_size = int(page_size)
            start = (page - 1) * page_size
            end = page * page_size
            file_path = os.path.join(
                settings.CELL_IDENTIFICATION_ZIP_CSV_DOWNLOAD, "{}".format(file_name))
            obj_data = pd.read_csv(file_path)
            page_total = len(obj_data)
            obj_data = obj_data[start:end]  # 分页
            index_list = obj_data.index.tolist()  # 该代码返回所有的索引号组成的列表
            obj_data = obj_data.to_dict(orient="records")  # dataframe 转换成 字典
            index_data = [{'id': index} for index in index_list]
            for index, one in enumerate(obj_data):
                one.update(index_data[index])  # 添加dataframe 索引列到数据中
            obj_data = {
                "code": 200,
                "data": {
                    "page_size": int(end - start),
                    "results": obj_data,
                    "count": page_total
                }
            }
        except Exception as e:
            print(e)
            obj_data = {
                "code": 200,
                "data": []
            }
        return JSONResponse(data=obj_data)


class CellIdentificationCsvZipDownloadViewSet(viewsets.ModelViewSet):
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """Integration zip下载脚本接口"""
        file_name = self.request.GET.get('file_name')  # 文件名
        file_type = self.request.GET.get('file_type')  # 区别下载文件类型
        try:
            file_name_list = ['Cell_type.csv', 'Cell_type_probility.csv', 'cors_matrix.csv', 'top_cors.csv']
            files_uuid = file_name.split('_')[0]
            if file_type == 'all':
                out_name = os.path.join(settings.CELL_IDENTIFICATION_ZIP_CSV_DOWNLOAD, '{}.zip'.format(files_uuid))
                zip = zipfile.ZipFile(out_name, "w", zipfile.ZIP_DEFLATED)  # outFullName为压缩文件的完整路径
                for zip_name in file_name_list:
                    # 组合文件路径
                    path = os.path.join(settings.CELL_IDENTIFICATION_ZIP_CSV_DOWNLOAD,
                                        '{files_uuid}_{zip_name}'.format(files_uuid=files_uuid, zip_name=zip_name))
                    zip.write(path, zip_name)
                zip.close()
                # 返回zip文件压缩包
                data = {
                    'cell_identification_csv_zip': settings.CELL_IDENTIFICATION_ZIP_CSV + str(files_uuid) + '.zip',
                }
                # 下载示例csv
            elif file_type == 'example':
                data = {
                    'cell_identification_csv_zip': settings.CELL_IDENTIFICATION_ZIP_CSV + 'test.csv',
                }
            elif file_type == 'cell_type':
                data = {
                    'cell_identification_csv_zip': settings.CELL_IDENTIFICATION_ZIP_CSV + str(
                        files_uuid) + '_Cell_type.csv',
                }
            elif file_type == 'cors_matrix':
                data = {
                    'cell_identification_csv_zip': settings.CELL_IDENTIFICATION_ZIP_CSV + str(
                        files_uuid) + '_cors_matrix.csv',
                }
            else:
                data = {
                    'cell_identification_csv_zip': settings.CELL_IDENTIFICATION_ZIP_CSV + file_name,
                }
        except Exception as e:
            print(e)
            data = {
                'integration_zip': '',
            }
        return JSONResponse(data=data)


class CellBrowseStatisticsViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    marker_queryset = MarkerGenesInfo.objects.all()
    sra_information_queryset = SraInformation.objects.all()
    serializer_class = PlantHomeUmaptSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get', ]

    def list(self, request, *args, **kwargs):
        # 统计去重之后的chemistry
        chemistry_data = list(set(self.queryset.values_list('chemistry', flat=True).exclude(chemistry='')))
        # 通过chemistry 查找对应的project_id去重之后的个数
        data_list = []
        for chemistry in chemistry_data:
            dic = {}
            project_id_count = len(
                list(set(self.queryset.filter(chemistry=chemistry).values_list('project_id',
                                                                               flat=True))))
            dic['name'] = chemistry
            dic['value'] = project_id_count
            data_list.append(dic)
        # 统计的是每个物种对应所有cell的和
        species_cells_list = self.sra_information_queryset.values('species').annotate(
            cell_count=Sum('cells')
        )
        speace_cell_count = []
        for species_cell in species_cells_list:
            cells_count = species_cell['cell_count'] if species_cell['cell_count'] else 0
            dict_data = {
                'name': species_cell['species'],
                'value': cells_count
            }
            speace_cell_count.append(dict_data)
        # 统计基因标记的和
        marker_list = self.marker_queryset.values('species').annotate(value=Count('gene'))
        all_data = {
            'speace_cell_total': speace_cell_count,
            'project_id_total': data_list,
            'marker_total': marker_list,
        }

        return JSONResponse(data=all_data)


class CellSpeciesTissuesViewSet(viewsets.ModelViewSet):
    '''物种组织下拉框'''
    queryset = Sample.objects.all()
    serializer_class = PlantHomeUmaptSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get', ]

    def list(self, request, *args, **kwargs):
        specie_tissue_data = [
            {
                'name': 'Arabidopsis thaliana',
                'label': 'Arabidopsis_thaliana',
                'value': ['Root tip', 'Leaf', 'Shoot apex', 'Root'],
            }, {
                'name': 'Oryza sativa',
                'label': 'Oryza_sativa',
                'value': ['Root', 'Leaf'],
            }, {
                'name': 'Zea mays',
                'label': 'Zea_mays',
                'value': ['Ear', 'Leaf'],
            }, {
                'name': 'Nicotiana attenuate',
                'label': 'Nicotiana_tabacum',
                'value': ['Flower'],
            }, {
                'name': 'Populus alba var. pyramidalis',
                'label': 'Popular_alba',
                'value': ['Stem'],
            }

        ]
        return JSONResponse(data=specie_tissue_data)


class CellIdentificationFilterCsvViewSet(viewsets.ModelViewSet):
    """Cell_ident_for_seuratQC文件上传接口"""
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name')
        tissue = self.request.GET.get('tissue')
        uuid_rds = self.request.GET.get('uuid_rds')
        # 获取rds文件名
        uuid_rds_split = uuid_rds.split('filter_rds/')[1]
        try:
            str_uuid = str(uuid.uuid4())
            # print(str_uuid)
            f = os.popen(
                f'Rscript /data/Cell_identification/Cell_ident_for_seuratQC.R  -r {species_name}_{tissue}.rds -q  {uuid_rds_split} -u {str_uuid}'.format(
                    species_name=species_name, tissue=tissue, uuid_rds_split=uuid_rds_split, str_uuid=str_uuid))
            f.read()
            # 返回生成文件链接供下载时传参使用
            data = {
                "classifier_cell_type_csv": "{str_uuid}_Cell_type.csv".format(
                    str_uuid=str_uuid),
                "classifier_cors_matrix_csv": "{str_uuid}_cors_matrix.csv".format(
                    str_uuid=str_uuid),
            }
        except Exception as e:
            print(e)
            data = {
                "classifier_cell_type_csv": '',
                "classifier_cors_matrix_csv": '',
            }
        return JSONResponse(data=data)


class BrowseListViewSet(viewsets.ModelViewSet):
    """Browse列表页接口"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name')
        title = self.request.GET.get('title')
        try:
            query_list = []
            if species_name:
                query_list.append(Q(species_name=species_name))
            if title:
                query_list.append(Q(title__icontains=title))
        except Exception as e:
            query_list = []
        # querysets = self.queryset.filter(*query_list).exclude(qc_cells='0')
        querysets = self.queryset.filter(*query_list)
        page = self.paginate_queryset(querysets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(query_list, many=True)
        return JSONResponse(serializer.data)


class SraInformationViewSet(viewsets.ModelViewSet):
    """Browse》Project information列表接口"""
    queryset = SraInformation.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SraInformationSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species = self.request.GET.get('species', '')
        tissue = self.request.GET.get('tissue', '')
        bioProject = self.request.GET.get('bioProject', '')
        dataset = self.request.GET.get('dataset', '')
        try:
            query_list = []
            if species:
                query_list.append(Q(species__contains=species))
            if tissue:
                query_list.append(Q(tissue__contains=tissue))
            if bioProject:
                query_list.append(Q(bio_project__contains=bioProject))
            if dataset:
                query_list.append(Q(dataset__contains=dataset))
        except Exception as e:
            query_list = []
        # querysets = self.queryset.filter(*query_list).exclude(qc_cells='0')
        querysets = self.queryset.filter(*query_list)
        page = self.paginate_queryset(querysets)
        serializer = self.get_serializer(page, many=True)

        result_data = []
        for item in serializer.data:
            sample_id = item['dataset_id'] + "_" + item['dataset']
            browser_download = settings.BASE_URL + 'browser_download/{}.zip'.format(sample_id)
            item['browser_download'] = browser_download
            item['sample_id'] = sample_id
            result_data.append(item)
        return self.get_paginated_response(serializer.data)

    @list_route(methods=('get',), url_path='information_drop_down')
    def SraInformationDropDownViewSet(self, request, *args, **kwargs):
        species = self.request.GET.get('species', '')
        tissue = self.request.GET.get('tissue', '')
        bioProject = self.request.GET.get('bioProject', '')
        dataset = self.request.GET.get('dataset', '')
        drop_type = self.request.GET.get('drop_type', 'species')

        query_list = []
        if species:
            query_list.append(Q(species=species))
        if tissue:
            query_list.append(Q(tissue=tissue))
        if bioProject:
            query_list.append(Q(bio_project=bioProject))
        if dataset:
            query_list.append(Q(dataset=dataset))
        if drop_type == 'bioProject':
            drop_type = 'bio_project'

        query_data = self.queryset.filter(*query_list).values(drop_type).distinct()
        result_data = [obj[drop_type] for obj in query_data]
        return JSONResponse(result_data)


class MarkerTreeDataViewSet(viewsets.ModelViewSet):
    """Marker页面左侧树状图数据"""
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name', 'Arabidopsis thaliana')
        # 全部树状图数据
        data = markers_tree_data
        # 匹配一级节点，返回对应一级节点的数据
        for tree_data in data:
            if tree_data['name'] == species_name:
                data = tree_data

        return JSONResponse(data)


class MarkerHistogramViewSet(viewsets.ModelViewSet):
    """Marker页面点击树状图一级节点的柱状图数据"""
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name', 'Arabidopsis thaliana')
        data = marker_histogram_data
        for species in data:
            if species['species_name'] == species_name:
                data = species

        return JSONResponse(data)


class MarkerDetailsSearchData(viewsets.ModelViewSet):
    """Marker Details 列表 搜索条件"""
    queryset = MarkerGenesInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = MarkerGenesInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name', 'Arabidopsis thaliana')
        query_data = self.queryset.filter(species=species_name).exclude(avg_log2FC=9999).aggregate(
            pct_diff_min=Min('pct_diff'), pct_diff_max=Max('pct_diff'),
            avg_log2FC_min=Min('avg_log2FC'), avg_log2FC_max=Max('avg_log2FC')
        )
        data = {
            'pct_diff': {
                'min': query_data['pct_diff_min'],
                'max': query_data['pct_diff_max']
            },
            'avg_log2FC': {
                'min': query_data['avg_log2FC_min'],
                'max': query_data['avg_log2FC_max']
            }
        }
        return JSONResponse(data)


class MarkerDetailsListViewSet(viewsets.ModelViewSet):
    """Marker页面右侧列表Details列表数据"""
    queryset = MarkerGenesInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = MarkerGenesInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        result_data = self.query_list(self, request)
        # 分页
        page = self.paginate_queryset(result_data)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(result_data, many=True)
        return JSONResponse(serializer.data)

    @list_route(methods=('get',), url_path='marker_details_download')
    def marker_details_download(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name', 'Arabidopsis thaliana')
        result_data = self.query_list(self, request)
        serializer = self.get_serializer(result_data, many=True)
        # 文件名称
        file_name = 'marker_' + species_name + '_details.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
        writer = csv.writer(response)
        # 表头
        # headers = ['gene', 'name', 'p_val', 'p_val_adj', 'pct_1','pct_2','pct_diff','avg_log2FC','clusterName','celltype_id','species','tissue','dataset']
        headers = MarkerGenesInfoSerializer.Meta.fields;
        writer.writerow(headers)
        for item in serializer.data:
            row = []
            # 提取每条记录对应字段的值并添加到行列表中
            for header in headers:
                value = item[header] if header in item else ''
                row.append(value)
            writer.writerow(row)

        return response

    def query_list(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name', 'Arabidopsis thaliana')
        tissue_name = self.request.GET.get('tissue_name', '')
        cell_name = self.request.GET.get('cell_name', '')
        pct_diff_min = self.request.GET.get('pct_diff_min')
        pct_diff_max = self.request.GET.get('pct_diff_max')
        avg_log2FC_min = self.request.GET.get('avg_log2FC_min')
        avg_log2FC_max = self.request.GET.get('avg_log2FC_max')
        search_gene = self.request.GET.get('search_gene', '')
        try:
            # 拼接查询条件
            parameter_list = []
            if species_name:
                parameter_list.append(Q(species=species_name))
            if tissue_name:
                parameter_list.append(Q(tissue=tissue_name))
            if cell_name:
                parameter_list.append(Q(clusterName=cell_name))
            if pct_diff_min:
                parameter_list.append(Q(pct_diff__gte=pct_diff_min))
            if pct_diff_max:
                parameter_list.append(Q(pct_diff__lte=pct_diff_max))
            if avg_log2FC_min:
                parameter_list.append(Q(avg_log2FC__gte=avg_log2FC_min))
            if avg_log2FC_max:
                parameter_list.append(Q(avg_log2FC__lte=avg_log2FC_max))
            if search_gene:
                parameter_list.append(Q(gene__contains=search_gene) | Q(name__contains=search_gene))
        except Exception as e:
            parameter_list = []
        # 获取数据
        query_list = self.queryset.filter(*parameter_list).exclude(avg_log2FC=9999).order_by('gene')
        return query_list


class MarkerSummaryListViewSet(viewsets.ModelViewSet):
    """ Marker页面右侧列表Summary列表数据 """
    queryset = SummaryResultInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SummaryResultInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        result_data = self.query_list(self, request)
        page = self.paginate_queryset(result_data)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    @list_route(methods=('get',), url_path='marker_summary_download')
    def marker_summary_download(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name', 'Arabidopsis thaliana')
        result_data = self.query_list(self, request)
        serializer = self.serializer_class(result_data, many=True)
        # 文件名称
        file_name = 'marker_' + species_name + '_summary.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)

        writer = csv.writer(response)
        # 表头
        headers = ['gene', 'name', 'cellType_id', 'source_no', 'dataset', 'classic_marker', 'cell_type']
        writer.writerow(headers)

        for item in serializer.data:
            row = []
            # 提取每条记录对应字段的值并添加到行列表中
            for header in headers:
                if header == 'cell_type':
                    header = "clusterName"
                value = item[header] if header in item else ''
                row.append(value)
            writer.writerow(row)

        return response

    def query_list(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name', 'Arabidopsis thaliana')
        tissue_name = self.request.GET.get('tissue_name', '')
        cell_name = self.request.GET.get('cell_name', '')
        search_gene = self.request.GET.get('search_gene', '')
        query_type = self.request.GET.get('query_type', '')
        query_params = Q(species=species_name)

        if tissue_name == "Whole Plant" or tissue_name == "WholePlant":
            tissue_name = ""
        # Arabidopsis thaliana物种的Root tip组织没有数据，因此获取的Root的数据
        if tissue_name == "Root tip" or tissue_name == "Root_tip":
            tissue_name = "Root"

        if tissue_name:
            query_params = query_params & Q(tissue=tissue_name)
        if cell_name:
            query_params = query_params & Q(clusterName=cell_name)
        if search_gene:
            query_params = query_params & (Q(gene__contains=search_gene) | Q(name__contains=search_gene))

        # 首页二级页面调用时query_type不为空
        if query_type and species_name == 'Arabidopsis thaliana' and tissue_name != 'Shoot' and tissue_name != 'Embryo' and tissue_name != 'Inflorescence':
            query_params = query_params & Q(source_no__gt=1)
        if species_name == 'Zea mays' or species_name == 'Zea_mays':
            # 玉米物种以组织排序
            data = self.queryset.filter(query_params).order_by('tissue', '-classic_marker')
        elif species_name == 'Catharanthus roseus' or species_name == 'Catharanthus_roseus':
            # 长春花以基因排序
            data = self.queryset.filter(query_params).order_by('-gene', '-classic_marker')
        else:
            data = self.queryset.filter(query_params).order_by('id')
        return data


class AtlasExpressedGeneCellTypeCountViewSet(viewsets.ModelViewSet):
    """Atlas热力图和柱状图统计接口"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name')
        tissue = self.request.GET.get('tissue', 'Root')
        view_by = self.request.GET.get('view_by', 'Cell_type')

        try:
            hot_png_path = settings.BASE_URL + 'source_material/{}/{}/pearson_{}.png'.format(
                species_name, tissue, view_by
            )
            # 读取物种对应的文件
            file_path = os.path.join(
                settings.ATLAS_HOT_PNG_DIR,
                "umap/{species_name}/{tissue}/expresse_gene_count_{view_by}.txt".format(species_name=species_name,
                                                                                        tissue=tissue, view_by=view_by))
            with open(file_path, encoding='utf-8') as file:
                content = file.read()
            cell_count = eval(content)
            # 处理成键值对
            dic_list = [{"name": [a for a in i.keys()][0], 'value': [a for a in i.values()][0]} for i in cell_count]
            dic_list = sorted(dic_list, key=lambda x: x['value'], reverse=True)

            data = {
                "cell_count": dic_list,
                "hot_png": hot_png_path
            }
        except Exception as e:
            data = {
                "cell_count": '',
                # "hot_png": '' , 数据不全 临时处理
                "hot_png": hot_png_path
            }

        return JSONResponse(data=data)


class AtlasGeneCellTypeCountViewSet(viewsets.ModelViewSet):
    """Atlas热力图和柱状图统计接口"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name')
        tissue = self.request.GET.get('tissue', 'Root')
        view_by = self.request.GET.get('view_by', 'Cell_type')
        try:

            # 读取物种对应的文件
            file_path = os.path.join(
                settings.ATLAS_HOT_PNG_DIR,
                "umap/{species_name}/{tissue}/umap_gene_count_{view_by}.txt".format(species_name=species_name,
                                                                                    tissue=tissue, view_by=view_by))
            with open(file_path, encoding='utf-8') as file:
                cell_count = file.read()
            cell_count_dic = eval(cell_count)
            # 处理成键值对
            dic_list = [{'name': k, 'value': v} for k, v in cell_count_dic.items()]
            dic_list = sorted(dic_list, key=lambda x: x['value'], reverse=True)
            data = {
                "cell_count": dic_list,
            }
        except Exception as e:
            data = {
                "cell_count": '',
            }

        return JSONResponse(data=data)


class ExpressedGeneCellTypeCountViewSet(viewsets.ModelViewSet):
    """热力图和柱状图统计接口"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        lit_id = self.request.GET.get('lit_id')
        project_id = self.request.GET.get('project_id')
        species_name = self.request.GET.get('species_name')
        try:
            if species_name == 'Popular_alba':
                species_name = 'Populus'
            else:
                species_name = species_name
            file_path = os.path.join(
                settings.CELL_EXPRESSION_DIR,
                "{}/{}_{}/{}".format(species_name, lit_id, project_id, 'expresse_gene_count.txt'))
            with open(file_path, encoding='utf-8') as file:
                content = file.read()
            cell_count = eval(content)
            # 处理成键值对
            dic_list = [{"name": [a for a in i.keys()][0], 'value': [a for a in i.values()][0]} for i in cell_count]
            dic_list = sorted(dic_list, key=lambda x: x['value'], reverse=True)
            data = {
                "cell_count": dic_list,
                "hot_png": settings.CELL_EXPRESSION_PICTURE_PNG + '{}_{}_hot.png'.format(lit_id, project_id),
            }
        except Exception as e:
            data = {
                "cell_count": '',
                "hot_png": '',
            }

        return JSONResponse(data=data)


class AtlasExpressedGeneViolinBoxPlotViewSet(viewsets.ModelViewSet):
    """Atlas手风琴和箱图接口"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        tissue = self.request.GET.get('tissue')
        species_name = self.request.GET.get('species_name')
        gene_id = self.request.GET.get('gene_id')
        type = self.request.GET.get('type', 'umap_data')
        view_type = request.GET.get('view_type', 'Cell_type')
        try:
            # 返回绘制的手风琴和箱图
            violinplot_png, boxplot_png = draw_atlas_violinplot(species_name, tissue, type, gene_id, view_type)
            if violinplot_png:
                data = {
                    "violinplot_png": settings.BASE_URL + 'violinplot_png/' + violinplot_png,  # 手风琴
                    "boxplot_png": settings.BASE_URL + 'violinplot_png/' + boxplot_png  # 箱图
                }
            else:
                data = {
                    "violinplot_png": settings.BASE_URL + 'violinplot_png/' + '4d30409b-57b0-48e0-bddf-5fd45222be64_boxplot.png',
                    # 手风琴
                    "boxplot_png": settings.BASE_URL + 'violinplot_png/' + '4d30409b-57b0-48e0-bddf-5fd45222be64_boxplot.png'
                    # 箱图
                }

        except Exception as e:
            print(e)
            data = {
                "violinplot_png": settings.BASE_URL + 'violinplot_png/' + '4d30409b-57b0-48e0-bddf-5fd45222be64_boxplot.png',
                # 手风琴
                "boxplot_png": settings.BASE_URL + 'violinplot_png/' + '4d30409b-57b0-48e0-bddf-5fd45222be64_boxplot.png'
                # 箱图
            }
        return JSONResponse(data=data)


class ExpressedGeneViolinBoxPlotViewSet(viewsets.ModelViewSet):
    """手风琴和箱图接口"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        lit_id = self.request.GET.get('lit_id')
        project_id = self.request.GET.get('project_id')
        gene_id = self.request.GET.get('gene_id')
        species_name = self.request.GET.get('species_name')
        try:
            if species_name == 'Popular_alba':
                species_name = 'Populus'
            else:
                species_name = species_name
            # 返回绘制的手风琴和箱图
            violinplot_png, boxplot_png = draw_violinplot(lit_id, project_id, gene_id, species_name)
            data = {
                "violinplot_png": settings.CELL_EXPRESSION_VIOLINPOLT_PNG + violinplot_png,  # 手风琴
                "boxplot_png": settings.CELL_EXPRESSION_VIOLINPOLT_PNG + boxplot_png  # 箱图
            }
        except Exception as e:
            print(e)
            data = {
                "violinplot_png": '',
                "boxplot_png": '',
            }
        return JSONResponse(data=data)


class ExpressedUmapDatasetViewSet(viewsets.ModelViewSet):
    """umap散点图接口"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        lit_id = self.request.GET.get('lit_id')
        project_id = self.request.GET.get('project_id')
        species_name = self.request.GET.get('species_name')
        gene_id = self.request.GET.get('gene_id')
        umap_type = request.GET.get('umap_type', 'Cell_type')
        # 先通过gene_symbol找gene_id 没的话 在直接通过gene_id 去找
        if CellMarkerInfo.objects.filter(gene_symbol=gene_id).exists():
            gene_id = CellMarkerInfo.objects.filter(gene_symbol=gene_id).first().gene_id
        else:
            gene_id = gene_id
        try:
            if species_name == 'Popular_alba':
                species_name = 'Populus'
            else:
                species_name = species_name
            if not gene_id:
                file_path = os.path.join(
                    settings.CELL_EXPRESSION_DIR,
                    "{}/{}_{}/{}".format(species_name, lit_id, project_id, 'umap_data.csv'))
                # 读取物种对应的文件
                # umap_data = pd.read_csv(file_path, usecols=['UMAP_1', 'UMAP_2', 'Clusters', 'Cell_type'])
                umap_data = pd.read_csv(file_path, usecols=['UMAP_1', 'UMAP_2', 'Clusters', umap_type])

                umap_data = umap_data.iloc[1:40000]
                # 通过cell_type组成的df
                cell_type_df = umap_data
                # 将Clusters和Cell_type进行拼接聚合
                # umap_data['Clusters_Cell_type'] = umap_data['Clusters'].map(str) + ':' + umap_data['Cell_type'].map(str)
                umap_data['Clusters_Cell_type'] = umap_data['Clusters'].map(str) + ':' + umap_data[umap_type].map(str)
                clusters_data = umap_data.groupby(['Clusters_Cell_type'])
                data_list = []
                if lit_id != 'LT68':
                    for group_name, group_data in clusters_data:
                        group_data = group_data[['UMAP_1', 'UMAP_2']]
                        data = {
                            'name': group_name.split(':')[1],
                            'data': group_data.to_dict('split').get('data', []),
                            'sort': int(group_name.split(':')[0])
                        }
                        data_list.append(data)
                    data_list = sorted(data_list, key=lambda x: x['sort'])
                else:
                    for group_name, group_data in clusters_data:
                        group_data = group_data[['UMAP_1', 'UMAP_2']]
                        data = {
                            'name': group_name.split(':')[1],
                            'data': group_data.to_dict('split').get('data', []),
                            'sort': group_name.split(':')[1]
                        }
                        data_list.append(data)
                # 组合cell_type的df
                # cell_type_df = cell_type_df.groupby('Cell_type')
                cell_type_df = cell_type_df.groupby(umap_type)
                cell_type_data_list = []
                for group_name, group_data in cell_type_df:
                    group_data = group_data[['UMAP_1', 'UMAP_2']]
                    data = {
                        'name': str(group_name),
                        'data': group_data.to_dict('split').get('data', []),
                    }
                    cell_type_data_list.append(data)
                all_data_ = {
                    'clusters_data': data_list,
                    'cell_type_data': cell_type_data_list,
                }
            else:
                umap_path = os.path.join(
                    settings.CELL_EXPRESSION_DIR,
                    "{}/{}_{}/{}".format(species_name, lit_id, project_id, 'umap_data.csv'))
                file_name = '{}/{}_{}/expression_data'.format(species_name, lit_id, project_id)
                gene_path = os.path.join(
                    settings.CELL_EXPRESSION_DIR,
                    "{file_name}/{gene_id}.csv".format(file_name=file_name, gene_id=gene_id))
                # expression_data = pd.read_csv(umap_path, usecols=['Cell_ID', 'UMAP_1', 'UMAP_2', 'Clusters', 'Cell_type'])
                expression_data = pd.read_csv(umap_path, usecols=['Cell_ID', 'UMAP_1', 'UMAP_2', 'Clusters', umap_type])
                # 通过cell_type组成的df
                cell_type_df = expression_data
                # umpa 数据返回所有的点
                if os.path.exists(gene_path):
                    gene_data = pd.read_csv(gene_path, usecols=['Cell_ID', 'value'])
                    expression_data = pd.merge(
                        expression_data, gene_data, how='left', on='Cell_ID').fillna(0)
                    expression_data['value'] = expression_data['value'].astype(
                        str).str[:4].astype(float)
                    cell_type_df = pd.merge(
                        cell_type_df, gene_data, how='left', on='Cell_ID').fillna(0)
                    cell_type_df['value'] = cell_type_df['value'].astype(
                        str).str[:4].astype(float)
                else:
                    expression_data['value'] = 0
                    cell_type_df['value'] = 0
                expression_data = expression_data.drop('Cell_ID', axis=1)
                cell_type_df = cell_type_df.drop('Cell_ID', axis=1)
                expression_data = expression_data.iloc[1:40000]
                cell_type_df = cell_type_df.iloc[1:40000]
                # expression_data['Clusters_Cell_type'] = expression_data['Clusters'].map(str) + ':' + expression_data['Cell_type'].map(str)
                expression_data['Clusters_Cell_type'] = expression_data['Clusters'].map(str) + ':' + expression_data[
                    umap_type].map(str)
                expression_data = expression_data.groupby(['Clusters_Cell_type'])
                data_list = []
                if lit_id != 'LT68':
                    for group_name, group_data in expression_data:
                        group_data = group_data[['UMAP_1', 'UMAP_2']]
                        data = {
                            'name': group_name.split(':')[1],
                            'data': group_data.to_dict('split').get('data', []),
                            'sort': int(group_name.split(':')[0])
                        }
                        data_list.append(data)
                    data_list = sorted(data_list, key=lambda x: x['sort'])
                else:
                    for group_name, group_data in expression_data:
                        group_data = group_data[['UMAP_1', 'UMAP_2']]
                        data = {
                            'name': group_name.split(':')[1],
                            'data': group_data.to_dict('split').get('data', []),
                            'sort': group_name.split(':')[1]
                        }
                        data_list.append(data)
                # 组合cell_type的df
                # cell_type_df = cell_type_df.groupby('Cell_type')
                cell_type_df = cell_type_df.groupby(umap_type)
                cell_type_data_list = []
                for group_name, group_data in cell_type_df:
                    group_data = group_data[['UMAP_1', 'UMAP_2', 'value']]
                    data = {
                        'name': str(group_name),
                        'data': group_data.to_dict('split').get('data', []),
                    }
                    cell_type_data_list.append(data)
                all_data_ = {
                    'clusters_data': data_list,
                    'cell_type_data': cell_type_data_list,
                }
        except Exception as e:
            print(e)
            all_data_ = []
        return JSONResponse(all_data_)


class TissueStructureViewSet(viewsets.ModelViewSet):
    """Tissue structure"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        # species = request.GET.get('species', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        if tissue == 'Root':
            data = all_tissue_structure_data
        else:
            data = all_tissue_Leaf_structure_data
        return JSONResponse(data=data)


class SpeciesEfpViewSet(viewsets.ModelViewSet):
    """Tissue structure"""
    queryset = EfpGeneExpress.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SpeciesEfpSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species = request.GET.get('species', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', '')
        gene_id = request.GET.get('gene_id')
        s_gene_id = gene_id
        data = {}
        if species == 'Arabidopsis_thaliana' and gene_id:
            if GeneInfo.objects.filter(Q(gene_symbol__icontains=gene_id) | Q(gene_id__icontains=gene_id)).exists():
                gene_id = GeneInfo.objects.filter(
                    Q(gene_symbol__icontains=gene_id) | Q(gene_id__icontains=gene_id)).first().gene_id
            else:
                gene_id = ''
        elif CellMarkerInfo.objects.filter(
                Q(gene_symbol__icontains=gene_id) | Q(gene_id__icontains=gene_id)).exists() and gene_id:
            gene_id = CellMarkerInfo.objects.filter(
                Q(gene_symbol__icontains=gene_id) | Q(gene_id__icontains=gene_id)).first().gene_id
        else:
            gene_id = ''
        if gene_id:
            # 根据物种名称映射文件
            umap_path = 'umap/{}/{}_class_color'.format(species, tissue)
            file_path = os.path.join(settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(umap_path))
            # 读取物种对应的文件
            file_name = '{}/{}/expression_data'.format(species, tissue)
            class_color_df = pd.read_csv(file_path, usecols=['Class_name', 'Cell_type'])
            # # 读取物种对应的文件
            gene_path = os.path.join(settings.ATLAS_HOT_PNG_DIR,
                                     "umap/{file_name}/{gene_id}.csv".format(file_name=file_name, gene_id=gene_id))
            tissue_name = 'umap/{}/'.format(species)
            species_file = os.path.join(settings.ATLAS_HOT_PNG_DIR,
                                        "{file_name}/{tissue}/umap_data.csv".format(file_name=tissue_name,
                                                                                    tissue=tissue))
            if os.path.exists(gene_path):
                umap_tsne_df = pd.read_csv(gene_path)
                gene_df = pd.read_csv(species_file)
                value_data = pd.merge(umap_tsne_df, gene_df, how='left', on='Cell_ID').fillna(0)
                value_data = value_data.groupby('Cell_type').value.mean()
                data2 = (value_data - value_data.min()) / (value_data.max() - value_data.min())
                expression_data = pd.merge(
                    class_color_df, data2, how='left', on='Cell_type').fillna(0)
                if tissue == 'Root':
                    # root Xylem是否有值
                    specified_index = 'Xylem'
                    is_index_present = specified_index in data2.index
                    # 判断是否存在该索引
                    if is_index_present:
                        Xylem_value = data2.loc['Xylem']
                    else:
                        Xylem_value = 0

                    Phloem_index = 'Phloem'
                    is_index_Phloem_index = Phloem_index in data2.index
                    if is_index_Phloem_index:
                        Phloem_value = data2.loc['Phloem']
                    else:
                        Phloem_value = 0
                    # 指定多列等于某一个值20230516
                    specified_values = ['Metaxylem', 'Protoxylem']
                    expression_data.loc[expression_data['Cell_type'].isin(specified_values), 'value'] = Xylem_value
                    Phloem_values = ['Protophloem', 'Metaphloem', 'Phloem sieve element', 'Phloem companion cell']
                    expression_data.loc[expression_data['Cell_type'].isin(Phloem_values), 'value'] = Phloem_value
                else:
                    # leaf Mesophyll是否有值
                    Mesophyll_index = 'Mesophyll'
                    is_index_Mesophyll_index_index = Mesophyll_index in data2.index
                    if is_index_Mesophyll_index_index:
                        Mesophyll_value = data2.loc['Mesophyll', 'value']
                    else:
                        Mesophyll_value = 0
                    Phloems_index = 'Phloem'
                    is_index_Phloems_index_index = Phloems_index in data2.index
                    if is_index_Phloems_index_index:
                        Phloem_value = data2.loc['Phloem', 'value']
                    else:
                        Phloem_value = 0
                    # value_data = pd.read_csv(gene_path, usecols=['Cell_type', 'value'])
                    value_data = value_data.groupby('Cell_type').mean()
                    data2 = (value_data - value_data.min()) / (value_data.max() - value_data.min())
                    expression_data = pd.merge(
                        class_color_df, data2, how='left', on='Cell_type').fillna(0)
                    # 指定多列等于某一个值20230516
                    specified_values = ['Palisade mesophyll', 'Spongy mesophyll']
                    expression_data.loc[
                        expression_data['Cell_type'].isin(specified_values), 'value'] = Mesophyll_value
                    Phloem_values = ['Protophloem', 'Metaphloem']
                    expression_data.loc[expression_data['Cell_type'].isin(Phloem_values), 'value'] = Phloem_value
                expression_data['value'] = expression_data['value'].astype(
                    str).str[:6].astype(float)
                expression_data = expression_data.drop('Cell_type', axis=1)
                df = expression_data.set_index("Class_name")
                # 将 DataFrame 转换为字典
                dict_data = df.to_dict()["value"]
                # 遍历字典并将其转换为所需格式
                result = {f"{k}": f"{color_value_new(v)}" for k, v in dict_data.items()}
            else:
                result = {}
        else:
            result = {}
        try:
            if s_gene_id:
                print(s_gene_id)
                svg = EfpSvgInfo.objects.filter(species_name=species,
                                                tissue="{tissue}_color".format(tissue=tissue)).first().svg
            else:
                svg = EfpSvgInfo.objects.filter(species_name=species, tissue=tissue).first().svg
        except Exception as e:
            print(e)
            svg = ''
        data["stage_plant"] = result
        data["stage_svg"] = svg
        return JSONResponse(data=data)


class ReferenceCellTypeListViewSet(viewsets.ModelViewSet):
    """ReferenceCellType列表页接口"""
    queryset = ReferenceCellTypeInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ReferenceCellTypeInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        tissue = self.request.GET.get('tissue')
        cell_type = self.request.GET.get('cell_type')
        types = self.request.GET.get('types')
        parent = self.request.GET.get('parent')
        try:
            query_list = []
            if tissue:
                query_list.append(Q(tissue__icontains=tissue))
            if cell_type:
                query_list.append(Q(cell_type__icontains=cell_type))
            if types:
                query_list.append(Q(type__icontains=types))
            if parent:
                query_list.append(Q(parent__icontains=parent))
        except Exception as e:
            query_list = []
        querysets = self.queryset.filter(*query_list)
        page = self.paginate_queryset(querysets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(query_list, many=True)
        return JSONResponse(serializer.data)


class ProjectStaticUmapPngtViewSet(viewsets.ModelViewSet):
    """Project static umap 静态图"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        lit_id = self.request.GET.get('lit_id')
        project_id = self.request.GET.get('project_id')
        try:
            data = {
                "project_static_umap_png": settings.PROJECT_STATIC_UMAP_PNG + '{}_{}.png'.format(lit_id, project_id)
            }
            # data = {
            #     "project_static_umap_png": settings.PROJECT_STATIC_UMAP_PNG + '{}.png'.format(lit_id)
            # }
        except Exception as e:
            data = {
                "project_static_umap_png": ''
            }
        return JSONResponse(data=data)


class AtlasStaticUmapPngtViewSet(viewsets.ModelViewSet):
    """Atlas static umap 静态图"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        type = request.GET.get('type', 'umap')  # 1:umap,2:tsne
        view_type = request.GET.get('view_type', 'Cell_type')  # 1:Cell_type 2:Clusters 3:Project_ID
        try:
            # data = {Arabidopsis_thaliana_Leaf_tsne_cell_type
            #     # umap静态图
            #     "project_static_umap_png": settings.PROJECT_STATIC_UMAP_PNG + species + '_' + tissue + '_static.png',
            #     # tsne静态图
            #     "project_static_tsne_png": settings.PROJECT_STATIC_UMAP_PNG + species + '_' + tissue + '_tsne.png'
            #
            # }
            data = {
                "project_static_umap_png": settings.PROJECT_STATIC_UMAP_PNG + species + '_' + tissue + '_' + type + '_' + view_type + '.png',

            }
        except Exception as e:
            data = {
                "project_static_umap_png": '',
            }
        return JSONResponse(data=data)


class MonocleExpressedGenesListViewSet(viewsets.ModelViewSet):
    """Monocle differential_expressed_genes"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = self.request.GET.get('tissue')
        cell_type = self.request.GET.get('cell_type')
        page = self.request.GET.get('page', '1')
        page_size = self.request.GET.get('page_size', '10')
        try:
            file_path = os.path.join(settings.MONOCLE_FILE,
                                     "{}_{}_{}_{}".format(species, tissue, cell_type, 'Expresse.csv'))
            # 本地测试
            # file_path = 'D:\plant_marker_backend\excel\Arabidopsis_thaliana_Root_Columella_Expresse.csv'
            map_data = pd.read_csv(
                file_path, usecols=['status', 'family', 'pval', 'qval', 'gene_short_name', 'num_cells_expressed'])
            map_data['gene_id'] = map_data['gene_short_name']
            # 2023-06-27新增别名
            # 获取所有需要查询的基因短名称列表
            gene_short_names = map_data['gene_short_name'].tolist()
            # 构造查询条件
            query = Q(gene_id__in=gene_short_names)
            # 批量查询数据库
            if species == 'Arabidopsis_thaliana':
                gene_info = GeneInfo.objects.filter(query).values('gene_id', 'gene_symbol')
            else:
                gene_info = CellMarkerInfo.objects.filter(query).values('gene_id', 'gene_symbol')
            # 创建字典以便映射查询结果
            gene_dict = {entry['gene_id']: entry['gene_symbol'] for entry in gene_info}
            # 使用映射字典替换 gene_short_name 列的值
            map_data['gene_short_name'] = map_data['gene_short_name'].map(gene_dict).fillna(map_data['gene_short_name'])
            count = len(map_data)
            # 进行分页操作
            page = int(page)
            page_size = int(page_size)
            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            map_data = map_data.iloc[start_index:end_index].to_dict(orient='records')
            # 列表分页
            # all_data_ = map_data[(int(page) - 1) * int(page_size): (int(page) - 1) * int(page_size) + int(page_size)]
            # map_data = eval(all_data_.to_json(orient="records"))
            data = {
                'code': 200,
                'msg': "OK",
                'data': map_data,
                'count': count
            }
        except Exception as e:
            print(e)
            data = {
                'code': 200,
                'msg': "OK",
                'data': '',
                'count': ''
            }
        return JSONResponse(data)


class MonocleHeatMapGenesListViewSet(viewsets.ModelViewSet):
    """Monocle Heatmap_genes"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = self.request.GET.get('tissue')
        cell_type = self.request.GET.get('cell_type')
        page = self.request.GET.get('page', '1')
        page_size = self.request.GET.get('page_size', '10')
        try:
            file_path = os.path.join(settings.MONOCLE_FILE,
                                     "{}_{}_{}_{}".format(species, tissue, cell_type, 'Time.csv'))
            # 本地测试
            # file_path = 'D:\plant_marker_backend\excel\Arabidopsis_thaliana_Root_Atrichoblast_Time.csv'
            map_data = pd.read_csv(
                file_path, usecols=['status', 'family', 'pval', 'qval', 'gene_short_name', 'num_cells_expressed',
                                    'use_for_ordering'])
            map_data['gene_id'] = map_data['gene_short_name']
            # 2023-06-27新增别名
            # 获取所有需要查询的基因短名称列表
            gene_short_names = map_data['gene_short_name'].tolist()
            # 构造查询条件
            query = Q(gene_id__in=gene_short_names)
            # 批量查询数据库
            if species == 'Arabidopsis_thaliana':
                gene_info = GeneInfo.objects.filter(query).values('gene_id', 'gene_symbol')
            else:
                gene_info = CellMarkerInfo.objects.filter(query).values('gene_id', 'gene_symbol')
            # 创建字典以便映射查询结果
            gene_dict = {entry['gene_id']: entry['gene_symbol'] for entry in gene_info}
            # 使用映射字典替换 gene_short_name 列的值
            map_data['gene_short_name'] = map_data['gene_short_name'].map(gene_dict).fillna(map_data['gene_short_name'])
            # # 将use_for_ordering这一列的bool转换成str
            map_data['use_for_ordering'] = map_data['use_for_ordering'].astype('str')
            count = len(map_data)
            # 优化分页操作
            page = int(page)
            page_size = int(page_size)
            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            map_data = map_data.iloc[start_index:end_index].to_dict(orient='records')
            # 列表分页
            # all_data_ = map_data[(int(page) - 1) * int(page_size): (int(page) - 1) * int(page_size) + int(page_size)]
            # # 将use_for_ordering这一列的bool转换成str
            # map_data['use_for_ordering'] = map_data['use_for_ordering'].astype('str')
            # map_data = eval(all_data_.to_json(orient="records"))
            data = {
                'code': 200,
                'msg': "OK",
                'data': map_data,
                'count': count
            }
        except Exception as e:
            print(e)
            data = {
                'code': 200,
                'msg': "OK",
                'data': '',
                'count': ''
            }
        return JSONResponse(data)


class MonocleExpressedGenesPngViewSet(viewsets.ModelViewSet):
    """MonocleExpressedGenes png图片生成接口"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name')
        tissue = self.request.GET.get('tissue')
        cell_type = self.request.GET.get('cell_type')
        gene = self.request.GET.get('gene')
        type = self.request.GET.get('type')
        try:
            str_uuid = str(uuid.uuid4())
            f = os.popen(
                f'Rscript /data/Monocle/Monocle_expression.R  -r {species_name}_{tissue}_{cell_type}.rds -g  {gene} -u {str_uuid} -c {type}'.format(
                    species_name=species_name, tissue=tissue, cell_type=cell_type, gene=gene, str_uuid=str_uuid,
                    type=type))
            f.read()
            pdf_file = settings.MONOCLE_EXPRESSION_FILE + '{str_uuid}.pdf'.format(str_uuid=str_uuid)
            doc = fitz.open(pdf_file)
            page = doc.load_page(0)  # 要加载的页码
            pix = page.get_pixmap()
            # 保存图片
            pix.save(settings.MONOCLE_EXPRESSION_FILE + '/' + '{str_uuid}.png'.format(str_uuid=str_uuid))
            data = {
                "expression_png": settings.BASE_URL + 'Expression/' + str_uuid + '.png'
            }
        except Exception as e:
            print(e)
            data = {
                "expression_png": '',
            }
        return JSONResponse(data=data)


class MonocleHeatMapGenesPngViewSet(viewsets.ModelViewSet):
    """HeatMapGenesPng  png图片生成接口"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name')
        tissue = self.request.GET.get('tissue')
        cell_type = self.request.GET.get('cell_type')
        gene = self.request.GET.get('gene')
        try:
            str_uuid = str(uuid.uuid4())
            print(str_uuid)
            f = os.popen(
                f'Rscript /data/Monocle/Monocle_heatmap.R  -r {species_name}_{tissue}_{cell_type}.rds -g  {gene} -u {str_uuid}'.format(
                    species_name=species_name, tissue=tissue, cell_type=cell_type, gene=gene, str_uuid=str_uuid))
            # print(f)
            f.read()
            pdf_file = settings.MONOCLE_HEATMAP_FILE + '{str_uuid}.pdf'.format(str_uuid=str_uuid)
            doc = fitz.open(pdf_file)
            page = doc.load_page(0)  # 要加载的页码
            pix = page.get_pixmap()
            # 保存图片
            pix.save(settings.MONOCLE_HEATMAP_FILE + '{str_uuid}.png'.format(str_uuid=str_uuid))
            data = {
                "heatmap_png": settings.BASE_URL + 'Heatmap/' + str_uuid + '.png'
            }
        except Exception as e:
            print(e)
            data = {
                "heatmap_png": '',
            }
        return JSONResponse(data=data)


class MonocleExpressedGenesDownViewSet(viewsets.ModelViewSet):
    """Monocle differential_expressed_genes 基因下拉框"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = self.request.GET.get('tissue')
        cell_type = self.request.GET.get('cell_type')
        page = self.request.GET.get('page', '1')
        page_size = self.request.GET.get('page_size', '20')
        try:
            file_path = os.path.join(
                settings.MONOCLE_FILE,
                "{}_{}_{}_{}".format(species, tissue, cell_type, 'Expresse.csv'))
            map_data = pd.read_csv(
                file_path, usecols=['gene_short_name'])
            count = len(map_data)
            # 列表分页
            all_data_ = map_data[(int(page) - 1) * int(page_size): (int(page) - 1) * int(page_size) + int(page_size)]

            map_data = eval(all_data_.to_json(orient="records"))
            data = {
                'code': 200,
                'msg': "OK",
                'data': map_data,
            }
        except Exception as e:
            print(e)
            data = {
                'code': 200,
                'msg': "OK",
                'data': '',
            }
        return JSONResponse(data)


class MonocleHeatMapGenesDownViewSet(viewsets.ModelViewSet):
    """Monocle heatmap_genes 基因下拉框"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = self.request.GET.get('tissue')
        cell_type = self.request.GET.get('cell_type')
        page = self.request.GET.get('page', '1')
        page_size = self.request.GET.get('page_size', '20')
        try:
            file_path = os.path.join(
                settings.MONOCLE_FILE,
                "{}_{}_{}_{}".format(species, tissue, cell_type, 'Time.csv'))
            map_data = pd.read_csv(
                file_path, usecols=['gene_short_name'])
            count = len(map_data)
            # 列表分页
            all_data_ = map_data[(int(page) - 1) * int(page_size): (int(page) - 1) * int(page_size) + int(page_size)]

            map_data = eval(all_data_.to_json(orient="records"))
            data = {
                'code': 200,
                'msg': "OK",
                'data': map_data,
            }
        except Exception as e:
            print(e)
            data = {
                'code': 200,
                'msg': "OK",
                'data': '',
            }
        return JSONResponse(data)


class SpeciesDownViewSet(viewsets.ModelViewSet):
    """下拉框"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        specie_data = [{

            "label": "Arabidopsis thaliana",
            "value": "Arabidopsis_thaliana"
        },
            {
                "label": "Oryza sativa",
                "value": "Oryza_sativa"
            },
            {
                "label": "Zea mays",
                "value": "Zea_mays"
            }
        ]
        data = {
            'code': 200,
            'msg': "OK",
            'data': specie_data,
        }
        return JSONResponse(data)


class SpeciesTissueDownViewSet(viewsets.ModelViewSet):
    """下拉框"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species = request.GET.get('species_name', 'Arabidopsis_thaliana')
        data = [{'label': "Root", 'value': 'Root'}]
        data = {
            'code': 200,
            'msg': "OK",
            'data': data,
        }
        return JSONResponse(data)


class SpeciesCellTypeDownViewSet(viewsets.ModelViewSet):
    """下拉框"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        if species == 'Arabidopsis_thaliana':
            data = [
                {'label': "Atrichoblast", 'value': 'Atrichoblast'},
                {'label': " Columella", 'value': 'Columella'},
                {'label': "Cortex", 'value': 'Cortex'},
                {'label': "Epidermis", 'value': 'Epidermis'},
                {'label': "Lateralrootcap", 'value': 'Lateralrootcap'},
                {'label': "Pericycle", 'value': 'Pericycle'},
                {'label': " Phloem", 'value': 'Phloem'},
                {'label': " Root Endodermis", 'value': 'Root_Endodermis'},
                {'label': " Root Trichoblast", 'value': 'Trichoblast'},
            ]
        elif species == 'Oryza_sativa':
            data = [
                {'label': "Cortex", 'value': 'Cortex'},
                {'label': "Epidermis", 'value': 'Epidermis'},
                {'label': "Stele", 'value': 'Stele'},
            ]
        else:
            data = [
                {'label': "Epidermis", 'value': 'Epidermis'},
                {'label': "RootEndodermis", 'value': 'RootEndodermis'},
                {'label': "Stele", 'value': 'Stele'}
            ]
        data = {
            'code': 200,
            'msg': "OK",
            'data': data,
        }

        return JSONResponse(data)


class MonocleHeatPngViewSet(viewsets.ModelViewSet):
    """MonocleExpressedGenes png图片生成接口"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name')
        tissue = self.request.GET.get('tissue')
        cell_type = self.request.GET.get('cell_type', '')
        type = self.request.GET.get('type')
        try:
            str_uuid = str(uuid.uuid4())
            pdf_file = settings.MONOCLE_FILE + 'Monocle_pdf/' + '{}_{}_{}_{}.pdf'.format(species_name, tissue,
                                                                                         cell_type, type)
            doc = fitz.open(pdf_file)
            page = doc.load_page(0)  # 要加载的页码
            pix = page.get_pixmap()
            # 保存图片 直接存到MONOCLE_EXPRESSION_FILE的文件夹就行
            pix.save('/data/source_material/monocle_expression_png/' + '{str_uuid}.png'.format(str_uuid=str_uuid))
            data = {
                "monocle_heat_png": settings.BASE_URL + 'source_material/monocle_expression_png/' + str_uuid + '.png'
            }
        except Exception as e:
            print(e)
            data = {
                "monocle_heat_png": '',
            }
        return JSONResponse(data=data)


class AtlasDownloadListViewSet(viewsets.ModelViewSet):
    queryset = AtlasDownload.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AtlasDownloadListSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name_value = self.request.GET.get('species_name_value')
        tissue = self.request.GET.get('tissue')
        try:
            query_list = []
            if species_name_value:
                query_list.append(Q(species_name__icontains=species_name_value))
            if tissue:
                query_list.append(Q(atlas_name__icontains=tissue))

        except Exception as e:
            query_list = []
        querysets = self.queryset.filter(*query_list)
        page = self.paginate_queryset(querysets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class CellMarkerDownloadListViewSet(viewsets.ModelViewSet):
    queryset = CellMarkerDownload.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CellMarkerDownloadListSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name_value = self.request.GET.get('species_name_value')
        tissue = self.request.GET.get('tissue')
        try:
            query_list = []
            if species_name_value:
                query_list.append(Q(species_name__icontains=species_name_value))
            if tissue:
                query_list.append(Q(tissue__icontains=tissue))

        except Exception as e:
            query_list = []
        querysets = self.queryset.filter(*query_list)
        page = self.paginate_queryset(querysets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class CellClusterDownloadListViewSet(viewsets.ModelViewSet):
    queryset = ClusterMarkerDownload.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ClusterMarkerDownloadListSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name_value = self.request.GET.get('species_name_value')
        tissue = self.request.GET.get('tissue')
        try:
            query_list = []
            if species_name_value:
                query_list.append(Q(species_name__icontains=species_name_value))
            if tissue:
                query_list.append(Q(tissue=tissue))
        except Exception as e:
            query_list = []
        querysets = self.queryset.filter(*query_list)
        page = self.paginate_queryset(querysets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class AtlasDownloadViewSet(viewsets.ModelViewSet):
    queryset = AtlasDownload.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AtlasDownloadListSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name_value = self.request.GET.get('species_name_value', 'Arabidopsis_thaliana')
        atlas_type = self.request.GET.get('atlas_type', 'WholePlant')
        atlas_name_value = self.request.GET.get('atlas_name_value', 'WholePlant')
        download_type = self.request.GET.get('download_type', 'GE_Matrix')
        try:
            if download_type != 'RDS':
                if atlas_type != "Project":
                    download_type = download_type.replace('_', '')
                    download_url = settings.PROJECT_ATLAS_DOWNLOAD_URL + species_name_value + '_' + atlas_name_value + '_{}.txt'.format(
                        download_type)
                else:
                    download_type = download_type.replace('_', '')
                    download_url = settings.PROJECT_ATLAS_DOWNLOAD_URL + atlas_name_value + '_{}.txt'.format(
                        download_type)
            else:
                if atlas_type != "Project":
                    download_url = settings.PROJECT_ATLAS_DOWNLOAD_RDS_URL + species_name_value + '_' + atlas_name_value + '.rds'
                else:
                    download_url = settings.PROJECT_ATLAS_DOWNLOAD_RDS_URL + atlas_name_value + '.rds'
            data = {
                "atlas_download": download_url,
            }
        except Exception as e:
            data = {
                "atlas_download": '',
            }
        return JSONResponse(data=data)


class CellMarkerDownloadViewSet(viewsets.ModelViewSet):
    queryset = AtlasDownload.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AtlasDownloadListSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name_value = self.request.GET.get('species_name_value', 'Arabidopsis_thaliana')
        tissue = self.request.GET.get('tissue', 'Root')
        try:
            download_url = settings.CELL_MARKER_DOWNLOAD_URL + species_name_value + '_' + tissue + '.csv'
            data = {
                "atlas_download": download_url,
            }
        except Exception as e:
            data = {
                "atlas_download": '',
            }
        return JSONResponse(data=data)


class CellClusterDownloadViewSet(viewsets.ModelViewSet):
    queryset = AtlasDownload.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AtlasDownloadListSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name_value = self.request.GET.get('species_name_value', 'Arabidopsis_thaliana')
        tissue = self.request.GET.get('tissue', 'Root')
        try:
            download_url = settings.CELL_CLUSTER_DOWNLOAD_URL + species_name_value + '_' + tissue + '.csv'
            data = {
                "atlas_download": download_url,
            }
        except Exception as e:
            data = {
                "atlas_download": '',
            }
        return JSONResponse(data=data)


class AtalsSpeciesDownViewSet(viewsets.ModelViewSet):
    """下拉框"""
    queryset = AtlasDownload.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_queryset = self.queryset.values_list('species_name', flat=True)
        data = [{'label': str(x).replace('_', ' '), "name": x} for x in list(set(species_queryset))]
        return JSONResponse(data)


class AtalsnameDownViewSet(viewsets.ModelViewSet):
    """下拉框"""
    queryset = AtlasDownload.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name_value = self.request.GET.get('species_name_value', 'Arabidopsis_thaliana')
        atlas_name_queryset = self.queryset.filter(species_name__icontains=species_name_value).values_list('atlas_name',
                                                                                                           flat=True)
        data = [{'label': str(x).split("_")[1], "name": x} if str(x).startswith('LT') else {'label': x, "name": x}
                for x in list(set(atlas_name_queryset))]
        return JSONResponse(data)


class CellSpecieDownViewSet(viewsets.ModelViewSet):
    """下拉框"""
    queryset = CellMarkerDownload.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_queryset = self.queryset.values_list('species_name', flat=True)
        data = [{'label': str(x).replace('_', ' '), "name": x} for x in list(set(species_queryset))]
        return JSONResponse(data)


class ClusterMarkerDownViewSet(viewsets.ModelViewSet):
    """下拉框"""
    queryset = ClusterMarkerDownload.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_queryset = self.queryset.values_list('species_name', flat=True)
        data = [{'label': str(x).replace('_', ' '), "name": x} for x in list(set(species_queryset))]
        return JSONResponse(data)


class CellTissueDownViewSet(viewsets.ModelViewSet):
    """下拉框"""
    queryset = CellMarkerDownload.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name_value = self.request.GET.get('species_name_value', 'Arabidopsis_thaliana')
        atlas_name_queryset = self.queryset.filter(species_name__icontains=species_name_value).values_list('tissue',
                                                                                                           flat=True)
        data = [{'label': str(x).replace('_', ' '), "name": x} for x in list(set(atlas_name_queryset))]
        return JSONResponse(data)


class ClusterMarkerTissueDownViewSet(viewsets.ModelViewSet):
    """下拉框"""
    queryset = ClusterMarkerDownload.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name_value = self.request.GET.get('species_name_value', 'Arabidopsis_thaliana')
        atlas_name_queryset = self.queryset.filter(species_name__icontains=species_name_value).values_list('tissue',
                                                                                                           flat=True)
        data = [{'label': str(x).replace('_', ' '), "name": x} for x in list(set(atlas_name_queryset))]
        return JSONResponse(data)


class CrossSpecieExpressionViewSet(viewsets.ModelViewSet):
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """
        物种umap接口
        """
        tissue = request.GET.get('tissue', 'Root')
        try:
            species_name = 'Arabidopsis_thaliana'
            secsend_specie = 'Oryza_sativa'
            third_specie = 'Zea_mays'
            # 根据物种名称映射文件
            file_name = 'umap/{}/{}/umap_data'.format(species_name, tissue)
            # 读取物种对应的文件
            file_path = os.path.join(
                settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(file_name))
            # 1：Sample_ID;2:Clusters;3:Project_ID 筛选相应的列
            umap_data = pd.read_csv(file_path, usecols=['UMAP_1', 'UMAP_2', 'Clusters',
                                                        'Cell_type'])
            umap_data = umap_data.iloc[1:15000]
            # 通过cell_type组成的df
            cell_type_df = umap_data
            # 将Clusters和Cell_type进行拼接聚合
            umap_data['Clusters_Cell_type'] = umap_data['Clusters'].map(str) + ':' + umap_data['Cell_type'].map(
                str)
            # 组合cell_type的df
            cell_type_df = cell_type_df.groupby('Cell_type')
            cell_type_data_list = []
            for group_name, group_data in cell_type_df:
                group_data = group_data[['UMAP_1', 'UMAP_2']]
                data = {
                    'specie': species_name,
                    'name': str(group_name),
                    'data': group_data.to_dict('split').get('data', [])[1:15000],
                }
                cell_type_data_list.append(data)
            #########################目标物种的umap图数据
            if secsend_specie:
                reference_file_name = 'umap/{}/{}/umap_data'.format(secsend_specie, tissue)
                # 读取物种对应的文件
                reference_file_path = os.path.join(
                    settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(reference_file_name))
                reference_umap_data = pd.read_csv(reference_file_path, usecols=['UMAP_1', 'UMAP_2', 'Clusters',
                                                                                'Cell_type'])
                reference_umap_data = reference_umap_data.iloc[1:15000]
                # 通过cell_type组成的df
                reference_umap_data_df = reference_umap_data
                reference_umap_data['Clusters_Cell_type'] = reference_umap_data['Clusters'].map(str) + ':' + \
                                                            reference_umap_data['Cell_type'].map(
                                                                str)
                reference_umap_data_df = reference_umap_data_df.groupby('Cell_type')
                reference_umap_data_df_list = []
                for group_name, group_data in reference_umap_data_df:
                    group_data = group_data[['UMAP_1', 'UMAP_2']]
                    data = {
                        'specie': secsend_specie,
                        'name': str(group_name),
                        'data': group_data.to_dict('split').get('data', [])[1:15000],
                    }
                    reference_umap_data_df_list.append(data)
            else:
                reference_umap_data_df_list = []
            ###################第三个物种的umap
            if third_specie:
                third_specie_file_name = 'umap/{}/{}/umap_data'.format(third_specie, tissue)
                # 读取物种对应的文件
                third_specie_file_path = os.path.join(
                    settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(third_specie_file_name))
                third_umap_data = pd.read_csv(third_specie_file_path, usecols=['UMAP_1', 'UMAP_2', 'Clusters',
                                                                               'Cell_type'])
                third_umap_data = third_umap_data.iloc[1:15000]
                # 通过cell_type组成的df
                third_umap_data_df = third_umap_data
                third_umap_data['Clusters_Cell_type'] = third_umap_data['Clusters'].map(str) + ':' + \
                                                        third_umap_data['Cell_type'].map(
                                                            str)
                third_umap_data_df = third_umap_data_df.groupby('Cell_type')
                third_umap_data_df_list = []
                for group_name, group_data in third_umap_data_df:
                    group_data = group_data[['UMAP_1', 'UMAP_2']]
                    data = {
                        'specie': third_specie,
                        'name': str(group_name),
                        'data': group_data.to_dict('split').get('data', [])[1:15000],
                    }
                    third_umap_data_df_list.append(data)
            else:
                third_umap_data_df_list = []
            all_data_ = {
                'specice_umap_data': cell_type_data_list,
                'secsend_specie_umap_data': reference_umap_data_df_list,
                'third_specie_umap_data': third_umap_data_df_list,
            }
        except Exception as e:
            print(e)
            all_data_ = []
        return JSONResponse(all_data_)


class CrossSpecieGeneExpressionViewSet(viewsets.ModelViewSet):
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name', '')
        tissue = request.GET.get('tissue', '')
        gene_id = request.GET.get('gene_id', '')
        try:
            # 2023-06-06新增基因别名
            # if species_name == 'Arabidopsis_thaliana':
            #     if GeneInfo.objects.filter(Q(gene_symbol__icontains=gene_id) | Q(gene_id__icontains=gene_id)).exists():
            #         gene_id = GeneInfo.objects.filter(
            #             Q(gene_symbol__icontains=gene_id) | Q(gene_id__icontains=gene_id)).first().gene_id
            #     else:
            #         gene_id = gene_id
            # elif CellMarkerInfo.objects.filter(
            #         Q(gene_symbol__icontains=gene_id) | Q(gene_id__icontains=gene_id)).exists():
            #     gene_id = CellMarkerInfo.objects.filter(
            #         Q(gene_symbol__icontains=gene_id) | Q(gene_id__icontains=gene_id)).first().gene_id
            # else:
            #     gene_id = gene_id
            specie_list = ['Arabidopsis_thaliana', 'Oryza_sativa', 'Zea_mays']
            # species_all = self.queryset.filter(specie_name=species_name, specie_gene=gene_id).values_list(
            #     'reference_name', 'reference_gene')
            species_querysets = self.queryset.filter(specie_name=species_name, specie_gene=gene_id)
            # 如果输入的ID只在拟南芥里面找到（在水稻和玉米里面没找到），那就用这个找到的拟南芥ID再去水稻和玉米里面找一下
            if species_querysets.count() == 1 and species_querysets.first().reference_name == 'Arabidopsis_thaliana':
                _reference_gene = species_querysets.first().reference_gene
                _species_all = self.queryset.filter(specie_gene=_reference_gene)
                species_querysets = species_querysets.union(_species_all)
                species_querysets = species_querysets.distinct()
            species_all = species_querysets.values_list('reference_name', 'reference_gene')
            # 按照第一个元素的首字母进行排序
            sorted_list = sorted(species_all, key=lambda x: x[0][0])
            new_gene_list = [(species, [x[1] for x in sorted_list if x[0] == species][0] if species in [x[0] for x in
                                                                                                        sorted_list] else '')
                             for species in specie_list]

            sorted_list_new = sorted(new_gene_list, key=lambda x: x[0][0])
            # # 列表推导式提取所有元组的第一个元素和第二个元素
            first_element = [t[0] for t in sorted_list_new]
            second_element = [t[1] for t in sorted_list_new]
            species_name = first_element[0]
            gene_id = second_element[0]
            reference_name = first_element[1]
            reference_gene = second_element[1]
            third_specie = first_element[2]
            third_gene = second_element[2]

            # 根据物种名称映射文件
            umap_path = 'umap/{}/{}/umap_data'.format(species_name, tissue)
            file_path = os.path.join(settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(umap_path))
            # 读取物种对应的文件
            file_name = '{}/{}/expression_data'.format(species_name, tissue)
            # # 读取物种对应的文件
            gene_path = os.path.join(settings.ATLAS_HOT_PNG_DIR,
                                     "umap/{file_name}/{gene_id}.csv".format(file_name=file_name, gene_id=gene_id))
            # 1：Sample_ID;2:Clusters;3:Project_ID 筛选相应的列
            expression_data = pd.read_csv(file_path, usecols=['Cell_ID', 'UMAP_1', 'UMAP_2', 'Clusters', 'Cell_type'])
            # 组合cell_type的df
            cell_type_df = expression_data
            if os.path.exists(gene_path):
                gene_data = pd.read_csv(gene_path, usecols=['Cell_ID', 'value'])
                expression_data = pd.merge(
                    expression_data, gene_data, how='left', on='Cell_ID').fillna(0)
                expression_data['value'] = expression_data['value'].astype(
                    str).str[:4].astype(float)
                cell_type_df = pd.merge(
                    cell_type_df, gene_data, how='left', on='Cell_ID').fillna(0)
                cell_type_df['value'] = cell_type_df['value'].astype(
                    str).str[:4].astype(float)
            else:
                expression_data['value'] = 0
                cell_type_df['value'] = 0
            expression_data = expression_data.drop('Cell_ID', axis=1)
            expression_data = expression_data.iloc[1:15000]
            expression_data['Clusters_Cell_type'] = expression_data['Clusters'].map(str) + ':' + expression_data[
                'Cell_type'].map(str)
            expression_data = expression_data.groupby(['Clusters_Cell_type'])
            data_list = []
            for group_name, group_data in expression_data:
                group_data = group_data[['UMAP_1', 'UMAP_2', 'value']]
                group_name = group_name[0]
                data = {
                    'specie': species_name,
                    'name': group_name.split(":")[1],
                    'data': group_data.to_dict('split').get('data', []),
                    'sort': int(group_name.split(":")[0]) if tissue != 'WholePlant' else group_name.split(":")[0]
                }
                data_list.append(data)
            data_list = sorted(data_list, key=lambda x: x['sort'])
            ################第二个目标物种基因的umap
            if reference_name:
                reference_umap_path = 'umap/{}/{}/umap_data'.format(reference_name, tissue)
                reference_file_path = os.path.join(settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(reference_umap_path))
                # 读取物种对应的文件
                reference_file_name = '{}/{}/expression_data'.format(reference_name, tissue)
                # # 读取物种对应的文件
                reference_gene_path = os.path.join(settings.ATLAS_HOT_PNG_DIR,
                                                   "umap/{file_name}/{gene_id}.csv".format(
                                                       file_name=reference_file_name,
                                                       gene_id=reference_gene))
                reference_expression_data = pd.read_csv(reference_file_path,
                                                        usecols=['Cell_ID', 'UMAP_1', 'UMAP_2', 'Clusters',
                                                                 'Cell_type'])
                # 组合reference_df的df
                reference_df = reference_expression_data
                if os.path.exists(reference_gene_path):
                    reference_gene_data = pd.read_csv(reference_gene_path, usecols=['Cell_ID', 'value'])
                    reference_expression_data = pd.merge(
                        reference_expression_data, reference_gene_data, how='left', on='Cell_ID').fillna(0)
                    reference_expression_data['value'] = reference_expression_data['value'].astype(
                        str).str[:4].astype(float)
                    reference_df = pd.merge(
                        reference_df, reference_gene_data, how='left', on='Cell_ID').fillna(0)
                    reference_df['value'] = reference_df['value'].astype(
                        str).str[:4].astype(float)
                else:
                    reference_expression_data['value'] = 0
                    reference_df['value'] = 0
                reference_expression_data = reference_expression_data.drop('Cell_ID', axis=1)
                reference_expression_data = reference_expression_data.iloc[1:15000]
                reference_expression_data['Clusters_Cell_type'] = reference_expression_data['Clusters'].map(str) + ':' + \
                                                                  reference_expression_data[
                                                                      'Cell_type'].map(str)
                reference_expression_data = reference_expression_data.groupby(['Clusters_Cell_type'])
                reference_expression_data_list = []
                for group_name, group_data in reference_expression_data:
                    group_data = group_data[['UMAP_1', 'UMAP_2', 'value']]
                    group_name = group_name[0]
                    data = {
                        'specie': reference_name,
                        'name': group_name.split(":")[1],
                        'data': group_data.to_dict('split').get('data', []),
                        'sort': int(group_name.split(":")[0]) if tissue != 'WholePlant' else group_name.split(":")[0]
                    }
                    reference_expression_data_list.append(data)
                reference_expression_data_list = sorted(reference_expression_data_list, key=lambda x: x['sort'])
            else:
                reference_expression_data_list = []
            ################第三个目标物种基因的umap
            if third_specie:
                third_specie_umap_path = 'umap/{}/{}/umap_data'.format(third_specie, tissue)
                third_specie_file_path = os.path.join(settings.ATLAS_HOT_PNG_DIR,
                                                      "{}.csv".format(third_specie_umap_path))
                # 读取物种对应的文件
                third_specie_file_name = '{}/{}/expression_data'.format(third_specie, tissue)
                # # 读取物种对应的文件
                third_specie_reference_gene_path = os.path.join(settings.ATLAS_HOT_PNG_DIR,
                                                                "umap/{file_name}/{gene_id}.csv".format(
                                                                    file_name=third_specie_file_name,
                                                                    gene_id=third_gene))
                third_specie_expression_data = pd.read_csv(third_specie_file_path,
                                                           usecols=['Cell_ID', 'UMAP_1', 'UMAP_2', 'Clusters',
                                                                    'Cell_type'])
                # 组合reference_df的df
                third_specie_df = third_specie_expression_data
                if os.path.exists(third_specie_reference_gene_path):
                    third_specie_df_data = pd.read_csv(third_specie_reference_gene_path, usecols=['Cell_ID', 'value'])
                    third_specie_expression_data = pd.merge(
                        third_specie_expression_data, third_specie_df_data, how='left', on='Cell_ID').fillna(0)
                    third_specie_expression_data['value'] = third_specie_expression_data['value'].astype(
                        str).str[:4].astype(float)
                    third_specie_df = pd.merge(
                        third_specie_df, third_specie_df_data, how='left', on='Cell_ID').fillna(0)
                    third_specie_df['value'] = third_specie_df['value'].astype(
                        str).str[:4].astype(float)
                else:
                    third_specie_expression_data['value'] = 0
                    third_specie_df['value'] = 0
                third_specie_expression_data = third_specie_expression_data.drop('Cell_ID', axis=1)
                third_specie_expression_data = third_specie_expression_data.iloc[1:15000]
                third_specie_expression_data['Clusters_Cell_type'] = third_specie_expression_data['Clusters'].map(
                    str) + ':' + \
                                                                     third_specie_expression_data[
                                                                         'Cell_type'].map(str)
                third_specie_expression_data = third_specie_expression_data.groupby(['Clusters_Cell_type'])
                third_specie_expression_data_list = []
                for group_name, group_data in third_specie_expression_data:
                    group_data = group_data[['UMAP_1', 'UMAP_2', 'value']]
                    group_name = group_name[0]
                    data = {
                        'specie': third_specie,
                        'name': group_name.split(":")[1],
                        'data': group_data.to_dict('split').get('data', []),
                        'sort': int(group_name.split(":")[0]) if tissue != 'WholePlant' else group_name.split(":")[0]
                    }
                    third_specie_expression_data_list.append(data)
                third_specie_expression_data_list = sorted(third_specie_expression_data_list, key=lambda x: x['sort'])
            else:
                third_specie_expression_data_list = []
            all_data_ = {
                'species_gene_data': data_list,
                'reference_data_list': reference_expression_data_list,
                'third_data_list': third_specie_expression_data_list,
            }
        except Exception as e:
            print(e)
            all_data_ = []
        return JSONResponse(all_data_)


class CrossSpecieViolinBoxPlotViewSet(viewsets.ModelViewSet):
    """手风琴和箱图接口"""
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        gene_id = request.GET.get('gene_id', 'AT1G50920')
        try:
            specie_list = ['Arabidopsis_thaliana', 'Oryza_sativa', 'Zea_mays']
            species_all = self.queryset.filter(specie_name=species_name, specie_gene=gene_id).values_list(
                'reference_name', 'reference_gene')
            # # 按照第一个元素的首字母进行排序
            sorted_list = sorted(species_all, key=lambda x: x[0][0])
            new_gene_list = [(species, [x[1] for x in sorted_list if x[0] == species][0] if species in [x[0] for x in
                                                                                                        sorted_list] else '')
                             for species in specie_list]

            sorted_list_new = sorted(new_gene_list, key=lambda x: x[0][0])
            # # 列表推导式提取所有元组的第一个元素和第二个元素
            first_element = [t[0] for t in sorted_list_new]
            second_element = [t[1] for t in sorted_list_new]
            species_name = first_element[0]
            gene_id = second_element[0]
            reference_name = first_element[1]
            reference_gene = second_element[1]
            third_specie = first_element[2]
            third_gene = second_element[2]
            # 返回绘制的手风琴和箱图
            # print(species_name, tissue, gene_id)
            species_violinplot_png, boxplot_png = draw_atlas_cell_violinplot_new(species_name, tissue, gene_id)
            reference_violinplot_png, boxplot_png = draw_atlas_cell_violinplot_new(reference_name, tissue,
                                                                                   reference_gene)
            third_specie_violinplot_png, boxplot_png = draw_atlas_cell_violinplot_new(third_specie, tissue, third_gene)
            data = {
                "species_violinplot_png": settings.BASE_URL + 'violinplot_png/' + species_violinplot_png if species_violinplot_png else '',
                # 手风琴
                "reference_violinplot_png": settings.BASE_URL + 'violinplot_png/' + reference_violinplot_png if reference_violinplot_png else '',
                "third_specie_violinplot_png": settings.BASE_URL + 'violinplot_png/' + third_specie_violinplot_png if third_specie_violinplot_png else '',
                # 手风琴
            }
        except Exception as e:
            print(e)
            data = {
                "species_violinplot_png": '',
                "reference_violinplot_png": '',
                "third_specie_violinplot_png": '',
            }
        return JSONResponse(data=data)


class CrossSpecieNameDownViewSet(viewsets.ModelViewSet):
    """手风琴和箱图接口"""
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        data = [
            {
                'label': 'Arabidopsis thaliana',
                'value': 'Arabidopsis_thaliana'
            },
            {
                'label': 'Oryza sativa',
                'value': 'Oryza_sativa'
            },
            {
                'label': 'Zea mays',
                'value': 'Zea_mays'
            },
            {
                'label': 'Actinidia chinensis',
                'value': 'Actinidia_chinensis'
            },
            {
                'label': 'Capsicum annuum',
                'value': 'Capsicum_annuum'
            },
            {
                'label': 'Citrus clementina',
                'value': 'Citrus_clementina'
            },
            {
                'label': 'Gossypium hirsutum',
                'value': 'Gossypium_hirsutum'
            },
            {
                'label': 'Gossypium raimondii',
                'value': 'Gossypium_raimondii'
            },
            {
                'label': 'Nicotiana tabacum',
                'value': 'Nicotiana_tabacum'
            },
            {
                'label': 'Nicotiana attenuate',
                'value': 'Nicotiana_attenuata'
            },
            {
                'label': 'Populus tremula x alba',
                'value': 'Populus_tremula_x_alba'
            },
            {
                'label': 'Solanum lycopersicum',
                'value': 'Solanum_lycopersicum'
            }
        ]
        return JSONResponse(data=data)


class CrossReferenceSpecieDownViewSet(viewsets.ModelViewSet):
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        try:
            reference_querysets = self.queryset.filter(specie_name=species_name).values_list('reference_name',
                                                                                             flat=True)
            data = [{'label': str(x).replace('_', ' '), 'value': x} for x in list(set(reference_querysets))]
        except Exception as e:
            print(e)
            data = []
        return JSONResponse(data=data)


class CrossSpecieGeneDownViewSet(viewsets.ModelViewSet):
    """手风琴和箱图接口"""
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        reference_name = request.GET.get('reference_name', 'Oryza_sativa')
        gene_id = request.GET.get('gene_id')
        try:
            query_list = []
            if species_name:
                query_list.append(Q(specie_name=species_name))
            if gene_id:
                query_list.append(Q(specie_gene__icontains=gene_id))
            gene_querysets = self.queryset.filter(*query_list).values_list('specie_gene',
                                                                           flat=True)
            data = [{'label': x, 'value': x} for x in list(set(gene_querysets))][0:20]
            # print(len(data))
        except Exception as e:
            print(e)
            data = []
        return JSONResponse(data=data)


class CellIdentificationCsvViewSet(viewsets.ModelViewSet):
    """Cell_Idetification文件上传接口"""
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        reference_name = request.GET.get('reference_name', 'Oryza_sativa')
        tissue = request.GET.get('tissue', 'Root')
        file_name = self.request.GET.get('file_name')
        num_top = self.request.GET.get('num_top')
        try:
            str_uuid = str(uuid.uuid4())
            f = os.popen(
                f'Rscript /data/Cell_identification/Cell_ident_for_CSV.R -r {reference_name}_{tissue}.rds -c {file_name} -n {num_top} -u {str_uuid}'.format(
                    reference_name=reference_name, tissue=tissue,
                    file_name=file_name, num_top=num_top, str_uuid=str_uuid))
            f.read()
            # 返回生成文件链接供下载时传参使用
            data = {
                "classifier_cell_type_csv": "{str_uuid}_Cell_type.csv".format(
                    str_uuid=str_uuid),
                "classifier_cors_matrix_csv": "{str_uuid}_cors_matrix.csv".format(
                    str_uuid=str_uuid),
            }
        except Exception as e:
            print(e)
            data = {
                "classifier_cell_type_csv": '',
                "classifier_cors_matrix_csv": '',
            }
        return JSONResponse(data=data)


class CrossSpeciesAnnotationUploadViewSet(viewsets.ModelViewSet):
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        file = self.request.FILES.get('myfile')
        reference_name = self.request.POST.get('reference_name')
        species_name = request.POST.get('species_name')
        try:
            reference_name = str(reference_name).replace('_', ' ')
            specie = str(species_name).replace('_', ' ')
            if file.name:
                files_uuid = uuid.uuid4()
                # 如果上传的是 rds 文件直接存储在 /data/Sample_QC/upload_data 下
                file_name = str(files_uuid) + '_' + file.name
                file_url = os.path.join(settings.CELL_IDENTIFICATION_CSV_UPLOAD + file_name)
                file_time = str(uuid.uuid4()) + strftime("%Y%m%d%H", localtime())
                # 上传文件的话上传的指定的路径下,进行数据的比对
                with open(file_url, 'wb+') as f:
                    # 分块写入文件
                    for chunk in file.chunks():
                        f.write(chunk)
                        # 根据物种名称映射文件
                    # # 读取物种对应的文件
                homo_log_gene_path = os.path.join(settings.CELL_IDENTIFICATION_CSV_UPLOAD + 'HomologGenes_data.csv')
                homo_log_gene_data = pd.read_csv(
                    homo_log_gene_path, usecols=['Specie', 'Specie_Ref', 'Input_Gene', 'Homolog_Gene'])
                gene_path = file_url
                if os.path.exists(file_url):
                    gene_data = pd.read_csv(gene_path)
                    # 获取当前表头
                    headers = gene_data.columns.tolist()
                    # 将表头1替换为自定义字段名称
                    headers[0] = 'Input_Gene'
                    # 更新表头
                    gene_data.columns = headers
                    # 第一步 根据 传入的 specie 和 reference_name 筛选数据
                    homo_log_gene_data = homo_log_gene_data[
                        (homo_log_gene_data["Specie"] == specie) & (homo_log_gene_data["Specie_Ref"] == reference_name)]
                    # 第二步 根据 Input_Gene 基因这一列合并数据
                    new_df = pd.merge(homo_log_gene_data, gene_data, how="inner", on='Input_Gene')
                    # 删除 'Specie', 'Specie_Ref', 'Input_Gene' 列
                    new_df = new_df.drop(['Specie', 'Specie_Ref', 'Input_Gene'], axis=1)
                    # 根据 Homolog_Gene 去重复
                    new_df = new_df.drop_duplicates(subset=['Homolog_Gene'])
                    # 保存数据
                    new_df.to_csv(os.path.join(
                        settings.CELL_IDENTIFICATION_CSV_UPLOAD + '{file_time}.csv'.format(file_time=file_time)),
                        index=False)
            else:
                return JSONResponse(data={'msg': 'File upload failed！', 'file_name': ''})
            return JSONResponse(data={'msg': 'File upload successfully！', 'file_name': file_time + '.csv'})
        except Exception as e:
            print(e)
            return JSONResponse(data={'msg': 'File upload failed！', 'file_name': ''})


class CellInteractionPngViewSet(viewsets.ModelViewSet):
    """Cell-Cell interactions图接口"""
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        try:
            # data = {
            #     "cell_iteraction_first_png": settings.ATLAS_CELL_EXPRESSION_PICTURE_PNG + '{species_name}_{tissue}_1.png'.format(
            #         species_name=species_name, tissue=tissue),
            #     "cell_iteraction_second_png": settings.ATLAS_CELL_EXPRESSION_PICTURE_PNG + '{species_name}_{tissue}_2.png'.format(
            #         species_name=species_name, tissue=tissue),
            #     "cell_iteraction_thired_png": settings.ATLAS_CELL_EXPRESSION_PICTURE_PNG + '{species_name}_{tissue}_3.png'.format(
            #         species_name=species_name, tissue=tissue),
            #
            # }
            data = {
                "cell_iteraction_first_png": settings.BASE_URL + '/atlas_hot_png/' + '{species_name}_{tissue}_1.png'
                    .format(species_name=species_name, tissue=tissue),
                "cell_iteraction_second_png": settings.BASE_URL + '/atlas_hot_png/' + '{species_name}_{tissue}_2.png'
                    .format(species_name=species_name, tissue=tissue),
                "cell_iteraction_thired_png": settings.BASE_URL + '/atlas_hot_png/' + '{species_name}_{tissue}_3.png'
                    .format(species_name=species_name, tissue=tissue),
            }
        except Exception as e:
            print(e)
            data = {
                "cell_iteraction_first_png": '',
                "cell_iteraction_second_png": '',
                "cell_iteraction_thired_png": '',
            }
        return JSONResponse(data=data)


class CellInteractionCsvListViewSet(viewsets.ModelViewSet):
    """Cell-Cell interactions列表页接口"""
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        page = self.request.GET.get('page', '1')
        page_size = self.request.GET.get('page_size', '20')
        try:
            # 根据物种名称映射文件
            file_name = '{}_{}_Sig'.format(
                species_name, tissue)
            # 读取物种对应的文件
            file_path = os.path.join(
                settings.CELL_IDENTIFICATION_CSV_UPLOAD, "{}.csv".format(file_name))
            # 读取物种对应的文件
            obj_data = pd.read_csv(file_path)
            data = eval(obj_data.to_json(orient="records"))
            data_drfm = data[(int(page) - 1) *
                             10: (int(page) - 1) * 10 + int(page_size)]
            data = {
                "code": 200,
                "data": {
                    "page_size": int(page_size),
                    "results": data_drfm,
                    "count": len(data)
                }
            }
        except Exception as e:
            print(e)
            data = {
            }
        return JSONResponse(data=data)


class CellHistogramPngViewSet(viewsets.ModelViewSet):
    """Cell-Cell interactions柱状图接口"""
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        lr_pair = request.GET.get('lr_pair', 'AT1G01900->AT1G20850')
        gene_list = lr_pair.split('->')
        gene_one = gene_list[0]
        gene_second = gene_list[1]
        try:
            # 根据物种名称映射文件
            file_name = '{}_{}_Sig'.format(
                species_name, tissue)
            # 读取物种对应的文件
            file_path = os.path.join(
                settings.CELL_IDENTIFICATION_CSV_UPLOAD, "{}.csv".format(file_name))
            # 读取物种对应的文件
            obj_data = pd.read_csv(file_path, usecols=['Ligands', 'Receptors', 'Ligands_cell', 'LR_pair'])
            if type == 'All':
                filtered_df = obj_data
            else:
                filtered_df = obj_data[obj_data['LR_pair'] == lr_pair]
            counts = filtered_df['Ligands_cell'].value_counts()
            # print(counts)
            # 将DataFrame转换为包含字典的列表
            result = counts.rename(columns={'name': 'key', 'value': 'value'}).to_dict('records')

            print(result)

            data = {
                "code": 200,
                "data": ''
            }
        except Exception as e:
            print(e)
            data = {
            }
        return JSONResponse(data=data)


class CrossInteractionsLigandsReceptorsDownViewSet(viewsets.ModelViewSet):
    """Cell-Cell interactions列表页接口"""
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """#Ligands和Receptors下拉框接口"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        ligands_receptors_type = request.GET.get('ligands_receptors_type', 'Ligands_cell')
        tissue_data = []
        try:
            # 根据物种名称映射文件
            file_name = '{}_{}_Sig'.format(
                species_name, tissue)
            # 读取物种对应的文件
            file_path = os.path.join(settings.CELL_IDENTIFICATION_CSV_UPLOAD, "{}.csv".format(file_name))
            # 本地测试
            # file_path = 'D:\plant_marker_backend\excel\Arabidopsis_thaliana_Leaf_Sig.csv'
            # 读取物种对应的文件
            obj_data = pd.read_csv(file_path, usecols=[ligands_receptors_type])
            unique_values = obj_data[ligands_receptors_type].drop_duplicates().tolist()
            for type in list(set(unique_values)):
                data = {
                    'label': type,
                    'value': type
                }
                tissue_data.append(data)
        except Exception as e:
            tissue_data = []
        return JSONResponse(data=tissue_data)


class CrossInteractionsLigandsReceptorsGeneDownViewSet(viewsets.ModelViewSet):
    """Cell-Cell interactions列表页接口"""
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """#Ligands和Receptors下拉框接口"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        ligands_receptors_type = request.GET.get('ligands_receptors_type', 'Ligands')
        gene_id = request.GET.get('gene_id', 'AT1G01900')
        tissue_data = []
        try:
            # 根据物种名称映射文件
            file_name = '{}_{}_Sig'.format(
                species_name, tissue)
            # 读取物种对应的文件
            file_path = os.path.join(settings.CELL_IDENTIFICATION_CSV_UPLOAD, "{}.csv".format(file_name))
            # print(file_path)
            # 本地测试
            # file_path = 'D:\plant_marker_backend\excel\Arabidopsis_thaliana_Vegetative_Shoot_Apex_Sig.csv'
            # 读取物种对应的文件
            obj_data = pd.read_csv(file_path, usecols=['Ligands', 'Receptors'])
            if ligands_receptors_type == 'Ligands':
                gene_type = 'Receptors'
            else:
                gene_type = 'Ligands'
            if gene_id:
                obj_data = obj_data[obj_data[ligands_receptors_type] == gene_id]
            else:
                obj_data = obj_data
            unique_values = obj_data[gene_type].drop_duplicates().tolist()
            for type in list(set(unique_values)):
                data = {
                    'label': type,
                    'value': type
                }
                tissue_data.append(data)
        except Exception as e:
            tissue_data = []
        return JSONResponse(data=tissue_data)


class CrossInteractionsLigandsReceptorsHistogramViewSet(viewsets.ModelViewSet):
    """Cell-Cell interactions柱状图接口"""
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """#Ligands和Receptors下拉框接口"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        ligands_receptors_type = request.GET.get('ligands_receptors_type', 'Ligands_cell')
        cell_type = request.GET.get('cell_type', '')
        result = []
        try:
            # 根据物种名称映射文件
            file_name = '{}_{}_Sig'.format(
                species_name, tissue)
            # 读取物种对应的文件
            file_path = os.path.join(settings.CELL_IDENTIFICATION_CSV_UPLOAD, "{}.csv".format(file_name))
            # 本地测试
            # file_path = 'D:\plant_marker_backend\excel\Arabidopsis_thaliana_Leaf_Sig.csv'
            # 读取物种对应的文件
            obj_data = pd.read_csv(file_path,
                                   usecols=['Ligands', 'Receptors', 'Ligands_cell', 'Receptors_cell'])
            if cell_type:
                # 根据指定值筛选 DataFrame 中的某一列数据
                obj_data = obj_data[obj_data[ligands_receptors_type] == cell_type]
            else:
                obj_data = obj_data
            if ligands_receptors_type == 'Ligands_cell':
                counts_type = 'Receptors_cell'
            else:
                counts_type = 'Ligands_cell'
            # 指定的Ligands_cell值
            counts = obj_data[counts_type].value_counts()
            result = [{'label': index, 'value': value} for index, value in counts.items()]
        except Exception as e:
            result = []
        return JSONResponse(data=result)


class CrossInteractionsLigandsReceptorsListViewSet(viewsets.ModelViewSet):
    """Cell-Cell interactions列表页接口"""
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """#Ligands和Receptors下拉框接口"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        ligands_receptors_type = request.GET.get('ligands_receptors_type', 'Ligands_cell')
        cell_type = request.GET.get('cell_type', '')
        histogram_cell_type = request.GET.get('histogram_cell_type', '')
        sorted_type = request.GET.get('sorted_type', '1')  # 1正排 2：倒排
        page = request.GET.get('page', '1')
        page_size = request.GET.get('page_size', '10')
        data_dic = {}
        try:
            # 根据物种名称映射文件
            file_name = '{}_{}_Sig'.format(
                species_name, tissue)
            # 读取物种对应的文件
            file_path = os.path.join(settings.CELL_IDENTIFICATION_CSV_UPLOAD, "{}.csv".format(file_name))
            # 本地测试
            # file_path = 'D:\plant_marker_backend\excel\Arabidopsis_thaliana_Root_Sig.csv'
            # 读取物种对应的文件
            obj_data = pd.read_csv(file_path,
                                   usecols=['Ligands', 'Receptors', 'Ligands_cell', 'Receptors_cell', 'Ligands_expr',
                                            'Receptors_expr',
                                            'Score']
                                   )
            if sorted_type == '1':
                obj_data = obj_data.sort_values(by='Score')
            else:
                obj_data = obj_data.sort_values(by='Score', ascending=False)
            if cell_type:
                # 根据指定值筛选 DataFrame 中的某一列数据
                obj_data = obj_data[obj_data[ligands_receptors_type] == cell_type]
            else:
                obj_data = obj_data
            if ligands_receptors_type == 'Ligands_cell':
                counts_type = 'Receptors_cell'
            else:
                counts_type = 'Ligands_cell'
            if histogram_cell_type:
                obj_data = obj_data[obj_data[counts_type] == histogram_cell_type]
            else:
                obj_data = obj_data
            obj_data = obj_data.drop(ligands_receptors_type, axis=1)
            obj_data.rename(columns={'Receptors_cell': counts_type}, inplace=True)
            data = obj_data.to_dict(orient="records")
            data_drfm = data[(int(page) - 1) *
                             10: (int(page) - 1) * 10 + int(page_size)]
            data_dic = {
                "code": 200,
                "data": {
                    "page_size": int(page_size),
                    "results": data_drfm,
                    "count": len(data)
                }
            }
        except Exception as e:
            data_dic = {
                "code": 200,
                "data": []
            }
        return JSONResponse(data=data_dic)


class CrossReferenceSpeciesDownViewSet(viewsets.ModelViewSet):
    """Cell-Cell interactions列表页接口"""
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """tissue物种组织"""
        reference_name = request.GET.get('reference_name', 'Arabidopsis_thaliana')
        try:
            data_1 = ['Root', "Leaf", "RootTip", 'Shoot', 'Flower']
            data_2 = ['Root', "Leaf"]
            data_3 = ['Ear', "Leaf"]
            tissue_data = list()
            if reference_name == 'Arabidopsis_thaliana':
                tissue_type_list = data_1
            elif reference_name == 'Oryza_sativa':
                tissue_type_list = data_2
            else:
                tissue_type_list = data_3
            for tissue_one in tissue_type_list:
                data = {
                    'label': tissue_one,
                    'value': tissue_one
                }
                tissue_data.append(data)
        except Exception as e:
            tissue_data = []
        return JSONResponse(data=tissue_data)


class CellInteractionSpecieGeneExpressionViewSet(viewsets.ModelViewSet):
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        # lr_pair = request.GET.get('lr_pair', 'AT1G01900->AT1G20850')
        ligand_gene = request.GET.get('ligand_gene', 'AT1G01900')
        receptor_gene = request.GET.get('receptor_gene', 'AT1G20850')
        gene_one = ligand_gene
        gene_second = receptor_gene
        if tissue == 'Vegetative_Shoot_Apex':
            tissue = 'Shoot'
        else:
            tissue = tissue
        try:
            # 根据物种名称映射文件
            file_name = 'umap/{}/{}/umap_data'.format(species_name, tissue)
            # 读取物种对应的文件
            file_path = os.path.join(
                settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(file_name))
            # 1：Sample_ID;2:Clusters;3:Project_ID 筛选相应的列
            umap_data = pd.read_csv(file_path, usecols=['UMAP_1', 'UMAP_2', 'Clusters',
                                                        'Cell_type'])
            umap_data = umap_data.iloc[1:15000]
            # 通过cell_type组成的df
            cell_type_df = umap_data
            # 将Clusters和Cell_type进行拼接聚合
            umap_data['Clusters_Cell_type'] = umap_data['Clusters'].map(str) + ':' + umap_data['Cell_type'].map(
                str)
            # 组合cell_type的df
            cell_type_df = cell_type_df.groupby('Cell_type')
            cell_type_data_list = []
            for group_name, group_data in cell_type_df:
                group_data = group_data[['UMAP_1', 'UMAP_2']]
                data = {
                    'name': str(group_name),
                    'data': group_data.to_dict('split').get('data', [])[1:15000],
                }
                cell_type_data_list.append(data)
            ################第二个目标物种基因的umap
            reference_umap_path = 'umap/{}/{}/umap_data'.format(species_name, tissue)
            reference_file_path = os.path.join(settings.ATLAS_HOT_PNG_DIR, "{}.csv".format(reference_umap_path))
            # 读取物种对应的文件
            reference_file_name = '{}/{}/expression_data'.format(species_name, tissue)
            # # 读取物种对应的文件
            reference_gene_path = os.path.join(settings.ATLAS_HOT_PNG_DIR,
                                               "umap/{file_name}/{gene_id}.csv".format(
                                                   file_name=reference_file_name,
                                                   gene_id=gene_one))
            reference_expression_data = pd.read_csv(reference_file_path,
                                                    usecols=['Cell_ID', 'UMAP_1', 'UMAP_2', 'Clusters',
                                                             'Cell_type'])
            # 组合reference_df的df
            reference_df = reference_expression_data
            if os.path.exists(reference_gene_path):
                reference_gene_data = pd.read_csv(reference_gene_path, usecols=['Cell_ID', 'value'])
                reference_expression_data = pd.merge(
                    reference_expression_data, reference_gene_data, how='left', on='Cell_ID').fillna(0)
                reference_expression_data['value'] = reference_expression_data['value'].astype(
                    str).str[:4].astype(float)
                reference_df = pd.merge(
                    reference_df, reference_gene_data, how='left', on='Cell_ID').fillna(0)
                reference_df['value'] = reference_df['value'].astype(
                    str).str[:4].astype(float)
            else:
                reference_expression_data['value'] = 0
                reference_df['value'] = 0
            reference_expression_data = reference_expression_data.drop('Cell_ID', axis=1)
            reference_expression_data = reference_expression_data.iloc[1:15000]
            reference_expression_data['Clusters_Cell_type'] = reference_expression_data['Clusters'].map(str) + ':' + \
                                                              reference_expression_data[
                                                                  'Cell_type'].map(str)
            reference_expression_data = reference_expression_data.groupby(['Clusters_Cell_type'])
            reference_expression_data_list = []
            for group_name, group_data in reference_expression_data:
                group_data = group_data[['UMAP_1', 'UMAP_2', 'value']]
                group_name = group_name[0]
                data = {
                    'name': group_name.split(":")[1],
                    'data': group_data.to_dict('split').get('data', []),
                    'sort': int(group_name.split(":")[0]) if tissue != 'WholePlant' else group_name.split(":")[0]
                }
                reference_expression_data_list.append(data)
            reference_expression_data_list = sorted(reference_expression_data_list, key=lambda x: x['sort'])
            ################第三个目标物种基因的umap
            third_specie_umap_path = 'umap/{}/{}/umap_data'.format(species_name, tissue)
            third_specie_file_path = os.path.join(settings.ATLAS_HOT_PNG_DIR,
                                                  "{}.csv".format(third_specie_umap_path))
            # 读取物种对应的文件
            third_specie_file_name = '{}/{}/expression_data'.format(species_name, tissue)
            # # 读取物种对应的文件
            third_specie_reference_gene_path = os.path.join(settings.ATLAS_HOT_PNG_DIR,
                                                            "umap/{file_name}/{gene_id}.csv".format(
                                                                file_name=third_specie_file_name,
                                                                gene_id=gene_second))
            third_specie_expression_data = pd.read_csv(third_specie_file_path,
                                                       usecols=['Cell_ID', 'UMAP_1', 'UMAP_2', 'Clusters',
                                                                'Cell_type'])
            # 组合reference_df的df
            third_specie_df = third_specie_expression_data
            if os.path.exists(third_specie_reference_gene_path):
                third_specie_df_data = pd.read_csv(third_specie_reference_gene_path, usecols=['Cell_ID', 'value'])
                third_specie_expression_data = pd.merge(
                    third_specie_expression_data, third_specie_df_data, how='left', on='Cell_ID').fillna(0)
                third_specie_expression_data['value'] = third_specie_expression_data['value'].astype(
                    str).str[:4].astype(float)
                third_specie_df = pd.merge(
                    third_specie_df, third_specie_df_data, how='left', on='Cell_ID').fillna(0)
                third_specie_df['value'] = third_specie_df['value'].astype(
                    str).str[:4].astype(float)
            else:
                third_specie_expression_data['value'] = 0
                third_specie_df['value'] = 0
            third_specie_expression_data = third_specie_expression_data.drop('Cell_ID', axis=1)
            third_specie_expression_data = third_specie_expression_data.iloc[1:15000]
            third_specie_expression_data['Clusters_Cell_type'] = third_specie_expression_data['Clusters'].map(
                str) + ':' + \
                                                                 third_specie_expression_data[
                                                                     'Cell_type'].map(str)
            third_specie_expression_data = third_specie_expression_data.groupby(['Clusters_Cell_type'])
            third_specie_expression_data_list = []
            for group_name, group_data in third_specie_expression_data:
                group_data = group_data[['UMAP_1', 'UMAP_2', 'value']]
                group_name = group_name[0]
                data = {
                    'name': group_name.split(":")[1],
                    'data': group_data.to_dict('split').get('data', []),
                    'sort': int(group_name.split(":")[0]) if tissue != 'WholePlant' else group_name.split(":")[0]
                }
                third_specie_expression_data_list.append(data)
            third_specie_expression_data_list = sorted(third_specie_expression_data_list, key=lambda x: x['sort'])
            all_data_ = {
                'species_umap_data': cell_type_data_list,
                'species_gene_one_umap_data': reference_expression_data_list,
                'species_gene_second_umap_data': third_specie_expression_data_list,
            }
        except Exception as e:
            print(e)
            all_data_ = {
                'species_umap_data': '',
                'species_gene_one_umap_data': '',
                'species_gene_second_umap_data': '',
            }
        return JSONResponse(all_data_)


class CellInteractionTxtDownloadViewSet(viewsets.ModelViewSet):
    """Cell-Cell interactions Txt下载接口"""
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        try:
            data = {
                "cell_iteraction_download_txt": settings.ATLAS_CELL_EXPRESSION_PICTURE_PNG + '{species_name}_{tissue}_Sig.txt'.format(
                    species_name=species_name, tissue=tissue),
            }
        except Exception as e:
            print(e)
            data = {
                "cell_iteraction_download_txt": '',
            }
        return JSONResponse(data=data)


class CrossLrPairGeneDownViewSet(viewsets.ModelViewSet):
    """lr_pair下拉框接口"""
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name', '')
        tissue = request.GET.get('tissue', 'Root')
        type = request.GET.get('type', 'Autocrine')
        cell_type = request.GET.get('cell_type', 'Xylem')
        try:
            # 根据物种名称映射文件
            file_name = '{}_{}_Sig'.format(
                species_name, tissue)
            # 读取物种对应的文件
            file_path = os.path.join(
                settings.CELL_IDENTIFICATION_CSV_UPLOAD, "{}.csv".format(file_name))
            # 读取物种对应的文件
            obj_data = pd.read_csv(file_path)
            if type == 'All':
                type = 'Autocrine'
            else:
                type = type
            # 使用变量进行筛选
            filtered_df = obj_data.loc[(obj_data['Type'] == type) & (obj_data['Ligands_cell'] == cell_type)]
            lr_pair_column = filtered_df['LR_pair'].tolist()[0:20]
            data = [{'label': x, 'value': x} for x in list(set(lr_pair_column))]
        except Exception as e:
            data = []
        return JSONResponse(data=data)


class InteractionCellTypeViewSet(viewsets.ModelViewSet):
    """lr_pair下拉框接口"""
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        type = request.GET.get('type', 'Autocrine')
        try:
            # 根据物种名称映射文件
            file_name = '{}_{}_Sig'.format(
                species_name, tissue)
            # 读取物种对应的文件
            file_path = os.path.join(
                settings.CELL_IDENTIFICATION_CSV_UPLOAD, "{}.csv".format(file_name))
            # 读取物种对应的文件
            obj_data = pd.read_csv(file_path)
            if type == 'All':
                filtered_df = obj_data
            else:
                filtered_df = obj_data[obj_data['Type'] == type]
            lr_pair_column = filtered_df['Ligands_cell'].tolist()
            data = [{'label': x, 'value': x} for x in list(set(lr_pair_column))][0:20]
        except Exception as e:
            data = []
        return JSONResponse(data=data)


class CellInteractionSpeciesDownViewSet(viewsets.ModelViewSet):
    """下拉框"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        data = [{'label': "Arabidopsis thaliana", 'value': 'Arabidopsis_thaliana'}]
        data = {
            'code': 200,
            'msg': "OK",
            'data': data,
        }
        return JSONResponse(data)


class CellInteractionSpeciesTissueDownViewSet(viewsets.ModelViewSet):
    """下拉框"""
    queryset = BrowseInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species = request.GET.get('species_name', 'Arabidopsis_thaliana')
        data = [
            {'label': "Root", 'value': 'Root'},
            {'label': "Leaf", 'value': 'Leaf'},
            {'label': "Vegetative Shoot Apex", 'value': 'Vegetative_Shoot_Apex'},

        ]
        data = {
            'code': 200,
            'msg': "OK",
            'data': data,
        }
        return JSONResponse(data)


class HomeUpdateLogsViewSet(viewsets.ModelViewSet):
    """下拉框"""
    queryset = HomeLogs.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = HomeLogsSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """首页底部日志接口"""
        queryset = HomeLogs.objects.all().order_by('-updated_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = HomeLogsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return JSONResponse(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset_one = self.queryset.filter(id=kwargs['pk']).first()
        serializer = self.serializer_class(queryset_one)
        data = serializer.data
        return JSONResponse(data=data)


class HomeAtlasStaticViewSet(viewsets.ModelViewSet):
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        umap_type = request.GET.get('umap_type', 'umap')
        view_type = request.GET.get('view_type', 'Cell_type')
        try:
            data = {
                "home_atlas_static_png": settings.BASE_URL + 'static_umap_png/' + '{species_name}_{tissue}_{umap_type}_{view_type}.png'.format(
                    species_name=species_name, tissue=tissue, umap_type=umap_type, view_type=view_type),
            }
        except Exception as e:
            print(e)
            data = {
                "home_atlas_static_png": '',
            }
        return JSONResponse(data=data)


class AtlasGeneDonloadViewSet(viewsets.ModelViewSet):
    queryset = MarkerGenesInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = MarkerGenesInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        gene_id = request.GET.get('gene_id', 'AT3G05730')
        try:
            parameter_list = []
            species = species_name.replace("_", " ").replace(" x ", " × ").replace(" var ", " var. ")
            if species_name:
                parameter_list.append(Q(species=species))
            if tissue and tissue != 'WholePlant':
                parameter_list.append(Q(tissue=tissue))
            if gene_id:
                parameter_list.append(Q(gene=gene_id) | Q(name=gene_id))

            gene_id_3 = self.queryset.filter(*parameter_list).values_list("gene", flat=True).distinct()
            # 根据物种名称映射文件-------------取指定路径下的文件名
            file_name = 'umap/{}/{}'.format(species_name, tissue)
            # 读取物种对应的文件
            file_path = os.path.join(
                settings.ATLAS_HOT_PNG_DIR, "{}/expression_data/".format(file_name))
            matched_files = []
            # 使用glob模块进行文件名匹配
            files = glob.glob(os.path.join(file_path, f'*{gene_id}*'))
            for file_path in files:
                file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0] if os.path.splitext(
                    os.path.basename(file_path)) else ''
                # 根据输入的参数动态返回文件名
                matched_files.append(file_name_without_extension)
            gene_id_list = list(set(matched_files))
            gene_id = list(set(chain(gene_id_list, gene_id_3)))[0]
            file_name = 'umap/{}/{}/expression_data'.format(species_name, tissue)
            file_path = os.path.join(
                settings.ATLAS_HOT_PNG_DIR, "{file_name}/{gene_id}.csv".format(file_name=file_name, gene_id=gene_id))
            response = StreamingHttpResponse(open(file_path))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename={file_name}'.format(
                file_name=format(escape_uri_path('{}.csv'.format(gene_id))))
            return response
        except Exception as e:
            print(e)
            data = {
                "gene_download": '下载失败,文件不存在',
            }
        return JSONResponse(data=data)


class AtlasTotalMeanCountViewSet(viewsets.ModelViewSet):
    queryset = HomologGenes.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BrowseInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        view_type = request.GET.get('view_by')
        try:
            file_path = os.path.join(
                settings.ATLAS_HOT_PNG_DIR,
                'umap/{species_name}/{tissue}/total_mean_{view_type}.csv'.format(species_name=species_name,
                                                                                 tissue=tissue, view_type=view_type))
            df_data = pd.read_csv(file_path)
            # 将所有列中的科学计数法格式的数字转换为小数点格式的数字
            for col in df_data.columns:
                df_data[col] = df_data[col].apply(lambda x: '{:.9f}'.format(x))
            # 将转换后的数据重新组成列表
            result = [[col, df_data[col].tolist()[0:1500]] for col in df_data.columns]
        except Exception as e:
            print(e)
            result = []
        return JSONResponse(data=result)


class CellIdentificationCsvDownloadViewSet(viewsets.ModelViewSet):
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """Integration zip下载脚本接口"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        try:
            file_name = '{}_{}.csv'.format(species_name, tissue)
            data = {
                'cell_identification_example_file': settings.CELL_IDENTIFICATION_ZIP_CSV + file_name,
            }
        except Exception as e:
            print(e)
            data = {
                'data': [],
            }
        return JSONResponse(data=data)


class CellAtlasRdsDownloadViewSet(viewsets.ModelViewSet):
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """Atlas Download下载rds文件接口"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        data = {
            'rds_download_url': settings.PROJECT_ATLAS_DOWNLOAD_RDS_URL + species_name + '_' + tissue + '.rds'
        }
        return JSONResponse(data=data)


class CellAtlasDetailDiagramMapViewSet(viewsets.ModelViewSet):
    queryset = CellMarkerInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlantHomeUmaptSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        """Atlas 箱图数据返回接口"""
        species_name = request.GET.get('species_name', 'Arabidopsis_thaliana')
        tissue = request.GET.get('tissue', 'Root')
        view_by = request.GET.get('view_by', 'Cell_type')  # 1:Cell_type、2：Clusters、3：Project_ID
        file_path = settings.ATLAS_HOT_PNG_DIR + 'diagram_map/' + species_name + '/' + tissue + '/expresse_gene_number_{view_by}.txt'.format(
            view_by=view_by)
        print(file_path)
        # 本地测试
        # file_path = 'D:\免疫单细胞数据库\备份数据\diagram_map\Arabidopsis_thaliana\Embryos\expresse_gene_number_Clusters.txt'
        data = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
            data = [line.replace(', ', ',') for line in lines]
            # 把列表中的字典字符串类型转换成字典类型
            data = ast.literal_eval(data[0])
        # print(data)
        return JSONResponse(data)


class CellAtlasGeneSymbolDownloadViewSet(viewsets.ModelViewSet):
    queryset = MarkerGenesInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = MarkerGenesInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        species_name = request.GET.get('species_name')
        tissue = request.GET.get('tissue', 'WholePlant')
        gene_id = request.GET.get('gene_id', '')
        try:
            # Arabidopsis thaliana物种的Root tip组织没有数据，因此获取的Root的数据
            if tissue == "Root_tip" or tissue == "Root tip":
                tissue = "Root"
            # 第一步匹配MarkerGenes
            parameter_list = []
            # tissue = tissue.replace("_", " ").replace(" ","")
            if species_name:
                # 格式化物种名称
                species = species_name.replace("_", " ").replace(" x ", " × ").replace(" var ", " var. ")
                parameter_list.append(Q(species=species))
            if tissue and tissue != 'WholePlant' and tissue != 'Whole Plant':
                tissue_name = tissue.replace(" ", "_")
                parameter_list.append(Q(tissue=tissue))
            else:
                tissue_name = tissue.replace(" ","")
            if gene_id:
                parameter_list.append(Q(gene=gene_id) | Q(name=gene_id))
            gene_id_list1 = self.queryset.filter(*parameter_list).values_list("gene", flat=True).distinct()
            # 第二步匹配Gene文件
            # 根据物种名称映射文件-------------取指定路径下的文件名
            file_name = 'umap/{}/{}'.format(species_name, tissue_name)
            # 读取物种对应的文件
            file_path = os.path.join(settings.ATLAS_HOT_PNG_DIR, "{}/expression_data/".format(file_name))
            # 使用glob模块进行文件名匹配
            files = glob.glob(os.path.join(file_path, f'*{gene_id}*'))
            gene_id_list2 = []
            for file_path in files:
                file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
                gene_id_list2.append(file_name_without_extension)
            # 第三步 两个集合去重返回
            gene_list = list(set(chain(gene_id_list1, gene_id_list2)))
            if len(gene_list) > 0:
                gene_list = [{'name': i, 'value': i} for i in gene_list]

        except Exception as e:
            print(e)
            gene_list = []
        return JSONResponse(data=gene_list)


class MarkerViewSet(viewsets.ModelViewSet):
    """Marker页面下拉框数据展示"""
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        data_list = [
            "Arabidopsis thaliana",
            "Bombax ceiba",
            "Brassica rapa",
            "Catharanthus roseus",
            "Fragaria vesca",
            "Glycine max",
            "Gossypium bickii",
            "Gossypium hirsutum",
            "Manihot esculenta",
            "Marchantia polymorpha",
            "Medicago truncatula",
            "Nicotiana attenuata",
            "Oryza sativa",
            "Phalaenopsis Big Chili",
            "Phyllostachys edulis",
            "Populus alba var. pyramidalis",
            "Populus tremula × alba",
            "Populus trichocarpa",
            "Solanum lycopersicum",
            "Triticum aestivum",
            "Zea mays",
            "Nicotiana tabacum"
        ]

        return JSONResponse(data=data_list)


class MenuViewSet(viewsets.ModelViewSet):
    """菜单栏下拉框数据"""
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        data_list = [
            "All Species",
            "Tissue",
            "Cell Type",
            "Marker",
        ]

        return JSONResponse(data=data_list)


class WordCloudViewSet(viewsets.ModelViewSet):
    "marker页面词云图数据"
    queryset = MarkerGenesInfo.objects.all()
    classic_marker_queryset = ClassicMarkersInfo.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = MarkerGenesInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        query_data_list = self.query_data(self, request)
        result_data = []
        for dict_item in query_data_list:
            dict_data = {
                'name': dict_item[1],
                'source_no': dict_item[2] + 10 if dict_item[3] > 0 else dict_item[2],
            }
            result_data.append(dict_data)
        return JSONResponse(result_data)

    @list_route(methods=('get',), url_path='search_word_cloud_list')
    def search_word_cloud_list(self, request, *args, **kwargs):
        """Search 页面 词云图右侧 table数据接口"""
        query_data_list = self.query_data(self, request)
        result_data = []
        for dict_item in query_data_list:
            dict_data = {
                'name': dict_item[1],
                'source_no': dict_item[2],
            }
            result_data.append(dict_data)

        page = self.paginate_queryset(result_data)
        return self.get_paginated_response(page)

    def query_data(self, request, *args, **kwargs):
        # 当前节点所属的一级节点(one_node)对应物种
        species_name = self.request.GET.get('species_name', 'Arabidopsis thaliana')
        # 当前节点所属的二级节点(two_node)对应组织
        tissue_name = self.request.GET.get('tissue_name', '')
        # 当前节点对应细胞非必传参数
        cell_name = self.request.GET.get('cell_name', '')
        # 模糊搜索条件
        search_gene = self.request.GET.get('search_gene', '')
        # 自定义SQL
        params = [species_name] # SQL 参数
        query_sql = "SELECT " \
                    "mg.gene,IFNULL(mg.name,mg.gene) as name,COUNT(DISTINCT mg.dataset) as source_no, " \
                    "COUNT(DISTINCT cm.gene_id) as classic_count " \
                    "FROM marker_genes_info mg LEFT JOIN classic_markers_info cm ON mg.gene = cm.gene_id " \
                    "AND mg.species=cm.species_name AND mg.tissue=cm.tissue_id AND mg.clusterName = cell_id " \
                    "WHERE mg.species= %s"
        if tissue_name:
            query_sql += " AND mg.tissue = %s"
            params.append(tissue_name)
        if cell_name:
            query_sql += " AND mg.clusterName = %s"
            params.append(cell_name)
        if search_gene:
            query_sql += " AND (gene like %s or name like %s)"
            query_search = '%{}%'.format(search_gene)
            params.append(query_search)
            params.append(query_search)
        query_sql += " GROUP BY mg.gene,mg.name"
        query_sql += " ORDER BY source_no DESC,gene ASC limit 100"
        cursor = connection.cursor()
        cursor.execute(query_sql, params)
        results = cursor.fetchall()
        return results


class NodeDesViewSet(viewsets.ModelViewSet):
    "marker页面树状图子节点信息数据"
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']

    mgi_queryset = MarkerGenesInfo.objects.all()
    ctd_queryset = CellTypeDetails.objects.all()

    def list(self, request, *args, **kwargs):
        # 一级节点的值
        species_name = self.request.GET.get('species_name', 'Arabidopsis thaliana')
        # 二级节点的值
        tissue_name = self.request.GET.get('tissue_name', '')
        # 三级节点的值
        cell_name = self.request.GET.get('cell_name', '')
        query_params = Q(species=species_name)
        celltype_id = ""
        if tissue_name:
            query_params = query_params & Q(tissue=tissue_name)
        if cell_name:
            query_params = query_params & (Q(clusterName=cell_name))
            data = self.mgi_queryset.filter(query_params).first()
            celltype_id = data.celltype_id if data else ""
        name = cell_name if cell_name else tissue_name
        detail = self.ctd_queryset.filter(name=name).first()

        data_dict = {
            "po_id": detail.po_id,
            "celltype_id": celltype_id,
            "description": detail.description
        }

        return JSONResponse(data=data_dict)


class MenuSearchViewSet(viewsets.ModelViewSet):
    "菜单栏搜索结果列表数据"
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']
    queryset = MarkerGenesInfo.objects.all()

    def list(self, request, *args, **kwargs):
        opt_num = self.request.GET.get('opt_num')
        key_word = self.request.GET.get('key_word').strip()
        data = []
        if not key_word:
            return JSONResponse(data)
        # 物种搜索(All Species)
        if opt_num == '1':
            data = self.queryset.filter(species__icontains=key_word).values("species").distinct()
        # 组织搜索(Tissue)
        elif opt_num == '2':
            data = self.queryset.filter(tissue__icontains=key_word).values("tissue", "species").distinct()
        # 细胞搜索(Cell Type)
        elif opt_num == '3':
            data = self.queryset.filter(clusterName__icontains=key_word).values("clusterName", "species").distinct()
        # 基因搜索(Marker)
        elif opt_num == '4':
            # 根据geneid模糊搜索
            query_sql = "SELECT " \
                        "DISTINCT mg.gene, mg.species, gd.description " \
                        "FROM marker_genes_info mg LEFT JOIN gene_details_info gd ON mg.gene = gd.gene_id "
            if key_word:
                query_sql += "WHERE mg.gene like '%{}%'".format(key_word)
            cursor = connection.cursor()
            cursor.execute(query_sql)
            results = cursor.fetchall()

            for item in results:
                dict_data = {
                    "gene": item[0],
                    "species": item[1],
                    "description": item[2]
                }
                data.append(dict_data)
        page = self.paginate_queryset(data)
        return self.get_paginated_response(page)


class SearchCellSelectViewSet(viewsets.ModelViewSet):
    "search页面--通过细胞类型搜索项三级联动下拉框数据"
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        return JSONResponse(data=three_level_data)


class SearchMarkerGeneTable(viewsets.ModelViewSet):
    """Search页面"""
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']
    queryset = MarkerGenesInfo.objects.all()

    def list(self, request, *args, **kwargs):
        """Search页面By marker gene搜索结果页列表接口"""
        query_data_list = self.query_data(self, request)
        page = self.paginate_queryset(query_data_list)
        return self.get_paginated_response(page)

    @list_route(methods=('get',), url_path='search_marker_gene_down')
    def search_marker_gene_down(self, request, *args, **kwargs):
        """Search页面By marker gene (identifier or keyword)搜索结果页列表下载CSV接口"""
        species_name = self.request.GET.get('species_name', 'Arabidopsis thaliana')
        query_data_list = self.query_data(self, request)
        # 文件名称
        file_name = 'search_marker_gene_' + species_name + '.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)

        writer = csv.writer(response)
        # 表头
        headers = ['gene_id', 'species', 'gene_symbol', 'description']
        writer.writerow(headers)

        for item in query_data_list:
            row = []
            # 提取每条记录对应字段的值并添加到行列表中
            for header in headers:
                value = item[header] if header in item else ''
                row.append(value)
            writer.writerow(row)

        return response

    def query_data(self, request, *args, **kwargs):
        # 当前节点所属的一级节点(one_node)对应物种
        species_name = self.request.GET.get('species_name', 'Arabidopsis thaliana')
        search_gene = self.request.GET.get('search_gene', '')

        query_sql = "SELECT " \
                    "DISTINCT mg.gene, mg.name, mg.species, gd.description " \
                    "FROM marker_genes_info mg LEFT JOIN gene_details_info gd ON mg.gene = gd.gene_id " \
                    "WHERE mg.species= '{}'".format(species_name)
        if search_gene:
            query_sql += " AND (mg.gene like '%{}%' or mg.name like '%{}%')".format(search_gene, search_gene)

        cursor = connection.cursor()
        cursor.execute(query_sql)
        results = cursor.fetchall()

        # 整理数据
        result_list = []
        for item in results:
            dict_data = {
                "gene_id": item[0],
                "species": item[2],
                "gene_symbol": item[1],
                "description": item[3]
            }
            result_list.append(dict_data)
        return result_list


class SearchCellTypeTable(viewsets.ModelViewSet):
    """Search页面By cell type搜索结果"""
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']
    queryset = MarkerGenesInfo.objects.all()
    classic_marker_queryset = ClassicMarkersInfo.objects.all()
    sra_queryset = SraInformation.objects.all()

    def list(self, request, *args, **kwargs):
        """Search页面By cell type搜索结果页列表接口"""
        query_data_list = self.query_data(self, request)
        page = self.paginate_queryset(query_data_list)
        return self.get_paginated_response(page)

    @list_route(methods=('get',), url_path='search_clee_type_down')
    def search_clee_type_down(self, request, *args, **kwargs):
        """Search页面By cell type搜索结果页列表下载CSV接口"""
        species_name = self.request.GET.get('species_name', 'Arabidopsis thaliana')

        query_data_list = self.query_data(self, request)
        # 文件名称
        file_name = 'search_cell_type_' + species_name + '.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)

        writer = csv.writer(response)
        # 表头
        headers = ['gene_id', 'species', 'tissue', 'cell_type', 'gene_symbol', 'pmid', 'classic_marker']
        writer.writerow(headers)

        for item in query_data_list:
            row = []
            # 提取每条记录对应字段的值并添加到行列表中
            for header in headers:
                value = item[header] if header in item else ''
                row.append(value)
            writer.writerow(row)

        return response

    def query_data(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name', 'Arabidopsis thaliana')
        tissue_name = self.request.GET.get('tissue_name', '')
        cell_name = self.request.GET.get('cell_name', '')

        # 自定义SQL
        query_sql = "SELECT " \
                    "DISTINCT mg.gene,mg.name,mg.species,cm.id,mg.tissue,mg.clusterName," \
                    "(SELECT GROUP_CONCAT(pmid) as pmid FROM sra_information where species = mg.species " \
                    "and tissue=mg.tissue) as pmid " \
                    "FROM marker_genes_info mg LEFT JOIN classic_markers_info cm ON mg.gene = cm.gene_id " \
                    "AND mg.species=cm.species_name AND mg.tissue=cm.tissue_id AND mg.clusterName = cell_id " \
                    "WHERE mg.species= '{}'".format(species_name)
        # 拼接查询条件
        if tissue_name:
            query_sql += " AND mg.tissue = '{}'".format(tissue_name)
        if cell_name:
            query_sql += " AND mg.clusterName = '{}'".format(cell_name)
        query_sql += " ORDER BY gene ASC"

        cursor = connection.cursor()
        cursor.execute(query_sql)
        results = cursor.fetchall()

        result_data = []
        for dict_item in results:
            classic_flag = "0"
            if dict_item[3]:
                classic_flag = "1"
            dict_data = {
                "gene_id": dict_item[0],
                "species": dict_item[2],
                "tissue:": dict_item[4],
                "cell_type:": dict_item[5],
                "gene_symbol": dict_item[1],
                "classic_marker": classic_flag,
                "pmid": dict_item[6]
            }
            result_data.append(dict_data)
        return result_data


class GeneDetailsInfoViewSet(viewsets.ModelViewSet):
    """ 基因详情页面接口 """

    gene_queryset = GeneDetailsInfo.objects.all()
    marker_queryset = MarkerGenesInfo.objects.all()
    sra_queryset = SraInformation.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = GeneDetailsInfoSerializer
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        gene_id = self.request.GET.get('gene_id', '')

        query_data = self.gene_queryset.filter(gene_id=gene_id).values().first()
        serializer = self.serializer_class(query_data)
        result_data = serializer.data
        return JSONResponse(result_data)

    @list_route(methods=('get',), url_path='gene_details_cell_type')
    def gene_details_cell_type(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name', 'Arabidopsis thaliana')
        gene_id = self.request.GET.get('gene_id', '')
        species_name = str(species_name).replace('_', ' ')
        marker_gene_data = self.marker_queryset.filter(species=species_name, gene=gene_id).values(
            'species', 'tissue', 'clusterName'
        ).annotate(
            dataset_no=Count('dataset', distinct=True), dataset=GroupConcat('dataset')
        ).order_by('-dataset_no')
        if marker_gene_data:
            for dict_item in marker_gene_data:
                sra_data = self.sra_queryset.filter(
                    species=dict_item['species'], tissue=dict_item['tissue']
                ).values('pmid', 'doi_id').distinct()
                pmid_list = []
                for item in sra_data:
                    doi_list = item['doi_id'].split('DOI: ')
                    doi_http = doi_list[1] if len(doi_list) > 1 else doi_list[0]
                    doi_http = 'https://doi.org/' + doi_http if doi_http.startswith('10.') else doi_http.strip()
                    dic_data = {
                        'name': item['pmid'],
                        'label': doi_http
                    }
                    pmid_list.append(dic_data)
                dict_item['pmid'] = pmid_list

        return JSONResponse(marker_gene_data)


class BlastData(viewsets.ModelViewSet):
    """Search页面-blast数据"""
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        # 获取请求参数
        search_method = request.data.get('search_method', 'blastn')
        species = request.data.get('species', 'Arabidopsis_thaliana')
        database = request.data.get('database', 'cds')
        # evalue = request.data.get('evalue', '1e-5')
        query_sequence = request.data.get('query_sequence', None)
        file = request.FILES.get('file', None)

        try:
            # 随机生成文件名
            random_number = hashlib.sha1(os.urandom(24)).hexdigest()
            # 查询的数据库
            db = settings.BLAST_DATA_URL + "{species}_{database}".format(species=species, database=database)
            # 输出文件的名
            out_file_name = "{random_number}.xml".format(random_number=random_number)
            out_file = os.path.join(settings.TEMPS_DIR, out_file_name)
            query_file_name = '{random_number}.{form}'.format(random_number=random_number, form='fa')
            query_file = os.path.join(settings.TEMPS_DIR, query_file_name)
            data = {
                'msg': '数据过长,不符合匹配要求 或 文件格式不符合要求',
                'data': []
            }
            if file:
                content = file.read()
                content_str = content.decode('utf-8')
                filename = file.name
                if content_str.count('>') > 100 or filename.split('.')[-1] != 'fa':
                    return JSONResponse(data)
                with open(query_file, 'wb') as op:
                    op.write(content)
            else:
                if query_sequence and query_sequence.startswith('>'):
                    with open(query_file, 'w') as w_file:
                        w_file.write(query_sequence)
                else:
                    return JSONResponse(data)
            # 组装脚本命令
            blast_cmd = "{search_method} -query {query_file} -db {db} -outfmt 5 -out {out_file}".format(
                search_method=search_method, query_file=query_file, db=db, out_file=out_file
            )
            # 执行脚本
            os.system(blast_cmd)
            species_name = str(species).replace("_", " ")
            query_data = parse_blast_xml(out_file, search_method, species_name)
            dic_data = {
                'msg': 'success',
                'data': query_data
            }
            if os.path.exists(query_file):
                os.remove(query_file)
            if os.path.exists(out_file):
                os.remove(out_file)
        except Exception as e:
            dic_data = {
                'msg': 'success',
                'data': []
            }
            print(e)
        return JSONResponse(dic_data)


class BlastList(viewsets.ModelViewSet):
    """blast下拉框数据"""
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        return JSONResponse(blast_list)


class GetCellBlastData(viewsets.ModelViewSet):
    "search页面--通过细胞类型搜索项三级联动下拉框数据"
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']
    queryset = SpeciesMappingInfo.objects.all()
    serializer_class = SpeciesMappingInfoSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file', None)
        result = {}
        if file:
            # 请求文件名称
            filename = file.name
            filePath = os.path.join(settings.QUERY_FILE, filename)
            upload_file_data = pd.read_csv(file)
            # 保存到目录
            upload_file_data.to_csv(filePath, index=False)
            # 请求文件大小
            file_size = os.path.getsize(filePath)
            size = round(file_size / 1024, 2)
            df = pd.DataFrame(upload_file_data)
            # 请求文件行数、列数
            row_num, column_num = df.shape[0], df.shape[1] - 1
            # 获取前5行前6列数据
            df_sub = df.iloc[:5, :6]
            df_sub.rename(columns={'index': 'Genes'}, inplace=True)
            column_names = df_sub.columns.tolist()
            table_data = eval(df_sub.to_json(orient="records"))
            result = {
                "query_type": "Run",
                "file_name": filename,
                "file_size": "{}KB".format(size),
                "genes_number": row_num,
                "cells_number": column_num,
                "column_names": column_names,
                "table_data": table_data
            }
        return JSONResponse(result)

    @list_route(methods=('get',), url_path='cell_blast_example')
    def CellBlastExample(self, request, *args, **kwargs):
        file_name = "Arabidopsis_thaliana_Root_SRP182008.csv"
        # 示例输入文件地址
        file_path = os.path.join(settings.EXAMPLE_FILE, 'cell_blast/{}'.format(file_name))
        # 存入请求文件目录，后续接口需使用
        save_file_Path = os.path.join(settings.QUERY_FILE, file_name)
        # 读取文件内容
        upload_file_data = pd.read_csv(file_path)
        # 保存到新的目录
        upload_file_data.to_csv(save_file_Path, index=False)
        # 请求文件大小
        file_size = os.path.getsize(file_path)
        size = round(file_size / 1024, 2)
        df = pd.DataFrame(upload_file_data)
        # 请求文件行数、列数
        row_num, column_num = df.shape[0], df.shape[1] - 1
        # 获取前5行前6列数据
        df_sub = df.iloc[:5, :6]
        df_sub.rename(columns={'index': 'Genes'}, inplace=True)
        column_names = df_sub.columns.tolist()
        table_data = eval(df_sub.to_json(orient="records"))
        result = {
            "query_type": "Example",
            "file_name": file_name,
            "file_size": "{}KB".format(size),
            "genes_number": row_num,
            "cells_number": column_num,
            "column_names": column_names,
            "table_data": table_data
        }
        return JSONResponse(result)

    @list_route(methods=('get',), url_path='get_cell_blast_hits')
    def get_cell_blast_hits(self, request, *args, **kwargs):
        species = request.GET.get('species', 'Arabidopsis thaliana')
        tissue = request.GET.get('tissue', 'Hypocotyl callus')
        file_name = request.GET.get('file_name', 'Cell_Blast_Input.csv')
        query_type = request.GET.get('query_type', 'Example')

        data_list = []
        try:
            if query_type == "Example":
                # 示例结果文件路径
                print("请求示例接口开始")
                result_file_path = os.path.join(settings.EXAMPLE_FILE, 'cell_blast/cell_blast_result.csv')
            else:
                print("请求正式接口开始")
                mapping_data = self.queryset.filter(species=species, tissue=tissue).first()
                if mapping_data:
                    # 映射的数据集
                    dataset = mapping_data.mapping
                    print("获取映射数据：", dataset)
                    query_file_Path = os.path.join(settings.QUERY_FILE, file_name)
                    print("请求文件地址：", query_file_Path)
                    # 脚本路径
                    script_path = "/data/Tools/Cell_Blast/run.py"
                    # 执行脚本
                    get_api_data(script_path, dataset, query_file_Path)
                    # 运行结果文件路径
                    result_file_path = os.path.join(settings.RESULT_PATH, "cell_blast_result.csv")
            # 读取结果文件
            file_data = pd.read_csv(result_file_path)
            df = pd.DataFrame(file_data)
            qid_data = df['qid'].unique()

            for qid in qid_data:
                column_data = df[df['qid'] == qid]
                column_json = eval(column_data.to_json(orient='records'))
                qid_dict = {
                    "cell_name ": qid,
                    "count": len(column_data),
                    "query_cell_name": qid + "({})".format(len(column_data)),
                    "hits_table": column_json,
                }
                data_list.append(qid_dict)

        except Exception as e:
            print("cell blast hits error:", e)
            return JSONResponse(data={
                'msg': 'Sorry, there was an error in the job you submitted. Please confirm the format of the input data and submit it again.'},
                                status=status.HTTP_400_BAD_REQUEST)

        result = {
            "query_type": query_type,
            "download_url": settings.BASE_URL + "source_material/result_file/cell_blast_result.csv",
            "result_data": data_list
        }
        return JSONResponse(result)

    @list_route(methods=('get',), url_path='get_cell_blast_predictions')
    def get_cell_blast_predictions(self, request, *args, **kwargs):
        # 请求类型
        query_type = request.GET.get('query_type', 'Example')
        pval_cutoff = float(request.GET.get('pval_cutoff', '0.05'))
        min_hits = float(request.GET.get('min_hits', '2'))
        majority_threshold = float(request.GET.get('majority_threshold', '0.5'))

        try:
            if query_type == "Example":
                # 示例结果文件路径
                result_file_path = os.path.join(settings.EXAMPLE_FILE, "cell_blast/cell_blast_result.csv")
            else:
                # 运行结果文件路径
                result_file_path = os.path.join(settings.RESULT_PATH, "cell_blast_result.csv")
            # 读取结果文件
            file_data = pd.read_csv(result_file_path)
            df = pd.DataFrame(file_data)
            qid_data = df['qid'].unique()
            predictions_list = []
            chart_list = []
            for qid in qid_data:
                column_data = df[df['qid'] == qid]
                # 筛选数据，小于 pval cutoff 的数据筛选掉
                screen_data = column_data[column_data["pval"] < pval_cutoff]
                value_counts = screen_data['Celltype'].value_counts(normalize=True)
                # 占比最大的 cell_type 及 比值
                max_rate, max_value = value_counts.max(), value_counts.idxmax()
                # 保留一位小数的百分比
                percentage = f"{max_rate:.{1}%}"

                hits_number = len(screen_data)
                if hits_number < min_hits:
                    cell_type = "rejected (nan%)"
                elif max_rate < majority_threshold:
                    cell_type = "ambiguous ({})".format(percentage)
                else:
                    cell_type = max_value + "({})".format(percentage)
                dict_data = {
                    "query_cell_name": qid,
                    "cell_type": cell_type,
                    "hits_number": hits_number,
                }
                predictions_list.append(dict_data)
                cell_type = format_cell_type(cell_type)
                chart_data = {
                    "query_cell_name": qid,
                    "cell_type": cell_type,
                    "hits_number": hits_number,
                }
                chart_list.append(chart_data)
            # 根据 hits_number 倒序
            # result_data = sorted(predictions_list, key=lambda item: item["hits_number"], reverse=True)
            # 保存 predictions 结果到CSV文件
            predictions_file_path = os.path.join(settings.RESULT_PATH, "cell_blast_predictions.csv")
            with open(predictions_file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["query_cell_name", "cell_type", "hits_number"])  # CSV文件的头部
                for predictions in predictions_list:
                    writer.writerow(
                        [predictions["query_cell_name"], predictions["cell_type"], predictions["hits_number"]])

            # total_number = sum([item["hits_number"] for item in chart_list])
            # predictions_top_10 = chart_list[:10]
            # total_10 = sum([item["hits_number"] for item in predictions_top_10])
            # others_number = total_number - total_10
            # predictions_top_10.append(
            #     {"query_cell_name": "Others", "hits_number": others_number, "cell_type": "Others"})
            char_df = pd.DataFrame(chart_list)
            # 按列分组并求和
            result = char_df.groupby("cell_type")["hits_number"].sum()
            chart_result = result.to_dict()
            data = {
                "download_url": settings.BASE_URL + "source_material/result_file/cell_blast_predictions.csv",
                "chart_data": chart_result,
                "table_data": predictions_list,
            }
        except Exception as e:
            print("cell blast predictions error:", e)
            return JSONResponse(data={
                'msg': 'Sorry, there was an error in the job you submitted. Please confirm the format of the input data and submit it again.'},
                                status=status.HTTP_400_BAD_REQUEST)
        return JSONResponse(data)


class GetCellIdData(viewsets.ModelViewSet):
    "search页面--通过细胞类型搜索项三级联动下拉框数据"
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']
    queryset = SpeciesMappingInfo.objects.all()
    serializer_class = SpeciesMappingInfoSerializer

    def create(self, request, *args, **kwargs):
        species = request.data.get('species', 'Arabidopsis thaliana')
        tissue = request.data.get('tissue', 'Root')
        file = request.FILES.get('file', None)
        result_data = {}
        try:
            mapping_data = self.queryset.filter(species=species, tissue=tissue).first()
            if file and mapping_data:
                # 映射的数据集
                dataset = mapping_data.mapping
                # 请求的数据文件保存路径
                filePath = os.path.join(settings.QUERY_FILE, file.name)
                upload_file_data = pd.read_csv(file, index_col=0)
                # 保存到目录
                upload_file_data.to_csv(filePath)
                # 请求文件大小
                file_size = os.path.getsize(filePath)
                size = round(file_size / 1024, 2)
                df = pd.DataFrame(upload_file_data)
                # 请求文件行数、列数
                row_num, column_num = df.shape[0], df.shape[1] - 1
                # 脚本路径
                script_path = "/data/Tools/CelliD/run.py"
                # 执行脚本
                get_api_data(script_path, dataset, filePath)
                # 读取结果文件
                result_path = os.path.join(settings.RESULT_PATH, "cell_id_result.csv")
                result = pd.read_csv(result_path)
                # predicted_cell_type_1列去重后的个数
                df = pd.DataFrame(result)
                cell_type_counts = df['predicted_cell_type_1'].value_counts()
                bar_chart_data = cell_type_counts.to_dict()

                data = eval(result.to_json(orient="records"))
                for item in data:
                    item['predicted_cell_type_1'] = str(item['predicted_cell_type_1']).replace("\\", "")
                    item['predicted_cell_type_2'] = str(item['predicted_cell_type_2']).replace("\\", "")
                # 返回结果
                result_data = {
                    "download_url": settings.BASE_URL + "source_material/result_file/cell_id_result.csv",
                    "file_size": "{}KB".format(size),
                    "row_num": row_num,
                    "column_num": column_num,
                    "chart_data": bar_chart_data,
                    "table_data": data,
                }
        except Exception as e:
            print("cell id error:", e)
            result_data = {}

        return JSONResponse(result_data)

    @list_route(methods=('get',), url_path='cell_id_example')
    def CellIdExample(self, request, *args, **kwargs):
        # 请求文件大小
        query_file_path = os.path.join(settings.EXAMPLE_FILE, "cell_id/Arabidopsis_thaliana_Root_SRP182008.csv")
        file_size = os.path.getsize(query_file_path)
        size = round(file_size / 1024, 2)
        query_data = pd.read_csv(query_file_path)
        df = pd.DataFrame(query_data)
        # 请求文件行数、列数
        row_num, column_num = df.shape[0], df.shape[1] - 1

        # 读取结果文件
        file_path = os.path.join(settings.EXAMPLE_FILE, "cell_id/cell_id_result.csv")
        result = pd.read_csv(file_path)
        # predicted_cell_type_1列去除后的个数
        df = pd.DataFrame(result)
        cell_type_counts = df['predicted_cell_type_1'].value_counts()
        bar_chart_data = cell_type_counts.to_dict()
        # 格式化数据
        data = eval(result.to_json(orient="records"))
        for item in data:
            item['predicted_cell_type_1'] = str(item['predicted_cell_type_1']).replace("\\", "")
            item['predicted_cell_type_2'] = str(item['predicted_cell_type_2']).replace("\\", "")
        # 返回结果
        result_data = {
            "download_url": settings.BASE_URL + "source_material/result_file/cell_id_result.csv",
            "file_size": "{}KB".format(size),
            "row_num": row_num,
            "column_num": column_num,
            "chart_data": bar_chart_data,
            "table_data": data,
        }
        return JSONResponse(result_data)


class GetMtscData(viewsets.ModelViewSet):
    "search页面--通过细胞类型搜索项三级联动下拉框数据"
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']
    queryset = SpeciesMappingInfo.objects.all()
    serializer_class = SpeciesMappingInfoSerializer

    def create(self, request, *args, **kwargs):
        species = request.data.get('species', 'Arabidopsis thaliana')
        tissue = request.data.get('tissue', 'Hypocotyl callus')
        file = request.FILES.get('file', None)
        mapping_data = self.queryset.filter(species=species, tissue=tissue).first()
        result_data = {}
        try:
            if file and mapping_data:
                dataset = mapping_data.mapping
                print("获取映射数据：", dataset)
                # 保存上传文件
                filePath = os.path.join(settings.QUERY_FILE, file.name)
                upload_file_data = pd.read_csv(file)
                upload_file_data.to_csv(filePath, index=False)
                # 上传文件大小
                file_size = os.path.getsize(filePath)
                print("上传文件大小", file_size)
                size = round(file_size / 1024, 2)
                df = pd.DataFrame(upload_file_data)
                # 上传文件行数、列数
                row_num, column_num = df.shape[0], df.shape[1] - 1
                print("行数：{}，列数：{}".format(row_num, column_num))
                # 脚本路径
                script_path = "/data/Tools/mtSC/run.py"
                # 执行脚本
                get_api_data(script_path, dataset, filePath)
                print("脚本执行完成！")
                result_path = os.path.join(settings.RESULT_PATH, "CtAnnotation_result.csv")
                # 读取结果文件
                result = pd.read_csv(result_path)
                # cell_type列去重后的个数
                df = pd.DataFrame(result)
                cell_type_counts = df['cell_type'].value_counts()
                bar_chart_data = cell_type_counts.to_dict()
                # 格式化数据
                data = eval(result.to_json(orient="records"))
                for item in data:
                    item['cell_type'] = str(item['cell_type']).replace("\\", "")
                result_data = {
                    "download_url": settings.BASE_URL + "source_material/result_file/CtAnnotation_result.csv",
                    "file_size": "{}KB".format(size),
                    "row_num": row_num,
                    "column_num": column_num,
                    "chart_data": bar_chart_data,
                    "table_data": data,
                }
        except Exception as e:
            print("mtsc error:", e)
            result_data = {}

        return JSONResponse(result_data)

    @list_route(methods=('get',), url_path='mtsc_example')
    def mtSCExample(self, request, *args, **kwargs):
        # 示例上传文件大小
        query_file_path = os.path.join(settings.EXAMPLE_FILE, "mtsc/Arabidopsis_thaliana_Root_SRP182008.csv")
        file_size = os.path.getsize(query_file_path)
        size = round(file_size / 1024, 2)
        query_data = pd.read_csv(query_file_path)
        df = pd.DataFrame(query_data)
        # 上传文件行数、列数
        row_num, column_num = df.shape[0], df.shape[1] - 1

        # 读取示例结果文件内容
        file_path = os.path.join(settings.EXAMPLE_FILE, "mtsc/CtAnnotation_result.csv")
        result = pd.read_csv(file_path)
        # cell_type列去重后的个数
        df = pd.DataFrame(result)
        cell_type_counts = df['cell_type'].value_counts()
        bar_chart_data = cell_type_counts.to_dict()
        # 格式化数据
        data = eval(result.to_json(orient="records"))
        for item in data:
            item['cell_type'] = str(item['cell_type']).replace("\\", "")
        result_data = {
            "download_url": settings.BASE_URL + "source_material/result_file/CtAnnotation_result.csv",
            "file_size": "{}KB".format(size),
            "row_num": row_num,
            "column_num": column_num,
            "chart_data": bar_chart_data,
            "table_data": data,
        }
        return JSONResponse(result_data)


# 浙大对接物种下拉列表数据
class GetTrainSpeciesList(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']
    queryset = SpeciesMappingInfo.objects.all()
    serializer_class = SpeciesMappingInfoSerializer

    def list(self, request, *args, **kwargs):
        data = self.queryset.values("species").distinct()
        result = []
        for item in data:
            result.append(item['species'])

        return JSONResponse(result)


# 浙大对接组织下拉列表
class GetTrainTissueList(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']
    queryset = SpeciesMappingInfo.objects.all()
    serializer_class = SpeciesMappingInfoSerializer

    def list(self, request, *args, **kwargs):
        species = self.request.GET.get('species', 'Arabidopsis thaliana')
        data = self.queryset.filter(species=species).values("tissue").distinct()
        result = []
        for item in data:
            result.append(item['tissue'])
        return JSONResponse(result)
