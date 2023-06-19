from scipy import stats

def differential_expression(data, kmeans):
    cluster0_cells = data.columns[kmeans.labels_ == 0]
    cluster1_cells = data.columns[kmeans.labels_ == 1]
    ttest_results = stats.ttest_ind(data[cluster0_cells], data[cluster1_cells], axis=1)
    return ttest_results
