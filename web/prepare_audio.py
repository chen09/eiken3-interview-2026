#!/usr/bin/env python3
"""Derive question clips from existing MP3s; generate bonus clips locally on macOS."""
import json, re, subprocess, pathlib, shutil, tempfile, os
root = pathlib.Path(__file__).resolve().parent.parent
out = root / 'web/public/audio'
out.mkdir(parents=True, exist_ok=True)
for exam in json.loads((root/'data/mock_exams.json').read_text())['sets']:
    source = root/'audio'/f"{exam['id']}_mock_interview.mp3"
    result = subprocess.run(['ffmpeg','-hide_banner','-i',str(source),'-af','silencedetect=noise=-40dB:d=1.4','-f','null','-'],capture_output=True,text=True,check=True).stderr
    starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)',result)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)',result)]
    gaps = [(a,b) for a,b in zip(starts,ends) if b-a>8]
    if len(gaps)!=7: raise ValueError(f"Unexpected silence layout in {source}: {gaps}")
    # The first two long gaps are reading time; the short gap preceding Q1 is 2 seconds.
    short = [(a,b) for a,b in zip(starts,ends) if 1.8 < b-a < 4 and gaps[1][1] < a < gaps[2][0]]
    if len(short)!=1: raise ValueError(f'Cannot locate first question in {source}')
    question_starts = [short[0][1]] + [g[1] for g in gaps[2:6]]
    for i,(start,gap) in enumerate(zip(question_starts,gaps[2:]),1):
        subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(max(0,start-.18)),'-i',str(source),'-t',str(gap[0]-start+.35),'-codec:a','libmp3lame','-q:a','3',str(out/f"{exam['id']}_q{i}.mp3")],check=True)
    shutil.copy2(root/'audio'/f"{exam['id']}_reading_model.mp3",out/f"{exam['id']}_reading_model.mp3")
with tempfile.TemporaryDirectory() as tmp:
    for i,item in enumerate(json.loads((root/'data/personal_questions.json').read_text()),1):
        aiff=pathlib.Path(tmp)/'voice.aiff'
        wav=pathlib.Path(tmp)/'voice.wav'
        if shutil.which('espeak'):
            subprocess.run(['espeak','-v','en-us','-s','130','-a','150','-w',str(wav),item['q']],check=True)
            source=wav
        elif shutil.which('say'):
            subprocess.run(['say','-v',os.getenv('MAC_TTS_VOICE','Samantha'),'-r','145','-o',str(aiff),item['q']],check=True)
            source=aiff
        else: raise SystemExit('Install espeak or use macOS say')
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(source),'-codec:a','libmp3lame','-q:a','3',str(out/f'personal_{i:02}.mp3')],check=True)
        if (out/f'personal_{i:02}.mp3').stat().st_size < 1000: raise RuntimeError(f'Empty speech for personal question {i}')
