import pandas as pd
from scipy import stats


def run_differential_analysis(gene_names, df_cases, df_controls):
    # read in gene names and store as a list
    # gene_names = df_genename.values.tolist()
    # gene_names is list of string

    # perform t-test for each gene and select those with p-value < 0.01
    significant_genes = []
    for i, gene in enumerate(gene_names):
        case_data = df_cases.iloc[i, :]
        control_data = df_controls.iloc[i, :]
        _, p_value = stats.ttest_ind(case_data, control_data)
        if p_value < 0.001:
            significant_genes.append(gene)

    # extract data for significant genes and save to new files
    gene_indices = [i for i in range(len(gene_names)) if gene_names[i] in significant_genes]
    significant_cases = df_cases.iloc[gene_indices, :]
    significant_controls = df_controls.iloc[gene_indices, :]

    # Return dataframes as result
    significant_genes = pd.DataFrame(significant_genes)
    return significant_genes, significant_cases, significant_controls
