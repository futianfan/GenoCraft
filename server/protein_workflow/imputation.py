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