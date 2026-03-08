# Audio → Sheet Music

A backend API that converts an uploaded MP3 into musical notation by:

1. separating instruments from the audio
2. detecting pitch from a selected stem
3. generating MIDI notes
4. producing sheet music files

The system uses modern audio source separation and pitch detection to automatically generate a score.

---

# Pipeline

```
MP3
 ↓
Convert to WAV
 ↓
Source separation (Demucs)
 ↓
Select instrument stem
 ↓
Pitch detection (librosa pYIN)
 ↓
MIDI generation
 ↓
(Optional) MusicXML
```

Outputs can be opened directly in notation software like **MuseScore**.

---

# Features

- Upload an MP3 file
- Automatically separate audio into:
  - vocals
  - drums
  - bass
  - other instruments
- Transcribe an instrument stem into MIDI notes
- Generate MusicXML for sheet notation
- Compatible with MuseScore and other notation software

---

# Project Structure

```
audio_to_score
│
├── app
│   ├── main.py
│   ├── routes
│   │   └── upload.py
│   └── services
│       ├── separate.py
│       ├── transcribe.py
│       └── export_score.py
│
├── data
│   ├── input
│   ├── stems
│   └── output
│
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repo:

```
git clone https://github.com/YOUR_USERNAME/audio-to-score.git
cd audio-to-score
```

Create a virtual environment:

```
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Running the API

Start the server:

```
uvicorn app.main:app --reload
```

Open the API docs:

```
http://127.0.0.1:8000/docs
```

Upload an MP3 file through the `/upload` endpoint.

---

# Example Response

```json
{
  "original_file": "song.mp3",
  "wav_file": "data/input/song.wav",
  "stems": {
    "vocals_path": "...",
    "drums_path": "...",
    "bass_path": "...",
    "other_path": "..."
  },
  "transcription": {
    "midi_path": "data/output/bass.mid",
    "note_count": 93
  },
  "score": {
    "musicxml_path": "data/output/bass.musicxml"
  }
}
```

---

# Viewing the Sheet Music

Open the generated MIDI or MusicXML file in **MuseScore**:

```
data/output/bass.mid
```

MuseScore will automatically convert it into staff notation.

---

# Technologies Used

- FastAPI
- Demucs (audio source separation)
- librosa (pitch detection)
- pretty_midi
- music21
- MuseScore

---

# Limitations

Automatic transcription is imperfect and works best when:

- the instrument is **monophonic**
- the stem is **cleanly separated**
- the audio does not contain dense chords

Bass lines and vocal melodies tend to produce the best results.

---

# Future Improvements

- stem selection via API
- improved note smoothing and segmentation
- tempo detection and rhythmic quantization
- multi-instrument transcription
- frontend upload interface
- automated PDF score export