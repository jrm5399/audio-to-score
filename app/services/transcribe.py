import os
import librosa
import numpy as np
import pretty_midi

OUTPUT_DIR = "data/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def hz_to_midi_note(hz: float) -> int:
    return int(round(librosa.hz_to_midi(hz)))


def smooth_midi_sequence(midi_seq, window_size=5):
    smoothed = []
    half = window_size // 2

    for i in range(len(midi_seq)):
        if midi_seq[i] is None:
            smoothed.append(None)
            continue

        window = [
            midi_seq[j]
            for j in range(max(0, i - half), min(len(midi_seq), i + half + 1))
            if midi_seq[j] is not None
        ]

        if window:
            smoothed.append(int(round(np.median(window))))
        else:
            smoothed.append(None)

    return smoothed


def transcribe_audio_to_midi(audio_path: str):
    y, sr = librosa.load(audio_path, sr=44100, mono=True)

    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C7")
    )

    times = librosa.times_like(f0, sr=sr)

    midi_pitches = []
    for pitch in f0:
        if pitch is not None and not np.isnan(pitch):
            midi_pitches.append(hz_to_midi_note(pitch))
        else:
            midi_pitches.append(None)

    midi_pitches = smooth_midi_sequence(midi_pitches, window_size=7)

    notes = []
    current_note = None
    note_start = None

    for i, midi_note in enumerate(midi_pitches):
        t = times[i]

        if midi_note is not None:
            if current_note is None:
                current_note = midi_note
                note_start = t
            elif midi_note != current_note:
                notes.append((current_note, note_start, t))
                current_note = midi_note
                note_start = t
        else:
            if current_note is not None:
                notes.append((current_note, note_start, t))
                current_note = None
                note_start = None

    if current_note is not None and note_start is not None:
        notes.append((current_note, note_start, times[-1]))

    merged_notes = []
    for note in notes:
        pitch, start, end = note
        if merged_notes and merged_notes[-1][0] == pitch and abs(merged_notes[-1][2] - start) < 0.05:
            merged_notes[-1] = (pitch, merged_notes[-1][1], end)
        else:
            merged_notes.append(note)

    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)

    kept_count = 0
    for pitch, start, end in merged_notes:
        duration = end - start
        if duration >= 0.15:
            note = pretty_midi.Note(
                velocity=100,
                pitch=int(pitch),
                start=float(start),
                end=float(end)
            )
            instrument.notes.append(note)
            kept_count += 1

    midi.instruments.append(instrument)

    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    midi_path = os.path.join(OUTPUT_DIR, f"{base_name}.mid")
    midi.write(midi_path)

    return {
        "midi_path": midi_path,
        "note_count": kept_count
    }