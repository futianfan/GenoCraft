import io

import matplotlib.pyplot as plt
import matplotlib


def plot_clusters(data, kmeans):
    stream = io.BytesIO()
    matplotlib.use('agg')
    print("=== kmeans.labels_ ===\n", kmeans.labels_[:10])
    scatter = plt.scatter(data[:, 0], data[:, 1], c=kmeans.labels_, cmap='viridis')
    plt.title('t-SNE plot with KMeans clusters')
    handles, labels = scatter.legend_elements()
    plt.savefig(stream, format='png')
    stream.seek(0)
    plt.close()

    return stream.getvalue()
