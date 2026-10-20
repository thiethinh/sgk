import sys
import json
import asyncio
from pathlib import Path
import edge_tts

sys.stdout.reconfigure(encoding='utf-8')

entries_file = Path('src/data/entries.json')
vi_dir = Path('public/audio/vi')
en_dir = Path('public/audio/en/us')

vi_dir.mkdir(parents=True, exist_ok=True)
en_dir.mkdir(parents=True, exist_ok=True)

with open(entries_file, encoding='utf-8') as f:
    entries = json.load(f)

VI_VOICE = "vi-VN-HoaiMyNeural"
EN_VOICE = "en-US-JennyNeural"

async def generate_speech(text: str, voice: str, out_path: Path):
    if out_path.exists() and out_path.stat().st_size > 500:
        return
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(out_path))
    print(f"  + Generated: {out_path.name} ({text})")

async def main():
    print(f"Checking audio for {len(entries)} entries...")
    tasks = []
    for entry_id, entry in entries.items():
        word_vi = entry['wordVi']
        meanings = entry.get('meaningsEn', [])
        primary_en = meanings[0]['meaning'].split(' (')[0] if meanings else word_vi

        vi_path = vi_dir / f"{entry_id}.mp3"
        en_path = en_dir / f"{entry_id}.mp3"

        if not (vi_path.exists() and vi_path.stat().st_size > 500):
            tasks.append(generate_speech(word_vi, VI_VOICE, vi_path))
        if not (en_path.exists() and en_path.stat().st_size > 500):
            tasks.append(generate_speech(primary_en, EN_VOICE, en_path))

    if tasks:
        print(f"Generating {len(tasks)} missing audio files...")
        # Run in chunks of 5
        chunk_size = 5
        for i in range(0, len(tasks), chunk_size):
            chunk = tasks[i:i+chunk_size]
            await asyncio.gather(*chunk)
            await asyncio.sleep(0.3)
    else:
        print("All audio files already exist and are valid!")

    print("Audio check and generation complete.")

if __name__ == '__main__':
    asyncio.run(main())
