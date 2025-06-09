import os
import subprocess
import shutil
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django_celery_results.models import TaskResult

from django_server.apps.analysis.models import Analysis, AnalysisStep, DataProcessResult, ClusterResult, \
    AnnotationResult, SampleQcFilterResult, SampleQCFilterData, DataProcessAnalysis
from django_server.celery import app
import time
import pandas as pd
import scanpy as sc
from ... import settings
from django_server.utils.data_process import data_process
from django_server.utils.qc_filter import qc_filter
from ...utils.cell_type import get_cell_type
from ...utils.cluster import cluster_fun
from itertools import chain


# 测试 Celery 任务
@app.task(name='add_num')
def add_num(*args, **kwargs):
    time.sleep(20)
    x = kwargs.get('x', 0)
    y = kwargs.get('y', 0)
    return x + y


# 回调方法
@shared_task
def create_task_result_callback(task_id, analysis, step_name):
    """任务成功后的回调方法，记录 TaskResult 和 AnalysisStep"""
    task_result, _ = TaskResult.objects.get_or_create(task_id=task_id)
    AnalysisStep.objects.create(
        analysis=analysis,
        step_name=step_name,
        status='PENDING',
        task_result=task_result
    )


# 示例任务
@shared_task(name='cellranger')
def cellranger(*args, **kwargs):
    """
    执行 cellranger count 异步任务
    @count_cmd_path: 执行cellranger count命令的路径
    @transcriptome_dir_path: transcriptome存放的路径
    @step_name: 当前步骤名称
    @analysis_id: 当前分析ID
    """
    count_cmd_path = kwargs.get('count_cmd_path', None)
    transcriptome_dir_path = kwargs.get('transcriptome_dir_path', None)
    analysis_id = kwargs.get('analysis_id', None)
    analysis = Analysis.objects.filter(id=analysis_id).first()

    try:
        obj = Analysis.objects.filter(id=analysis_id).first()
        # 进行记录执行结果
        task_id = cellranger.request.id
        create_task_result_callback(task_id, obj, 'cell_ranger')
        # 必须是上传两组数据，分别存在 data1、data2
        for dir_name in ['data1', 'data2']:
            # 执行 cellranger count 的路径
            count_cmd_dir = f"{count_cmd_path}/{dir_name}"
            # 存放 fastqs 的路径
            fastqs_dir_name = f"{count_cmd_dir}/fastqs"
            # 执行命令
            count_cmd = f"cellranger count --id=outs --fastqs={fastqs_dir_name} --transcriptome={transcriptome_dir_path} --create-bam=false --nosecondary"
            # 先切换到执行命令的路径
            os.chdir(count_cmd_dir)
            result = subprocess.run(count_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # 如果没有执行成功抛出异常，抛出异常任务会失败并记录失败的原因
            if result.returncode != 0:
                raise Exception(result.stderr)

            # 执行完以后直接删除 fastqs 文件夹（防止占用存储）
            shutil.rmtree(fastqs_dir_name)
            # 成功之后更新到当前步骤
            if Analysis.objects.filter(id=analysis_id).exists():
                obj.current_step = 'sample_qc'
                obj.save()
            else:
                pass
        return 'Finished'
    except Exception as e:
        # 任务失败
        status = "Failure"
        print(f"Task failed with error: {str(e)}")
        analysis.current_step = 'cell_ranger'
        analysis.save()
        raise


@shared_task(name='sample_qc')
def sample_qc(*args, **kwargs):
    """
    执行 sample_qc  异步任务
    @count_cmd_path: 执行sample_qc命令的路径
    @analysis_id: 主表id 成功之后用来更新主表字段
    剩下8个参数为filter 的入参
    """
    count_cmd_path = kwargs.get('count_cmd_path', None)
    analysis_id = kwargs.get('analysis_id', None)
    uuid = kwargs.get('uuid', None)
    max_n_genes_by_counts = kwargs.get('max_n_genes_by_counts', 5500)
    min_n_genes_by_counts = kwargs.get('min_n_genes_by_counts', 0)
    max_total_counts = kwargs.get('max_total_counts', 0)
    min_total_counts = kwargs.get('min_total_counts', 0)
    max_pct_counts_mt = kwargs.get('max_pct_counts_mt', None)
    min_pct_counts_mt = kwargs.get('min_pct_counts_mt', None)
    max_pct_counts_pt = kwargs.get('max_pct_counts_pt', None)
    min_pct_counts_pt = kwargs.get('min_pct_counts_pt', None)
    try:
        # 准备一个列表来保存所有 dir_name 的 QC 结果
        all_qc_results = []
        stats_data = []  # 用来存储所有统计信息
        obj = Analysis.objects.filter(id=analysis_id).first()
        # 进行记录执行结果
        task_id = sample_qc.request.id
        create_task_result_callback(task_id, obj, 'sample_qc')
        # 准备一个列表来保存统计信息
        stats_data = []
        for dir_name in ['data1', 'data2']:
            # 执行 cellranger count 的路径
            count_cmd_dir = f"{count_cmd_path}/{dir_name}"
            # 存放 h5文件的地方
            filtered_dir_name = f"{count_cmd_dir}/outs/outs/filtered_feature_bc_matrix.h5"
            # 读取h5文件
            try:
                adata = sc.read_h5ad(filtered_dir_name)
            except Exception as e:
                adata = sc.read_10x_h5(filtered_dir_name)
            # sample qc处理格式
            qc_data = {
                'max_n_genes_by_counts': max_n_genes_by_counts,
                'min_n_genes_by_counts': min_n_genes_by_counts,
                'max_total_counts': max_total_counts,
                'min_total_counts': min_total_counts,
                'max_pct_counts_mt': max_pct_counts_mt,
                'min_pct_counts_mt': min_pct_counts_mt,
                'max_pct_counts_pt': max_pct_counts_pt,
                'min_pct_counts_pt': min_pct_counts_pt
            }
            qc_filter_adata = qc_filter(adata, **qc_data)
            # 统计细胞数量
            n_cells = qc_filter_adata.shape[0]
            # 统计基因数量
            n_genes = qc_filter_adata.shape[1]
            # 将统计信息添加到列表中
            # stats_data.append([n_cells, n_genes])
            save_csv_file = f'{count_cmd_dir}/outs/outs/qc_filter.csv'
            save_h5ad_file = f'{count_cmd_dir}/outs/outs/{dir_name}_qc_filter.h5ad'
            gene_cell_file = f'{count_cmd_dir}/outs/outs/{dir_name}_gene_cell.csv'
            qc_filter_adata.obs.to_csv(save_csv_file, index=False)
            # 保存这步的结果
            qc_filter_adata.write_h5ad(filename=save_h5ad_file)
            # 保存统计数据
            stats_df = pd.DataFrame([{'n_cells': n_cells, 'n_genes': n_genes}])
            stats_df.to_csv(gene_cell_file, index=False)
            # 成功之后记录到数据库中
            # 获取生成的csv
            qc_df = pd.read_csv(save_csv_file)
            # 读取统计的数据
            gene_cell_df = pd.read_csv(gene_cell_file)
            # 文件代理地址
            file_ps_path = f'/{uuid}/{dir_name}/outs/outs/{dir_name}_qc_filter.h5ad'
            # 提取所需的四列，并重命名为指定的键

            qc_filter_finally_data = {
                'nCount_RNA': qc_df['total_counts'].astype(int).tolist(),  # 转换为 int
                'nFeature_RNA': qc_df['n_genes_by_counts'].astype(int).tolist(),  # 转换为 int
                'percent_mt': qc_df['pct_counts_mt'].astype(int).tolist() if 'pct_counts_mt' in qc_df.columns else [],
                # 转换为 int
                'percent_pt': qc_df['pct_counts_pt'].astype(int).tolist() if 'pct_counts_pt' in qc_df.columns else [],
                # 转换为 int
                'n_cells': int(gene_cell_df['n_cells'].iloc[0]) if 'n_cells' in gene_cell_df.columns else 0,
                'n_genes': int(gene_cell_df['n_genes'].iloc[0]) if 'n_genes' in gene_cell_df.columns else 0,
                'h5ad_file_download': '{ip}cell_ranger{save_h5ad_file}'.format(
                    ip=settings.ANALYSIS_BASE_URL, save_h5ad_file=file_ps_path)
            }
            # 将 QC 数据添加到结果列表
            all_qc_results.append({
                'uuid': uuid,
                'data_type': dir_name,
                'result_data': qc_filter_finally_data
            })
            # 批量更新或创建数据库记录
        for qc_result in all_qc_results:
            SampleQcFilterResult.objects.update_or_create(
                uuid=qc_result['uuid'],
                data_type=qc_result['data_type'],
                defaults={'result_data': qc_result['result_data']}
            )
        else:
            pass

        # 成功之后更新到当前步骤
        if Analysis.objects.filter(id=analysis_id).exists():
            obj.current_step = 'data_process'
            obj.save()
        else:
            pass

        return 'Finished'

    except Exception as e:
        # 任务失败,步骤为成功的上一步
        print(f"Task failed with error: {str(e)}")
        raise


@shared_task(name='data_process_async')
def data_process_async(*args, **kwargs):
    """
    第三步
    执行 data process 异步任务
    @count_cmd_path: 执行数据文件路径 命令的路径
    @analysis_id: 主表id 成功之后用来更新主表字段
    """
    count_cmd_path = kwargs.get('count_cmd_path', None)
    analysis_id = kwargs.get('analysis_id', None)
    data1_sample_name = kwargs.get('data1_sample_name', None)
    data2_sample_name = kwargs.get('data2_sample_name', None)
    uuid = kwargs.get('uuid', None)
    # 7个入参
    min_mean = kwargs.get('min_mean', 0)
    max_mean = kwargs.get('max_mean', 0)
    min_disp = kwargs.get('min_disp', 0)
    n_jobs = kwargs.get('n_jobs', 0)
    max_value = kwargs.get('max_value', 0)
    n_neighbors = kwargs.get('n_neighbors', 0)
    n_pcs = kwargs.get('n_pcs', 0)
    try:
        obj = Analysis.objects.filter(id=analysis_id).first()
        # 进行记录执行结果
        task_id = data_process_async.request.id
        create_task_result_callback(task_id, obj, 'data_process')

        # 执行 读取h5的路径
        data1_h5ad_file_path = f'{count_cmd_path}/data1/outs/outs/data1_qc_filter.h5ad'
        data2_h5ad_file_path = f'{count_cmd_path}/data2/outs/outs/data2_qc_filter.h5ad'
        # data1 qc_filter 以后的数据
        adata1 = sc.read(data1_h5ad_file_path)
        # data2 qc_filter 以后的数据
        adata2 = sc.read(data2_h5ad_file_path)
        # sample_list 顺序是 data1的sample name、data2的sample name
        sample_list = [data1_sample_name, data2_sample_name]  # 这个是文件上传的时候选的sample name
        adata1.obs['sample'], adata2.obs['sample'] = sample_list[0], sample_list[1]
        adata = adata1.concatenate(adata2, batch_key='sample', batch_categories=sample_list)

        request_data = {
            "min_mean": min_mean,
            "max_mean": max_mean,
            "min_disp": min_disp,
            "n_jobs": n_jobs,
            "max_value": max_value,
            "n_neighbors": n_neighbors,
            "n_pcs": n_pcs,
        }
        adata = data_process(adata, **request_data)
        # 提取 umap 结果
        umap_data = pd.DataFrame(adata.obsm['X_umap'], columns=['UMAP1', 'UMAP2'])
        # 保存 umap 结果 保存到data1中
        dir_name = 'data1'
        count_cmd_dir = f"{count_cmd_path}/{dir_name}"
        save_csv_file = f'{count_cmd_dir}/outs/outs/data_process.csv'
        save_h5ad_file = f'{count_cmd_dir}/outs/outs/data_process.h5ad'
        umap_data.to_csv(save_csv_file, index=False)
        # 保存这步的结果
        adata.write_h5ad(filename=save_h5ad_file)
        # 写到数据库中
        if os.path.exists(save_csv_file):
            cell_type_df = pd.read_csv(save_csv_file, usecols=['UMAP1', 'UMAP2'])
            # 将 DataFrame 转换为列表的列表
            points_list = cell_type_df.values.tolist()
            # 写到数据库前 先清除旧数据 再使用 update_or_create 方法
            umap_result, created = DataProcessResult.objects.update_or_create(
                uuid=uuid,
                defaults={'result_data': points_list}  # 更新或创建记录
            )
        else:
            pass

        if Analysis.objects.filter(id=analysis_id).exists():
            obj.current_step = 'cluster'
            obj.save()
        else:
            pass
        return 'Finished'

    except Exception as e:
        print(f"Task failed with error: {str(e)}")
        raise


@shared_task(name='cluster_async')
def cluster_async(*args, **kwargs):
    """
    第四步
    执行 cluster 异步任务
    @count_cmd_path: 执行cluster命令的路径
    @analysis_id: 主表id 成功之后用来更新主表字段
    """
    count_cmd_path = kwargs.get('count_cmd_path', None)
    analysis_id = kwargs.get('analysis_id', None)
    species_name = kwargs.get('species_name', None)
    tissue = kwargs.get('tissue', None)
    resolution = kwargs.get('resolution', None)
    uuid = kwargs.get('uuid', None)

    try:
        obj = Analysis.objects.filter(id=analysis_id).first()
        # 进行记录执行结果
        task_id = cluster_async.request.id
        create_task_result_callback(task_id, obj, 'cluster')
        # 执行 读取h5的路径
        dir_name = 'data1'
        count_cmd_dir = f"{count_cmd_path}/{dir_name}"
        save_h5ad_file = f'{count_cmd_dir}/outs/outs/data_process.h5ad'
        # 通过 h5ad 读取 Anndata
        adata = sc.read(save_h5ad_file)
        # 调用cluster函数
        resolution_data = {
            'resolution': resolution
        }
        adata = cluster_fun(adata, **resolution_data)
        # 存储数据
        umap_data = pd.DataFrame(adata.obsm['X_umap'], columns=['UMAP1', 'UMAP2'])
        umap_data['cluster'] = adata.obs['cluster'].values
        sc.tl.rank_genes_groups(adata, 'cluster', method='wilcoxon')
        # 设置图片存放的路径
        sc.settings.figdir = f'{count_cmd_dir}/outs/outs/'
        # 设置文件存储的后缀
        sc.settings.file_format_figs = 'png'
        # 保存 heatmap 图片 名称为 heatmap.png
        sc.pl.rank_genes_groups_heatmap(adata, n_genes=5, groupby='cluster', show_gene_labels=True, show=False,
                                        save=True)
        # 保存 dotplot 图片 名称为 dotplot.png
        sc.pl.rank_genes_groups_dotplot(adata, n_genes=5, groupby='cluster', show=False, save=True)
        # 保存 tracksplot 图片 名称为 tracksplot.png
        sc.pl.rank_genes_groups_tracksplot(adata, n_genes=3, groupby='cluster', show=False, save=True)

        # 获取cluster的差异基因详细信息列表
        rank_genes_groups_data = sc.get.rank_genes_groups_df(adata, group=None, pval_cutoff=0.001)
        rank_genes_groups_data = rank_genes_groups_data[rank_genes_groups_data['logfoldchanges'].abs() > 0.5]
        # 获取每个cluster里面差异表达基因的列表，去重合并成list
        degs_list = pd.DataFrame(adata.uns['rank_genes_groups']['names']).drop_duplicates().values.tolist()
        degs_list = list(set(list(chain(*degs_list))))
        # 确保差异基因在adata.var_names中
        degs_list = [gene for gene in degs_list if gene in adata.var_names]
        # 新建一个dataframe用来存储结果数据
        mean_expression_df = pd.DataFrame()
        base_dir = f'{count_cmd_dir}/outs/outs/'
        # 调取目标cluster中的每一个聚类细胞，计算其平均值
        for cluster in adata.obs['cluster'].unique():
            cluster_cells = adata[adata.obs['cluster'] == cluster]
            cluster_mean_expression = cluster_cells[:, degs_list].X.mean(axis=0)
            mean_expression_df[cluster] = cluster_mean_expression
        # 计算完成之后添加index索引
        mean_expression_df.index = degs_list
        # 保存 mean_expression_df, mean_expression_df.csv 变成动态获取 cluster_to_celltype，二期有接口(/server_plant_marker/api/v1/get_cell_id_data/)
        mean_expression_df_csv_filename = os.path.join(base_dir, 'mean_expression_df.csv')
        mean_expression_df.to_csv(mean_expression_df_csv_filename)
        cluster_to_celltype = get_cell_type(mean_expression_df_csv_filename, species_name, tissue)
        # 生成 umap_data 的 cell_type 数据
        umap_data['cluster'] = umap_data['cluster'].astype(int)
        umap_data['cell_type'] = umap_data['cluster'].map(cluster_to_celltype)
        # 生成 rank_genes_groups_data 的 cell_type 数据
        rank_genes_groups_data['group'] = rank_genes_groups_data['group'].astype(int)
        rank_genes_groups_data['cell_type'] = rank_genes_groups_data['group'].map(cluster_to_celltype)

        # 存储数据
        cluster_csv_file = f'{count_cmd_dir}/outs/outs/cluster.csv'
        rank_genes_groups_data_file = f'{count_cmd_dir}/outs/outs/rank_genes_groups_data.csv'
        cluster_h5ad_file = f'{count_cmd_dir}/outs/outs/cluster.h5ad'
        umap_data.to_csv(cluster_csv_file, index=False)
        rank_genes_groups_data.to_csv(rank_genes_groups_data_file, index=False)
        adata.write_h5ad(filename=cluster_h5ad_file)
        # 数据库中写入结果
        # 写到数据库中
        if os.path.exists(cluster_csv_file):
            # 第四步
            clster_umap_data = pd.read_csv(cluster_csv_file, usecols=['UMAP1', 'UMAP2', 'cluster'])
            # 按 cluster 列进行分组
            clusters_data = clster_umap_data.groupby('cluster')

            cluster_umap_result = []
            for cluster_name, group_data in clusters_data:
                group_data = group_data[['UMAP1', 'UMAP2']]
                data = {
                    'name': str(cluster_name),  # 使用 cluster 名称
                    'data': group_data.to_dict('split').get('data', []),
                    'sort': int(cluster_name)  # 将 cluster 用作排序键
                }
                cluster_umap_result.append(data)
            # 按 sort 排序
            cluster_umap_result = sorted(cluster_umap_result, key=lambda x: x['sort'])
            # 写入数据库前先清除旧数据

            cluster_umap_result, created = ClusterResult.objects.update_or_create(
                uuid=uuid,
                defaults={'result_data': cluster_umap_result, 'resolution': resolution}  # 更新或创建记录
            )

            # 第五步 Cell Annotation
            annotation_umap_data = pd.read_csv(cluster_csv_file, usecols=['UMAP1', 'UMAP2', 'cluster', 'cell_type'])
            umap_type = 'cell_type'
            # 通过 cell_type 组成的 DataFrame
            annotation_umap_data['cluster_cell_type'] = annotation_umap_data['cluster'].map(str) + ':' + \
                                                        annotation_umap_data[umap_type].map(str)
            # 按 cluster 和 cell_type 分组，此时 group_name 是 (cluster, cell_type) 的元组
            # annotation_data = annotation_umap_data.groupby(['cluster', umap_type])
            annotation_data = annotation_umap_data.groupby([umap_type])
            data_list = []
            for group_name, group_data in annotation_data:
                # group_name 是一个元组，包含 cluster 和 cell_type
                # cluster_name = str(group_name[0])  # cluster 值
                cell_type_name = group_name[0]  # cell_type 值
                group_data = group_data[['UMAP1', 'UMAP2']]
                data = {
                    'name': cell_type_name,
                    'data': group_data.to_dict('split').get('data', []),
                    # 'sort': int(cluster_name)
                }
                data_list.append(data)
            # 按 sort 排序
            # data_list = sorted(data_list, key=lambda x: x['sort'])
            # 使用 update_or_create 方法
            # download csv
            download_csv_file = f'/{uuid}/{dir_name}/outs/outs/rank_genes_groups_data.csv'
            # svg图片地址
            svg_file_path = f'/{uuid}/{dir_name}/outs/outs'
            download_cluster_csv = f'{settings.ANALYSIS_BASE_URL}cell_ranger{download_csv_file}'
            heatmap_svg = f'{settings.ANALYSIS_BASE_URL}cell_ranger{svg_file_path}/heatmap.png'
            dotplot_svg = f'{settings.ANALYSIS_BASE_URL}cell_ranger{svg_file_path}/dotplot_.png'
            tracksplot_svg = f'{settings.ANALYSIS_BASE_URL}cell_ranger{svg_file_path}/tracksplot.png'

            umap_result, created = AnnotationResult.objects.update_or_create(
                uuid=uuid,
                defaults={'result_data': data_list,
                          "download_cluster_csv": download_cluster_csv,
                          "heatmap_svg": heatmap_svg,
                          "dotplot_svg": dotplot_svg,
                          "tracksplot_svg": tracksplot_svg,
                          }  # 更新或创建记录
            )
        else:
            pass
        if Analysis.objects.filter(id=analysis_id).exists():
            obj.current_step = 'cell_annotation'
            obj.save()
        else:
            pass
        return 'Finished'

    except Exception as e:
        print(f"Task failed with error: {str(e)}")
        raise
