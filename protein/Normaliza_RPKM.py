import numpy as np
import pandas as pd

np.random.seed(0)

def compute_fpkm(df, gene_lengths):
    """
    Compute FPKM normalization for RNA-seq data.

    Parameters:
    df (pandas.DataFrame): DataFrame with raw count data for samples.
    gene_lengths (pandas.Series): Series with gene lengths in base pairs.

    Returns:
    pandas.DataFrame: DataFrame with FPKM-normalized data.
    """
    # Convert gene lengths from base pairs to kilobases
    gene_lengths_kb = gene_lengths / 1000

    # Calculate the total mapped reads (sum over each column)
    total_mapped_reads = df.sum()

    # Divide each cell by the gene length in kilobases to get reads per kilobase
    rpkm = df.div(gene_lengths_kb, axis=0)

    # Then, divide by the total mapped reads in millions to get FPKM
    fpkm = rpkm.div(total_mapped_reads / 1e6, axis=1)
    return fpkm

def normalize_rnaseq_data(df, case_samples, control_samples, gene_lengths):
    """
    Function to compute FPKM normalization for RNA-seq data and return normalized data.

    Parameters:
    df (pandas.DataFrame): DataFrame with raw count data.
    case_samples (list): List with the sample names for the case group.
    control_samples (list): List with the sample names for the control group.
    gene_lengths (pandas.Series): Series with gene lengths in base pairs.

    Returns:
    Tuple of DataFrames: raw DataFrame, case normalized DataFrame, control normalized DataFrame
    """
    # Separate the case and control data
    case_df = df[case_samples]
    control_df = df[control_samples]

    # Compute FPKM for case and control
    case_df_fpkm = compute_fpkm(case_df, gene_lengths)
    control_df_fpkm = compute_fpkm(control_df, gene_lengths)

    return df, case_df_fpkm, control_df_fpkm

# Example Usage
if __name__ == '__main__':
    from quality_control import filter_low_counts
    df = pd.read_csv('read_counts.csv', sep='\t', index_col=0)
    gene_lengths = pd.Series(df['gene_length'])  # Assuming gene lengths are in a column 'gene_length'
    df_filtered = filter_low_counts(df.drop(columns='gene_length'))  # Drop or separate the gene length for processing counts only
    from impute import impute_missing_values
    df_imputed = impute_missing_values(df_filtered)

    with open('case_label.txt') as fin:
        case_samples = [line.strip() for line in fin.readlines()]
    with open('control_label.txt') as fin:
        control_samples = [line.strip() for line in fin.readlines()]

    df, case_df_fpkm, control_df_fpkm = normalize_rnaseq_data(df_imputed, case_samples, control_samples, gene_lengths)
    print(df, case_df_fpkm, control_df_fpkm)
