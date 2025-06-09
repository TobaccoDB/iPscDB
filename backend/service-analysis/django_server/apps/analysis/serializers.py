import os
import subprocess
import time

import uuid as uuid
from datetime import datetime
import pandas as pd
from django.db.models import Count
from rest_framework import serializers
from django.conf import settings

from .models import *
from .tasks import add_num, cellranger, sample_qc, data_process_async, cluster_async
from .models import ChunkedUpload
import uuid
from celery import chain
from ...utils.data_qc_filter import collect_data


class CeleryTaskTestSerializer(serializers.ModelSerializer):
    """
    # 测试异步任务序列化
    """
    x = serializers.IntegerField(write_only=True, required=True)
    y = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = CeleryTaskTest
        fields = ('x', 'y')

    def save(self):
        # 启动 celery 任务
        x = self.validated_data.get('x', 0)
        y = self.validated_data.get('y', 0)
        # 创建任务的时候需要指定队列
        result = add_num.apply_async(kwargs={
            'x': x,
            'y': y
        })
        print(result.task_id)
        print(result.status)


class CellrangerTestSerializer(serializers.ModelSerializer):
    """
    """

    uuid = serializers.CharField(write_only=True, required=True)
    species = serializers.CharField(write_only=True, required=True)
    transcriptome = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = AnalysisRawData
        fields = ('uuid', 'species', 'transcriptome')

    def save(self):

        uuid = self.validated_data.get('uuid', None)
        species = self.validated_data.get('species', None)
        transcriptome = self.validated_data.get('species', None)

        # cellranger count 命令存储路径
        count_cmd_path = f'{settings.ANALYSE_BASE_DIR}/{uuid}'
        # transcriptome 文件夹路径
        # transcriptome_dir_path = f'{settings.TRANSCRIPTOME_BASE_DIR}/{species}/{transcriptome}'
        transcriptome_dir_path = f'{settings.TRANSCRIPTOME_BASE_DIR}/Transcriptome/{species}'

        # 创建任务的时候需要指定队列
        for dir_name in ['data1', 'data2']:
            # 执行 cellranger count的路径
            count_cmd_dir = f"{count_cmd_path}/{dir_name}"
            # 存放 fastqs 的路径
            fastqs_dir_name = f"{count_cmd_dir}/fastqs"

            # 执行命令
            # count_cmd = f"cellranger count --id=outs --fastqs={fastqs_dir_name} --transcriptome={transcriptome_dir_path} --create-bam=false"
            count_cmd = f"cellranger count --id=outs --fastqs={fastqs_dir_name} --transcriptome={transcriptome_dir_path} --create-bam=false"
            # 先切换到执行命令的路径
            os.chdir(count_cmd_dir)
            # 执行 count_cmd 命令，并捕获其输出和错误信息，方便后续处理
            result = subprocess.run(count_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(result.stderr)


class AnalysisSerializer(serializers.ModelSerializer):
    '''列表'''
    create_time = serializers.SerializerMethodField()
    update_time = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()
    data1_sample_name = serializers.SerializerMethodField()
    data2_sample_name = serializers.SerializerMethodField()
    is_run_qc = serializers.SerializerMethodField()

    class Meta:
        model = Analysis
        fields = (
            'id', 'uuid', 'email', 'analysis_name', 'status', 'create_time', 'update_time', 'current_step',
            'species_name',
            'transcriptome', 'file_name', 'source', 'data1_sample_name', 'data2_sample_name', 'is_run_qc')

    def get_create_time(self, obj):
        if obj.create_time:
            # 使用 strftime 格式化时间为 YYYY-MM-DD HH:MM:SS
            create_time = obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            create_time = ''
        return create_time

    def get_update_time(self, obj):
        if obj.update_time:
            # 使用 strftime 格式化时间为 YYYY-MM-DD HH:MM:SS
            update_time = obj.update_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            update_time = ''
        return update_time

    def get_status(self, obj):
        # 获取与当前 Analysis 关联的 AnalysisStep
        analysis_step = AnalysisStep.objects.filter(analysis=obj).order_by('-create_time').first()
        if analysis_step and analysis_step.task_result:
            # 获取 TaskResult 的状态
            status = analysis_step.task_result.status
            if status == 'SUCCESS':
                return 'Finished'
            if status == 'FAILURE':
                return 'Failure'
            return analysis_step.task_result.status
        else:
            status = obj.status
        return status

    # 20250424
    def get_is_run_qc(self, obj):
        analysis_step = AnalysisStep.objects.filter(analysis=obj).order_by('-create_time').first()
        if analysis_step and analysis_step.task_result:
            # 获取 TaskResult 的状态
            status = analysis_step.task_result.status
            if status == 'SUCCESS':
                is_run_qc = 2
            else:
                is_run_qc = 1
            return is_run_qc
        else:
            return obj.is_run_qc

    def get_file_name(self, obj):
        # 获取与当前 Analysis 关联的 UploadFile，并根据 data_type, file_submit_name, current_row, filename 进行去重
        upload_files = UploadFile.objects.filter(upload_id=obj.uuid).values(
            'data_type', 'file_submit_name', 'current_row', 'filename'
        ).annotate(file_count=Count('id')).distinct()

        # 将每个去重后的结果转换为字典
        file_data = []
        for upload_file in upload_files:
            file_data.append({
                'data_type': upload_file['data_type'],
                'file_submit_name': upload_file['file_submit_name'],
                'current_row': upload_file['current_row'],
                'filename': upload_file['filename'],
            })

        return file_data

    def get_data1_sample_name(self, obj):
        try:
            obj_name = FromSampleUploadFile.objects.filter(upload_id=obj.uuid)
            if obj_name.exists():
                data1_sample_name = obj_name.exclude(data1_sample_name='').first().data1_sample_name
            else:
                data1_sample_name = ''
            return data1_sample_name
        except Exception as e:
            data1_sample_name = ''
            return data1_sample_name

    def get_data2_sample_name(self, obj):
        try:
            obj_name = FromSampleUploadFile.objects.filter(upload_id=obj.uuid)
            if obj_name.exists():
                data2_sample_name = obj_name.exclude(data2_sample_name='').first().data2_sample_name
            else:
                data2_sample_name = ''
            return data2_sample_name
        except Exception as e:
            data2_sample_name = ''
            return data2_sample_name


class AnalysisSimpleSerializer(serializers.ModelSerializer):
    '''列表'''
    create_time = serializers.SerializerMethodField()
    update_time = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    is_run_qc = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = Analysis
        fields = (
            'id', 'uuid', 'email', 'analysis_name', 'status', 'create_time', 'update_time', 'current_step',
            'species_name',
            'transcriptome', 'file_name', 'source', 'is_run_qc')

    def get_create_time(self, obj):
        if obj.create_time:
            # 使用 strftime 格式化时间为 YYYY-MM-DD HH:MM:SS
            create_time = obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            create_time = ''
        return create_time

    def get_update_time(self, obj):
        if obj.update_time:
            # 使用 strftime 格式化时间为 YYYY-MM-DD HH:MM:SS
            update_time = obj.update_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            update_time = ''
        return update_time

    def get_status(self, obj):
        # 获取与当前 Analysis 关联的 AnalysisStep
        analysis_step = AnalysisStep.objects.filter(analysis=obj).order_by('-create_time').first()
        if analysis_step and analysis_step.task_result:
            # 获取 TaskResult 的状态
            status = analysis_step.task_result.status
            if status == 'SUCCESS':
                return 'Finished'
            if status == 'FAILURE':
                return 'Failure'
            return analysis_step.task_result.status
        else:
            status = obj.status
        return status

    def get_is_run_qc(self, obj):
        analysis_step = AnalysisStep.objects.filter(analysis=obj).order_by('-create_time').first()
        if analysis_step and analysis_step.task_result:
            # 获取 TaskResult 的状态
            status = analysis_step.task_result.status
            if status == 'SUCCESS':
                is_run_qc = 2

            else:
                is_run_qc = obj.is_run_qc if obj.is_run_qc else 0
            return is_run_qc
        else:
            return obj.is_run_qc

    def get_file_name(self, obj):
        # 获取与当前 Analysis 关联的 UploadFile，并根据 data_type, file_submit_name, current_row, filename 进行去重
        upload_files = UploadFile.objects.filter(upload_id=obj.uuid).values(
            'data_type', 'file_submit_name', 'current_row', 'filename'
        ).annotate(file_count=Count('id')).distinct()

        # 将每个去重后的结果转换为字典
        file_data = []
        for upload_file in upload_files:
            file_data.append({
                'data_type': upload_file['data_type'],
                'file_submit_name': upload_file['file_submit_name'],
                'current_row': upload_file['current_row'],
                'filename': upload_file['filename'],
            })

        return file_data

    def get_email(self, obj):
        local, domain = str(obj.email).split('@')
        return f"xxxxx@{domain}"


class AnalysisDetailSerializer(serializers.ModelSerializer):
    '''详情'''
    create_time = serializers.SerializerMethodField()
    update_time = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()
    data1_sample_name = serializers.SerializerMethodField()
    data2_sample_name = serializers.SerializerMethodField()

    class Meta:
        model = Analysis
        fields = (
            'id', 'uuid', 'email', 'analysis_name', 'status', 'create_time', 'update_time', 'current_step',
            'species_name',
            'transcriptome', 'file_name', 'data1_sample_name', 'data2_sample_name')

    def get_create_time(self, obj):
        if obj.create_time:
            # 使用 strftime 格式化时间为 YYYY-MM-DD HH:MM:SS
            create_time = obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            create_time = ''
        return create_time

    def get_update_time(self, obj):
        if obj.update_time:
            # 使用 strftime 格式化时间为 YYYY-MM-DD HH:MM:SS
            update_time = obj.update_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            update_time = ''
        return update_time

    def get_status(self, obj):
        # 获取与当前 Analysis 关联的 AnalysisStep
        analysis_step = AnalysisStep.objects.filter(analysis=obj).order_by('-create_time').first()
        if analysis_step and analysis_step.task_result:
            # 获取 TaskResult 的状态
            # 获取 TaskResult 的状态
            status = analysis_step.task_result.status
            if status == 'SUCCESS':
                return 'Finished'
            if status == 'FAILURE':
                return 'Failure'
            return analysis_step.task_result.status
        return 'Started'

    def get_file_name(self, obj):
        # 获取与当前 Analysis 关联的 UploadFile，并根据 data_type, file_submit_name, current_row, filename 进行去重
        upload_files = UploadFile.objects.filter(upload_id=obj.uuid).values(
            'data_type', 'file_submit_name', 'current_row', 'filename'
        ).annotate(file_count=Count('id')).distinct()

        # 将每个去重后的结果转换为字典
        file_data = []
        for upload_file in upload_files:
            file_data.append({
                'data_type': upload_file['data_type'],
                'file_submit_name': upload_file['file_submit_name'],
                'current_row': upload_file['current_row'],
                'filename': upload_file['filename'],
            })

        return file_data

    def get_data1_sample_name(self, obj):
        obj_name = FromSampleUploadFile.objects.filter(upload_id=obj.uuid)
        if obj_name.exists():
            data1_sample_name = obj_name.exclude(data1_sample_name='').first().data1_sample_name
        else:
            data1_sample_name = ''
        return data1_sample_name

    def get_data2_sample_name(self, obj):
        obj_name = FromSampleUploadFile.objects.filter(upload_id=obj.uuid)
        if obj_name.exists():
            data2_sample_name = obj_name.exclude(data2_sample_name='').first().data2_sample_name
        else:
            data2_sample_name = ''
        return data2_sample_name


class CellrangerSerializer(serializers.ModelSerializer):
    """
    创建 第一步 RawData 数据
    """

    uuid = serializers.CharField(write_only=True, required=True)
    species_name = serializers.CharField(write_only=True, required=True)
    transcriptome = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Analysis
        fields = ('uuid', 'species_name', 'transcriptome')

    def save(self):
        uuid = self.validated_data.get('uuid', None)
        species_name = self.validated_data.get('species_name', None)
        transcriptome = self.validated_data.get('transcriptome', None)

        # cellranger count 命令存储路径
        count_cmd_path = f'{settings.ANALYSE_BASE_DIR}/{uuid}'
        # transcriptome 文件夹路径

        transcriptome_dir_path = f'{settings.TRANSCRIPTOME_BASE_DIR}/Transcriptome/{species_name}'
        analysis = Analysis.objects.filter(uuid=uuid).first()
        # 创建任务并指定队列
        result = cellranger.apply_async(kwargs={
            'count_cmd_path': count_cmd_path,
            'transcriptome_dir_path': transcriptome_dir_path,
            'step_name': 'cell_ranger',
            'analysis_id': analysis.id,
        }, queue="cellranger")

        return analysis


class SampleQCSerializer(serializers.ModelSerializer):
    """
    创建 第二步SampleQC
    """

    uuid = serializers.CharField(write_only=True, required=True)
    max_n_genes_by_counts = serializers.CharField(write_only=True, required=True)
    min_n_genes_by_counts = serializers.CharField(write_only=True, required=True)
    max_total_counts = serializers.CharField(write_only=True, required=True)
    min_total_counts = serializers.CharField(write_only=True, required=True)
    max_pct_counts_mt = serializers.CharField(write_only=True, required=False)
    min_pct_counts_mt = serializers.CharField(write_only=True, required=False)
    max_pct_counts_pt = serializers.CharField(write_only=True, required=False)
    min_pct_counts_pt = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Analysis
        fields = ('uuid',
                  'max_n_genes_by_counts',
                  'min_n_genes_by_counts',
                  'max_total_counts',
                  'min_total_counts',
                  'max_pct_counts_mt',
                  'min_pct_counts_mt',
                  'max_pct_counts_pt',
                  'min_pct_counts_pt',
                  )

    def save(self):
        uuid = self.validated_data.get('uuid', None)
        max_n_genes_by_counts = self.validated_data.get('max_n_genes_by_counts', None)
        min_n_genes_by_counts = self.validated_data.get('min_n_genes_by_counts', None)
        max_total_counts = self.validated_data.get('max_total_counts', None)
        min_total_counts = self.validated_data.get('min_total_counts', None)
        max_pct_counts_mt = self.validated_data.get('max_pct_counts_mt', None)
        min_pct_counts_mt = self.validated_data.get('min_pct_counts_mt', None)
        max_pct_counts_pt = self.validated_data.get('max_pct_counts_pt', None)
        min_pct_counts_pt = self.validated_data.get('min_pct_counts_pt', None)

        ## 第二步，通过查询，如果存在旧数据就清空 当前步骤以及后面的第三、四步和第五步的数据
        # 定义要查询的模型
        models_to_check = [SampleQcFilterResult, DataProcessResult, ClusterResult, AnnotationResult]
        # 循环处理每个模型
        for model in models_to_check:
            queryset = model.objects.filter(uuid=uuid)
            if queryset.exists():
                queryset.delete()
        # 记录filter提交参数
        filter_obj = SampleQCFilterData.objects.filter(uuid=uuid)
        if filter_obj.exists():
            # 如果存在该数据再次提交更新该条数据
            obj = filter_obj.first()
            obj.max_n_genes_by_counts = max_n_genes_by_counts
            obj.min_n_genes_by_counts = min_n_genes_by_counts
            obj.max_total_counts = max_total_counts
            obj.min_total_counts = min_total_counts
            obj.max_pct_counts_mt = max_pct_counts_mt
            obj.min_pct_counts_mt = min_pct_counts_mt
            obj.max_pct_counts_pt = max_pct_counts_pt
            obj.min_pct_counts_pt = min_pct_counts_pt
            obj.save()
        else:
            # 第一次提交则进行创建
            SampleQCFilterData.objects.create(uuid=uuid,
                                              max_n_genes_by_counts=max_n_genes_by_counts,
                                              min_n_genes_by_counts=min_n_genes_by_counts,
                                              max_total_counts=max_total_counts,
                                              min_total_counts=min_total_counts,
                                              max_pct_counts_mt=max_pct_counts_mt,
                                              min_pct_counts_mt=min_pct_counts_mt,
                                              max_pct_counts_pt=max_pct_counts_pt,
                                              min_pct_counts_pt=min_pct_counts_pt)
        # cellranger count 命令存储路径
        count_cmd_path = f'{settings.ANALYSE_BASE_DIR}/{uuid}'
        analysis = Analysis.objects.filter(uuid=uuid).first()
        # 创建任务
        data_dic = {
            'count_cmd_path': count_cmd_path,
            'step_name': 'sample_qc',
            'uuid': uuid,
            'analysis_id': analysis.id,
            'max_n_genes_by_counts': int(max_n_genes_by_counts),
            'min_n_genes_by_counts': int(min_n_genes_by_counts),
            'max_total_counts': int(max_total_counts),
            'min_total_counts': int(min_total_counts),
            # 'max_pct_counts_mt': int(max_pct_counts_mt) if max_pct_counts_mt else max_pct_counts_mt,
            # 'min_pct_counts_mt': int(min_pct_counts_mt) if min_pct_counts_mt else min_pct_counts_mt,
            # 'max_pct_counts_pt': int(max_pct_counts_pt) if max_pct_counts_pt else max_pct_counts_pt,
            # 'min_pct_counts_pt': int(min_pct_counts_pt) if min_pct_counts_pt else min_pct_counts_pt
        }
        if max_pct_counts_mt or max_pct_counts_mt == 0:
            data_dic['max_pct_counts_mt'] = int(max_pct_counts_mt)
        if min_pct_counts_mt or min_pct_counts_mt == 0:
            data_dic['min_pct_counts_mt'] = int(min_pct_counts_mt)
        if max_pct_counts_pt or max_pct_counts_pt == 0:
            data_dic['max_pct_counts_pt'] = int(max_pct_counts_pt)
        if min_pct_counts_pt or min_pct_counts_pt == 0:
            data_dic['min_pct_counts_pt'] = int(min_pct_counts_pt)

        result = sample_qc.apply_async(kwargs=data_dic)
        # 更新记录run qc跑了第几步
        Analysis.objects.update_or_create(uuid=uuid, defaults={'is_run_qc': 2})

        return {'task_id': result.task_id, 'status': 'Started'}


class DataProcessSerializer(serializers.ModelSerializer):
    """
    创建 第三步 data_process
    """

    uuid = serializers.CharField(write_only=True, required=True)
    min_mean = serializers.CharField(write_only=True, required=True)
    max_mean = serializers.CharField(write_only=True, required=True)
    min_disp = serializers.CharField(write_only=True, required=True)
    n_jobs = serializers.CharField(write_only=True, required=True)
    max_value = serializers.CharField(write_only=True, required=True)
    n_neighbors = serializers.CharField(write_only=True, required=True)
    n_pcs = serializers.CharField(write_only=True, required=True)
    data1_sample_name = serializers.CharField(write_only=True, required=True)
    nfeatures = serializers.CharField(write_only=True, required=False)
    selection_method = serializers.CharField(write_only=True, required=False)
    data2_sample_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Analysis
        fields = ('uuid',
                  'min_mean',
                  'max_mean',
                  'min_disp',
                  'n_jobs',
                  'max_value',
                  'n_neighbors',
                  'n_pcs',
                  'data1_sample_name',
                  'data2_sample_name',
                  'selection_method',
                  'nfeatures',
                  )

    def save(self):
        uuid = self.validated_data.get('uuid', None)
        min_mean = self.validated_data.get('min_mean', 0.0125)
        selection_method = self.validated_data.get('selection_method', 'vst')
        nfeatures = self.validated_data.get('nfeatures', 200)
        max_mean = self.validated_data.get('max_mean', 3)
        min_disp = self.validated_data.get('min_disp', 0.25)
        n_jobs = self.validated_data.get('n_jobs', 10)
        max_value = self.validated_data.get('max_value', 10)
        n_neighbors = self.validated_data.get('n_neighbors', 30)
        n_pcs = self.validated_data.get('n_pcs', 50)
        data1_sample_name = self.validated_data.get('data1_sample_name', None)
        data2_sample_name = self.validated_data.get('data2_sample_name', None)
        # 记录filter提交参数
        process_obj = DataProcessAnalysis.objects.filter(uuid=uuid)
        if process_obj.exists():
            # 如果存在该数据再次提交更新该条数据
            obj = process_obj.first()
            obj.min_mean = min_mean
            obj.max_mean = max_mean
            obj.min_disp = min_disp
            obj.n_jobs = n_jobs
            obj.max_value = max_value
            obj.n_neighbors = n_neighbors
            obj.n_pcs = n_pcs
            obj.selection_method = selection_method
            obj.nfeatures = nfeatures
            obj.data2_sample_name = data2_sample_name
            obj.data1_sample_name = data1_sample_name
            obj.save()
        else:
            # 第一次提交则进行创建
            DataProcessAnalysis.objects.create(uuid=uuid,
                                               min_mean=min_mean,
                                               max_mean=max_mean,
                                               min_disp=min_disp,
                                               n_jobs=n_jobs,
                                               max_value=max_value,
                                               n_neighbors=n_neighbors,
                                               n_pcs=n_pcs,
                                               selection_method=selection_method,
                                               nfeatures=nfeatures,
                                               data1_sample_name=data1_sample_name,
                                               data2_sample_name=data2_sample_name,
                                               )
        # 第三步，通过查询，如果存在旧数据就清空 当前步骤以及后面的第四步和第五步的数据
        # 定义要查询的模型
        models_to_check = [DataProcessResult, ClusterResult, AnnotationResult]
        # 循环处理每个模型
        for model in models_to_check:
            queryset = model.objects.filter(uuid=uuid)
            if queryset.exists():
                queryset.delete()
        # cellranger count 命令存储路径
        count_cmd_path = f'{settings.ANALYSE_BASE_DIR}/{uuid}'
        analysis = Analysis.objects.filter(uuid=uuid).first()
        # 创建任务
        result = data_process_async.apply_async(kwargs={
            'count_cmd_path': count_cmd_path,
            'analysis_id': analysis.id,
            'min_mean': float(min_mean),
            'max_mean': int(max_mean),
            'min_disp': float(min_disp),
            'n_jobs': int(n_jobs),
            'max_value': int(max_value),
            'n_neighbors': int(n_neighbors),
            'n_pcs': int(n_pcs),
            'data1_sample_name': data1_sample_name,
            'data2_sample_name': data2_sample_name,
            'uuid': uuid,
        })

        return result.status


class ClusterSerializer(serializers.ModelSerializer):
    """
    创建 第四步 cluster
    """

    uuid = serializers.CharField(write_only=True, required=True)
    resolution = serializers.CharField(write_only=True, required=True)
    species_name = serializers.CharField(write_only=True, required=True)
    tissue = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Analysis
        fields = ('uuid', 'resolution', 'species_name', 'tissue')

    def save(self):
        uuid = self.validated_data.get('uuid', None)
        resolution = self.validated_data.get('resolution', 0.2)
        species_name = self.validated_data.get('species_name', 'Arabidopsis_thaliana')
        tissue = self.validated_data.get('tissue', 'Root')
        # 第四步，通过查询，如果存在旧数据就清空 当前步骤以及后面的第五步的数据
        # 定义要查询的模型
        models_to_check = [ClusterResult, AnnotationResult]
        # 循环处理每个模型
        for model in models_to_check:
            queryset = model.objects.filter(uuid=uuid)
            if queryset.exists():
                queryset.delete()
        # 命令存储路径
        count_cmd_path = f'{settings.ANALYSE_BASE_DIR}/{uuid}'
        analysis = Analysis.objects.filter(uuid=uuid).first()
        # 创建任务
        result = cluster_async.apply_async(kwargs={
            'count_cmd_path': count_cmd_path,
            'species_name': species_name,
            'tissue': tissue,
            'analysis_id': analysis.id,
            'uuid': uuid,
            'resolution': float(resolution),
        })
        return result.status


class AnalysisNewJobSerializer(serializers.ModelSerializer):
    """
    创建 第一步 RawData 数据
    """
    email = serializers.CharField(write_only=True, required=True)
    analysis_name = serializers.CharField(write_only=True, required=False)
    source = serializers.CharField(write_only=True, required=False)
    uuid = serializers.CharField(read_only=True)  # 添加UUID为只读字段
    species_name = serializers.CharField(write_only=True, required=True)
    transcriptome = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Analysis
        fields = ('email', 'analysis_name', 'uuid', 'species_name', 'transcriptome', 'source')

    def save(self):
        email = self.validated_data.get('email', None)
        source = self.validated_data.get('source', 'cell_ranger')
        analysis_name = self.validated_data.get('analysis_name', None)
        species = self.validated_data.get('species_name', None)
        transcriptome = self.validated_data.get('transcriptome', None)

        # 创建 Analysis 实例
        uuid_str = str(uuid.uuid4())
        analysis = Analysis.objects.create(
            uuid=uuid_str,
            email=email,
            species_name=species,
            transcriptome=transcriptome,
            analysis_name=analysis_name,
            status="Failure",  # 初始状态设置为 PENDING
            current_step=source,  # 第一阶段默认设置为 'cell_ranger'
            source=source  # 标识来源是cell_ranger 还是sample_qc
        )
        return analysis.uuid


class ChunkedUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChunkedUpload
        fields = ('id', 'file', 'upload_id', 'chunk_number', 'total_chunks', 'created_at')


class SpeciesDownBoxSerializer(serializers.ModelSerializer):
    """
    物种名和转录组名下拉框
    """

    class Meta:
        model = SpeciesTranscriptome
        fields = ('species_name', 'transcriptome')


class QcFilterDatAShowSerializer(serializers.ModelSerializer):
    """
    filter数据显示
    """

    class Meta:
        model = SampleQCFilterData
        fields = ('uuid',
                  'max_n_genes_by_counts',
                  'min_n_genes_by_counts',
                  'max_total_counts',
                  'min_total_counts',
                  'max_pct_counts_mt',
                  'min_pct_counts_mt',
                  'max_pct_counts_pt',
                  'min_pct_counts_pt',
                  )


class DataProcessShowSerializer(serializers.ModelSerializer):
    """
    data process数据显示
    """

    class Meta:
        model = DataProcessAnalysis
        fields = ('uuid',
                  'min_mean',
                  'max_mean',
                  'min_disp',
                  'n_jobs',
                  'max_value',
                  'n_neighbors',
                  'n_pcs',
                  'data1_sample_name',
                  'data2_sample_name',
                  'nfeatures',
                  'selection_method',
                  )


class SampleQcFilterResultSerializer(serializers.ModelSerializer):
    """
    SampleQcFilterResult 数据显示
    """

    class Meta:
        model = SampleQcFilterResult
        fields = ('result_data',)


class DataProcessResultSerializer(serializers.ModelSerializer):
    """
    data process数据显示
    """

    class Meta:
        model = DataProcessResult
        fields = ('uuid', 'result_data')


class ClusterResultSerializer(serializers.ModelSerializer):
    """
    Cluster数据显示
    """

    class Meta:
        model = ClusterResult
        fields = ('uuid', 'result_data')


class ClusterResolutionSerializer(serializers.ModelSerializer):
    """
    Cluster resolution默认值数据显示
    """

    class Meta:
        model = ClusterResult
        fields = ('uuid', 'resolution')


class AnnotationResultSerializer(serializers.ModelSerializer):
    """
    Annotation数据显示
    """

    class Meta:
        model = AnnotationResult
        fields = ('uuid', 'result_data', 'download_cluster_csv', 'heatmap_svg', 'dotplot_svg', 'tracksplot_svg')


class SampleQcPtMtSerializer(serializers.ModelSerializer):
    """
    pt mt默认值数据显示
    """

    class Meta:
        model = SampleQcPtMt
        fields = ('pt', 'mt')


class SampleQcDataTypeResultSerializer(serializers.ModelSerializer):
    """
    qc的data1和data2表格数据显示
    """

    class Meta:
        model = SampleQcDataTypeResult
        fields = ('result_data',)


class SampleQcUploadShowSerializer(serializers.ModelSerializer):
    '''列表'''
    file_name = serializers.SerializerMethodField()
    data1_sample_name = serializers.SerializerMethodField()
    data2_sample_name = serializers.SerializerMethodField()
    pt = serializers.SerializerMethodField()
    mt = serializers.SerializerMethodField()
    data1_type = serializers.SerializerMethodField()
    data2_type = serializers.SerializerMethodField()

    class Meta:
        model = Analysis
        fields = (
            'id', 'uuid', 'file_name', 'data1_sample_name', 'data2_sample_name', 'pt', 'mt', 'data1_type',
            'data2_type',)

    def get_data1_sample_name(self, obj):
        fil_obj = FromSampleUploadFile.objects.filter(upload_id=obj.uuid, data_type='data1')
        if fil_obj.exists():
            data1_sample_name = fil_obj.first().data1_sample_name
        else:
            data1_sample_name = ''
        return data1_sample_name

    def get_data2_sample_name(self, obj):
        fil_obj = FromSampleUploadFile.objects.filter(upload_id=obj.uuid, data_type='data2')
        if fil_obj.exists():
            data2_sample_name = fil_obj.first().data2_sample_name
        else:
            data2_sample_name = ''
        return data2_sample_name

    def get_mt(self, obj):
        mt_obj = SampleQcPtMt.objects.filter(uuid=obj.uuid)
        if mt_obj.exists():
            mt = mt_obj.first().mt
        else:
            mt = ''
        return mt

    def get_pt(self, obj):
        pt_obj = SampleQcPtMt.objects.filter(uuid=obj.uuid)
        if pt_obj.exists():
            pt = pt_obj.first().pt
        else:
            pt = ''
        return pt

    def get_data1_type(self, obj):
        file_obj = FromSampleUploadFile.objects.filter(upload_id=obj.uuid, data_type='data1')
        if file_obj.exists():
            data1_type = 'gz' if file_obj.first().file_source_name.endswith('.gz') else 'h5'
        else:
            data1_type = ''
        return data1_type

    def get_data2_type(self, obj):
        file_obj = FromSampleUploadFile.objects.filter(upload_id=obj.uuid, data_type='data2')
        if file_obj.exists():
            data2_type = 'gz' if file_obj.first().file_source_name.endswith('.gz') else 'h5'
        else:
            data2_type = ''
        return data2_type

    def get_file_name(self, obj):
        # 获取与当前 Analysis 关联的 UploadFile，并根据 data_type, file_submit_name, current_row, filename 进行去重
        upload_files = FromSampleUploadFile.objects.filter(upload_id=obj.uuid).values(
            'data_type', 'file_source_name', 'file_name'
        ).annotate(file_count=Count('id')).distinct()

        # 将每个去重后的结果转换为字典
        file_data = []
        for upload_file in upload_files:
            file_data.append({
                'data_type': upload_file['data_type'],
                'file_source_name': upload_file['file_source_name'],
                'file_name': upload_file['file_name']
            })

        return file_data


class UploadFileDeleteSerializer(serializers.ModelSerializer):
    '''列表'''

    class Meta:
        model = UploadFile
        fields = (
            'id', 'upload_id', 'data_type', 'file_submit_name', 'current_row', 'filename',)


class AnalysisStepProgressSerializer(serializers.ModelSerializer):
    '''列表'''
    progress = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    current_step = serializers.SerializerMethodField()
    uuid = serializers.SerializerMethodField()

    class Meta:
        model = AnalysisStep
        fields = (
            'uuid', 'current_step', 'progress', 'status',)

    def get_current_step(self, obj):
        current_step = self.context.get('current_step', None)
        return current_step

    def get_uuid(self, obj):
        uuid = self.context.get('uuid', None)
        return uuid

    def get_progress(self, obj):
        current_step = self.context.get('current_step', None)
        step_obj = self.context.get('step_obj', None)

        # 获取最新的 AnalysisStep 并关联 TaskResult
        analysis_step = step_obj.steps.first()  # 已经预加载的步骤
        if analysis_step and analysis_step.task_result:
            task_result = analysis_step.task_result
            task_status = task_result.status

            # 如果任务状态是 SUCCESS，直接返回 100% 进度
            if task_status == 'SUCCESS':
                return 100
            # 如果任务状态是 FAILURE，直接返回 0% 进度
            if task_status == 'FAILURE':
                return 0
            try:
                # 获取对应步骤的时间设置
                step_time_setting = AnalysisStepTimeSetting.objects.get(step_name=current_step)
                step_time = step_time_setting.step_time
            except AnalysisStepTimeSetting.DoesNotExist:
                step_time = 120  # 如果没有找到对应的配置，则默认为 0 秒

            # 获取当前时间
            current_time = datetime.now()
            task_result_time = task_result.date_created

            # 计算时间差（秒）
            time_difference_seconds = (current_time - task_result_time).total_seconds()

            # 计算进度，考虑时间差减去步骤时间
            if step_time > 0:
                progress = (time_difference_seconds / step_time) * 100  # 计算实际进度
            else:
                progress = 0

            # 如果进度大于 100%，并且任务状态不是 'SUCCESS' 或 'FAILURE'，则返回 99%
            if progress > 100 and task_status not in ['SUCCESS', 'FAILURE']:
                return 99  # 返回 99%

            # 否则，正常返回进度
            return round(min(progress, 100))  # 最大100

        return 0  # 如果没有找到分析步骤或任务结果，返回 0% 进度

    def get_status(self, obj):
        step_obj = self.context.get('step_obj', None)
        # 获取与当前 Analysis 关联的最新 AnalysisStep 并返回 TaskResult 的状态
        analysis_step = step_obj.steps.first()  # 已经预加载的步骤
        if analysis_step and analysis_step.task_result:
            task_status = analysis_step.task_result.status
            if task_status == 'SUCCESS':
                return 'SUCCESS'
            return task_status  # 返回实际的任务状态（如 'PENDING', 'RUNNING', 等）

        return 'Started'  # 默认状态


class AnalysisFromCellrangerOneStepSerializer(serializers.ModelSerializer):
    """
    整合 SampleQC, DataProcess, Cluster 三个步骤的序列化器
    """
    # Cellranger的字段
    transcriptome = serializers.CharField(write_only=True, required=False)
    # SampleQC 的字段
    uuid = serializers.CharField(write_only=True, required=True)
    max_n_genes_by_counts = serializers.CharField(write_only=True, required=False)
    min_n_genes_by_counts = serializers.CharField(write_only=True, required=False)
    max_total_counts = serializers.CharField(write_only=True, required=False)
    min_total_counts = serializers.CharField(write_only=True, required=False)
    max_pct_counts_mt = serializers.CharField(write_only=True, required=False)
    min_pct_counts_mt = serializers.CharField(write_only=True, required=False)
    max_pct_counts_pt = serializers.CharField(write_only=True, required=False)
    min_pct_counts_pt = serializers.CharField(write_only=True, required=False)

    # DataProcess 的字段
    min_mean = serializers.CharField(write_only=True, required=False)
    max_mean = serializers.CharField(write_only=True, required=False)
    min_disp = serializers.CharField(write_only=True, required=False)
    n_jobs = serializers.CharField(write_only=True, required=False)
    max_value = serializers.CharField(write_only=True, required=False)
    n_neighbors = serializers.CharField(write_only=True, required=False)
    n_pcs = serializers.CharField(write_only=True, required=False)
    data1_sample_name = serializers.CharField(write_only=True, required=False)
    data2_sample_name = serializers.CharField(write_only=True, required=False)
    nfeatures = serializers.CharField(write_only=True, required=False)
    selection_method = serializers.CharField(write_only=True, required=False)

    # Cluster 的字段
    resolution = serializers.CharField(write_only=True, required=False)
    species_name = serializers.CharField(write_only=True, required=False)
    tissue = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Analysis
        fields = (
            # Cellranger的字段
            'uuid',
            'transcriptome',
            # SampleQC 的字段
            'max_n_genes_by_counts', 'min_n_genes_by_counts',
            'max_total_counts', 'min_total_counts', 'max_pct_counts_mt',
            'min_pct_counts_mt', 'max_pct_counts_pt', 'min_pct_counts_pt',
            # DataProcess 的字段
            'min_mean', 'max_mean', 'min_disp', 'n_jobs', 'max_value',
            'n_neighbors', 'n_pcs', 'data1_sample_name', 'data2_sample_name',
            'nfeatures', 'selection_method',
            # Cluster 的字段
            'resolution', 'species_name', 'tissue'
        )

    def save(self):
        uuid = self.validated_data.get('uuid', None)
        species_name = self.validated_data.get('species_name', None)
        transcriptome = self.validated_data.get('transcriptome', None)
        mt = 'ATCG' if species_name == 'Arabidopsis_thaliana' else ''
        pt = 'ATMG' if species_name == 'Arabidopsis_thaliana' else ''
        base_path = f'{settings.ANALYSE_BASE_DIR}/{uuid}'
        # 处理进度条问题 防止查询历史记录直接返回
        analysis = Analysis.objects.filter(uuid=uuid).first()
        species_name = analysis.species_name
        transcriptome = analysis.transcriptome
        analysis.current_step = 'cell_ranger'
        analysis.save()
        if analysis:
            AnalysisStep.objects.filter(analysis=analysis,
                                        step_name__in=['cell_ranger', 'sample_qc', 'data_process', 'cluster']).delete()

        request_data = {"mt": mt, "pt": pt, 'base_path': base_path}
        # 处理相关模型删除
        models_to_check = [SampleQcDataTypeResult, SampleQcFilterResult, DataProcessResult,
                           ClusterResult, AnnotationResult]
        for model in models_to_check:
            model.objects.filter(uuid=uuid).delete()

        # 更新或创建 SampleQcPtMt
        # SampleQcPtMt.objects.update_or_create(uuid=uuid, defaults={'mt': mt, 'pt': pt})
        SampleQcPtMt.objects.update_or_create(uuid=uuid, defaults={
            'mt': 'ATMG' if analysis.species_name == 'Arabidopsis_thaliana' else '',
            'pt': 'ATCG' if analysis.species_name == 'Arabidopsis_thaliana' else ''})
        all_data = collect_data(base_path, request_data)
        SampleQcDataTypeResult.objects.update_or_create(
            uuid=uuid,
            defaults={'result_data': all_data}
        )

        # 每个异步任务调用前的参数准备
        cell_ranger_data = self.process_cell_ranger(uuid)
        sample_qc_data = self.process_sample_qc(uuid, pt, mt)
        data_process_data = self.process_data_process(uuid)
        cluster_data = self.process_cluster(uuid)

        # 创建任务步骤记录
        cell_ranger_task = cellranger.s(**cell_ranger_data).set(queue="cellranger")  # 动态设置队列
        sample_qc_task = sample_qc.s(**sample_qc_data)
        data_process_task = data_process_async.s(**data_process_data)
        cluster_task = cluster_async.s(**cluster_data)
        # 创建任务链
        task_chain = chain(
            cell_ranger_task,
            sample_qc_task,
            data_process_task,
            cluster_task
        )
        task_chain.apply_async()

        return {"status": 200, 'message': 'All steps processed successfully'}

    def process_cell_ranger(self, uuid):
        # cellranger count 命令存储路径
        count_cmd_path = f'{settings.ANALYSE_BASE_DIR}/{uuid}'
        # transcriptome 文件夹路径
        analysis = Analysis.objects.filter(uuid=uuid).first()
        species_name = analysis.species_name
        transcriptome_dir_path = f'{settings.TRANSCRIPTOME_BASE_DIR}/Transcriptome/{species_name}'
        cell_ranger_data_dic = {
            'count_cmd_path': count_cmd_path,
            'transcriptome_dir_path': transcriptome_dir_path,
            'step_name': 'cell_ranger',
            'analysis_id': analysis.id,
        }
        return cell_ranger_data_dic

    def process_sample_qc(self, uuid, pt, mt):
        """处理 SampleQC 步骤"""
        if SampleQCFilterData.objects.filter(uuid=uuid).exists():
            sample_obj = SampleQCFilterData.objects.get(uuid=uuid)
            max_n_genes_by_counts = sample_obj.max_n_genes_by_counts
            min_n_genes_by_counts = sample_obj.min_n_genes_by_counts
            max_total_counts = sample_obj.max_total_counts
            min_total_counts = sample_obj.min_total_counts
            max_pct_counts_mt = sample_obj.max_pct_counts_mt if mt else None
            min_pct_counts_mt = sample_obj.min_pct_counts_mt if mt else None
            max_pct_counts_pt = sample_obj.max_pct_counts_pt if pt else None
            min_pct_counts_pt = sample_obj.min_pct_counts_pt if pt else None
        else:
            max_n_genes_by_counts = 5500
            min_n_genes_by_counts = 2000
            max_total_counts = 8000
            min_total_counts = 200
            max_pct_counts_mt = None
            min_pct_counts_mt = None
            max_pct_counts_pt = None
            min_pct_counts_pt = None
            SampleQCFilterData.objects.create(uuid=uuid,
                                              max_n_genes_by_counts=max_n_genes_by_counts,
                                              min_n_genes_by_counts=min_n_genes_by_counts,
                                              max_total_counts=max_total_counts,
                                              min_total_counts=min_total_counts,
                                              max_pct_counts_mt=max_pct_counts_mt,
                                              min_pct_counts_mt=min_pct_counts_mt,
                                              max_pct_counts_pt=max_pct_counts_pt,
                                              min_pct_counts_pt=min_pct_counts_pt)
        count_cmd_path = f'{settings.ANALYSE_BASE_DIR}/{uuid}'
        # 更新或创建 SampleQCFilterData
        SampleQCFilterData.objects.update_or_create(
            uuid=uuid,
            defaults={
                'max_n_genes_by_counts': max_n_genes_by_counts,
                'min_n_genes_by_counts': min_n_genes_by_counts,
                'max_total_counts': max_total_counts,
                'min_total_counts': min_total_counts,
                'max_pct_counts_mt': max_pct_counts_mt,
                'min_pct_counts_mt': min_pct_counts_mt,
                'max_pct_counts_pt': max_pct_counts_pt,
                'min_pct_counts_pt': min_pct_counts_pt,
            },
        )
        # 创建任务
        analysis = Analysis.objects.get(uuid=uuid)
        data_dic = {
            'count_cmd_path': count_cmd_path,
            'step_name': 'sample_qc',
            'uuid': uuid,
            'analysis_id': analysis.id,
            'max_n_genes_by_counts': int(max_n_genes_by_counts),
            'min_n_genes_by_counts': int(min_n_genes_by_counts),
            'max_total_counts': int(max_total_counts),
            'min_total_counts': int(min_total_counts),
            'max_pct_counts_mt': int(max_pct_counts_mt) if max_pct_counts_mt else max_pct_counts_mt,
        }
        if max_pct_counts_mt or max_pct_counts_mt == 0:
            data_dic['max_pct_counts_mt'] = int(max_pct_counts_mt)
        if min_pct_counts_mt or min_pct_counts_mt == 0:
            data_dic['min_pct_counts_mt'] = int(min_pct_counts_mt)
        if max_pct_counts_pt or max_pct_counts_pt == 0:
            data_dic['max_pct_counts_pt'] = int(max_pct_counts_pt)
        if min_pct_counts_pt or min_pct_counts_pt == 0:
            data_dic['min_pct_counts_pt'] = int(min_pct_counts_pt)
        return data_dic

    def process_data_process(self, uuid):
        """处理 DataProcess 步骤"""
        # 从 查询 中提取相关参数
        sample1_name_obj = FromSampleUploadFile.objects.filter(upload_id=uuid, data_type='data1').first()
        sample2_name_obj = FromSampleUploadFile.objects.filter(upload_id=uuid, data_type='data2').first()
        min_mean = 0.0125
        selection_method = 'vst'
        nfeatures = 200
        max_mean = 3
        min_disp = 0.25
        n_jobs = 10
        max_value = 10
        n_neighbors = 10
        n_pcs = 50
        data1_sample_name = sample1_name_obj.data1_sample_name if sample1_name_obj else ''
        data2_sample_name = sample2_name_obj.data2_sample_name if sample2_name_obj else ''
        analysis = Analysis.objects.get(uuid=uuid)
        # 更新或创建处理数据
        DataProcessAnalysis.objects.update_or_create(
            uuid=uuid,
            defaults={
                'min_mean': min_mean,
                'max_mean': max_mean,
                'min_disp': min_disp,
                'n_jobs': n_jobs,
                'max_value': max_value,
                'n_neighbors': n_neighbors,
                'n_pcs': n_pcs,
                'selection_method': selection_method,
                'nfeatures': nfeatures,
                'data1_sample_name': data1_sample_name,
                'data2_sample_name': data2_sample_name,
            }
        )

        # 执行异步任务
        data_process_dic = {
            'count_cmd_path': f'{settings.ANALYSE_BASE_DIR}/{uuid}',
            'analysis_id': analysis.id,
            'min_mean': float(min_mean),
            'max_mean': int(max_mean),
            'min_disp': float(min_disp),
            'n_jobs': int(n_jobs),
            'max_value': int(max_value),
            'n_neighbors': int(n_neighbors),
            'n_pcs': int(n_pcs),
            'data1_sample_name': data1_sample_name,
            'data2_sample_name': data2_sample_name,
            'uuid': uuid,
        }
        return data_process_dic

    def process_cluster(self, uuid):
        """处理 Cluster 步骤"""
        # 从 查询中提取相关参数
        analysis = Analysis.objects.get(uuid=uuid)
        species_name = analysis.species_name
        tissue = analysis.transcriptome
        cluster_dic = {
            'count_cmd_path': f'{settings.ANALYSE_BASE_DIR}/{uuid}',
            'resolution': 0.2,
            'uuid': uuid,
            'analysis_id': analysis.id,
            'species_name': species_name,
            'tissue': tissue,
        }
        return cluster_dic


class AnalysisFromSampleQCOneStepSerializer(serializers.ModelSerializer):
    """
    整合 SampleQC, DataProcess, Cluster 三个步骤的序列化器
    """

    # SampleQC 的字段
    uuid = serializers.CharField(write_only=True, required=True)
    max_n_genes_by_counts = serializers.CharField(write_only=True, required=False)
    min_n_genes_by_counts = serializers.CharField(write_only=True, required=False)
    max_total_counts = serializers.CharField(write_only=True, required=False)
    min_total_counts = serializers.CharField(write_only=True, required=False)
    max_pct_counts_mt = serializers.CharField(write_only=True, required=False)
    min_pct_counts_mt = serializers.CharField(write_only=True, required=False)
    max_pct_counts_pt = serializers.CharField(write_only=True, required=False)
    min_pct_counts_pt = serializers.CharField(write_only=True, required=False)

    # DataProcess 的字段
    min_mean = serializers.CharField(write_only=True, required=False)
    max_mean = serializers.CharField(write_only=True, required=False)
    min_disp = serializers.CharField(write_only=True, required=False)
    n_jobs = serializers.CharField(write_only=True, required=False)
    max_value = serializers.CharField(write_only=True, required=False)
    n_neighbors = serializers.CharField(write_only=True, required=False)
    n_pcs = serializers.CharField(write_only=True, required=False)
    data1_sample_name = serializers.CharField(write_only=True, required=False)
    data2_sample_name = serializers.CharField(write_only=True, required=False)
    nfeatures = serializers.CharField(write_only=True, required=False)
    selection_method = serializers.CharField(write_only=True, required=False)

    # Cluster 的字段
    resolution = serializers.CharField(write_only=True, required=False)
    species_name = serializers.CharField(write_only=True, required=False)
    tissue = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Analysis
        fields = (
            # SampleQC 的字段
            'uuid', 'max_n_genes_by_counts', 'min_n_genes_by_counts',
            'max_total_counts', 'min_total_counts', 'max_pct_counts_mt',
            'min_pct_counts_mt', 'max_pct_counts_pt', 'min_pct_counts_pt',
            # DataProcess 的字段
            'min_mean', 'max_mean', 'min_disp', 'n_jobs', 'max_value',
            'n_neighbors', 'n_pcs', 'data1_sample_name', 'data2_sample_name',
            'nfeatures', 'selection_method',
            # Cluster 的字段
            'resolution', 'species_name', 'tissue'
        )

    def save(self):
        uuid = self.validated_data.get('uuid')
        mt = self.validated_data.get('mt', '')
        pt = self.validated_data.get('pt', '')
        tag = self.validated_data.get('tag', 'run')
        base_path = f'{settings.ANALYSE_BASE_DIR}/{uuid}'

        # 锁定当前记录，减少锁范围，只锁定必要的记录
        request_data = {"mt": mt, "pt": pt, 'base_path': base_path}
        if tag == 'run':
            analysis = Analysis.objects.filter(uuid=uuid).first()
            analysis.current_step = 'sample_qc'
            analysis.save()
            if analysis:
                AnalysisStep.objects.filter(analysis=analysis,
                                            step_name__in=['sample_qc', 'data_process',
                                                           'cluster']).delete()
            # 处理相关模型删除
            models_to_check = [SampleQcDataTypeResult, SampleQcFilterResult, DataProcessResult,
                               ClusterResult, AnnotationResult]
            for model in models_to_check:
                model.objects.filter(uuid=uuid).delete()

            # 更新或创建 SampleQcPtMt
            # SampleQcPtMt.objects.update_or_create(uuid=uuid, defaults={'mt': mt, 'pt': pt})
            SampleQcPtMt.objects.update_or_create(uuid=uuid, defaults={
                'mt': 'ATMG' if analysis.species_name == 'Arabidopsis_thaliana' else '',
                'pt': 'ATCG' if analysis.species_name == 'Arabidopsis_thaliana' else ''})

            all_data = collect_data(base_path, request_data)
            SampleQcDataTypeResult.objects.update_or_create(
                uuid=uuid,
                defaults={'result_data': all_data}
            )

            # 每个异步任务调用前的参数准备
            sample_qc_data = self.process_sample_qc(uuid, pt, mt)
            data_process_data = self.process_data_process(uuid)
            cluster_data = self.process_cluster(uuid)

            # 创建任务步骤记录
            sample_qc_task = sample_qc.s(**sample_qc_data)
            data_process_task = data_process_async.s(**data_process_data)

            cluster_task = cluster_async.s(**cluster_data)
            # 创建任务链
            task_chain = chain(
                sample_qc_task,
                data_process_task,
                cluster_task
            )
            task_chain.apply_async()

        return {"status": 200, 'message': 'All steps processed successfully'}

    def process_sample_qc(self, uuid, pt, mt):

        """处理 SampleQC 步骤"""
        if SampleQCFilterData.objects.filter(uuid=uuid).exists():
            sample_obj = SampleQCFilterData.objects.get(uuid=uuid)
            max_n_genes_by_counts = sample_obj.max_n_genes_by_counts
            min_n_genes_by_counts = sample_obj.min_n_genes_by_counts
            max_total_counts = sample_obj.max_total_counts
            min_total_counts = sample_obj.min_total_counts
            max_pct_counts_mt = sample_obj.max_pct_counts_mt if mt else None
            min_pct_counts_mt = sample_obj.min_pct_counts_mt if mt else None
            max_pct_counts_pt = sample_obj.max_pct_counts_pt if pt else None
            min_pct_counts_pt = sample_obj.min_pct_counts_pt if pt else None
        else:
            max_n_genes_by_counts = 5500
            min_n_genes_by_counts = 2000
            max_total_counts = 8000
            min_total_counts = 200
            max_pct_counts_mt = None
            min_pct_counts_mt = None
            max_pct_counts_pt = None
            min_pct_counts_pt = None
            SampleQCFilterData.objects.create(uuid=uuid,
                                              max_n_genes_by_counts=max_n_genes_by_counts,
                                              min_n_genes_by_counts=min_n_genes_by_counts,
                                              max_total_counts=max_total_counts,
                                              min_total_counts=min_total_counts,
                                              max_pct_counts_mt=max_pct_counts_mt,
                                              min_pct_counts_mt=min_pct_counts_mt,
                                              max_pct_counts_pt=max_pct_counts_pt,
                                              min_pct_counts_pt=min_pct_counts_pt)

        count_cmd_path = f'{settings.ANALYSE_BASE_DIR}/{uuid}'
        # 更新或创建 SampleQCFilterData
        SampleQCFilterData.objects.update_or_create(
            uuid=uuid,
            defaults={
                'max_n_genes_by_counts': max_n_genes_by_counts,
                'min_n_genes_by_counts': min_n_genes_by_counts,
                'max_total_counts': max_total_counts,
                'min_total_counts': min_total_counts,
                'max_pct_counts_mt': max_pct_counts_mt,
                'min_pct_counts_mt': min_pct_counts_mt,
                'max_pct_counts_pt': max_pct_counts_pt,
                'min_pct_counts_pt': min_pct_counts_pt,
            },
        )
        # 创建任务
        analysis = Analysis.objects.get(uuid=uuid)
        data_dic = {
            'count_cmd_path': count_cmd_path,
            'step_name': 'sample_qc',
            'uuid': uuid,
            'analysis_id': analysis.id,
            'max_n_genes_by_counts': int(max_n_genes_by_counts),
            'min_n_genes_by_counts': int(min_n_genes_by_counts),
            'max_total_counts': int(max_total_counts),
            'min_total_counts': int(min_total_counts),
            'max_pct_counts_mt': int(max_pct_counts_mt) if max_pct_counts_mt else max_pct_counts_mt,
        }
        if max_pct_counts_mt or max_pct_counts_mt == 0:
            data_dic['max_pct_counts_mt'] = int(max_pct_counts_mt)
        if min_pct_counts_mt or min_pct_counts_mt == 0:
            data_dic['min_pct_counts_mt'] = int(min_pct_counts_mt)
        if max_pct_counts_pt or max_pct_counts_pt == 0:
            data_dic['max_pct_counts_pt'] = int(max_pct_counts_pt)
        if min_pct_counts_pt or min_pct_counts_pt == 0:
            data_dic['min_pct_counts_pt'] = int(min_pct_counts_pt)
        return data_dic

    def process_data_process(self, uuid):
        """处理 DataProcess 步骤"""
        # 从 查询 中提取相关参数
        sample1_name_obj = FromSampleUploadFile.objects.filter(upload_id=uuid, data_type='data1').first()
        sample2_name_obj = FromSampleUploadFile.objects.filter(upload_id=uuid, data_type='data2').first()
        min_mean = 0.0125
        selection_method = 'vst'
        nfeatures = 200
        max_mean = 3
        min_disp = 0.25
        n_jobs = 10
        max_value = 10
        n_neighbors = 10
        n_pcs = 50
        data1_sample_name = sample1_name_obj.data1_sample_name if sample1_name_obj else ''
        data2_sample_name = sample2_name_obj.data2_sample_name if sample2_name_obj else ''
        analysis = Analysis.objects.get(uuid=uuid)
        # 更新或创建处理数据
        DataProcessAnalysis.objects.update_or_create(
            uuid=uuid,
            defaults={
                'min_mean': min_mean,
                'max_mean': max_mean,
                'min_disp': min_disp,
                'n_jobs': n_jobs,
                'max_value': max_value,
                'n_neighbors': n_neighbors,
                'n_pcs': n_pcs,
                'selection_method': selection_method,
                'nfeatures': nfeatures,
                'data1_sample_name': data1_sample_name,
                'data2_sample_name': data2_sample_name,
            }
        )

        # 执行异步任务
        data_process_dic = {
            'count_cmd_path': f'{settings.ANALYSE_BASE_DIR}/{uuid}',
            'analysis_id': analysis.id,
            'min_mean': float(min_mean),
            'max_mean': int(max_mean),
            'min_disp': float(min_disp),
            'n_jobs': int(n_jobs),
            'max_value': int(max_value),
            'n_neighbors': int(n_neighbors),
            'n_pcs': int(n_pcs),
            'data1_sample_name': data1_sample_name,
            'data2_sample_name': data2_sample_name,
            'uuid': uuid,
        }
        return data_process_dic

    def process_cluster(self, uuid):
        """处理 Cluster 步骤"""
        # 从 查询中提取相关参数
        analysis = Analysis.objects.get(uuid=uuid)
        species_name = analysis.species_name
        tissue = analysis.transcriptome
        cluster_dic = {
            'count_cmd_path': f'{settings.ANALYSE_BASE_DIR}/{uuid}',
            'resolution': 0.2,
            'uuid': uuid,
            'analysis_id': analysis.id,
            'species_name': species_name,
            'tissue': tissue,
        }
        return cluster_dic
