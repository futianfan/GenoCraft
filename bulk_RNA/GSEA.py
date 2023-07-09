import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import csv
import io 
from pandas.core.frame import DataFrame 


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

def save_stream_to_file(stream, filepath):
    # Create a Matplotlib figure from the stream
    fig = plt.figure()
    fig.canvas.draw()

    # Save the figure to the file
    fig.savefig(filepath, format='png', bbox_inches='tight')
    
    # Close the figure to free up resources
    plt.close(fig)
    
    print(f"Image saved to {filepath}")





def plot_results(data, csv_filename):
    kegg = data['KEGG_2021_Human']

    # sort the results by p-value
    kegg.sort(key=lambda x: x[2])

    # Get the pathway names
    pathways = [result[1] for result in kegg]
    
    # Get the p-values and apply -log10 transformation
    p_values_raw = [result[2] for result in kegg]
    p_values_log10 = [-np.log10(result[2]) for result in kegg]



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
    # Save the pathway names and p-values to a CSV file
    # with open(csv_filename, 'w', newline='') as csvfile:
    #     fieldnames = ['Pathway', 'P-value']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    #     writer.writeheader()
    #     for pathway, p_value in zip(pathways, p_values):
    #         writer.writerow({'Pathway': pathway, 'P-value': p_value})
    df = DataFrame({'Pathway': pathways, 'P-value': p_values_raw})
    return stream, df  


def run_gsea_analysis(gene_names_file, csv_filename):
    with open(gene_names_file, 'r') as file:
        gene_names = [line.strip() for line in file.readlines()]

    enrichment_data = perform_enrichment_analysis(gene_names)
    results = get_enrichment_results(enrichment_data)
    stream, df = plot_results(results, csv_filename)
    return stream, df 

if __name__ == '__main__':
    
    ### 1. quality control 
    import pandas as pd 
    from quality_control import filter_low_counts 
    # df = pd.read_csv('read_counts.csv', index_col=0)
    df = pd.read_csv('read_counts.csv', sep = '\t')
    df_filtered = filter_low_counts(df)

    ### 2. normalize 
    with open('case_label.txt') as fin:
        lines = fin.readlines() 
        case_samples = [line.strip() for line in lines]
    with open('control_label.txt') as fin:
        lines = fin.readlines() 
        control_samples = [line.strip() for line in lines]

    from Normalize import normalize_rnaseq_data 
    # print(case_samples, control_samples)
    df, case_df_cpm, control_df_cpm = normalize_rnaseq_data(df, case_samples, control_samples)

    ### 3. visualize 
    case_df_cpm = case_df_cpm[:1000]
    control_df_cpm = control_df_cpm[:1000]
    print(df, case_df_cpm, control_df_cpm)
    print(case_df_cpm.isna().sum())
    print(control_df_cpm.isna().sum()) 
    from Visualize import visualize  
    stream = visualize(case_df_cpm, control_df_cpm) 

    ### 4. differential analysis 
    from differential_analysis import run_differential_analysis
    with open('read_counts.csv', 'r') as fin:
        lines = fin.readlines()[1:]
        gene_names = [line.split()[0] for line in lines] 
    genename_list = gene_names[:len(case_df_cpm)]

    significant_genes, significant_cases, significant_controls = \
        run_differential_analysis(genename_list, case_df_cpm, control_df_cpm) 

    print(' ', significant_genes)
    exit() 

    ### 5/6. GSEA 
    gene_names_file = 'significant_gene.txt'
    stream = run_gsea_analysis(gene_names_file, 'pathway_with_pvalues.csv')
    save_stream_to_file(stream, 'tmp.png')




