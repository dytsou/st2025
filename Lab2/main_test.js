const test = require('node:test');
const assert = require('assert');
const { Application, MailSystem } = require('./main');


test('MailSystem.write returns expected context', () => {
  const ms = new MailSystem();
  const out = ms.write('Alice');
  assert.strictEqual(out, 'Congrats, Alice!');
});

test('MailSystem.send returns true on success and false on failure', () => {
  const originalRandom = Math.random;
  try {
    const ms = new MailSystem();
    // Force to use success branch
    Math.random = () => 0.7;
    assert.strictEqual(ms.send('Bob', 'ctx'), true);
    // Force to use failure branch
    Math.random = () => 0.3;
    assert.strictEqual(ms.send('Bob', 'ctx'), false);
  } finally {
    // Restore original Math.random
    Math.random = originalRandom;
  }
});

test('Application.getNames reads file and returns people and empty selected', async () => {
  const fs = require('fs');
  fs.writeFileSync('name_list.txt', 'Alice\nBob', 'utf8');

  const app = new Application();
  // Wait a tick to allow constructor .then to run
  await new Promise((r) => setImmediate(r));

  const [people, selected] = await app.getNames();
  assert.deepStrictEqual(people, ['Alice', 'Bob']);
  assert.deepStrictEqual(selected, []);
});

test('Application.getRandomPerson returns an indexed person based on Math.random', () => {
  const originalRandom = Math.random;
  try {
    const app = new Application();
    app.people = ['Alice', 'Bob', 'Charlie'];

    Math.random = () => 0.0; // index 0
    assert.strictEqual(app.getRandomPerson(), 'Alice');

    Math.random = () => 0.7; // 0.7 * 3 = 2.1 -> floor 2
    assert.strictEqual(app.getRandomPerson(), 'Charlie');
  } finally {
    Math.random = originalRandom;
  }
});

test('Application.selectNextPerson selects new person and avoids duplicates', () => {
  const app = new Application();
  app.people = ['Alice', 'Bob'];
  app.selected = [];


  let seq = ['Alice', 'Alice', 'Bob'];
  app.getRandomPerson = () => seq.shift() ?? 'Bob';

  const first = app.selectNextPerson();
  assert.strictEqual(first, 'Alice');
  assert.deepStrictEqual(app.selected, ['Alice']);

  // Duplicate on first try ('Alice'), then pick the other ('Bob') to run while-loop
  const second = app.selectNextPerson();
  assert.strictEqual(second, 'Bob');
  assert.deepStrictEqual(app.selected, ['Alice', 'Bob']);

  // When all selected, returns null
  const third = app.selectNextPerson();
  assert.strictEqual(third, null);
});

test('Application.notifySelected writes and sends for each selected', () => {
  const app = new Application();
  app.selected = ['Alice', 'Bob'];

  // Spy on write and send
  const calls = [];
  app.mailSystem = {
    write(name) {
      calls.push(['write', name]);
      return 'CTX ' + name;
    },
    send(name, ctx) {
      calls.push(['send', name, ctx]);
      return true;
    },
  };

  app.notifySelected();

  assert.deepStrictEqual(calls, [
    ['write', 'Alice'],
    ['send', 'Alice', 'CTX Alice'],
    ['write', 'Bob'],
    ['send', 'Bob', 'CTX Bob'],
  ]);
});

