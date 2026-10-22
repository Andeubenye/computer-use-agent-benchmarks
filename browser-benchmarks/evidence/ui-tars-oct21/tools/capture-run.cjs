// Evidence only: no navigation, input, evaluation, or task-solving calls.
const fs = require('node:fs');
const path = require('node:path');
const cp = require('node:child_process');
const [dest, mainLog, offsetArg, electronPid] = process.argv.slice(2);
const offset = JSON.parse(fs.readFileSync(path.join(dest,'submission.json'),'utf8')).log_offset;
let socket, nextId = 0, sessionId, lastCount = -1;
const pending = new Map();
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
const events = path.join(dest, 'screenshot-events.jsonl');
const record = value => fs.appendFileSync(events, JSON.stringify({utc: new Date().toISOString(), ...value})+'\n');
const send = (method, params = {}, session) => new Promise((resolve, reject) => {
  const id = ++nextId;
  const timer = setTimeout(() => { pending.delete(id); reject(new Error('local capture timeout')); }, 5000);
  pending.set(id, {resolve, reject, timer});
  socket.send(JSON.stringify({id, method, params, ...(session && {sessionId: session})}));
});
async function connect() {
  const rows = cp.execFileSync('ps', ['-axo', 'pid=,ppid=,args='], {encoding:'utf8'}).split('\n');
  const row = rows.find(line => {
    const parts = line.trim().split(/\s+/, 3);
    return parts[1] === electronPid && line.includes('/Google Chrome.app/Contents/MacOS/Google Chrome ') && line.includes('puppeteer_dev_chrome_profile-');
  });
  if (!row) return false;
  const profile = row.match(/--user-data-dir=([^\s]+)/)?.[1];
  if (!profile) return false;
  const active = fs.readFileSync(path.join(profile, 'DevToolsActivePort'), 'utf8').trim().split('\n');
  socket = new WebSocket('ws://127.0.0.1:'+active[0]+active[1]);
  await new Promise((resolve, reject) => {socket.addEventListener('open', resolve, {once:true});socket.addEventListener('error', reject, {once:true});});
  socket.addEventListener('message', event => {
    const m = JSON.parse(event.data); const p = pending.get(m.id);
    if (p) { clearTimeout(p.timer); pending.delete(m.id); m.error ? p.reject(new Error(m.error.message)) : p.resolve(m.result); }
  });
  record({event:'capture_connected',browser_pid:Number(row.trim().split(/\s+/)[0]),profile_basename:path.basename(profile),browser_version:(await send('Browser.getVersion')).product});
  return true;
}
(async () => {
  const deadline = Date.now()+605000;
  while (Date.now()<deadline) {
    const log = fs.readFileSync(mainLog).subarray(offset).toString();
    const count = (log.match(/\[GUIAgent\] Action:/g)||[]).length;
    const ended = /\[GUIAgent\] Finally: status/.test(log);
    try {
      if (!socket && !await connect()) {await sleep(500);continue;}
      if (count !== lastCount || ended) {
        const {targetInfos} = await send('Target.getTargets');
        const candidates = targetInfos.filter(t=>t.type==='page' && !t.url.startsWith('about:') && !t.url.startsWith('chrome:'));
        const target = candidates.at(-1);
        if (target) {
          const attached = await send('Target.attachToTarget', {targetId:target.targetId,flatten:true}); sessionId=attached.sessionId;
          const shot = await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false},sessionId);
          const name = String(count).padStart(3,'0')+(ended?'-terminal':'-action')+'.png';
          fs.writeFileSync(path.join(dest,'screenshots',name),Buffer.from(shot.data,'base64'));
          record({event:'screenshot',file:'screenshots/'+name,action_count_observed:count,page_url:target.url,terminal:ended});
          await send('Target.detachFromTarget',{sessionId});
          lastCount=count;
        }
      }
    } catch(e) { record({event:'capture_error',error:e.message}); }
    if (ended) break;
    await sleep(1000);
  }
  if(socket)socket.close(); // Disconnect evidence channel only; do not close Chrome.
  record({event:'capture_finished'});
})().catch(e=>{record({event:'capture_fatal',error:e.message});process.exitCode=1;});
