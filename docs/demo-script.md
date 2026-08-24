# NOVA — 3–5 Minute Demo Script

## 0:00–0:30 — Introduction

Hello, I’m presenting my project, NOVA, or Natural Voice Appointment Assistant.

NOVA is designed to make appointment scheduling easier through a natural voice interaction. Instead of using a traditional form, a user can explain what they need, and the system identifies the request and sends it through the scheduling logic.

## 0:30–1:15 — What the project does

The main actions are booking, cancellation, rescheduling and checking available slots.

The important part is that the AI or intent layer does not directly change appointment data. The request goes through the backend and scheduling validation first.

## 1:15–2:45 — Live run

I’ll show the actual running API through the FastAPI documentation page.

First, I can send a normal appointment request to the intent endpoint. NOVA identifies the type of request.

Next, I can ask for available slots. The scheduling engine checks the working hours and existing appointments before returning suggestions.

If a requested slot conflicts with an existing appointment, NOVA does not simply accept it. It rejects the conflict and can suggest another available slot.

I can then book an appointment and demonstrate the cancellation or rescheduling flow.

## 2:45–3:30 — Design decision

One design decision I made was to keep appointment-state changes behind deterministic validation. This means the conversational AI can help understand the request, but it does not get direct authority to modify appointment data.

I chose this because scheduling mistakes can directly affect a real user's appointment, so the final action should be checked by predictable backend logic.

## 3:30–4:00 — Limitation

The main limitation of the current version is that the repository is a runnable MVP and is not a fully deployed production phone service. A real phone deployment still needs public HTTPS hosting and real Twilio credentials.

The next planned improvement is multilingual voice interaction, starting with Hindi.

## 4:00–4:20 — Closing

That is NOVA. The project combines voice interaction, intent understanding and deterministic scheduling into one appointment workflow. The repository contains the setup instructions, source code, tests and documentation so another person can reproduce the local version.
