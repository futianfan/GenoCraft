import mimetypes
from math import ceil
from typing import List
from pathlib import Path

import pandas as pd
import re
import shinyswatch
from shiny import App, render, ui

import sys
sys.path.append('../')
from bulk_RNA.quality_control import filter_low_counts as bulk_rna_filter_low_counts
from bulk_RNA.Normalize import normalize_rnaseq_data as bulk_rna_normalize_rnaseq_data
from bulk_RNA.Visualize import visualize as bulk_rna_visualize
from bulk_RNA.differential_analysis import run_differential_analysis as bulk_rna_run_differential_analysis
from bulk_RNA.GSEA import run_gsea_analysis as bulk_rna_run_gsea_analysis, save_stream_to_file as bulk_rna_save_stream_to_file

app_ui = ui.page_fluid(
    shinyswatch.theme.sandstone(),

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
                        ui.h1("Bulk RNA Workflow"),
                        # input slider
                    ),
                    ui.markdown(
                        """    
                        ### Import Libraries
                        ```
                        
                        import pandas as pd 
                        import re 
                        
                        from bulk_RNA.quality_control import filter_low_counts 
                        from bulk_RNA.Normalize import normalize_rnaseq_data 
                        from bulk_RNA.Visualize import visualize  
                        from bulk_RNA.differential_analysis import run_differential_analysis
                        from bulk_RNA.GSEA import run_gsea_analysis, save_stream_to_file 
                        
                        ```
                        """
                    ),
                    ui.markdown(
                        """    
                        ### Generate Input Files
                        **How to generate read_counts.csv from GSE99611_read_count.csv**
                        ```
                        
                        df = pd.read_csv('GSE99611_read_count.csv', sep = ',', dtype={0: str})
                        df = df.dropna()
                        
                        print(df.shape)
                        df.head()
                        
                        ```
                        """
                    ),
                    ui.output_text("raw_df_shape"),
                    ui.output_table("raw_df_head"),
                    ui.markdown(
                        """    
                        **convert ID_REF to gene name**
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
                        
                        df = df.drop('ID_REF', axis=1)
                        df = df.set_index('gene_name')
                        
                        print(df.shape)
                        df.head()
                        df.to_csv("read_counts.csv")
                        
                        ```
                        """
                    ),
                    ui.output_text("gene_name_length"),
                    ui.output_text("gene_name_head"),
                    ui.output_text("df_shape"),
                    ui.output_table("df_head"),
                    ui.markdown(
                        """    
                        ### Generate Case and Control 
                        ```
                        
                        with open('GSE99611_sample_label.csv', 'r') as fin:
                            lines = fin.readlines() 
                        labels = [int(line.strip().split(',')[1]) for line in lines]

                        patient_names = df.columns.tolist()

                        case_samples = [patient for patient,label in zip(patient_names, labels) if label==1]
                        control_samples = [patient for patient,label in zip(patient_names, labels) if label==0]
                        print(case_samples)
                        print(control_samples)
                        ```
                        """
                    ),
                    ui.markdown(
                        """    
                        ```
                        pd.DataFrame(case_samples).to_csv("case_label.txt",  header=None, index=None, sep=' ')
                        pd.DataFrame(control_samples).to_csv("control_label.txt",  header=None, index=None, sep=' ')
                        ```
                        """
                    ),
                    ui.markdown(
                        """    
                        ### Qaulity Control
                        ```
                    
                        df_filtered = filter_low_counts(df)
                        print(df_filtered.shape)
                        df_filtered.head()
                        ```
                        """
                    ),
                    ui.markdown(
                        """    
                        ### Normalize   
                        ```
                        
                        df_normalized, case_df_cpm, control_df_cpm = normalize_rnaseq_data(df_filtered, case_samples, control_samples)
                        print('normalize', df_normalized.shape)
                        print(case_df_cpm.shape, case_df_cpm.head())
                        print(control_df_cpm.shape, control_df_cpm.head())
                        
                        ```
                        """
                    ),
                    ui.markdown(
                        """    
                        ### Visualize 
                        ```
                        
                        stream = visualize(case_df_cpm, control_df_cpm)
                        
                        ```
                        """
                    ),
                    ui.markdown(
                        """    
                        ### Differential Analysis 
                        ```
                       
                        genename_list_short = [str(x).strip() for x in case_df_cpm.index]
                        print(len(genename_list_short), genename_list_short)

                        significant_genes, significant_cases, significant_controls = \
                                run_differential_analysis(genename_list_short, case_df_cpm, control_df_cpm) 
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
                    ui.markdown(
                        """    
                        ```
                        stream
                        ```
                        """
                    ),
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
    infile = Path(__file__).parent.parent / "bulk_RNA/GSE99611_read_count.csv"
    raw_df = pd.read_csv(infile, sep=',', dtype={0: str})

    infile = Path(__file__).parent.parent / "bulk_RNA/id_to_name.csv"
    id2name = pd.read_csv(infile, sep=',', encoding='latin-1')
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
        print(gene_id, gene_name)
        id2name[str(gene_id)] = gene_name
        if ii > 10000:
            break
    df = raw_df.copy()
    df['gene_name'] = df['ID_REF'].map(id2name)
    df = df.dropna(subset=['gene_name'])

    gene_name_list = df['gene_name'].tolist()
    print(len(gene_name_list))
    df = df.drop('ID_REF', axis=1)
    df = df.set_index('gene_name')
    print(df.shape)
    df.head()

    @output
    @render.text
    def raw_df_shape():
        return raw_df.shape

    @output
    @render.table
    def raw_df_head():
        return raw_df.head()

    @output
    @render.text
    def df_shape():
        return df.shape

    @output
    @render.table
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
