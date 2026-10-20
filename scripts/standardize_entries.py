import json
from pathlib import Path

entries_file = Path('src/data/entries.json')
with open(entries_file, encoding='utf-8') as f:
    entries = json.load(f)

for k, entry in entries.items():
    if 'meaningVi' not in entry and 'definitionVi' in entry:
        entry['meaningVi'] = entry['definitionVi']
    if 'ipa' not in entry:
        entry['ipa'] = entry['meaningsEn'][0]['ipa'] if entry.get('meaningsEn') else ''
    
    pos = entry.get('partOfSpeech', 'noun')
    for m in entry.get('meaningsEn', []):
        if 'partOfSpeech' not in m:
            m['partOfSpeech'] = 'noun' if 'danh' in pos else ('verb' if 'động' in pos else 'adj')

with open(entries_file, 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

print(f"Standardized {len(entries)} entries successfully.")
