import os
from pydub import AudioSegment


def preprocess_audio(audio_path: str) -> str:
    base_name = os.path.splitext(audio_path)[0]
    wav_path = f"{base_name}.wav"

    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_channels(1).set_frame_rate(44100)
    audio.export(wav_path, format="wav")

    return wav_path