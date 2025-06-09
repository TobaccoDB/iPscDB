from django.conf import settings

markers_tree_data = [
  {
    "name": "Arabidopsis thaliana",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Arabidopsis_thaliana/Arabidopsis_thaliana.png",
    "gene_number": 144822,
    "classic_number": 1843,
    "node_number": 150,
    "children": [
      {
        "name": "Root",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Arabidopsis_thaliana/Root/Root.png",
        "gene_number": 91050,
        "classic_number": 1008,
        "node_number": 36,
        "children": [
          {
            "name": "Root epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 1649,
            "classic_number": 25,
            "node_number": 3,
            "children": [
              {
                "name": "Non-hair",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 5580,
                "classic_number": 69,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Root hair",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 7451,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Trichoblast",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 69,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 6,
            "children": [
              {
                "name": "Cambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Root cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 5004,
                "classic_number": 90,
                "node_number": 1,
                "children": [
                  {
                    "name": "Root endodermis",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 4757,
                    "classic_number": 121,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Root cap",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 3211,
                "classic_number": 1,
                "node_number": 2,
                "children": [
                  {
                    "name": "Lateral root cap",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 6883,
                    "classic_number": 72,
                    "node_number": 0
                  },
                  {
                    "name": "Columella root cap",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 5852,
                    "classic_number": 76,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Root stele",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 2301,
            "classic_number": 33,
            "node_number": 14,
            "children": [
              {
                "name": "Pericycle",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1111,
                "classic_number": 38,
                "node_number": 3,
                "children": [
                  {
                    "name": "Phloem pole pericycle",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 3309,
                    "classic_number": 6,
                    "node_number": 0
                  },
                  {
                    "name": "Xylem pole pericycle",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 3019,
                    "classic_number": 6,
                    "node_number": 0
                  },
                  {
                    "name": "Lateral root primordia",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 632,
                    "classic_number": 14,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Phloem/Pericycle",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 161,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 2203,
                "classic_number": 54,
                "node_number": 4,
                "children": [
                  {
                    "name": "Sieve element",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 4031,
                    "classic_number": 11,
                    "node_number": 0
                  },
                  {
                    "name": "Companion cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 3540,
                    "classic_number": 19,
                    "node_number": 0
                  },
                  {
                    "name": "Phloem parenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 1565,
                    "classic_number": 0,
                    "node_number": 0
                  },
                  {
                    "name": "Protophloem",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 5,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Root procambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 2611,
                "classic_number": 37,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 2034,
                "classic_number": 86,
                "node_number": 2,
                "children": [
                  {
                    "name": "Protoxylem",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 4097,
                    "classic_number": 20,
                    "node_number": 0
                  },
                  {
                    "name": "Metaxylem",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 4465,
                    "classic_number": 3,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 1835,
            "classic_number": 0,
            "node_number": 8,
            "children": [
              {
                "name": "G2/M phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 5448,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "G1/10 phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Stem cell niche",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1883,
                "classic_number": 26,
                "node_number": 3,
                "children": [
                  {
                    "name": "Quiescent center",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 99,
                    "node_number": 0
                  },
                  {
                    "name": "Lateral root cap initial",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 4,
                    "node_number": 0
                  },
                  {
                    "name": "Columella root cap initial",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 2,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Dividing cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 7,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Initial cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell1",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "S phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 5219,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Leaf",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Arabidopsis_thaliana/Leaf/Leaf.png",
        "gene_number": 38533,
        "classic_number": 437,
        "node_number": 29,
        "children": [
          {
            "name": "Leaf epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 1300,
            "classic_number": 21,
            "node_number": 4,
            "children": [
              {
                "name": "Leaf pavement cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 4078,
                "classic_number": 1,
                "node_number": 2,
                "children": [
                  {
                    "name": "Leaf abaxial pavement cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 1,
                    "node_number": 0
                  },
                  {
                    "name": "Leaf adaxial pavement cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 2,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Leaf guard cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 4664,
                "classic_number": 16,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 8,
            "children": [
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 7588,
                "classic_number": 65,
                "node_number": 2,
                "children": [
                  {
                    "name": "Spongy mesophyll",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 987,
                    "classic_number": 2,
                    "node_number": 0
                  },
                  {
                    "name": "Palisade mesophyll",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 1497,
                    "classic_number": 5,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Bundle sheath",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1375,
                "classic_number": 24,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Cambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 4,
                "node_number": 1,
                "children": [
                  {
                    "name": "Procambium",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 39,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Endodermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 18,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Hydathodes",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 784,
            "classic_number": 15,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 491,
            "classic_number": 0,
            "node_number": 8,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1544,
                "classic_number": 3,
                "node_number": 3,
                "children": [
                  {
                    "name": "Phloem parenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 3015,
                    "classic_number": 16,
                    "node_number": 0
                  },
                  {
                    "name": "Sieve element",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 289,
                    "classic_number": 4,
                    "node_number": 0
                  },
                  {
                    "name": "Companion cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 2415,
                    "classic_number": 29,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 3154,
                "classic_number": 10,
                "node_number": 1,
                "children": [
                  {
                    "name": "Xylem parenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 11,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Tracheary element",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Vasculature cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 28,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 1111,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "S phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1792,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "G2/M phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1425,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Idioblast cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Stress response",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 1024,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Shoot axis apex",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Arabidopsis_thaliana/Shoot_axis_apex/Shoot_axis_apex.png",
        "gene_number": 2609,
        "classic_number": 49,
        "node_number": 12,
        "children": [
          {
            "name": "Shoot apical meristem",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 250,
            "classic_number": 4,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 403,
                "classic_number": 4,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Shoot system epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 285,
            "classic_number": 8,
            "node_number": 1,
            "children": [
              {
                "name": "Guard cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 251,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 401,
            "classic_number": 14,
            "node_number": 2,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Companion cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 567,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "G2/M phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 296,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "S phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 156,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Proliferating cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Inflorescence",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Arabidopsis_thaliana/Inflorescence/Inflorescence.png",
        "gene_number": 1315,
        "classic_number": 111,
        "node_number": 18,
        "children": [
          {
            "name": "Shoot apical meristem",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Flower meristem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 45,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Anther",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 20,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 4,
            "children": [
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 123,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 131,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Cambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Epidermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 10,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 13,
            "node_number": 4,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 346,
                "classic_number": 10,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 172,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Xylem parenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 5,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Vascular cambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 125,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Shoot system epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 102,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 13,
            "node_number": 3,
            "children": [
              {
                "name": "G2/M phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 170,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "S phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 101,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Dividing cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 24,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Pollen",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Arabidopsis_thaliana/Pollen/Pollen.png",
        "gene_number": 3265,
        "classic_number": 22,
        "node_number": 6,
        "children": [
          {
            "name": "Microspore nuclei",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 999,
            "classic_number": 1,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Vegetative nuclei",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 905,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Generative nuclei",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 201,
            "classic_number": 5,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Sperm nuclei",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 557,
            "classic_number": 12,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Contaminating nuclei",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 370,
            "classic_number": 1,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Transitory",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 233,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Hypocotyl callus",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Arabidopsis_thaliana/Hypocotyl_callus/Hypocotyl_callus.png",
        "gene_number": 2587,
        "classic_number": 0,
        "node_number": 5,
        "children": [
          {
            "name": "Outer cell layer",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 324,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Middle cell layer",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 4,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Inner cell layer",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 1089,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Explant vasculature and callus founder cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 901,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 269,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Ovule",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Arabidopsis_thaliana/Ovule/Ovule.png",
        "gene_number": 3126,
        "classic_number": 68,
        "node_number": 2,
        "children": [
          {
            "name": "Archesporial cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 923,
            "classic_number": 23,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Megaspore mother cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 1221,
            "classic_number": 45,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Callus",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Arabidopsis_thaliana/Callus/Callus.png",
        "gene_number": 0,
        "classic_number": 43,
        "node_number": 12,
        "children": [
          {
            "name": "Epidermis-like cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 4,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Lateral-root-cap-like cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 1,
            "node_number": 0,
            "children": []
          },
          {
            "name": "QC-like cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 6,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Vascular-initial-like cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 5,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Explant vasculature and callus founder cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 8,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Dividing cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 2,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Root cap",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Root hair",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 3,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 5,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Mesophyll",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 2,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 2,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Pericycle",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 3,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Embryo",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Arabidopsis_thaliana/Embryo/Embryo.png",
        "gene_number": 0,
        "classic_number": 52,
        "node_number": 6,
        "children": [
          {
            "name": "Columella initial",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 3,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Ground tissue initial",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 2,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Vascular initial",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 22,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Quiescent center initial",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 4,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Suspensor",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 11,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Upper inner periphery",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 10,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Root;Shoot",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Arabidopsis_thaliana/Root_Shoot/Root_Shoot.png",
        "gene_number": 0,
        "classic_number": 53,
        "node_number": 15,
        "children": [
          {
            "name": "Epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Trichoblast",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 7,
            "node_number": 5,
            "children": [
              {
                "name": "Cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 7,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Endodermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Epidermal hypocotyl",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 7,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Cambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Procambium",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 1,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 18,
            "node_number": 3,
            "children": [
              {
                "name": "Pericycle",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Dividing cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Initial cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Shoot",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Arabidopsis_thaliana/Shoot/Shoot.png",
        "gene_number": 7117,
        "classic_number": 28,
        "node_number": 18,
        "children": [
          {
            "name": "Epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 1,
            "node_number": 2,
            "children": [
              {
                "name": "Cotyledon epidermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1011,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Hypocotyl epidermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1032,
                "classic_number": 4,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 6,
            "children": [
              {
                "name": "Cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 203,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Endodermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 161,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Parenchyma cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 415,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Companion cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 314,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1426,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Procambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 883,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Sieve element",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 332,
                    "classic_number": 3,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 581,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Shoot apical meristem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 392,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              },
              {
                "name": "G2/M phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 280,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              },
              {
                "name": "S phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 87,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Oryza sativa",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Oryza_sativa/Oryza_sativa.png",
    "gene_number": 17838,
    "classic_number": 311,
    "node_number": 76,
    "children": [
      {
        "name": "Root",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Oryza_sativa/Root/Root.png",
        "gene_number": 9107,
        "classic_number": 138,
        "node_number": 20,
        "children": [
          {
            "name": "Root epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 1012,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Root hair",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1518,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Trichoblast",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 8,
            "children": [
              {
                "name": "Root cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 507,
                "classic_number": 0,
                "node_number": 2,
                "children": [
                  {
                    "name": "Root endodermis",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 826,
                    "classic_number": 1,
                    "node_number": 0
                  },
                  {
                    "name": "Exodermis",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 216,
                    "classic_number": 1,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Root cap",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 832,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Lateral root cap",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 2,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Sclerenchyma",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 743,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Cambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Procambium",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 3,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Root stele",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 1116,
            "classic_number": 0,
            "node_number": 5,
            "children": [
              {
                "name": "Pericycle",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 315,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 348,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 2,
                "children": [
                  {
                    "name": "Protoxylem",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 711,
                    "classic_number": 0,
                    "node_number": 0
                  },
                  {
                    "name": "Metaxylem",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 842,
                    "classic_number": 8,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 121,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Stem cell niche",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 4,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Leaf",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Oryza_sativa/Leaf/Leaf.png",
        "gene_number": 1123,
        "classic_number": 14,
        "node_number": 12,
        "children": [
          {
            "name": "Leaf epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 458,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Leaf guard cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 317,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Cambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Procambium",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 277,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Leaf sheath cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Initial cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 71,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Inflorescence",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Oryza_sativa/Inflorescence/Inflorescence.png",
        "gene_number": 282,
        "classic_number": 123,
        "node_number": 7,
        "children": [
          {
            "name": "Inflorescence axis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 49,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Spikelet",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 32,
            "classic_number": 31,
            "node_number": 2,
            "children": [
              {
                "name": "Spikelet floret",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 54,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Spikelet meristem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 42,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Inflorescence meristem",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 64,
            "classic_number": 92,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Branch meristem",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 24,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Flag leaf",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 17,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Root;Leaf",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Oryza_sativa/Root_Leaf/Root_Leaf.png",
        "gene_number": 6563,
        "classic_number": 36,
        "node_number": 19,
        "children": [
          {
            "name": "Epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 347,
            "classic_number": 2,
            "node_number": 2,
            "children": [
              {
                "name": "Guard cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Trichome",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 8,
            "children": [
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 12,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Mesophyll/Cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 267,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Mesophyll precursor/Root endodermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 342,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Root exodermis/Sclerenchym",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 745,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Pericycle",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 689,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Mestome sheath",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 472,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Parenchyma",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 235,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Fiber cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 370,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Root stele",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 863,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 259,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 351,
                "classic_number": 7,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 702,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Procambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 486,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Initial cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 435,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Pistil",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Oryza_sativa/Pistil/Pistil.png",
        "gene_number": 684,
        "classic_number": 0,
        "node_number": 12,
        "children": [
          {
            "name": "Stigma",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 91,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Style",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 62,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Ovary wall",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 85,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Outer ovary wall",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 90,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ovule",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 23,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "CT-Ovule",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 50,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "S-Ovule",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 5,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Integument",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 43,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Inner ovary wall/Outer integument",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 70,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Nucellus",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 69,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Stamen residue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 26,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 70,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Zea mays",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Zea_mays/Zea_mays.png",
    "gene_number": 20896,
    "classic_number": 325,
    "node_number": 80,
    "children": [
      {
        "name": "Root",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Zea_mays/Root/Root.png",
        "gene_number": 8531,
        "classic_number": 173,
        "node_number": 25,
        "children": [
          {
            "name": "Root epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 564,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Root hair",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 361,
                "classic_number": 19,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Non-hair",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Trichoblast",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 5,
            "children": [
              {
                "name": "Root cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 709,
                "classic_number": 0,
                "node_number": 2,
                "children": [
                  {
                    "name": "Root endodermis",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 790,
                    "classic_number": 2,
                    "node_number": 0
                  },
                  {
                    "name": "Root exodermis",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 314,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Root cap",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1334,
                "classic_number": 6,
                "node_number": 1,
                "children": [
                  {
                    "name": "Lateral root cap",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 10,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Root stele",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 801,
            "classic_number": 0,
            "node_number": 10,
            "children": [
              {
                "name": "Root pith",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 133,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 549,
                "classic_number": 5,
                "node_number": 2,
                "children": [
                  {
                    "name": "Metaxylem",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 1,
                    "node_number": 0
                  },
                  {
                    "name": "Protoxylem",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 2,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 1,
                "node_number": 3,
                "children": [
                  {
                    "name": "Companion cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 750,
                    "classic_number": 2,
                    "node_number": 0
                  },
                  {
                    "name": "Protophloem",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 648,
                    "classic_number": 0,
                    "node_number": 0
                  },
                  {
                    "name": "Sieve element",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 2,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Pericycle",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 223,
                "classic_number": 7,
                "node_number": 1,
                "children": [
                  {
                    "name": "Phloem pole pericycle",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 1,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 968,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Stem cell niche",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 387,
                "classic_number": 0,
                "node_number": 2,
                "children": [
                  {
                    "name": "Quiescent center",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 15,
                    "node_number": 0
                  },
                  {
                    "name": "Columella root cap initial",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "name": "Ear inflorescence",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Zea_mays/Ear_inflorescence/Ear_inflorescence.png",
        "gene_number": 3260,
        "classic_number": 22,
        "node_number": 22,
        "children": [
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 5,
            "children": [
              {
                "name": "Cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 341,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Bundle sheath",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 200,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Epidermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Determinate lateral organ",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 474,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Leaf adaxial pavement cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 4,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 5,
            "children": [
              {
                "name": "Pith",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 110,
                "classic_number": 4,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 633,
                "classic_number": 0,
                "node_number": 2,
                "children": [
                  {
                    "name": "Companion cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 2,
                    "node_number": 0
                  },
                  {
                    "name": "Sieve element",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 2,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 142,
                "classic_number": 4,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ear meristem",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 6,
            "children": [
              {
                "name": "Meristem epidermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 321,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Meristem boundary",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 120,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Meristem base",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 265,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Adaxial meristem periphery",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 187,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Determinate lateral organ",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 474,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Spikelet meristem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "G2/M phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 361,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "S phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 106,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Leaf",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Zea_mays/Leaf/Leaf.png",
        "gene_number": 6142,
        "classic_number": 94,
        "node_number": 18,
        "children": [
          {
            "name": "Leaf primordium",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 18,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Leaf epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 126,
            "classic_number": 0,
            "node_number": 6,
            "children": [
              {
                "name": "Leaf pavement cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 2,
                "children": [
                  {
                    "name": "Pavement cell-A",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 80,
                    "classic_number": 0,
                    "node_number": 0
                  },
                  {
                    "name": "Pavement cell-N",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 122,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Leaf adaxial pavement cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Leaf guard cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 122,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Leaf subsidiary cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 137,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 3785,
                "classic_number": 6,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Bundle sheath",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1245,
                "classic_number": 12,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Endodermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 92,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Vasculature cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "S phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 75,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "G2/M phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 60,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Contamination",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 280,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Shoot axis apex",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Zea_mays/Shoot_axis_apex/Shoot_axis_apex.png",
        "gene_number": 2627,
        "classic_number": 36,
        "node_number": 10,
        "children": [
          {
            "name": "Leaf primordium",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 377,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Shoot apical meristem",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 209,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Shoot system epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 341,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Shoot system epidermis L1",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Leaf rim",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 191,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 348,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Vasculature cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "G2/M phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 639,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "S phase",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 522,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Gossypium hirsutum",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Gossypium_hirsutum/Gossypium_hirsutum.png",
    "gene_number": 4821,
    "classic_number": 116,
    "node_number": 27,
    "children": [
      {
        "name": "Ovule",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Gossypium_hirsutum/Ovule/Ovule.png",
        "gene_number": 0,
        "classic_number": 68,
        "node_number": 5,
        "children": [
          {
            "name": "Ovule outer integument",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 4,
            "children": [
              {
                "name": "Epidermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Fiber cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Outer pigment layer",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 8,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Endodermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 37,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Hypocotyl",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Gossypium_hirsutum/Hypocotyl/Hypocotyl.png",
        "gene_number": 379,
        "classic_number": 28,
        "node_number": 9,
        "children": [
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Cambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 150,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 42,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 131,
            "classic_number": 3,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 4,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 4,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Sieve element",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 4,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 3,
                "node_number": 1,
                "children": [
                  {
                    "name": "Xylem parenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 50,
                    "classic_number": 4,
                    "node_number": 0
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "name": "Leaf",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Gossypium_hirsutum/Leaf/Leaf.png",
        "gene_number": 1112,
        "classic_number": 20,
        "node_number": 9,
        "children": [
          {
            "name": "Leaf epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 106,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Leaf guard cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 402,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Secretory glandular cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 190,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 132,
                "classic_number": 4,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Proliferating cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 218,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Vasculature cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 64,
                "classic_number": 7,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Anther",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Gossypium_hirsutum/Anther/Anther.png",
        "gene_number": 1265,
        "classic_number": 0,
        "node_number": 8,
        "children": [
          {
            "name": "Epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 135,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Endothecium",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 323,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Middle cell layer",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 112,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Tapetum cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 453,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Microspore after meiotic",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 22,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Vascular region",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 137,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Connective cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 31,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Meiotic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 52,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Solanum lycopersicum",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Solanum_lycopersicum/Solanum_lycopersicum.png",
    "gene_number": 3454,
    "classic_number": 16,
    "node_number": 13,
    "children": [
      {
        "name": "Shoot axis apex",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Solanum_lycopersicum/Shoot_axis_apex/Shoot_axis_apex.png",
        "gene_number": 3299,
        "classic_number": 16,
        "node_number": 12,
        "children": [
          {
            "name": "Leaf marginal meristem",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 174,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Shoot system epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 549,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Trichome",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 751,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Abaxial epidermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 110,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 123,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 20,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 347,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Shoot apical meristem",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Rib Zone",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1225,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Leaf",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Solanum_lycopersicum/Leaf/Leaf.png",
        "gene_number": 1393,
        "classic_number": 0,
        "node_number": 9,
        "children": [
          {
            "name": "Leaf epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 100,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Trichome cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 467,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Leaf guard cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 194,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Mesophyll cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 100,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Proliferating cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 432,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Vasculature cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 100,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 155,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Populus alba × glandulosa",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Populus_alba_×_glandulosa/Populus_alba_×_glandulosa.png",
    "gene_number": 0,
    "classic_number": 66,
    "node_number": 10,
    "children": [
      {
        "name": "Stem",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Populus_alba_×_glandulosa/Stem/Stem.png",
        "gene_number": 0,
        "classic_number": 66,
        "node_number": 8,
        "children": [
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 4,
            "children": [
              {
                "name": "Vasculature cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 2,
                "children": [
                  {
                    "name": "Ray parenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 0,
                    "node_number": 0
                  },
                  {
                    "name": "Xylem precursor cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 3,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Fiber cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 15,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Uninfected cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 12,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Bombax ceiba",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Bombax_ceiba/Bombax_ceiba.png",
    "gene_number": 558,
    "classic_number": 53,
    "node_number": 5,
    "children": [
      {
        "name": "Ovule inner integument",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Bombax_ceiba/Ovule_inner_integument/Ovule_inner_integument.png",
        "gene_number": 311,
        "classic_number": 53,
        "node_number": 3,
        "children": [
          {
            "name": "Epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 219,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Fiber cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 92,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Ovary wall",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Medicago truncatula",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Medicago_truncatula/Medicago_truncatula.png",
    "gene_number": 2671,
    "classic_number": 95,
    "node_number": 16,
    "children": [
      {
        "name": "Root",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Medicago_truncatula/Root/Root.png",
        "gene_number": 2551,
        "classic_number": 95,
        "node_number": 14,
        "children": [
          {
            "name": "Root epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Non-hair",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 133,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Root hair",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 573,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Trichoblast",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 10,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Root cap",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 272,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Root cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 189,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Root endodermis",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 141,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Root stele",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 173,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 273,
                "classic_number": 6,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 343,
                "classic_number": 26,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Pericycle",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 264,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Stem cell niche",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 190,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Triticum aestivum",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Triticum_aestivum/Triticum_aestivum.png",
    "gene_number": 7572,
    "classic_number": 110,
    "node_number": 26,
    "children": [
      {
        "name": "Root",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Triticum_aestivum/Root/Root.png",
        "gene_number": 7572,
        "classic_number": 110,
        "node_number": 24,
        "children": [
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 5,
            "children": [
              {
                "name": "Root cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Root endodermis",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 208,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Root cap",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 550,
                "classic_number": 0,
                "node_number": 2,
                "children": [
                  {
                    "name": "Columella root cap",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 236,
                    "classic_number": 0,
                    "node_number": 0
                  },
                  {
                    "name": "Root broder",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 1154,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Root epidermis/Root cortex",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 239,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Root epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 30,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Root hair",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1107,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Root stele",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 11,
            "children": [
              {
                "name": "Pericycle",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 272,
                "classic_number": 0,
                "node_number": 2,
                "children": [
                  {
                    "name": "Phloem pole pericycle",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 773,
                    "classic_number": 5,
                    "node_number": 0
                  },
                  {
                    "name": "Xylem pole pericycle",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 921,
                    "classic_number": 5,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 3,
                "children": [
                  {
                    "name": "Sieve element",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 316,
                    "classic_number": 0,
                    "node_number": 0
                  },
                  {
                    "name": "Companion cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 471,
                    "classic_number": 5,
                    "node_number": 0
                  },
                  {
                    "name": "Protophloem",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 175,
                    "classic_number": 5,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 2,
                "children": [
                  {
                    "name": "Protoxylem",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 142,
                    "classic_number": 10,
                    "node_number": 0
                  },
                  {
                    "name": "Metaxylem",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 576,
                    "classic_number": 5,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Provascular",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 97,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 121,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Proximal meristem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 60,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Stem cell niche",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 124,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Nicotiana attenuata",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Nicotiana_attenuata/Nicotiana_attenuata.png",
    "gene_number": 932,
    "classic_number": 30,
    "node_number": 8,
    "children": [
      {
        "name": "Corolla",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Nicotiana_attenuata/Corolla/Corolla.png",
        "gene_number": 932,
        "classic_number": 30,
        "node_number": 7,
        "children": [
          {
            "name": "Pollen",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 94,
            "classic_number": 6,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 196,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Vasculature cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 4,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Parenchyma",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 374,
                "classic_number": 6,
                "node_number": 1,
                "children": [
                  {
                    "name": "Chlorenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 242,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 26,
            "classic_number": 14,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Manihot esculenta",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Manihot_esculenta/Manihot_esculenta.png",
    "gene_number": 5197,
    "classic_number": 28,
    "node_number": 20,
    "children": [
      {
        "name": "Tuberous root",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Manihot_esculenta/Tuberous_root/Tuberous_root.png",
        "gene_number": 5124,
        "classic_number": 28,
        "node_number": 18,
        "children": [
          {
            "name": "Root epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 252,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Root hair",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 354,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Trichoblast",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 5,
            "children": [
              {
                "name": "Root cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 334,
                "classic_number": 0,
                "node_number": 2,
                "children": [
                  {
                    "name": "Root exodermis",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 426,
                    "classic_number": 0,
                    "node_number": 0
                  },
                  {
                    "name": "Root endodermis",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Root cap",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Columella root cap",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Root stele",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 7,
            "children": [
              {
                "name": "Pericycle",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 145,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 423,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Phloem parenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 302,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 487,
                "classic_number": 2,
                "node_number": 1,
                "children": [
                  {
                    "name": "Metaxylem",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 852,
                    "classic_number": 3,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Root procambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 414,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Vascular bundle",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 144,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 991,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Fragaria vesca",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Fragaria_vesca/Fragaria_vesca.png",
    "gene_number": 4399,
    "classic_number": 44,
    "node_number": 14,
    "children": [
      {
        "name": "Leaf",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Fragaria_vesca/Leaf/Leaf.png",
        "gene_number": 4190,
        "classic_number": 44,
        "node_number": 12,
        "children": [
          {
            "name": "Hydathodes",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 297,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 448,
                "classic_number": 20,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Bundle sheath",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Leaf epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 3,
            "node_number": 2,
            "children": [
              {
                "name": "Adaxial epidermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 388,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Abaxial epidermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 809,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 524,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 495,
                "classic_number": 2,
                "node_number": 1,
                "children": [
                  {
                    "name": "Xylem parenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 301,
                    "classic_number": 2,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 928,
            "classic_number": 5,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Brassica rapa",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Brassica_rapa/Brassica_rapa.png",
    "gene_number": 3362,
    "classic_number": 62,
    "node_number": 13,
    "children": [
      {
        "name": "Leaf",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Brassica_rapa/Leaf/Leaf.png",
        "gene_number": 3175,
        "classic_number": 62,
        "node_number": 11,
        "children": [
          {
            "name": "Leaf epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 393,
            "classic_number": 6,
            "node_number": 1,
            "children": [
              {
                "name": "Leaf guard cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 415,
                "classic_number": 9,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 341,
                "classic_number": 15,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Bundle sheath",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 218,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 367,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 804,
                "classic_number": 4,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 301,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Vasculature cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 13,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 336,
            "classic_number": 6,
            "node_number": 1,
            "children": [
              {
                "name": "Proliferating cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 6,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Catharanthus roseus",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Catharanthus_roseus/Catharanthus_roseus.png",
    "gene_number": 1804,
    "classic_number": 80,
    "node_number": 28,
    "children": [
      {
        "name": "Leaf",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Catharanthus_roseus/Leaf/Leaf.png",
        "gene_number": 1763,
        "classic_number": 64,
        "node_number": 15,
        "children": [
          {
            "name": "Leaf epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 443,
            "classic_number": 9,
            "node_number": 1,
            "children": [
              {
                "name": "Leaf guard cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 4,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 177,
                "classic_number": 17,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Cambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Procambium",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 1,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Idioblast cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 170,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 464,
            "classic_number": 0,
            "node_number": 5,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 3,
                "children": [
                  {
                    "name": "Phloem parenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 172,
                    "classic_number": 5,
                    "node_number": 0
                  },
                  {
                    "name": "Companion cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 4,
                    "node_number": 0
                  },
                  {
                    "name": "Sieve element",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Vasculature cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 12,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 337,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Proliferating cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Root",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Catharanthus_roseus/Root/Root.png",
        "gene_number": 0,
        "classic_number": 16,
        "node_number": 10,
        "children": [
          {
            "name": "Root epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Non-hair",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Root cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Root endodermis",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 2,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Root cap",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 5,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Root stele",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Gossypium bickii",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Gossypium_bickii/Gossypium_bickii.png",
    "gene_number": 3226,
    "classic_number": 80,
    "node_number": 14,
    "children": [
      {
        "name": "Seed",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Gossypium_bickii/Seed/Seed.png",
        "gene_number": 3226,
        "classic_number": 80,
        "node_number": 12,
        "children": [
          {
            "name": "Leaf epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 257,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Leaf guard cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 117,
                "classic_number": 10,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1372,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 5,
            "children": [
              {
                "name": "Procambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 477,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 2,
                "children": [
                  {
                    "name": "Phloem parenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 210,
                    "classic_number": 0,
                    "node_number": 0
                  },
                  {
                    "name": "Companion cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 354,
                    "classic_number": 10,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 204,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Secretory tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Pigment gland",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 235,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Populus alba var. pyramidalis",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Populus_alba_var_pyramidalis/Populus_alba_var_pyramidalis.png",
    "gene_number": 10990,
    "classic_number": 108,
    "node_number": 17,
    "children": [
      {
        "name": "Stem",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Populus_alba_var_pyramidalis/Stem/Stem.png",
        "gene_number": 9501,
        "classic_number": 108,
        "node_number": 15,
        "children": [
          {
            "name": "Epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 445,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 4,
            "children": [
              {
                "name": "Cortex/Endodermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 524,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Endodermis",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 372,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Cortex/Endodermis initial",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 619,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Cork cambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 541,
                "classic_number": 9,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 7,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 3,
                "children": [
                  {
                    "name": "Sieve element",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 519,
                    "classic_number": 12,
                    "node_number": 0
                  },
                  {
                    "name": "Companion cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 922,
                    "classic_number": 5,
                    "node_number": 0
                  },
                  {
                    "name": "Phloem parenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 100,
                    "classic_number": 10,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Vascular cambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 563,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 1333,
                "classic_number": 25,
                "node_number": 1,
                "children": [
                  {
                    "name": "Xylem parenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 654,
                    "classic_number": 2,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Photosynthetic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 604,
            "classic_number": 31,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Glycine max",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Glycine_max/Glycine_max.png",
    "gene_number": 1626,
    "classic_number": 43,
    "node_number": 21,
    "children": [
      {
        "name": "Root",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Glycine_max/Root/Root.png",
        "gene_number": 1585,
        "classic_number": 43,
        "node_number": 19,
        "children": [
          {
            "name": "Root stele",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 238,
            "classic_number": 2,
            "node_number": 6,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 3,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Pericycle",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 1,
                "node_number": 2,
                "children": [
                  {
                    "name": "Phloem pole pericycle",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 1,
                    "node_number": 0
                  },
                  {
                    "name": "Xylem pole pericycle",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 1,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Root procambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Root epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 457,
            "classic_number": 5,
            "node_number": 1,
            "children": [
              {
                "name": "Trichoblast",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 5,
            "children": [
              {
                "name": "Root cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 6,
                "node_number": 3,
                "children": [
                  {
                    "name": "Inner cortex",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 112,
                    "classic_number": 1,
                    "node_number": 0
                  },
                  {
                    "name": "Outer cortex",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 106,
                    "classic_number": 1,
                    "node_number": 0
                  },
                  {
                    "name": "Root endodermis",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 1,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Bundle sheath",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 4,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Infected cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 362,
            "classic_number": 4,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Uninfected cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 310,
            "classic_number": 1,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Marchantia polymorpha",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Marchantia_polymorpha/Marchantia_polymorpha.png",
    "gene_number": 2773,
    "classic_number": 44,
    "node_number": 11,
    "children": [
      {
        "name": "Gemmae",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Marchantia_polymorpha/Gemmae/Gemmae.png",
        "gene_number": 2773,
        "classic_number": 44,
        "node_number": 9,
        "children": [
          {
            "name": "Air pore cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 300,
            "classic_number": 6,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Cell surrounding the notch",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 190,
            "classic_number": 4,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Gemma cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 443,
            "classic_number": 9,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Initials of assimillatory filament",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 58,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Mature cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 112,
            "classic_number": 4,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Mucilage hair",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 185,
            "classic_number": 5,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Oil body cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 271,
            "classic_number": 4,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Rhizoid",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 227,
            "classic_number": 4,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Ventral scale",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 59,
            "classic_number": 4,
            "node_number": 0,
            "children": []
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Arachis hypogaea",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Arachis_hypogaea/Arachis_hypogaea.png",
    "gene_number": 0,
    "classic_number": 40,
    "node_number": 12,
    "children": [
      {
        "name": "Leaf",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Arachis_hypogaea/Leaf/Leaf.png",
        "gene_number": 0,
        "classic_number": 40,
        "node_number": 10,
        "children": [
          {
            "name": "Leaf epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 5,
            "node_number": 1,
            "children": [
              {
                "name": "Leaf guard cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Leaf primordium",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 5,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 5,
            "children": [
              {
                "name": "Bundle sheath",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 2,
                "children": [
                  {
                    "name": "Spongy mesophyll",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 5,
                    "node_number": 0
                  },
                  {
                    "name": "Palisade mesophyll",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 5,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Parenchyma",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Populus euramericana",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Populus_euramericana/Populus_euramericana.png",
    "gene_number": 0,
    "classic_number": 51,
    "node_number": 15,
    "children": [
      {
        "name": "Stem",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Populus_euramericana/Stem/Stem.png",
        "gene_number": 0,
        "classic_number": 51,
        "node_number": 13,
        "children": [
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Cork cambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Cortex/Pith",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 4,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 8,
            "children": [
              {
                "name": "Vasculature cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 3,
                "children": [
                  {
                    "name": "Phloem parenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 3,
                    "node_number": 0
                  },
                  {
                    "name": "Phloem precursor cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 7,
                    "node_number": 0
                  },
                  {
                    "name": "Sieve-Companion cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 9,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 2,
                "children": [
                  {
                    "name": "Xylem fiber",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 4,
                    "node_number": 0
                  },
                  {
                    "name": "Xylem precursor cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Camellia sinensis",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Camellia_sinensis/Camellia_sinensis.png",
    "gene_number": 0,
    "classic_number": 64,
    "node_number": 14,
    "children": [
      {
        "name": "Leaf",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Camellia_sinensis/Leaf/Leaf.png",
        "gene_number": 0,
        "classic_number": 64,
        "node_number": 12,
        "children": [
          {
            "name": "Leaf epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 22,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 5,
            "children": [
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 2,
                "children": [
                  {
                    "name": "Spongy mesophyll",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 9,
                    "node_number": 0
                  },
                  {
                    "name": "Palisade mesophyll",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 6,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Cambium",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Procambium",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 4,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 1,
                "node_number": 1,
                "children": [
                  {
                    "name": "Protophloem",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 8,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Protoxylem",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 6,
                    "node_number": 0
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Populus tremula × alba",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Populus_tremula_x_alba/Populus_tremula_x_alba.png",
    "gene_number": 721,
    "classic_number": 51,
    "node_number": 15,
    "children": [
      {
        "name": "Shoot axis apex",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Populus_tremula_x_alba/Shoot_axis_apex/Shoot_axis_apex.png",
        "gene_number": 721,
        "classic_number": 51,
        "node_number": 13,
        "children": [
          {
            "name": "Epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 129,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Trichome",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 50,
                "classic_number": 4,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 1,
            "children": [
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 49,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 1,
                "children": [
                  {
                    "name": "Companion cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 41,
                    "classic_number": 3,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Vasculature cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 66,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Shoot apical meristem",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Proliferating cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 174,
                "classic_number": 11,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Ground meristem cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 79,
                "classic_number": 5,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Shoot meristematic cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 70,
                "classic_number": 6,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Populus trichocarpa",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Populus_trichocarpa/Populus_trichocarpa.png",
    "gene_number": 1049,
    "classic_number": 27,
    "node_number": 11,
    "children": [
      {
        "name": "Stem",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Populus_trichocarpa/Stem/Stem.png",
        "gene_number": 1049,
        "classic_number": 27,
        "node_number": 9,
        "children": [
          {
            "name": "Fusiform early precursor",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 100,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Fusiform intermediate precurso",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 250,
            "classic_number": 4,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Fusiform organizer",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 50,
            "classic_number": 4,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Vascular tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 5,
            "children": [
              {
                "name": "Vasculature cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 200,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 0,
                "node_number": 3,
                "children": [
                  {
                    "name": "Libriform fiber",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 150,
                    "classic_number": 4,
                    "node_number": 0
                  },
                  {
                    "name": "Ray organizer",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 50,
                    "classic_number": 2,
                    "node_number": 0
                  },
                  {
                    "name": "Ray parenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 50,
                    "classic_number": 0,
                    "node_number": 0
                  }
                ]
              }
            ]
          }
        ]
      },
      {
        "name": "Unknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Phyllostachys edulis",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Phyllostachys_edulis/Phyllostachys_edulis.png",
    "gene_number": 609,
    "classic_number": 21,
    "node_number": 9,
    "children": [
      {
        "name": "Root",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Phyllostachys_edulis/Root/Root.png",
        "gene_number": 609,
        "classic_number": 21,
        "node_number": 7,
        "children": [
          {
            "name": "Root epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 50,
            "classic_number": 2,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Ground tissue cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 166,
                "classic_number": 7,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Root cap",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 228,
                "classic_number": 8,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 2,
            "children": [
              {
                "name": "Root initial cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 15,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Transition cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 50,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              }
            ]
          }
        ]
      },
      {
        "name": "Uknown",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
        "gene_number": 0,
        "classic_number": 0,
        "node_number": 0,
        "children": []
      }
    ]
  },
  {
    "name": "Phalaenopsis Big Chili",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Phalaenopsis_Big_Chili/Phalaenopsis_Big_Chili.png",
    "gene_number": 900,
    "classic_number": 0,
    "node_number": 7,
    "children": [
      {
        "name": "Flower",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Phalaenopsis_Big_Chili/Flower/Flower.png",
        "gene_number": 900,
        "classic_number": 0,
        "node_number": 6,
        "children": [
          {
            "name": "Tepal",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 100,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Lip",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 50,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Stamen/Column",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 350,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Floral primordium",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 100,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Flower bract",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 50,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 250,
            "classic_number": 0,
            "node_number": 0,
            "children": []
          }
        ]
      }
    ]
  },
  {
    "name": "Nicotiana tabacum",
    "level": "1",
    "icon_url": f"{settings.BASE_URL}source_material/Nicotiana_tabacum/Nicotiana_tabacum.png",
    "gene_number": 2350,
    "classic_number": 31,
    "node_number": 23,
    "children": [
      {
        "name": "Seedling",
        "level": "2",
        "icon_url": f"{settings.BASE_URL}source_material/Nicotiana_tabacum/Seedling/Seedling.png",
        "gene_number": 2350,
        "classic_number": 31,
        "node_number": 22,
        "children": [
          {
            "name": "Stele",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 8,
            "children": [
              {
                "name": "Vasculature cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 347,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Xylem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 1,
                "node_number": 1,
                "children": [
                  {
                    "name": "Xylem pole pericycle",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 1,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Phloem",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 1,
                "node_number": 2,
                "children": [
                  {
                    "name": "Phloem parenchyma",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 100,
                    "classic_number": 2,
                    "node_number": 0
                  },
                  {
                    "name": "Phloem companion cell",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 0,
                    "classic_number": 1,
                    "node_number": 0
                  }
                ]
              },
              {
                "name": "Root stele",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 44,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Pericycle",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 58,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Ground tissue",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 0,
            "classic_number": 0,
            "node_number": 3,
            "children": [
              {
                "name": "Mesophyll",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 500,
                "classic_number": 4,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Endodermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 0,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Cortex",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 34,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Epidermis",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 528,
            "classic_number": 3,
            "node_number": 4,
            "children": [
              {
                "name": "Leaf guard cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 61,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Trichome",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 81,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Non-hair",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 100,
                "classic_number": 1,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Stem epidermis",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 25,
                "classic_number": 2,
                "node_number": 0,
                "children": []
              }
            ]
          },
          {
            "name": "Meristematic cell",
            "level": "3",
            "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
            "gene_number": 29,
            "classic_number": 2,
            "node_number": 3,
            "children": [
              {
                "name": "Proliferating cell",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 100,
                "classic_number": 0,
                "node_number": 0,
                "children": []
              },
              {
                "name": "Stem cell niche",
                "level": "4",
                "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                "gene_number": 100,
                "classic_number": 2,
                "node_number": 1,
                "children": [
                  {
                    "name": "Quiescent center",
                    "level": "5",
                    "icon_url": f"{settings.BASE_URL}source_material/other/Unknown.png",
                    "gene_number": 100,
                    "classic_number": 1,
                    "node_number": 0
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
]