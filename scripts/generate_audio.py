#!/usr/bin/env python3
"""Generate MP3 speaking drills with offline voices (espeak on Linux, say on macOS).

Requires: ffmpeg and pydub. Choose a different Mac voice by setting MAC_TTS_VOICE.
Question files contain audible 8–10 second reply gaps.
"""
import json,os,shutil,subprocess,tempfile,platform
from pathlib import Path
from pydub import AudioSegment
ROOT=Path(__file__).resolve().parents[1]
EXAMS=json.loads((ROOT/'data'/'mock_exams.json').read_text())['sets']
OUT=ROOT/'audio';OUT.mkdir(exist_ok=True)
VOICE=os.environ.get('MAC_TTS_VOICE','Samantha')

def tts(text):
 with tempfile.TemporaryDirectory() as td:
  wav=Path(td)/'tts.wav'
  if platform.system()=='Darwin' and shutil.which('say'):
   aiff=Path(td)/'tts.aiff'
   subprocess.run(['say','-v',VOICE,'-r','145','-o',str(aiff),text],check=True)
   subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(aiff),str(wav)],check=True)
  elif shutil.which('espeak'):
   subprocess.run(['espeak','-v','en-us','-s','130','-a','150','-w',str(wav),text],check=True)
  else:
   raise SystemExit('No supported offline TTS. Install espeak or use macOS say.')
  return AudioSegment.from_wav(wav).set_channels(1).set_frame_rate(24000)

def silence(sec):return AudioSegment.silent(duration=int(sec*1000),frame_rate=24000)
def export(seg,path):seg.export(path,format='mp3',bitrate='128k')
all_audio=AudioSegment.silent(duration=300)
for s in EXAMS:
 idx=s['id']
 # Model reading: pronunciation aid ONLY, not something played during the formal interview.
 read=tts('Reading model. '+s['topic']+'.')+silence(1)+tts(s['passage'])
 export(read,OUT/f'{idx}_reading_model.mp3')
 interview=tts('Practice set '+str(int(idx))+'. '+s['topic']+'.')+silence(1)
 interview+=tts('Please read the passage silently for twenty seconds.')+silence(20)
 interview+=tts('Now, please read it aloud.')+silence(24)
 interview+=tts('Thank you. Now, I will ask you five questions.')+silence(2)
 for i,q in enumerate(s['questions'],1):
  interview+=tts('Question '+str(i)+'. '+q['prompt'])+silence(9 if i<4 else 12)
 interview+=tts('Thank you. This is the end of the practice.')
 export(interview,OUT/f'{idx}_mock_interview.mp3')
 all_audio+=tts('Next practice set.')+silence(2)+interview+silence(4)
 print('Rendered set',idx)
export(all_audio,OUT/'all_four_mock_interviews.mp3')
print('Done')
