import sys

import pandas as pd
import plotly.graph_objs as go
import shinyswatch
from pathlib import Path
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, register_widget

sys.path.append('../')
from bulk_RNA.quality_control import filter_low_counts as bulk_rna_filter_low_counts
from bulk_RNA.Normalize import normalize_rnaseq_data as bulk_rna_normalize_rnaseq_data
from bulk_RNA.Visualize import get_data_for_visualization as bulk_rna_get_data_for_visualization
from bulk_RNA.differential_analysis import run_differential_analysis as bulk_rna_run_differential_analysis
from bulk_RNA.GSEA import run_gsea_analysis_helper as bulk_rna_run_gsea_analysis_helper


app_ui = ui.page_fluid(
    shinyswatch.theme.spacelab(),

    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_file("file", "Upload your own data:", multiple=True, accept=[".csv", ".txt"]),
            ui.output_ui("file_content")
        ),
        ui.panel_main(
            ui.navset_tab(
                ui.nav(
                    "Bulk RNA",
                    ui.head_content(
                        ui.tags.script(
                            src="https://mathjax.rstudio.com/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"
                        ),
                        ui.tags.script(
                            "if (window.MathJax) MathJax.Hub.Queue(['Typeset', MathJax.Hub]);"
                        ),
                    ),
                    ui.column(
                        10,
                        {"class": "col-md-10 col-lg-8 py-5 mx-auto text-lg-center text-left"},
                        ui.h2("Preparation"),
                    ),
                    ui.markdown(
                        """  
                        ### Import Libraries
                        ```
                        
                        import pandas as pd 
                        import re 
                        
                        from quality_control import filter_low_counts 
                        from Normalize import normalize_rnaseq_data 
                        from Visualize import visualize  
                        from differential_analysis import run_differential_analysis
                        from GSEA import run_gsea_analysis, save_stream_to_file 
                        
                        ```
                        """
                    ),
                    ui.markdown(
                        """    
                        ### Optional: Generate Input Files
                        **How to generate `read_counts.csv`**
                        
                        **Input:** 
                        ```
                        
                        read_count = pd.read_csv('GSE99611_read_count.csv', sep = ',', dtype={0: str})
                        read_count = read_count.dropna()
                        
                        print(read_count.shape)
                        print(read_count.head())
                        
                        ```
                        **Output:**
                        """
                    ),
                    ui.output_text_verbatim("raw_read_count_shape"),
                    ui.output_table("raw_read_count_head"),
                    ui.markdown(
                        """   
                        **Input:** 
                        ```
                        
                        id2name = pd.read_csv('id_to_name.csv', sep=',', encoding='latin-1')
                        first_column = id2name.iloc[:, 0]
                        last_column = id2name.iloc[:, -3]
                        id2name = dict()
                        for ii, (gene_id, gene_line) in enumerate(zip(first_column, last_column)):
                            try:
                                idx1 = gene_line.index('(')
                                idx2 = gene_line.index(')')
                            except:
                                continue 
                            gene_name = gene_line[idx1+1:idx2]
                            if (
                                any(char.islower() for char in gene_name) 
                                or len(gene_name) > 7 
                                or ' ' in gene_name 
                                or ',' in gene_name 
                                or '/' in gene_name 
                                or '-' in gene_name 
                                or "'" in gene_name
                            ): 
                                continue 
                            id2name[str(gene_id)] = gene_name
                            if ii > 10000: 
                                break 
                        read_count['gene_name'] = read_count['ID_REF'].map(id2name)
                        read_count = read_count.dropna(subset=['gene_name'])
                        
                        gene_name_list = read_count['gene_name'].tolist()
                        print(len(gene_name_list))
                        print(gene_name_list[0:10])
                        
                        ```
                        **Output:**
                        """
                    ),
                    ui.output_text_verbatim("gene_name_length"),
                    ui.output_text_verbatim("gene_name_head"),
                    ui.markdown(
                    """
                    **Input:** 
                    ```
                    
                    read_count = read_count.drop('ID_REF', axis=1)
                    read_count = read_count.set_index('gene_name')
                    
                    print(read_count.shape)
                    print(read_count.head())
                    read_count.to_csv("read_counts.csv")
                    
                    ```
                    **Output:**
                    """
                    ),
                    ui.output_text_verbatim("read_count_shape"),
                    ui.output_table("read_count_head"),
                    ui.markdown(
                        """    
                        ### Optional: Generate Case and Control Files
                        **How to generate `case_label.txt` and `control_label.txt`**
                        
                        **Input:** 
                        ```
                        
                        with open('GSE99611_sample_label.csv', 'r') as fin:
                            lines = fin.readlines() 
                        labels = [int(line.strip().split(',')[1]) for line in lines]

                        patient_names = read_count.columns.tolist()

                        case_samples = [patient for patient,label in zip(patient_names, labels) if label==1]
                        control_samples = [patient for patient,label in zip(patient_names, labels) if label==0]
                        
                        print(case_samples)
                        print(control_samples)
                        
                        pd.DataFrame(case_samples).to_csv("case_label.txt",  header=None, index=None, sep=' ')
                        pd.DataFrame(control_samples).to_csv("control_label.txt",  header=None, index=None, sep=' ')
                        
                        ```
                        **Output:**
                        """
                    ),
                    ui.output_text_verbatim("case"),
                    ui.output_text_verbatim("control"),
                    ui.column(
                        10,
                        {"class": "col-md-10 col-lg-8 py-5 mx-auto text-lg-center text-left"},
                        ui.h2("Where The Magic Begins"),
                    ),
                    ui.markdown(
                        """    
                        ### Quality Control
                        **Input:** 
                        ```
                    
                        filtered_read_count = filter_low_counts(read_count)
                        
                        print(filtered_read_count.shape)
                        print(filtered_read_count.head())
                        
                        ```
                        **Output:**
                        """
                    ),
                    ui.output_text_verbatim("quality_controled_df_shape"),
                    ui.output_table("quality_controled_df_head"),
                    ui.markdown(
                        """    
                        ### Normalization  
                        
                        **Input:**
                        ```
                        
                        normalized_read_count, case_read_count_cpm, control_read_count_cpm = normalize_rnaseq_data(filtered_read_count, case_samples, control_samples)
                        
                        print(case_read_count_cpm.shape, case_read_count_cpm.head())
                        print(control_read_count_cpm.shape, control_read_count_cpm.head())
                        
                        ```
                        **Output:**
                        """
                    ),
                    ui.output_text_verbatim("case_normalized_shape"),
                    ui.output_table("case_normalized_head"),
                    ui.output_text_verbatim("control_normalized_shape"),
                    ui.output_table("control_normalized_head"),
                    ui.markdown(
                        """    
                        ### Visualization
                        **Input:** 
                        ```
                        
                        visualize(case_read_count_cpm, control_read_count_cpm)
                        
                        ```
                        **Output:** 
                        
                        (It may take a few seconds to render the plot)
                        """
                    ),
                    output_widget("normalized_data_scatterplot"),
                    ui.markdown(
                        """    
                        ### Differential Analysis 
                        **Input:**
                        ```
                       
                        genename_list_short = [str(x).strip() for x in case_read_count_cpm.index]
                        
                        print(len(genename_list_short), genename_list_short[:10])
 
                        ```
                        **Output:**
                        """
                    ),
                    ui.output_text_verbatim("len_gene_list_short"),
                    ui.output_text_verbatim("gene_list_short"),
                    ui.markdown(
                        """    
                        **Input:**
                        ```
                        
                        significant_genes, significant_cases, significant_controls = run_differential_analysis(genename_list_short, case_read_count_cpm, control_read_count_cpm) 
                        
                        print(significant_genes[:10])
                        print(significant_cases.head())
                        print(significant_controls.head())
                        
                        ```
                        **Output:**
                        """
                    ),
                    ui.output_text_verbatim("significant_genes_list"),
                    ui.output_table("significant_cases_head"),
                    ui.output_table("significant_controls_head"),
                    ui.markdown(
                        """    
                        ### Gene Set Enrichment Analysis 
                        **Input:** 
                        ```
                        
                        run_gsea_analysis(significant_genes[0].tolist(), 'pathway_with_pvalues.csv')
                        
                        ```
                        **Output:** 
                        
                        (It may take a few seconds to render the plot)
                        """
                    ),
                    output_widget("gsea_barplot"),
                    ui.output_table("gsea_result_df"),
                ),
                ui.nav("Single Cell"),
                ui.nav("Protein"),
            )
        ),
    ),
    title="Welcome | Genocraft Shiny",

)


def server(input, output, session):
    raw_read_count_file = Path(__file__).parent / "local_data/bulk_RNA/GSE99611_read_count.csv"
    raw_read_count = pd.read_csv(raw_read_count_file, sep=',', dtype={0: str})
    raw_read_count = raw_read_count.dropna()

    id2name_file = Path(__file__).parent / "local_data/bulk_RNA/id_to_name.csv"
    id2name = pd.read_csv(id2name_file, sep=',', encoding='latin-1')
    first_column = id2name.iloc[:, 0]
    last_column = id2name.iloc[:, -3]
    id2name = dict()
    for ii, (gene_id, gene_line) in enumerate(zip(first_column, last_column)):
        try:
            idx1 = gene_line.index('(')
            idx2 = gene_line.index(')')
        except:
            continue
        gene_name = gene_line[idx1 + 1:idx2]
        if (
                any(char.islower() for char in gene_name)
                or len(gene_name) > 7
                or ' ' in gene_name
                or ',' in gene_name
                or '/' in gene_name
                or '-' in gene_name
                or "'" in gene_name
        ):
            continue
        id2name[str(gene_id)] = gene_name
        if ii > 10000:
            break

    read_count = raw_read_count.copy()
    read_count['gene_name'] = read_count['ID_REF'].map(id2name)
    read_count = read_count.dropna(subset=['gene_name'])

    gene_name_list = read_count['gene_name'].tolist()
    read_count = read_count.drop('ID_REF', axis=1)
    read_count = read_count.set_index('gene_name')

    filtered_read_count = bulk_rna_filter_low_counts(read_count)
    
    sample_label_file = Path(__file__).parent / "local_data/bulk_RNA/GSE99611_sample_label.csv"
    with open(sample_label_file, 'r') as fin:
        lines = fin.readlines()
    labels = [int(line.strip().split(',')[1]) for line in lines]
    patient_names = read_count.columns.tolist()
    case_samples = [patient for patient, label in zip(patient_names, labels) if label == 1]
    control_samples = [patient for patient, label in zip(patient_names, labels) if label == 0]

    normalized_read_count, case_read_count_cpm, control_read_count_cpm = bulk_rna_normalize_rnaseq_data(
        filtered_read_count, case_samples, control_samples
    )
    case_x, case_y, control_x, control_y = bulk_rna_get_data_for_visualization(
        case_read_count_cpm, control_read_count_cpm
    )

    normalized_data_scatterplot = go.FigureWidget(
        data=[
            go.Scattergl(
                x=case_x,
                y=case_y,
                mode="markers",
                marker=dict(color="red", size=5),
                name="Case"
            ),
            go.Scattergl(
                x=control_x,
                y=control_y,
                mode="markers",
                marker=dict(color="blue", size=5),
                name="Control"
            ),
        ],
        layout={
            "title": "t-SNE Visualization",
            "xaxis_title": "t-SNE Dimension 1",
            "yaxis_title": "t-SNE Dimension 2",
        }
    )
    register_widget("normalized_data_scatterplot", normalized_data_scatterplot)

    genename_list_short = [str(x).strip() for x in case_read_count_cpm.index]
    significant_genes, significant_cases, significant_controls = bulk_rna_run_differential_analysis(
        genename_list_short, case_read_count_cpm, control_read_count_cpm
    )
    print(significant_cases)

    pathways, p_values_raw, p_values_log10, gsea_result_df = bulk_rna_run_gsea_analysis_helper(
        significant_genes[0].tolist()
    )

    gsea_barplot = go.FigureWidget(
        data=[
            go.Bar(
                x=p_values_log10,
                y=pathways,
                orientation="h"
            ),
        ],
        layout={
            "title": "Pathway Enrichment Analysis",
            "xaxis_title": "-log10(p-value)",
            "yaxis_title": "Pathway",
        }
    )
    register_widget("gsea_barplot", gsea_barplot)

    @output
    @render.text
    def raw_read_count_shape():
        return raw_read_count.shape

    @output
    @render.table(index=True)
    def raw_read_count_head():
        return raw_read_count.head()

    @output
    @render.text
    def read_count_shape():
        return read_count.shape

    @output
    @render.table(index=True)
    def read_count_head():
        return read_count.head()

    @output
    @render.text
    def gene_name_head():
        return gene_name_list[0:10]

    @output
    @render.text
    def gene_name_length():
        return len(gene_name_list)

    @output
    @render.text
    def case():
        return case_samples

    @output
    @render.text
    def control():
        return control_samples

    @output
    @render.text
    def quality_controled_df_shape():
        return filtered_read_count.shape

    @output
    @render.table(index=True)
    def quality_controled_df_head():
        return filtered_read_count.head()
    
    @output
    @render.text
    def case_normalized_shape():
        return case_read_count_cpm.shape

    @output
    @render.table(index=True)
    def case_normalized_head():
        return case_read_count_cpm.head()

    @output
    @render.text
    def control_normalized_shape():
        return control_read_count_cpm.shape

    @output
    @render.table(index=True)
    def control_normalized_head():
        return control_read_count_cpm.head()

    @output
    @render.text
    def len_gene_list_short():
        return len(genename_list_short)

    @output
    @render.text
    def gene_list_short():
        return genename_list_short[:10]

    @output
    @render.table(index=True)
    def significant_cases_head():
        return significant_cases.head()

    @output
    @render.table(index=True)
    def significant_controls_head():
        return significant_controls.head()

    @output
    @render.text
    def significant_genes_list():
        return significant_genes[0].tolist()
    
    @output
    @render.table(index=True)
    def gsea_result_df():
        return gsea_result_df
    
    @reactive.Effect
    def _():
        normalized_data_scatterplot.data[1].visible = input.show_fit()
        gsea_barplot.data[1].visible = input.show_fit()

    @output
    @render.ui
    def file_content():
        file_infos = input.file1()
        if not file_infos:
            return

        df_list = []
        result = ui.TagList()
        for file_info in file_infos:
            with open(file_info["datapath"], "r") as f:
                table = pd.DataFrame(f).head()
                print(table)
                result.append(ui.output_table(table))
        return result


app = App(app_ui, server)
