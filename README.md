# NOVA — Natural Voice Appointment Assistant

NOVA is a voice-first appointment scheduling assistant. The goal is simple: a caller should be able to explain an appointment request naturally, while the system validates the request before changing appointment data.

## What NOVA does

- Books appointments
- Cancels appointments
- Reschedules appointments
- Checks availability and suggests alternative slots
- Detects common appointment intents from natural-language text
- Stores local appointment data in SQLite
- Exposes a FastAPI backend with interactive API documentation
- Provides a Twilio-compatible voice/TwiML flow
- Includes optional speech-to-text and text-to-speech adapters
- Includes an optional Llama 4 Scout adapter through Groq

## Who it is for

NOVA is intended for small businesses and service-based teams that handle appointments, such as clinics, salons, consultation services and similar appointment-driven workflows.

## Setup

A stranger should be able to reproduce the local setup from this README alone.

### Requirements

- Python 3.10+
- Git

### Install

From the repository root:

```bash
python -m venv .venv

# Windows
.venv\\Scripts\\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Run

```bash
uvicorn app:app --reload
```

Then open:

`http://127.0.0.1:8000/docs`

The Swagger page can be used to test the API without any extra frontend application.

## Simple architecture

```text
Caller
  ↓
Twilio / Voice Adapter
  ↓
Speech-to-Text
  ↓
Intent Detection / Llama 4 Scout
  ↓
FastAPI Action Layer
  ↓
Scheduling + Conflict Validation
  ↓
SQLite (local MVP)
  ↓
Voice / API Response
  ↓
Caller
```

### Important design decision

The AI/intent layer does **not** directly modify appointment state. Booking, cancellation and rescheduling go through deterministic scheduling and validation logic first. This makes the system easier to test and reduces the chance of an AI response changing appointment data incorrectly.

## API examples

### Check the service

`GET /`

### Detect an intent

`POST /intent`

```json
{"text":"I want to reschedule my doctor appointment"}
```

### Find available slots

`POST /suggest-slots`

```json
{
  "name":"Demo User",
  "service":"doctor",
  "preferred_date":"2026-09-01",
  "preferred_time":"10:00",
  "duration_minutes":30
}
```

### Book an appointment

`POST /appointments`

```json
{
  "name":"Demo User",
  "service":"doctor",
  "start":"2026-09-01T10:00:00",
  "duration_minutes":30
}
```

### Other actions

- `GET /appointments` — list active appointments
- `POST /appointments/{id}/cancel` — cancel an appointment
- `POST /appointments/{id}/reschedule` — reschedule an appointment
- `POST /voice/twilio` — start the Twilio-compatible voice flow
- `POST /voice/twilio/speech` — receive the speech callback

## Evaluation and v2 results

The current repository includes automated tests for intent detection, scheduling conflicts, slot suggestions and API behavior. The project evaluation documentation also records a 15-scenario evaluation covering booking, cancellation, rescheduling, invalid slots, ambiguity, urgency, silence handling and escalation.

The documented project-level evaluation figures are **81% interaction accuracy, 0.86 precision, 0.79 recall and 0.82 F1-score**. These figures are project evaluation results, not production benchmarks.

For the next iteration, the planned v2 improvement is **multilingual voice appointment assistance**, starting with Hindi. The goal is to test whether users can make the same appointment requests naturally in Hindi and whether the existing scheduling validation continues to behave correctly.

## Current limitation

The local repository is a runnable MVP rather than a fully deployed production phone service. A real phone deployment still requires public HTTPS hosting and real Twilio credentials. The external production services are kept behind adapters so they can be connected without rewriting the scheduling core.

## Demo video

**YouTube:** https://youtube.com/watch?v=LVLwIuHN0OE&t=32&feature=shared

The video demonstrates the project and explains how NOVA works, including its design choice and limitation.

## AI transparency

AI was used as a development partner for parts of the project, including planning, implementation support and documentation. The generated work was reviewed and structured into the runnable repository. The repository is a reconstructed MVP/reference implementation based on the documented NOVA project specification because the original private source repository was not available; it is not presented as a copy of a private original codebase.

## Security

Never commit real API keys, passwords, tokens or customer data. Use environment variables and keep local secrets in `.env`.
