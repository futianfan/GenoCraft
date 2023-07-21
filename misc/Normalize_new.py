import pandas as pd

def normalize(df, case_samples, control_samples):
    """
    Function to compute CPM normalization for RNA-seq data and save to files.

    Parameters:
    df (pandas.DataFrame): DataFrame with raw count data.
    case_samples (list): List with the sample names for the case group.
    control_samples (list): List with the sample names for the control group.
    """

    # Separate the case and control data
    case_df = df[case_samples]
    control_df = df[control_samples]

    # Function to compute CPM
    def compute_cpm(df):
        return df.div(df.sum()) * 1e6

    # Compute CPM for case and control
    case_df_cpm = compute_cpm(case_df)
    control_df_cpm = compute_cpm(control_df)

    # Save the gene names to a text file
    with open('genename.txt', 'w') as f:
        for gene in df.index:
            f.write(gene + '\n')

    # Save the CPM-normalized case and control data to TXT files
    case_df_cpm.to_csv('case.txt', sep='\t')
    control_df_cpm.to_csv('control.txt', sep='\t')

# Usage:
# df = pd.read_csv('your_data.csv', index_col=0)
# case_samples = ['sample1', 'sample2', 'sample3']
# control_samples = ['sample4', 'sample5', 'sample6']
# normalize_rnaseq_data(df, case_samples, control_samples)
