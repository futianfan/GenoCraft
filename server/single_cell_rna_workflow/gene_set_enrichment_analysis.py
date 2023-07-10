import requests
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import csv
import pandas as pd
import io


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
        raise Exception(
            f"Error occurred while performing enrichment analysis. Status code: {response.status_code} Error message: {response.text}")


def get_enrichment_results(data):
    user_list_id = data['userListId']
    url = f'https://maayanlab.cloud/Enrichr/enrich?backgroundType=KEGG_2021_Human&userListId={user_list_id}'
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        raise Exception(
            f"Error occurred while fetching enrichment results. Status code: {response.status_code} Error message: {response.text}")


def plot_results(data):
    kegg = data['KEGG_2021_Human']

    if not kegg:
        return None, None

    # sort the results by p-value
    kegg.sort(key=lambda x: x[2])

    # Get the pathway names
    pathways = [result[1] for result in kegg]

    # Get the p-values and apply -log10 transformation
    p_values_raw = [result[2] for result in kegg]
    p_values_log10 = [-np.log10(result[2]) for result in kegg]

    # Create a bar plot with seaborn
    matplotlib.use('agg')
    fig, ax = plt.subplots()
    stream = io.BytesIO()
    # Plot explained variance
    # ax.plot(range(pca.n_components_), np.cumsum(pca.explained_variance_ratio_))

    # Create a bar plot with seaborn
    # ax.figure(figsize=(10, 8))
    sns.set(style="whitegrid")
    ax = sns.barplot(x=p_values_log10, y=pathways, palette="viridis", orient="h")
    plt.xlabel('-log10(p-value)', fontsize=14)
    plt.ylabel('Pathway', fontsize=14)
    plt.title('Pathway Enrichment Analysis', fontsize=16)
    # plt.savefig('GSEA.png')
    fig.savefig(stream, format='png')
    stream.seek(0)
    plt.close(fig)

    fieldnames = ['Pathway', 'P-value']
    list_of_tuples = list(zip(pathways, p_values_raw))
    df = pd.DataFrame(list_of_tuples, columns=fieldnames)

    print("=== pathway_with_pvalues ===", df.shape, df.head())
    return stream.getvalue(), df


def run_gsea_analysis(df_genename):
    gene_names = [genename[0] for genename in df_genename.values.tolist()]
    print("=== gene_names ===\n", len(gene_names), gene_names[0:10])
    enrichment_data = perform_enrichment_analysis(gene_names)
    results = get_enrichment_results(enrichment_data)

    return plot_results(results)
