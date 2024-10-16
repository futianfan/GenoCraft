import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import csv

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

def get_enrichment_results(data):
    user_list_id = data['userListId']
    url = f'https://maayanlab.cloud/Enrichr/enrich?backgroundType=KEGG_2021_Human&userListId={user_list_id}'
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        raise Exception(f"Error occurred while fetching enrichment results. Status code: {response.status_code} Error message: {response.text}")

def plot_results(data, csv_filename):
    kegg = data['KEGG_2021_Human']

    # sort the results by p-value
    kegg.sort(key=lambda x: x[2])

    # Get the pathway names
    pathways = [result[1] for result in kegg]
    
    # Get the p-values and apply -log10 transformation
    p_values = [-np.log10(result[2]) for result in kegg]

    # Create a bar plot with seaborn
    plt.figure(figsize=(10, 8))
    sns.set(style="whitegrid")
    ax = sns.barplot(x=p_values, y=pathways, palette="viridis", orient="h")
    plt.xlabel('-log10(p-value)', fontsize=14)
    plt.ylabel('Pathway', fontsize=14)
    plt.title('Pathway Enrichment Analysis', fontsize=16)
    plt.savefig('GSEA.png')

    # Save the pathway names and p-values to a CSV file
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['Pathway', 'P-value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for pathway, p_value in zip(pathways, p_values):
            writer.writerow({'Pathway': pathway, 'P-value': p_value})

def run_gsea_analysis(gene_names_file, csv_filename):
    with open(gene_names_file, 'r') as file:
        gene_names = [line.strip() for line in file.readlines()]

    enrichment_data = perform_enrichment_analysis(gene_names)
    results = get_enrichment_results(enrichment_data)
    plot_results(results, csv_filename)

if __name__ == "__main__":
    gene_names_file = 'significant_gene.txt'
    run_gsea_analysis(gene_names_file, 'pathway_with_pvalues.csv')
