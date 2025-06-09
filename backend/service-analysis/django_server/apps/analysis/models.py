from django.db import models
from django.utils import timezone
import os
from django.core.files.storage import FileSystemStorage
from ... import settings
from django_celery_results.models import TaskResult


class CeleryTaskTest(models.Model):
    """
    测试 Celry 表
    """
    id = models.AutoField(primary_key=True)
    # UUID
    uuid = models.CharField(max_length=200, null=True, blank=True)
    # 数据详情
    detail = models.CharField(max_length=200, null=True, blank=True)
    # 状态 
    state = models.CharField(max_length=200, null=True, blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'celery_task_test'
        ordering = ('-create_time',)


class Analysis(models.Model):
    """
    # 数据分析主表
    """
    id = models.AutoField(primary_key=True)
    # UUID 分析的唯一表示 也是目录的唯一标识
    uuid = models.CharField(max_length=50, null=True, blank=True)
    # email 用户筛选标识
    email = models.CharField(max_length=100, null=True, blank=True)
    # email 用户筛选标识
    analysis_name = models.CharField(max_length=100, null=True, blank=True)
    # 物种名
    species_name = models.CharField(max_length=100, null=True, blank=True)
    # 转录组
    transcriptome = models.CharField(max_length=100, null=True, blank=True)
    # 状态
    status = models.CharField(max_length=50, null=True, blank=True)
    source = models.CharField(max_length=50, null=True, blank=True, default='cell_ranger')
    # 第三步data_process状态记录
    # data_process_status = models.CharField(max_length=50, null=True, blank=True)
    current_step = models.CharField(max_length=50, null=True, blank=True)  # 字段来记录当前成功步骤
    # qc 分两步  0默认是用户上传了文件但是没有提交data1和data2的生成 1:代表进行了data1和data2的生成但没有提交异步任务 2:代表有异步任务提交
    is_run_qc = models.IntegerField(default=0)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analysis'
        ordering = ('-create_time',)


class AnalysisRawData(models.Model):
    """
    # 第一步任务数据关联表
    """
    id = models.AutoField(primary_key=True)
    # analysis_uuid:Analysis主数据表的UUID
    analysis_uuid = models.CharField(max_length=50, null=True, blank=True)
    # task_uuid 异步任务的ID
    task_uuid = models.CharField(max_length=50, null=True, blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analysis_row_data'
        ordering = ('-create_time',)


class AnalysisStep(models.Model):
    '''分析步骤'''
    STEP_CHOICES = (
        ('cell_ranger', 'Cell Ranger'),
        ('sample_qc', 'Sample QC'),
        ('data_process', 'Data Process'),
        ('cluster', 'Cluster'),
        ('cell_annotation', 'Cell Annotation'),
    )

    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE, related_name='steps')
    step_name = models.CharField(max_length=50, choices=STEP_CHOICES)
    status = models.CharField(max_length=50, null=True, blank=True)
    task_result = models.ForeignKey(TaskResult, on_delete=models.SET_NULL, null=True, blank=True)
    # analysis_step = models.ForeignKey(AnalysisStepTimeSetting, on_delete=models.SET_NULL, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analysis_step'
        ordering = ('-create_time',)


# 自定义存储类，用于处理文件的存储路径
class ChunkedFileSystemStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        # 基础存储路径
        self.base_location = getattr(settings, 'ANALYSE_BASE_DIR', '/home/Data_analyse/')
        super().__init__(*args, **kwargs)

    def _get_upload_to(self, uuid_str, data_type, filename):
        # 生成完整的文件存储路径
        return os.path.join(self.base_location, uuid_str, data_type, 'fastqs', filename)

    def save(self, name, content, max_length=None):
        # 从实例中获取自定义参数
        uuid_str = getattr(self, 'custom_uuid_str', '')
        data_type = getattr(self, 'custom_data_type', '')
        # 生成新的存储路径
        new_name = self._get_upload_to(uuid_str, data_type, name)
        # 调用父类的保存方法将文件内容保存到新路径
        return super().save(new_name, content, max_length)

    def set_custom_params(self, uuid_str, data_type):
        # 设置自定义参数
        self.custom_uuid_str = uuid_str
        self.custom_data_type = data_type


# 使用自定义的存储类
chunked_storage = ChunkedFileSystemStorage()


class UploadSession(models.Model):
    # 管理大文件上传 用于跟踪每次上传的唯一 upload_id 和上传状态 (is_complete)。
    upload_id = models.CharField(max_length=255, unique=True)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'upload_session'


class ChunkedUpload(models.Model):
    # 用于存储每个文件分片的信息
    file = models.FileField(storage=chunked_storage)  # 指定自定义的存储类
    upload_id = models.CharField(max_length=255)
    data_type = models.CharField(max_length=50)  # 'data1' or 'data2'
    file_index = models.IntegerField()  # 0, 1, 2, 3 每组数据对应的索引
    chunk_number = models.IntegerField()
    total_chunks = models.IntegerField()
    filename = models.CharField(max_length=255)  # 存储文件名
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('upload_id', 'data_type', 'filename', 'chunk_number')
        db_table = 'chunked_upload'


class UploadFile(models.Model):
    # 用于存储每组数据的八个文件名：data1下面的R1 I1 R2 R2 以及data2下面的文件名
    upload_id = models.CharField(max_length=255)  # uuid
    data_type = models.CharField(max_length=50)  # 'data1' or 'data2'
    file_submit_name = models.CharField(max_length=100, null=True, blank=True)  # R1 I1 R2 R2 每组提交按钮对应的名字
    current_row = models.CharField(max_length=50, null=True, blank=True)  # 字段来记录当前第几行 first、second、third
    filename = models.CharField(max_length=255)  # 存储文件名
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'upload_file'


class SpeciesTranscriptome(models.Model):
    # 物种名
    species_name = models.CharField(max_length=100, null=True, blank=True)
    # 转录组
    transcriptome = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analysis_species_transcriptome'


class SampleQCFilterData(models.Model):
    # UUID 分析的唯一表示 也是目录的唯一标识
    uuid = models.CharField(max_length=50, null=True, blank=True)
    max_n_genes_by_counts = models.IntegerField(verbose_name='max_n_genes_by_counts', null=True, blank=True)
    min_n_genes_by_counts = models.IntegerField(verbose_name='min_n_genes_by_counts', null=True, blank=True)
    max_total_counts = models.IntegerField(verbose_name='max_total_counts', null=True, blank=True)
    min_total_counts = models.IntegerField(verbose_name='min_total_counts', null=True, blank=True)
    max_pct_counts_mt = models.IntegerField(verbose_name='max_pct_counts_mt', null=True, blank=True)
    min_pct_counts_mt = models.IntegerField(verbose_name='min_pct_counts_mt', null=True, blank=True)
    max_pct_counts_pt = models.IntegerField(verbose_name='max_pct_counts_pt', null=True, blank=True)
    min_pct_counts_pt = models.IntegerField(verbose_name='min_pct_counts_pt', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sample_qc_filter_data'


class SampleQcFilterResult(models.Model):
    # UUID 分析的唯一表示 也是目录的唯一标识
    uuid = models.CharField(max_length=50, null=True, blank=True)
    data_type = models.CharField(max_length=50, null=True, blank=True)
    result_data = models.JSONField(null=True, blank=True)  # 允许为空
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'qc_filter_data_result'


class DataProcessAnalysis(models.Model):
    # UUID 分析的唯一表示 也是目录的唯一标识
    uuid = models.CharField(max_length=50, null=True, blank=True)
    selection_method = models.CharField(verbose_name='选择方法', max_length=253, null=True, blank=True)
    min_mean = models.FloatField(verbose_name='min_mean', null=True, blank=True)
    max_mean = models.FloatField(verbose_name='max_mean', null=True, blank=True)
    min_disp = models.FloatField(verbose_name='min_disp', null=True, blank=True)
    n_jobs = models.FloatField(verbose_name='n_jobs', null=True, blank=True)
    max_value = models.FloatField(verbose_name='max_value', null=True, blank=True)
    n_neighbors = models.FloatField(verbose_name='n_neighbors', null=True, blank=True)
    n_pcs = models.FloatField(verbose_name='n_pcs', null=True, blank=True)
    nfeatures = models.IntegerField(verbose_name='nfeatures', null=True, blank=True)
    data1_sample_name = models.CharField(max_length=100, verbose_name='data1_sample_name', null=True, blank=True)
    data2_sample_name = models.CharField(max_length=100, verbose_name='data2_sample_name', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analysis_data_process'


class DataProcessResult(models.Model):
    # UUID 分析的唯一表示 也是目录的唯一标识
    uuid = models.CharField(max_length=50, null=True, blank=True)
    result_data = models.JSONField(null=True, blank=True)  # 允许为空
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'data_process_result'


class ClusterResult(models.Model):
    # UUID 分析的唯一表示 也是目录的唯一标识
    uuid = models.CharField(max_length=50, null=True, blank=True)
    resolution = models.FloatField(null=True, blank=True)
    result_data = models.JSONField(null=True, blank=True)  # 允许为空
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cluster_result'


class AnnotationResult(models.Model):
    # UUID 分析的唯一表示 也是目录的唯一标识
    uuid = models.CharField(max_length=50, null=True, blank=True)
    download_cluster_csv = models.CharField(max_length=253, null=True, blank=True)
    heatmap_svg = models.CharField(max_length=253, null=True, blank=True)
    dotplot_svg = models.CharField(max_length=253, null=True, blank=True)
    tracksplot_svg = models.CharField(max_length=253, null=True, blank=True)
    result_data = models.JSONField(null=True, blank=True)  # 允许为空
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'annotation_result'


class SampleQcPtMt(models.Model):
    # UUID 分析的唯一表示 也是目录的唯一标识
    uuid = models.CharField(max_length=50, null=True, blank=True)
    pt = models.CharField(max_length=50, null=True, blank=True)
    mt = models.CharField(max_length=50, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sample_qc_pt_mt'


class SampleQcDataTypeResult(models.Model):
    # UUID 分析的唯一表示 也是目录的唯一标识
    uuid = models.CharField(max_length=50, null=True, blank=True)
    result_data = models.JSONField(null=True, blank=True)  # 允许为空
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sample_qc_data_type_result'


class FromSampleUploadFile(models.Model):
    # 用于存储每组数据的八个文件名：data1下面的R1 I1 R2 R2 以及data2下面的文件名
    upload_id = models.CharField(max_length=255)  # uuid
    data_type = models.CharField(max_length=50)  # 'data1' or 'data2'
    file_source_name = models.CharField(max_length=100, null=True, blank=True)  # 显示初始名字
    file_name = models.CharField(max_length=100, null=True, blank=True)
    data1_sample_name = models.CharField(max_length=50, null=True, blank=True)
    data2_sample_name = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'from_sample_upload_file'


class AnalysisStepTimeSetting(models.Model):
    '''分析步骤时间设置表'''

    step_name = models.CharField(verbose_name='步骤名称', max_length=150, null=True, blank=True)
    step_time = models.IntegerField(verbose_name='每一步的时间(秒)', default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'analysis_step_time_setting'
