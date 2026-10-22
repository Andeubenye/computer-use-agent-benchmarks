// Independent post-run inspection only. Refuses to inspect a running task.
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const [dest,electronPid]=process.argv.slice(2);
if(!/\[GUIAgent\] Finally: status/.test(fs.readFileSync(path.join(dest,'execution-trace.txt'),'utf8')))throw new Error('Task is not terminal; verification refused');
const row=cp.execFileSync('ps',['-axo','pid=,ppid=,args='],{encoding:'utf8'}).split('\n').find(l=>l.trim().split(/\s+/)[1]===electronPid&&l.includes('/Google Chrome.app/Contents/MacOS/Google Chrome ')&&l.includes('puppeteer_dev_chrome_profile-'));
if(!row)throw new Error('No identified agent browser available');
const profile=row.match(/--user-data-dir=([^\s]+)/)[1];const [port,endpoint]=fs.readFileSync(path.join(profile,'DevToolsActivePort'),'utf8').trim().split('\n');
const ws=new WebSocket('ws://127.0.0.1:'+port+endpoint);let id=0;const pending=new Map();
const send=(method,params={},sessionId)=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params,...(sessionId&&{sessionId})}));});
ws.addEventListener('message',e=>{const m=JSON.parse(e.data),p=pending.get(m.id);if(p){pending.delete(m.id);m.error?p.reject(new Error(m.error.message)):p.resolve(m.result);}});
(async()=>{
 await new Promise((resolve,reject)=>{ws.addEventListener('open',resolve,{once:true});ws.addEventListener('error',reject,{once:true});});
 const {targetInfos}=await send('Target.getTargets');const target=targetInfos.filter(t=>t.type==='page'&&!/^(about:|chrome:)/.test(t.url)).at(-1);if(!target)throw new Error('No public task page');
 const {sessionId}=await send('Target.attachToTarget',{targetId:target.targetId,flatten:true});
 const state=await send('Runtime.evaluate',{expression:'JSON.stringify({url:location.href,title:document.title,text:document.body.innerText,fields:[...document.querySelectorAll("input,textarea,select")].map(e=>({tag:e.tagName,type:e.type,name:e.name,id:e.id,value:e.value,disabled:e.disabled,readOnly:e.readOnly,checked:e.checked,selectedText:e.tagName==="SELECT"?e.selectedOptions[0]?.text:null}))})',returnByValue:true},sessionId);
 const result={verified_after_agent_stopped:true,captured_at_utc:new Date().toISOString(),...JSON.parse(state.result.value)};
 fs.writeFileSync(path.join(dest,'independent-final-state.json'),JSON.stringify(result,null,2)+'\n');
 const shot=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false},sessionId);fs.writeFileSync(path.join(dest,'screenshots/independent-final.png'),Buffer.from(shot.data,'base64'));
 await send('Target.detachFromTarget',{sessionId});ws.close();console.log('Saved independent final page state and screenshot; no navigation or input performed.');
})().catch(e=>{ws.close();console.error(e.message);process.exitCode=1;});
setTimeout(()=>{if(ws.readyState!==WebSocket.CLOSED){ws.close();process.exitCode=1;}},10000).unref();
