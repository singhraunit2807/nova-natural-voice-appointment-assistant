from xml.sax.saxutils import escape

from ai.intent import detect_intent

GREETINGS = {
    "en": "Hello, you are connected to NOVA. How can I help with your appointment?",
    "hi": "Namaste, aap NOVA se connected hain. Main aapki appointment mein kaise madad kar sakta hoon?",
}

MESSAGES = {
    "en": {
        "book": "I can help you book an appointment.",
        "cancel": "I can help you cancel an appointment.",
        "reschedule": "I can help you reschedule an appointment.",
        "availability": "I can check available appointment slots.",
    },
    "hi": {
        "book": "Main aapki appointment book karne mein madad kar sakta hoon.",
        "cancel": "Main aapki appointment cancel karne mein madad kar sakta hoon.",
        "reschedule": "Main aapki appointment ki date ya time badalne mein madad kar sakta hoon.",
        "availability": "Main available appointment slots check kar sakta hoon.",
    },
}

TWILIO_LANGUAGES = {"en": "en-US", "hi": "hi-IN"}


def normalize_language(language: str | None) -> str:
    value = (language or "en").lower().strip()
    if value in {"hi", "hi-in", "hindi"}:
        return "hi"
    return "en"


def start_call_response(language: str = "en") -> dict:
    language = normalize_language(language)
    return {"message": GREETINGS[language], "language": language, "next": "/voice/speech"}


def handle_speech(transcript: str, language: str | None = None) -> dict:
    intent = detect_intent(transcript)
    resolved_language = normalize_language(language or intent.language)
    return {
        "transcript": transcript,
        "intent": intent.__dict__,
        "language": resolved_language,
        "response": MESSAGES[resolved_language][intent.action],
    }


def twilio_greeting(language: str = "en") -> str:
    language = normalize_language(language)
    prompt = escape(GREETINGS[language])
    twilio_language = TWILIO_LANGUAGES[language]
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<Response><Gather input="speech" method="POST" action="/voice/twilio/speech" '
        f'language="{twilio_language}" speechTimeout="auto">'
        f'<Say language="{twilio_language}">{prompt}</Say></Gather>'
        f'<Say language="{twilio_language}">Goodbye.</Say></Response>'
    )


def twilio_speech_response(transcript: str, language: str | None = None) -> str:
    result = handle_speech(transcript, language)
    resolved_language = result["language"]
    twilio_language = TWILIO_LANGUAGES[resolved_language]
    text = escape(result["response"] + " Please provide the date and time if you want to continue.")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<Response><Say language="{twilio_language}">{text}</Say><Hangup/></Response>'
    )
