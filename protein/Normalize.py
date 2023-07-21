import numpy as np
import pandas as pd

np.random.seed(0)



def normalize_rnaseq_data(df, case_samples, control_samples):
    """
    Function to compute CPM normalization for RNA-seq data and save to files.

    Parameters:
    df (pandas.DataFrame): DataFrame with raw count data.
    case_samples (list): List with the sample names for the case group.
    control_samples (list): List with the sample names for the control group.
    """

    df = df.apply(pd.to_numeric, errors='ignore')


    # Separate the case and control data
    case_df = df[case_samples]
    control_df = df[control_samples]

    # Function to compute CPM
    def compute_cpm(df):
        return df.div(df.sum()) * 1e6

    # Compute CPM for case and control
    case_df_cpm = compute_cpm(case_df)
    control_df_cpm = compute_cpm(control_df)
    return df, case_df_cpm, control_df_cpm 

    # Save the gene names to a text file
    # with open('genename.txt', 'w') as f:
    #     for gene in df.index:
    #         f.write(gene + '\n')

    # Save the CPM-normalized case and control data to TXT files
    # case_df_cpm.to_csv('case.txt', sep='\t')
    # control_df_cpm.to_csv('control.txt', sep='\t')
# Usage:
# df = pd.read_csv('your_data.csv', index_col=0)
# case_samples = ['sample1', 'sample2', 'sample3']
# control_samples = ['sample4', 'sample5', 'sample6']
# normalize_rnaseq_data(df, case_samples, control_samples)



if __name__ == '__main__':
    from quality_control import filter_low_counts 
    # df = pd.read_csv('read_counts.csv', index_col=0)
    df = pd.read_csv('read_counts.csv', sep = '\t')
    df_filtered = filter_low_counts(df)
    from impute import impute_missing_values
    df_imputed = impute_missing_values(df_filtered)


    with open('case_label.txt') as fin:
        lines = fin.readlines() 
        case_samples = [line.strip() for line in lines]
    with open('control_label.txt') as fin:
        lines = fin.readlines() 
        control_samples = [line.strip() for line in lines]

    # print(case_samples, control_samples)
    df, case_df_cpm, control_df_cpm = normalize_rnaseq_data(df_imputed, case_samples, control_samples)
    print(df, case_df_cpm, control_df_cpm)

    ''' 
        df: 
            39376 rows x 19 columns

        case_df_cpm: 
            39376 rows x 10 columns

        control_df_cpm:
            39376 rows x 8 columns

    '''


# if __name__ == "__main__":
#     # Function to generate RNA-seq count data
#     def generate_data(n_genes, n_samples, baseline, fold_change, upregulated_genes):
#         data = np.random.poisson(lam=baseline, size=(n_genes, n_samples))
#         data[upregulated_genes, :] *= fold_change
#         return data

#     # Define parameters
#     n_genes = 5
#     n_case_samples = 3
#     n_control_samples = 3
#     baseline = 100
#     fold_change = 2

#     # Generate data for case and control groups
#     case_data = generate_data(n_genes, n_case_samples, baseline, fold_change, [0, 1])
#     control_data = generate_data(n_genes, n_control_samples, baseline, fold_change, [3, 4])

#     # Combine the data and create a DataFrame
#     data = np.concatenate([case_data, control_data], axis=1)
#     genes = ['gene' + str(i+1) for i in range(n_genes)]
#     samples = ['sample' + str(i+1) for i in range(n_case_samples + n_control_samples)]
#     df = pd.DataFrame(data, index=genes, columns=samples)

#     case_samples = ['sample1', 'sample2', 'sample3']
#     control_samples = ['sample4', 'sample5', 'sample6']

#     print(df)
#     normalize_rnaseq_data(df, case_samples, control_samples)




