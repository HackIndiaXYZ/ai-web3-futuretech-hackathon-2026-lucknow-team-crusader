import base64
import json
import asyncio
from datetime import datetime, timezone
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from state import get_initial_state
from agents import process_crisis_event
from events import INCIDENTS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Crisis Room API is running"}


@app.post("/classify-image")
async def classify_image(file: UploadFile = File(...)):
    """Converts image to Base64 to be sent directly to the VLM."""
    image_bytes = await file.read()
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    return {"base64_image": encoded_image}


def build_custom_event(payload: dict) -> dict:
    """Formats live injected data to match scripted incidents."""
    return {
        "event_id": f"LIVE-{datetime.now(timezone.utc).strftime('%H%M%S')}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "location": payload.get("location") or "Live-injected event",
        "crop_type": payload.get("crop_type") or "Unspecified",
        "sensor_data": {},
        "visual_flags": payload.get("description", ""),
        "suspected_issue": payload.get("description", ""),
        "base64_image": payload.get("base64_image")
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            if payload.get("mode") == "custom" or payload.get("description") or payload.get("base64_image"):
                target_event = build_custom_event(payload)
            else:
                event_id = payload.get("event_id", "EVT-001")
                target_event = next(
                    (e for e in INCIDENTS if e["event_id"] == event_id), INCIDENTS[0]
                )

            state = get_initial_state(target_event)
            await websocket.send_json({"type": "start", "event": target_event})

            for agent_name, message, updated_state in process_crisis_event(state, target_event):
                await websocket.send_json({
                    "type": "agent_update",
                    "agent": agent_name,
                    "message": message,
                    "state": updated_state
                })
                await asyncio.sleep(1.2)

            await websocket.send_json({"type": "complete"})

    except WebSocketDisconnect:
        print("Frontend client disconnected")