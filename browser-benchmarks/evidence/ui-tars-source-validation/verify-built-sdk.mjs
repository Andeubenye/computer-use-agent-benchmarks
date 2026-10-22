import assert from 'node:assert/strict';
import { UITarsModel } from '../../work/UI-TARS-desktop-v0.2.4-2026-10-20/packages/ui-tars/sdk/dist/Model.mjs';
import { UITarsModelVersion } from '../../work/UI-TARS-desktop-v0.2.4-2026-10-20/packages/ui-tars/shared/dist/types/index.mjs';
let requests = 0;
const model = new UITarsModel({
  model: 'ByteDance-Seed/UI-TARS-1.5-7B',
  apiKey: 'test-key', // Existing unit-test placeholder; no real credential.
  baseURL: 'http://127.0.0.1:1/v1',
  fetch: async (url, options) => {
    // Fetch is replaced entirely. No socket or network request is made.
    requests++;
    assert.equal(String(url), 'http://127.0.0.1:1/v1/chat/completions');
    const body = JSON.parse(options.body);
    assert.equal(body.model, 'ByteDance-Seed/UI-TARS-1.5-7B');
    assert.equal(body.max_tokens, 2048);
    return new Response(JSON.stringify({
      id: 'offline-mock', object: 'chat.completion', created: 0,
      model: body.model,
      choices: [{index: 0, message: {role: 'assistant', content: 'Action: finished()'}, finish_reason: 'stop'}],
      usage: {prompt_tokens: 10, completion_tokens: 5, total_tokens: 15},
    }), {status: 200, headers: {'content-type': 'application/json'}});
  },
});
const result = await model.invoke({
  uiTarsVersion: UITarsModelVersion.V1_5,
  conversations: [{from: 'human', value: 'Finish'}], images: [],
  screenContext: {width: 1920, height: 1080},
});
assert.equal(requests, 1);
assert.equal(result.parsedPredictions[0].action_type, 'finished');
console.log('PASS: built ESM SDK uses Chat Completions, model identity preserved, max_tokens=2048, finished action parsed. Fetch mocked; no network I/O.');
