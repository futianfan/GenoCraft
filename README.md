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


10X, commercial software

The goal is to transform the raw feature (fastq) into read count. 

Source 
- [C++ Package](https://github.com/alexdobin/STAR.git)
- [R package](https://github.com/rdeborj/STAR)
- https://www.saraballouz.com/post/workflows/howtos_alignment/ 
- https://www.gencodegenes.org/human/#
- HTseq-count: https://htseq.readthedocs.io/en/master/overview.html
- Star: https://hbctraining.github.io/Intro-to-rnaseq-hpc-O2/lessons/03_alignment.html


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

genomeFastaFiles: from mouse. download
gtf: download for mouse, human 
once for all, one for a specicies (human, mouse).  

### 1.3 htseq-count

`paired` (2 fastq files) versus `unpaired` (1 fastq file). 


`fastq` to `read count`. 

for each single-cell, process. 

two fastq files and index file (optional). 


```
# map single end reads to genome
STAR --runThreadN 12 \
     --readFilesIn SRR11542244_1.fastq \
     --genomeDir ./genomeDir \
     --outSAMtype BAM SortedByCoordinate \
     --outFileNamePrefix seed_sample  \
     --outSAMunmapped Within
```


```
# map paired-end reads to genome
./STAR/source/STAR --runThreadN 12 \
     --readFilesIn SRR11542244_1.fastq SRR11542244_2.fastq \
     --genomeDir ./genomeDir \
     --outSAMtype BAM SortedByCoordinate \
     --outFileNamePrefix seed_sample  \
     --outSAMunmapped Within
```


## Step 2. Normalization

Normalization leverages gene length information (`gene_lengths.csv`) to normalize the gene count (`count.csv`). 

- input:
	- `counts.csv`: read count
	- `gene_lengths.csv`: gene length.   
- method:
	- TPM/CPM, log_{10}, 
- output:
	- `count_scaled.csv`: normalized count file. 


## Step 3. Clustering 

Each data point is a cell, we use clustering to identify the cell types (e.g., blood cell, neuron cell, ). 
Common packages include PCA, tSNE, K-means, graph-based clustering, ...


Clustering mainly for single-cell. bulk-RNA has 10-20 data points. 
Number of clusters is determined by labors. 


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
Gene Network Generation 
-Common Dependency Network
-Differential Dependency Network (DDN)

Heatmap Visualization

t-SNE/UMAP




## Step 7. pseudotime 











