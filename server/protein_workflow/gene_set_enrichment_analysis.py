import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import csv
import io
from pandas.core.frame import DataFrame
import matplotlib


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

    # sort the results by p-value
    kegg.sort(key=lambda x: x[2])

    # Get the pathway names
    pathways = [result[1] for result in kegg]

    # Get the p-values and apply -log10 transformation
    p_values = [-np.log10(result[2]) for result in kegg]

    pathways = pathways[:10]
    p_values = p_values[:10]

    plt.cla()
    # fig, ax = plt.subplots()
    matplotlib.use('agg')
    stream = io.BytesIO()
    # # Plot explained variance
    # ax.plot(range(pca.n_components_), np.cumsum(pca.explained_variance_ratio_))

    # Create a bar plot with seaborn
    # ax.figure(figsize=(10, 8))
    sns.set(style="whitegrid")
    ax = sns.barplot(x=p_values, y=pathways, palette="viridis", orient="h")

    plt.xlabel('-log10(p-value)', fontsize=14)
    plt.ylabel('Pathway', fontsize=14)
    plt.title('Pathway Enrichment Analysis', fontsize=16)
    plt.tight_layout()

    plt.savefig(stream, format='png')
    stream.seek(0)
    plt.close()
    df = DataFrame({'Pathway': pathways, 'P-value': p_values})

    return stream.getvalue(), df


def run_gsea_analysis(df_genename):
    gene_names = [genename[0] for genename in df_genename.values.tolist()]

    enrichment_data = perform_enrichment_analysis(gene_names)
    results = get_enrichment_results(enrichment_data)

    return  plot_results(results)