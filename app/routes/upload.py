from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os
from pydub import AudioSegment
from app.services.separate import separate_audio
from app.services.transcribe import transcribe_vocals_to_midi
from app.services.export_score import midi_to_pdf

router = APIRouter()

INPUT_DIR = "data/input"
os.makedirs(INPUT_DIR, exist_ok=True)


@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...),
    stem: str = Form("bass")
):
    file_path = os.path.join(INPUT_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    base_name = os.path.splitext(file_path)[0]
    wav_path = f"{base_name}.wav"

    audio = AudioSegment.from_file(file_path)
    audio = audio.set_channels(1).set_frame_rate(44100)
    audio.export(wav_path, format="wav")

    stems_info = separate_audio(wav_path)

    stem_map = {
        "vocals": stems_info["vocals_path"],
        "bass": stems_info["bass_path"],
        "other": stems_info["other_path"]
    }

    if stem not in stem_map:
        raise HTTPException(
            status_code=400,
            detail="Invalid stem. Choose one of: vocals, bass, other"
        )

    selected_stem_path = stem_map[stem]

    transcription_info = transcribe_vocals_to_midi(selected_stem_path)
    score_info = midi_to_pdf(transcription_info["midi_path"])

    return {
        "original_file": file.filename,
        "wav_file": wav_path,
        "selected_stem": stem,
        "selected_stem_path": selected_stem_path,
        "stems": stems_info,
        "transcription": transcription_info,
        "score": score_info
    }