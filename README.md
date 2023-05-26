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

### 1.1 fastq to fasta 

Install [seqtk](https://github.com/lh3/seqtk). 


```
./seqtk/seqtk seq -aQ64 -q20 -n N ./data/1.fastq > ./data/1.fasta
```


### 1.2 create index 

```
./STAR/source/STAR --runThreadN 1 --runMode genomeGenerate --genomeDir ./genomeDir --genomeFastaFiles data/1.fasta --sjdbGTFfile data/toy.gtf
```



### 1.2 




## Step 2. Normalization 




## Step 3. Clustering 

Each data point is a cell, we use clustering to identify the cell types (e.g., blood cell, neuron cell, ). 
Common packages include PCA, tSNE, ...



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



submit -> pathway -> KEGG 2021 Human -> Bar Graph 
									 -> Table 

- input: 
	- `significant_gene.txt` 
- run:
	- `pathway.py` 
- output: 
	- `.jpg` 
	- `.txt` (table)


## Step 6. Visualization 






## Step 7. pseudotime 











