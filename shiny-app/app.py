import mimetypes
from math import ceil
from typing import List
from pathlib import Path

import pandas as pd
import shinyswatch
import plotly.graph_objs as go
import re
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, register_widget

import sys
sys.path.append('../')
from bulk_RNA.quality_control import filter_low_counts as bulk_rna_filter_low_counts
from bulk_RNA.Normalize import normalize_rnaseq_data as bulk_rna_normalize_rnaseq_data
from bulk_RNA.Visualize import visualize as bulk_rna_visualize, get_data_for_visualization as bulk_rna_get_data_for_visualization
from bulk_RNA.differential_analysis import run_differential_analysis as bulk_rna_run_differential_analysis
from bulk_RNA.GSEA import run_gsea_analysis_helper as bulk_rna_run_gsea_analysis_helper, run_gsea_analysis as bulk_rna_run_gsea_analysis, save_stream_to_file as bulk_rna_save_stream_to_file

app_ui = ui.page_fluid(
    shinyswatch.theme.spacelab(),

    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_file("file", "File input:"),
            ui.input_text("txt", "Text input:", "general"),
            ui.input_slider("slider", "Slider input:", 1, 100, 30),
            ui.tags.h5("Default actionButton:"),
            ui.input_action_button("action", "Search"),
            ui.tags.h5("actionButton with CSS class:"),
            ui.input_action_button(
                "action2", "Action button", class_="btn-primary"
            ),
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
                        # Title
                        ui.h2("Bulk RNA Workflow"),
                        # input slider
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
                        ### Generate Input Files
                        **How to generate read_counts.csv**
                        
                        **Input:** 
                        ```
                        
                        df = pd.read_csv('GSE99611_read_count.csv', sep = ',', dtype={0: str})
                        df = df.dropna()
                        
                        print(df.shape)
                        df.head()
                        
                        ```
                        **Output:**
                        """
                    ),
                    ui.output_text_verbatim("raw_df_shape"),
                    ui.output_table("raw_df_head"),
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
                        df['gene_name'] = df['ID_REF'].map(id2name)
                        df = df.dropna(subset=['gene_name'])
                        
                        gene_name_list = df['gene_name'].tolist()
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
                    
                    df = df.drop('ID_REF', axis=1)
                    df = df.set_index('gene_name')
                    
                    print(df.shape)
                    df.head()
                    df.to_csv("read_counts.csv")
                    
                    ```
                    **Output:**
                    """
                    ),
                    ui.output_text_verbatim("df_shape"),
                    ui.output_table("df_head"),
                    ui.markdown(
                        """    
                        ### Generate Case and Control 
                        **Input:** 
                        ```
                        
                        with open('GSE99611_sample_label.csv', 'r') as fin:
                            lines = fin.readlines() 
                        labels = [int(line.strip().split(',')[1]) for line in lines]

                        patient_names = df.columns.tolist()

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
                    ui.markdown(
                        """    
                        ### Qaulity Control
                        ```
                    
                        df_filtered = filter_low_counts(df)
                        print(df_filtered.shape)
                        df_filtered.head()
                        
                        ```
                        **Output:**
                        """
                    ),
                    ui.output_text_verbatim("qc_shape"),
                    ui.output_table("qc_head"),
                    ui.markdown(
                        """    
                        ### Normalize   
                        
                        **Input:**
                        ```
                        
                        df_normalized, case_df_cpm, control_df_cpm = normalize_rnaseq_data(df_filtered, case_samples, control_samples)
                        print('normalize', df_normalized.shape)
                        print(case_df_cpm.shape, case_df_cpm.head())
                        print(control_df_cpm.shape, control_df_cpm.head())
                        
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
                        ### Visualize 
                        ```
                        
                        stream = visualize(case_df_cpm, control_df_cpm)
                        
                        ```
                        **(It takes some time to render the plot)**
                        """
                    ),
                    output_widget("scatterplot1"),
                    ui.markdown(
                        """    
                        ### Differential Analysis 
                        **Input:**
                        ```
                       
                        genename_list_short = [str(x).strip() for x in case_df_cpm.index]
                        print(len(genename_list_short), genename_list_short)
 
                        ```
                        **Output:**
                        """
                    ),
                    ui.output_text_verbatim("len_gene_list_short"),
                    ui.output_text_verbatim("gene_list_short"),
                    ui.markdown(
                        """    
                        ```
                        
                        significant_genes, significant_cases, significant_controls = run_differential_analysis(genename_list_short, case_df_cpm, control_df_cpm) 
                        
                        ```
                        """
                    ),
                    ui.markdown(
                        """    
                        ### Gene Set Enrichment Analysis 
                        ```
                        
                        stream = run_gsea_analysis(significant_genes[0].tolist(), 'pathway_with_pvalues.csv')
                        
                        ```
                        """
                    ),
                    output_widget("barplot1"),
                    ui.markdown(
                        """    
                        ```
                        stream
                        ```
                        """
                    ),
                    ui.output_table("gsea_table"),
                ),
                ui.nav("Single Cell"),
                ui.nav("Protein"),
            )
        ),
    ),
    title="Welcome | Genocraft",

)


def server(input, output, session):
    MAX_SIZE = 50000
    infile_df = Path(__file__).parent.parent / "bulk_RNA/GSE99611_read_count.csv"
    raw_df = pd.read_csv(infile_df, sep=',', dtype={0: str})

    infile_gene = Path(__file__).parent.parent / "bulk_RNA/id_to_name.csv"
    id2name = pd.read_csv(infile_gene, sep=',', encoding='latin-1')
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
        if any(char.islower() for char in gene_name) or len(
                gene_name) > 7 or ' ' in gene_name or ',' in gene_name or '/' in gene_name or '-' in gene_name or "'" in gene_name:
            continue
        # print(gene_id, gene_name)
        id2name[str(gene_id)] = gene_name
        if ii > 10000:
            break
    df = raw_df.copy()
    df['gene_name'] = df['ID_REF'].map(id2name)
    df = df.dropna(subset=['gene_name'])

    gene_name_list = df['gene_name'].tolist()
    df = df.drop('ID_REF', axis=1)
    df = df.set_index('gene_name')

    infile_label = Path(__file__).parent.parent / "bulk_RNA/GSE99611_sample_label.csv"
    with open(infile_label, 'r') as fin:
        lines = fin.readlines()
    labels = [int(line.strip().split(',')[1]) for line in lines]
    patient_names = df.columns.tolist()

    case_samples = [patient for patient, label in zip(patient_names, labels) if label == 1]
    control_samples = [patient for patient, label in zip(patient_names, labels) if label == 0]

    df_filtered = bulk_rna_filter_low_counts(df)

    df_normalized, case_df_cpm, control_df_cpm = bulk_rna_normalize_rnaseq_data(df_filtered, case_samples, control_samples)
    case_x, case_y, control_x, control_y = bulk_rna_get_data_for_visualization(case_df_cpm, control_df_cpm)


    scatterplot = go.FigureWidget(
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

    register_widget("scatterplot1", scatterplot)

    genename_list_short = [str(x).strip() for x in case_df_cpm.index]

    significant_genes, significant_cases, significant_controls = \
        bulk_rna_run_differential_analysis(genename_list_short, case_df_cpm, control_df_cpm)

    pathways,  p_values_raw, p_values_log10, gsea_df = bulk_rna_run_gsea_analysis_helper(significant_genes[0].tolist())

    barplot = go.FigureWidget(
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

    register_widget("barplot1", barplot)

    @reactive.Effect
    def _():
        scatterplot.data[1].visible = input.show_fit()
        barplot.data[1].visible = input.show_fit()

    @output
    @render.text
    def len_gene_list_short():
        return len(genename_list_short)

    @output
    @render.text
    def gene_list_short():
        return genename_list_short[:10]

    @output
    @render.text
    def case_normalized_shape():
        return case_df_cpm.shape

    @output
    @render.table(index=True)
    def case_normalized_head():
        return case_df_cpm.head()

    @output
    @render.table(index=True)
    def gsea_table():
        return gsea_df

    @output
    @render.text
    def control_normalized_shape():
        return control_df_cpm.shape

    @output
    @render.table(index=True)
    def control_normalized_head():
        return control_df_cpm.head()

    @output
    @render.text
    def raw_df_shape():
        return raw_df.shape

    @output
    @render.table(index=True)
    def raw_df_head():
        return raw_df.head()

    @output
    @render.text
    def df_shape():
        return df.shape

    @output
    @render.table(index=True)
    def df_head():
        return df.head()

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
    def qc_shape():
        return df_filtered.shape

    @output
    @render.table(index=True)
    def qc_head():
        return df_filtered.head()


    @output
    @render.text
    def file_content():
        file_infos = input.file1()
        if not file_infos:
            return

        # file_infos is a list of dicts; each dict represents one file. Example:
        # [
        #   {
        #     'name': 'data.csv',
        #     'size': 2601,
        #     'type': 'text/csv',
        #     'datapath': '/tmp/fileupload-1wnx_7c2/tmpga4x9mps/0.csv'
        #   }
        # ]
        out_str = ""
        for file_info in file_infos:
            out_str += (
                    "=" * 47
                    + "\n"
                    + file_info["name"]
                    + "\nMIME type: "
                    + str(mimetypes.guess_type(file_info["name"])[0])
            )
            if file_info["size"] > MAX_SIZE:
                out_str += f"\nTruncating at {MAX_SIZE} bytes."

            out_str += "\n" + "=" * 47 + "\n"

            if input.type() == "Text":
                with open(file_info["datapath"], "r") as f:
                    out_str += f.read(MAX_SIZE)
            else:
                with open(file_info["datapath"], "rb") as f:
                    data = f.read(MAX_SIZE)
                    out_str += format_hexdump(data)

        return out_str


def format_hexdump(data: bytes) -> str:
    hex_vals = ["{:02x}".format(b) for b in data]
    hex_vals = group_into_blocks(hex_vals, 16)
    hex_vals = [" ".join(row) for row in hex_vals]
    hex_vals = "\n".join(hex_vals)
    return hex_vals


def group_into_blocks(x: List[str], blocksize: int):
    """
    Given a list, return a list of lists, where the inner lists each have `blocksize`
    elements.
    """
    return [
        x[i * blocksize: (i + 1) * blocksize] for i in range(ceil(len(x) / blocksize))
    ]




app = App(app_ui, server)
