#!/usr/bin/env python3
"""Regenerate A4 printable PDFs from data/mock_exams.json and vector scenes."""
from pathlib import Path
from html import escape
import json
from weasyprint import HTML
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data'/'mock_exams.json').read_text())
OUT=ROOT/'print';OUT.mkdir(exist_ok=True)
SVG={
 '01':'scene_01_library.svg','02':'scene_02_park.svg',
 '03':'scene_03_kitchen.svg','04':'scene_04_tennis.svg'
}
CSS='''
@page {size:A4; margin: 16mm 17mm 15mm 17mm; }
body{font-family:"Noto Sans CJK SC", "Noto Sans CJK JP", "Arial",sans-serif;color:#24354a;font-size:11.2pt;line-height:1.5;}
.eyebrow{font-size:9pt;letter-spacing:1px;font-weight:650;color:#607c92;}
h1{font-size:22pt;letter-spacing:-.3px;margin:0 0 8px;color:#193d56;}
h2{font-size:15pt;margin:15px 0 7px;color:#1d4b65;}
h3{font-size:12pt;margin:8px 0 3px;color:#31506c;}
p{margin:5px 0 8px;}
.page {break-after:page;}
.page:last-child {break-after:auto;}
.panel{background:#f1f7fa;border-left:5px solid #638ca3;border-radius:5px;padding:12px 15px;}
.passage{font-size:15pt;line-height:1.7;letter-spacing:.1px;}
.scene{display:block;width:100%;max-height:93mm;margin:14px 0 6px;border:1px solid #d6e3e9;border-radius:5px;}
.hint{color:#64788a;font-size:9pt;}
.footer{margin-top:15px;padding-top:8px;border-top:1px solid #d9e5eb;color:#788b99;font-size:8pt;}
.qrow{margin:10px 0 14px;break-inside:avoid;}
.qindex{display:inline-block;vertical-align:middle;background:#2d607b;color:white;border-radius:99px;padding:2px 9px;font-size:10pt;font-weight:bold;margin-right:5px;}
.question{font-size:12.5pt;font-weight:650;}
.answer{margin:7px 0 2px 28px;color:#196b67;font-size:11pt;font-weight:600;}
.alt{margin:0 0 1px 28px;font-size:9.8pt;}
.note{margin:0 0 0 28px;color:#7a8590;font-size:9pt;}
.tag{font-size:8pt;border:1px solid #c9dce7;border-radius:3px;color:#527489;padding:2px 6px;}
.line{border-bottom:1px dashed #b8cad4;height:18px;}
.row{display:flex;gap:12px}.col{flex:1}
ul,ol{margin:5px 0 7px;padding-left:21px;}li{margin:3px 0}
.table{width:100%;border-collapse:collapse;margin:10px 0;}
.table th,.table td{border-bottom:1px solid #d9e6ec;padding:9px;text-align:left;vertical-align:top;}
.table th{color:#607a8e;font-size:9pt;}
.muted{color:#6c8090;font-size:9pt;}
.practice{margin:10px 0;padding:9px 12px;border:1px solid #d3e1e7;border-radius:5px;}
'''

def write_pdf(name,body):
 doc=f'<!doctype html><html lang="zh"><meta charset="utf-8"><style>{CSS}</style><body>{body}</body></html>'
 HTML(string=doc,base_url=str(ROOT)).write_pdf(OUT/name)
 print(name,(OUT/name).stat().st_size)

student=[]
for set_ in DATA['sets']:
 pic=(ROOT/'assets'/'scenes'/set_.get('scene', SVG.get(set_['id'], ''))).as_uri()
 student.append(f'''<section class="page">
 <div class="eyebrow">EIKEN GRADE 3 · INTERVIEW CARD {set_['id']}</div>
 <h1>{escape(set_['topic'])}</h1>
 <div class="panel passage">{escape(set_['passage'])}</div>
 <img class="scene" src="{pic}" alt="Picture card scene">
 <h2>20 seconds to read silently → Read aloud</h2>
 <p class="hint">After reading, turn the passage card face down when the examiner asks you to. Listen carefully and answer aloud. During actual interview practice, do not read the examiner questions.</p>
 <div class="footer">Original practice card · For home study only · Not an official EIKEN past paper</div>
 </section>''')
write_pdf('01_student_cards_A4.pdf',''.join(student))

ex=[]
for set_ in DATA['sets']:
 qrows=[]
 for idx,q in enumerate(set_['questions'],1):
  alts=' / '.join(escape(x) for x in q['alternatives'])
  qrows.append(f'''<div class="qrow"><div><span class="qindex">{idx}</span><span class="tag">{q['kind'].upper()}</span> <span class="question">{escape(q['prompt'])}</span></div>
 <div class="answer">Model: {escape(q['model'])}</div>
 <div class="alt">Also OK (practice): {alts}</div>
 <div class="note">提示：{escape(q['tip'])}</div></div>''')
 ex.append(f'''<section class="page"><div class="eyebrow">EXAMINER SCRIPT / PARENT'S COPY · SET {set_['id']}</div><h1>{escape(set_['topic'])}</h1>
 <p class="muted">孩子只拿 Student Card。家长按顺序朗读5题，不要提前给孩子看答案。示例答案供练习参考，不代表官方逐字评分标准。</p>
 <div class="panel"><b>Start</b>: "Hello. Please read the passage silently for 20 seconds."<br>Wait 20 seconds. "Now, please read it aloud."<br>After reading: "Thank you. Now I will ask you five questions."</div>
 {''.join(qrows)}
 <div class="footer">Tip: Allow 5–10 seconds to answer. If the child freezes, ask "Pardon?" once and answer with a short sentence.</div></section>''')
write_pdf('02_parent_examiner_guide_A4.pdf',''.join(ex))

cram='''<section class="page">
<div class="eyebrow">EIKEN GRADE 3 · LAST-MINUTE PLAN</div><h1>2–3小时冲刺安排</h1>
<p>目标：熟悉完整流程、开口回答、减少因紧张而失分。孩子已经过一次考试；今天不追求复杂句，只练清楚、及时、自然地回答。</p>
<table class="table"><tr><th>时间</th><th>任务</th><th>操作</th></tr>
<tr><td>0–15分钟</td><td>流程热身</td><td>阅读本页 + 跟读下方关键句；确认面试准考证。</td></tr>
<tr><td>15–40分钟</td><td>Set 01 图书馆</td><td>听示范朗读；孩子读卡；完成5题；再讲答案。</td></tr>
<tr><td>40–65分钟</td><td>Set 02 公园</td><td>不看答案独立回答；只纠正影响理解的错误。</td></tr>
<tr><td>65–75分钟</td><td>休息10分钟</td><td>喝水、放松。</td></tr>
<tr><td>75–100分钟</td><td>Set 03 做饭</td><td>重点练 going to 与位置词 under / on / in。</td></tr>
<tr><td>100–125分钟</td><td>Set 04 运动</td><td>重点练 Why–Because 与 There are。</td></tr>
<tr><td>125–145分钟</td><td>闭卷随机模拟</td><td>家长任选2套，再问5题；孩子不能看答案。</td></tr>
<tr><td>145–160分钟</td><td>整理与确认</td><td>看准考证/地点/时间/证件要求；早点休息。</td></tr></table>
<h2>先记住这8句</h2>
<div class="practice">1. <b>Pardon?</b> &nbsp;（听不清时自然请求重复一次）<br>
2. <b>She is reading a book.</b><br>
3. <b>He is flying a kite.</b><br>
4. <b>There are three books.</b><br>
5. <b>It is under the table.</b><br>
6. <b>Because it is good for their health.</b><br>
7. <b>Yes, I do. I like soccer.</b><br>
8. <b>No, I don't. I like music.</b></div>
<h2>家长注意</h2>
<ul><li>先让孩子答完，再做纠正；不要打断每句话。</li><li>答题不需要一模一样，语义正确、语法基本可懂就可以。</li><li>口语流利度和主动回应重要，不要背空泛长段落。</li><li>正式面试以准考证和英检官方最新说明为准。</li></ul>
<div class="footer">2026-11-14 · Original practice material · Not affiliated with EIKEN</div>
</section>'''
write_pdf('03_last_minute_plan_A4.pdf',cram)

quick='''<section class="page"><div class="eyebrow">EIKEN GRADE 3 · SPEAKING CHEAT SHEET</div><h1>面试万能句型卡</h1>
<h2>1. 图片里的人正在做什么？</h2>
<div class="practice"><b>What is he/she doing?</b> → He/She is <b>verb-ing</b>.<br>He is cooking. / She is reading. / They are playing tennis.</div>
<h2>2. 几个？在哪里？</h2>
<div class="practice"><b>How many ... are there?</b> → There are two dogs.<br><b>Where is ...?</b> → It is under the table.<br>in（里） / on（上） / under（下） / next to（旁边） / behind（后面）</div>
<h2>3. 为什么？</h2>
<div class="practice"><b>Why is ...?</b> → <b>Because</b> it is fun / useful / good for us.</div>
<h2>4. 将要做什么？</h2>
<div class="practice"><b>What is he going to do?</b> → He is <b>going to</b> wash the dishes.</div>
<h2>5. 你自己的事情</h2>
<div class="practice"><b>Do you like sports?</b> → Yes, I do. I like soccer.<br><b>What do you do on weekends?</b> → I usually play games.<br><b>What subject do you like?</b> → I like math because it is fun.</div>
<h2>6. 没听清、没想好</h2>
<div class="practice"><b>Pardon?</b> / <b>Could you say that again?</b><br>如果暂时想不到长答案，可以用简短但相关的句子回答；避免一直沉默。</div>
<h2>最后5分钟</h2>
<ul><li>放慢一点，说清楚；答完可微笑看考官。</li><li>出错不要反复重来，继续下一题。</li><li>Don't panic. Speak English in simple sentences.</li></ul>
<div class="footer">Practice examples only; not official scoring criteria.</div>
</section>'''
write_pdf('04_speaking_patterns_A4.pdf',quick)

bonus_path=ROOT/'data'/'personal_questions.json'
if bonus_path.exists():
 items=json.loads(bonus_path.read_text())
 pages=[]
 for part in range(0,len(items),10):
  rows=''.join(f'''<div class="qrow"><div class="question"><span class="qindex">{part+i+1}</span>{escape(item['q'])}</div><div class="answer">{escape(item['a'])}</div></div>''' for i,item in enumerate(items[part:part+10]))
  pages.append(f'''<section class="page"><div class="eyebrow">EXTRA PRACTICE · PERSONAL QUESTIONS</div><h1>高频个人问答 {part+1}–{min(part+10,len(items))}</h1><p class="muted">先不看绿色示范答案，让孩子用真实情况回答。句子越简单、越自然越好。</p>{rows}<div class="footer">Examples for practice only · Answers may vary</div></section>''')
 write_pdf('05_bonus_personal_questions_A4.pdf',''.join(pages))
