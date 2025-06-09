from itertools import chain
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
from django.conf import settings
import uuid
from django.db.models import Q
from plant_marker.apps.plant_home.models import GeneInfo, CellMarkerInfo, ClusterMarkerInfo, MarkerGenesInfo

sns.set(style="whitegrid")


# 以下两句防止中文显示为窗格
# plt.rcParams["font.sans-serif"]=["SimHei"]
# plt.rcParams["axes.unicode_minus"] = False

def draw_violinplot(lit_id, project_id, gene_id, species_name):
    '''Project'''
    # 2023-06-06新增基因别名
    if species_name == 'Arabidopsis_thaliana':
        if GeneInfo.objects.filter(species=species_name).filter(
                Q(gene_symbol__icontains=gene_id) | Q(gene_id__icontains=gene_id)).exists():
            gene_id = GeneInfo.objects.filter(species=species_name).filter(
                Q(gene_symbol__icontains=gene_id) | Q(gene_id__icontains=gene_id)).first().gene_id
        else:
            gene_id = ''
    elif ClusterMarkerInfo.objects.filter(species_name=species_name).filter(Q(cluster_marker__icontains=gene_id) | Q(
            gene_id__icontains=gene_id)).exists() or CellMarkerInfo.objects.filter(species_name=species_name).filter(
        Q(gene_symbol__icontains=gene_id) | Q(gene_id__icontains=gene_id)).exclude(gene_symbol='').exists():
        gene_id_list = CellMarkerInfo.objects.filter(species_name=species_name).filter(
            Q(gene_symbol__icontains=gene_id) | Q(gene_id__icontains=gene_id)).exclude(gene_symbol='').values_list(
            'gene_id', flat=True)
        gene_id_list_3 = ClusterMarkerInfo.objects.filter(species_name=species_name).filter(
            cluster_marker__icontains=gene_id).exclude(cluster_marker='').values_list('gene_id', flat=True)
        gene_id = list(set(chain(gene_id_list, gene_id_list_3)))[0]
    else:
        gene_id = ''
    # 导入数据，从excel中
    file_name = '{}/{}_{}/expression_data'.format(species_name, lit_id, project_id)
    # # 读取物种对应的文件
    file_path = os.path.join(
        settings.CELL_EXPRESSION_DIR, "{file_name}/{gene_id}.csv".format(file_name=file_name, gene_id=gene_id))
    df = pd.read_csv(file_path)
    uuid_str = str(uuid.uuid4())
    # 绘制小提琴图
    # 设置窗口的大小
    f, ax = plt.subplots(figsize=(16, 9), tight_layout=True)
    # 设置轴显示的范围
    ax.set(ylim=(df["value"].min(), df['value'].max()))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=14)
    # 去除上下左右的边框（默认该函数会取出右上的边框）
    sns.despine(right=True, top=True)
    # vio = sns.violinplot(data=df, x=df["Clusters"], y=df["value"], palette="Set3")
    vio = sns.violinplot(data=df, x=df["Cell_type"], y=df["value"], palette="Set3", scale='width',
                         inner=None)  # Cell_type
    # 设置图片标题
    # vio.set_title('violinplot', fontsize=30)
    plt.xlabel('')
    save_path = os.path.join(
        settings.CELL_EXPRESSION_DIR, "{file_name}".format(file_name='violinplot_png'))
    save_violinplot_png = '{save_path}/{uuid_str}_violinplot.png'.format(save_path=save_path, uuid_str=uuid_str)
    plt.savefig(save_violinplot_png)
    plt.close()
    # 绘制箱型图
    # 设置窗口的大小
    f, ax = plt.subplots(figsize=(16, 9), tight_layout=True)
    # 设置轴显示的范围
    ax.set(ylim=(df["value"].min(), df['value'].max()))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=14)
    # 去除上下左右的边框（默认该函数会取出右上的边框）
    sns.despine(right=True, top=True)
    # box = sns.boxplot(data=df, x=df["Clusters"], y=df["value"], palette="Set3")
    box = sns.boxplot(data=df, x=df["Cell_type"], y=df["value"], palette="Set3")
    # 设置图片标题
    # box.set_title('boxplot', fontsize=30)
    # 保存
    plt.xlabel('')
    save_boxplot_png = '{save_path}/{uuid_str}_boxplot.png'.format(save_path=save_path, uuid_str=uuid_str)
    plt.savefig(save_boxplot_png)
    plt.close()

    return uuid_str + "_" + 'violinplot.png', uuid_str + "_" + 'boxplot.png'


#  Cell_ID格式化
def cell_id_format(x):
    x = x.replace('@', '.')
    return x


def draw_atlas_violinplot(species_name, tissue, type, gene_id, view_type):
    '''Atlas'''

    # 导入数据，从excel中
    file_name = 'umap/{}/{}/expression_data'.format(species_name, tissue)
    umap_tsne_path = os.path.join(settings.ATLAS_HOT_PNG_DIR,"umap/{}/{}/{}.csv".format(species_name, tissue, type))

    # 读取物种对应的文件
    file_path = os.path.join(settings.ATLAS_HOT_PNG_DIR, "{}/{}.csv".format(file_name, gene_id))
    try:
        umap_tsne_df = pd.read_csv(umap_tsne_path)
        umap_tsne_df['Cell_ID'] = umap_tsne_df['Cell_ID'].apply(cell_id_format)
        if os.path.exists(file_path):
            gene_df = pd.read_csv(file_path)
            gene_df['Cell_ID'] = gene_df['Cell_ID'].apply(cell_id_format)
        else:
            print("基因CSV文件不存在时创建空白的DataFrame")
            gene_df = pd.DataFrame({'Cell_ID': [], 'value': []})

        df = pd.merge(umap_tsne_df, gene_df, how='left', on='Cell_ID').fillna(0)
        uuid_str = str(uuid.uuid4())
        # 绘制小提琴图
        # 设置窗口的大小
        f, ax = plt.subplots(figsize=(10, 9), tight_layout=True)
        # 设置轴显示的范围
        ax.set(ylim=(df["value"].min(), df['value'].max()))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=14)
        # 去除上下左右的边框（默认该函数会取出右上的边框）
        sns.despine(right=True, top=True)
        # vio = sns.violinplot(data=df, x=df["Cell_type"], y=df["value"], palette="Set3", scale='width',
        vio = sns.violinplot(data=df, x=df[view_type], y=df["value"], palette="Set3", scale='width',
                             inner=None)  # Cell_type
        plt.xlabel('')
        # 设置图片标题
        # vio.set_title('violinplot', fontsize=30)
        save_path = os.path.join(
            settings.ATLAS_HOT_PNG_DIR, "{file_name}".format(file_name='violinplot_png'))
        save_violinplot_png = '{save_path}/{uuid_str}_violinplot.png'.format(save_path=save_path, uuid_str=uuid_str)
        plt.savefig(save_violinplot_png)
        plt.close()
        # 绘制箱型图
        # 设置窗口的大小
        f, ax = plt.subplots(figsize=(10, 9), tight_layout=True)
        # 设置轴显示的范围
        ax.set(ylim=(df["value"].min(), df['value'].max()))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=14)
        # 去除上下左右的边框（默认该函数会取出右上的边框）
        sns.despine(right=True, top=True)
        # box = sns.boxplot(data=df, x=df["Clusters"], y=df["value"], palette="Set3")
        box = sns.boxplot(data=df, x=df[view_type], y=df["value"], palette="Set3")
        # 设置图片标题
        # box.set_title('boxplot', fontsize=30)
        plt.xlabel('')
        # 保存
        save_boxplot_png = '{save_path}/{uuid_str}_boxplot.png'.format(save_path=save_path, uuid_str=uuid_str)
        plt.savefig(save_boxplot_png)
        plt.close()
        return uuid_str + "_" + 'violinplot.png', uuid_str + "_" + 'boxplot.png'
    except Exception as e:
        print(e)
        return '', ''


def draw_atlas_cell_violinplot(species_name, tissue, gene_id):
    '''Atlas'''
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
            file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0] if os.path.splitext(
                os.path.basename(file_path)) else ''
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
            file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0] if os.path.splitext(
                os.path.basename(file_path)) else ''
            # 根据输入的参数动态返回文件名
            matched_files.append(file_name_without_extension)
        gene_id_list = list(set(matched_files))
        gene_id = list(set(chain(gene_id_list, gene_id_)))[0]
    # 导入数据，从excel中
    file_name = 'umap/{}/{}/expression_data'.format(species_name, tissue)
    # # 读取物种对应的文件
    file_path = os.path.join(settings.ATLAS_HOT_PNG_DIR,
                             "{file_name}/{gene_id}.csv".format(file_name=file_name, gene_id=gene_id))
    tissue_name = 'umap/{}/'.format(species_name)
    species_file = os.path.join(settings.ATLAS_HOT_PNG_DIR,
                                "{file_name}/{tissue}/umap_data.csv".format(file_name=tissue_name, tissue=tissue))
    try:
        if os.path.exists(file_path):
            umap_tsne_df = pd.read_csv(file_path)
            gene_df = pd.read_csv(species_file)
            df = pd.merge(umap_tsne_df, gene_df, how='left', on='Cell_ID').fillna(0)
            uuid_str = str(uuid.uuid4())
            # 绘制小提琴图
            # 设置窗口的大小
            f, ax = plt.subplots(figsize=(8, 9), tight_layout=True)
            # 设置轴显示的范围
            ax.set(ylim=(df["value"].min(), df['value'].max()))
            ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=18)
            # 去除上下左右的边框（默认该函数会取出右上的边框）
            sns.despine(right=True, top=True)

            vio = sns.violinplot(data=df, x=df["Cell_type"], y=df["value"], palette="Set3", scale='width',
                                 inner=None)  # Cell_type
            # 设置图片标题
            # vio.set_title('violinplot', fontsize=30)
            plt.xlabel('')
            save_path = os.path.join(
                settings.ATLAS_HOT_PNG_DIR, "{file_name}".format(file_name='violinplot_png'))
            save_violinplot_png = '{save_path}/{uuid_str}_violinplot.png'.format(save_path=save_path, uuid_str=uuid_str)
            plt.savefig(save_violinplot_png)
            plt.close()
            # 绘制箱型图
            # 设置窗口的大小
            f, ax = plt.subplots(figsize=(8, 9), tight_layout=True)
            # 设置轴显示的范围
            ax.set(ylim=(df["value"].min(), df['value'].max()))
            ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=18)
            # 去除上下左右的边框（默认该函数会取出右上的边框）
            sns.despine(right=True, top=True)
            # box = sns.boxplot(data=df, x=df["Clusters"], y=df["value"], palette="Set3")
            box = sns.boxplot(data=df, x=df["Cell_type"], y=df["value"], palette="Set3")
            # 设置图片标题
            # box.set_title('boxplot', fontsize=30)
            # 保存
            plt.xlabel('')
            save_boxplot_png = '{save_path}/{uuid_str}_boxplot.png'.format(save_path=save_path, uuid_str=uuid_str)
            plt.savefig(save_boxplot_png)
            plt.close()
            return uuid_str + "_" + 'violinplot.png', uuid_str + "_" + 'boxplot.png'
        else:
            df = pd.read_csv(species_file)
            df["value_min"] = 0
            df["value_max"] = 6
            uuid_str = str(uuid.uuid4())
            # 绘制小提琴图
            # 设置窗口的大小
            f, ax = plt.subplots(figsize=(8, 9), tight_layout=True)
            # 设置轴显示的范围
            ax.set(ylim=(df["value_min"].min(), df['value_max'].max()))
            ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=18)
            # 去除上下左右的边框（默认该函数会取出右上的边框）
            sns.despine(right=True, top=True)
            vio = sns.violinplot(data=df, x=df["Cell_type"], y=df["value_max"], palette="Set3", scale='width',
                                 inner=None)
            plt.xlabel('')
            save_path = os.path.join(
                settings.ATLAS_HOT_PNG_DIR, "{file_name}".format(file_name='violinplot_png'))
            save_violinplot_png = '{save_path}/{uuid_str}_violinplot.png'.format(save_path=save_path, uuid_str=uuid_str)

            plt.savefig(save_violinplot_png)
            # plt.close()
            # 绘制箱型图
            # 设置窗口的大小

            f, ax = plt.subplots(figsize=(8, 9), tight_layout=True)
            # 设置轴显示的范围
            ax.set(ylim=(0, 1))
            ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=18)
            # 去除上下左右的边框（默认该函数会取出右上的边框）
            sns.despine(right=True, top=True)

            box = sns.boxplot(data=df, x=df["Cell_type"], y=df["value_max"], palette="Set3")
            plt.xlabel('')
            save_boxplot_png = '{save_path}/{uuid_str}_boxplot.png'.format(save_path=save_path, uuid_str=uuid_str)
            plt.savefig(save_boxplot_png)
            plt.close()
            return uuid_str + "_" + 'violinplot.png', uuid_str + "_" + 'boxplot.png'
    except Exception as e:
        print(e)
        return '', ''


def draw_atlas_cell_violinplot_new(species_name, tissue, gene_id):
    '''Atlas'''
    # 导入数据，从excel中
    file_name = 'umap/{}/{}/expression_data'.format(species_name, tissue)
    # # 读取物种对应的文件
    file_path = os.path.join(settings.ATLAS_HOT_PNG_DIR,
                             "{file_name}/{gene_id}.csv".format(file_name=file_name, gene_id=gene_id))
    tissue_name = 'umap/{}/'.format(species_name)
    species_file = os.path.join(settings.ATLAS_HOT_PNG_DIR,
                                "{file_name}/{tissue}/umap_data.csv".format(file_name=tissue_name, tissue=tissue))
    try:
        if os.path.exists(file_path):
            umap_tsne_df = pd.read_csv(file_path)
            gene_df = pd.read_csv(species_file)
            df = pd.merge(umap_tsne_df, gene_df, how='left', on='Cell_ID').fillna(0)
            uuid_str = str(uuid.uuid4())
            # 绘制小提琴图
            # 设置窗口的大小
            f, ax = plt.subplots(figsize=(8, 9), tight_layout=True)
            # 设置轴显示的范围
            ax.set(ylim=(df["value"].min(), df['value'].max()))
            ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=18)
            # 去除上下左右的边框（默认该函数会取出右上的边框）
            sns.despine(right=True, top=True)

            vio = sns.violinplot(data=df, x=df["Cell_type"], y=df["value"], palette="Set3", scale='width',
                                 inner=None)  # Cell_type
            # 设置图片标题
            # vio.set_title('violinplot', fontsize=30)
            plt.xlabel('')
            save_path = os.path.join(
                settings.ATLAS_HOT_PNG_DIR, "{file_name}".format(file_name='violinplot_png'))
            save_violinplot_png = '{save_path}/{uuid_str}_violinplot.png'.format(save_path=save_path, uuid_str=uuid_str)
            plt.savefig(save_violinplot_png)
            plt.close()
            # 绘制箱型图
            # 设置窗口的大小
            f, ax = plt.subplots(figsize=(8, 9), tight_layout=True)
            # 设置轴显示的范围
            ax.set(ylim=(df["value"].min(), df['value'].max()))
            ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=18)
            # 去除上下左右的边框（默认该函数会取出右上的边框）
            sns.despine(right=True, top=True)
            # box = sns.boxplot(data=df, x=df["Clusters"], y=df["value"], palette="Set3")
            box = sns.boxplot(data=df, x=df["Cell_type"], y=df["value"], palette="Set3")
            # 设置图片标题
            # box.set_title('boxplot', fontsize=30)
            # 保存
            plt.xlabel('')
            save_boxplot_png = '{save_path}/{uuid_str}_boxplot.png'.format(save_path=save_path, uuid_str=uuid_str)
            plt.savefig(save_boxplot_png)
            plt.close()
            return uuid_str + "_" + 'violinplot.png', uuid_str + "_" + 'boxplot.png'
        else:
            df = pd.read_csv(species_file)
            df["value_min"] = 0
            df["value_max"] = 6
            uuid_str = str(uuid.uuid4())
            # 绘制小提琴图
            # 设置窗口的大小
            f, ax = plt.subplots(figsize=(8, 9), tight_layout=True)
            # 设置轴显示的范围
            ax.set(ylim=(df["value_min"].min(), df['value_max'].max()))
            ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=18)
            # 去除上下左右的边框（默认该函数会取出右上的边框）
            sns.despine(right=True, top=True)
            vio = sns.violinplot(data=df, x=df["Cell_type"], y=df["value_max"], palette="Set3", scale='width',
                                 inner=None)
            plt.xlabel('')
            save_path = os.path.join(
                settings.ATLAS_HOT_PNG_DIR, "{file_name}".format(file_name='violinplot_png'))
            save_violinplot_png = '{save_path}/{uuid_str}_violinplot.png'.format(save_path=save_path, uuid_str=uuid_str)

            plt.savefig(save_violinplot_png)
            # plt.close()
            # 绘制箱型图
            # 设置窗口的大小

            f, ax = plt.subplots(figsize=(8, 9), tight_layout=True)
            # 设置轴显示的范围
            ax.set(ylim=(0, 1))
            ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right", fontsize=18)
            # 去除上下左右的边框（默认该函数会取出右上的边框）
            sns.despine(right=True, top=True)

            box = sns.boxplot(data=df, x=df["Cell_type"], y=df["value_max"], palette="Set3")
            plt.xlabel('')
            save_boxplot_png = '{save_path}/{uuid_str}_boxplot.png'.format(save_path=save_path, uuid_str=uuid_str)
            plt.savefig(save_boxplot_png)
            plt.close()
            return uuid_str + "_" + 'violinplot.png', uuid_str + "_" + 'boxplot.png'
    except Exception as e:
        print(e)
        return '', ''
