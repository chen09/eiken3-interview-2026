# 英检3级面试：2～3小时冲刺工程（2026-11）

这是一个**独立的 Codex 本地工程**，提供4套原创模拟面试题、额外20道个人问答、A4打印PDF、英语提问MP3，以及可修改的JSON数据和生成脚本。不是英检协会的历年真题或官方试题。

## 解压到指定位置

```bash
mkdir -p /Volumes/WDC2T/Project
unzip eiken3-interview-2026.zip -d /Volumes/WDC2T/Project
cd /Volumes/WDC2T/Project/eiken3-interview-2026
codex
```

ZIP 已含一层 `eiken3-interview-2026/` 根目录，避免重复嵌套。把 ZIP 放在 Terminal 当前路径，或在 `unzip` 命令里写 ZIP 的完整路径。

## 先打印

1. `print/01_student_cards_A4.pdf` — **只给孩子**（每套1页，短文+图）
2. `print/02_parent_examiner_guide_A4.pdf` — **家长看**（全部5题+参考答案）
3. `print/03_last_minute_plan_A4.pdf` — 160分钟练习计划
4. `print/04_speaking_patterns_A4.pdf` — 面试基础句型
5. `print/05_bonus_personal_questions_A4.pdf` — **额外20道**个人生活问答（两页）

## 听MP3

- `audio/01_mock_interview.mp3` 至 `audio/04_mock_interview.mp3` — 四套模拟面试，含20秒默读、朗读等待、每题回答间隔。播放时让孩子只看题卡。
- `audio/01_reading_model.mp3` 至 `audio/04_reading_model.mp3` — **练习时**听短文示范朗读。正式模拟不可先播放它，否则违背真实流程。
- `audio/all_four_mock_interviews.mp3` — 4套连播。

**音质说明**：ZIP内MP3使用离线英语合成音，语速较慢、能用于听题，但并非真人录音。Mac上可以用系统语音重新生成改善音色（见下面）。

## 目录结构

```text
eiken3-interview-2026/
├── README.md
├── AGENTS.md
├── requirements.txt
├── data/
│   ├── mock_exams.json        # 4套题、参考答案及中文提示
│   └── personal_questions.json # 附加20道个人问答
├── assets/scenes/             # 4张可编辑SVG情景图
├── print/                     # 已生成的5份A4 PDF
├── audio/                     # 已生成的9份MP3
└── scripts/
    ├── draw_scenes.py        # 可修改的SVG绘图脚本
    ├── generate_materials.py # 生成PDF
    ├── generate_audio.py     # 生成MP3
    └── rebuild.sh            # 一键重新生成
```

## 在Mac上用Codex修改和重建

```bash
cd /Volumes/WDC2T/Project/eiken3-interview-2026
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
brew install ffmpeg          # Mac默认已带 say TTS，不用额外安装espeak
bash scripts/rebuild.sh
```

默认在 Mac 上使用 macOS `say` 的 Samantha 英语语音。如果该语音不可用，可以改用其他已安装的英语语音：

```bash
say -v '?' | grep en_
MAC_TTS_VOICE=Samantha python scripts/generate_audio.py
```

## 复习方法（家长实际操作）

- 先把4张学生题卡打印，家长手册留给自己。
- 每套先听对应 `reading_model.mp3` 一次（只限学习环节），让孩子再自行朗读。
- 随后只播放 `mock_interview.mp3`，孩子看卡、读短文、回答5题；家长核对答案，别让孩子看答案页。
- 答案只需语义正确，不必逐字相同；短句清楚优于背长句。
- 正式考试日期、入场时间、地点及身份证件以孩子本人的二次受験票和英检官方最新公告为准。

## 后续工程方向

适合让Codex在此基础上继续做：本地网页答题器、随机抽题、计时器、自测计分、错题复习、更多题卡、导出到Anki。

建议Codex指令：`请阅读 AGENTS.md 和 data/mock_exams.json，为这个项目增加一个离线运行的单页英语面试练习器，保留现有PDF及MP3。`

## 来源和边界

题目及场景均为为本项目原创模拟材料，非官方试题。考试形式可参考日本英语检定协会的3级介绍：<https://www.eiken.or.jp/eiken/exam/grade_3/>。本工程不包含任何个人报名、账号、密码或实际成绩数据。

## 网页版

网页现有 **24套原创模拟面试，共120道问题**，另有20道个人问答。第01–04套保留原内容，第05–24套为追加内容，短文为28–32词。每套均有文章理解1题、图片2题、个人问答2题，以及配图、文字答案、中文提示和微软英语语音。首页按每6套分组。

首页另设英检协会官方样题 PDF 和官方面试示范入口。已核对官方题型与难度；官方样题明确禁止擅自转载，页面直接打开原站材料。新增题为本项目原创，不标记为真题。研究参考在2026-11-15核对。

- [英检协会3级试验说明](https://www.eiken.or.jp/eiken/exam/grade_3/solutions.html)
- [英检协会二次面试样题与答案](https://www.eiken.or.jp/eiken/exam/virtual/grade_3/pdf/grade_3.pdf)
- [英检协会使用条款](https://www.eiken.or.jp/sitepolicy/)
- [Eigox 公开模拟题示例](https://eigox.jp/textbook/Eiken2ji/student/TestCard_Eiken3_L3.pdf)
- [スクールコンパス的8套练习](https://eleschool-compass.com/english/englishstudy/eiken3-mensetsu.html)

原有 `print/` PDF 与 `audio/` 连续模拟录音仍为最初4套。`scripts/draw_scenes.py` 可重建全部24张SVG；`scripts/generate_materials.py` 已支持扩展题库，执行时会重建打印文件。本次扩充更新网页素材，未重写原有PDF与连续录音。

在线使用：<https://eiken3-interview-2026.pages.dev/>。网页及其题目和答案是公开的；自评和进度保存在浏览器中。

### 在 Mac 上启动

需要 Node.js 20.19 或更高版本。首次安装后，运行时无需网络；题库和媒体均在本地。

```bash
cd /Volumes/WDC2T/Project/eiken3-interview-2026/web
npm install
npm run dev
```

在 Mac 浏览器打开终端显示的 `http://localhost:5173/`。选择一套题并点击「練習をはじめる」，即可看到英文短文、第一道问题和参考答案。三项均有语音播放按钮，每题练习后手动进入下一题。进度和自评保存在当前浏览器的 localStorage，清除浏览器数据会删除记录；页面直接显示英文问题与参考答案，可分别播放语音。

如需在 iPad 上访问 Mac 的本地服务，可用同一局域网中的 Mac 地址和终端显示的端口。进度保存在访问设备的浏览器中，不在不同设备间同步。

```bash
npm test       # 进度逻辑测试
npm run build  # 静态网页输出到 web/dist/
```

网页题目直接读取 `data/` 中的 JSON。训练页面直接显示英文短文、问题、参考答案，各自提供音频播放按钮。网页使用 `web/public/audio-neural/` 中的微软 Jenny 英语语音。课文、问题和参考答案音频可通过安装 edge-tts 7.3.1 后运行 `python3 web/generate_answer_audio.py` 生成，生成时需要网络，播放已生成的文件可离线进行。默认保留已有音频，题目修改后使用 `--set 05 --overwrite` 更新指定套题。`web/prepare_audio.py` 用于旧版离线合成音频。题库修改后需要核对并更新对应音频，再重新构建。修改原 SVG 后也需将对应文件复制到 `web/public/scenes/`。原有 PDF 和音频重建命令保持不变。
