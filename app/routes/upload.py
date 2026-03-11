from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.ingest import save_uploaded_file, download_youtube_audio
from app.services.pipeline import process_audio

router = APIRouter()


@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...),
    stem: str = Form("bass")
):
    try:
        ingest_result = save_uploaded_file(file)
        result = process_audio(ingest_result["audio_path"], stem)

        return {
            **ingest_result,
            **result
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
        result = process_audio(ingest_result["audio_path"], stem)

        return {
            **ingest_result,
            **result
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))