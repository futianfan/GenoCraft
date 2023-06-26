import numpy as np
import pandas as pd

def impute_missing_values(df):
    """
    Impute missing values with the minimum observed value for each protein.

    Parameters:
    df (pandas.DataFrame): DataFrame with raw protein expression data.

    Returns:
    df_imputed (pandas.DataFrame): DataFrame with imputed values for missing data.
    """
    # Compute the minimum value for each protein
    min_values = df.min()
    # Impute missing values
    df_imputed = df.fillna(min_values)
    
    return df_imputed

if __name__ == "__main__":
    import pandas as pd 
    # df = pd.read_csv('read_counts.csv', index_col=0)
    df = pd.read_csv('read_counts.csv', sep = '\t')
    from quality_control import filter_low_counts
    df_filtered = filter_low_counts(df)
    print(df)
    print(df_filtered)
    df_imputed = impute_missing_values(df_filtered)




# # Impute missing values
# df_imputed = impute_missing_values(df)

# # Now pass the imputed dataframe to the normalization function
# df, case_df_cpm, control_df_cpm = normalize_rnaseq_data(df_imputed, case_samples)



