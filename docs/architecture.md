# NOVA Architecture

```text
Caller
  ↓
Twilio / Voice Adapter
  ↓
Speech-to-Text
  ↓
Intent / Llama 4 Scout Adapter
  ↓
FastAPI Action Layer
  ↓
Scheduling + Deterministic Validation
  ↓
SQLite Local Persistence
  ↓
Voice Response
  ↓
Caller
```

The core scheduling action is deliberately separated from the language model. The AI can interpret a request, but appointment state is changed only after deterministic validation.

## Production mapping

The local SQLite layer can be replaced with Supabase/PostgreSQL. The local voice adapters can be replaced with hosted Whisper and Orpheus or another TTS provider. Groq/Llama 4 Scout is optional and requires a real API key.
