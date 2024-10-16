import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scipy import stats

# Load data into a pandas DataFrame
# data = pd.read_csv('counts.csv', index_col=0)
data = pd.read_csv('./rectum/read_count.tsv', sep = '\t', index_col = 0)


# Normalization - library size scaling and log-transformation
data_norm = data.div(data.sum(axis=0), axis=1) * 1e6
data_norm = data_norm.transform(np.log1p)

# Filter out lowly expressed genes
data_norm = data_norm.loc[data_norm.sum(axis=1) > 3]

# Dimensionality reduction - PCA
pca = PCA(n_components=50)
pca_result = pca.fit_transform(data_norm.transpose())

# Further dimensionality reduction - t-SNE
tsne = TSNE(n_components=2, random_state=0)
tsne_result = tsne.fit_transform(pca_result)

# Clustering - KMeans
kmeans = KMeans(n_clusters=10, random_state=0).fit(tsne_result)

# Plotting
scatter = plt.scatter(tsne_result[:, 0], tsne_result[:, 1], c=kmeans.labels_, cmap='viridis')
plt.title('t-SNE plot with KMeans clusters')

# Create a legend for the colors
handles, labels = scatter.legend_elements()
# plt.legend(handles, title="Clusters")

plt.show()

# Differential expression analysis - simple t-test as an example
cluster0_cells = data.columns[kmeans.labels_ == 0]
cluster1_cells = data.columns[kmeans.labels_ == 1]

ttest_results = stats.ttest_ind(data[cluster0_cells], data[cluster1_cells], axis=1)
