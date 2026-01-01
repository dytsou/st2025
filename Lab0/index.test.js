import assert from 'assert';
import secret from './index.js';
import { test } from 'node:test';

test('outputs the correct string', () => {
  assert.strictEqual(secret(), "SQLAB{YoU_6OT_TH3_SEcret_me$5a6e_F0r_La8_0}");
});