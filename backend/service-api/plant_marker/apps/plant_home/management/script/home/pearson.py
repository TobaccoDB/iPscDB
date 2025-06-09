from datetime import datetime

import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

print(datetime.now())


# Project_ID Clusters Cell_type
def pearson_cell_type():
    data = pd.read_csv("./total_mean_Cell_type.csv")
    # f, ax = plt.subplots(figsize=(6.5, 6.5))
    corr = data.corr()
    # sns.heatmap(corr, cmap='RdBu', linewidths=0.05, ax=ax)
    # plt.tight_layout()
    g = sns.clustermap(corr,
                       row_cluster=True,  # 行 聚类
                       col_cluster=True,  # 列 聚类
                       cmap='coolwarm',  # 颜色配置
                       figsize=(10, 10),
                       linewidths=0.01
                       )
    plt.setp(g.ax_heatmap.get_xticklabels(), rotation=75)
    plt.setp(g.ax_heatmap.get_xticklabels(), rotation=75)

    # g.fig.subplots_adjust(right=0.7)
    g.ax_cbar.set_position((1.05, 0.3, 0.02, 0.4))
    g.savefig('pearson_Cell_type.png', dpi=150, bbox_inches='tight')
    # 设置Axes的标题
    # ax.set_title('Correlation between features')
    # plt.show()
    plt.close()
    # f.savefig('pearson.png', dpi=100, bbox_inches='tight')


def pearson_clusters():
    data = pd.read_csv("./total_mean_Clusters.csv")
    # f, ax = plt.subplots(figsize=(16, 10))
    corr = data.corr()
    # sns.heatmap(corr, cmap='RdBu', linewidths=0.05, ax=ax)
    plt.tight_layout()
    g = sns.clustermap(corr,
                       row_cluster=True,  # 行 聚类
                       col_cluster=True,  # 列 聚类
                       cmap='coolwarm',  # 颜色配置
                       figsize=(7.5, 5),
                       linewidths=0.01)
    g.fig.subplots_adjust(right=0.7)
    g.ax_cbar.set_position((0.8, 0.3, 0.02, 0.4))
    g.savefig('pearson_Clusters.png', dpi=150, bbox_inches='tight')
    # 设置Axes的标题
    # ax.set_title('Correlation between features')
    # plt.show()
    plt.close()


def pearson_project_id():
    data = pd.read_csv("./total_mean_Project_ID.csv")
    num_cols = len(data.columns)
    corr = data.corr()
    if num_cols < 2:
        f, ax = plt.subplots(figsize=(6.5, 5.5))
        sns.heatmap(corr, cmap='RdBu', linewidths=0.05, ax=ax)
        # 设置Axes的标题
        ax.set_title('Correlation between features')
        plt.savefig('pearson_Project_ID.png', dpi=150, bbox_inches='tight')
    else:
        plt.tight_layout()
        g = sns.clustermap(corr,
                           row_cluster=True,  # 行 聚类
                           col_cluster=True,  # 列 聚类
                           cmap='coolwarm',  # 颜色配置
                           figsize=(6.5, 5.5),
                           linewidths=0.01)
        g.fig.subplots_adjust(right=0.7)
        g.ax_cbar.set_position((0.95, 0.3, 0.02, 0.4))
        g.savefig('pearson_Project_ID.png', dpi=150, bbox_inches='tight')

    # plt.show()
    plt.close()


if __name__ == "__main__":
    pearson_cell_type()
    pearson_clusters()
    pearson_project_id()
