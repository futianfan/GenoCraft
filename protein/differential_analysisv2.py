import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
# from sklearn.manifold import UMAP
import umap 
from matplotlib_venn import venn2
import statsmodels.api as sm
import numpy as np 

# Differential Analysis Function
def run_differential_analysis(gene_names, df_cases, df_controls):
    significant_genes = []
    p_values = []
    fold_changes = []

    for i, gene in enumerate(gene_names):
        case_data = df_cases.iloc[i, :]
        control_data = df_controls.iloc[i, :]
        fold_change = np.mean(case_data) - np.mean(control_data)
        _, p_value = stats.ttest_ind(case_data, control_data)
        p_values.append(p_value)
        fold_changes.append(fold_change)
        if p_value < 0.2:  # p-value threshold for significance
            significant_genes.append(gene)

    gene_indices = [i for i in range(len(gene_names)) if gene_names[i] in significant_genes]
    significant_cases = df_cases.iloc[gene_indices, :]
    significant_controls = df_controls.iloc[gene_indices, :]

    df_p_values = pd.DataFrame({
        'Gene': gene_names,
        'p-value': p_values,
        'Fold Change': fold_changes
    })

    return significant_genes, significant_cases, significant_controls, df_p_values

# Visualization Functions
def plot_volcano(df_p_values):
    df_p_values['-log10(p-value)'] = -np.log10(df_p_values['p-value'])
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x='Fold Change', y='-log10(p-value)', data=df_p_values, hue=(df_p_values['p-value'] < 0.2), palette=['grey', 'red'])
    plt.title("Volcano Plot")
    plt.xlabel("Fold Change")
    plt.ylabel("-log10(p-value)")
    plt.savefig("figure/Volcano.png")

# def plot_pca(df, labels):
#     pca = PCA(n_components=2)
#     principal_components = pca.fit_transform(df.T)
#     plt.figure(figsize=(10, 7))
#     sns.scatterplot(x=principal_components[:, 0], y=principal_components[:, 1], hue=labels)
#     plt.title("PCA Plot")
#     plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.2f}%)")
#     plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.2f}%)")
#     plt.savefig("figure/pca.png")

from sklearn.impute import SimpleImputer
def plot_pca(df, labels):
    # Impute missing values using the mean of each gene
    imputer = SimpleImputer(strategy='mean')
    df_imputed = imputer.fit_transform(df.T)
    
    # Perform PCA
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(df_imputed)
    
    # Plot the PCA results
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x=principal_components[:, 0], y=principal_components[:, 1], hue=labels)
    plt.title("PCA Plot")
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.2f}%)")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.2f}%)")
    plt.savefig("figure/pca.png")


import umap.umap_ as umap

def plot_umap(df, labels):
    imputer = SimpleImputer(strategy='mean')
    df_imputed = imputer.fit_transform(df.T)
    
    # Create and fit the UMAP model
    umap_model = umap.UMAP(n_components=2, random_state=42)
    umap_embedding = umap_model.fit_transform(df_imputed)
    
    # Plot the UMAP results
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x=umap_embedding[:, 0], y=umap_embedding[:, 1], hue=labels)
    plt.title("UMAP Plot")
    plt.savefig("figure/umap.png")


# def plot_umap(df, labels):
#     umap_model = umap(n_components=2, random_state=42)
#     umap_embedding = umap_model.fit_transform(df.T)
#     plt.figure(figsize=(10, 7))
#     sns.scatterplot(x=umap_embedding[:, 0], y=umap_embedding[:, 1], hue=labels)
#     plt.title("UMAP Plot")
#     plt.savefig("figure/umap.png")

def plot_heatmap(df):
    plt.figure(figsize=(12, 10))
    sns.heatmap(df, cmap="viridis")
    plt.title("Heatmap of Significant Genes")
    plt.savefig("figure/heatmap.png")

def plot_venn(set1, set2, labels=("Set1", "Set2")):
    plt.figure(figsize=(7, 7))
    venn2([set(set1), set(set2)], set_labels=labels)
    plt.title("Venn Diagram")
    plt.savefig("figure/venn.png")

def plot_boxplot(df_cases, df_controls):
    combined_df = pd.concat([df_cases.melt(value_name='Expression', var_name='Sample'), 
                             df_controls.melt(value_name='Expression', var_name='Sample')], axis=0)
    plt.figure(figsize=(10, 7))
    sns.boxplot(x='Sample', y='Expression', data=combined_df)
    plt.title("Boxplot of Significant Genes")
    plt.savefig("figure/boxplot.png")

def plot_qqplot(p_values):
    sm.qqplot(p_values, line='45')
    plt.title("QQ Plot of p-values")
    plt.savefig("figure/qqplot.png")

def plot_mean_variance(df_cases, df_controls):
    mean_expression = pd.concat([df_cases.mean(axis=1), df_controls.mean(axis=1)], axis=0)
    variance_expression = pd.concat([df_cases.var(axis=1), df_controls.var(axis=1)], axis=0)
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x=mean_expression, y=variance_expression)
    plt.title("Mean-Variance Trend Plot")
    plt.xlabel("Mean Expression")
    plt.ylabel("Variance")
    plt.savefig("figure/mean_variance.png")

if __name__ == '__main__':
    
    ### 1. Quality Control 
    df = pd.read_csv('read_counts.csv', sep='\t')
    from quality_control import filter_low_counts 
    df_filtered = filter_low_counts(df)

    ### 2. Normalize 
    with open('case.txt') as fin:
        case_samples = [line.strip() for line in fin.readlines()]
    with open('control.txt') as fin:
        control_samples = [line.strip() for line in fin.readlines()]

    from Normalize import normalize_rnaseq_data 
    df, case_df_cpm, control_df_cpm = normalize_rnaseq_data(df_filtered, case_samples, control_samples)

    cutoff=1000
    ### 3. Visualize 
    case_df_cpm = case_df_cpm[:cutoff]
    control_df_cpm = control_df_cpm[:cutoff]
    from Visualize import visualize  
    stream = visualize(case_df_cpm, control_df_cpm) 

    ### 4. Differential Analysis 
    genename_list_short = df.index.tolist()[:cutoff]
    print(genename_list_short, len(genename_list_short), case_df_cpm.shape, '+++++++++')
    significant_genes, significant_cases, significant_controls, df_p_values = run_differential_analysis(genename_list_short, case_df_cpm, control_df_cpm)
    
    with open('significant_gene.txt', 'w') as fout:
        for gene in significant_genes:
            fout.write(str(gene) + '\n')

    ### 5. Visualization of Differential Analysis Results
    # Plotting the results using the defined visualization functions
    plot_volcano(df_p_values)
    plot_pca(pd.concat([case_df_cpm, control_df_cpm], axis=0), labels=case_samples + control_samples)
    plot_umap(pd.concat([case_df_cpm, control_df_cpm], axis=0), labels=case_samples + control_samples)
    plot_heatmap(significant_cases)
    plot_venn(significant_genes, genename_list_short, labels=("Significant Genes", "All Genes"))
    plot_boxplot(significant_cases, significant_controls)
    plot_qqplot(df_p_values['p-value'])
    plot_mean_variance(significant_cases, significant_controls)



