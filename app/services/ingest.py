import os
import re
import shutil
import yt_dlp
from fastapi import UploadFile

INPUT_DIR = "data/input"
os.makedirs(INPUT_DIR, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    name, ext = os.path.splitext(filename)
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")
    safe_ext = re.sub(r"[^A-Za-z0-9.]+", "", ext)

    if not safe_name:
        safe_name = "audio_input"

    return f"{safe_name}{safe_ext}"

ALLOWED_UPLOAD_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac"}
def save_uploaded_file(file: UploadFile) -> dict:
    safe_filename = sanitize_filename(file.filename or "uploaded_audio.mp3")
    ext = os.path.splitext(safe_filename)[1].lower()

    if ext not in ALLOWED_UPLOAD_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")

    file_path = os.path.join(INPUT_DIR, safe_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return {
        "audio_path": file_path,
        "source_type": "upload",
        "original_name": file.filename,
        "saved_name": safe_filename,
    }


def download_youtube_audio(url: str) -> dict:
    node_path = shutil.which("node")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(INPUT_DIR, "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "noplaylist": True,
        "quiet": False,
        "noprogress": True,
        "verbose": True,
    }

    if node_path:
        ydl_opts["js_runtimes"] = {
            "node": {
                "path": node_path
            }
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        original_filename = ydl.prepare_filename(info)

    mp3_path = os.path.splitext(original_filename)[0] + ".mp3"
    safe_filename = sanitize_filename(os.path.basename(mp3_path))
    safe_path = os.path.join(INPUT_DIR, safe_filename)

    if mp3_path != safe_path and os.path.exists(mp3_path):
        os.replace(mp3_path, safe_path)

    return {
        "audio_path": safe_path,
        "source_type": "youtube",
        "original_name": info.get("title"),
        "saved_name": safe_filename,
        "source_url": url,
    }