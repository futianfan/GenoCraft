import pandas as pd
from scipy import stats
import numpy as np
import csv

def run_DEGs_analysis(genename_file, case_file, control_file, output_file):
    # read in gene names and store as a list
    with open(genename_file, 'r') as file:
        gene_names = file.readlines() 
        gene_names = [gene.strip() for gene in gene_names]

    # read in data for cases and controls
    df_cases = pd.read_csv(case_file, header=None, sep='\t')
    df_controls = pd.read_csv(control_file, header=None, sep='\t')

    # perform t-test for each gene and select those with p-value < 0.01
    significant_genes = []
    for i, gene in enumerate(gene_names):
        case_data = df_cases.iloc[i,:]
        control_data = df_controls.iloc[i,:]
        _, p_value = stats.ttest_ind(case_data, control_data)
        if p_value < 0.001:
            significant_genes.append(gene)

    # extract data for significant genes and save to new files
    gene_indices = [i for i in range(len(gene_names)) if gene_names[i] in significant_genes]
    significant_cases = df_cases.iloc[gene_indices,:]
    significant_controls = df_controls.iloc[gene_indices,:]

    # print significant genes with corresponding p-values
    with open(output_file, 'w') as fout:
        for gene in significant_genes:
            fout.write(gene + '\n')


run_DEGs_analysis('genename.txt', 'case.txt', 'control.txt', 'significant_gene.txt')

