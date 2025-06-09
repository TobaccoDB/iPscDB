#!/usr/bin/python
"""
DESCRIPTION
Frame for parsing BLAST report
AUTHOR
Wubin Qu: quwubin@gmail.com
"""
from Bio.Blast import NCBIXML

from plant_marker.apps.plant_home.models import GeneDetailsInfo


def parse_blast_xml(xml_name, search_method, species_name):
    hit_data = list()
    # queryset_cell_home_info = CellHomeInfo.objects.all()
    # queryset_base_info = SearchBasicInfo.objects.all()
    blast_records = NCBIXML.parse(open(xml_name))
    for blast_record in blast_records:
        if blast_record.alignments:
            for alignment in blast_record.alignments:
                for hsp in alignment.hsps:
                    if not alignment.hit_def:
                        continue
                    gene_id = alignment.hit_def.split('|')[0]
                    gene_details = GeneDetailsInfo.objects.filter(gene_id__icontains=gene_id.split('.')[0].strip())
                    if not (gene_details.exists()):
                        continue
                    gene_details = gene_details.first()
                    hsp_data = dict()
                    hsp_data["id"] = gene_details.id
                    hsp_data["description"] = gene_details.description
                    hsp_data["species_name"] = species_name
                    hsp_data["hits"] = gene_id
                    hsp_data["hit_id"] = gene_id
                    hsp_data["query_id"] = blast_record.query
                    hsp_data["query"] = hsp.query
                    hsp_data["match"] = hsp.match
                    hsp_data["sbjct"] = hsp.sbjct
                    hsp_data["query_start"] = hsp.query_start
                    hsp_data["query_end"] = hsp.query_end
                    hsp_data["bits"] = int(hsp.bits)
                    hsp_data["sbjct_start"] = hsp.sbjct_start
                    hsp_data["sbjct_end"] = hsp.sbjct_end
                    hsp_data["score"] = int(hsp.score)
                    hsp_data["strand"] = '/'.join(hsp.strand) if search_method == "blastn" else ''
                    hsp_data["align_length"] = hsp.align_length
                    hsp_data["identities"] = hsp.identities
                    hsp_data["expect"] = hsp.expect
                    hsp_data["positives"] = hsp.positives
                    hsp_data["alignment_length"] = alignment.length
                    hit_data.append(hsp_data)
    # 排序
    hit_data.sort(key=lambda a: a["identities"], reverse=True)
    return hit_data
