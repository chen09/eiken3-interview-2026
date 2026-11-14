#!/usr/bin/env python3
"""Generate the web passage, question and answer MP3s from the canonical JSON.

Requires edge-tts 7.3.1+. Existing audio is retained unless --overwrite is passed.
Use --set 05 to generate one mock interview's files only.
"""
import argparse
import asyncio
import json
import subprocess
import tempfile
from pathlib import Path
import edge_tts

root = Path(__file__).resolve().parent.parent
output = root / 'web' / 'public' / 'audio-neural'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--set', dest='set_id')
parser.add_argument('--overwrite', action='store_true')
args = parser.parse_args()
exams = json.loads((root / 'data' / 'mock_exams.json').read_text())['sets']
personal = json.loads((root / 'data' / 'personal_questions.json').read_text())
if args.set_id and args.set_id not in {exam['id'] for exam in exams}:
    parser.error('Unknown set ID')
items = []
for exam in exams:
    if args.set_id and exam['id'] != args.set_id:
        continue
    items.append((f"{exam['id']}_reading_model.mp3", exam['passage']))
    for number, question in enumerate(exam['questions'], 1):
        items.append((f"{exam['id']}_q{number}.mp3", question['prompt']))
        items.append((f"{exam['id']}_answer{number}.mp3", question['model']))
if not args.set_id:
    for number, question in enumerate(personal, 1):
        items.append((f'personal_{number:02}.mp3', question['q']))
        items.append((f'personal_answer_{number:02}.mp3', question['a']))

def validate(path):
    probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', str(path)], check=True, capture_output=True, text=True)
    duration = float(json.loads(probe.stdout)['format']['duration'])
    if duration < 0.5:
        raise ValueError(f'Empty or truncated audio: {path}')

async def main():
    output.mkdir(parents=True, exist_ok=True)
    limit = asyncio.Semaphore(3)
    staging = tempfile.TemporaryDirectory(prefix='.tts-', dir=root / 'web')
    async def generate(filename, text):
        path = output / filename
        if path.exists() and not args.overwrite:
            validate(path)
            return
        async with limit:
            temporary = Path(staging.name) / filename
            for attempt in range(3):
                try:
                    await edge_tts.Communicate(text, 'en-US-JennyNeural', rate='-10%').save(str(temporary))
                    validate(temporary)
                    temporary.replace(path)
                    print(filename, flush=True)
                    return
                except Exception:
                    temporary.unlink(missing_ok=True)
                    if attempt == 2:
                        raise
                    await asyncio.sleep(2 * (attempt + 1))
    try:
        await asyncio.gather(*(generate(filename, text) for filename, text in items))
    finally:
        staging.cleanup()

asyncio.run(main())
