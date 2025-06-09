from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'analysis', views.AnalysisViewSet, basename='analysis')

# Celery 测试接口
router.register(r'celery_task_test', views.CeleryTaskTestViewSet, basename='celery_task_test')
# 创建提交数据-返回文件uuid
router.register(r'analysis_new_job', views.AnalysisNewJobViewSet, basename='analysis_new_job')
# 分片上传接口
router.register(r'analysis_file_upload', views.AnalysisFileUploadViewSet, basename='analysis_file_upload')
# Cell_ranger第一步生成文件下载接口

router.register(r'analysis_file_download', views.AnalysisFileDownloadViewSet, basename='analysis_file_download')
# 类别下拉框
router.register(r'specie_down_box', views.SpeciesDownBoxViewSet, basename='specie_down_box')
router.register(r'specie_tissue_down_box', views.SpeciesTissueDownBoxViewSet, basename='specie_tissue_down_box')
# Qcdata1，和data2的数据 展示
router.register(r'sqmple_qc_data_show', views.SampleQcDataShowViewSet, basename='sqmple_qc_data_show')
# 第二步filter的默认数据显示
router.register(r'qc_filter_data_show', views.QcFilterDatAShowViewSet, basename='qc_filter_data_show')
router.register(r'qc_filter_data_result', views.QcFilterDatAResultViewSet, basename='qc_filter_data_result')
# 第三步data_process的默认数据显示
router.register(r'data_process_show', views.DataProcessShowViewSet, basename='data_process_show')
# 第三步 data process 数据展示
router.register(r'data_process_result', views.DataProcessResultViewSet, basename='data_process_result')
# resolution 默认值显示
router.register(r'cluster_resolution', views.ClusterResolutionViewSet, basename='cluster_resolution')
# 第四步点图查看接口
router.register(r'cluster_result', views.ClusterResultViewSet, basename='cluster_result')
# 第五步点图查看结果
router.register(r'cell_annotation_result', views.CellAnnotationResultViewSet, basename='cell_annotation_result')
# 第五步列表查看接口
router.register(r'cluster_result_list', views.ClusterResultListViewSet, basename='cluster_result_list')
# sample qc pt mt 默认值显示
router.register(r'sample_qc_pt_mt', views.SampleQcPtMtViewSet, basename='sample_qc_pt_mt')
# sample qc gz或者h5 文件上传接口

router.register(r'sample_qc_upload', views.SampleQcUploadViewSet, basename='sample_qc_upload')
router.register(r'sample_qc_upload_show', views.SampleQcUploadShowViewSet, basename='sample_qc_upload_show')
router.register(r'upload_file_delete', views.UploadFileDeleteViewSet, basename='upload_file_delete')
#进度条任务查询
router.register(r'analysis_step_progress', views.AnalysisStepProgressViewSet, basename='analysis_step_progress')
