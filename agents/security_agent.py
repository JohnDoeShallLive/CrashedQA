import os
import json
import requests
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

class SecurityAgent:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.client = Mistral(api_key=self.api_key) if self.api_key else None
        self.target_url = "http://localhost:8000/checkout"

    def generate_payloads(self, endpoint_spec):
        """
        Uses Mistral to generate 5 SQLi payloads.
        """
        if not self.client:
            # Fallback payloads
            return [
                "' OR 1=1 --",
                "admin' --",
                "'; DROP TABLE users; --",
                "' UNION SELECT NULL, NULL, NULL --",
                "1' OR '1'='1"
            ]

        prompt = (
            "You are a security testing agent. Given an API endpoint specification, generate "
            "exactly 5 SQL injection test payloads as a JSON array of strings. Target string "
            "parameters. Include: classic comment injection, UNION-based, boolean-based, "
            "time-based, and stacked queries. Return ONLY the JSON array. No explanation."
        )

        try:
            response = self.client.chat.complete(
                model="mistral-small-latest",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": json.dumps(endpoint_spec)}
                ],
                temperature=0.1
            )
            content = response.choices[0].message.content
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
            return json.loads(content)
        except Exception as e:
            print(f"SecurityAgent Error: {e}")
            return ["' OR 1=1 --"]

    def run_tests(self, payloads):
        results = []
        for payload in payloads:
            try:
                # Assuming the endpoint expects {"user_id": "...", "amount": 100}
                response = requests.post(
                    self.target_url,
                    json={"user_id": payload, "amount": 10.0},
                    timeout=5
                )
                
                status = "safe"
                # If we get a 500 error with a database-related message, it's a confirmed vulnerability
                if response.status_code == 500 and "Database error" in response.text:
                    status = "confirmed"
                elif response.status_code == 200:
                    # If it actually succeeds with a payload, it might be even worse
                    status = "suspected (success on payload)"
                
                results.append({
                    "payload": payload,
                    "status_code": response.status_code,
                    "response": response.text[:200],
                    "status": status
                })
            except Exception as e:
                results.append({"payload": payload, "error": str(e), "status": "error"})
        
        return results

    def run(self, context):
        print(f"[SecurityAgent] Starting analysis for {self.target_url}")
        spec = context.get("api_spec", {}).get("paths", {}).get("/checkout", {})
        payloads = self.generate_payloads(spec)
        findings = self.run_tests(payloads)
        
        confirmed = [f for f in findings if f["status"] == "confirmed"]
        
        return {
            "agent": "SecurityAgent",
            "findings": findings,
            "confirmed_vulnerabilities": len(confirmed),
            "summary": f"Found {len(confirmed)} confirmed SQLi vulnerabilities."
        }
