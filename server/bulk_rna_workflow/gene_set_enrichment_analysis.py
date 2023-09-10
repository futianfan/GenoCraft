import io

import requests
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd


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
    plt.figure(figsize=(10, 8))
    sns.set(style="whitegrid")
    ax = sns.barplot(x=p_values_log10, y=pathways, palette="viridis", orient="h")
    plt.xlabel('-log10(p-value)', fontsize=14)
    plt.ylabel('Pathway', fontsize=14)
    plt.title('Pathway Enrichment Analysis', fontsize=16)
    stream = io.BytesIO()
    plt.savefig(stream, format='png')
    stream.seek(0)
    plt.close()

    fieldnames = ['Pathway', 'P-value']
    list_of_tuples = list(zip(pathways, p_values_raw))
    df = pd.DataFrame(list_of_tuples, columns=fieldnames)
    return stream.getvalue(), df


def run_gsea_analysis(gene_names):
    enrichment_data = perform_enrichment_analysis(gene_names)
    results = get_enrichment_results(enrichment_data)

    return plot_results(results)
