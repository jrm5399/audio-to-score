from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from urllib.parse import quote

from app.services.ingest import save_uploaded_file, download_youtube_audio
from app.services.pipeline import process_audio

router = APIRouter()

OUTPUT_DIR = Path("data/output").resolve()
STEMS_DIR = Path("data/stems").resolve()
ALLOWED_EXTENSIONS = {".mid", ".musicxml", ".xml", ".wav"}


def build_download_url(file_path: str) -> str:
    return f"/download?file={quote(file_path)}"


def add_stem_downloads(stems: dict) -> dict:
    return {
        "vocals": {"download": build_download_url(stems["vocals_path"])},
        "drums": {"download": build_download_url(stems["drums_path"])},
        "bass": {"download": build_download_url(stems["bass_path"])},
        "other": {"download": build_download_url(stems["other_path"])},
    }


@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...),
    stem: str = Form("bass")
):
    try:
        ingest_result = save_uploaded_file(file)
        print("UPLOAD INGEST RESULT:", ingest_result)
        result = process_audio(
            audio_path=ingest_result["audio_path"],
            stem=stem
        )

        transcription = result["transcription"]
        score = result["score"]
        stems = add_stem_downloads(result["stems"])

        return {
            **ingest_result,
            "wav_file": result["wav_file"],
            "selected_stem": result["selected_stem"],
            "selected_stem_path": result["selected_stem_path"],
            "stems": stems,
            "transcription": {
                **transcription,
                "midi_download": build_download_url(transcription["midi_path"])
            },
            "score": {
                **score,
                "musicxml_download": build_download_url(score["musicxml_path"])
            }
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/youtube")
async def process_youtube(
    url: str = Form(...),
    stem: str = Form("bass")
):
    try:
        ingest_result = download_youtube_audio(url)
        print("YOUTUBE INGEST RESULT:", ingest_result)
        result = process_audio(
            audio_path=ingest_result["audio_path"],
            stem=stem
        )

        transcription = result["transcription"]
        score = result["score"]
        stems = add_stem_downloads(result["stems"])

        return {
            **ingest_result,
            "wav_file": result["wav_file"],
            "selected_stem": result["selected_stem"],
            "selected_stem_path": result["selected_stem_path"],
            "stems": stems,
            "transcription": {
                **transcription,
                "midi_download": build_download_url(transcription["midi_path"])
            },
            "score": {
                **score,
                "musicxml_download": build_download_url(score["musicxml_path"])
            }
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download")
async def download_file(file: str):
    requested_path = Path(file).resolve()
    allowed_roots = [OUTPUT_DIR, STEMS_DIR]

    if not any(root == requested_path or root in requested_path.parents for root in allowed_roots):
        raise HTTPException(status_code=400, detail="Invalid file path")

    if requested_path.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    if not requested_path.exists() or not requested_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=str(requested_path),
        filename=requested_path.name
    )