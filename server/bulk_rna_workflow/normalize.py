import numpy as np

np.random.seed(0)


def normalize_rnaseq_data(df, case_samples, control_samples):
    """
    Function to compute CPM normalization for RNA-seq data and save to files.

    Parameters:
    df (pandas.DataFrame): DataFrame with raw count data.
    case_samples (list): List with the sample names for the case group.
    control_samples (list): List with the sample names for the control group.
    """

    # Separate the case and control data
    case_df = df.loc[:, case_samples]
    control_df = df.loc[:, control_samples]

    # Function to compute CPM
    def compute_cpm(df):
        return df.div(df.sum()) * 1e6

    # Compute CPM for case and control
    case_df_cpm = compute_cpm(case_df)
    control_df_cpm = compute_cpm(control_df)
    return case_df_cpm, control_df_cpm