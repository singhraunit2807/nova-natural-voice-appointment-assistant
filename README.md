# NOVA — Natural Voice Appointment Assistant

NOVA is a voice-first appointment scheduling assistant. The goal is simple: a caller should be able to explain an appointment request naturally, while the system validates the request before changing appointment data.

## What NOVA does

- Books appointments
- Cancels appointments
- Reschedules appointments
- Checks availability and suggests alternative slots
- Detects common appointment intents from natural-language text
- Supports English, Hindi, and Hinglish scheduling requests
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
Language + Intent Detection
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

The multilingual improvement follows the same boundary: English, Hindi, and Hinglish requests are mapped to the same internal actions before the deterministic scheduling layer runs.

## Multilingual voice scheduling — v2.1

The voice interface now supports English plus Hindi/Hinglish scheduling requests.

### Supported behavior

- Detects Hindi written in Devanagari.
- Detects common Hindi/Hinglish phrases such as `mujhe`, `karna hai`, `slot`, `cancel kar`, and `badalna`.
- Detects booking, cancellation, rescheduling, and availability intents in Hindi/Hinglish.
- Preserves the existing date (`YYYY-MM-DD`) and time (`HH:MM`) extraction used by the scheduler.
- Returns a `language` field with the detected intent.
- Produces language-aware voice responses.
- Supports `hi-IN` in the Twilio-compatible `<Gather>` flow when Hindi is selected.

### API examples

Hindi intent detection:

```bash
curl -X POST http://127.0.0.1:8000/intent \\
  -H "Content-Type: application/json" \\
  -d '{"text":"मुझे डॉक्टर की appointment 2026-09-10 को 10:00 बजे book करनी है"}'
```

Language-aware voice start:

```text
POST /voice/start?language=hi
```

Language-aware speech handling:

```text
POST /voice/speech?text=mujhe%20doctor%20ki%20appointment%20book%20karni%20hai
```

The detailed three-beat case study is in `docs/case-study-multilingual-voice-scheduling.md`.

Twilio `<Gather>` language reference: https://www.twilio.com/docs/voice/twiml/gather

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
- `POST /voice/start` — start the voice flow; accepts `language=en` or `language=hi`
- `POST /voice/speech` — handle a transcript; language can be supplied or detected
- `POST /voice/twilio` — start the Twilio-compatible voice flow; accepts `language=en` or `language=hi`
- `POST /voice/twilio/speech` — receive the speech callback

## Evaluation and v2 results

The current repository includes automated tests for intent detection, scheduling conflicts, slot suggestions, API behavior, and the multilingual voice improvement. The project evaluation documentation also records a 15-scenario evaluation covering booking, cancellation, rescheduling, invalid slots, ambiguity, urgency, silence handling and escalation.

The documented project-level evaluation figures are **81% interaction accuracy, 0.86 precision, 0.79 recall and 0.82 F1-score**. These figures are project evaluation results, not production benchmarks.

The v2 multilingual improvement was implemented as a focused language-layer change rather than a rewrite of the scheduling core. No production percentage improvement is claimed because the repository does not yet contain a production call-volume experiment.

## Current limitation

The local repository is a runnable MVP rather than a fully deployed production phone service. A real phone deployment still requires public HTTPS hosting and real Twilio credentials. The external production services are kept behind adapters so they can be connected without rewriting the scheduling core.

The multilingual layer currently covers English, Hindi, and Hinglish. Additional languages can be added by extending the language/intent dictionaries and voice locale mapping without changing the scheduling engine.

## Demo video

**YouTube:** https://youtube.com/watch?v=LVLwIuHN0OE&t=32&feature=shared

The video demonstrates the project and explains how NOVA works, including its design choice and limitation.

## AI transparency

AI was used as a development partner for parts of the project, including planning, implementation support and documentation. The generated work was reviewed and structured into the runnable repository. The repository is a reconstructed MVP/reference implementation based on the documented NOVA project specification because the original private source repository was not available; it is not presented as a copy of a private original codebase.

## Security

Never commit real API keys, passwords, tokens or customer data. Use environment variables and keep local secrets in `.env`.
