from dataclasses import dataclass
import re


@dataclass
class AppointmentIntent:
    action: str
    service: str | None = None
    date: str | None = None
    time: str | None = None
    language: str = "en"


def detect_language(text: str) -> str:
    """Detect the small supported language set used by the voice MVP.

    Hindi is detected from Devanagari text or common Hindi/Hinglish scheduling
    words. Everything else falls back to English so the existing flow remains
    backward compatible.
    """
    value = text.lower().strip()
    if re.search(r"[\u0900-\u097f]", value):
        return "hi"

    hindi_markers = [
        "mujhe", "mera", "meri", "mere", "chahiye", "karna", "karni",
        "hai", "hain", "kal", "aaj", "samay", "waqt", "baje", "slot",
        "book kar", "booking kar", "cancel kar", "radd", "badalna",
        "dobara", "reschedule kar", "kab", "doctor se", "appointment lena",
    ]
    return "hi" if any(marker in value for marker in hindi_markers) else "en"


def _first_match(value: str, words: list[str]) -> bool:
    return any(word in value for word in words)


def detect_intent(text: str) -> AppointmentIntent:
    value = text.lower().strip()
    language = detect_language(value)

    if _first_match(value, [
        "cancel", "cancellation", "remove my appointment",
        "cancel kar", "cancel karna", "radd", "रद्द", "रद्द करना",
        "appointment hata", "appointment cancel",
    ]):
        action = "cancel"
    elif _first_match(value, [
        "reschedule", "change my appointment", "move my appointment",
        "reschedule kar", "badalna", "badal do", "date badal", "समय बदल",
        "तारीख बदल", "appointment badal",
    ]):
        action = "reschedule"
    elif _first_match(value, [
        "available", "availability", "free slot", "what times",
        "available hai", "kaunsa slot", "konsa slot", "slot bata",
        "kab available", "खाली स्लॉट", "उपलब्ध", "कौन सा समय",
    ]):
        action = "availability"
    else:
        action = "book"

    service = next((x for x in [
        "doctor", "dentist", "salon", "service", "consultation", "appointment",
        "doktor", "daktar", "doctor se", "dentist", "clinic", "क्लिनिक",
        "डॉक्टर", "डेंटिस्ट", "सलून",
    ] if x in value), None)

    date_match = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", value)
    time_match = re.search(r"\b([01]?\d|2[0-3]):[0-5]\d\b", value)
    return AppointmentIntent(
        action,
        service,
        date_match.group(1) if date_match else None,
        time_match.group(0) if time_match else None,
        language,
    )
