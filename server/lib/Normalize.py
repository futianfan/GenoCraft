
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy import sparse
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# ## input
# count_file = 'counts.csv'
# gene_length_file = 'gene_lengths.csv'
# ## output 
# count_scaled_file = 'count_scaled.csv'


def run_normalize(count_file, gene_length_file, ):

	# Load the count matrix
	counts = pd.read_csv(count_file, index_col=0)

	# Load gene lengths. This will need to be modified to fit your actual file.
	gene_lengths = pd.read_csv(gene_length_file, index_col=0)

	# Transpose so that rows are cells and columns are genes
	counts = counts.transpose()

	# Normalization (TPM normalization)
	# Divide by gene lengths (in kilobases) to get RPK
	counts = counts.div(gene_lengths['Length'] / 1000, axis=1)

	# Then scale to sum to a million (to get TPM)
	counts = counts.div(counts.sum(axis=1), axis=0)
	counts = counts.mul(10**6)

	# Logarithmize the data
	counts = np.log1p(counts)

	# Scale data to zero mean and unit variance
	scaler = StandardScaler()
	counts_scaled = pd.DataFrame(scaler.fit_transform(counts), columns=counts.columns, index=counts.index)
	return count_scaled 
	# counts_scaled.to_csv(count_scaled_file)
