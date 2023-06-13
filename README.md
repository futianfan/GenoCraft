# GenoCraft 

![pipeline](pipeline.png)



GenoCraft is a comprehensive software solution designed to handle the entire pipeline of omics data processing. It provides a streamlined, user-friendly interface for researchers and data scientists to manage and analyze large-scale omics data.

The process begins with data normalization and quality control, ensuring data reliability. Advanced algorithms like T-SNE are then used for data visualization and pattern recognition. Clustering techniques group similar data points together, revealing key trends. Differential analysis allows for the comparison of different data sets, identifying unique patterns and anomalies. The final step is pathway analysis, which provides a deeper understanding of the underlying biological processes.

In summary, GenoCraft is a powerful, all-in-one solution for omics data processing, providing researchers with the tools they need to transform raw data into meaningful insights.

## outline 

This repo has two folders: `single_cell` and `bulk_RNA`.  


## install package 

```
pip install numpy 
pip install scipy 
pip install matplotlib 
pip install tqdm 
pip install scikit-learn 
pip install networkx 
pip install statsmodels 
pip install seaborn 
pip install pyyaml==4.2b1 
pip install HTSeq 
```


# Bulk RNA 


## Step 2. Normalization (almost done)
This step involves adjusting the raw gene expression measurements to minimize the effects of systematic technical differences, enabling more accurate comparison of gene expression levels across samples.

This step start from read counts. Normalization leverages gene length information (`gene_lengths.csv`) to normalize the gene count (`count.csv`). 

- input:
	- `counts.csv`: read count
	- `gene_lengths.csv`: gene length.   
- run:
	- `Normalize.py` 
- output:
	- `count_scaled.csv`: normalized count file. 





## Step 3. Differential Analysis
This step involves identifying genes that are expressed differently between different conditions or groups. The goal is to find genes whose changes in expression levels are statistically significant.

- input: 
	- `case.txt` 351*100
	- `control.txt`  351*100
	- `genename.txt` 351 lines, all the gene names
- run:
	- `DEG.py` 
- output: 
	- `significant_gene.txt`: all the significant gene names 

## Step 4.  Network Analysis: 
This step involves the construction and analysis of gene networks. These networks can help identify key genes and pathways involved in the condition being studied.

- input: 
	- `case.txt` 351*100
	- `control.txt`  351*100
	- `significant_gene.txt` from step 3
- run:
	- `DDN.py` 
- output: 
	- `differential_network.csv` & differential network

## Step 5. Gene Set Enrichment Analysis/pathway enrichment (almost finish)
Gene Set Enrichment Analysis (GSEA) is a computational method that determines whether an a priori defined set of genes shows statistically significant, concordant differences between two biological states (e.g., phenotypes).

search the signficant genes in database [Enrichr](https://maayanlab.cloud/Enrichr). 


submit -> pathway -> KEGG 2021 Human -> Bar Graph 
									 -> Table 

- input: 
	- `significant_gene.txt` from step 3
- run:
	- `GSEA.py` 
- output: 
- pathway list with statistical significance detected
	- `pathway_with_pvalues.jpg` - visualization
	- `pathway_with_pvalues.csv` 





## Step 6. Visualization (TODO)
The results of the analysis are visualized. This helps in interpreting the results and in generating hypotheses for further research.

Gene Network Generation 
- Common Dependency Network
- Differential Dependency Network (DDN)

Heatmap Visualization

t-SNE/UMAP

- input: 
	- `significant_gene.txt`
	- `case.txt`
	- `control.txt`
- run: 
	- `XXX.py`
- output: 
	- `common.png`
	- `differential.png`



## Step 7. pseudotime 







# Single cell

## Step 1. Normalization: 
This is the process of standardizing and scaling the data. In the context of data analysis, normalization often refers to the process of rescaling the values of numeric columns in the dataset to a common scale.


- input: 
	- `xxx`
	- `xxx`
- run: 
	- `xxx.py`
- output: 
	- `xxx`
	- `xxx`



## Step 2. Quality Control: 
Quality control involves the examination of a product, service, or process for certain minimum levels of quality. In data analysis, this could involve various checks to ensure the data is accurate, consistent and reliable.


- input: 
	- `xxx`
	- `xxx`
- run: 
	- `xxx.py`
- output: 
	- `xxx`
	- `xxx`

## Step 3. T-SNE (t-Distributed Stochastic Neighbor Embedding): 
T-SNE is a machine learning algorithm for visualization. It is a nonlinear dimensionality reduction technique well-suited for embedding high-dimensional data for visualization in a low-dimensional space of two or three dimensions.

- input: 
	- `xxx`
	- `xxx`
- run: 
	- `xxx.py`
- output: 
	- `xxx`
	- `xxx`



## Step 4. Clustering (almost done)
Clustering is a Machine Learning technique that involves the grouping of data points. In theory, data points that are in the same group should have similar properties and/or features, while data points in different groups should have highly dissimilar properties and/or features.
Each data point is a cell, we use clustering to identify the cell types (e.g., blood cell, neuron cell, ). 
Common packages include PCA, tSNE, K-means, graph-based clustering, ...


- input: 
	- `xxx`
	- `xxx`
- run: 
	- `xxx.py`
- output: 
	- `xxx`
	- `xxx`

Clustering is only for single-cell. bulk-RNA has 10-20 data points. 
Number of clusters is determined by labors. 

- input:
	- `xxx`
- run:
	- `clustering_singlecell.py`: only for single-cell 
- output:
	- `xxxx`

## Step 5. Differential Analysis: 
This involves the comparison of different data sets to identify patterns and anomalies. It's often used in gene expression analysis where one might be interested in identifying genes whose expression are up-regulated or down-regulated when comparing two different conditions (like a disease state versus a control state).

- input: 
	- `xxx`
	- `xxx`
- run: 
	- `xxx.py`
- output: 
	- `xxx`
	- `xxx`


## Step 6. Pathway Analysis: 
Pathway analysis is a tool for interpreting the results of expression data within the context of pathways. The aim is to identify the pathways significantly impacted in a condition under study. Pathway analysis has become the first choice for gaining insight into the underlying biology of differentially expressed genes and proteins, as it reduces complexity and has increased explanatory power.



- input: 
	- `xxx`
	- `xxx`
- run: 
	- `xxx.py`
- output: 
	- `xxx`
	- `xxx`







