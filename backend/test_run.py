# backend/test_run.py
from events import INCIDENTS
from state import get_initial_state
from agents import process_crisis_event

def test_pipeline():
    sample_event = INCIDENTS[0]  # Pyrilla in Sugarcane
    state = get_initial_state(sample_event)
    
    print(f"--- Running Crisis Room Chain for Event: {sample_event['event_id']} ---")
    for agent_name, message, updated_state in process_crisis_event(state, sample_event):
        print(f"\n[{agent_name}]:\n{message}")
        print("-" * 50)

if __name__ == "__main__":
    test_pipeline()