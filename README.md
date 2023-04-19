# ChiRelPrompt:  Extracting Chinese Multi-relations from Language Models with Prompt


# Requirements

conda env: `/cxy_conda_environment.yaml`

pip package: `/cxy_pip_packages.txt`

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

Hypernymy Detection: `/examples/training/hypernymy/training_hypernymy_benchmark.py`

Concept Attribute Detection: `/examples/training/attribute/training_attribute_benchmark.py`

Multi-relation Detection: `/examples/training/multirelation/training_multi_relation_benchmark.py`

# Run

```
python training_*_benchmark.py
```

# Results

Multi-relation detection:

| Model    | Dataset |  Macro_p   | Macro_R   | Macro_F1  |
| -------- | ------- |  --------- | --------- | --------- |
| D-Tensor | CTLD-m  |  76.52     | 73.34     | 74.78     |
| Sphere   | CTLD-m  |  79.32     | 75.18     | 77.56     |
| CCE      | CTLD-m  |  65.89     | 75.30     | 69.53     |
|TraConcept| CTLD-m  |  65.89     | 75.30     | 69.53     |
| DPRE     | CTLD-m  |  **82.23** | **81.56** | **81.80** |
| CPRE     | CTLD-m  |  **82.23** | **81.56** | **81.80** |
| IPRE     | CTLD-m  |  **82.23** | **81.56** | **81.80** |

Binary relation detection:

| Model    | Dataset | Precision | Recall    | F1        |
| -------- | ------- | --------- | --------- | --------- | 
| D-Tensor | CTLD-h  | 87.78     | 74.88     | 61.56     | 
| D-Tensor | CTLD-a  | 83.27     | 70.15     | 60.18     | 
| Sphere   | CTLD-h  | 91.52     | 82.31     | 79.68     | 
| Sphere   | CTLD-a  | 85.34     | 71.25     | 65.48     | 
| CEE      | CTLD-h  | 92.34     | 85.25     | 83.56     | 
| CEE      | CTLD-a  | 88.56     | 72.17     | 70.86     | 
|TraConcept| CTLD-h  | 90.85     | 87.03     | 84.31     | 
|TraConcept| CTLD-a  | 89.90     | 74.22     | 73.44     | 
| DPRE     | CTLD-h  | 93.00     | 87.88     | **89.79** | 
| DPRE     | CTLD-a  | 91.09     | 77.66     | **81.02** | 
| CPRE     | CTLD-h  | 93.00     | 87.88     | **89.79** | 
| CPRE     | CTLD-a  | 91.09     | 77.66     | **81.02** | 
| IPRE     | CTLD-h  | 93.00     | 87.88     | **89.79** | 
| IPRE     | CTLD-a  | 91.09     | 77.66     | **81.02** | 

> D-Tensor: Dual tensor model for detecting asymmetric lexicosemantic relations. EMNLP 2017
>
> Spherere: Distinguishing lexical relations with hyperspherical relation embeddings. ACL 2019
>
> CCE: Learning Conceptual-Contextual Embeddings for Medical Text. AAAI 2020
>
> TraConcept: TraConcept: Constructing a Concept Framework from Chinese Traffic Legal Texts. CCKS 2022
>

# Reference

[SentenceTransformers]([SentenceTransformers Documentation — Sentence-Transformers documentation (sbert.net)](https://www.sbert.net/))

> refer to [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084)(EMNLP 2019)
