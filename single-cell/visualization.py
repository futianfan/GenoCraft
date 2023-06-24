import matplotlib.pyplot as plt
def plot_clusters(data, kmeans, filepath):
    scatter = plt.scatter(data[:, 0], data[:, 1], c=kmeans.labels_, cmap='viridis')
    plt.title('t-SNE plot with KMeans clusters')
    handles, labels = scatter.legend_elements()
    plt.savefig(filepath)



