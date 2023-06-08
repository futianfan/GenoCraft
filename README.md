# GenoCraft 


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





## Step 2. Normalization (almost done)
This step involves adjusting the raw gene expression measurements to minimize the effects of systematic technical differences, enabling more accurate comparison of gene expression levels across samples.

This step start from read counts. Normalization leverages gene length information (`gene_lengths.csv`) to normalize the gene count (`count.csv`). 

- input:
	- `counts.csv`: read count
	- `gene_lengths.csv`: gene length.   
- run:
	- `normalization.csv`
	- `Normalize.py` 
- output:
	- `count_scaled.csv`: normalized count file. 


## Step 3. Clustering (almost done)

Each data point is a cell, we use clustering to identify the cell types (e.g., blood cell, neuron cell, ). 
Common packages include PCA, tSNE, K-means, graph-based clustering, ...


Clustering is only for single-cell. bulk-RNA has 10-20 data points. 
Number of clusters is determined by labors. 

- input:
	- `xxx`
- run:
	- `clustering_singlecell.py`: only for single-cell 
- output:
	- `xxxx`


Network Analysis: This step involves the construction and analysis of gene networks. These networks can help identify key genes and pathways involved in the condition being studied.


## Step 4. Differential Analysis
This step involves identifying genes that are expressed differently between different conditions or groups. The goal is to find genes whose changes in expression levels are statistically significant.

- input: 
	- `case.txt` 351*100
	- `control.txt`  351*100
	- `genename.txt` 351 lines, all the gene names
- run:
	- `DEGs.py` 
- output: 
	- `significant_gene.txt`: all the significant gene names 


## Step 5. Gene Set Enrichment Analysis/pathway enrichment (almost finish)
Gene Set Enrichment Analysis (GSEA) is a computational method that determines whether an a priori defined set of genes shows statistically significant, concordant differences between two biological states (e.g., phenotypes).

search the signficant genes in database [Enrichr](https://maayanlab.cloud/Enrichr). 



submit -> pathway -> KEGG 2021 Human -> Bar Graph 
									 -> Table 

- input: 
	- `significant_gene.txt` 
- run:
	- `pathway.py` 
- output: 
	- `.jpg` 
	- `.txt` (table)


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
	- `DDN.py`
- output: 
	- `common.png`
	- `differential.png`



## Step 7. pseudotime 











