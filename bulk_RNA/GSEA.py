import pandas as pd
from scipy.stats import ttest_ind
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import csv
import io
from pandas.core.frame import DataFrame

# Load the raw counts data
file_path = '/mnt/data/GSE152418_p20047_Study1_RawCounts.csv'
df_raw_counts = pd.read_csv(file_path)

# Quality control: Filter out low-expressed genes based on a threshold
def filter_low_counts(df, threshold=10):
    return df[df.iloc[:, 1:].sum(axis=1) > threshold]

df_filtered = filter_low_counts(df_raw_counts)

# Normalization: Perform CPM normalization
def normalize_rnaseq_data(df):
    total_counts = df.iloc[:, 1:].sum(axis=0)
    cpm = df.iloc[:, 1:].div(total_counts, axis=1) * 1e6
    return df.iloc[:, 0], cpm

genes, df_normalized = normalize_rnaseq_data(df_filtered)

# Split samples into case and control
num_samples = df_normalized.shape[1]
case_samples = df_normalized.columns[:num_samples // 2].tolist()
control_samples = df_normalized.columns[num_samples // 2:].tolist()

# Optimized t-test for differential expression analysis
def run_optimized_ttest_analysis(df_normalized, case_samples, control_samples, p_value_threshold=0.05):
    case_data = df_normalized[case_samples]
    control_data = df_normalized[control_samples]
    t_stats, p_values = ttest_ind(case_data, control_data, axis=1, equal_var=False)
    significant_genes = df_normalized.index[p_values < p_value_threshold].tolist()
    return significant_genes

significant_genes_p_05 = run_optimized_ttest_analysis(df_normalized, case_samples, control_samples, p_value_threshold=0.05)

# Map ENSEMBL IDs to gene symbols (mock-up predefined mapping)
ensembl_to_symbol_extended = {
    'ENSG00000227232': 'WASH7P',
    'ENSG00000278267': 'MIR1302-10',
    'ENSG00000268903': 'OR4F5',
    'ENSG00000279928': 'RP11-34P13.7',
    'ENSG00000225972': 'APC',
    'ENSG00000237973': 'BRAF',
    'ENSG00000229344': 'BRCA1',
    'ENSG00000228794': 'EGFR',
    'ENSG00000234711': 'TP53',
    'ENSG00000230699': 'PTEN',
    'ENSG00000223764': 'TSPAN6',
    'ENSG00000187583': 'ZFP36',
    'ENSG00000187642': 'HSP90AB1',
    'ENSG00000131591': 'GAPDH',
    'ENSG00000078808': 'SDHA',
    'ENSG00000176022': 'ENO1',
    'ENSG00000260179': 'MIRLET7BHG',
    'ENSG00000169962': 'RPLP1',
    'ENSG00000162576': 'TUBA1B',
    'ENSG00000175756': 'RPL13A'
}

# Map the ENSEMBL IDs to gene symbols
significant_genes_ensembl_ids_p_05 = df_filtered.loc[significant_genes_p_05, 'ENSEMBLID'].tolist()
significant_gene_symbols_p_05 = [ensembl_to_symbol_extended.get(ensembl, 'Unknown') for ensembl in significant_genes_ensembl_ids_p_05]

# Perform Enrichment Analysis using Enrichr API
def perform_enrichment_analysis(gene_names):
    url = 'https://maayanlab.cloud/Enrichr/addList'
    payload = {
        'list': (None, '\n'.join(gene_names)),
        'description': (None, 'Gene List')
    }
    response = requests.post(url, files=payload)
    if response.ok:
        return response.json()
    else:
        raise Exception(f"Error occurred while performing enrichment analysis. Status code: {response.status_code} Error message: {response.text}")

# Get Enrichment Results
def get_enrichment_results(data):
    user_list_id = data['userListId']
    url = f'https://maayanlab.cloud/Enrichr/enrich?backgroundType=Reactome_2022&userListId={user_list_id}' 
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        raise Exception(f"Error occurred while fetching enrichment results. Status code: {response.status_code} Error message: {response.text}")

# Save a figure from stream
def save_stream_to_file(stream, filepath):
    fig = plt.figure()
    fig.canvas.draw()
    fig.savefig(filepath, format='png', bbox_inches='tight')
    plt.close(fig)
    print(f"Image saved to {filepath}")

# Run Enrichment Analysis
enrichment_data = perform_enrichment_analysis(significant_gene_symbols_p_05)
enrichment_results = get_enrichment_results(enrichment_data)

# Example of using the results (You could visualize or save them as needed)
print(json.dumps(enrichment_results, indent=4))

# Print top 20 significant genes with gene symbols
print("Top 20 significant genes with gene symbols:")
for gene in significant_gene_symbols_p_05[:20]:
    print(gene)

# Plot GSEA results (for visualization)
sns.set(style="whitegrid")
p_values = [item[1] for item in enrichment_results['Reactome_2022']]
terms = [item[0] for item in enrichment_results['Reactome_2022']]
plt.figure(figsize=(10, 8))
sns.barplot(x=p_values, y=terms, palette="coolwarm")
plt.title('GSEA Enrichment Results')
plt.xlabel('p-value')
plt.ylabel('Pathways')
plt.tight_layout()
plt.show()
