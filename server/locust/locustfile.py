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
            "normalization":True,
            "visualization":True,
            "differential_analysis":True,
            "network_analysis":True,
            "pathway_analysis": True
        })
