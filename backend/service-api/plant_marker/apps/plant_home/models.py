from django.db import models
from django.utils import timezone


class CellMarkerInfo(models.Model):
    """
    细胞标记信息表
    """
    mar_id = models.CharField(verbose_name='Mar_ID', max_length=150, null=True, blank=True, db_index=True)
    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True)
    tissue_id = models.CharField(verbose_name='组织ID', max_length=100, null=True, blank=True)
    cell_id = models.CharField(verbose_name='细胞ID', max_length=100, null=True, blank=True, db_index=True)
    gene_symbol = models.CharField(verbose_name='基因标志', max_length=100, null=True, blank=True)
    gene_id = models.CharField(verbose_name='基因ID', max_length=100, null=True, blank=True, db_index=True)
    gene_id_other = models.CharField(verbose_name='基因其他ID', max_length=100, null=True, blank=True)
    lit_id = models.CharField(verbose_name='Lit_ID', max_length=100, null=True, blank=True, db_index=True)
    source_id = models.CharField(verbose_name='来源ID', max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "cell_marker_info"


class ClusterMarkerInfo(models.Model):
    """
    簇标记信息表
    """
    cluster_marker_id = models.CharField(verbose_name='ClMark_ID', max_length=150, null=True, blank=True, db_index=True)
    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True)
    tissue_id = models.CharField(verbose_name='组织ID', max_length=100, null=True, blank=True)
    cell_type = models.CharField(verbose_name='细胞类型', max_length=150, null=True, blank=True)
    cluster_name = models.CharField(verbose_name='(同类物丛生或聚集的)簇名称', max_length=100, null=True, blank=True)
    cluster_marker = models.CharField(verbose_name='簇标记', max_length=1000, null=True, blank=True)
    gene_id = models.CharField(verbose_name='基因ID', max_length=100, null=True, blank=True)
    gene_id_other = models.CharField(verbose_name='基因其他ID', max_length=100, null=True, blank=True)
    lit_id = models.CharField(verbose_name='Lit_ID', max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "cluster_marker_info"


class LiteratureInfo(models.Model):
    """
    文献信息表
    """
    lit_id = models.CharField(verbose_name='Lit_ID', max_length=100, null=True, blank=True, db_index=True)
    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True, db_index=True)
    pmid = models.CharField(verbose_name='PMID', max_length=100, null=True, blank=True)
    doi = models.CharField(verbose_name='DOI', max_length=255, null=True, blank=True)
    title = models.CharField(verbose_name='标题', max_length=5000, blank=True, null=True)
    year = models.CharField(verbose_name="年份", max_length=100, null=True, blank=True)
    data_type = models.CharField(verbose_name="数据类型", max_length=100, null=True, blank=True)
    download = models.CharField(verbose_name="下载", max_length=100, null=True, blank=True)
    unzip = models.CharField(verbose_name="解压", max_length=100, null=True, blank=True)
    cell_ranger = models.CharField(verbose_name="CellRanger", max_length=100, null=True, blank=True)
    qc = models.CharField(verbose_name="CellRanger", max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "literature_info"


class Sample(models.Model):
    """
    样品表
    """
    sam_id = models.CharField(verbose_name='Sam_ID', max_length=100, null=True, blank=True, db_index=True)
    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True, db_index=True)
    project_id = models.CharField(verbose_name='Project_ID', max_length=100, null=True, blank=True, db_index=True)
    sample_id = models.CharField(verbose_name='Sample_ID', max_length=100, null=True, blank=True, db_index=True)
    sample_name = models.CharField(verbose_name='Sample_Name', max_length=250, null=True, blank=True)
    geno_type = models.CharField(verbose_name='基因型', max_length=250, null=True, blank=True)
    treament = models.CharField(verbose_name='处理', max_length=100, null=True, blank=True)
    ecotype = models.CharField(verbose_name='生态型', max_length=100, null=True, blank=True)
    age = models.CharField(verbose_name='年龄段', max_length=100, null=True, blank=True)
    tissue = models.CharField(verbose_name='组织', max_length=100, null=True, blank=True)
    chemistry = models.CharField(verbose_name='物质的化学组成', max_length=150, null=True, blank=True)
    lit_id = models.CharField(verbose_name='Lit_ID', max_length=100, null=True, blank=True)
    qc_check = models.CharField(verbose_name='QC_check', max_length=100, null=True, blank=True)
    qc_cells = models.CharField(verbose_name='QC_Cells', max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "sample"


class TissueType(models.Model):
    """
     组织类型表
    """
    tiss_id = models.CharField(verbose_name='Tiss_ID', max_length=100, null=True, blank=True, db_index=True)
    tiss_name_lit = models.CharField(verbose_name='Tiss_Name_Lit', max_length=150, null=True, blank=True)
    tiss_po_name = models.CharField(verbose_name='Tiss_PO_Name', max_length=150, null=True, blank=True)
    po_num = models.CharField(verbose_name='PO_Num', max_length=150, null=True, blank=True)
    parent_id = models.CharField(verbose_name='Parent_ID', max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "tissue_type"


class CellType(models.Model):
    """
    细胞类型表
    """
    cell_id = models.CharField(verbose_name='Cell_ID', max_length=100, null=True, blank=True, db_index=True)
    cell_name_lit = models.CharField(verbose_name='Cell_Name_Lit', max_length=150, null=True, blank=True)
    cell_name = models.CharField(verbose_name='Cell_Name', max_length=150, null=True, blank=True)
    cell_po = models.CharField(verbose_name='Cell_PO', max_length=150, null=True, blank=True)
    tiss_id = models.CharField(verbose_name='Tiss_ID', max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "cell_type"


class MarkerInfo(models.Model):
    """
    标记表
    """
    p_va1 = models.FloatField(verbose_name='p_val', null=True, blank=True)
    log_2fc = models.FloatField(verbose_name='Log2FC', null=True, blank=True)
    pct1 = models.FloatField(verbose_name='Pct1', null=True, blank=True)
    pct2 = models.FloatField(verbose_name='Pct2', null=True, blank=True)
    p_val_adj = models.FloatField(verbose_name='P_val_adj', null=True, blank=True)
    cluster_id = models.IntegerField(verbose_name='Cluster_ID', null=True, blank=True)
    gene_id = models.CharField(verbose_name='基因ID', max_length=100, null=True, blank=True)
    cell_type = models.CharField(verbose_name='细胞类型', max_length=150, null=True, blank=True)
    tissue = models.CharField(verbose_name='细胞类型', max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "marker_info"


class SampleRdsDownload(models.Model):
    """
     SampleRds数据下载表
    """
    sample_id = models.CharField(verbose_name='Sample_ID', max_length=100, null=True, blank=True, db_index=True)

    class Meta:
        db_table = "sample_rds_download"


class ProjrctAtlasCellType(models.Model):
    """
    ProjrctAtlasCellType表
    """

    lit_id = models.CharField(verbose_name='Lit_ID', max_length=100, null=True, blank=True, db_index=True)
    gene_symbol = models.CharField(verbose_name='基因别名', max_length=50, default=None, null=True, blank=True)
    clusters = models.IntegerField(verbose_name='Clusters', null=True, blank=True)
    cluster_name = models.CharField(verbose_name='Clusters_Name', max_length=150, null=True, blank=True)
    cell_name = models.CharField(verbose_name='细胞名称', max_length=100, null=True, blank=True)
    cell_po = models.CharField(verbose_name='细胞PO', max_length=100, null=True, blank=True)
    po_num = models.CharField(verbose_name='PONum', max_length=100, null=True, blank=True)
    gene_id = models.CharField(verbose_name='基因ID', max_length=100, null=True, blank=True, db_index=True)
    doi = models.CharField(verbose_name='文献', max_length=100, null=True, blank=True)
    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True)
    tissue_id = models.CharField(verbose_name='组织ID', max_length=100, null=True, blank=True)
    sorce = models.IntegerField(verbose_name='Sorce', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "project_atlas_cell_type"


class UserIP(models.Model):
    ip = models.CharField(verbose_name='IP 地址', max_length=30, null=True, blank=True)
    ip_addr = models.CharField(verbose_name='IP 地理位置', max_length=30, null=True, blank=True)
    count = models.IntegerField(verbose_name='访问次数', default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "user_ip_record"


# 网站总访问次数
class VisitNumber(models.Model):
    total_visit = models.IntegerField(verbose_name='网站访问总次数', default=0)  # 网站访问总次数
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'total_visit_number'


# 单日访问量统计
class DayNumber(models.Model):
    day = models.DateField(verbose_name='日期', default=timezone.now)
    count = models.IntegerField(verbose_name='网站访问次数', default=0)  # 网站访问总次数
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'day_visit_number'


class CellIdentificationInfo(models.Model):
    """
    CellIdentification表
    """
    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True)
    title = models.CharField(verbose_name='标题', max_length=100, null=True, blank=True)
    cell_type = models.CharField(verbose_name='细胞类型', max_length=100, null=True, blank=True, db_index=True)
    pdf_name = models.CharField(verbose_name='对应的PDF', max_length=100, null=True, blank=True)
    scope_url = models.CharField(verbose_name='对应的SCope地址', max_length=1024, null=True, blank=True, db_index=True)
    project_id = models.CharField(verbose_name='Project_ID', max_length=100, null=True, blank=True)
    lit_id = models.CharField(verbose_name='Lit_ID', max_length=100, null=True, blank=True, db_index=True)
    rds_name = models.CharField(verbose_name='RDS文件名', max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    cells_reference = models.IntegerField(verbose_name='网站访问总次数', default=0)

    class Meta:
        db_table = "cell_identification_info"


class BrowseInfo(models.Model):
    """
    CellIdentification表
    """
    lit_id = models.CharField(verbose_name='Lit_ID', max_length=100, null=True, blank=True, db_index=True)
    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True, db_index=True)
    pmid = models.CharField(verbose_name='PMID', max_length=100, null=True, blank=True)
    doi = models.CharField(verbose_name='DOI', max_length=255, null=True, blank=True)
    title = models.CharField(verbose_name='标题', max_length=5000, blank=True, null=True)
    project_id = models.CharField(verbose_name='Project_ID', max_length=100, null=True, blank=True, db_index=True)
    tissue = models.CharField(verbose_name='组织', max_length=100, null=True, blank=True)
    chemistry = models.CharField(verbose_name='物质的化学组成', max_length=150, null=True, blank=True)
    qc_cells = models.CharField(verbose_name='QC_Cells', max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "browse_info"


class SraInformation(models.Model):
    """SraInformation"""
    # db_index：数据库索引
    dataset_id = models.CharField(verbose_name='dataset_id', max_length=100, null=True, blank=True, db_index=True)
    dataset = models.CharField(verbose_name='数据集', max_length=100, null=True, blank=True, db_index=True)
    bio_project = models.CharField(verbose_name='生物项目', max_length=100, null=True, blank=True, db_index=True)
    species = models.CharField(verbose_name='物种', max_length=255, null=True, blank=True, db_index=True)
    tissue = models.CharField(verbose_name='组织', max_length=255, null=True, blank=True, db_index=True)
    sample = models.CharField(verbose_name='样品', max_length=255, null=True, blank=True)
    condition = models.CharField(verbose_name='环境', max_length=255, null=True)
    genotype = models.CharField(verbose_name='基因类型', max_length=255, null=True)
    libraries = models.CharField(verbose_name='资料', max_length=100, null=True)
    age = models.CharField(verbose_name='年龄', max_length=255, null=True)
    experiments = models.CharField(verbose_name='实验', max_length=10)
    cells = models.CharField(verbose_name='细胞', max_length=10, null=True, blank=True, db_index=True)
    pmid = models.CharField(verbose_name='pmid', max_length=255, blank=True, db_index=True)
    doi_id = models.CharField(verbose_name='doi_id', max_length=255, blank=True)

    class Meta:
        db_table = "sra_information"


class PapersInfo(models.Model):
    """PapersInfo表"""
    # db_index：数据库索引
    lit_id = models.CharField(verbose_name='Lit_id', max_length=100, null=True, blank=True, db_index=True)
    species = models.CharField(verbose_name='物种', max_length=100, null=True, blank=True, db_index=True)
    pmid = models.CharField(verbose_name='pmid', max_length=100, null=True, db_index=True)
    doi_id = models.CharField(verbose_name='doi_id', max_length=255, null=True, blank=True, db_index=True)
    title = models.TextField(verbose_name='标题', null=True, blank=True)
    year = models.CharField(verbose_name='年份', max_length=50, null=True, blank=True)
    author = models.TextField(verbose_name='作者', null=True, blank=True)
    abstract = models.TextField(verbose_name='摘要', null=True, blank=True)

    class Meta:
        db_table = "papers_info"


class ClassicMarkersInfo(models.Model):
    """ classic_markers_info表 """
    mar_id = models.CharField(verbose_name='mar_id', max_length=100, null=True, blank=True, db_index=True)
    species_name = models.CharField(verbose_name='物种名称', max_length=100, null=True, blank=True, db_index=True)
    tissue_id = models.CharField(verbose_name='组织ID', max_length=100, null=True, blank=True, db_index=True)
    cell_id = models.CharField(verbose_name='细胞ID', max_length=255, null=True, blank=True, db_index=True)
    po_id = models.CharField(verbose_name='po_id', max_length=100, null=True, blank=True, db_index=True)
    po_name = models.CharField(verbose_name='po_name', max_length=255, null=True, blank=True)
    gene_id = models.CharField(verbose_name='基因ID', max_length=100, null=True, blank=True, db_index=True)
    gene_symbol = models.CharField(verbose_name='基因符号', max_length=100, null=True, blank=True, db_index=True)
    geneid_other = models.CharField(verbose_name='基因其它', max_length=100, null=True, blank=True)
    pmid = models.CharField(verbose_name='pmid', max_length=100, null=True, blank=True, db_index=True)

    class Meta:
        db_table = "classic_markers_info"


class MarkerGenesInfo(models.Model):
    """ marker_genes_info """
    gene = models.CharField(verbose_name='gene', max_length=100, null=True, blank=True, db_index=True)
    name = models.CharField(verbose_name='name', max_length=100, null=True, blank=True, db_index=True)
    p_val = models.FloatField(verbose_name='p_val', null=True, blank=True)
    p_val_adj = models.FloatField(verbose_name='p_val_adj', null=True, blank=True)
    pct_1 = models.FloatField(verbose_name='pct_1', null=True, blank=True)
    pct_2 = models.FloatField(verbose_name='pct_2', null=True, blank=True)
    pct_diff = models.FloatField(verbose_name='pct_diff', null=True, blank=True)
    avg_log2FC = models.FloatField(verbose_name='avg_log2FC', null=True, blank=True)
    clusterName = models.CharField(verbose_name='clusterName', max_length=100, null=True, blank=True, db_index=True)
    celltype_id = models.CharField(verbose_name='celltype_id', max_length=255, null=True, blank=True, db_index=True)
    species = models.CharField(verbose_name='species', max_length=100, null=True, blank=True, db_index=True)
    tissue = models.CharField(verbose_name='tissue', max_length=100, null=True, blank=True, db_index=True)
    dataset = models.CharField(verbose_name='dataset', max_length=100, null=True, blank=True, db_index=True)

    class Meta:
        db_table = "marker_genes_info"


class SummaryResultInfo(models.Model):
    """ summary_result_info """
    species = models.CharField(verbose_name='species', max_length=100, null=True, blank=True, db_index=True)
    tissue = models.CharField(verbose_name='tissue', max_length=100, null=True, blank=True, db_index=True)
    clusterName = models.CharField(verbose_name='clusterName', max_length=100, null=True, blank=True, db_index=True)
    gene = models.CharField(verbose_name='gene', max_length=100, null=True, blank=True, db_index=True)
    name = models.CharField(verbose_name='name', max_length=100, null=True, blank=True, db_index=True)
    cellType_id = models.CharField(verbose_name='cellType_id', max_length=255, null=True, blank=True, db_index=True)
    source_no = models.CharField(verbose_name='source_no', blank=True, null=True, max_length=100)
    dataset = models.CharField(verbose_name='dataset', max_length=100, null=True, blank=True, db_index=True)
    classic_count = models.CharField(verbose_name='classic_count', blank=True, null=True, max_length=100)
    classic_marker = models.CharField(verbose_name='classic_marker', max_length=100, null=True, blank=True)

    class Meta:
        db_table = "summary_result_info"


class EfpSvgInfo(models.Model):
    """
   EfpSvg表
    """
    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True, db_index=True)
    tissue = models.CharField(verbose_name='组织', max_length=100, null=True, blank=True)
    svg = models.TextField(verbose_name='物种SVG', default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "efp_svg_info"


class EfpGeneExpress(models.Model):
    """
   物种基因表达值
   """
    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True, db_index=True)
    gene_id = models.CharField(verbose_name='基因id', max_length=50, default=None, db_index=True)
    class_name = models.CharField(verbose_name='ClassName', max_length=50, default=None, db_index=True)
    tissue = models.CharField(verbose_name='组织', max_length=50, default=None, db_index=True)
    tissue_id = models.CharField(verbose_name='组织', max_length=50, null=True, blank=True)
    value = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "efp_gene_express"


class ReferenceCellTypeInfo(models.Model):
    """
   ReferenceCellType
   """
    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True, db_index=True)
    tissue = models.CharField(verbose_name='组织', max_length=50, default=None, db_index=True)
    cell_type = models.CharField(verbose_name='细胞类型', max_length=100, default=None)
    type = models.CharField(verbose_name='类型', max_length=50, default=None)
    parent = models.CharField(verbose_name='亲本的', max_length=50, default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "reference_cell_type_info"


class GeneSymbolToGeneIdInfo(models.Model):
    """
   GeneSymbolToGeneId
   """
    gene_symbol = models.CharField(verbose_name='基因别名', max_length=50, default=None)
    gene_id = models.CharField(verbose_name='基因', max_length=50, default=None)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "gene_symbol_gene_id_info"


class ProjrctAtlasCellMarker(models.Model):
    """
    ProjrctAtlasCellMarker表
    """
    mar_id = models.CharField(verbose_name='Mar_ID', max_length=100, null=True, blank=True)
    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True)
    tissue_id = models.CharField(verbose_name='组织', max_length=50, default=None, db_index=True)
    cell_type = models.CharField(verbose_name='细胞类型', max_length=100, default=None)
    gene_symbol = models.CharField(verbose_name='基因别名', max_length=50, default=None)
    gene_id = models.CharField(verbose_name='基因ID', max_length=100, null=True, blank=True, db_index=True)
    gene_id_other = models.CharField(verbose_name='基因其他ID', max_length=100, null=True, blank=True)
    lit_id = models.CharField(verbose_name='Lit_ID', max_length=100, null=True, blank=True)
    sorce = models.IntegerField(verbose_name='Sorce', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "project_atlas_cell_marker"


class ProjrctAtlasClusterMarker(models.Model):
    """
    ProjrctAtlasClusterMarker表
    """

    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True)
    tissue_id = models.CharField(verbose_name='组织', max_length=50, default=None, db_index=True)
    cell_type = models.CharField(verbose_name='细胞类型', max_length=100, default=None)
    gene_id = models.CharField(verbose_name='基因ID', max_length=100, null=True, blank=True, db_index=True)
    cluster_marker = models.CharField(verbose_name='cluster_marker', max_length=100, null=True, blank=True)
    gene_id_other = models.CharField(verbose_name='基因其他ID', max_length=100, null=True, blank=True)
    lit_id = models.CharField(verbose_name='Lit_ID', max_length=100, null=True, blank=True)
    sorce = models.IntegerField(verbose_name='Sorce', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "project_atlas_cluster_marker"


class CellTypeToGeneIdInfo(models.Model):
    """
   CellType和基因对应的数据
   """
    lit_id = models.CharField(verbose_name='Lit_ID', max_length=100, null=True, blank=True)
    cell_type = models.CharField(verbose_name='细胞类型', max_length=100, default=None)
    gene_id = models.CharField(verbose_name='基因', max_length=50, default=None)
    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True)
    tissue = models.CharField(verbose_name='组织', max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "cell_type_gene_id_info"


class AtlasDownload(models.Model):
    """
   Atlas下载列表
   """
    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True)
    version = models.CharField(verbose_name='版本', max_length=150, null=True, blank=True)
    atlas_type = models.CharField(verbose_name='类型', max_length=150, null=True, blank=True)
    atlas_name = models.CharField(verbose_name='名字', max_length=150, null=True, blank=True)
    source = models.CharField(verbose_name='来源', max_length=150, null=True, blank=True)
    size = models.CharField(verbose_name='大小', max_length=150, null=True, blank=True)
    md5 = models.CharField(verbose_name='MD5', max_length=150, null=True, blank=True)
    last_update = models.CharField(verbose_name='最近更新时间', max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "atlas_download"


class CellMarkerDownload(models.Model):
    """
   CellMarker下载列表
   """
    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True)
    tissue = models.CharField(verbose_name='组织', max_length=150, null=True, blank=True)
    source = models.CharField(verbose_name='来源', max_length=150, null=True, blank=True)
    size = models.CharField(verbose_name='大小', max_length=150, null=True, blank=True)
    md5 = models.CharField(verbose_name='MD5', max_length=150, null=True, blank=True)
    last_update = models.CharField(verbose_name='最近更新时间', max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "cell_marker_download"


class ClusterMarkerDownload(models.Model):
    """
   ClusterMarker下载列表
   """
    species_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True)
    tissue = models.CharField(verbose_name='组织', max_length=150, null=True, blank=True)
    source = models.CharField(verbose_name='来源', max_length=150, null=True, blank=True)
    size = models.CharField(verbose_name='大小', max_length=150, null=True, blank=True)
    md5 = models.CharField(verbose_name='MD5', max_length=150, null=True, blank=True)
    last_update = models.CharField(verbose_name='最近更新时间', max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "cluster_marker_download"


class HomologGenes(models.Model):
    """
   HomologGenes列表
   """
    specie_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True)
    reference_name = models.CharField(verbose_name='相关物种', max_length=150, null=True, blank=True)
    specie_gene = models.CharField(verbose_name='物种基因', max_length=150, null=True, blank=True)
    reference_gene = models.CharField(verbose_name='相关物种基因', max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "homo_log_gene"


class HomeLogs(models.Model):
    title = models.CharField(verbose_name='日志', max_length=255, default='empty')
    content = models.TextField(verbose_name='日志内容', default='empty')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "home_update_log"


# 为了基因别名映射、从Plncdb迁移过来的数据
'''基因信息表'''


class GeneInfo(models.Model):
    gene_id = models.CharField(verbose_name='基因ID', max_length=255, null=True, blank=True, db_index=True)
    isoform_id = models.CharField(verbose_name='亚型ID', max_length=255, null=True, blank=True, db_index=True)

    gene_symbol = models.TextField(verbose_name='其他名称', null=True, blank=True, max_length=1024)
    species = models.CharField(verbose_name='物种名称', max_length=255, null=True, blank=True, db_index=True)
    ref_genome_vers = models.CharField(verbose_name='参考基因组', max_length=255, null=True, blank=True)

    chromesome_scaffold = models.CharField(verbose_name='色度/支架', max_length=255, null=True, blank=True)
    start = models.IntegerField(verbose_name='开始', null=True, blank=True)
    end = models.IntegerField(verbose_name='结束', null=True, blank=True)
    strand = models.CharField(verbose_name='链', max_length=255, null=True, blank=True)
    exon_num = models.IntegerField(verbose_name='外显子', null=True, blank=True)
    interpro_id = models.CharField(verbose_name='注释基因', max_length=255, null=True, blank=True)
    pfam_id = models.TextField(verbose_name='蛋白数据库', max_length=255, null=True, blank=True)
    panther_id = models.CharField(verbose_name='蛋白质分析数据库', null=True, blank=True, max_length=255)
    kog_id = models.CharField(verbose_name='真核原组', null=True, blank=True, max_length=255)
    ec_id = models.CharField(verbose_name='酶编号', null=True, blank=True, max_length=255)
    kegg_id = models.CharField(verbose_name='京都基因与基因组百科全书', null=True, blank=True, max_length=255)
    go_id = models.TextField(verbose_name='基因本体论', max_length=1024, null=True, blank=True)
    uniprotkb_id = models.TextField(verbose_name='蛋白数据库集', null=True, blank=True, max_length=1024)
    function = models.TextField(verbose_name='功能', max_length=255, null=True, blank=True)
    subcellular = models.CharField(verbose_name='亚细胞', null=True, blank=True, max_length=255)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", null=True, blank=True)

    class Meta:
        verbose_name = "gene_info"
        db_table = verbose_name
        verbose_name_plural = verbose_name


class ProjectAtlasCount(models.Model):
    lit_id = models.CharField(verbose_name='Lit_ID', max_length=100, null=True, blank=True)
    project_id = models.CharField(verbose_name='Project_ID', max_length=100, null=True, blank=True, db_index=True)
    cell_count = models.CharField(verbose_name='细胞的个数', max_length=100, null=True, blank=True, db_index=True)
    sample_count = models.CharField(verbose_name='sample的个数', max_length=100, null=True, blank=True, db_index=True)
    specie_name = models.CharField(verbose_name='物种名称', max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = "project_atlas_count"


class CellTypeRelations(models.Model):
    species_name = models.CharField(verbose_name='物种', max_length=255, null=True, blank=True, db_index=True)
    tissue_name = models.CharField(verbose_name='组织', max_length=255, null=True, blank=True, db_index=True)
    l1 = models.CharField(verbose_name='l1', max_length=255, null=True, blank=True, db_index=True)
    l2 = models.CharField(verbose_name='l2', max_length=255, null=True, blank=True, db_index=True)
    l3 = models.CharField(verbose_name='l3', max_length=255, null=True, blank=True, db_index=True)

    class Meta:
        db_table = "cell_type_relations"


class CellTypeDetails(models.Model):
    name = models.CharField(verbose_name='组织或细胞名称', max_length=100, null=True, blank=True, db_index=True)
    po_id = models.CharField(verbose_name='组织或细胞po_id', max_length=100, null=True, blank=True, db_index=True)
    other_names = models.CharField(verbose_name='别名', max_length=100, null=True, blank=True)
    description = models.TextField(verbose_name='描述', null=True, blank=True)
    link = models.CharField(verbose_name='链接', max_length=255, null=True, blank=True)

    class Meta:
        db_table = "cell_type_details"


class GeneDetailsInfo(models.Model):
    scaffold = models.CharField(verbose_name='参考序列', max_length=100, null=True, blank=True)
    start = models.CharField(verbose_name='起始位置', max_length=100, null=True, blank=True)
    end = models.CharField(verbose_name='终止位置', max_length=100, null=True, blank=True)
    strand = models.CharField(verbose_name='链', max_length=10, null=True, blank=True)
    gene_id = models.CharField(verbose_name='基因ID', max_length=100, null=True, blank=True, db_index=True)
    gene_symbol = models.CharField(verbose_name='基因符号', max_length=100, null=True, blank=True)
    description = models.TextField(verbose_name='描述', null=True, blank=True)

    class Meta:
        db_table = "gene_details_info"


class SpeciesMappingInfo(models.Model):
    species = models.CharField(verbose_name='物种', max_length=100, null=True, blank=True)
    tissue = models.CharField(verbose_name='组织', max_length=100, null=True, blank=True)
    mapping = models.CharField(verbose_name='映射', max_length=100, null=True, blank=True)

    class Meta:
        db_table = "species_mapping_info"