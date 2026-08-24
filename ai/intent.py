from dataclasses import dataclass
import re


@dataclass
class AppointmentIntent:
    action: str
    service: str | None = None
    date: str | None = None
    time: str | None = None


def detect_intent(text: str) -> AppointmentIntent:
    value = text.lower().strip()
    if any(word in value for word in ["cancel", "cancellation", "remove my appointment"]):
        action = "cancel"
    elif any(word in value for word in ["reschedule", "change my appointment", "move my appointment"]):
        action = "reschedule"
    elif any(word in value for word in ["available", "availability", "free slot", "what times"]):
        action = "availability"
    else:
        action = "book"

    service = next((x for x in ["doctor", "dentist", "salon", "service", "consultation", "appointment"] if x in value), None)
    date_match = re.search(r"\b(20\d{2}-\d{2}-\d{2})\b", value)
    time_match = re.search(r"\b([01]?\d|2[0-3]):[0-5]\d\b", value)
    return AppointmentIntent(action, service, date_match.group(1) if date_match else None, time_match.group(0) if time_match else None)
