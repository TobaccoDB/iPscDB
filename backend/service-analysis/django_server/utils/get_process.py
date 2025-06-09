from django.db.models import Q, Sum
from rest_framework.response import Response

from django_server.apps.analysis.models import AnalysisStepTimeSetting, AnalysisStep, Analysis
from datetime import datetime


def get_sqmple_qc_progress(uuid):
    '''qc一键生成进度查看'''
    # 获取总时间
    total_time = AnalysisStepTimeSetting.objects.filter(
        step_name__in=['sample_qc', 'data_process', 'cluster']
    ).aggregate(Sum('step_time'))
    total_time_sum = total_time.get('step_time__sum', 540)  # 获取
    # 获取当前分析步骤
    analysis = Analysis.objects.get(uuid=uuid)
    analysis_current_step = analysis.current_step
    print('analysis_current_step',analysis_current_step)
    if analysis_current_step == 'cell_annotation':  # 执行完成最后一步
        progress = 100
        return progress
    # 获取第一步（sample_qc）的任务开始时间
    first_step = AnalysisStep.objects.filter(analysis=analysis, step_name='sample_qc').first()

    task_result_time = first_step.task_result.date_created  # 获取任务的开始时间
    steps = ['sample_qc', 'data_process', 'cluster']
    # completed_steps_time = AnalysisStepTimeSetting.objects.filter(
    #     step_name__in=steps[:steps.index(analysis_current_step) + 1]
    # ).aggregate(Sum('step_time'))
    # accumulated_time = completed_steps_time.get('step_time__sum', 0)
    # 计算从第一步的任务开始到当前时间的时间差
    current_time = datetime.now()
    time_difference_seconds = (current_time - task_result_time).total_seconds()

    # 计算实际进度，使用时间差和总时间的比例
    # progress = (accumulated_time + time_difference_seconds) / total_time_sum * 100
    progress = (time_difference_seconds / total_time_sum) * 100

    # 检查任务是否失败
    step = AnalysisStep.objects.filter(analysis=analysis, step_name=analysis_current_step).first()
    if analysis_current_step in ['sample_qc', 'data_process', 'cluster']:
        if step and step.task_result and step.task_result.status == 'FAILURE':
            progress = 0  # 如果当前步骤失败，返回进度 0%
        if step and step.task_result and step.task_result.status == 'SUCCESS':
            progress = 100  # 如果当前步骤成功，返回进度 100%
    # 进度大于 100% 且状态不是 'SUCCESS' 或 'FAILURE'，返回 99%
    if progress > 100 and step.task_result.status not in ['SUCCESS', 'FAILURE']:
        progress = 99
    result = 1 if 0 < progress < 1 else round(progress)
    return round(min(result, 100))  # 最大100


def get_cell_ranger_progress(uuid):
    '''qc一键生成进度查看'''
   # total_time = AnalysisStepTimeSetting.objects.filter(step_name__in=['cell_ranger', 'sample_qc', 'data_process', 'cluster']).aggregate(Sum('step_time'))
    #total_time_sum = total_time.get('step_time__sum', 4140) 
    # 获取当前总时间
    total_time_sum=AnalysisStepTimeSetting.objects.get(step_name='cell_ranger').step_time
    # 获取当前分析步骤
    analysis = Analysis.objects.get(uuid=uuid)
    analysis_current_step = analysis.current_step
    if analysis_current_step == 'cell_annotation':  # 执行完成最后一步
        progress = 100
        return progress
    # 获取第一步（cell_ranger）的任务开始时间
    first_step = AnalysisStep.objects.filter(analysis=analysis, step_name='cell_ranger').first()

    task_result_time = first_step.task_result.date_created  # 获取任务的开始时间
    current_time = datetime.now()
    time_difference_seconds = (current_time - task_result_time).total_seconds()
    print('11111',time_difference_seconds)
    # 计算实际进度，使用时间差和总时间的比例
    progress = (time_difference_seconds / total_time_sum) * 100
    print('progress',progress)
    # 检查任务是否失败
    step = AnalysisStep.objects.filter(analysis=analysis, step_name=analysis_current_step).first()
    
    if analysis_current_step in ['cell_ranger', 'sample_qc', 'data_process', 'cluster']:
        if step and step.task_result.status == 'FAILURE':
            progress = 0  # 如果当前步骤失败，返回进度 0%
        if step and step.task_result.status == 'SUCCESS':
            progress = 100  # 如果当前步骤成功，返回进度 100%

    # 进度大于 100% 且状态不是 'SUCCESS' 或 'FAILURE'，返回 99%
    if progress > 100 and step.task_result.status not in ['SUCCESS', 'FAILURE']:
        progress = 99
    result = 1 if 0 < progress < 1 else round(progress)
    return round(min(result, 100))  # 最大100
