#!/usr/bin/env python3
"""Generate 4 deterministic, editable vector illustrations for exam pictures."""
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
