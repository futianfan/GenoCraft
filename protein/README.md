# 🧬 Protein Analysis in GenoCraft 📊

Welcome to the `Protein` folder! In this directory, you'll find various scripts to carry out comprehensive protein analysis. Each script corresponds to a specific step in the protein analysis pipeline.

## 📁 File Structure and Descriptions

Here are the main scripts and their functionalities:

- 📄 `quality_control.py` : This script is for Quality Control (QC). It ensures the protein data is accurate, consistent, and reliable.

- 📄 `impute.py` : This script is for missing data imputation. It uses advanced statistical methods to estimate and fill in missing protein data.

    ```bash
    python impute.py
    ```

- 📄 `Normalize.py` : This script is for normalization. It adjusts raw protein expression measurements to reduce systematic technical differences.

- 📄 `Visualize.py` : This script is for visualization. You can use this to create intuitive and informative plots of your protein data.

    ```bash
    python Visualize.py
    ```

- 📄 `differential_analysis.py` : This script is for differential analysis. It identifies proteins with statistically significant changes in expression levels between different conditions.

    ```bash
    python differential_analysis.py
    ```

- 📄 `network_analysis.py` : This script is for network analysis. It constructs and analyzes protein networks to identify key proteins and pathways.

- 📄 `GSEA.py` : This script is for Pathway Analysis. It identifies biological pathways associated with differentially expressed proteins.

## 🚀 Usage

Make sure you've installed all required dependencies using pip:

```bash
pip install -r requirements.txt


