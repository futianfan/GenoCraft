# GenoCraft 


## install package 

R and Python 

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
```


## pipeline 




## Internal Data 



## User Input data 



## Step 1. Alignment 

The goal is to transform the raw feature (fastq) into read count. 

Source 
- [C++ Package](https://github.com/alexdobin/STAR.git)
- [R package](https://github.com/rdeborj/STAR)

- input: 
	- 
	- 
- output: 
	- 
	- 



## Step 2. Normalization 




## Step 3. Clustering 




## Step 4. DEGs (differential expression genes)

This is essentially a hypothesis testing. 
Bulk RNA starts from Step 2 or Step 4. 

- input: 
	- `case.txt` 351*100
	- `control.txt`  351*100
	- `genename.txt` 351 lines, all the gene names
- run:
	- `DEGs.py` 
- output: 
	- `significant_gene.txt`: all the significant gene names 


## Step 5. GO/pathway enrichment 

search the signficant genes in database [Enrichr](https://maayanlab.cloud/Enrichr). 


- input: 
	- `significant_gene.txt` 
- run:
	- `pathway.py` 
- output: 
	- `.jpg` 
	- `.txt` (table)


## Step 6. Visualization 






## Step 7. pseudotime 











