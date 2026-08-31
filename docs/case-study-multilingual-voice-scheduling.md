# NOVA case study: multilingual voice scheduling

## 1. Problem

NOVA already handled appointment booking, cancellation, rescheduling, and availability through natural-language voice input. The first version of the intent layer was English-centric: it looked for English action words such as `cancel`, `reschedule`, and `available`.

That created a practical usability gap. A caller could speak naturally in Hindi or Hinglish, but the same scheduling request was not reliably mapped to the existing booking workflow. The scheduling engine itself did not need to change; the language understanding and voice-response layer did.

## 2. What I did

I added a multilingual language layer while keeping the existing deterministic scheduling path intact:

- Added Hindi and Hinglish language detection alongside the existing English path.
- Added Hindi/Hinglish intent patterns for booking, cancellation, rescheduling, and availability.
- Kept date and time extraction compatible with the existing ISO date and `HH:MM` format used by the scheduler.
- Added a `language` field to the detected intent so downstream voice responses know which language to use.
- Added language-aware voice responses for English and Hindi.
- Added Hindi `hi-IN` support to the Twilio-compatible `<Gather>` flow and language-aware `<Say>` responses.
- Added explicit language controls to `/voice/start`, `/voice/speech`, and `/voice/twilio`, while still auto-detecting Hindi/Hinglish from the transcript when no language is supplied.
- Added automated tests for Devanagari Hindi, Hinglish, Hindi rescheduling, Hindi availability, Hindi cancellation, language-aware responses, and Hindi Twilio XML.

The core scheduling rules were deliberately left unchanged. The language layer translates different ways of expressing the same scheduling intent into the same internal actions, so booking validation and appointment state changes continue to use the existing deterministic code path.

Twilio's `<Gather>` supports a `language` attribute for speech recognition, including `hi-IN` for Hindi. Reference: https://www.twilio.com/docs/voice/twiml/gather

## 3. What came of it

The improvement turns NOVA's voice interface from an English-only intent surface into a bilingual English + Hindi/Hinglish scheduling interface without rewriting the scheduling core.

The resulting behavior is:

- English request → English intent and response.
- Hindi request → Hindi intent and response.
- Hinglish request → Hindi intent and response.
- Booking, cancellation, rescheduling, and availability continue to use the same scheduling actions underneath.
- The new behavior is covered by deterministic automated tests.

This is an implementation outcome, not a production performance claim. The repository does not yet contain a production call-volume experiment, so no unsupported percentage improvement is claimed.

## Example

**Before:**

> "Mujhe doctor ki appointment book karni hai."

could fall through to the default English intent behavior.

**After:**

> "Mujhe doctor ki appointment book karni hai 2026-09-10 10:00"

is detected as:

- language: `hi`
- action: `book`
- service: `doctor`
- date: `2026-09-10`
- time: `10:00`

The same booking action then continues through NOVA's existing scheduling validation path.
