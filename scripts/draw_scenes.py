#!/usr/bin/env python3
"""Generate deterministic, editable vector illustrations for the interview bank."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
OUT=R/'assets'/'scenes'
OUT.mkdir(parents=True,exist_ok=True)

def svg_start(title):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="420" viewBox="0 0 960 420" role="img" aria-label="{title}">
<rect width="960" height="420" rx="16" fill="#eff6fa"/>
<rect x="0" y="336" width="960" height="84" fill="#e5edf1"/>
<path d="M0 336H960" stroke="#b7cbd7" stroke-width="3"/>
'''
def end(s):return s+'</svg>'
def rect(x,y,w,h,fill,rx=0,stroke='none',sw=1):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def line(x1,y1,x2,y2,color='#405467',sw=5):return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>'
def circle(x,y,r,fill,stroke='none',sw=1):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def path(d,fill='none',stroke='#405467',sw=5):return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>'
def human(x,y,shirt='#e48a69',pants='#365e7c',rightarm=True):
 # x at center, y at head top
 s=circle(x,y+24,27,'#f1c4a2')+path(f'M{x-22} {y+19} Q{x} {y-10} {x+23} {y+19}', '#364757','#364757',2)
 s+=rect(x-31,y+55,62,92,shirt,15)+line(x-18,y+147,x-25,y+225,pants,16)+line(x+18,y+147,x+23,y+225,pants,16)
 s+=line(x-32,y+71,x-63,y+122,'#f1c4a2',14)+line(x+32,y+71,x+59,y+112,'#f1c4a2',14)
 s+=path(f'M{x-42} {y+223} h30 M{x+8} {y+223} h30','none','#2d4053',11)
 return s

def dog(x,y,scale=1,color='#bc865e'):
 s=f'<g transform="translate({x} {y}) scale({scale})">'
 s+=rect(0,20,74,34,color,17)+circle(13,20,26,color)+path('M-7 11 L-24 -14 L5 -4 Z',color,'none',0)
 s+=circle(4,15,3,'#263746')+circle(-14,29,4,'#263746')+line(20,48,18,77,color,11)+line(60,48,62,77,color,11)+path('M73 25 Q99 11 94 -7','none',color,10)
 return s+'</g>'

# Library: girl reads book, exactly 3 closed books on the right side of the table.
s=svg_start('A girl reads a book at a library table. Three books rest on the table.')
s+=rect(38,56,150,238,'#7296aa',8)+rect(50,69,126,208,'#edf4f3',3)
for yy in (92,147,202,257):s+=line(53,yy,173,yy,'#7296aa',8)
for i,(x,w,c) in enumerate([(60,13,'#dc806d'),(76,18,'#77a995'),(97,12,'#607ba8'),(113,19,'#d9a45c'),(138,13,'#b79ac1')]):
 for yy in (98,153,208):s+=rect(x,yy,w,42,c,2)
s+=rect(205,232,670,29,'#b17d55',9)+rect(252,255,22,90,'#996b4c',3)+rect(805,255,22,90,'#996b4c',3)
s+=circle(482,141,26,'#f0c39f')+path('M453 139 Q475 105 505 137','#40505e','#40505e',3)
s+=rect(442,170,77,79,'#e9a276',18)+line(460,247,454,310,'#365e7c',17)+line(500,247,510,310,'#365e7c',17)
s+=path('M427 200 L475 221 L490 191 L458 174 Z','#e7f0dd','#4d6b74',3)
s+=path('M475 221 L523 199 L496 173 L490 191 Z','#ffffff','#4d6b74',3)
s+=line(445,195,450,218,'#f0c39f',12)+line(519,190,511,211,'#f0c39f',12)
# 3 closed books on table, separate from the open one
s+=rect(661,202,111,12,'#dc826c',3)+rect(669,188,103,11,'#75a991',3)+rect(665,173,108,11,'#6c8caf',3)
(OUT/'scene_01_library.svg').write_text(end(s))

# Park: 2 dogs close to bench, boy flying kite.
s=svg_start('A boy flies a kite. Exactly two dogs are near a park bench.')
s+=circle(135,112,75,'#91bda2')+circle(194,148,58,'#a4caae')+rect(149,160,19,171,'#8b6d51',7)
s+=circle(824,110,67,'#9fcaaf')+rect(815,145,18,187,'#8b6d51',7)
s+=rect(260,252,242,18,'#b78359',7)+rect(265,212,232,26,'#bb8a61',7)+line(286,275,284,333,'#6e8190',10)+line(469,275,470,333,'#6e8190',10)
s+=dog(288,282,.72,'#c88b62')+dog(395,285,.65,'#9b8067')
s+=human(684,101,'#e48e6d','#3b6081')
s+=line(740,213,848,55,'#677889',2)+path('M850 40 L907 83 L847 116 L793 82 Z','#efb162','#9a7251',4)+line(851,40,848,116,'#9a7251',3)+line(793,82,907,83,'#9a7251',3)+path('M848 115 Q823 138 850 161 Q874 181 858 204','none','#a07b66',3)
(OUT/'scene_02_park.svg').write_text(end(s))

# Kitchen: boy holding plates near sink; cat under table.
s=svg_start('A boy with dirty dishes near a kitchen sink. A cat rests under the table.')
s+=rect(41,63,236,204,'#d7e7ee',9)+rect(60,89,194,149,'#bfd2da',3)
s+=rect(50,268,316,61,'#9cb3bc',5)+rect(70,228,254,41,'#d2e3eb',6)+rect(150,236,99,27,'#738c9c',8)
s+=path('M196 236 L196 201 Q196 187 215 187 L226 187','none','#607a89',8)+circle(236,185,6,'#7e98a8')
s+=human(440,90,'#91afa4','#3a5b7b')
s+=path('M457 208 Q505 221 542 203','none','#f0c39f',16)
s+=path('M493 183 Q536 159 576 184 Q535 207 493 183','#f5f8f8','#8ea4af',4)+path('M503 177 Q540 158 566 176','none','#a6bdc1',3)
s+=rect(656,224,246,24,'#ab7c5e',5)+rect(681,245,15,104,'#9e6e50',3)+rect(853,245,15,104,'#9e6e50',3)
# cat crouches under the table
s+=path('M718 304 Q730 273 761 281 Q788 288 791 314 Q800 338 763 340 L730 338 Z','#d5ae89','#a78363',3)
s+=path('M715 287 L718 264 L738 278 M757 280 L768 262 L780 287','#d5ae89','#a78363',3)
s+=circle(735,296,3,'#3b4d57')+circle(761,296,3,'#3b4d57')+path('M741 304 L750 309 L757 305','none','#3b4d57',3)+path('M791 317 Q836 300 821 271','none','#b18c6d',10)
(OUT/'scene_03_kitchen.svg').write_text(end(s))

# Tennis: girl playing tennis; 3 ground balls clearly distinct.
s=svg_start('A girl playing tennis. Exactly three tennis balls lie on the ground.')
s+=rect(0,283,960,137,'#bcdac4',0)+line(60,286,898,286,'#ffffff',5)+line(140,333,820,333,'#ffffff',4)
s+=human(452,92,'#efb56f','#4c7292')
s+=path('M495 195 Q549 155 602 130','none','#efc5a5',13)+path('M591 112 L650 47 M613 122 L671 63','none','#576f81',6)
s+=path('M650 40 Q690 10 724 46 Q742 75 697 103 Q664 122 639 90 Q626 68 650 40 Z','none','#5e8195',7)
for x,y in [(693,325),(754,354),(824,316)]:
 s+=circle(x,y,17,'#f0d25e','#ffffff',2)+path(f'M{x-10} {y-12} Q{x+12} {y} {x-10} {y+13}','none','#faf4d6',2)
(OUT/'scene_04_tennis.svg').write_text(end(s))
print('Generated 4 SVG scenes')

# Expanded cards use explicit object groups so the count questions remain auditable.
import json
from html import escape

def table(x=580, y=248):
 return rect(x,y,310,18,'#b17d55',5)+rect(x+20,y+18,16,105,'#996b4c',3)+rect(x+274,y+18,16,105,'#996b4c',3)

def cup(x,y):
 return rect(x,y,30,38,'#83b4c4',4)+path(f'M{x+30} {y+8} q23 -3 16 20 h-16','none','#5e8c9d',4)

def flower(x,y):
 s=line(x,y,x,y+48,'#5b906f',4)
 for dx,dy in [(0,-12),(12,0),(0,12),(-12,0)]: s+=circle(x+dx,y+dy,9,'#e5a28f')
 return s+circle(x,y,7,'#e3bd53')

def envelope(x,y):
 return rect(x,y,80,44,'#ffffff',3, '#6b8898',3)+path(f'M{x} {y} l40 26 l40 -26','none','#6b8898',3)

def tree(x,y):
 return rect(x-8,y+28,16,90,'#97755a',3)+circle(x,y,46,'#92b99a')

def expanded_scene(kind):
 s=''
 if kind=='watering':
  s+=human(350,80,'#d6927c')+rect(399,187,70,45,'#6b99b5',5)+path('M468 200 l45 12 l-44 11','#6b99b5','#4a748d',3)
  s+=path('M510 218 q20 18 28 48 M510 225 q10 20 13 41','none','#6da8cf',3)
  for x in [560,690,820]: s+=flower(x,225)+path(f'M{x-26} 278 h52 l-8 55 h-36 Z','#be8968','#8b6d55',3)
 elif kind=='bicycle':
  for x in [375,555]:s+=circle(x,300,60,'none','#566b7a',7)
  s+=path('M375 300 l80 -100 l100 100 h-100 l-45 -100 M455 300 l50 -122 h40','none','#58978d',7)
  s+=circle(451,102,25,'#f1c4a2')+path('M440 133 l-18 63 l70 19 l-32 57 M430 150 l70 25','none','#cf8c71',17)+line(475,180,519,176,'#f1c4a2',12)
  s+=tree(780,120)+line(737,154,825,154,'#81694e',6)
  for x in [752,802]:s+=circle(x,139,13,'#879bad')+path(f'M{x+10} 139 l12 5 l-12 5 Z','#d7a45e','none',0)+circle(x+4,136,2,'#263746')
 elif kind=='piano':
  s+=human(350,80,'#d6a174')+rect(410,148,220,140,'#556674',8)+rect(400,204,240,35,'#f8faf9',3)
  for x in range(415,630,20):s+=line(x,205,x,235,'#667783',2)
  s+=line(410,288,410,339,'#556674',10)+line(620,288,620,339,'#556674',10)+line(391,195,447,217,'#f1c4a2',12)
  for x in [690,775,860]:s+=rect(x,210,52,55,'#7ba89b',5)+rect(x-4,269,60,12,'#638c80',2)+line(x+5,280,x+5,338,'#638c80',6)+line(x+46,280,x+46,338,'#638c80',6)
 elif kind=='shopping':
  s+=human(335,80)+rect(398,210,62,74,'#d6ad66',4)+path('M410 210 v-18 q20 -30 38 0 v18','none','#9e7942',5)+table()
  for x in [620,690,760,830]:s+=circle(x,224,20,'#d17d68')+line(x,205,x+4,194,'#6b8053',4)
 elif kind=='photo':
  s+=human(335,80,'#8aa9bb')+rect(372,158,66,45,'#4b6173',6)+circle(406,180,17,'#a5c3ce','#304556',4)+line(365,158,380,178,'#f1c4a2',12)
  for x in range(560,900,50):s+=rect(x,205,14,110,'#c8aa85',2)
  s+=line(550,235,900,235,'#b28d67',9)
  for x in [650,810]:
   s+=path(f'M{x-20} 297 q20 -50 52 -10 q25 50 -38 44 Z','#e5dfd4','#8f9fa5',3)+circle(x,275,24,'#e5dfd4','#8f9fa5',3)
   s+=path(f'M{x-14} 255 q-20 -68 2 -57 q15 16 10 55 M{x+7} 252 q5 -73 22 -60 q15 20 -4 64','#e5dfd4','#8f9fa5',3)+circle(x+2,275,3,'#334b59')
 elif kind=='umbrella':
  s+=human(320,90,'#a0b3a2')+path('M180 117 q95 -145 190 0 Z','#8eb4c5','#627f98',4)+path('M275 117 v126 q25 18 25 -7','none','#627f98',5)
  s+=rect(610,260,244,86,'#9eb3bf',8)
  for i,x in enumerate([650,730,810]):
   s+=path(f'M{x} 150 v155 M{x} 150 q18 -30 28 0','none','#667e8d',5)+path(f'M{x} 184 l-18 91 l38 0 Z',['#d5a06f','#799f95','#b092ae'][i],'#6e8793',2)
 elif kind=='beach':
  s+=rect(0,270,960,150,'#e6d6af')+rect(0,250,960,32,'#9fc7d7')
  s+=circle(360,177,25,'#f1c4a2')+path('M350 209 l-40 50 l64 13 l18 60 M320 250 l-38 71','none','#739caa',18)+line(370,219,437,290,'#f1c4a2',13)
  s+=rect(424,290,23,51,'#a6c6d5',5)+rect(429,277,13,15,'#6e99b2',2)
  for x,y in [(610,315),(720,338),(833,302)]:s+=circle(x,y,22,'#dcb36f','#ffffff',3)
 elif kind=='computer':
  s+=human(350,80,'#91afa4')+table(430,245)+rect(535,120,180,100,'#607c91',6)+rect(545,130,160,77,'#bddbe6',2)+rect(614,220,17,23,'#607c91',2)+rect(515,235,220,9,'#e0e8eb',2)+line(390,193,532,237,'#f1c4a2',12)
  for y in [221,237]:s+=line(790,y,860,y,'#cf9d62',8)
 elif kind=='snow':
  s+=rect(0,300,960,120,'#f9fcfd')+human(320,85,'#b28aa0')
  for x in [550,800]:
   s+=circle(x,280,58,'#ffffff','#b5cbd5',3)+circle(x,194,38,'#ffffff','#b5cbd5',3)+circle(x-12,188,4,'#405467')+circle(x+12,188,4,'#405467')+path(f'M{x} 198 l28 4 l-28 5 Z','#d99b5a','none',0)
  s+=line(380,197,509,185,'#f1c4a2',13)
 elif kind=='birthday':
  s+=human(390,85,'#8faa9e')+line(420,175,490,204,'#f1c4a2',12)+rect(460,190,240,70,'#e9b6ad',8)+rect(448,258,265,12,'#91aebb',4)
  for x in [485,523,561,599,637,675]:s+=rect(x,157,7,34,'#dfb657',1)+path(f'M{x+3} 150 q-12 -10 1 -18 q12 11 -1 18','#dfa052','none',0)
 elif kind=='breakfast':
  s+=human(350,80,'#cf9b86')+table(460,248)+path('M367 113 l40 -12 l15 37 l-40 12 Z','#e2c58d','#a98c60',3)+line(380,185,392,137,'#f1c4a2',12)
  for x in [500,610,720]:s+=cup(x,208)
 elif kind=='picnic':
  s+=human(320,80,'#d8aa78')+cup(365,110)+line(356,180,371,128,'#f1c4a2',12)+rect(500,275,400,95,'#c5d8b7',6)
  for x,y in [(550,310),(620,340),(690,310),(760,340),(830,310)]:s+=circle(x,y,21,'#dca456')+line(x,y-21,x+3,y-30,'#769460',3)
 elif kind=='cleaning':
  s+=rect(690,66,175,270,'#adc3cb',6)+circle(837,210,6,'#6c8797')+human(320,80,'#a58da9')+line(380,190,490,310,'#9e805f',9)+path('M480 293 l55 21 l-23 33 l-59 -20 Z','#c7ab76','#9b8056',3)
  for x in [610,730]:s+=path(f'M{x-32} 282 h64 l-7 54 h-50 Z','#8eb5c4','#688d9e',3)+path(f'M{x-27} 284 q27 -57 54 0','none','#688d9e',4)
 elif kind=='drawing':
  s+=human(320,80,'#d3a075')+rect(420,133,150,150,'#f7f9f5',3,'#b69c79',5)+line(420,283,393,344,'#a98c66',7)+line(570,283,593,344,'#a98c66',7)+line(375,190,463,210,'#f1c4a2',12)+line(459,209,484,177,'#657f91',4)
  s+=flower(496,203)+table(630,280)+path('M715 235 h88 l-13 45 h-60 Z','#8fb5c0','#6d929f',3)
  for x in [715,744,773,802]:s+=flower(x,178)
 elif kind=='pets':
  s+=human(330,80,'#91afa4')+dog(700,252,1.05)+rect(405,195,65,46,'#c5a77b',5)+path('M468 218 l32 36','none','#c5a77b',12)
  for x in [530,625,720]:s+=path(f'M{x-32} 320 h64 q-5 31 -32 31 q-27 0 -32 -31 Z','#8bb5c4','#668d9e',3)
  s+=line(365,170,417,210,'#f1c4a2',12)
  for x,y in [(486,266),(499,290),(519,309)]:s+=circle(x,y,4,'#a98561')
 elif kind=='station':
  s+=human(320,80,'#9bb4a2')+rect(395,216,74,113,'#b59679',8)+path('M415 216 v-29 h35 v29','none','#7e735f',5)+circle(411,333,7,'#516a77')+circle(452,333,7,'#516a77')+rect(570,278,320,16,'#a68162',3)+line(592,294,592,340,'#6c8592',8)+line(867,294,867,340,'#6c8592',8)
  for x in [610,770]:s+=rect(x,210,81,67,'#8ba4ba',7)+path(f'M{x+20} 210 v-20 h40 v20','none','#617e98',5)
 elif kind=='swimming':
  s+=rect(0,245,960,175,'#a7d1df')+circle(350,238,26,'#f1c4a2')+path('M370 260 l95 22 l77 -35 M450 279 l62 26','none','#e1ab8b',16)+path('M220 306 q45 -20 90 0 t90 0 t90 0 t90 0','none','#d7eef5',5)
  for x in [590,680,770,860]:s+=circle(x,140,32,'#d3a168')+circle(x,140,17,'#eff6fa')
 elif kind=='recycling':
  s+=human(320,80,'#bd9680')+line(370,185,550,206,'#f1c4a2',12)+rect(534,192,21,51,'#9fbdcf',4)+rect(539,181,11,15,'#709aaf',2)
  for x in [505,650,795]:s+=rect(x,268,115,72,'#9ab7a5',4,'#6e9980',3)+rect(x+25,265,65,7,'#456a56',3)
 elif kind=='letters':
  s+=human(320,80,'#a2acbe')+table(420,248)+rect(455,206,104,40,'#fafbf9',2)+line(380,192,482,226,'#f1c4a2',12)+line(482,226,503,195,'#597f96',4)
  for x in [650,790]:s+=envelope(x,203)
 elif kind=='rope':
  for x in [110,730,860]:s+=tree(x,170)
  s+=human(415,55,'#dca77b')+path('M350 176 C220 420 620 420 475 166','none','#7b92a3',6)
 else:raise ValueError(kind)
 return s

exams=json.loads((R/'data/mock_exams.json').read_text())['sets']
for exam in exams:
 if 'scene_type' not in exam:continue
 picture_questions=' '.join(q['model'] for q in exam['questions'] if q['kind']=='picture')
 content=svg_start(escape(picture_questions))+expanded_scene(exam['scene_type'])
 (OUT/exam['scene']).write_text(end(content))
print(f'Generated {len(exams)} SVG scenes in total')
