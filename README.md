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





## Step 2. Normalization 

This step start from read counts. Normalization leverages gene length information (`gene_lengths.csv`) to normalize the gene count (`count.csv`). 

- input:
	- `counts.csv`: read count
	- `gene_lengths.csv`: gene length.   
- method:
	- TPM/CPM, log_{10}, 
	- `normalization.csv`
	- `python Normalize.py` 
- output:
	- `count_scaled.csv`: normalized count file. 


## Step 3. Clustering 

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

## Step 4. DEGs (differential expression genes) (done)

This is essentially a hypothesis testing
Bulk RNA starts from Step 2 or Step 4. 

- input: 
	- `case.txt` 351*100
	- `control.txt`  351*100
	- `genename.txt` 351 lines, all the gene names
- run:
	- `DEGs.py` 
- output: 
	- `significant_gene.txt`: all the significant gene names 


## Step 5. GO/pathway enrichment (almost finish)

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











