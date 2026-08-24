def transcribe_audio(audio_path: str, model_size: str = "base") -> str:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("Install faster-whisper to use local transcription.") from exc

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_path)
    return " ".join(segment.text.strip() for segment in segments).strip()
