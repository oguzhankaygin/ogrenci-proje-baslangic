import assert from 'node:assert/strict';
import { test } from 'node:test';

import { topla } from '../src/topla.js';

test('iki sayıyı toplar', () => {
  assert.equal(topla(2, 3), 5);
});
