from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
perplexity_value = 7


def reduce_dimension(data, n_components=10):
    pca = PCA(n_components=n_components)
    pca_result = pca.fit_transform(data.transpose())
    tsne = TSNE(n_components=2, random_state=0, perplexity=perplexity_value)
    tsne_result = tsne.fit_transform(pca_result)
    return tsne_result
