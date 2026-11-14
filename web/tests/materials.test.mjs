import {test} from 'node:test';
import {strict as assert} from 'node:assert';
import {readFileSync,readdirSync,statSync} from 'node:fs';

const sets=JSON.parse(readFileSync(new URL('../../data/mock_exams.json',import.meta.url))).sets;
const scenes=new URL('../public/scenes/',import.meta.url);
const audio=new URL('../public/audio-neural/',import.meta.url);

test('expanded bank provides complete five-question interviews at the existing reading level',()=>{
  assert.ok(sets.length>=24);
  assert.equal(new Set(sets.map(set=>set.id)).size,sets.length);
  assert.equal(new Set(sets.map(set=>set.passage)).size,sets.length);
  for(const set of sets){
    assert.deepEqual(set.questions.map(question=>question.kind),['passage','picture','picture','personal','personal']);
    const words=set.passage.split(/\s+/).length;
    assert.ok(words>=25 && words<=35,`${set.id}: ${words} words`);
    for(const question of set.questions){
      for(const field of ['prompt','model','tip']) assert.ok(question[field]?.trim(),`${set.id}: missing ${field}`);
    }
  }
});

test('every interview has its editable scene and all eleven web audio files',()=>{
  for(const set of sets){
    const scene=set.scene ?? readdirSync(scenes).find(name=>name.startsWith(`scene_${set.id}_`));
    assert.ok(scene,`missing scene for ${set.id}`);
    assert.equal(readFileSync(new URL(scene,scenes)).toString().includes('<svg'),true);
    const files=[`${set.id}_reading_model.mp3`];
    for(let number=1;number<=5;number++) files.push(`${set.id}_q${number}.mp3`,`${set.id}_answer${number}.mp3`);
    for(const file of files) assert.ok(statSync(new URL(file,audio)).size>1000,`empty audio ${file}`);
  }
  assert.equal(readdirSync(audio).filter(name=>name.includes('.part.')).length,0);
});

test('passages, questions, answers and alternatives have Japanese and Chinese translations',()=>{
  const personal=JSON.parse(readFileSync(new URL('../../data/personal_questions.json',import.meta.url)));
  const translated=[];
  for(const set of sets){
    translated.push(set.translation.topic,set.translation.passage);
    for(const question of set.questions){
      translated.push(question.translation.prompt,question.translation.model,question.translation.tip);
      assert.equal(question.translation.alternatives.length,question.alternatives.length);
      translated.push(...question.translation.alternatives);
    }
  }
  for(const question of personal) translated.push(question.translation.q,question.translation.a);
  for(const text of translated){
    for(const language of ['ja','zh']){
      assert.equal(typeof text?.[language],'string',`missing ${language}`);
      assert.ok(text[language].trim().length>0);
      assert.match(text[language],/[\u3040-\u30ff\u3400-\u9fff]/);
    }
  }
});
