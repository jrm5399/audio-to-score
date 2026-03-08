import os
import subprocess
from music21 import converter

OUTPUT_DIR = os.path.abspath("data/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

MUSESCORE_PATH = "/Applications/MuseScore 4.app/Contents/MacOS/mscore"


def midi_to_pdf(midi_path: str):
    midi_path = os.path.abspath(midi_path)

    score = converter.parse(midi_path)

    base_name = os.path.splitext(os.path.basename(midi_path))[0]
    xml_path = os.path.join(OUTPUT_DIR, f"{base_name}.musicxml")
    pdf_path = os.path.join(OUTPUT_DIR, f"{base_name}.pdf")

    score.write("musicxml", fp=xml_path)

    command = [
        MUSESCORE_PATH,
        "-o",
        pdf_path,
        xml_path
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    # Treat it as success if the PDF was actually created
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        return {
            "musicxml_path": xml_path,
            "pdf_path": pdf_path,
            "musescore_returncode": result.returncode,
            "musescore_stderr": result.stderr
        }

    raise RuntimeError(
        f"MuseScore PDF export failed.\n"
        f"Return code: {result.returncode}\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )