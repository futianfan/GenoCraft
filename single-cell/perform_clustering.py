from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def perform_clustering(data, n_clusters=10):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(data)
    return kmeans

def plot_clusters(data, kmeans, filepath):
    scatter = plt.scatter(data[:, 0], data[:, 1], c=kmeans.labels_, cmap='viridis')
    plt.title('t-SNE plot with KMeans clusters')
    handles, labels = scatter.legend_elements()
    plt.savefig(filepath)
