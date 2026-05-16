from agents.security_agent import SecurityAgent
from agents.regression_agent import RegressionAgent

class Dispatcher:
    def __init__(self):
        self.agents = {
            "security_agent": SecurityAgent(),
            "regression_agent": RegressionAgent()
        }

    def dispatch(self, risk_queue, context):
        """
        Executes the recommended agents for each high-risk item.
        """
        results = []
        for risk in risk_queue:
            agent_name = risk.get("recommended_agent")
            if agent_name in self.agents:
                print(f"[Dispatcher] Routing {risk['module']} ({risk['dimension']}) to {agent_name}")
                agent_result = self.agents[agent_name].run(context)
                results.append({
                    "risk": risk,
                    "evidence": agent_result
                })
            else:
                print(f"[Dispatcher] No active agent for {agent_name} (P1 Stub)")
                results.append({
                    "risk": risk,
                    "evidence": {"summary": "Agent not implemented (P1 Stub)"}
                })
        return results
