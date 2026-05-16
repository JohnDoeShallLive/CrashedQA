import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

class IngestionEngine:
    def __init__(self):
        self.jira_url = os.getenv("JIRA_URL")
        self.jira_email = os.getenv("JIRA_EMAIL")
        self.jira_token = os.getenv("JIRA_API_TOKEN")
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.swagger_path = "swagger.json"

    def get_jira_context(self):
        """
        Reads JIRA sprint stories. Mocked if no credentials.
        """
        if not all([self.jira_url, self.jira_email, self.jira_token]):
            # Mock data for demo if JIRA not configured
            return [
                {
                    "id": "QA-101",
                    "title": "Implement partial refund logic in wallet module",
                    "description": "Calculates partial refunds based on percentage. Needs to be precise.",
                    "acceptance_criteria": ["Rounding must follow financial standards", "No precision loss"]
                },
                {
                    "id": "QA-102",
                    "title": "Checkout endpoint for mobile users",
                    "description": "Expose POST /checkout for mobile app to process payments.",
                    "acceptance_criteria": ["Validates user_id", "Deducts balance", "Returns 200 on success"]
                }
            ]
        
        # Real JIRA API call logic would go here
        # Example: requests.get(f"{self.jira_url}/rest/api/3/search?jql=sprint in openSprints()", auth=(self.jira_email, self.jira_token))
        return []

    def get_github_context(self):
        """
        Reads GitHub diffs or file content. Mocked for demo.
        """
        # In a real scenario, we'd use self.github_token to fetch PR diffs
        # For the demo, we point to our local mock_server/wallet.py
        return {
            "touched_files": ["mock_server/wallet.py", "mock_server/app.py"],
            "diffs": {
                "mock_server/wallet.py": "def partial_refund(amount: float, percentage: float) -> float:\n    refund = amount * percentage\n    return refund"
            }
        }

    def get_swagger_context(self):
        """
        Reads the local swagger.json file.
        """
        try:
            with open(self.swagger_path, "r") as f:
                return json.load(f)
        except Exception as e:
            return {"error": str(e)}

    def gather_full_context(self):
        """
        Merges all context into a unified JSON object.
        """
        context = {
            "jira_stories": self.get_jira_context(),
            "github_data": self.get_github_context(),
            "api_spec": self.get_swagger_context()
        }
        return context

if __name__ == "__main__":
    engine = IngestionEngine()
    print(json.dumps(engine.gather_full_context(), indent=2))
