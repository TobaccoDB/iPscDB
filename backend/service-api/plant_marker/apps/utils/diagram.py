a = {
    'name': 'data',
    'children': [
        {
            'name': 'converters',
            'children': [
                {'name': 'Converters'},
                {'name': 'DelimitedTextConverter'}
            ]
        },
        {
            'name': 'DataUtil',
        }
    ]
}

RootTip = {

}

all_tissue_structure_data = {
    'name': 'RootTip',
    'children': [
        {'name': 'Stele',
         'children': [
             {
                 'name': 'Phloem',
                 'children': [
                     {
                         'name': 'Protophloem',
                         'children': [
                             {'name': 'Phloem sieve element'},
                         ]
                     },
                     {
                         'name': 'Metaphloem',
                         'children': [
                             {'name': 'Phloem companion cell'},
                             {'name': 'Phloem sieve element'},
                         ]

                     },
                 ]
             },
             {
                 'name': 'Procambium',
                 'children': [
                     {
                         'name': 'Phloem procambium',
                     },
                     {
                         'name': 'Xylem procambium',

                     },
                 ]
             },
             {
                 'name': 'Xylem',
                 'children': [
                     {
                         'name': 'Metaxylem',
                     },
                     {
                         'name': 'Protoxylem',

                     },
                 ]
             },
             {
                 'name': 'Pericycle',
                 'children': [
                     {
                         'name': 'Phloem pole pericycle',
                     },
                     {
                         'name': 'Xylem pole pericycle',

                     },
                 ]
             },
         ], },
        {'name': 'Epidermis',
         'children': [
             {
                 'name': 'Trichoblast (Root hair cell)',

             },
             {'name': 'Atrichoblast (Non-hair cell)', }
         ]
         },
        ####
        {'name': 'Stem cell niche(Initial cell/Root meristem/Dividing cell)',
         'children': [
             {'name': 'Quiescent center'},
             {'name': 'Cortex/endodermis initial'},
             {'name': 'Epidermis/lateral root cap initial'},
             {
                 'name': 'Vascular initials',
                 'children': [
                     {'name': 'Stele/procambium initial'},
                     {'name': 'Pericycle initial'}
                 ]
             },
             {'name': 'Columella initial'},
         ]
         },
        {
            'name': 'Columella (Columella root cap)'
        },
        {
            'name': 'Cortex',
            'children': [
                {'name': 'Exodermis'},
                {'name': 'Cortex parenchyma'},
                {'name': 'Root endodermis'},
                {'name': 'Casparian strip'},
            ]
        },
        {
            'name': 'Lateral root cap',
        },

    ]
}

all_tissue_Leaf_structure_data = {
    'name': 'Leaf',
    'children': [
        {'name': 'Mesophyll',
         'children': [
             {'name': 'Palisade mesophyll'},
             {'name': 'Spongy mesophyll'},
             {'name': 'Myrosin idioblast（Myrosin cell）'},

         ]
         },
        {'name': 'Epidermis',
         'children': [
             {'name': 'Protoderm cell',
              'children': [{'name': 'Proliferating cell'}]
              },
             {
                 'name': 'Upper epidermis',
                 'children': [{'name': 'Adaxial pavement cell'}]
             },
             {
                 'name': 'Lower epidermis',
                 'children': [{'name': 'Adaxial pavement cell'}]

             }, {
                 'name': 'Meristemoid mother cell',
             }, {
                 'name': 'Meristemoid cell',
             }, {
                 'name': 'Guard cell',
                 'children': [
                     {'name': 'Guard mother cell',
                      }, {'name': 'Young guard cell',
                          },
                 ]
             }, {
                 'name': 'Pavement cell'},
             {
                 'name': 'Trichome （Epidermal hair）',
                 'children': [{'name': 'Basal cell'}]
             }
         ]
         },
        {'name': 'Vasculature',
         'children': [
             {'name': 'Phloem',
              'children': [
                  {'name': 'Protophloem'},
                  {'name': 'Metaphloem'},
                  {'name': 'Phloem sieve element'},
                  {'name': 'Phloem companion cell'},
                  {'name': 'Phloem precursor'},
              ]
              },
             {
                 'name': "Xylem",
                 'children': [
                     {'name': 'Metaxylem'},
                     {'name': 'Protoxylem'},
                     {'name': 'sieve element '},
                     {'name': 'companion cell'},
                     {'name': 'Xylem precursor'},
                 ]
             },
             {'name': "Sclerenchyma"},
             {'name': "Parenchyma",
              'children': [
                  {'name': 'Phloem parenchyma'},
                  {'name': 'Xylem parenchyma'},
              ]
              },
             {'name': "Bundle sheath"},
             {'name': "Fiber"},
             {'name': "Cambium",
              'children': [
                  {'name': 'Procambium'},
                  {'name': 'Preprocambium'},
              ]
              },

         ]
         },
        {'name': 'Hydathode',
         'children': [
             {'name': 'Guard cell'},
             {'name': 'Epithem'},
             {'name': 'Epidermis'},
             {'name': 'Xylem'},
         ]
         },
        {'name': 'Initial cell'}

    ]
}
