from normalize import load_data, normalize_data
from clustering import reduce_dimension, perform_clustering
from visualization import plot_clusters
from differential_expression import differential_expression

# Usage
data = load_data('./read_counts.csv')
data_norm = normalize_data(data)
data_norm = load_data('GSE69405_PROCESSED_GENE_TPM_ALL_ready.txt')
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
ttest_results, controldata, casedata = differential_expression(data_norm, kmeans)
print(controldata.shape, casedata.shape)

# exit()
with open('GSE69405_PROCESSED_GENE_TPM_ALL_ready.txt') as fin:
	lines = fin.readlines() 
	gene_names = [line.split()[0] for line in lines]
with open('genename.txt', 'w') as fout:
	for gene in gene_names:
		fout.write(gene + '\n')


### DDN 
from DDN import DDN 
ddn = DDN() 
lambda1 = 0.3
lambda2 = 0.05
neighbors = ddn.DDNPipline(casedata=casedata, \
                           controldata=controldata, \
                           gene_name_file='genename.txt', \
                           output_file='differential_network.csv', \
                           lambda1=lambda1, lambda2=lambda2)

print('success')
