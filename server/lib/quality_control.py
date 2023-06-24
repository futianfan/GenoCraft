def filter_low_counts(df, min_counts=10, min_samples=3):
    """
    Filter out genes with low counts.

    Parameters:
    df (pandas.DataFrame): DataFrame with raw count data.
    min_counts (int): Minimum count number to keep a gene.
    min_samples (int): Minimum number of samples to keep a gene.
    """
    return df[(df >= min_counts).sum(axis=1) >= min_samples]


if __name__ == "__main__":
	import pandas as pd 
	df = pd.read_csv('read_counts.csv', index_col=0)
	df_filtered = filter_low_counts(df)
	# Continue with normalization
	# normalize_rnaseq_data(df_filtered, case_samples, control_samples)	

