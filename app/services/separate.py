import subprocess
import os
import shutil

STEMS_DIR = "data/stems"
os.makedirs(STEMS_DIR, exist_ok=True)


def separate_audio(input_wav: str):
    demucs_path = shutil.which("demucs")
    if not demucs_path:
        raise RuntimeError("Demucs executable not found. Install demucs in the active environment.")

    command = [
        demucs_path,
        "-o", STEMS_DIR,
        input_wav
    ]

    print("Running Demucs:", " ".join(command))

    result = subprocess.run(command)

    if result.returncode != 0:
        raise RuntimeError(f"Demucs failed with return code {result.returncode}")

    file_name = os.path.splitext(os.path.basename(input_wav))[0]
    model_dir = os.path.join(STEMS_DIR, "htdemucs", file_name)

    return {
        "stems_dir": model_dir,
        "vocals_path": os.path.join(model_dir, "vocals.wav"),
        "drums_path": os.path.join(model_dir, "drums.wav"),
        "bass_path": os.path.join(model_dir, "bass.wav"),
        "other_path": os.path.join(model_dir, "other.wav"),
    }