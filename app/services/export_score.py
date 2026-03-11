import os
from music21 import converter

OUTPUT_DIR = "data/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def midi_to_musicxml(midi_path: str) -> dict:
    score = converter.parse(midi_path)

    base_name = os.path.splitext(os.path.basename(midi_path))[0]
    xml_path = os.path.join(OUTPUT_DIR, f"{base_name}.musicxml")

    score.write("musicxml", fp=xml_path)

    return {
        "musicxml_path": xml_path
    }