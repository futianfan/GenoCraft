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
ttest_results = differential_expression(data_norm, kmeans)


### DDN 


print('success')
