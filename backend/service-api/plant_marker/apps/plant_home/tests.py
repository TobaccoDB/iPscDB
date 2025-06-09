# # @list_route(methods=('get',), url_path='atlas_tissue_count')
# # def atlas_tissue_count(self, request, *args, **kwargs):
# #     """首页物种相关统计"""
# #
# #     root_list = ['Dividing', 'Stem Cell Niche', 'Atrichoblast', 'Cortex', 'Protophloem', 'Epidermis',
# #                  'Metaphloem & Companion Cell', 'Columella', 'Quiescent Center', 'Phloem', 'Lateral Root Cap',
# #                  'Procambium',
# #                  'Xylem', 'Initials', 'Root Hair Cell', 'Trichoblast', 'Protoxylem', 'Xylem Pole Pericycle',
# #                  'Phloem Pole Pericycle', 'Endodermis', 'Metaxylem', 'Pericycle']
# #     cell_data_list = []
# #     for one in root_list:
# #         cell_count = list(set(LiteratureInfo.objects.filter(doi=one).values_list('pmid', flat=True)))
# #         cell_data_list += cell_count
# #     print(len(list(set(cell_data_list))))
# #     return JSONResponse(data=cell_data_list)
# # import re
# #
# # result = '[1] 245\n[1] 10377\n[1] 500\n[1] 170328\n[1] 0\n[1] 17.50742\n[1] 0\n[1] 11.00746\n[1] -298.9358\n[1] 5677.252\n[1] 500\n[1] 170328\n[1] 0\n[1] 15\n[1] 0\n[1] 15\n'
# # # re_c = '\d+\.\d+|\d+'
# # re_c = '-?[0-9]+\.[0-9]*|-?[0-9]+'
# # result_list = re.findall(re_c, result)
# #
# # print(result_list)
# # a = ['1', '245', '1', '10377', '1', '500', '170328', '0', '1', '17', '50742', '1', '0', '1', '11', '00746', '1',
# #      '-298.9358', '1', '5677', '252', '1', '500', '1', '170328', '1', '0', '1', '15', '1', '0', '1', '15']
# # print(a)
# #
# # t = '&filter_min_Feature_RNA_cutmin=245&filter_max_Feature_RNA_cutax=10000&filter_min_mt_cutmin=0&filter_max_mt_cutmax=17&filter_min_pt_cutmin=1&filter_max_pt_cutmax=10'
# # a=['1','2','3']
# #
# umap_path = os.path.join(
#                 settings.UMAP_DIR, species_name, tissue + '/' + 'umap_data.csv')
#             gene_path = os.path.join(
#                 settings.GENE_EXPRESSION_FILE, species_name, tissue, gene_id + '.csv')
#             expression_data = pd.read_csv(
#                 umap_path, usecols=['Cell_ID', 'UMAP_1', 'UMAP_2', 'Clusters'])
#             # umpa 数据返回所有的点
#             if os.path.exists(gene_path):
#                 gene_data = pd.read_csv(gene_path)
#                 expression_data = pd.merge(
#                     expression_data, gene_data, how='left', on='Cell_ID').fillna(0)
#                 expression_data['value'] = expression_data['value'].astype(
#                     str).str[:4].astype(float)
#             else:
#                 expression_data['value'] = 1
#             expression_data = expression_data.drop('Cell_ID', axis=1)
#             umap_data = expression_data.iloc[1:20000]
#             expression_data_list = eval(
#                 expression_data.to_json(orient="split")).get('data', '')
#             clusters_data = umap_data.groupby('Clusters')
#             data_list = []
#             for group_name, group_data in clusters_data:
#                 group_data = group_data[['UMAP_1', 'UMAP_2']]
#                 data = {
#                     'name': group_name,
#                     'data': group_data.to_dict('split').get('data', []),
#                     'sort': int(group_name.split(":")[0])
#                 }
#                 data_list.append(data)
#
#             data_list = sorted(data_list, key=lambda x: x['sort'])
#
#             umap_data = umap_data.drop('Clusters', axis=1)
#             expression_data_list = eval(
#                 umap_data.to_json(orient="split")).get('data', '')
#             data = {
#                 'umpa_data': data_list,
#                 'expression_data': expression_data_list,
#             }
#         except Exception as e:
#             print(e)
#             data = {
#                 'expression_data': []
#             }
