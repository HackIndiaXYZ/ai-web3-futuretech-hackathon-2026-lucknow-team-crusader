# Crisis Room — Farm Operations AI Dashboard 🚜🧠

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB.svg?logo=react&logoColor=black)](https://vitejs.dev)
[![Gemini](https://img.shields.io/badge/AI-Google%20Gemini%20Flash%20Lite-8E75B2.svg?logo=google&logoColor=white)](https://ai.google.dev)

> Real-time multi-agent AI dashboard automating agricultural crisis management through low-latency vision-language triage, localized resource planning, and government scheme matchmaking.

---

## 📌 Overview

**Crisis Room** processes live field imagery and environmental data to diagnose crop anomalies, prescribe localized treatments, and match farmers with relevant government relief schemes.

The system uses a Vision–Language Model (VLM) pipeline streamed over WebSockets, allowing human operators to observe a team of 5 specialized AI agents collaborating on a solution in real time.

---

## ✨ Key Features

* **Multi-Agent AI Chain:** Sequential pipeline of 5 specialized agents that break down complex agricultural incidents into actionable outputs.
* **Vision–Language Integration:** Field photos are compressed and encoded with Pillow and analyzed alongside sensor data to maximize visual insight while minimizing token overhead.
* **Live WebSocket Streaming:** React frontend maintains a persistent connection to the FastAPI backend, rendering agents' intermediate states dynamically.
* **Live Session Analytics:** Tracks active streams, engaged agent nodes, pipeline latency (seconds), and total processed events in real time.
* **Intelligent Quota Management:** Drops heavy image payloads after the initial vision triage; non-crisis detections bypass heavy downstream LLM calls.
* **SMS/WhatsApp-Ready Advisories:** Generates concise, human-readable advisories formatted for rapid field dissemination.

---

## 🏗 System Architecture

![System Architecture](assets/architecture-diagram.png)

```mermaid
flowchart TD
    A([Trigger: Field Photo / Sensor Alert]) --> B[FastAPI Ingestion & Auth]
    B --> C[Pillow: Sanitize & Optimize Image]
    C --> D[VLM: Field Monitor - gemini-flash-lite]
    D --> E{Issue Detected?}
    E -- No Issue / Normal --> Z1[Log Status & Update Dashboard]
    E -- Low Confidence --> Z2[Request Retake via SMS]
    E -- Verified Issue --> F[Agronomist Agent: Diagnosis & Loss %]
    F --> G[Resource Agent: Treatment & Inventory]
    F --> H[Scheme Agent: PMFBY / PMKSY Match]
    G --> I[Farmer Advisory Agent: Action Plan]
    H --> I
    I --> J{Requires Human Review?}
    J -- High Risk --> K[Operator UI Review Queue]
    K -->|Approved| L[Notification Dispatch: SMS/WhatsApp]
    J -- Standard --> L
    L --> M[(Session Logs & DB)]
    M --> N[Optional: State Hash Attestation]

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
