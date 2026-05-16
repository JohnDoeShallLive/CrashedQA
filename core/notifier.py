import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class Notifier:
    def __init__(self):
        self.slack_webhook = os.getenv("SLACK_WEBHOOK")
        self.jira_url = os.getenv("JIRA_URL")
        self.jira_email = os.getenv("JIRA_EMAIL")
        self.jira_token = os.getenv("JIRA_API_TOKEN")

    def notify_slack(self, verdict):
        """
        Sends the release verdict to Slack.
        """
        if not self.slack_webhook:
            print("[Notifier] Slack Webhook not configured. Skipping Slack notification.")
            return

        payload = {
            "text": f"🚀 *CrashedQA Release Verdict: {verdict['recommendation']}*\n"
                    f"Initial Risk: {verdict['initial_risk_score']} | Final Risk: {verdict['final_risk_score']}\n"
                    f"*Findings:*\n"
        }
        
        for f in verdict["findings"]:
            icon = "🔴" if f["status"] == "confirmed" else "🟢"
            payload["text"] += f"{icon} {f['module']} ({f['dimension']}): {f['summary']}\n"

        try:
            requests.post(self.slack_webhook, json=payload)
            print("[Notifier] Slack notification sent.")
        except Exception as e:
            print(f"[Notifier] Slack Error: {e}")

    def file_jira_bug(self, summary, description):
        """
        Files a bug in JIRA.
        """
        if not all([self.jira_url, self.jira_email, self.jira_token]):
            print("[Notifier] JIRA not configured. Skipping bug filing.")
            return

        url = f"{self.jira_url}/rest/api/3/issue"
        auth = (self.jira_email, self.jira_token)
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "fields": {
                "project": {"key": "QA"}, # Assuming project key is QA
                "summary": f"[CrashedQA] {summary}",
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": description}]
                        }
                    ]
                },
                "issuetype": {"name": "Bug"}
            }
        }

        try:
            response = requests.post(url, json=payload, auth=auth, headers=headers)
            if response.status_code == 201:
                print(f"[Notifier] JIRA bug filed: {summary}")
            else:
                print(f"[Notifier] JIRA Error: {response.status_code} {response.text}")
        except Exception as e:
            print(f"[Notifier] JIRA Exception: {e}")

    def process_verdict(self, verdict):
        self.notify_slack(verdict)
        for f in verdict["findings"]:
            if f["status"] == "confirmed":
                self.file_jira_bug(
                    f"Critical Finding in {f['module']}",
                    f"Dimension: {f['dimension']}\nSummary: {f['summary']}"
                )
