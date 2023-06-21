from normalize import load_data, normalize_data
from reduce_dimension import reduce_dimension
from clustering import perform_clustering, plot_clusters
from differential_expression import differential_expression

# Usage
data = load_data('./read_counts.csv')
data_norm = normalize_data(data)
tsne_result = reduce_dimension(data_norm)
kmeans = perform_clustering(tsne_result)
plot_clusters(tsne_result, kmeans, 'xxx.png')
ttest_results = differential_expression(data, kmeans)
print('success')