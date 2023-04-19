# ChiRelPrompt:  Extracting Chinese Multi-relations from Language Models with Prompt


# Requirements

conda env: `/conda_environment.yaml`

pip package: `/pip_packages.txt`

# Datasets

CTLD-h: `/examples/training/hypernymy/datasets/hypernymydetection.tsv.gz`

CTLD-a: `/examples/training/attribute/datasets/attributedetection.tsv.gz`

CTLD-m: `/examples/training/multirelation/datasets/multi-relation-detection-detection.tsv.gz`

CTLD-f: `/examples/training/datasets/relation-similarity.tsv.gz`

Statistical information of datasets is below:

| Datasets | Train  |  Dev   |  Test  |
| :------: | :----: | :----: | :----: |
|  CTLD-h  | 18,847 | 6,302  | 6,292  |
|  CTLD-a  | 40,412 | 13,449 | 13,451 |
|  CTLD-m  | 19,100 | 6,120  | 6,515  |
|  CTLD-f  | 23,846 | 6,115  |   -    |

# Main File

Multi-relation Detection: `/examples/training/multirelation/training_multi_relation_benchmark.py`

Hypernymy Detection: `/examples/training/hypernymy/training_hypernymy_benchmark.py`

Concept Attribute Detection: `/examples/training/attribute/training_attribute_benchmark.py`

# Run

```
python training_*_benchmark.py
```

# Results

CTLD-m:

| Model    |  Macro_p   | Macro_R   | Macro_F1  |
| -------- |  --------- | --------- | --------- |
| D-Tensor |  76.52     | 73.34     | 74.89     |
| SphereRE |  83.59     | 81.08     | 82.31     |
| CCE      |  78.97     | 77.67     | 78.31     |
|TraConcept|  82.23     | 81.56     | 81.90     |
| DPRE     |  83.44     | 82.39     | 82.91     |
| CPRE     |  **83.59** | 82.42     | 83.17     |
| IPRE     |  83.42     | **82.99** | **83.20** |

CTLD-h:

| Model    | Precision | Recall    | F1        |
| -------- | --------- | --------- | --------- | 
| D-Tensor | 74.88     | 61.56     | 67.57     | 
| SphereRE | 87.85     | 85.16     | 86.48     | 
| CEE      | 83.34     | 81.51     | 82.41     | 
|TraConcept| 87.88     | **89.79** | 88.82     | 
| DPRE     | 88.41     | 85.97     | 87.17     | 
| CPRE     | **89.04** | 87.40     | 88.21     | 
| IPRE     | 89.01     | 88.72     | **88.86** | 

CTLD-a:

| Model    | Precision | Recall    | F1        |
| -------- | --------- | --------- | --------- | 
| D-Tensor | 70.15     | 60.18     | 64.78     | 
| SphereRE | 75.37     | 76.39     | 75.87     | 
| CEE      | 70.15     | 68.29     | 69.20     | 
|TraConcept| 77.66     | 81.02     | 79.31     | 
| DPRE     | **80.60** | 79.37     | 79.98     | 
| CPRE     | 78.27     | 80.49     | 79.36     | 
| IPRE     | 79.67     | **82.14** | **80.88** | 

> D-Tensor: Dual tensor model for detecting asymmetric lexicosemantic relations. EMNLP 2017
>
> Spherere: Distinguishing lexical relations with hyperspherical relation embeddings. ACL 2019
>
> CCE: Learning Conceptual-Contextual Embeddings for Medical Text. AAAI 2020
>
> TraConcept: TraConcept: Constructing a Concept Framework from Chinese Traffic Legal Texts. CCKS 2022
>
