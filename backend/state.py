# backend/state.py

def get_initial_state(event_data: dict) -> dict:
    """Creates a clean initial state from an incoming incident event."""
    return {
        "event_id": event_data.get("event_id"),
        "timestamp": event_data.get("timestamp"),
        "location": event_data.get("location"),
        "crop_type": event_data.get("crop_type"),
        "sensor_data": event_data.get("sensor_data", {}),
        "visual_flags": event_data.get("visual_flags", ""),
        # Cumulative state filled by agents
        "anomaly_severity": None,
        "diagnosis": None,
        "recommended_action": None,
        "estimated_loss_percent": 0,
        "matched_schemes": [],
        "farmer_advisory": None,   # <-- added: gives the frontend one clean field to read
        "timeline": []
    }