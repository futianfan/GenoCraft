# 🦠 Single-Cell Analysis in GenoCraft 📊

Welcome to the `Single-Cell` folder! Here, you will find various scripts to perform comprehensive single-cell RNA-seq (scRNA-seq) analysis. Each script corresponds to a specific step in the single-cell analysis pipeline.

## 📁 File Structure and Descriptions

Here are the main scripts and their functionalities:

- 📄 `normalize.py` : This script loads and normalizes the data. It adjusts raw gene expression measurements to reduce systematic technical differences.

    ```bash
    python -c "from normalize import load_data, normalize_data"
    ```

- 📄 `clustering.py` : This script reduces the dimensionality of the data and performs clustering.

    ```bash
    python -c "from clustering import reduce_dimension, perform_clustering"
    ```

- 📄 `visualization.py` : This script visualizes the clusters.

    ```bash
    python -c "from visualization import plot_clusters"
    ```

- 📄 `differential_expression.py` : This script performs differential expression analysis.

    ```bash
    python -c "from differential_expression import differential_expression"
    ```

- 📄 `GSEA.py` : This script runs Gene Set Enrichment Analysis (GSEA).

    ```bash
    python -c "from GSEA import run_gsea_analysis"
    ```

## 🚀 Usage

First, make sure you've installed all required dependencies using pip:

```bash
pip install -r requirements.txt
