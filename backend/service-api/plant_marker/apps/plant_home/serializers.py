from rest_framework import serializers
from .models import *
import os
from django.conf import settings


class PlantHomeUmaptSerializer(serializers.ModelSerializer):
    """
    列表
    """

    class Meta:
        model = CellMarkerInfo
        fields = ['mar_id', 'species_name', 'tissue_id', 'cell_id', 'gene_symbol', 'gene_id', 'gene_id_other', 'lit_id',
                  'source_id']


class MarkerInfoSerializer(serializers.ModelSerializer):
    """
    Marker列表
    """

    class Meta:
        model = MarkerInfo
        fields = ['p_va1', 'log_2fc', 'pct1', 'pct2', 'p_val_adj', 'cluster_id', 'gene_id', 'cell_type']


class CellTypeSerializer(serializers.ModelSerializer):
    """
    CellType列表
    """
    species_name = serializers.SerializerMethodField()

    class Meta:
        model = CellMarkerInfo
        fields = ['mar_id', 'species_name', 'tissue_id', 'cell_id', 'gene_symbol', 'gene_id', 'gene_id_other', 'lit_id',
                  'source_id']

    def get_species_name(self, obj):
        try:
            species_name = str(obj.species_name).replace('_', ' ')
        except Exception as e:
            species_name = obj.species_name
        return species_name


class SampleSerializer(serializers.ModelSerializer):
    """
    Sample样品列表
    """
    species_name = serializers.SerializerMethodField()
    lit_id = serializers.SerializerMethodField()
    process_status = serializers.SerializerMethodField()

    class Meta:
        model = Sample
        fields = ['sam_id', 'sample_id', 'project_id', 'species_name', 'tissue', 'chemistry', 'lit_id',
                  'process_status', 'ecotype', 'geno_type', 'sample_name']

    def get_species_name(self, obj):
        try:
            species_name = str(obj.species_name).replace('_', ' ')
        except Exception as e:
            species_name = obj.species_name
        return species_name

    def get_lit_id(self, obj):
        try:
            lit_id = str(obj.lit_id).split(',')
            lit_id_dio_list = []
            for i in lit_id:
                dio = LiteratureInfo.objects.get(lit_id=i.strip()).doi
                dio = dio.split('DOI: ')[1]
                dic = {'label': 'https://doi.org/' + dio if dio.startswith('10.') else dio.strip(),
                       'value': i}

                lit_id_dio_list.append(dic)
            lit_id = lit_id_dio_list
        except Exception as e:
            lit_id = []
        return lit_id

    def get_process_status(self, obj):
        try:
            if obj.qc_check:
                process_status = obj.qc_check
            else:
                process_status = 'under process'
        except Exception as e:
            process_status = 'under process'
        return process_status


class SampleSearchSerializer(serializers.ModelSerializer):
    """
    Sample Search
    """
    species_name = serializers.SerializerMethodField()
    process_status = serializers.SerializerMethodField()
    lit_id = serializers.SerializerMethodField()
    is_sample_rds = serializers.SerializerMethodField()

    class Meta:
        model = Sample
        fields = ['sam_id', 'species_name', 'project_id', 'sample_id', 'tissue', 'process_status', 'sample_name',
                  'geno_type', 'treament', 'ecotype', 'age', 'chemistry', 'is_sample_rds', 'lit_id']

    def get_species_name(self, obj):
        try:
            species_name = str(obj.species_name).replace('_', ' ')
        except Exception as e:
            species_name = obj.species_name
        return species_name

    def get_process_status(self, obj):
        try:
            if os.path.lexists(r'/data/Sample_clean_rds/{}'.format(obj.sample_id + '.rds')):
                process_status = 'QC Pass'
            else:
                process_status = 'Under process'
        except Exception as e:
            process_status = 'Under process'
        return process_status

    def get_lit_id(self, obj):
        try:
            lit_id = str(obj.lit_id).split(',')
            lit_id_dio_list = []
            for i in lit_id:
                dio = LiteratureInfo.objects.get(lit_id=i.strip()).doi
                dio = dio.split('DOI: ')[1]
                dic = {'label': i,
                       'value': 'https://doi.org/' + dio if dio.startswith('10.') else dio.strip()}
                lit_id_dio_list.append(dic)
            lit_id = lit_id_dio_list
        except Exception as e:
            lit_id = []
        return lit_id

    def get_is_sample_rds(self, obj):
        """是否显示下载图标 标识
        is_sample_rds  "1"：标识显示下载图标  "0":标识不显示下载图标
        """
        try:
            # if os.path.lexists(r'D:\免疫单细胞数据库\sample_ click_rds\sample_ click_rds\{}'.format(obj.sample_id+'.rds')): 本地测试路径
            if os.path.lexists(r'/data/Sample_clean_rds/{}'.format(obj.sample_id + '.rds')):
                is_sample_rds = '1'
            else:
                is_sample_rds = '0'
        except Exception as e:
            is_sample_rds = '0'
        return is_sample_rds


class ClusterMarkerSearchSerializer(serializers.ModelSerializer):
    """
     ClusterMarkerSearch列表
    """
    species_name = serializers.SerializerMethodField()
    pmid = serializers.SerializerMethodField()

    class Meta:
        model = ClusterMarkerInfo
        fields = ['cluster_marker_id', 'species_name', 'tissue_id', 'cluster_name', 'cluster_marker', 'gene_id',
                  'gene_id_other', 'lit_id',
                  'pmid']

    def get_species_name(self, obj):
        try:
            species_name = str(obj.species_name).replace('_', ' ')
        except Exception as e:
            species_name = obj.species_name
        return species_name

    def get_pmid(self, obj):
        try:
            pmid = str(LiteratureInfo.objects.get(lit_id=obj.lit_id).pmid).split('.')[0]
        except Exception as e:
            pmid = ''
        return pmid


class CellMarkerInfoSearchSerializer(serializers.ModelSerializer):
    """
   CellMarkerInfoSearch列表
    """
    species_name = serializers.SerializerMethodField()
    pmid = serializers.SerializerMethodField()

    class Meta:
        model = CellMarkerInfo
        fields = ['mar_id', 'species_name', 'tissue_id', 'cell_id', 'gene_symbol', 'gene_id', 'gene_id_other', 'lit_id',
                  'source_id',
                  'pmid']

    def get_species_name(self, obj):
        try:
            species_name = str(obj.species_name).replace('_', ' ')
        except Exception as e:
            species_name = obj.species_name
        return species_name

    def get_pmid(self, obj):
        try:
            pmid = str(LiteratureInfo.objects.get(lit_id=obj.lit_id).pmid).split('.')[0]
        except Exception as e:
            pmid = ''
        return pmid


class ProjrctAtlasCellTypeSerializer(serializers.ModelSerializer):
    """
   ProjrctAtlasCellType列表
    """
    doi = serializers.SerializerMethodField()
    gene_id = serializers.SerializerMethodField()
    cell_po = serializers.SerializerMethodField()

    class Meta:
        model = ProjrctAtlasCellType
        fields = ['lit_id', 'cluster_name', 'cell_po', 'tissue_id', 'gene_id', 'doi', 'sorce']

    def get_doi(self, obj):
        try:
            doi_list = []
            if obj.doi:
                for dio in obj.doi.split(','):
                    doi_http = LiteratureInfo.objects.filter(lit_id=dio).first().doi
                    doi_http = doi_http.split('DOI: ')[1]
                    doi_http = 'https://doi.org/' + doi_http if doi_http.startswith('10.') else doi_http.strip()
                    dic_data = {
                        'name': dio,
                        'label': doi_http
                    }
                    doi_list.append(dic_data)
        except Exception as e:

            doi_list = []
        return doi_list

    def get_gene_id(self, obj):
        try:
            gene_id_list = []
            if obj.gene_id:
                for gene in obj.gene_id.split(','):
                    # 先去plncdb中的数据中去找
                    if GeneInfo.objects.filter(gene_id=gene).exists():
                        if GeneInfo.objects.filter(gene_id=gene).first():
                            gene_id_s = GeneInfo.objects.filter(gene_id=gene).first().gene_symbol
                        else:
                            gene_id_s = gene
                    elif CellMarkerInfo.objects.filter(gene_id=gene).exists():
                        if CellMarkerInfo.objects.filter(gene_id=gene).exclude(
                                gene_symbol='').first():
                            gene_id_s = CellMarkerInfo.objects.filter(gene_id=gene).exclude(
                                gene_symbol='').first().gene_symbol
                        else:
                            gene_id_s = gene
                    else:
                        gene_id_s = gene

                    dic_data = {
                        'name': gene_id_s if gene_id_s and gene_id_s != '-' else gene,
                        'label': gene
                    }
                    gene_id_list.append(dic_data)
        except Exception as e:
            print(e)
            gene_id_list = []
        return gene_id_list[0:8]

    def get_cell_po(self, obj):
        try:
            if obj.cell_po:
                cell_po = obj.cluster_name + '-' + obj.cell_po
            else:
                cell_po = obj.cluster_name
        except Exception as e:
            cell_po = obj.cluster_name
        return cell_po


class CellIdentificationPdfTitleSerializer(serializers.ModelSerializer):
    """
    列表
    """
    refrence_title = serializers.SerializerMethodField()

    class Meta:
        model = CellIdentificationInfo
        fields = ['refrence_title']


class CellIdentificationReferenceDetaileSerializer(serializers.ModelSerializer):
    """
    列表
    """
    cells_reference = serializers.SerializerMethodField()
    doi = serializers.SerializerMethodField()
    species_name_down = serializers.SerializerMethodField()
    species_name = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    cell_identification_pdf = serializers.SerializerMethodField()

    class Meta:
        model = LiteratureInfo
        fields = ['species_name', 'cells_reference', 'pmid', 'doi', 'data_type', 'species_name_down', 'title',
                  'cell_identification_pdf']

    def get_species_name(self, obj):
        try:

            species_name = obj.species_name
        except Exception as e:
            print(e)
            species_name = ''
        return species_name

    def get_cell_identification_pdf(self, obj):
        query = CellIdentificationInfo.objects.filter(lit_id__contains=obj.lit_id).first()
        try:
            cell_identification_pdf = settings.CELL_IDENTIFICATION_PDF + '{}.png'.format(query.pdf_name),  # 图片展示
        except Exception as e:
            print(e)
            cell_identification_pdf = ''
        return cell_identification_pdf

    def get_title(self, obj):
        query = CellIdentificationInfo.objects.filter(lit_id__contains=obj.lit_id).first()

        try:
            if query.title == 'Nicotiana_tabacum':
                title = 'Nicotiana attenuate' + '-' + query.cell_type
            elif query.title == 'Populus':
                title = 'Populus alba' + '-' + query.cell_type
            else:
                title = query.title.replace('_', ' ') + '-' + query.cell_type
        except Exception as e:
            print(e)
            title = ''
        return title

    def get_species_name_down(self, obj):
        try:
            if obj.species_name == 'Nicotiana_tabacum':
                species_name = 'Nicotiana attenuate'
            elif obj.species_name == 'Populus':
                species_name = 'Populus alba'
            else:
                species_name = str(obj.species_name).replace('_', ' ')

        except Exception as e:
            print(e)
            species_name = ''
        return species_name

    def get_doi(self, obj):
        try:
            dio = obj.doi.split('DOI: ')[1]
            doi = 'https://doi.org/' + dio if dio.startswith('10.') else dio.strip()
        except Exception as e:
            print(e)
            doi = ''
        return doi

    def get_cells_reference(self, obj):
        try:
            # 不需要去重
            cells_reference = CellIdentificationInfo.objects.get(lit_id=obj.lit_id).cells_reference
        except Exception as e:
            print(e)
            cells_reference = 0
        return cells_reference


class HomeLogsSerializer(serializers.ModelSerializer):
    """
    日志序列化
    """
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = HomeLogs
        fields = ['id', 'title', 'content', 'updated_at']

    def get_updated_at(self, obj):
        return str(obj.updated_at.date())


class BrowseInfoSerializer(serializers.ModelSerializer):
    """
   ProjrctAtlasCellType列表
    """
    species_name = serializers.SerializerMethodField()
    doi = serializers.SerializerMethodField()
    species_value = serializers.SerializerMethodField()
    cell_count = serializers.SerializerMethodField()
    sample_count = serializers.SerializerMethodField()

    class Meta:
        model = BrowseInfo
        fields = ['lit_id', 'species_name', 'pmid', 'doi', 'title', 'project_id', 'tissue', 'chemistry', 'qc_cells',
                  'species_value', 'cell_count', 'sample_count'
                  ]

    def get_species_name(self, obj):
        try:
            species_name = str(obj.species_name).replace('_', ' ')
        except Exception as e:
            print(e)
            species_name = ''
        return species_name

    def get_doi(self, obj):
        try:
            dio = obj.doi.split('DOI: ')[1]
            doi = 'https://doi.org/' + dio if dio.startswith('10.') else dio.strip()
        except Exception as e:
            print(e)
            doi = ''
        return doi

    def get_species_value(self, obj):
        try:
            species_value = obj.species_name
        except Exception as e:
            species_value = ''
        return species_value

    def get_cell_count(self, obj):
        try:
            cell_count = ProjectAtlasCount.objects.get(lit_id=obj.lit_id, project_id=obj.project_id).cell_count
        except Exception as e:
            cell_count = '0'
        return cell_count

    def get_sample_count(self, obj):
        try:
            sample_count = ProjectAtlasCount.objects.get(lit_id=obj.lit_id, project_id=obj.project_id).sample_count
        except Exception as e:
            sample_count = '0'
        return sample_count


class SraInformationSerializer(serializers.ModelSerializer):
    """sra_information"""
    condition = serializers.SerializerMethodField()
    genotype = serializers.SerializerMethodField()

    # pmid = serializers.SerializerMethodField()

    class Meta:
        model = SraInformation
        fields = ['dataset_id','dataset', 'bio_project', 'species', 'tissue', 'sample', 'condition', 'genotype', 'libraries', 'age',
                  'experiments', 'cells', 'pmid', 'doi_id']

    def get_condition(self, obj):
        try:
            condition_list = []
            if obj.condition:
                for item in obj.condition.split(';'):
                    # 数据可能存在::，因此先把::替换为#
                    dic_item = str(item).replace('::', '#').split(':')
                    if len(dic_item) == 2:
                        dic_data = {
                            'name': str(dic_item[0]).replace("#", "::"),
                            'value': dic_item[1],
                        }
                        condition_list.append(dic_data)
        except Exception as e:
            condition_list = []

        return condition_list

    def get_genotype(self, obj):
        try:
            genotype_list = []
            if obj.genotype:
                for item in obj.genotype.split(';'):
                    # 数据可能存在::，因此先把::替换为#
                    dic_item = str(item).replace('::', '#').split(':')
                    if len(dic_item) == 2:
                        dic_data = {
                            'name': str(dic_item[0]).replace("#", "::"),
                            'value': dic_item[1],
                        }
                        genotype_list.append(dic_data)
        except Exception as e:
            genotype_list = []

        return genotype_list

    # def get_pmid(self, obj):
    #     try:
    #         dic_data = {}
    #         if obj.pmid:
    #             doi_http = PapersInfo.objects.filter(pmid=obj.pmid).first().doi_id
    #             doi_http = doi_http.split('DOI: ')[1]
    #             doi_http = 'https://doi.org/' + doi_http if doi_http.startswith('10.') else doi_http.strip()
    #             dic_data = {
    #                 'name': obj.pmid,
    #                 'label': doi_http
    #             }
    #     except Exception as e:
    #         print(e)
    #         dic_data = {}
    #     return dic_data


class PapersInfoSerializer(serializers.ModelSerializer):
    """papers_info"""

    class Meta:
        model = PapersInfo
        fields = ['lit_id', 'species', 'pmid', 'doi_id', 'title', 'year', 'author', 'abstract']


# classic_markers_info表序列化器
class ClassicMarkersInfoSerializer(serializers.ModelSerializer):
    """classic_markers_info"""

    class Meta:
        model = ClassicMarkersInfo
        fields = ['mar_id', 'species_name', 'tissue_id', 'cell_id','po_id', 'po_name', 'gene_id', 'gene_symbol', 'geneid_other', 'pmid']


class MarkerGenesInfoSerializer(serializers.ModelSerializer):
    """ marker_genes_info """
    avg_log2FC = serializers.SerializerMethodField()

    class Meta:
        model = MarkerGenesInfo
        fields = ['gene', 'name', 'p_val', 'p_val_adj', 'pct_1', 'pct_2', 'pct_diff', 'avg_log2FC', 'clusterName',
                  'celltype_id', 'species', 'tissue', 'dataset']

    def get_avg_log2FC(self, obj):
        if obj.avg_log2FC == 999:
            avg_log = 'inf'
        else:
            avg_log = obj.avg_log2FC
        return avg_log


class SummaryResultInfoSerializer(serializers.ModelSerializer):
    """ summary_result_info """
    class Meta:
        model = SummaryResultInfo
        fields = ['species','tissue','clusterName','gene','name','cellType_id','source_no','dataset','classic_count','classic_marker']



class SpeciesEfpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EfpGeneExpress
        fields = ['species_name', 'gene_id', 'class_name', 'tissue', 'value']


class ReferenceCellTypeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceCellTypeInfo
        fields = ['cell_type', 'type', 'parent']


class AtlasDownloadListSerializer(serializers.ModelSerializer):
    species_name = serializers.SerializerMethodField()
    species_name_value = serializers.SerializerMethodField()
    atlas_name_value = serializers.SerializerMethodField()
    atlas_name = serializers.SerializerMethodField()

    class Meta:
        model = AtlasDownload
        fields = ['species_name', 'species_name_value', 'version', 'atlas_type', 'atlas_name', 'atlas_name_value',
                  'source', 'size', 'md5',
                  'last_update']

    def get_species_name(self, obj):
        try:
            species_name = str(obj.species_name).replace('_', ' ')
        except Exception as e:
            print(e)
            species_name = ''
        return species_name

    def get_species_name_value(self, obj):
        try:
            species_name_value = obj.species_name
        except Exception as e:
            print(e)
            species_name_value = ''
        return species_name_value

    def get_atlas_name(self, obj):
        try:
            if obj.atlas_type == 'Project':
                atlas_name = str(obj.atlas_name).split('_')[1]
            else:
                atlas_name = obj.atlas_name
        except Exception as e:
            print(e)
            atlas_name = ''
        return atlas_name

    def get_atlas_name_value(self, obj):
        try:
            atlas_name_value = obj.atlas_name
        except Exception as e:
            print(e)
            atlas_name_value = ''
        return atlas_name_value


class CellMarkerDownloadListSerializer(serializers.ModelSerializer):
    species_name = serializers.SerializerMethodField()
    species_name_value = serializers.SerializerMethodField()

    class Meta:
        model = CellMarkerDownload
        fields = ['species_name', 'species_name_value', 'tissue', 'source', 'size', 'md5',
                  'last_update']

    def get_species_name(self, obj):
        try:
            species_name = str(obj.species_name).replace('_', ' ')
        except Exception as e:
            print(e)
            species_name = ''
        return species_name

    def get_species_name_value(self, obj):
        try:
            species_name_value = obj.species_name
        except Exception as e:
            print(e)
            species_name_value = ''
        return species_name_value


class ClusterMarkerDownloadListSerializer(serializers.ModelSerializer):
    species_name = serializers.SerializerMethodField()
    species_name_value = serializers.SerializerMethodField()

    class Meta:
        model = ClusterMarkerDownload
        fields = ['species_name', 'species_name_value', 'tissue', 'source', 'size', 'md5',
                  'last_update']

    def get_species_name(self, obj):
        try:
            species_name = str(obj.species_name).replace('_', ' ')
        except Exception as e:
            print(e)
            species_name = ''
        return species_name

    def get_species_name_value(self, obj):
        try:
            species_name_value = obj.species_name
        except Exception as e:
            print(e)
            species_name_value = ''
        return species_name_value


class CellTypeRelaRelationsSerializer(serializers.ModelSerializer):
    model = CellTypeRelations

    class Meta:
        fields = ['species_name', 'tissue_name', 'L1', 'L2', 'L3']


class CellTypeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CellTypeDetails
        fields = ["po_id", "name", "other_names", "description", "link"]


class GeneDetailsInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeneDetailsInfo
        fields = ['scaffold', 'start', 'end', 'strand', 'gene_id', 'gene_symbol', 'description']


class SpeciesMappingInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpeciesMappingInfo
        fields = ['species', 'tissue', 'mapping']