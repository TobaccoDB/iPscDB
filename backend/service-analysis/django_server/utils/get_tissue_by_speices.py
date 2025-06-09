def get_tissue(species_name):
    dic = {
        "Arabidopsis_thaliana": [
            {'name': 'Embryo', 'value': 'Embryo'},
            {'name': 'Hypocotyl callus', 'value': 'Hypocotyl_callus'},
            {'name': 'Inflorescence', 'value': 'Inflorescence'},
            {'name': 'Leaf', 'value': 'Leaf'},
            {'name': 'Pollen', 'value': 'Pollen'},
            {'name': 'Root', 'value': 'Root'},
            {'name': 'Root tip', 'value': 'Root_tip'},
            {'name': 'Vegetative shoot apex', 'value': 'Vegetative_shoot_apex'}
        ],
        "Bombax_ceiba": [{'name': 'Ovule inner integument', 'value': 'Ovule_inner_integument'}],
        "Brassica_rapa": [{'name': 'Rosette leaf', 'value': 'Rosette_leaf'}],
        "Catharanthus_roseus": [{'name': 'Leaf', 'value': 'Leaf'}],
        "Fragaria_vesca": [{'name': 'The first true leaves', 'value': 'The_first_true_leaves'}],
        "Glycine_max": [{'name': 'Nodule root', 'value': 'Nodule_root'}],
        "Gossypium_bickii": [{'name': 'Cotyledon', 'value': 'Cotyledon'}],
        "Gossypium_hirsutumv": [{'name': 'Ovule_outer integum', 'value': 'Ovule_outer_integum'}],
        "Manihot_esculenta": [{'name': 'Tuberous root', 'value': 'Tuberous_root'}],
        "Marchantia_polymorpha": [{'name': 'Tip base', 'value': 'Tip_base'}],
        "Medicago_truncatula": [{'name': 'Root', 'value': 'Root'}],
        "Nicotiana_attenuata": [{'name': 'Corolla', 'value': 'Corolla'}],
        "Oryza_sativa": [
            {'name': 'Flag leaf and inflorescence', 'value': 'Flag_leaf_and_inflorescence'},
            {'name': 'Inflorescence', 'value': 'Inflorescence'},
            {'name': 'Leaf', 'value': 'Leaf'},
            {'name': 'Pistil', 'value': 'Pistil'},
            {'name': 'Root', 'value': 'Root'},
            {'name': 'Root tip', 'value': 'Root_tip'}],
        "Phalaenopsis_Big_Chili": [{'name': 'Flower', 'value': 'Flower'}],
        "Phyllostachys_edulis": [{'name': 'Root tip', 'value': 'Root_tip'}],
        "populus_alba_var._pyramidalis": [
            {'name': 'Bark tissue', 'value': 'Bark tissue'},
            {'name': 'Wood tissue', 'value': 'Wood_tissue'}],
        "Populus_alba_x_glandulosa": [{'name': 'Stem stele', 'value': 'Stem_stele'}],
        "Populus_tremula_x_alba": [{'name': 'Shoot apices', 'value': 'Shoot_apices'}],
        "Populus_trichocarpa": [{'name': 'Stem', 'value': 'Stem'}],
        "Solanum_lycopersicum": [
            {'name': 'Stem-Borne Root', 'value': 'Stem-Borne_Root'},
            {'name': 'Vegetative shoot apex', 'value': 'Vegetative_shoot_apex'}],
        "Triticum_aestivum": [{'name': 'Root tip', 'value': 'Root_tip'}],
        "Zea_mays": [
            {'name': 'Leaf', 'value': 'Leaf'},
            {'name': 'Ear inflorescence', 'value': 'Ear_inflorescence'},
            {'name': 'Vegetative shoot apex', 'value': 'Vegetative_shoot_apex'},
            {'name': 'Root tip', 'value': 'Root_tip'}],
    }
    # 检查物种名是否在数据中
    if species_name in dic:
        return {"code": 200, "data": dic[species_name]}
    else:
        return {"code": 404, "message": "Species not found"}
