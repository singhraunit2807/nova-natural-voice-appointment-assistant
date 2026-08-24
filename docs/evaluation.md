# NOVA Evaluation Notes

The project documentation reports 15 functional scenarios covering booking, cancellation, rescheduling, invalid slots, ambiguity, urgency, silence handling and escalation.

Reported project-level results:

| Metric | Result |
|---|---:|
| Interaction accuracy | 81% |
| Precision | 0.86 |
| Recall | 0.79 |
| F1-score | 0.82 |
| Booking F1 | 0.86 |
| Cancellation F1 | 0.80 |
| Rescheduling F1 | 0.83 |

These figures are documented project evaluation results, not production benchmarks.

## Known limitations

- Production cloud services require real credentials.
- The local reference implementation uses SQLite.
- The documented voice interaction is English-first.
- Full-duplex real-time conversation is not implemented in the local MVP.
- Persistent cross-call memory is not implemented.
