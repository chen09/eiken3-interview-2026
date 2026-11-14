#!/usr/bin/env python3
"""Generate English model-answer audio from the project's JSON data with edge-tts."""
import asyncio
import json
from pathlib import Path
import edge_tts

root = Path(__file__).resolve().parent.parent
output = root / 'web' / 'public' / 'audio-neural'
exams = json.loads((root / 'data' / 'mock_exams.json').read_text())['sets']
personal = json.loads((root / 'data' / 'personal_questions.json').read_text())
items = []
for exam in exams:
    for number, question in enumerate(exam['questions'], 1):
        items.append((f"{exam['id']}_answer{number}.mp3", question['model']))
for number, question in enumerate(personal, 1):
    items.append((f'personal_answer_{number:02}.mp3', question['a']))

async def main():
    output.mkdir(parents=True, exist_ok=True)
    limit = asyncio.Semaphore(3)
    async def generate(filename, text):
        async with limit:
            await edge_tts.Communicate(text, 'en-US-JennyNeural', rate='-10%').save(str(output / filename))
            print(filename, flush=True)
    await asyncio.gather(*(generate(filename, text) for filename, text in items))

asyncio.run(main())
