from google.cloud import texttospeech
from pathlib import Path

client = texttospeech.TextToSpeechClient()

Path("audio/male").mkdir(parents=True, exist_ok=True)
Path("audio/female").mkdir(parents=True, exist_ok=True)

word = "der Hackerangriff"

def save(filename, voice):
    response = client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=word),
        voice=texttospeech.VoiceSelectionParams(
            language_code="de-DE",
            name=voice
        ),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        ),
    )

    with open(filename, "wb") as f:
        f.write(response.audio_content)

save("audio/male/der_Hackerangriff.mp3", "de-DE-Neural2-D")
save("audio/female/der_Hackerangriff.mp3", "de-DE-Neural2-F")

print("Done!")
