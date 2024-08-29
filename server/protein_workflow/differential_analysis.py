import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import io
import matplotlib
import numpy as np
from pycirclize import Circos

## new ## 
from sklearn.decomposition import PCA
import umap 
import umap.umap_ as umap
from matplotlib_venn import venn2
import statsmodels.api as sm
from sklearn.impute import SimpleImputer

### V1 
# def run_differential_analysis(gene_names, df_cases, df_controls):
#     # read in gene names and store as a list
#     # gene_names = df_genename.values.tolist()
#     # gene_names is list of string

#     # perform t-test for each gene and select those with p-value < 0.01
#     significant_genes = []
#     for i, gene in enumerate(gene_names):
#         case_data = df_cases.iloc[i, :]
#         control_data = df_controls.iloc[i, :]
#         _, p_value = stats.ttest_ind(case_data, control_data)
#         if p_value < 0.2:
#             significant_genes.append(gene)

#     # extract data for significant genes and save to new files
#     gene_indices = [i for i in range(len(gene_names)) if gene_names[i] in significant_genes]
#     significant_cases = df_cases.iloc[gene_indices, :]
#     significant_controls = df_controls.iloc[gene_indices, :]

#     # Return dataframes as result
#     significant_genes = pd.DataFrame(significant_genes)
#     return significant_genes, significant_cases, significant_controls

### V2  2024.08.29 
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


def plot_heatmap(case_df_cpm, control_df_cpm):
    case_df = case_df_cpm.add_suffix('_case')
    control_df = control_df_cpm.add_suffix('_control')
    data_matrix = pd.concat([control_df, case_df], axis=1)

    # z-score
    data_matrix_z = data_matrix.apply(lambda x: (x - x.mean())/x.std(), axis=0)

    # Create the heatmap
    matplotlib.use('agg')
    stream = io.BytesIO()

    plt.figure(figsize=(10, 8)) 
    sns.set(font_scale=1)

    # define the color
    cmap = sns.diverging_palette(240, 10, as_cmap=True)

    cg = sns.clustermap(
        data_matrix_z,
        row_cluster=True, 
        col_cluster=False, 
        cmap=cmap,
        standard_scale=1,
        figsize=(10, 8)
    )

    # adjust the position of legend
    cg.cax.set_position([0.05, 0.85, 0.03, 0.15])

    plt.xticks(rotation=90)

    plt.savefig(stream, format='png')
    stream.seek(0)
    plt.close()

    return stream.getvalue()

def plot_circlize(case_df_cpm, control_df_cpm):
    case_df = case_df_cpm.add_suffix('_case')
    control_df = control_df_cpm.add_suffix('_control')

    data_matrix = pd.concat([control_df, case_df], axis=1)

    # Compute z-scores for the rows (proteins)
    data_matrix_z = data_matrix.apply(lambda x: (x - x.mean())/x.std(), axis=0)

    sectors = {"A": 100}
    circos = Circos(sectors, space=20)

    vmin, vmax = data_matrix_z.values.min(), data_matrix_z.values.max()

    matplotlib.use('agg')
    stream = io.BytesIO()

    cmap = sns.diverging_palette(240, 10, as_cmap=True)

    for sector in circos.sectors:
        # Plot heatmap with labels
        track1 = sector.add_track((50, 99))
        track1.axis()

        len_x = int(data_matrix_z.shape[1])
        interval_v = track1.size / (len_x)
        x = np.linspace(interval_v, int(track1.size), len_x) - interval_v/2
        xlabels = [col_name[7:].replace('control', 'cont') for col_name in data_matrix_z.columns]

        y = np.linspace(1, int(data_matrix_z.shape[0]), int(data_matrix_z.shape[0])) - 0.5
        ylabels = data_matrix_z.index

        track1.xticks(x, xlabels, outer=True)
        track1.yticks(y, ylabels, vmin=0, vmax=int(data_matrix_z.shape[0]))
        
        track1.heatmap(data_matrix_z.values, vmin=vmin, vmax=vmax, cmap=cmap, end=track1.end-0.000001, rect_kws=dict(ec="white", lw=1))

    circos.colorbar(bounds=(0.35, 0.45, 0.3, 0.01), vmin=vmin, vmax=vmax, orientation="horizontal", cmap=cmap)

    fig = circos.plotfig()

    fig.savefig(stream, format='png')
    stream.seek(0)

    return stream.getvalue()


def plot_volcano(df_p_values):
    matplotlib.use('agg')
    stream = io.BytesIO()

    df_p_values['-log10(p-value)'] = -np.log10(df_p_values['p-value'])
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x='Fold Change', y='-log10(p-value)', data=df_p_values, hue=(df_p_values['p-value'] < 0.2), palette=['grey', 'red'])
    plt.title("Volcano Plot")
    plt.xlabel("Fold Change")
    plt.ylabel("-log10(p-value)")
    # plt.savefig("figure/Volcano.png")

    plt.savefig(stream, format='png')
    stream.seek(0)
    plt.close()
    return stream.getvalue()


def plot_pca(df, labels):
    matplotlib.use('agg')
    stream = io.BytesIO()

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
    # plt.savefig("figure/pca.png")

    plt.savefig(stream, format='png')
    stream.seek(0)
    plt.close()
    return stream.getvalue()



def plot_umap(df, labels):
    matplotlib.use('agg')
    stream = io.BytesIO()

    imputer = SimpleImputer(strategy='mean')
    df_imputed = imputer.fit_transform(df.T)
    
    # Create and fit the UMAP model
    umap_model = umap.UMAP(n_components=2, random_state=42)
    umap_embedding = umap_model.fit_transform(df_imputed)
    
    # Plot the UMAP results
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x=umap_embedding[:, 0], y=umap_embedding[:, 1], hue=labels)
    plt.title("UMAP Plot")
    # plt.savefig("figure/umap.png")

    plt.savefig(stream, format='png')
    stream.seek(0)
    plt.close()
    return stream.getvalue()


# def plot_heatmap(df):
#     matplotlib.use('agg')
#     stream = io.BytesIO()

#     plt.figure(figsize=(12, 10))
#     sns.heatmap(df, cmap="viridis")
#     plt.title("Heatmap of Significant Genes")
#     # plt.savefig("figure/heatmap.png")

#     plt.savefig(stream, format='png')
#     stream.seek(0)
#     plt.close()
#     return stream.getvalue()


def plot_venn(set1, set2, labels=("Set1", "Set2")):
    matplotlib.use('agg')
    stream = io.BytesIO()

    plt.figure(figsize=(7, 7))
    venn2([set(set1), set(set2)], set_labels=labels)
    plt.title("Venn Diagram")
    # plt.savefig("figure/venn.png")

    plt.savefig(stream, format='png')
    stream.seek(0)
    plt.close()
    return stream.getvalue()

def plot_boxplot(df_cases, df_controls):
    matplotlib.use('agg')
    stream = io.BytesIO()

    combined_df = pd.concat([df_cases.melt(value_name='Expression', var_name='Sample'), 
                             df_controls.melt(value_name='Expression', var_name='Sample')], axis=0)
    plt.figure(figsize=(10, 7))
    sns.boxplot(x='Sample', y='Expression', data=combined_df)
    plt.title("Boxplot of Significant Genes")
    # plt.savefig("figure/boxplot.png")

    plt.savefig(stream, format='png')
    stream.seek(0)
    plt.close()
    return stream.getvalue()
 

def plot_qqplot(p_values):
    matplotlib.use('agg')
    stream = io.BytesIO()

    sm.qqplot(p_values, line='45')
    plt.title("QQ Plot of p-values")
    # plt.savefig("figure/qqplot.png")

    plt.savefig(stream, format='png')
    stream.seek(0)
    plt.close()
    return stream.getvalue()

def plot_mean_variance(df_cases, df_controls):
    matplotlib.use('agg')
    stream = io.BytesIO()

    mean_expression = pd.concat([df_cases.mean(axis=1), df_controls.mean(axis=1)], axis=0)
    variance_expression = pd.concat([df_cases.var(axis=1), df_controls.var(axis=1)], axis=0)
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x=mean_expression, y=variance_expression)
    plt.title("Mean-Variance Trend Plot")
    plt.xlabel("Mean Expression")
    plt.ylabel("Variance")
    # plt.savefig("figure/mean_variance.png")

    plt.savefig(stream, format='png')
    stream.seek(0)
    plt.close()
    return stream.getvalue()




    