from normalize import load_data, normalize_data
from dimensionality_reduction import reduce_dimension
from clustering import perform_clustering, plot_clusters
from differential_analysis import differential_expression

# Usage
data = load_data('./rectum/read_count.tsv')
data_norm = normalize_data(data)
tsne_result = reduce_dimension(data_norm)
kmeans = perform_clustering(tsne_result)
plot_clusters(tsne_result, kmeans, 'xxx.png')
ttest_results = differential_expression(data, kmeans)
