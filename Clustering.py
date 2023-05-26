# -input: normalized data
# -output: data after clustering with two conditions


import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans



# Run KMeans clustering
kmeans = KMeans(n_clusters=5)
clusters = kmeans.fit_predict(pca_result)

# Add clusters to the pca_result dataframe
pca_result_df = pd.DataFrame(pca_result, columns=[f"PC{i+1}" for i in range(pca.n_components_)], index=counts.index)
pca_result_df['Cluster'] = clusters

# Visualize the clusters (we can only visualize two dimensions, so we will use the first two principal components)
plt.figure(figsize=(10, 10))
for cluster in set(clusters):
    cluster_cells = pca_result_df[pca_result_df['Cluster'] == cluster]
    plt.scatter(cluster_cells['PC1'], cluster_cells['PC2'], label=f"Cluster {cluster}")
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.legend()
plt.show()
