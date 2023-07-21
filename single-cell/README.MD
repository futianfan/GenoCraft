# 🦠 Single-Cell Analysis in GenoCraft 📊

Welcome to the `Single-Cell` folder! Here, you will find various scripts to perform comprehensive single-cell RNA-seq (scRNA-seq) analysis. Each script corresponds to a specific step in the single-cell analysis pipeline.

## 📁 File Structure and Descriptions

Here are the main scripts and their functionalities:

- 📄 `normalize.py` : This script contains functions to load and normalize the data. 

    - `load_data(file)`: Reads the file located at the given path and returns a pandas DataFrame containing the data.
    - `normalize_data(data)`: Takes a pandas DataFrame as input and returns a normalized DataFrame. Normalization adjusts raw gene expression measurements to reduce systematic technical differences.

    ```bash
    python -c "from normalize import load_data, normalize_data"
    ```

- 📄 `clustering.py` : This script contains functions for dimensionality reduction and clustering. 

    - `reduce_dimension(data)`: Applies t-SNE dimensionality reduction to the input data and returns the 2D t-SNE representation.
    - `perform_clustering(data)`: Takes the 2D t-SNE representation as input and returns the identified clusters.

    ```bash
    python -c "from clustering import reduce_dimension, perform_clustering"
    ```

- 📄 `visualization.py` : This script contains functions for visualizing clusters. 

    - `plot_clusters(data, labels)`: Takes the 2D t-SNE representation and cluster labels as input and creates a scatter plot of the data with different clusters color-coded.

    ```bash
    python -c "from visualization import plot_clusters"
    ```

- 📄 `differential_expression.py` : This script contains functions for differential expression analysis. 

    - `differential_expression(data, labels)`: Takes the normalized data and cluster labels as input and returns the results of differential expression analysis.

    ```bash
    python -c "from differential_expression import differential_expression"
    ```

- 📄 `GSEA.py` : This script contains functions for Gene Set Enrichment Analysis (GSEA). 

    - `run_gsea_analysis(gene_list_file, output_file)`: Takes a file with a list of significant genes and an output file path. It runs GSEA and writes the results to the output file.

    ```bash
    python -c "from GSEA import run_gsea_analysis"
    ```

## 🚀 Usage

First, make sure you've installed all required dependencies using pip:

```bash
pip install -r requirements.txt
