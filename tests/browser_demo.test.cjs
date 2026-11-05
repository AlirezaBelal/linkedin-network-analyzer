const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { categorizeTitle, analyze, sample } = require('../docs/app.js');

test('browser title rules match representative project categories', () => {
  for (const [title, expected] of [
    ['Technical Recruiter', 'HR / Recruiter'], ['AI Engineer', 'AI / Data'],
    ['PM', 'Product'], ['Backend Software Engineer', 'Developer'],
    ['Community Founder', 'Other'], ['', 'Other']
  ]) assert.equal(categorizeTitle(title), expected);
});

test('browser scoring follows category weight plus profile completeness', () => {
  const results = analyze(sample);
  assert.deepEqual(results.map(x => [x.category, x.score, x.priority]), [
    ['Product', 8, 'High'], ['AI / Data', 6, 'Medium'],
    ['HR / Recruiter', 6, 'Medium'], ['Developer', 7, 'High'], ['Other', 3, 'Low']
  ]);
  assert.ok(results.every(x => x.recommendation && x.first.endsWith('Example')));
});

test('public demo exposes no contact upload or outbound processing', () => {
  const page = fs.readFileSync('docs/index.html', 'utf8');
  const app = fs.readFileSync('docs/app.js', 'utf8');
  assert.doesNotMatch(page, /type=["']file|<form\b/i);
  assert.match(page, /connect-src 'none'/);
  assert.doesNotMatch(app, /fetch\s*\(|XMLHttpRequest|WebSocket|sendBeacon|localStorage/);
});

