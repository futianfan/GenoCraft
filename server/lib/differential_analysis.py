import pandas as pd
from scipy import stats


def run_differential_analysis(gene_names, df_cases, df_controls):
    # read in gene names and store as a list
    # gene_names = df_genename.values.tolist()
    # gene_names is list of string 

    # perform t-test for each gene and select those with p-value < 0.01
    significant_genes = []
    for i, gene in enumerate(gene_names):
        case_data = df_cases.iloc[i,:]
        control_data = df_controls.iloc[i,:]
        _, p_value = stats.ttest_ind(case_data, control_data)
        if p_value < 0.001:
            significant_genes.append(gene)

    # extract data for significant genes and save to new files
    gene_indices = [i for i in range(len(gene_names)) if gene_names[i] in significant_genes]
    significant_cases = df_cases.iloc[gene_indices,:]
    significant_controls = df_controls.iloc[gene_indices,:]

    # Return dataframes as result
    significant_genes = pd.DataFrame(significant_genes)
    return significant_genes, significant_cases, significant_controls





if __name__ == '__main__':
    
    ### 1. quality control 
    import pandas as pd 
    from quality_control import filter_low_counts 
    # df = pd.read_csv('read_counts.csv', index_col=0)
    df = pd.read_csv('read_counts.csv', sep = '\t')
    df_filtered = filter_low_counts(df)



    ### 2. normalize 
    with open('case.txt') as fin:
        lines = fin.readlines() 
        case_samples = [line.strip() for line in lines]
    with open('control.txt') as fin:
        lines = fin.readlines() 
        control_samples = [line.strip() for line in lines]

    from Normalize import normalize_rnaseq_data 
    # print(case_samples, control_samples)
    df, case_df_cpm, control_df_cpm = normalize_rnaseq_data(df, case_samples, control_samples)


    ### 3. visualize 
    case_df_cpm = case_df_cpm[:1000]
    control_df_cpm = control_df_cpm[:1000]
    print(df, case_df_cpm, control_df_cpm)
    print(case_df_cpm.isna().sum())
    print(control_df_cpm.isna().sum()) 
    from Visualize import visualize  
    stream = visualize(case_df_cpm, control_df_cpm) 



    ### 4. differential analysis 

    with open('read_counts.csv', 'r') as fin:
        lines = fin.readlines()[1:]
        gene_names = [line.split()[0] for line in lines] 
    genename_list = gene_names[:len(case_df_cpm)]

    significant_genes, significant_cases, significant_controls = \
        run_differential_analysis(genename_list, case_df_cpm, control_df_cpm) 










