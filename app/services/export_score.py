import os
from pathlib import Path
from music21 import converter

OUTPUT_DIR = "data/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def midi_to_musicxml(midi_path: str) -> dict:
    score = converter.parse(midi_path)

    midi_path_obj = Path(midi_path)
    job_id = midi_path_obj.parent.name
    base_name = midi_path_obj.stem

    job_output_dir = Path(OUTPUT_DIR) / job_id
    job_output_dir.mkdir(parents=True, exist_ok=True)

    xml_path = str(job_output_dir / f"{base_name}.musicxml")

    score.write("musicxml", fp=xml_path)

    return {
        "musicxml_path": xml_path
    }