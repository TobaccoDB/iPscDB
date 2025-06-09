import os
import re
import shutil

import pandas as pd
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from django_server.celery import app
from django_server.response import JSONResponse
from django_server.celery import app
from .serializers import *
from .models import *
# 分片上传文件导入相关模块
from .models import ChunkedUpload, UploadSession
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response
from ... import settings
from ...utils.get_tissue_by_speices import get_tissue
from ...utils.merge_chunks_files import merge_chunks
from ...paginations import PageNumberOffsetPagination
import scanpy as sc

from ...utils.sqmple_qc import sample_qc_fun
from ...utils.get_process import get_sqmple_qc_progress, get_cell_ranger_progress

chunked_storage = FileSystemStorage(location=settings.ANALYSE_BASE_DIR)


class CeleryTaskTestViewSet(viewsets.ModelViewSet):
    queryset = CeleryTaskTest.objects.all()
    serializer_class = CeleryTaskTestSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        # 测试创建异步任务
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return JSONResponse({'msg': '创建成功!'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=('post',), url_path='cellranger_test')
    def cellranger_test(self, request):
        """
        # 执行第一步 cellranger
        """

        serializer = CellrangerTestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return JSONResponse(data={}, status=status.HTTP_200_OK)


class AnalysisViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post', 'delete']
    pagination_class = PageNumberOffsetPagination

    def get_queryset(self):
        email = self.request.GET.get('email', '')
        uuid = self.request.GET.get('uuid', '')
        analysis_name = self.request.GET.get('analysis_name', '')
        source = self.request.GET.get('source', 'cell_ranger')
        self.query_list = []  # 初始化 query_list 为实例变量

        if email:
            self.query_list.append(Q(email=email))
        if analysis_name:
            self.query_list.append(Q(analysis_name=analysis_name))
        # if uuid:
        #     self.query_list.append(Q(uuid=uuid))
        # self.query_list.append(Q(source=source))
        # 根据 query_list 构建 queryset
        # return self.queryset.filter(*self.query_list) if self.query_list else self.queryset
        return self.queryset.filter(*self.query_list).filter(uuid=uuid) if uuid else self.queryset.filter(
            *self.query_list)

    def get_serializer_class(self):
        # 如果 email 和 analysis_name 都为空，则使用简单的序列化器
        email = self.request.GET.get('email', '')

        if not email:
            return AnalysisSimpleSerializer  # 使用简单的序列化器
        else:
            return AnalysisSerializer  # 使用详细的序列化器

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset_values_list = self.paginate_queryset(queryset)

        # 根据 query_list 是否为空选择序列化器
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset_values_list, many=True)

        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        return JSONResponse({'msg': '非法操作!'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        # 你可以选择调用父类的 retrieve 方法来确保默认行为
        instance = self.get_object()  # 通过DRF的方式获取对象
        serializer = AnalysisDetailSerializer(instance)  # 使用当前设置的序列化器
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """删除操作"""
        try:
            analysis = self.queryset.get(id=kwargs['pk'])
            analysis.delete()
            return JSONResponse({'msg': '删除成功'}, status=status.HTTP_200_OK)

        except Analysis.DoesNotExist:

            return JSONResponse({'msg': '该数据不存在'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=('post',), url_path='cellranger')
    def cellranger(self, request):
        """
        # 执行第一步 cellranger
        """

        serializer = CellrangerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return JSONResponse(data={}, status=status.HTTP_200_OK)

    @action(detail=False, methods=('post',), url_path='sample_qc')
    def sample_qc(self, request):
        """
        # 执行第二步 sample_qc
        """

        serializer = SampleQCSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        qc_filter_finally_data = serializer.save()

        return Response(qc_filter_finally_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=('post',), url_path='data_process')
    def data_process(self, request):
        """
        # 执行第三步 data_process
        """

        serializer = DataProcessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        qc_filter_finally_data = serializer.save()

        return Response(qc_filter_finally_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=('post',), url_path='cluster')
    def cluster(self, request):
        """
        # 执行第四步 cluster
        """

        serializer = ClusterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        qc_filter_finally_data = serializer.save()

        return Response(qc_filter_finally_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=('post',), url_path='from_sample_qc_one_step')
    def from_sample_qc_one_step(self, request):
        """
        # 一键生成 从sample Qc开始
        """

        serializer = AnalysisFromSampleQCOneStepSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        qc_filter_finally_data = serializer.save()

        return Response(qc_filter_finally_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=('post',), url_path='from_cell_ranger_one_step')
    def from_cell_ranger_one_step(self, request):
        """
        # 一键生成 从Cell ranger开始
        """

        serializer = AnalysisFromCellrangerOneStepSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        qc_filter_finally_data = serializer.save()

        return Response(qc_filter_finally_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=('post',), url_path='revoke')
    def revoke(self, request):
        """
        # 停止定时任务
        """
        task_id = request.data.get('task_id', None)
        if task_id:
            app.control.revoke(task_id, terminate=True)

        return JSONResponse(data={"msg": "停止成功"}, status=status.HTTP_200_OK)


class AnalysisNewJobViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisNewJobSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = AnalysisNewJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return JSONResponse(data, status=status.HTTP_200_OK)


class AnalysisFileUploadViewSet(viewsets.ModelViewSet):
    queryset = ChunkedUpload.objects.all()
    serializer_class = ChunkedUploadSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        '''
        upload_id: 唯一标识一次完整上传会话的ID，用于区分不同的上传任务。在需求中，它代表存储路径中的UUID部分。
        data_type: 用于区分文件属于哪一组（data1 或 data2）。
        file_index: 当前文件在这组文件中的位置，从 0 开始。
        chunk_number: 当前文件块（分片）的编号，从 1 开始递增。
        total_chunks: 当前文件的总分片数，用于判断文件的所有分片是否已上传完成。
        file: 当前请求上传的文件块（分片），是 request.FILES 对象的一部分。
        filename: 原始文件的名称。虽然文件被分块，但每个分片在上传时仍然需要关联原始文件的名称，以便最终合并成一个完整的文件。
        在实现分块上传时，后端会接收这些文件分片并将其存储在服务器的临时位置。当所有分片上传完成后，再将这些分片合并为一个完整的文件。file 字段在每次上传请求中包含当前的文件分片内容。
        '''
        filename = request.data.get('filename')  # 存储的文件名
        sample_name = request.data.get('sample_name')  # sampleNmae校验文件名 是否合法
        pattern = fr'^{re.escape(sample_name)}_S\d+_L\d+_R\d+_\d+\.fastq\.gz$'
        # pattern = r'^[\w\-]+_S\d+_L\d+_R\d+_\d+\.fastq\.gz$'
        # 使用 re.match() 校验文件名
        if not re.match(pattern, filename):
            return Response({'error': '上传文件名不符合规范,请重新上传!'}, status=400)
        upload_id = request.data.get('upload_id')  # 每套数据的最外层文件夹 uuid
        data_type = request.data.get('data_type')  # 区分是data1 or data2
        file_index = int(request.data.get('file_index'))  # 0, 1, 2, 3 每组数据对应的索引
        chunk_number = int(request.data.get('chunk_number'))
        total_chunks = int(request.data.get('total_chunks'))
        file = request.FILES.get('file')
        file_submit_name = request.data.get('file_submit_name')  # R1 I1 R2 R2 每组提交按钮对应的名字
        current_row = request.data.get('current_row', 'first')  # data1或者data2下第几行的文件字段来记录当前第几行 first、second、third,默认第一行
        data1_sample_name = request.data.get('data1_sample_name', '')  # 用于重命名上传文件的字段
        data2_sample_name = request.data.get('data2_sample_name', '')  # 用于重命名上传文件的字段
        # 校验是否缺少参数
        if not all(
                [upload_id, data_type, file_index is not None, chunk_number is not None, total_chunks is not None, file,
                 filename]):
            return Response({'error': 'Missing required parameters'}, status=400)

        # 获取或创建 UploadSession，用于判断文件是分所有分片上传完成
        session, created = UploadSession.objects.get_or_create(upload_id=upload_id)

        # 创建 UUID 文件夹
        uuid_path = os.path.join(settings.ANALYSE_BASE_DIR, upload_id, data_type, 'fastqs')
        if not os.path.exists(uuid_path):
            os.makedirs(uuid_path)

        # 设置自定义存储参数
        chunked_storage = ChunkedFileSystemStorage()
        chunked_storage.set_custom_params(upload_id, data_type)

        # 存储分片
        chunk = ChunkedUpload(
            upload_id=upload_id,
            data_type=data_type,
            file_index=file_index,
            chunk_number=chunk_number,
            total_chunks=total_chunks,
            filename=filename,  # 存储文件名
            file=file
        )
        chunk.file.storage = chunked_storage
        chunk.save()

        # 检查是否所有分片都上传完成
        uploaded_chunks = ChunkedUpload.objects.filter(upload_id=upload_id, data_type=data_type, filename=filename)
        total_uploaded_chunks = uploaded_chunks.count()
        expected_chunks = uploaded_chunks.values('total_chunks').distinct()
        if len(expected_chunks) == 1 and total_uploaded_chunks == expected_chunks[0]['total_chunks']:
            session.is_complete = True
            session.save()
            # 上传完后记录到文件名存储表中
            UploadFile.objects.create(upload_id=upload_id, data_type=data_type,
                                      file_submit_name=file_submit_name,
                                      current_row=current_row, filename=filename)
            # 记录sqmple name的数据
            FromSampleUploadFile.objects.create(upload_id=upload_id, data_type=data_type, file_name=filename,
                                                file_source_name=file.name, data1_sample_name=data1_sample_name,
                                                data2_sample_name=data2_sample_name)
            # 触发文件合并逻辑
            merge_chunks(upload_id, data_type, filename, chunked_storage)
            # 删除数据库中对应的分块记录，防止再次上传到同一个文件夹下面报错
            with transaction.atomic():
                uploaded_chunks.delete()

            return Response({'message': 'Upload completed successfully!', 'upload_id': upload_id})

        return Response({'message': 'Chunk uploaded successfully!', 'upload_id': upload_id})


class AnalysisFileDownloadViewSet(viewsets.ModelViewSet):
    queryset = ChunkedUpload.objects.all()
    serializer_class = ChunkedUploadSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        file_uuid = request.GET.get('file_uuid', '')
        data_type = request.GET.get('data_type', '')
        try:
            dic = {
                'barcodes_download_url': '{ip}cell_ranger/{file_uuid}/{data_type}/outs/outs/filtered_feature_bc_matrix/barcodes.tsv.gz'.format(
                    ip=settings.ANALYSIS_BASE_URL, file_uuid=file_uuid, data_type=data_type),
                'features_download_url': '{ip}cell_ranger/{file_uuid}/{data_type}/outs/outs/filtered_feature_bc_matrix/features.tsv.gz'.format(
                    ip=settings.ANALYSIS_BASE_URL, file_uuid=file_uuid, data_type=data_type),
                'matrix_download_url': '{ip}cell_ranger/{file_uuid}/{data_type}/outs/outs/filtered_feature_bc_matrix/matrix.mtx.gz'.format(
                    ip=settings.ANALYSIS_BASE_URL, file_uuid=file_uuid, data_type=data_type),
                'web_summary_url': '{ip}cell_ranger/{file_uuid}/{data_type}/outs/outs/web_summary.html'.format(
                    ip=settings.ANALYSIS_BASE_URL, file_uuid=file_uuid, data_type=data_type)
            }
        except Exception as e:
            dic = {
                'file_download_url': '',
                'web_summary_url': ''
            }
        return JSONResponse(dic, status=status.HTTP_200_OK)


class SpeciesDownBoxViewSet(viewsets.ModelViewSet):
    '''类别下拉框窗口'''
    queryset = SpeciesTranscriptome.objects.all().order_by('id')
    serializer_class = SpeciesDownBoxSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        # 下拉框接口：物种下拉框是传值 ：species；转录组下拉框是传值：transcriptome
        type = self.request.GET.get('type', '')
        species_name = self.request.GET.get('species_name', 'Arabidopsis_thaliana')
        if type == 'species':
            down_box = [
                {
                    "name": "Arabidopsis thaliana",
                    "value": "Arabidopsis_thaliana"
                },
                {
                    "name": "Bombax ceiba",
                    "value": "Bombax_ceiba"
                },
                {
                    "name": "Brassica rapa",
                    "value": "Brassica_rapa"
                },
                {
                    "name": "Catharanthus roseus",
                    "value": "Catharanthus_roseus"
                },
                {
                    "name": "Fragaria vesca",
                    "value": "Fragaria_vesca"
                },
                {
                    "name": "Glycine max",
                    "value": "Glycine_max"
                },
                {
                    "name": "Gossypium bickii",
                    "value": "Gossypium_bickii"
                },
                {
                    "name": "Gossypium hirsutumv",
                    "value": "Gossypium_hirsutumv"
                },
                {
                    "name": "Manihot esculenta",
                    "value": "Manihot_esculenta"
                },
                {
                    "name": "Marchantia polymorpha",
                    "value": "Marchantia_polymorpha"
                },
                {
                    "name": "Medicago truncatula",
                    "value": "Medicago_truncatula"
                },
                {
                    "name": "Nicotiana attenuata",
                    "value": "Nicotiana_attenuata"
                },
                {
                    "name": "Oryza sativa",
                    "value": "Oryza_sativa"
                },
                {
                    "name": "Phalaenopsis Big Chili",
                    "value": "Phalaenopsis_Big_Chili"
                },
                {
                    "name": "Phyllostachys edulis",
                    "value": "Phyllostachys_edulis"
                },
                {
                    "name": "Populus alba × glandulosa",
                    "value": "Populus_alba_x_glandulosa"
                },
                {
                    "name": "Populus alba var. pyramidalis",
                    "value": "Populus_alba_var._pyramidalis"
                },
                {
                    "name": "Populus tremula × alba",
                    "value": "Populus_tremula_x_alba"
                },
                {
                    "name": "Populus trichocarpa",
                    "value": "Populus_trichocarpa"
                },
                {
                    "name": "Solanum lycopersicum",
                    "value": "Solanum_lycopersicum"
                },
                {
                    "name": "Triticum aestivum",
                    "value": "Triticum_aestivum"
                },
                {
                    "name": "Zea mays",
                    "value": "Zea_mays"
                }
            ]
        else:
            transcriptome_records = self.queryset.filter(species_name=species_name).values_list('transcriptome',
                                                                                                flat=True).distinct()
            down_box = [{"name": transcriptome} for transcriptome in transcriptome_records]
        return JSONResponse(data=down_box, status=status.HTTP_200_OK)


class SpeciesTissueDownBoxViewSet(viewsets.ModelViewSet):
    '''类别下拉框窗口'''
    queryset = SpeciesTranscriptome.objects.all().order_by('id')
    serializer_class = SpeciesDownBoxSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        species_name = self.request.GET.get('species_name', 'Arabidopsis_thaliana')
        down_box = get_tissue(species_name)
        return Response(data=down_box)


class SampleQcDataShowViewSet(viewsets.ModelViewSet):
    '''Qcdata1，和data2的数据 展示'''
    queryset = SampleQcDataTypeResult.objects.all().order_by('id')
    serializer_class = SampleQcDataTypeResultSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        try:
            uuid = request.GET.get('uuid', '')
            mt = request.GET.get('mt', '')
            pt = request.GET.get('pt', '')
            tag = request.GET.get('tag', None)
            base_path = f'{settings.ANALYSE_BASE_DIR}/{uuid}'
            request_data = {"mt": mt, "pt": pt, 'base_path': base_path}
            if tag == 'run':
                ## 第二步，通过查询，如果存在旧数据就清空 当前步骤以及后面的第三、四步和第五步的数据
                # 定义要查询的模型
                models_to_check = [SampleQcDataTypeResult, SampleQcFilterResult, DataProcessResult, ClusterResult,
                                   AnnotationResult]
                for model in models_to_check:
                    queryset = model.objects.filter(uuid=uuid)
                    if queryset.exists():
                        queryset.delete()
                # 更新或创建记录
                SampleQcPtMt.objects.update_or_create(uuid=uuid, defaults={'mt': mt, 'pt': pt})
                all_data = self._collect_data(base_path, request_data)

                # 更新数据
                SampleQcDataTypeResult.objects.update_or_create(
                    uuid=uuid,
                    defaults={'result_data': all_data}
                )
                # 更新记录run qc跑了第几步
                Analysis.objects.update_or_create(uuid=uuid, defaults={'is_run_qc': 1, 'status': 'Finished'})
                return JSONResponse(all_data, status=status.HTTP_200_OK)
            else:
                # 获取查询结果
                result = self.queryset.filter(uuid=uuid)
                serializer = self.serializer_class(result, many=True)
                serialized_data = serializer.data
                response_data = {
                    "code": 200,
                    "data": [item['result_data'] for item in serialized_data][0] if serialized_data else []
                }
                return Response(response_data)
        except Exception as e:
            # 捕获任何异常并返回错误响应
            error_message = f"出现错误: {str(e)}"
            return Response({"code": 500, "message": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _collect_data(self, base_path, request_data):
        """私有方法来收集数据，减少重复代码"""
        all_data = []
        for dir_name in ['data1', 'data2']:
            try:
                # 自动检测文件类型
                file_path_gz = self._get_file_path(base_path, dir_name, 'gz')
                file_path_h5 = self._get_file_path(base_path, dir_name, 'h5')

                if os.path.exists(file_path_gz):
                    adata = sc.read_10x_mtx(file_path_gz, var_names='gene_symbols')
                    qc_data = sample_qc_fun(adata, dir_name, **request_data)
                elif os.path.exists(file_path_h5):
                    # adata = sc.read_h5ad(file_path_h5)
                    try:
                        adata = sc.read_h5ad(file_path_h5)
                    except Exception as e:
                        adata = sc.read_10x_h5(file_path_h5)
                    qc_data = sample_qc_fun(adata, dir_name, **request_data)
                else:
                    qc_data = self._default_qc_data()

                all_data.append({dir_name: qc_data})
            except Exception as e:
                # 捕获收集数据过程中的异常
                qc_data = self._default_qc_data()
                error_message = f"数据收集错误 ({dir_name}): {str(e)}"
                all_data.append({"error": error_message})
        return all_data

    def _get_file_path(self, base_path, dir_name, run_type):
        """根据运行类型获取文件路径"""
        if run_type == 'gz':
            return f"{base_path}/{dir_name}/outs/outs/filtered_feature_bc_matrix"
        return f"{base_path}/{dir_name}/outs/outs/filtered_feature_bc_matrix.h5"

    def _load_data(self, file_path, run_type):
        """根据运行类型加载数据"""
        if run_type == 'gz':
            return sc.read_10x_mtx(file_path, var_names='gene_symbols')
        # 读取h5
        else:
            try:
                adata = sc.read_h5ad(file_path)
            except Exception as e:
                adata = sc.read_10x_h5(file_path)
        return adata

    def _default_qc_data(self):
        """返回默认的QC数据字典"""
        return {
            "max_n_genes_by_counts": 0,
            "min_n_genes_by_counts": 0,
            "max_total_counts": 0,
            "min_total_counts": 0,
            "max_pct_counts_mt": 0,
            "min_pct_counts_mt": 0,
            "max_pct_counts_pt": 0,
            "min_pct_counts_pt": 0
        }


class QcFilterDatAShowViewSet(viewsets.ModelViewSet):
    '''filter数据显示'''
    queryset = SampleQCFilterData.objects.all().order_by('id')
    serializer_class = QcFilterDatAShowSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        uuid = self.request.GET.get('uuid', '')
        query_list = list()
        if uuid:
            query_list.append(Q(uuid=uuid))
        queryset = self.queryset.filter(*query_list)
        queryset_values_list = self.paginate_queryset(queryset)
        if not queryset_values_list:  # 如果没有数据
            # 返回默认值
            default_data = {
                "page_size": 15,
                "results": [
                    {
                        "uuid": uuid,
                        "max_n_genes_by_counts": 5500,
                        "min_n_genes_by_counts": 2000,
                        "max_total_counts": 8000,
                        "min_total_counts": 200,
                        "max_pct_counts_mt": 0,
                        "min_pct_counts_mt": 0,
                        "max_pct_counts_pt": 0,
                        "min_pct_counts_pt": 0
                    }
                ],
                "count": 1
            }
            return Response({"code": 200, "data": default_data})
            # 如果有数据，正常序列化并返回分页结果
        serializer = self.serializer_class(queryset_values_list, many=True)
        return self.get_paginated_response(serializer.data)


class DataProcessShowViewSet(viewsets.ModelViewSet):
    '''data process数据显示'''
    queryset = DataProcessAnalysis.objects.all().order_by('id')
    serializer_class = DataProcessShowSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        uuid = self.request.GET.get('uuid', '')
        query_list = list()
        if uuid:
            query_list.append(Q(uuid=uuid))
        queryset = self.queryset.filter(*query_list)
        queryset_values_list = self.paginate_queryset(queryset)
        if not queryset_values_list:  # 如果没有数据
            obj = FromSampleUploadFile.objects.filter(upload_id=uuid)
            # 返回默认值
            default_data = {
                "page_size": 15,
                "results": [
                    {
                        "uuid": uuid,
                        "min_mean": 0.0125,
                        "max_mean": 3,
                        "min_disp": 0.25,
                        "n_jobs": 10,
                        "max_value": 10,
                        "n_neighbors": 30,
                        "n_pcs": 50,
                        "nfeatures": 200,
                        "selection_method": 'vst',
                        'data1_sample_name': obj.exclude(
                            data1_sample_name='').first().data1_sample_name if obj.exists() else 'scDR1',
                        'data2_sample_name': obj.exclude(
                            data2_sample_name='').first().data2_sample_name if obj.exists() else 'scDR2'
                    }
                ],
                "count": 1
            }
            return Response({"code": 200, "data": default_data})
            # 如果有数据，正常序列化并返回分页结果
        serializer = self.serializer_class(queryset_values_list, many=True)
        return self.get_paginated_response(serializer.data)


class QcFilterDatAResultViewSet(viewsets.ModelViewSet):
    '''filter数据显示'''
    queryset = SampleQcFilterResult.objects.all().order_by('id')
    serializer_class = SampleQcFilterResultSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        uuid = self.request.GET.get('uuid', '')
        data_type = self.request.GET.get('data_type', '')
        result = self.queryset.filter(uuid=uuid, data_type=data_type)
        queryset_values_list = self.paginate_queryset(result)
        serializer = self.serializer_class(queryset_values_list, many=True)
        return self.get_paginated_response(serializer.data)


class DataProcessResultViewSet(viewsets.ModelViewSet):
    '''data process数据显示'''
    queryset = DataProcessResult.objects.all().order_by('id')
    serializer_class = DataProcessResultSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        uuid = self.request.GET.get('uuid', '')
        result = self.queryset.filter(uuid=uuid)
        queryset_values_list = self.paginate_queryset(result)
        status_filter = Analysis.objects.filter(uuid=uuid)
        # 如果有数据，正常序列化并返回分页结果
        serializer = self.serializer_class(queryset_values_list, many=True)
        return self.get_paginated_response(serializer.data)


class ClusterResultViewSet(viewsets.ModelViewSet):
    '''ClusterResult数据显示'''
    queryset = ClusterResult.objects.all().order_by('id')
    serializer_class = ClusterResultSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        uuid = self.request.GET.get('uuid', '')
        result = self.queryset.filter(uuid=uuid)
        queryset_values_list = self.paginate_queryset(result)
        status_filter = self.queryset.filter(uuid=uuid)
        # 当前数据只有在异步任务跑成功，才能读取文件，进行数据返回。
        if status_filter.exists():
            # 如果有数据，正常序列化并返回分页结果
            serializer = self.serializer_class(queryset_values_list, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response({'msg': '数据正在处理，请稍后再试!', 'code': 200, 'data': {}})


class ClusterResolutionViewSet(viewsets.ModelViewSet):
    '''ClusterResult数据显示'''
    queryset = ClusterResult.objects.all().order_by('id')
    serializer_class = ClusterResolutionSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        uuid = self.request.GET.get('uuid', '')
        result = self.queryset.filter(uuid=uuid).values('resolution')
        if not result:
            result = [{
                "resolution": 0.5
            }]
        return JSONResponse(result, status=status.HTTP_200_OK)


class CellAnnotationResultViewSet(viewsets.ModelViewSet):
    '''AnnotationResult数据显示'''
    queryset = AnnotationResult.objects.all().order_by('id')
    serializer_class = AnnotationResultSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        uuid = self.request.GET.get('uuid', '')
        result = self.queryset.filter(uuid=uuid)
        queryset_values_list = self.paginate_queryset(result)
        serializer = self.serializer_class(queryset_values_list, many=True)
        return self.get_paginated_response(serializer.data)


class ClusterResultListViewSet(viewsets.ModelViewSet):
    '''ClusterResultList数据显示'''
    queryset = ClusterResult.objects.all().order_by('id')
    serializer_class = ClusterResultSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        uuid = self.request.GET.get('uuid', '')
        page = int(self.request.GET.get('page', 1))
        page_size = int(self.request.GET.get('page_size', 10))
        count_cmd_path = f'{settings.ANALYSE_BASE_DIR}/{uuid}'
        dir_name = 'data1'
        count_cmd_dir = f"{count_cmd_path}/{dir_name}"
        rank_genes_groups_data_file = f'{count_cmd_dir}/outs/outs/rank_genes_groups_data.csv'
        # 读取 CSV 文件
        df = pd.read_csv(rank_genes_groups_data_file)
        if 'cell_type' in df.columns:
            df['cell_type'] = df['cell_type'].fillna('No Cell')
        else:
            df['cell_type'] = 'No Cell'
        total_rows = len(df)
        start = (page - 1) * page_size
        end = start + page_size
        # 获取当前页的数据
        page_data = df.iloc[start:end].to_dict(orient='records')
        if self.queryset.filter(uuid=uuid).exists():
            # 构建分页结果
            result = {
                "page_size": page_size,
                "results": page_data,  # 将分页数据放入 results 数组
                "count": total_rows,  # 数据总条数,
            }
            # 返回响应
            return Response({"code": 200, "data": result})
        else:
            # 返回响应
            result = {
                "page_size": page_size,
                "results": [],  # 将分页数据放入 results 数组
                "count": 0,  # 数据总条数,
            }
            return Response({"code": 200, "data": result})


class SampleQcPtMtViewSet(viewsets.ModelViewSet):
    '''pt mt数据显示'''
    queryset = SampleQcPtMt.objects.all().order_by('id')
    serializer_class = SampleQcPtMtSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        uuid = self.request.GET.get('uuid', '')
        # 获取查询结果
        result = self.queryset.filter(uuid=uuid)
        # 序列化查询结果
        serializer = self.serializer_class(result, many=True)
        # 获取序列化后的数据
        serialized_data = serializer.data
        if result:
            return Response({"code": 200, "data": serialized_data})
        species_name_obj = Analysis.objects.filter(uuid=uuid)
        if species_name_obj.exists():
            species_name = species_name_obj.first().species_name
        else:
            species_name = ''

        if species_name and species_name == 'Arabldopsls_thaliana':
            serialized_data = [{
                "pt": "ATCG",
                "mt": "ATMG"
            }]
        else:
            serialized_data = [{
                "pt": "",
                "mt": ""
            }]
        # 组织最终返回的数据结构
        return Response({"code": 200, "data": serialized_data})


class SampleQcUploadViewSet(viewsets.ModelViewSet):
    """SampleQc文件上传接口"""
    queryset = ChunkedUpload.objects.all()
    serializer_class = ChunkedUploadSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        '''
        QC 文件上传接口
        '''
        file = request.FILES.get('file')
        upload_id = request.data.get('upload_id')  # 每套数据的最外层文件夹 uuid
        data_type = request.data.get('data_type')  # 区分是data1 or data2
        file_name = request.data.get('file_name')  # 用于重命名上传文件的字段
        data1_sample_name = request.data.get('data1_sample_name', '')  # 用于重命名上传文件的字段
        data2_sample_name = request.data.get('data2_sample_name', '')  # 用于重命名上传文件的字段

        if not file or not upload_id or not data_type:
            return Response({'message': '上传失败：缺少必要的参数或文件！', 'upload_id': ''}, status=400)
        # 如果没有提供file_name, 使用上传的文件原名
        new_file_name = file_name if file_name else file.name
        try:
            # 创建 UUID 文件夹
            # 判断文件后缀是否为 '.h5'
            if new_file_name.lower().endswith('.h5ad') or new_file_name.lower().endswith('.h5'):
                uuid_path = os.path.join(settings.ANALYSE_BASE_DIR, upload_id, data_type, 'outs', 'outs')
            else:
                uuid_path = os.path.join(settings.ANALYSE_BASE_DIR, upload_id, data_type, 'outs', 'outs',
                                         'filtered_feature_bc_matrix')
            os.makedirs(uuid_path, exist_ok=True)

            file_path = os.path.join(uuid_path, new_file_name)  # 使用 file.name 而不是 f'{file}' 确保文件名安全
            # 上传文件到指定的路径下, 进行数据的比对
            with open(file_path, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            FromSampleUploadFile.objects.create(upload_id=upload_id, data_type=data_type,
                                                file_name=file_name,
                                                file_source_name=file.name,
                                                data1_sample_name=data1_sample_name,
                                                data2_sample_name=data2_sample_name
                                                )
        except Exception as e:
            return Response({'message': f'上传失败: {str(e)}', 'upload_id': ''}, status=500)

        return Response({'message': '上传成功！', 'upload_id': upload_id})


class SampleQcUploadShowViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.all()
    serializer_class = SampleQcUploadShowSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post', 'delete']
    pagination_class = PageNumberOffsetPagination

    def list(self, request, *args, **kwargs):
        uuid = self.request.GET.get('uuid', '')
        query_list = list()
        if uuid:
            query_list.append(Q(uuid=uuid))
        queryset = self.queryset.filter(*query_list)
        queryset_values_list = self.paginate_queryset(queryset)
        serializer = self.serializer_class(queryset_values_list, many=True)
        return self.get_paginated_response(serializer.data)


class UploadFileDeleteViewSet(viewsets.ModelViewSet):
    queryset = UploadFile.objects.all()
    serializer_class = UploadFileDeleteSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post', 'delete']
    pagination_class = PageNumberOffsetPagination

    def list(self, request, *args, **kwargs):
        upload_id = self.request.GET.get('upload_id', '')
        data_type = self.request.GET.get('data_type', '')
        file_name = self.request.GET.get('file_name', '')
        file_names_list = file_name.split(',')  # 将逗号分隔的文件名字符串转为列表
        base_path = f'{settings.ANALYSE_BASE_DIR}/{upload_id}/{data_type}/fastqs'
        folder_path = os.path.join(base_path)

        # 检查文件夹是否存在
        if not os.path.exists(folder_path):
            return Response({'message': f"Folder {folder_path} does not exist.", 'upload_id': upload_id})

        deleted_files = []
        failed_files = []

        for file_name in file_names_list:
            file_path = os.path.join(folder_path, file_name)

            if os.path.exists(file_path):
                try:
                    os.remove(file_path)  # 删除文件
                    # 删除数据库中的对应记录
                    delete_query = self.queryset.filter(upload_id=upload_id, data_type=data_type, filename=file_name)
                    delete_query.delete()
                    deleted_files.append(file_name)
                except Exception as e:
                    failed_files.append({'file': file_name, 'error': str(e)})
            else:
                failed_files.append({'file': file_name, 'error': 'File does not exist'})

        # 返回删除结果
        if deleted_files:
            message = f"Deleted files: {', '.join(deleted_files)}"
        else:
            message = "No files were deleted."

        return Response({
            'message': message,
            'upload_id': upload_id,
            'failed_files': failed_files
        })


class AnalysisStepProgressViewSet(viewsets.ModelViewSet):
    queryset = AnalysisStep.objects.all()
    serializer_class = AnalysisStepProgressSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get', 'post', 'delete']
    pagination_class = PageNumberOffsetPagination

    def list(self, request, *args, **kwargs):
        uuid = self.request.GET.get('uuid', '')
        current_step = self.request.GET.get('current_step', '')
        source = self.request.GET.get('source', '')  # 标识一键生成的进度
        if source == 'sample_qc':
            progress = get_sqmple_qc_progress(uuid)
            # 如果进度大于 100%，则返回 99%
            if progress == 100:
                status_ = 'SUCCESS'
            elif progress == 0:
                status_ = 'FAILURE'
            else:
                status_ = 'Started'
            dic = {
                "uuid": uuid,
                "current_step": "sample_qc_one_step",
                "progress": progress if progress < 100 else 100,
                "status": status_
            }
            return Response(data=[dic], status=status.HTTP_200_OK)  # 最大100

        elif source == 'cell_ranger':
            progress = get_cell_ranger_progress(uuid)
            if progress == 100:
                status_ = 'SUCCESS'
            elif progress == 0:
                status_ = 'FAILURE'
            else:
                status_ = 'Started'
            dic = {
                "uuid": uuid,
                "current_step": "cell_ranger_one_step",
                "progress": progress if progress < 100 else 100,
                "status": status_
            }
            return Response(data=[dic], status=status.HTTP_200_OK)  # 最大100
        else:
            query_list = list()
            # 过滤条件
            if uuid:
                query_list.append(Q(analysis__uuid=uuid))  # 查询与 Analysis 相关的 uuid
            if current_step:
                query_list.append(Q(step_name=current_step))  # 查询与 Analysis 相关的 current_step

            # 查询符合条件的 AnalysisStep 对象
            queryset = self.queryset.filter(*query_list).select_related('task_result',
                                                                        'analysis').order_by(
                '-create_time')  # 关联查询 task_result 和 analysis
            # 获取第一个符合条件的 AnalysisStep 对象
            queryset_values_list = queryset[:1]  # 只获取第一个符合条件的对象
            # 获取第一个符合条件的 Analysis 对象，用于填充 context
            step_obj = None
            if queryset_values_list:
                step_obj = queryset_values_list[0].analysis  # 获取第一个 AnalysisStep 对应的 Analysis 对象

            # 构造 context 传递给序列化器
            context = {
                'current_step': current_step,
                'step_obj': step_obj,
                'uuid': uuid,
            }

            # 序列化
            serializer = self.serializer_class(queryset_values_list, many=True, context=context)
            # 返回直接的 Response 对象，不使用分页
            return Response(serializer.data)
