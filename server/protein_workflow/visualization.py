import io

from sklearn.manifold import TSNE
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib


def visualize(case_df_cpm, control_df_cpm):
    # Combine the case and control data
    normalized_data = pd.concat([case_df_cpm, control_df_cpm])

    # Normalize the combined data
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(normalized_data)
    normalized_data = np.nan_to_num(normalized_data, nan=0)
    print(normalized_data.shape)
    assert np.sum(np.isnan(normalized_data)) == 0

    # Compute t-SNE embedding
    tsne = TSNE(n_components=2, perplexity=30, learning_rate=200)
    tsne_embedding = tsne.fit_transform(normalized_data)

    # Visualize the t-SNE embedding
    case_samples_count = len(case_df_cpm)
    control_samples_count = len(control_df_cpm)

    # fig, ax = plt.subplots()
    matplotlib.use('agg')
    stream = io.BytesIO()
    # plt.figure(figsize=(10, 8))
    plt.scatter(tsne_embedding[:case_samples_count, 0], tsne_embedding[:case_samples_count, 1], color='red',
                label='Case')
    plt.scatter(tsne_embedding[case_samples_count:, 0], tsne_embedding[case_samples_count:, 1], color='blue',
                label='Control')
    plt.xlabel('t-SNE Dimension 1')
    plt.ylabel('t-SNE Dimension 2')
    plt.title('t-SNE Visualization')
    plt.legend()

    plt.savefig(stream, format='png')
    stream.seek(0)
    plt.close()

    return stream.getvalue()
