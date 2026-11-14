import { test } from 'node:test';
import { strict as assert } from 'node:assert';
import { saveSession, toggleReview } from '../src/progress.mjs';

test('saving a completed session retains earlier history and records its date and rating', () => {
  const old = { sessions: [{setId:'01', date:'old', rating:'good'}], review: ['mock:01:0'] };
  const result = saveSession(old, '02', 'again', '2026-11-14T12:00:00Z');
  assert.deepEqual(result.sessions[1], {setId:'02', rating:'again', date:'2026-11-14T12:00:00Z'});
  assert.equal(result.sessions.length, 2);
  assert.deepEqual(result.review, ['mock:01:0']);
});
test('review marks can be added and removed without changing history', () => {
  const p = { sessions: [], review: [] };
  assert.deepEqual(toggleReview(toggleReview(p, 'personal:3'), 'personal:3'), p);
});
