from scipy import stats
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import seaborn as sns


def differential_expression(data, kmeans):
    data = np.log1p(data)
    cluster0_cells = data.columns[kmeans.labels_ == 0]
    cluster1_cells = data.columns[kmeans.labels_ == 1]
    casedata = data[cluster1_cells]
    controldata = data[cluster0_cells]
    ttest_results = stats.ttest_ind(data[cluster0_cells], data[cluster1_cells], axis=1)
    significant_genes = data.index[ttest_results.pvalue < 0.05]
    significant_gene_and_expression = data.loc[significant_genes, :]

    # scaler = MinMaxScaler()
    # significant_gene_and_expression = scaler.fit_transform(significant_gene_and_expression)

    print("=== controldata.shape ===", controldata.shape)
    print("=== casedata.shape ===", casedata.shape)

    t_stat, pvalues = ttest_results
    print("=== t_stat.shape ===", t_stat.shape)
    gene_list = data.index.tolist()
    significant_gene = [gene for gene, pvalue in zip(gene_list, pvalues) if pvalue < 0.05]
    print(significant_gene)
    return significant_gene



def plot_differential_analysis_heatmap(significant_gene_and_expression):
    fig, ax = plt.subplots(figsize=(10,10))
    sns.heatmap(significant_gene_and_expression, cmap='coolwarm') ## cmap = 'viridis'
    fig.savefig(output_file, format='png')
    plt.close(fig)
    plt.cla()

