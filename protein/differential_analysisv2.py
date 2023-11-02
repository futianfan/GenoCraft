import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

def run_differential_analysis(gene_names, df_cases, df_controls):
    significant_genes = []
    p_values = []

    for i, gene in enumerate(gene_names):
        case_data = df_cases.iloc[i,:]
        control_data = df_controls.iloc[i,:]
        _, p_value = stats.ttest_ind(case_data, control_data)
        p_values.append(p_value)
        if p_value < 0.2:
            significant_genes.append(gene)

    gene_indices = [i for i in range(len(gene_names)) if gene_names[i] in significant_genes]
    significant_cases = df_cases.iloc[gene_indices,:]
    significant_controls = df_controls.iloc[gene_indices,:]

    df_p_values = pd.DataFrame({
        'Gene': gene_names,
        'p-value': p_values
    })

    return significant_genes, significant_cases, significant_controls, df_p_values

if __name__ == '__main__':
    # 1. Quality control
    import pandas as pd 
    from quality_control import filter_low_counts 
    df = pd.read_csv('read_counts.csv', sep='\t')
    df_filtered = filter_low_counts(df)

    # 2. Normalize
    with open('case.txt') as fin:
        lines = fin.readlines() 
        case_samples = [line.strip() for line in lines]
    with open('control.txt') as fin:
        lines = fin.readlines() 
        control_samples = [line.strip() for line in lines]

    from Normalize import normalize_rnaseq_data 
    df, case_df_cpm, control_df_cpm = normalize_rnaseq_data(df, case_samples, control_samples)

    # 3. Visualize
    case_df_cpm = case_df_cpm[:1000]
    control_df_cpm = control_df_cpm[:1000]
    print(df, case_df_cpm, control_df_cpm)
    print(case_df_cpm.isna().sum())
    print(control_df_cpm.isna().sum()) 
    from Visualize import visualize  
    stream = visualize(case_df_cpm, control_df_cpm) 

    # 4. Differential analysis
    with open('read_counts.csv', 'r') as fin:
        lines = fin.readlines()[1:]
        gene_names = [line.split()[0] for line in lines] 
    genename_list = gene_names[:len(case_df_cpm)]

    significant_genes, significant_cases, significant_controls, df_p_values = run_differential_analysis(genename_list, case_df_cpm, control_df_cpm)
    
    print(significant_genes)
    print(significant_cases)

    # Visualizing significant genes' p-values with heatmap after sorting
    significant_p_values = df_p_values[df_p_values['Gene'].isin(significant_genes)]
    sorted_significant_p_values = significant_p_values.sort_values(by='p-value')
    plt.figure(figsize=(10, 10))
    sns.heatmap(sorted_significant_p_values.set_index('Gene'), cmap="coolwarm_r", annot=True, cbar_kws={'label': 'p-value'})
    plt.title("P-values of Significant Genes (Sorted)")
    plt.show()
