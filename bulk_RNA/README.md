# 🧬 Bulk RNA Analysis in GenoCraft 📊

Welcome to the `bulk_RNA` folder! Here, you will find a set of functionalities that will assist you in performing comprehensive analysis on bulk RNA data. Each script has a specific role in the analysis pipeline.

## 📁 File Structure and Descriptions

Here are the main scripts and their functionalities:

- 📄 `quality_control.py` : A script for quality control (QC). It removes a subset of rows to ensure data quality.

- 📄 `Normalize.py` : A script for normalization. It adjusts raw gene expression measurements for systematic technical differences.

- 📄 `Visualize.py` : A script for data visualization. Use this to generate intuitive from the data.

    ```bash
    python Visualize.py
    ```

- 📄 `differential_analysis.py` : A script for performing differential analysis. It identifies genes with statistically significant changes in expression levels between different conditions.

    ```bash
    python differential_analysis.py
    ```

- 📄 `DDN.py` : A script for network analysis. It constructs and analyzes gene networks to identify key genes and pathways. You can choose to skip this step if it is too time-consuming for your requirements.

- 📄 `GSEA.py` : A script for pathway analysis. It identifies biological pathways associated with differentially expressed genes.

Each script performs an important step in the bulk RNA data analysis pipeline. Refer to the comments in each script for more detailed instructions and information.

## 🚀 Usage

Remember to first install all required dependencies using pip:

```bash
pip install -r requirements.txt
