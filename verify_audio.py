from pathlib import Path
import json

MANIFEST = Path("manifest.json")
MALE = Path("audio/male")
FEMALE = Path("audio/female")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

male_missing = []
female_missing = []

for word, data in manifest.items():
    male = Path(data["male"])
    female = Path(data["female"])

    if not male.exists():
        male_missing.append(word)

    if not female.exists():
        female_missing.append(word)

print("=" * 50)
print("Words in manifest :", len(manifest))
print("Male missing      :", len(male_missing))
print("Female missing    :", len(female_missing))
print("Male mp3 count    :", len(list(MALE.glob("*.mp3"))))
print("Female mp3 count  :", len(list(FEMALE.glob("*.mp3"))))
print("=" * 50)

if male_missing:
    print("\nFirst 20 missing male:")
    print(male_missing[:20])

if female_missing:
    print("\nFirst 20 missing female:")
    print(female_missing[:20])
