import subprocess
import os

STEMS_DIR = "data/stems"
os.makedirs(STEMS_DIR, exist_ok=True)

def separate_audio(input_wav: str):
    command = [
        "demucs",
        "-o",
        STEMS_DIR,
        input_wav
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(
            f"Demucs failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )

    file_name = os.path.splitext(os.path.basename(input_wav))[0]
    model_dir = os.path.join(STEMS_DIR, "htdemucs", file_name)

    return {
        "stems_dir": model_dir,
        "vocals_path": os.path.join(model_dir, "vocals.wav"),
        "drums_path": os.path.join(model_dir, "drums.wav"),
        "bass_path": os.path.join(model_dir, "bass.wav"),
        "other_path": os.path.join(model_dir, "other.wav")
    }