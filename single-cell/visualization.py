import io
import matplotlib.pyplot as plt

def plot_clusters(data, kmeans):
    fig, ax = plt.subplots()
    stream = io.BytesIO()
    scatter = plt.scatter(data[:, 0], data[:, 1], c=kmeans.labels_, cmap='viridis')
    plt.title('t-SNE plot with KMeans clusters')
    handles, labels = scatter.legend_elements()
    fig.savefig(stream, format='png')
    stream.seek(0)
    plt.close(fig)
    return stream 
    # plt.savefig(filepath)



