from locust import HttpUser, task


class GenoCraftUser(HttpUser):
    @task
    def get_time(self):
        self.client.get("api/time")

    @task
    def protein_workflow(self):
        self.client.post("api/analyze/protein", json={
            "uploadOwnFile": False,
            "number_of_files": 0,
            "quality_control": True,
            "imputation": True,
            "normalization": True,
            "visualization": True,
            "differential_analysis": True,
            "network_analysis": False,
            "pathway_analysis": True
        })

    @task
    def bulk_rna_workflow(self):
        self.client.post("api/analyze/bulk", json={
            "upload_own_file": False,
            "quality_control": True,
            "normalization": True,
            "visualization_after_normalization": True,
            "differential_analysis": True,
            "network_analysis": False,
            "gene_set_enrichment_analysis": True,
            "visualization": True,
            "number_of_files": 0
        })

    @task
    def single_cell_workflow(self):
        self.client.post("api/analyze/single-cell", json={
            "upload_own_file": False,
            "normalization": True,
            "clustering": True,
            "visualization": True,
            "differential_analysis": True,
            "network_analysis": False,
            "pathway_analysis": True,
            "number_of_files": 0,
        })
