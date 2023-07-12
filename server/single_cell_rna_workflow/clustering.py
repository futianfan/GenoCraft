from sklearn.cluster import KMeans


def perform_clustering(data, n_clusters=10):
    kmeans = KMeans(n_clusters=n_clusters, random_state=3425).fit(data)
    return kmeans

