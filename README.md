# NOVA — Natural Voice Appointment Assistant

NOVA is a voice-first appointment scheduling assistant. The system is designed so a caller can express an appointment request naturally while the backend validates the action before changing appointment data.

## Features

- Booking, cancellation and rescheduling
- Availability and alternative slot suggestions
- Deterministic conflict checking
- FastAPI REST API
- SQLite persistence for local development
- Intent detection with a deterministic fallback
- Optional Llama 4 Scout adapter through Groq
- Twilio-compatible voice/TwiML webhook flow
- Optional faster-whisper STT adapter
- Optional local TTS adapter
- Automated tests and GitHub Actions CI

## Architecture

```text
Caller
  ↓
Twilio / Voice Adapter
  ↓
Speech-to-Text
  ↓
Intent / Llama 4 Scout
  ↓
FastAPI Action Layer
  ↓
Scheduling + Validation
  ↓
SQLite / production DB adapter
  ↓
Voice Response
  ↓
Caller
```

The important design choice is that the AI/intent layer does not directly modify appointment state. Booking, cancellation and rescheduling pass through deterministic validation first.

## Run locally

From the repository root:

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000/docs` for Swagger API documentation.

## API

- `GET /` — health check
- `POST /intent` — detect appointment intent
- `POST /suggest-slots` — return available slots
- `POST /appointments` — book an appointment
- `GET /appointments` — list active appointments
- `POST /appointments/{id}/cancel` — cancel
- `POST /appointments/{id}/reschedule` — reschedule
- `POST /voice/twilio` — Twilio voice webhook
- `POST /voice/twilio/speech` — speech callback

## Demo video

https://youtube.com/watch?v=LVLwIuHN0OE&t=32&feature=shared

## Project evaluation notes

The documented project evaluation used 15 functional scenarios covering booking, cancellation, rescheduling, invalid slots, ambiguity, urgency, silence handling and escalation. Reported project-level results: 81% interaction accuracy, 0.86 precision, 0.79 recall and 0.82 F1-score. These are project evaluation figures, not production benchmarks.

## Transparency

This repository is a reconstructed, runnable MVP/reference implementation based on the documented NOVA project specification because the original private source repository was not available. It is not presented as a copy of a private original codebase.

## Security

Do not commit real API keys, passwords, tokens or customer data. Use environment variables and `.env` locally.
