import io

import requests
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
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

    '''
    matplotlib.use('agg')
    stream = io.BytesIO()
    sns.set(style="whitegrid")
    ax = sns.barplot(x=p_values_log10, y=pathways, palette="viridis", orient="h")
    plt.xlabel('-log10(p-value)', fontsize=14)
    plt.ylabel('Pathway', fontsize=14)
    plt.title('Pathway Enrichment Analysis', fontsize=16)

    plt.savefig(stream, format='png')
    stream.seek(0)
    '''

    fieldnames = ['Pathway', 'P-value']
    list_of_tuples = list(zip(pathways, p_values_log10))
    df = pd.DataFrame(list_of_tuples, columns=fieldnames)
    print("=== pathway_with_pvalues ===", df.shape, df.head())

    # Sort the DataFrame by the second column (p-value) in descending order
    df_sorted = df.sort_values(by=df.columns[1], ascending=False)

    # Select the top 10 rows
    top_10 = df_sorted.head(10)
    print("=== top_10 ===\n", top_10)

    # Define colors for the bars
    colors = plt.cm.get_cmap('tab10', len(top_10))

    # Plot the graph
    matplotlib.use('agg')
    stream = io.BytesIO()
    plt.figure(figsize=(10, 6))
    bars = plt.barh(top_10[df.columns[0]], top_10[df.columns[1]], color=colors(np.arange(len(top_10))))

    plt.xlabel('P-value')
    plt.ylabel('Pathway')
    plt.title('Top 10 Pathways by P-value')
    plt.gca().invert_yaxis()

    # Add legend showing the pathway names and their corresponding colors
    legend_labels = top_10[df.columns[0]]
    plt.autoscale()
    plt.legend(bars, legend_labels, loc='lower right')

    plt.savefig(stream, format='png')
    stream.seek(0)
    plt.close()
    return stream.getvalue(), df


def run_gsea_analysis(df_genename):
    gene_names = [genename[0] for genename in df_genename.values.tolist()]
    print("=== gene_names ===\n", len(gene_names), gene_names[0:10])
    enrichment_data = perform_enrichment_analysis(gene_names)
    results = get_enrichment_results(enrichment_data)

    return plot_results(results)
