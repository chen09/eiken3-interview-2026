import React, {useEffect, useRef, useState} from 'react';
import {createRoot} from 'react-dom/client';
import exams from '../../data/mock_exams.json';
import personal from '../../data/personal_questions.json';
import {saveSession, toggleReview} from './progress.mjs';
import { ArrowClockwise, ArrowLeft, ArrowRight, BookmarkSimple, BookOpen, Headphones, Pause, Play } from '@phosphor-icons/react';
import '@fontsource-variable/atkinson-hyperlegible-next';
import './style.css';

type Rating = 'good' | 'almost' | 'again';
type Progress = {sessions: {setId:string; rating:Rating; date:string}[]; review:string[]};
const labels: Record<Rating,string> = {good:'できた', almost:'もう少し', again:'もう一度'};
const originalScenes: Record<string,string> = {'01':'scene_01_library.svg','02':'scene_02_park.svg','03':'scene_03_kitchen.svg','04':'scene_04_tennis.svg'};
const scenes = Object.fromEntries(exams.sets.map(set => [set.id, set.scene ?? originalScenes[set.id]]));
const key = 'eiken3-progress-v1';
function loadProgress(): Progress { try {const p=JSON.parse(localStorage.getItem(key) || '{}'); return {sessions:Array.isArray(p.sessions)?p.sessions:[],review:Array.isArray(p.review)?p.review:[]};} catch {return {sessions:[],review:[]};} }
function App(){
 const [progress,setProgress]=useState<Progress>(loadProgress);
 const [page,setPage]=useState<'home'|'session'|'personal'|'progress'>('home');
 const [setId,setSetId]=useState('01');
 const [setGroup,setSetGroup]=useState(0);
 const [step,setStep]=useState(0);
 const [rate,setRate]=useState(1); const [personalIndex,setPersonalIndex]=useState(0);
 const [audioError,setAudioError]=useState('');
 const [activeFile,setActiveFile]=useState('');
 const [isPlaying,setIsPlaying]=useState(false);
 const [saved,setSaved]=useState(false); const audio=useRef<HTMLAudioElement|null>(null);
 const exam=exams.sets.find(x=>x.id===setId)!;
 useEffect(()=>{try {localStorage.setItem(key,JSON.stringify(progress));} catch { /* private mode or storage full */ }},[progress]);
 useEffect(()=>()=>{audio.current?.pause()},[]);
 const stopAudio = () => {
  if (audio.current) {
   audio.current.onplay = null;
   audio.current.onpause = null;
   audio.current.onended = null;
   audio.current.onerror = null;
   audio.current.pause();
   audio.current.currentTime = 0;
   audio.current = null;
  }
  setActiveFile('');
  setIsPlaying(false);
 };
 const play = (file: string, restart = false) => {
  setAudioError('');
  let player = audio.current;
  if (file !== activeFile || !player) {
   stopAudio();
   player = new Audio(`${import.meta.env.BASE_URL}audio-neural/${file}`);
   audio.current = player;
   setActiveFile(file);
   const currentPlayer = player;
   player.onplay = () => setIsPlaying(true);
   player.onpause = () => setIsPlaying(false);
   player.onended = () => setIsPlaying(false);
   player.onerror = () => {
    if (audio.current === currentPlayer) {
     setIsPlaying(false);
     setAudioError('音声ファイルを読み込めませんでした。');
    }
   };
  } else if (isPlaying && !restart) {
   player.pause();
   setIsPlaying(false);
   return;
  }
  if (restart || player.ended) player.currentTime = 0;
  player.playbackRate = rate;
  setIsPlaying(true);
  const currentPlayer = player;
  player.play().catch(error => {
   if (audio.current === currentPlayer && error.name !== 'AbortError') {
    setIsPlaying(false);
    setAudioError('音声を再生できません。もう一度ボタンを押してください。');
   }
  });
 };
 const audioControls = (file: string, label: string) => {
  const playing = activeFile === file && isPlaying;
  return <div className="audio-controls">
   <button className={`audio-toggle${playing ? ' is-playing' : ''}`} aria-pressed={playing} onClick={() => play(file)} aria-label={`${label}を${playing ? '一時停止' : '再生'}`}>
    {playing ? <Pause size={20} weight="fill" aria-hidden="true" /> : <Play size={20} weight="fill" aria-hidden="true" />}
    <span>{playing ? '一時停止' : `${label}を聞く`}</span>
   </button>
   <button className="audio-replay" onClick={() => play(file, true)} aria-label={`${label}を最初から聞く`}>
    <ArrowClockwise size={20} aria-hidden="true" /><span>もう一度</span>
   </button>
  </div>;
 };
 const start=(id:string)=>{stopAudio();setSetId(id);setStep(0);setSaved(false);setPage('session')};
 const move=(n:number)=>{stopAudio();setStep(Math.max(0,Math.min(5,n)))};
 const random=()=>{stopAudio();setPersonalIndex(i=>{const n=Math.floor(Math.random()*(personal.length-1));return n>=i?n+1:n})};
 const changeReview=(id:string)=>setProgress(p=>toggleReview(p,id));
 const reviewButton = (id: string) => {
  const marked = progress.review.includes(id);
  return <button className="review-toggle" aria-pressed={marked} onClick={() => changeReview(id)}>
   <BookmarkSimple size={19} weight={marked ? 'fill' : 'regular'} aria-hidden="true" />
   {marked ? '復習リストに追加済み' : 'あとで復習する'}
  </button>;
 };
 const ratingButtons=(fn:(r:Rating)=>void)=><div className="actions">{(['good','almost','again'] as Rating[]).map(r=><button key={r} className="secondary" onClick={()=>fn(r)}>{labels[r]}</button>)}</div>;
 return <><header><div className="wrap head"><button className="brand" onClick={()=>{stopAudio();setPage('home')}}><BookOpen size={26} weight="bold" aria-hidden="true" /><span className="brand-name">EIKEN 3 <span>面接れんしゅう</span></span></button><button className="nav" onClick={()=>{stopAudio();setPage('progress')}}>学習きろく</button></div></header><main className="wrap">
 {page === 'home' && <>
  <section className="hero">
   <h1>声に出して、<br className="mobile-break" />一歩ずつ。</h1>
   <p>英文を聞く。質問に答える。お手本をまねしてみよう。</p>
  </section>
  <aside className="official-materials" aria-label="英検協会の公式教材">
   <div><h2>まずは公式サンプルを確認</h2><p>英検協会が公開している問題カード・質問・解答例です。</p></div>
   <div className="official-links">
    <a href="https://www.eiken.or.jp/eiken/exam/virtual/grade_3/pdf/grade_3.pdf" target="_blank" rel="noopener noreferrer">公式サンプル問題・解答（PDF）</a>
    <a href="https://www.eiken.or.jp/eiken/exam/virtual/grade_3/" target="_blank" rel="noopener noreferrer">公式の面接の流れを見る</a>
   </div>
  </aside>
  <div className="section-title"><h2>模擬面接をえらぶ</h2><span>{exams.sets.length}セット・各5問</span></div>
  <nav className="set-groups" aria-label="セットの一覧ページ">
   {Array.from({length: Math.ceil(exams.sets.length / 6)}, (_, group) =>
    <button key={group} className="secondary" aria-current={setGroup === group ? 'page' : undefined} onClick={() => setSetGroup(group)}>
     {group * 6 + 1}〜{Math.min((group + 1) * 6, exams.sets.length)}
    </button>)}
  </nav>
  <div className="grid">
   {exams.sets.slice(setGroup * 6, (setGroup + 1) * 6).map(set => <article className="set-card" key={set.id}>
    <img src={`${import.meta.env.BASE_URL}scenes/${scenes[set.id]}`} alt="" width="960" height="420" />
    <div className="set-content">
     <p className="set-meta">セット {Number(set.id)}<span>{progress.sessions.filter(session => session.setId === set.id).length}回 完了</span></p>
     <h3>{set.topic}</h3>
     <button onClick={() => start(set.id)}>練習をはじめる<ArrowRight size={20} aria-hidden="true" /></button>
    </div>
   </article>)}
  </div>
  <section className="bonus">
   <div className="bonus-icon"><Headphones size={28} aria-hidden="true" /></div>
   <div><h2>自分のことを話そう</h2><p>20問の個人質問で、身近なことを英語に。</p></div>
   <button className="secondary" onClick={() => { random(); setPage('personal'); }}>個人質問を練習<ArrowRight size={20} aria-hidden="true" /></button>
  </section>
 </>}
 {page==='session'&&<><div className="breadcrumbs"><button onClick={()=>{stopAudio();setPage('home')}}><ArrowLeft size={18} aria-hidden="true" />セット選択</button><span>セット {Number(setId)}</span></div><div className="session-head"><div><h1>{exam.topic}</h1></div><span className="step">{step===5?'ふり返り':`質問 ${step+1} / 5`}</span></div>
 <div className="training-layout"><section className="card material"><div className="passage"><h2 className="material-title">英文を読もう</h2><p>{exam.passage}</p>{audioControls(`${setId}_reading_model.mp3`, '英文')}</div><img src={`${import.meta.env.BASE_URL}scenes/${scenes[setId]}`} alt="面接カードのイラスト" width="960" height="420"/></section>
 {step>=0&&step<5&&<section className="panel"><h2>質問 {step+1}</h2>{<><p className="english">{exam.questions[step].prompt}</p></>}{audioControls(`${setId}_q${step+1}.mp3`, '質問')}<p className="note">聞き終わったら、自分のペースで答えて次へ進もう。</p>{<><div className="answer"><h3 className="answer-title">答えの例</h3><strong>{exam.questions[step].model}</strong>{audioControls(`${setId}_answer${step+1}.mp3`, '答え')}<p className="tip"><span>ヒント</span>{exam.questions[step].tip}</p><small>ほかの例: {exam.questions[step].alternatives.join(' / ')}</small></div>{reviewButton(`mock:${setId}:${step}`)}</>}<div className="actions divider"><button className="secondary" disabled={step===0} onClick={()=>move(step-1)}><ArrowLeft size={18} aria-hidden="true" />前の質問</button><button onClick={()=>move(step+1)}>{step===4?'終了してふり返る':'次の質問へ'}<ArrowRight size={18} aria-hidden="true" /></button></div></section>}
 {step===5&&<section className="panel"><h2>おつかれさま！ 答えをふり返ろう</h2><p>答えは一例です。自分のことは、ほんとうのことを話して大丈夫。</p>{exam.questions.map((q,i)=><div className="review" key={i}><span className="number">QUESTION {i+1}</span><p className="english">{q.prompt}</p><strong>{q.model}</strong><p className="note">{q.tip}</p><div className="actions">{audioControls(`${setId}_q${i+1}.mp3`, '質問')}{audioControls(`${setId}_answer${i+1}.mp3`, '答え')}{reviewButton(`mock:${setId}:${i}`)}</div></div>)}<h3>今日の自分はどうだった？</h3>{saved?<p>学習きろくに保存しました。</p>:ratingButtons(r=>{setProgress(p=>saveSession(p,setId,r) as Progress);setSaved(true)})}<div className="actions"><button className="secondary" onClick={()=>move(4)}><ArrowLeft size={18} aria-hidden="true" />前の質問</button><button onClick={()=>{stopAudio();setPage('home')}}>セット選択へ</button></div></section>}
 </div></>}
 {page==='personal'&&<><div className="breadcrumbs"><button onClick={()=>{stopAudio();setPage('home')}}><ArrowLeft size={18} aria-hidden="true" />ホーム</button><span>個人質問</span></div><section className="panel"><p className="eyebrow">EXTRA / {personalIndex+1} OF {personal.length}</p><h1>自分のことを話そう</h1><p className="english">{personal[personalIndex].q}</p>{audioControls(`personal_${String(personalIndex+1).padStart(2,'0')}.mp3`, '質問')}<div className="actions"><button className="secondary" onClick={random}>次の問題をひく</button></div><div className="answer"><h3 className="answer-title">答えの例</h3><strong>{personal[personalIndex].a}</strong>{audioControls(`personal_answer_${String(personalIndex+1).padStart(2,'0')}.mp3`, '答え')}<p>自分のことに合わせて答えよう。</p></div>{reviewButton(`personal:${personalIndex}`)}<h3>自分で評価しよう</h3>{ratingButtons(r=>setProgress(p=>saveSession(p,`personal:${personalIndex}`,r) as Progress))}</section></>}
 {page==='progress'&&<><div className="breadcrumbs"><button onClick={()=>setPage('home')}><ArrowLeft size={18} aria-hidden="true" />ホーム</button></div><section className="panel"><h1>学習きろく</h1><h2>復習リスト <span className="note">{progress.review.length}問</span></h2>{progress.review.length===0?<p>まだありません。</p>:progress.review.map(id=>{const [kind,a,b]=id.split(':');const q=kind==='mock'?exams.sets.find(s=>s.id===a)?.questions[Number(b)]?.prompt:personal[Number(a)]?.q;return <div className="review" key={id}><p className="english">{q || '問題が見つかりません'}</p><button className="secondary" onClick={()=>{if(kind==='mock'){start(a);setStep(Number(b))}else{setPersonalIndex(Number(a));setPage('personal')}}}>この問題を練習</button> {reviewButton(id)}</div>})}<h2>練習のきろく</h2>{progress.sessions.length===0?<p>まだありません。</p>:<ul className="history">{[...progress.sessions].reverse().map((s,i)=><li key={i}><span>{s.setId.startsWith('personal:')?`個人質問 ${Number(s.setId.split(':')[1])+1}`:`セット ${s.setId}`}</span><span>{labels[s.rating]} · {new Date(s.date).toLocaleString('ja-JP')}</span></li>)}</ul>}</section></>}
 {page!=='home'&&<div className="speed"><label>音声スピード <select value={rate} onChange={e=>{const v=Number(e.target.value);setRate(v);if(audio.current)audio.current.playbackRate=v}}><option value="1">1x</option><option value="0.75">0.75x</option></select></label>{audioError&&<span role="alert">{audioError}</span>}</div>}
 </main><footer className="wrap">英検3級 面接れんしゅう · オリジナル教材・非公式</footer></>;
}

createRoot(document.getElementById('root')!).render(<App/>);
