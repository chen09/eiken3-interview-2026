# Codex project guide

## Objective
Maintain and extend a local Japanese EIKEN Grade 3 oral interview cram package used for private home study.

## Key constraints
- `data/mock_exams.json` is the single source of truth for the passage, 5 questions, and model answers in each set.
- Each set must have 1 passage question, 2 picture questions and 2 personal questions; passages should be about 30 words and readable by a Japanese middle-school learner.
- Keep each question and answer aligned with its corresponding illustration. Counts, positions and actions must be visually unambiguous.
- For the student-facing PDFs, do NOT expose examiner questions or model answers.
- Keep parent answer guide separate. Reference answers are examples, not official mark schemes.
- Preserve original SVGs for editable, accurate figure counts and placements.
- Scripts should work on macOS (preferred) and on Linux where possible.
- Do not insert names, emails, IDs, login credentials, CSE scores, or other private information.
- Materials are unofficial; do not label them 'official EIKEN past papers'.

## Main commands

```bash
python scripts/draw_scenes.py
python scripts/generate_materials.py
python scripts/generate_audio.py
```

`bash scripts/rebuild.sh` runs everything. PDF export uses WeasyPrint; MP3 export uses macOS `say` or Linux `espeak` plus ffmpeg/pydub.

## Suggested upgrades
Simple local-first React/Vite web practice: choose set, show passage and scene, 20-second reading countdown, play examiner audio, mic recording (opt-in), and answer reveal. Prioritize reliability and privacy. No backend is necessary.
