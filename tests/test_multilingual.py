from fastapi.testclient import TestClient

from app import app
from ai.intent import detect_intent, detect_language
from voice.twilio_handler import handle_speech, twilio_greeting

client = TestClient(app)


def test_hindi_and_hinglish_booking_are_detected():
    hindi = detect_intent("मुझे डॉक्टर की appointment 2026-09-10 को 10:00 बजे book करनी है")
    hinglish = detect_intent("mujhe doctor appointment book karni hai 2026-09-10 10:00")

    assert hindi.language == "hi"
    assert hindi.action == "book"
    assert hindi.date == "2026-09-10"
    assert hindi.time == "10:00"

    assert hinglish.language == "hi"
    assert hinglish.action == "book"
    assert hinglish.date == "2026-09-10"
    assert hinglish.time == "10:00"


def test_hindi_reschedule_and_availability_intents():
    assert detect_intent("मुझे अपनी appointment की तारीख बदलनी है").action == "reschedule"
    assert detect_intent("kal kaun sa slot available hai").action == "availability"


def test_hindi_cancel_intent():
    result = detect_intent("मेरी appointment रद्द करनी है")
    assert result.language == "hi"
    assert result.action == "cancel"


def test_voice_response_uses_detected_language():
    result = handle_speech("mujhe doctor ki appointment book karni hai")
    assert result["language"] == "hi"
    assert "appointment" in result["response"]


def test_twilio_hindi_greeting_uses_hindi_locale():
    xml = twilio_greeting("hi")
    assert 'language="hi-IN"' in xml
    assert "NOVA" in xml


def test_language_controls_are_exposed_by_api():
    assert client.get("/").json()["languages"] == ["en", "hi"]
    assert client.post("/voice/start?language=hi").json()["language"] == "hi"
