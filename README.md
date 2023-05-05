# Revealing gender biases in court decisions with natural language processing 
_Official repository of the project by Raysa M. Benatti and colaborators_ 

This repository contains the original scripts and results from the project, whose associated publications and datasets are listed below. 
A complete description of files, methods, tools, and pipelines can be found in this [dissertation](http://google.com). 

The repository is organized as follows:
* ```data-extract```: contains scripts used to extract the data, both for Dataset 1 (domestic violence cases -- ```lesao```) and Dataset 2 (parental alienation cases -- ```ap```); 
* ```data-prep```: contains data preparation scripts; 
* ```exp```: contains scripts used in the experimental pipeline and results (output files) as described in the original work. 

```bash
.
├── data-extract
│   ├── ap
│   │   ├── getLIstAp.py
│   │   ├── prepareApTable.py
│   │   └── pseudoscraper_ap.R
│   └── lesao
│       ├── annotate.py
│       ├── getListLesao.py
│       └── pseudoscraper_lesao.R
├── data-prep
│   ├── extract_chunks.py
│   └── extract_txt.py
└── exp
    ├── augmentation.py
    ├── model.py
    ├── results
    │   ├── ap
    │   │   ├── baseline
    │   │   │   ├── 0_cm_train.png
    │   │   │   ├── 0_cm_val.png
    │   │   │   ├── 0_graph_balanced_accuracy.png
    │   │   │   ├── 0_graph_loss.png
    │   │   │   ├── 0_saida_ap_baseline.txt
    │   │   │   ├── 10_cm_train.png
    │   │   │   ├── 10_cm_val.png
    │   │   │   ├── 10_graph_balanced_accuracy.png
    │   │   │   ├── 10_graph_loss.png
    │   │   │   ├── 10_saida_ap_baseline.txt
    │   │   │   ├── 3_cm_train.png
    │   │   │   ├── 3_cm_val.png
    │   │   │   ├── 3_graph_balanced_accuracy.png
    │   │   │   ├── 3_graph_loss.png
    │   │   │   ├── 3_saida_ap_baseline.txt
    │   │   │   ├── 7_cm_train.png
    │   │   │   ├── 7_cm_val.png
    │   │   │   ├── 7_graph_balanced_accuracy.png
    │   │   │   ├── 7_graph_loss.png
    │   │   │   └── 7_saida_ap_baseline.txt
    │   │   └── deep
    │   │       ├── 0_cm_train.png
    │   │       ├── 0_cm_val.png
    │   │       ├── 0_graph_balanced_accuracy.png
    │   │       ├── 0_graph_loss.png
    │   │       ├── 0_saida_ap_ft.txt
    │   │       ├── 10_cm_train.png
    │   │       ├── 10_cm_val.png
    │   │       ├── 10_graph_balanced_accuracy.png
    │   │       ├── 10_graph_loss.png
    │   │       ├── 10_saida_ap_ft.txt
    │   │       ├── 3_cm_train.png
    │   │       ├── 3_cm_val.png
    │   │       ├── 3_graph_balanced_accuracy.png
    │   │       ├── 3_graph_loss.png
    │   │       ├── 3_saida_ap_ft.txt
    │   │       ├── 7_cm_train.png
    │   │       ├── 7_cm_val.png
    │   │       ├── 7_graph_balanced_accuracy.png
    │   │       ├── 7_graph_loss.png
    │   │       └── 7_saida_ap_ft.txt
    │   └── lesao
    │       ├── baseline
    │       │   ├── 0_cm_train.png
    │       │   ├── 0_cm_val.png
    │       │   ├── 0_graph_balanced_accuracy.png
    │       │   ├── 0_graph_loss.png
    │       │   ├── 0_saida_lesao_baseline.txt
    │       │   ├── 10_cm_train.png
    │       │   ├── 10_cm_val.png
    │       │   ├── 10_graph_balanced_accuracy.png
    │       │   ├── 10_graph_loss.png
    │       │   ├── 10_saida_lesao_baseline.txt
    │       │   ├── 3_cm_train.png
    │       │   ├── 3_cm_val.png
    │       │   ├── 3_graph_balanced_accuracy.png
    │       │   ├── 3_graph_loss.png
    │       │   ├── 3_saida_lesao_baseline.txt
    │       │   ├── 7_cm_train.png
    │       │   ├── 7_cm_val.png
    │       │   ├── 7_graph_balanced_accuracy.png
    │       │   ├── 7_graph_loss.png
    │       │   └── 7_saida_lesao_baseline.txt
    │       └── deep
    │           ├── 0_cm_train.png
    │           ├── 0_cm_val.png
    │           ├── 0_graph_balanced_accuracy.png
    │           ├── 0_graph_loss.png
    │           ├── 0_saida_lesao_ft.txt
    │           ├── 10_cm_train.png
    │           ├── 10_cm_val.png
    │           ├── 10_graph_balanced_accuracy.png
    │           ├── 10_graph_loss.png
    │           ├── 10_saida_lesao_ft.txt
    │           ├── 3_cm_train.png
    │           ├── 3_cm_val.png
    │           ├── 3_graph_balanced_accuracy.png
    │           ├── 3_graph_loss.png
    │           ├── 3_saida_lesao_ft.txt
    │           ├── 7_cm_train.png
    │           ├── 7_cm_val.png
    │           ├── 7_graph_balanced_accuracy.png
    │           ├── 7_graph_loss.png
    │           └── 7_saida_lesao_ft.txt
    ├── run.sh
    └── train.py
```

### Related publications:
* Benatti, R. M. Revealing Gender Biases in Court Decisions with Natural Language Processing. Master's dissertation;
* Raysa M. Benatti, Camila M. L. Villarroel, Sandra Avila, Esther L. Colombini, and Fabiana Severi. [Should I disclose my dataset? Caveats between reproducibility and individual data rights](https://aclanthology.org/2022.nllp-1.20/). In _Proceedings of the Natural Legal Language Processing Workshop 2022_, pages 228–237, 2022;
* Datasets. 

### License: 
This work is published under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License (CC BY-NC-SA 4.0), which means anyone is free to share it or adapt it, under the following terms:
(a) Attribution: you must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use;
(b) NonCommercial: you may not use the material for commercial purposes; 
(c) ShareAlike: if you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.
More details can be found [here](https://creativecommons.org/licenses/by-nc-sa/4.0/) and in the [```LICENSE``` file](https://github.com/ra-ysa/gender_law_nlp/blob/main/LICENSE). 