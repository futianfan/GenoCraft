import numpy as np

np.random.seed(0)


def normalize_rnaseq_data(case_df, control_df):
    """
    Function to compute CPM normalization for RNA-seq data and save to files.
    """

    # Function to compute CPM
    def compute_cpm(df):
        return df.div(df.sum()) * 1e6

    # Compute CPM for case and control
    case_df_cpm = compute_cpm(case_df)
    control_df_cpm = compute_cpm(control_df)
    return case_df_cpm, control_df_cpm




