import io
import matplotlib.pyplot as plt
import matplotlib


def plot_clusters(data, kmeans):
    stream = io.BytesIO()
    matplotlib.use('agg')
    scatter = plt.scatter(data[:, 0], data[:, 1], c=kmeans.labels_, cmap='viridis')
    plt.title('t-SNE plot with KMeans clusters')
    handles, labels = scatter.legend_elements()
    plt.savefig(stream, format='png')
    stream.seek(0)

    return stream.getvalue()



