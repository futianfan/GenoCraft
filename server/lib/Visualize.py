from sklearn.manifold import TSNE

# Run t-SNE
tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
tsne_results = tsne.fit_transform(pca_result)

# Plot t-SNE
plt.figure(figsize=(8,8))
plt.scatter(tsne_results[:,0], tsne_results[:,1])
plt.xlabel('t-SNE 1')
plt.ylabel('t-SNE 2')
plt.show()
