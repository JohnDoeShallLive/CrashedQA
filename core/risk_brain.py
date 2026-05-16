import os
import json
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

class RiskBrain:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.model = "mistral-small-latest"
        self.client = Mistral(api_key=self.api_key) if self.api_key else None

    def analyze_risk(self, context):
        """
        Calls Mistral to analyze the context and returns a ranked risk queue.
        """
        if not self.client:
            # Fallback if no API key is provided for the demo
            return [
                {
                    "module": "mock_server/app.py",
                    "dimension": "Security",
                    "risk_score": 93,
                    "rationale": "Unvalidated user_id in SQL query; high traffic endpoint.",
                    "recommended_agent": "security_agent"
                },
                {
                    "module": "mock_server/wallet.py",
                    "dimension": "Regression",
                    "risk_score": 85,
                    "rationale": "Legacy code touched; no existing tests; float math used.",
                    "recommended_agent": "regression_agent"
                }
            ]

        prompt = (
            "You are a QA risk analyst. You receive a JSON object describing the engineering "
            "state of a fintech product. Analyse it across 6 dimensions: functional coverage, "
            "security vulnerabilities, performance gaps, accessibility compliance, regression "
            "coverage, and AI model quality. Return ONLY a valid JSON array. Each item must "
            "have: module (string), dimension (string), risk_score (integer 0-100), rationale "
            "(string, max 20 words), recommended_agent (string). Sort by risk_score descending. "
            "No markdown, no explanation, no preamble."
        )

        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": json.dumps(context)}
                ],
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            # Strip markdown fences if present
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
                
            return json.loads(content)
        except Exception as e:
            print(f"RiskBrain Error: {e}")
            # Fallback
            return []

    def compute_deterministic_score(self, risks):
        """
        Computes a final overall risk score based on the formula in the PRD.
        Formula: overall_risk = weighted_avg(all module_risks)
        """
        if not risks:
            return 0
        
        total_score = sum(r["risk_score"] for r in risks)
        return int(total_score / len(risks))

if __name__ == "__main__":
    brain = RiskBrain()
    sample_context = {"dummy": "data"}
    print(json.dumps(brain.analyze_risk(sample_context), indent=2))
