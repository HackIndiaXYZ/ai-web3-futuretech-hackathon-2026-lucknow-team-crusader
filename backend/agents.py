import json
from llm_client import call_llm
from scheme_data import scheme_matrix
from prompts import (
    FIELD_MONITOR_PROMPT,
    AGRONOMIST_PROMPT,
    RESOURCE_PROMPT,
    SCHEME_PROMPT,
    ADVISORY_PROMPT
)

def run_agent(role_name: str, role_prompt: str, shared_state: dict, event: dict, pass_image: bool = False) -> tuple[dict, str]:
    """Runs a single agent step with clean, lightweight context."""
    
    # Create a copy of event WITHOUT the heavy base64 string to keep text tokens under 500
    clean_event = {k: v for k, v in event.items() if k != "base64_image"}
    
    user_msg = f"""Current Farm State:
{json.dumps(shared_state, indent=2)}

Incident Event Context:
{json.dumps(clean_event, indent=2)}"""

    image_data = event.get("base64_image") if pass_image else None
    
    parsed = call_llm(role_prompt, user_msg, image_data)
    
    analysis = parsed.get("analysis", "")
    updates = parsed.get("state_updates", {})

    shared_state.update(updates)
    shared_state["timeline"].append({
        "agent": role_name,
        "message": analysis
    })

    return shared_state, analysis


def run_scheme_agent(shared_state: dict, event: dict) -> tuple[dict, str]:
    """Deterministic scheme matching combined with LLM phrasing."""
    matched = []

    if shared_state.get("estimated_loss_percent", 0) >= 20:
        if scheme_matrix.get("PMFBY"):
            matched.append({"scheme": "PMFBY", "data": scheme_matrix.get("PMFBY")})

    soil_moisture = event.get("sensor_data", {}).get("soil_moisture_percent", 100)
    suspected_issue = event.get("suspected_issue", "").lower()
    diagnosis = str(shared_state.get("diagnosis", "")).lower()

    if soil_moisture < 30 or "irrigation" in suspected_issue or "irrigation" in diagnosis:
        if scheme_matrix.get("PMKSY"):
            matched.append({"scheme": "PMKSY", "data": scheme_matrix.get("PMKSY")})

    severity = str(shared_state.get("anomaly_severity", "")).lower()
    has_crisis = (len(matched) > 0) or ("high" in severity) or ("medium" in severity) or (shared_state.get("estimated_loss_percent", 0) > 0)

    if has_crisis:
        for scheme_id, data in scheme_matrix.items():
            if data.get("category") == "standing reference":
                matched.append({"scheme": scheme_id, "data": data})

    shared_state["matched_schemes"] = matched

    if not has_crisis:
        msg = "Crop conditions optimal. No emergency financial schemes required."
        shared_state["timeline"].append({
            "agent": "Scheme Agent",
            "message": msg
        })
        return shared_state, msg

    clean_event = {k: v for k, v in event.items() if k != "base64_image"}
    user_msg = f"Current Farm State:\n{json.dumps(shared_state, indent=2)}\n\nVerified Scheme Matches:\n{json.dumps(matched, indent=2)}"
    
    parsed = call_llm(SCHEME_PROMPT, user_msg)
    analysis = parsed.get("analysis", "")

    shared_state["timeline"].append({
        "agent": "Scheme Agent",
        "message": analysis
    })

    return shared_state, analysis


def process_crisis_event(shared_state: dict, event: dict):
    """Generator pipeline streaming agents cleanly."""
    # Only Field Monitor gets pass_image=True
    shared_state, msg = run_agent("Field Monitor", FIELD_MONITOR_PROMPT, shared_state, event, pass_image=True)
    yield "Field Monitor", msg, shared_state

    shared_state, msg = run_agent("Agronomist", AGRONOMIST_PROMPT, shared_state, event, pass_image=False)
    yield "Agronomist", msg, shared_state

    shared_state, msg = run_agent("Resource Agent", RESOURCE_PROMPT, shared_state, event, pass_image=False)
    yield "Resource Agent", msg, shared_state

    shared_state, msg = run_scheme_agent(shared_state, event)
    yield "Scheme Agent", msg, shared_state

    shared_state, msg = run_agent("Farmer Advisory", ADVISORY_PROMPT, shared_state, event, pass_image=False)
    shared_state["farmer_advisory"] = msg 
    yield "Farmer Advisory", msg, shared_state