from sklearn.manifold import TSNE
from sklearn.preprocessing import MinMaxScaler 
import numpy as np 
import matplotlib.pyplot as plt
import io 
import pandas as pd 

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

	fig, ax = plt.subplots()
	stream = io.BytesIO()

	plt.figure(figsize=(10, 8))
	plt.scatter(tsne_embedding[:case_samples_count, 0], tsne_embedding[:case_samples_count, 1], color='red', label='Case')
	plt.scatter(tsne_embedding[case_samples_count:, 0], tsne_embedding[case_samples_count:, 1], color='blue', label='Control')
	plt.xlabel('t-SNE Dimension 1')
	plt.ylabel('t-SNE Dimension 2')
	plt.title('t-SNE Visualization')
	plt.legend()

	fig.savefig(stream, format='png')
	stream.seek(0)
	plt.close(fig)

	return stream 

# plt.savefig('visualize.png')

# # Run t-SNE
# tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
# tsne_results = tsne.fit_transform(pca_result)



# # Plot t-SNE
# plt.figure(figsize=(8,8))
# plt.scatter(tsne_results[:,0], tsne_results[:,1])
# plt.xlabel('t-SNE 1')
# plt.ylabel('t-SNE 2')
# plt.show()



if __name__ == '__main__':
    from quality_control import filter_low_counts 
    # df = pd.read_csv('read_counts.csv', index_col=0)
    df = pd.read_csv('../demo_data/bulk_data/read_counts.csv', sep ='\t')
    df_filtered = filter_low_counts(df)
    with open('../demo_data/bulk_data/case.txt') as fin:
        lines = fin.readlines() 
        case_samples = [line.strip() for line in lines]
    with open('../demo_data/bulk_data/control.txt') as fin:
        lines = fin.readlines() 
        control_samples = [line.strip() for line in lines]

    from Normalize import normalize_rnaseq_data 
    # print(case_samples, control_samples)
    df, case_df_cpm, control_df_cpm = normalize_rnaseq_data(df, case_samples, control_samples)
    case_df_cpm = case_df_cpm[:1000]
    control_df_cpm = control_df_cpm[:1000]
    print(df, case_df_cpm, control_df_cpm)

    stream = visualize(case_df_cpm, control_df_cpm) 



