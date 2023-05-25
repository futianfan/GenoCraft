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

- input: 
	- 
	- 
- output: 
	- 
	- 



## Step 2. Normalization 




## Step 3. Clustering 




## Step 4. DEGs (differential expression genes)

- input: 
	- `case.txt` 351*100
	- `control.txt`  351*100
	- `genename.txt` 351 lines, all the gene names
- run:
	- `DEGs.py` 
- output: 
	- `significant_gene.txt`: all the significant gene names 


## Step 5. GO/pathway enrichment



## Step 6. Visualization 



## Step 7. pseudotime 











