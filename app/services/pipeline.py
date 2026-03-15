from app.services.preprocess import preprocess_audio
from app.services.separate import separate_audio
from app.services.transcribe import transcribe_audio_to_midi
from app.services.export_score import midi_to_musicxml


def process_audio(audio_path: str, stem: str = "bass") -> dict:
    print("Step 1: Preprocessing audio...")
    wav_path = preprocess_audio(audio_path)
    print(f"Done preprocessing: {wav_path}")

    print("Step 2: Separating stems with Demucs...")
    stems_info = separate_audio(wav_path)
    print("Done separating stems.")

    stem_map = {
        "vocals": stems_info["vocals_path"],
        "drums": stems_info["drums_path"],
        "bass": stems_info["bass_path"],
        "other": stems_info["other_path"],
    }

    if stem not in stem_map:
        raise ValueError("Invalid stem. Choose one of: vocals, drums, bass, other")

    selected_stem_path = stem_map[stem]
    print(f"Selected stem: {selected_stem_path}")

    print("Step 3: Transcribing selected stem to MIDI...")
    transcription_info = transcribe_audio_to_midi(selected_stem_path)
    print("Done transcribing.")

    print("Step 4: Exporting to MusicXML...")
    score_info = midi_to_musicxml(transcription_info["midi_path"])
    print("Done exporting MusicXML.")

    return {
        "wav_file": wav_path,
        "selected_stem": stem,
        "selected_stem_path": selected_stem_path,
        "stems": stems_info,
        "transcription": transcription_info,
        "score": score_info,
    }