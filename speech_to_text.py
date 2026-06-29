import whisper
import tempfile
import os

model = whisper.load_model("base")


def transcribe_audio(audio):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as temp_audio:

        temp_audio.write(audio.read())

        temp_path = temp_audio.name

    result = model.transcribe(temp_path)

    os.remove(temp_path)

    return result["text"]