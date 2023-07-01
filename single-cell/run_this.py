from normalize import load_data, normalize_data
from clustering import reduce_dimension, perform_clustering
from visualization import plot_clusters
from differential_expression import differential_expression
from GSEA import run_gsea_analysis 
import numpy as np 

# Usage
data = load_data('./read_counts.csv')
data_norm = normalize_data(data)
data_norm = load_data('GSE69405_PROCESSED_GENE_TPM_ALL_ready.txt')
print(len(data_norm.index.tolist()))
# exit()
# print(data_norm.isna().sum().sum())
# exit() 
### download from: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE69405 
tsne_result = reduce_dimension(data_norm)
kmeans = perform_clustering(tsne_result)
stream = plot_clusters(tsne_result, kmeans)

### stream to png
file = open('GSE69405_clustering.png', 'wb')
for chunk in stream:
    file.write(chunk)
file.close()
### stream to png

### DEG 
# print('kmeans', kmeans)
print('before DEG data norm', data_norm.isna().sum().sum())
ttest_results, controldata, casedata = differential_expression(data_norm, kmeans)
print(controldata.shape, casedata.shape)

t_stat, pvalues = ttest_results 
print(t_stat.shape)
gene_list = data_norm.index.tolist()
significant_gene = [gene for gene, pvalue in zip(gene_list, pvalues) if pvalue < 0.05]
gene_names_file = 'significant_gene.txt'
with open(gene_names_file, 'w') as fout:
	for gene in significant_gene:
		fout.write(gene + '\n')
# t_stat = np.nan_to_num(t_stat)
# pvalues = np.nan_to_num(pvalues)
# exit()

with open('GSE69405_PROCESSED_GENE_TPM_ALL_ready.txt') as fin:
	lines = fin.readlines() 
	gene_names = [line.split()[0] for line in lines]
with open('genename.txt', 'w') as fout:
	for gene in gene_names:
		fout.write(gene + '\n')


### DDN 
# from DDN import DDN 
# ddn = DDN() 
# lambda1 = 0.3
# lambda2 = 0.05
# neighbors = ddn.DDNPipline(casedata=casedata, \
#                            controldata=controldata, \
#                            gene_name_file='genename.txt', \
#                            output_file='differential_network.csv', \
#                            lambda1=lambda1, lambda2=lambda2)



### GSEA 
gene_names_file = 'significant_gene.txt'
stream, df = run_gsea_analysis(gene_names_file, 'pathway_with_pvalues.csv')
print(df)




print('success')





