from pathlib import Path
import json,re
from google.cloud import texttospeech

INPUT_FILE = "german_words_only_all.txt"
MALE_DIR=Path("audio/male"); FEMALE_DIR=Path("audio/female")
MANIFEST=Path("manifest.json"); ERRORS=Path("errors.log")
MALE_DIR.mkdir(parents=True,exist_ok=True); FEMALE_DIR.mkdir(parents=True,exist_ok=True)
client=texttospeech.TextToSpeechClient()

def safe_name(s):
    for a,b in {"ä":"ae","ö":"oe","ü":"ue","Ä":"Ae","Ö":"Oe","Ü":"Ue","ß":"ss"}.items():
        s=s.replace(a,b)
    s=re.sub(r"[^\w\s-]","",s).replace(" ","_")
    return s

def synth(txt,voice,out):
    resp=client.synthesize_speech(
      input=texttospeech.SynthesisInput(text=txt),
      voice=texttospeech.VoiceSelectionParams(language_code="de-DE",name=voice),
      audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3))
    out.write_bytes(resp.audio_content)

if MANIFEST.exists():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
else:
    manifest = {}
words=[x.strip() for x in Path(INPUT_FILE).read_text(encoding="utf-8").splitlines() if x.strip()]
for i,w in enumerate(words,1):
    mf=MALE_DIR/(safe_name(w)+".mp3"); ff=FEMALE_DIR/(safe_name(w)+".mp3")
    try:
        if not mf.exists(): synth(w,"de-DE-Neural2-D",mf)
        if not ff.exists(): synth(w,"de-DE-Neural2-F",ff)
        manifest[w]={"male":str(mf),"female":str(ff)}
        print(f"[{i}/{len(words)}] {w}")
    except Exception as e:
        ERRORS.open("a",encoding="utf-8").write(f"{w}: {e}\n")
MANIFEST.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print("Finished")
