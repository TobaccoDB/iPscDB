import os
# ======================
# = Databases Settings
# ======================

SECRET_KEY = '$1zorj_e!j34%r0qcwh1o(a%4x83nne@hr9mzsgy8l^5$-c$yb'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'NAME': os.environ.get('DB_ANALYSIS_NAME'),
        'HOST': 'db',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 60,
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci'
        }
    }
}
# ======================
# ====Sample rds 数据 Settings ====
# ======================
BASE_URL = os.environ.get('API_BASE_URL')
SAMPLE_RDS_DOWNLOAD = '/data/Sample_clean_rds/'
SAMPLE_UPLOAD_RDS_DIR = '/data/Sample_QC/upload_rds_data/'
SAMPLE_UPLOAD_GZ_DIR = '/data/Sample_QC/upload_gz_data/'
SAPMLE_FILTER_RDS_ADDRESS = f'{BASE_URL}/filter_rds/'
SAPMLE_FILTER_RDS_DIR = '/data/Sample_QC/filter_rds_data/'
SAMPLE_PICTURE_ADDRESS = f'{BASE_URL}/picture/'
GENE_EXPRESSION_FILE = '/data/Gene_expression/'
'===============================INTEGRATION=============================='
# integration zip 压缩包下载
INTEGRATION_ZIP_DOWNLOAD = f'{BASE_URL}/integration/'
# integration Example 示例图片展示
INTEGRATION_EXAMPLE_SVG_SHOW = f'{BASE_URL}/integration_example_svg/'
# integration svg/png 图片下载
INTEGRATION_SVG_PNG_DOWNLOAD = f'{BASE_URL}/integration/'
# integration Result_Picture 生成图片展示
INTEGRATION_RESULT_PICTURE = f'{BASE_URL}/integration_svg/'
'===============================Cell Identification=============================='
# Cell Identification RDS文件上传目录
CELL_IDENTIFICATION_DIR = '/data/Cell_identification/upload_rds_data/'
# 图片生成保存文件路径
CELL_IDENTIFICATION_PICTURE = '/data/Cell_identification/classifier_picture/'
# svg展示和下载链接
CELL_IDENTIFICATION_PICTURE_SVG = f'{BASE_URL}/classifier_svg/'
# cell_identification_pdf展示
CELL_IDENTIFICATION_PDF = f'{BASE_URL}/classifier_png/'
# csv文件上传文夹路径
CELL_IDENTIFICATION_CSV_UPLOAD = '/data/Cell_identification/upload_csv_data/'
# csv文件下载文夹路径
CELL_IDENTIFICATION_ZIP_CSV_DOWNLOAD = '/data/Cell_identification/create_csv_dir'
# CELL_IDENTIFICATION zip 压缩包下载
CELL_IDENTIFICATION_ZIP_CSV = f'{BASE_URL}/Cell_identification_all_zip/'
# 热力图/data/Project_atlas/hot_png
CELL_EXPRESSION_PICTURE_PNG = f'{BASE_URL}/hot_png/'
# Project_atlas数据路径
CELL_EXPRESSION_DIR = '/data/Project_atlas/'
# 手风琴和箱图/data/Atlas/violinplot_png/
CELL_EXPRESSION_VIOLINPOLT_PNG = f'{BASE_URL}/violinplot_png/'
ATLAS_CELL_EXPRESSION_VIOLINPOLT_PNG = f'{BASE_URL}/atlas_violinplot_png/'
# Atlas数据路径
# Atlas 热力图/data/Atlas/hot_png/
ATLAS_CELL_EXPRESSION_PICTURE_PNG = f'{BASE_URL}/atlas_hot_png/'
ATLAS_HOT_PNG_DIR = '/data/Atlas/'
# Project组织小图标
PROJECT_TISSUE_HEAD = f'{BASE_URL}/project_tissue_head/'
# Project static umap 静态图
PROJECT_STATIC_UMAP_PNG = f'{BASE_URL}/project_static_umap_png/'
# Project rds文件下载
PROJECT_DOWNLOAD_RDS = f'{BASE_URL}/project_download_rds/'
'==============================Monocle相关功能=============================='
MONOCLE_FILE = '/data/Monocle/'
MONOCLE_EXPRESSION_FILE = '/data/Monocle/Expression/'
# Monocle expression 图
MONOCLE_EXPRESSION_PNG = f'{BASE_URL}/monocle_expression_png/'
# Monocle heatmap 图
MONOCLE_HEATMAP_PNG = f'{BASE_URL}/monocle_heatmap_png/'
MONOCLE_HEATMAP_FILE = '/data/Monocle/Heatmap/'
PROJECT_ATLAS_DOWNLOAD = '/data/project_gematrix_download/'
PROJECT_ATLAS_DOWNLOAD_URL = f'{BASE_URL}/project_atlas_download/'
PROJECT_ATLAS_DOWNLOAD_RDS = '/opt/project_rds_download/'
PROJECT_ATLAS_DOWNLOAD_RDS_URL = f'{BASE_URL}/project_atlas_download_rds/'
CELL_MARKER_DOWNLOAD = '/data/cell_marker_download/'
CELL_MARKER_DOWNLOAD_URL = f'{BASE_URL}/cell_marker_download/'
CELL_CLUSTER_DOWNLOAD = '/data/cluster_marker_download/'
CELL_CLUSTER_DOWNLOAD_URL = f'{BASE_URL}/cluster_marker_download/'

BLAST_DATA_URL = '/data/ncbi-blast-2.10.0+/data/'
QUERY_FILE = '/data/query_file/'
RESULT_PATH = '/data/source_material/result_file/'
EXAMPLE_FILE = '/data/source_material/Example_File/'
