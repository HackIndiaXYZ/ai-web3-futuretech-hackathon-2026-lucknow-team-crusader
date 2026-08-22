# Crisis Room — Farm Operations AI Dashboard 🚜🧠

[![Status](https://img.shields.io/badge/status-Prototype-yellowgreen)]() [![License: MIT](https://img.shields.io/badge/license-MIT-blue)]()

---

## Live KPI Grid (Realtime Monitoring)
We do not use mocked historical data. The KPI grid at the top of the dashboard tracks the AI architecture's live performance for the active session: it monitors active WebSocket data streams, counts exactly how many independent AI agent nodes have engaged the problem, measures the total pipeline execution latency in seconds, and tallies the total events processed while the session is active.

This is a session-level, real-time view (not an aggregated historical dashboard). Connect the grid to your monitoring or state channel for production usage.

---

## Overview
Crisis Room is a real-time, multi-agent AI dashboard built to automate agricultural crisis management. It processes live environmental data and field imagery to diagnose crop anomalies, prescribe localized treatments, and match farmers with relevant government relief schemes.

The system uses a Vision–Language Model (VLM) pipeline streamed over WebSockets, allowing human operators to observe a team of specialized AI agents collaborating on a solution in real time.

---

## Key Features
- Multi-Agent AI Chain: sequential pipeline of 5 specialized agents that break down complex agricultural incidents into actionable outputs.
- Vision–Language Integration: field photos are compressed and encoded with Pillow and analyzed alongside sensor data to provide visual and contextual insight without unnecessary token usage.
- Live WebSocket Streaming: React frontend maintains a persistent connection to the FastAPI backend and renders agents' intermediate states dynamically.
- Live Session Analytics: session-level KPIs (active streams, agent node count, pipeline latency, events processed) shown in the top KPI grid.
- Intelligent Quota Management: image payloads are dropped after the initial vision step and healthy crops bypass LLM calls to conserve API quota and reduce latency.
- SMS/WhatsApp-ready advisories: concise, human-readable advisories produced by the Farmer Advisory agent for rapid dissemination.

---

## Agent Chain — Roles & Responsibilities
When a field incident is triggered (either live or scripted), data flows through the following agents:

1. **Field Monitor (VLM)**
   - Inputs: compressed images (Pillow), textual sensor data
   - Output: visual + sensor summary and initial indicators (pest, discoloration, abiotic stress)

2. **Agronomist**
   - Inputs: Field Monitor summary
   - Output: diagnosis, likely causes, and estimated crop loss (%)

3. **Resource Agent**
   - Inputs: Agronomist diagnosis
   - Output: immediate operational actions (treatments, irrigation adjustments, safety notes)

4. **Scheme Agent**
   - Inputs: severity and loss estimate
   - Function: deterministic + LLM ruleset to match the crisis to government schemes (e.g., PMFBY, PMKSY, KCC). The agent halts the pipeline if there is no crisis, conserving resources.

5. **Farmer Advisory**
   - Inputs: Resource Agent + Scheme Agent outputs
   - Output: concise, actionable advisory formatted for SMS/WhatsApp and local-language distribution
---

## System Architecture
- Frontend: React + Vite + Tailwind — live dashboard and operator UI
- Backend: FastAPI + Uvicorn — WebSocket endpoints, orchestration, and agent runners
- AI Integration: Google Gemini API (`gemini-flash-lite-latest`) used as the VLM/LLM backend
- Image Processing: Pillow (PIL) for compression / encoding before transmission
- Communication: WebSockets for streaming agent events; optional task queue for long-running tasks
- Persistence: session logs and minimal metadata (on-disk or DB); keep PII off-chain
- Optional: blockchain attestations for non-identifying hashes and timestamps


---

## Tech Stack
| Layer | Technology |
|---|---|
| Frontend | React, Vite, Tailwind CSS (v3) |
| Backend | FastAPI, Uvicorn, WebSockets (Python) |
| AI / VLM | Google Gemini API (`gemini-flash-lite-latest`) |
| Image Processing | Pillow (PIL) |
| Delivery | SMS / WhatsApp Gateway (integration point) |
| Monitoring | Live KPI grid (WebSocket-powered session metrics) |

---

## How the Live KPI Grid Works (session-level)
- Active WebSocket streams: number of clients/streams currently connected and sending events
- Agent nodes engaged: exact count of distinct AI agent processes that participated during the session
- Pipeline latency (seconds): total time from first ingestion (image/text) to final advisory output
- Events processed: running total of events emitted by agents for the active session

This grid is intentionally real-time and per-session — it does not present aggregated historical metrics.

---

## Local Setup — Quick Start

### 1) Backend — environment
Create a `.env` file inside the `/backend` directory with your Gemini API key:

```env
# backend/.env
GEMINI_API_KEY=your_gemini_api_key_here
# optional: SMS_GATEWAY_API_KEY=your_sms_gateway_key
```

### 2) Backend — install & run
```bash
cd backend
pip install fastapi uvicorn requests pillow python-dotenv websockets python-multipart
uvicorn main:app --reload
```
Default: http://localhost:8000 — WebSocket endpoint: ws://localhost:8000/ws

### 3) Frontend — install & run
```bash
cd frontend
npm install
npm run dev
```
Default: http://localhost:5173

---

## Usage (Operator workflow)
1. Operator or field device uploads an image and sensor package.
2. Frontend opens/maintains a WebSocket session to the backend.
3. Agents stream intermediate "thoughts" and state updates to the UI in real time.
4. Operator watches the Crisis Room: diagnosis, recommended actions, scheme matches, and final advisory.
5. Operator dispatches advisory (SMS/WhatsApp) or downloads the checklist for the farmer.

---

## Example User Journey
- A field camera detects yellowing patches. The image data are streamed.
- VLM identifies irregular spots; Agronomist diagnoses probable fungal infection and estimates 20% loss.
- Resource Agent recommends localized fungicide and a temporary irrigation schedule.
- Scheme Agent matches the severity to PMFBY guidelines and suggests claim steps.
- Farmer Advisory formats a short message and the operator sends it via SMS.

---

## Screenshots & Demo
Add screenshots or GIFs in `/frontend/public/assets` or `/assets` and reference them here:

- Onboarding / Upload: `./assets/screenshot-upload.svg`
- Crisis Room live stream: `./assets/screenshot-dashboard.svg`
- Final advisory (SMS): `./assets/screenshot-advisory.svg`

---

## Judging Highlights
- Observable multi-agent collaboration with live traceability of agent outputs
- Quota- and cost-aware design that minimizes LLM calls for healthy crops
- Practicality: rapid, explainable advisories mapped to government relief schemes
- UX: Crisis Room enables judges and operators to observe the full diagnostic pipeline in real time

---

## Security & Privacy
- Images and PII remain off-chain; optional attestations only record non-identifying hashes and timestamps.
- Store API keys in environment variables or a secret manager; rotate keys regularly.
- Minimize personal data retention — store only session metadata and anonymized logs for audits.

---

## Limitations & Future Work
- System performance relies on the quality and coverage of scheme metadata; continuous curation required.
- Offline / low-bandwidth support and mobile-first offline synchronization are planned improvements.
- Expand VLM capabilities, add OCR for forms, and integrate multilingual voice intake.

---

## 👥 Contributors

* **Abdul Hannan** — Project Lead & Full-Stack Architect (Frontend + Backend)
* **Swaleha Khatoon** — Research & Ideation Lead
* **Mahmood Rahman** — UI/UX Design & Presentation Lead

---

## Acknowledgements

This project was developed as part of the **AI and Web3 Hackathon Grand Finale**. 

We extend our sincere gratitude to:
* **Hackathon Mentors & Organizers** — for their guidance, technical feedback, and continuous support throughout the event.
* **Farming Communities** — whose real-world challenges, insights, and resilience inspired the problem statement and practical design of this solution.
* **Open-Source Community** — for providing the robust foundational frameworks and libraries that powered this build.
---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---
