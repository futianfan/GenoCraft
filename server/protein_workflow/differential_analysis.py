import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
import io
import matplotlib
import numpy as np
from pycirclize import Circos


def run_differential_analysis(gene_names, df_cases, df_controls):
    # read in gene names and store as a list
    # gene_names = df_genename.values.tolist()
    # gene_names is list of string

    # perform t-test for each gene and select those with p-value < 0.01
    significant_genes = []
    for i, gene in enumerate(gene_names):
        case_data = df_cases.iloc[i, :]
        control_data = df_controls.iloc[i, :]
        _, p_value = stats.ttest_ind(case_data, control_data)
        if p_value < 0.2:
            significant_genes.append(gene)

    # extract data for significant genes and save to new files
    gene_indices = [i for i in range(len(gene_names)) if gene_names[i] in significant_genes]
    significant_cases = df_cases.iloc[gene_indices, :]
    significant_controls = df_controls.iloc[gene_indices, :]

    # Return dataframes as result
    significant_genes = pd.DataFrame(significant_genes)
    return significant_genes, significant_cases, significant_controls


def plot_heatmap(case_df_cpm, control_df_cpm):
    case_df = case_df_cpm.set_index('gene_name', inplace=False).add_suffix('_case')
    control_df = control_df_cpm.set_index('gene_name', inplace=False).add_suffix('_control')
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
    case_df = case_df_cpm.set_index('gene_name', inplace=False).add_suffix('_case')
    control_df = control_df_cpm.set_index('gene_name', inplace=False).add_suffix('_control')

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
        track2 = sector.add_track((50, 100))
        track2.axis()
        
        x = np.linspace(1, int(track2.size), int(data_matrix_z.shape[1]))
        xlabels = [col_name[7:].replace('control', 'cont') for col_name in data_matrix_z.columns]

        y = np.linspace(1, int(data_matrix_z.shape[0]), int(data_matrix_z.shape[0])) - 0.5
        ylabels = data_matrix_z.index

        track2.xticks(x, xlabels, outer=True)
        track2.yticks(y, ylabels)
        
        track2.heatmap(data_matrix_z.values, vmin=vmin, vmax=vmax, cmap=cmap, rect_kws=dict(ec="white", lw=1))

    circos.colorbar(bounds=(0.35, 0.45, 0.3, 0.01), vmin=vmin, vmax=vmax, orientation="horizontal", cmap=cmap)

    fig = circos.plotfig()

    fig.savefig(stream, format='png')
    stream.seek(0)

    return stream.getvalue()
    