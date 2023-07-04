from scipy import stats
from sklearn.preprocessing import MinMaxScaler
import numpy as np 
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

    return ttest_results, controldata, casedata, significant_gene_and_expression  
