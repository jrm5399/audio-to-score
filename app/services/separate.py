import subprocess
import os
import shutil
from pathlib import Path

STEMS_DIR = "data/stems"
os.makedirs(STEMS_DIR, exist_ok=True)


def separate_audio(input_wav: str):
    demucs_path = shutil.which("demucs")
    if not demucs_path:
        raise RuntimeError("Demucs executable not found. Install demucs in the active environment.")

    input_path = Path(input_wav)
    job_id = input_path.parent.name

    job_stems_dir = os.path.join(STEMS_DIR, job_id)

    command = [
        demucs_path,
        "-o", job_stems_dir,
        input_wav
    ]

    print("Running Demucs:", " ".join(command))

    result = subprocess.run(command)
    if result.returncode != 0:
        raise RuntimeError(f"Demucs failed with return code {result.returncode}")

    file_name = input_path.stem
    model_dir = os.path.join(job_stems_dir, "htdemucs", file_name)

    return {
        "stems_dir": model_dir,
        "vocals_path": os.path.join(model_dir, "vocals.wav"),
        "drums_path": os.path.join(model_dir, "drums.wav"),
        "bass_path": os.path.join(model_dir, "bass.wav"),
        "other_path": os.path.join(model_dir, "other.wav"),
    }