from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

def reduce_dimension(data, n_components=50):
    pca = PCA(n_components=n_components)
    pca_result = pca.fit_transform(data.transpose())
    tsne = TSNE(n_components=2, random_state=0)
    tsne_result = tsne.fit_transform(pca_result)
    return tsne_result
