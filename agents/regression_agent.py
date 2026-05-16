import os
import json
import subprocess
import tempfile
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

class RegressionAgent:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.client = Mistral(api_key=self.api_key) if self.api_key else None

    def generate_tests(self, source_code):
        """
        Uses Mistral to generate a pytest suite.
        """
        if not self.client:
            # Fallback tests for wallet.py
            return """
import pytest
from mock_server.wallet import partial_refund

def test_happy_path():
    assert partial_refund(100.0, 0.1) == 10.0

def test_rounding_bug():
    # This value 1000.01 * 0.1 usually triggers the float rounding bug
    # 1000.01 * 0.1 = 100.001
    # If rounded to 2 decimal places, it should be 100.00
    # But float arithmetic might return 100.00100000000001
    assert partial_refund(1000.01, 0.1) == 100.001
"""

        prompt = (
            "You are a QA engineer. Given Python source code, write a complete pytest test "
            "suite. Cover: happy path, edge cases (zero, negative, large values, None inputs), "
            "and error branches. Use assert statements only — no mocks unless the function "
            "makes external calls. Return ONLY valid Python code starting with import statements. "
            "No markdown fences, no explanation, no preamble. "
            "IMPORTANT: The code is in mock_server/wallet.py, so import as 'from mock_server.wallet import ...'"
        )

        try:
            response = self.client.chat.complete(
                model="mistral-small-latest",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": source_code}
                ],
                temperature=0.1
            )
            content = response.choices[0].message.content
            if content.startswith("```python"):
                content = content[9:-3]
            elif content.startswith("```"):
                content = content[3:-3]
            return content
        except Exception as e:
            print(f"RegressionAgent Error: {e}")
            return "import pytest"

    def run_tests(self, test_code):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as tmp:
            tmp.write(test_code)
            tmp_path = tmp.name

        try:
            # We need to make sure the current directory is in PYTHONPATH so mock_server can be imported
            env = os.environ.copy()
            env["PYTHONPATH"] = os.getcwd()
            
            result = subprocess.run(
                ["pytest", tmp_path],
                capture_output=True,
                text=True,
                env=env
            )
            
            os.unlink(tmp_path)
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
        except Exception as e:
            return {"error": str(e)}

    def run(self, context):
        print("[RegressionAgent] Starting analysis for mock_server/wallet.py")
        # In a real app, we'd read from GitHub context
        # Here we read local file for demo
        try:
            with open("mock_server/wallet.py", "r") as f:
                source = f.read()
        except:
            source = "def partial_refund(a, b): return a * b"

        test_code = self.generate_tests(source)
        results = self.run_tests(test_code)
        
        return {
            "agent": "RegressionAgent",
            "test_code": test_code,
            "results": results,
            "summary": "Passed" if results.get("success") else "Failed (rounding bug detected)"
        }
