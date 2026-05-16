import time
import json
from core.ingestion import IngestionEngine
from core.risk_brain import RiskBrain
from core.dispatcher import Dispatcher
from core.compiler import EvidenceCompiler
from core.notifier import Notifier

def main():
    print("==========================================")
    print("   CrashedQA: Risk-Weighted Orchestrator  ")
    print("==========================================")
    
    # 1. Ingestion
    print(f"[{time.strftime('%H:%M:%S')}] [L0] Ingesting engineering context...")
    ingestor = IngestionEngine()
    context = ingestor.gather_full_context()
    
    # 2. Risk Brain
    print(f"[{time.strftime('%H:%M:%S')}] [L1] Analyzing risk across 6 dimensions...")
    brain = RiskBrain()
    risk_queue = brain.analyze_risk(context)
    
    print("\n[Risk Brain Output]")
    for r in risk_queue:
        print(f" - {r['module']} ({r['dimension']}): {r['risk_score']}/100 - {r['rationale']}")
    
    # 3. Dispatcher
    print(f"\n[{time.strftime('%H:%M:%S')}] [L2] Dispatching specialist sub-agents...")
    dispatcher = Dispatcher()
    dispatcher_results = dispatcher.dispatch(risk_queue, context)
    
    # 4. Evidence Compiler
    print(f"\n[{time.strftime('%H:%M:%S')}] [L3] Compiling evidence and release verdict...")
    compiler = EvidenceCompiler()
    verdict = compiler.compile(risk_queue, dispatcher_results)
    
    print("\n[Release Verdict]")
    print(f" Initial Risk Score: {verdict['initial_risk_score']}")
    print(f" Final Risk Score:   {verdict['final_risk_score']}")
    print(f" Recommendation:     {verdict['recommendation']}")
    
    # 5. Notifier
    print(f"\n[{time.strftime('%H:%M:%S')}] [L4] Sending notifications and filing bugs...")
    notifier = Notifier()
    notifier.process_verdict(verdict)
    
    print("\n==========================================")
    print("            Pipeline Complete             ")
    print("==========================================")

if __name__ == "__main__":
    main()
