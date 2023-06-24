import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.manifold import TSNE

def normalize_and_visualize(df, case_samples, control_samples):
    """
    Function to compute CPM normalization for RNA-seq data, apply t-SNE, and visualize the embedding.

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

    # Combine the case and control data
    normalized_data = pd.concat([case_df_cpm, control_df_cpm])

    # Normalize the combined data
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(normalized_data)

    # Compute t-SNE embedding
    tsne = TSNE(n_components=2, perplexity=30, learning_rate=200)
    tsne_embedding = tsne.fit_transform(normalized_data)

    # Visualize the t-SNE embedding
    case_samples_count = len(case_samples)
    control_samples_count = len(control_samples)
    
    plt.figure(figsize=(10, 8))
    plt.scatter(tsne_embedding[:case_samples_count, 0], tsne_embedding[:case_samples_count, 1], color='red', label='Case')
    plt.scatter(tsne_embedding[case_samples_count:, 0], tsne_embedding[case_samples_count:, 1], color='blue', label='Control')
    plt.xlabel('t-SNE Dimension 1')
    plt.ylabel('t-SNE Dimension 2')
    plt.title('t-SNE Visualization')
    plt.legend()
    plt.show()

# Usage:
# df = pd.read_csv('your_data.csv', index_col=0)
# case_samples = ['sample1', 'sample2', 'sample3']
# control_samples = ['sample4', 'sample5', 'sample6']
# normalize_and_visualize(df, case_samples, control_samples)
