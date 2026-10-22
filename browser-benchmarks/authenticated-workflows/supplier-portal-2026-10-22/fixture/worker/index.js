const USERNAME = 'benchmark-buyer';
const esc = v => String(v ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const sha = async s => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s))),b=>b.toString(16).padStart(2,'0')).join('');
const now = () => new Date().toISOString();
const random = () => Array.from(crypto.getRandomValues(new Uint8Array(32)),b=>b.toString(16).padStart(2,'0')).join('');
const headers = {'Content-Type':'text/html; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'same-origin','Content-Security-Policy':"default-src 'self'; style-src 'unsafe-inline'; img-src 'self' data:; form-action 'self'; frame-ancestors 'none'; base-uri 'none'"};
const page = (title,body,status=200,extra={}) => new Response(`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)} — Supplier Review Lab</title><style>*{box-sizing:border-box}body{margin:0;background:#f3f5f7;color:#202b38;font:17px/1.5 system-ui,sans-serif}header{background:#173c43;color:white;padding:18px 32px}header b{font-size:22px}header span{float:right;font-size:14px}main{max-width:980px;margin:28px auto;padding:0 24px}h1{font-size:29px;line-height:1.2;margin-bottom:8px}.muted{color:#526575}.card{background:white;border:1px solid #d3dde4;border-radius:10px;padding:24px;margin:20px 0}label{display:block;font-weight:650;margin:18px 0 6px}input,select,textarea{display:block;width:100%;font:inherit;padding:11px;border:1px solid #708698;border-radius:5px;background:white}textarea{min-height:118px}button,.button{display:inline-block;background:#176b61;color:white;border:0;padding:12px 20px;margin:16px 0 0;border-radius:5px;font:inherit;font-weight:650;text-decoration:none;cursor:pointer}a{color:#145e75}table{width:100%;border-collapse:collapse}th,td{text-align:left;padding:12px;border-bottom:1px solid #dbe3e8}th{font-size:14px;color:#526575}.pill{background:#e9f2ef;color:#214d45;padding:4px 9px;border-radius:5px;font-size:14px}.notice{background:#e8f3ed;border-left:5px solid #257c56;padding:14px 18px;overflow-wrap:anywhere}.warning{background:#fff0dc;padding:14px;border-left:4px solid #bf7e1f}code{font-size:17px}.columns{display:grid;grid-template-columns:1fr 1fr;gap:20px}@media(max-width:650px){.columns{grid-template-columns:1fr}header span{float:none;display:block}table{font-size:14px}}</style></head><body><header><b>Supplier Review Lab</b><span>Synthetic benchmark portal · No real supplier data</span></header><main>${body}</main></body></html>`,{status,headers:{...headers,...extra}});
const json = (data,status=200) => new Response(JSON.stringify(data),{status,headers:{'Content-Type':'application/json','Cache-Control':'no-store'}});
const redirect = (location,extra={}) => new Response(null,{status:303,headers:{Location:location,'Cache-Control':'no-store',...extra}});
async function event(env,kind,record,session,details={}){await env.DB.prepare('INSERT INTO audit_events(event_id,at,kind,record_id,session_hash,details) VALUES(?,?,?,?,?,?)').bind(crypto.randomUUID(),now(),kind,record,session,JSON.stringify(details)).run();}
async function auth(request,env){const token=(request.headers.get('Cookie')||'').split(';').map(x=>x.trim()).find(x=>x.startsWith('__Host-supplier_session='))?.slice('__Host-supplier_session='.length);if(!token||!/^[a-f0-9]{64}$/.test(token))return null;const hash=await sha(token);const row=await env.DB.prepare('SELECT * FROM sessions WHERE token_hash=? AND revoked=0 AND expires_at>?').bind(hash,now()).first();return row?{...row,raw:token}:null;}
const loginPage = msg => page('Sign in',`<h1>Sign in to supplier review</h1><p class="muted">Dedicated synthetic test account only. Do not enter personal credentials.</p>${msg?`<p class="warning" role="alert">${esc(msg)}</p>`:''}<form class="card" method="post" action="/login"><label for="username">Username</label><input id="username" name="username" autocomplete="username" required><label for="password">Password</label><input id="password" name="password" type="password" autocomplete="current-password" required><button type="submit">Sign in</button></form>`);
async function admin(request,env,url){if(!env.FIXTURE_ADMIN_KEY||request.headers.get('Authorization')!=='Bearer '+env.FIXTURE_ADMIN_KEY)return json({error:'Unauthorized'},401);
 if(request.method==='POST'){
  let body;try{body=await request.json();}catch{return json({error:'Invalid JSON'},400);}
  if(url.pathname==='/__fixture/seed'){
   if(!Array.isArray(body.records)||body.records.length>50)return json({error:'Bounded records array required'},400);
   const statements=[];
   for(const r of body.records){if(!/^SUP-[CT][0-9]{3}$/.test(r.id)||!/^auth-[a-z0-9-]+$/.test(r.batch_id)||!Number.isInteger(r.pair_index)||!['tinyfish','claude'].includes(r.cohort))return json({error:'Invalid synthetic record'},400);statements.push(env.DB.prepare('INSERT INTO suppliers(id,batch_id,pair_index,cohort,name,status,notes) VALUES(?,?,?,?,?,?,?)').bind(r.id,r.batch_id,r.pair_index,r.cohort,'Synthetic Supplier '+String(r.pair_index).padStart(2,'0'),'Pending',''));}
   await env.DB.batch(statements);await event(env,'seed',null,null,{records:body.records.length,batch_id:body.records[0]?.batch_id});return json({created:body.records.length});
  }
  if(url.pathname==='/__fixture/cleanup-qa'){await env.DB.prepare("DELETE FROM suppliers WHERE batch_id='auth-qa' AND pair_index=999").run();await event(env,'qa_cleanup',null,null);return json({cleaned:true});}
  if(url.pathname==='/__fixture/reset'){
   if(!/^SUP-[CT][0-9]{3}$/.test(body.record_id))return json({error:'Invalid record'},400);
   await env.DB.prepare("UPDATE suppliers SET status='Pending',notes='',version=0,confirmation_id=NULL,updated_at=NULL,updated_session_hash=NULL WHERE id=?").bind(body.record_id).run();await event(env,'admin_reset',body.record_id,null);return json({reset:body.record_id});
  }
  if(url.pathname==='/__fixture/expire'){
   if(typeof body.session_hash!=='string'||!/^[a-f0-9]{64}$/.test(body.session_hash))return json({error:'Exact session hash required'},400);
   await env.DB.prepare('UPDATE sessions SET revoked=1 WHERE token_hash=?').bind(body.session_hash).run();await event(env,'admin_expire',null,body.session_hash);return json({expired:true});
  }
 }
 if(request.method==='GET'){
  if(url.pathname.startsWith('/__fixture/verify/')){const id=decodeURIComponent(url.pathname.slice('/__fixture/verify/'.length));const record=await env.DB.prepare('SELECT * FROM suppliers WHERE id=?').bind(id).first();const audit=await env.DB.prepare('SELECT * FROM audit_events WHERE record_id=? ORDER BY at,event_id').bind(id).all();return json({record,audit:audit.results,server_time:now()});}
  if(url.pathname==='/__fixture/audit'){const a=await env.DB.prepare('SELECT * FROM audit_events ORDER BY at,event_id').all();return json({events:a.results,server_time:now()});}
  if(url.pathname==='/__fixture/sessions'){const a=await env.DB.prepare('SELECT token_hash,username,created_at,expires_at,revoked FROM sessions ORDER BY created_at').all();return json({sessions:a.results});}
 }
 return json({error:'Not found'},404);
}
export default {async fetch(request,env){
 const url=new URL(request.url);
 try{
  if(url.pathname==='/health')return json({ok:true,fixture:'supplier-auth-v1',database:!!env.DB,secrets_configured:!!(env.FIXTURE_PASSWORD_SHA256&&env.FIXTURE_ADMIN_KEY)});
  if(!env.DB||!env.FIXTURE_PASSWORD_SHA256||!env.FIXTURE_ADMIN_KEY)return page('Unavailable','<h1>Fixture setup incomplete</h1>',503);
  if(url.pathname.startsWith('/__fixture/'))return admin(request,env,url);
  if(url.pathname==='/login'&&request.method==='GET')return loginPage(url.searchParams.get('expired')?'Your session has expired. Sign in again.':'');
  if(url.pathname==='/login'&&request.method==='POST'){
   if(request.headers.get('Origin')!==url.origin)return page('Denied','<h1>Origin check failed</h1>',403);
   const f=await request.formData();const valid=f.get('username')===USERNAME&&await sha(String(f.get('password')||''))===env.FIXTURE_PASSWORD_SHA256;
   if(!valid){await event(env,'login_failed',null,null);return loginPage('Username or password not recognised.');}
   const token=random(),hash=await sha(token),created=now(),expires=new Date(Date.now()+2*60*60*1000).toISOString();await env.DB.prepare('INSERT INTO sessions(token_hash,username,created_at,expires_at) VALUES(?,?,?,?)').bind(hash,USERNAME,created,expires).run();await event(env,'login_ok',null,hash);return redirect('/dashboard',{'Set-Cookie':`__Host-supplier_session=${token}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=7200`});
  }
  if(url.pathname==='/'||url.pathname==='/dashboard'||url.pathname.startsWith('/supplier/')){
   const s=await auth(request,env);if(!s)return redirect('/login?expired=1');
   await event(env,'authenticated_view',url.pathname.startsWith('/supplier/')?decodeURIComponent(url.pathname.slice(10)):null,s.token_hash,{path:url.pathname});
   if(url.pathname==='/'||url.pathname==='/dashboard'){
    const q=(url.searchParams.get('q')||'').trim().slice(0,50);const statement=q?env.DB.prepare('SELECT id,name,status,pair_index,cohort FROM suppliers WHERE id LIKE ? ORDER BY pair_index,cohort').bind('%'+q+'%'):env.DB.prepare('SELECT id,name,status,pair_index,cohort FROM suppliers ORDER BY pair_index,cohort');const rows=(await statement.all()).results;
    return page('Dashboard',`<h1>Supplier dashboard</h1><p class="muted">Signed in as Benchmark Buyer <span class="pill">Authenticated</span></p><form class="card" method="get" action="/dashboard"><label for="q">Find supplier by record ID</label><input id="q" name="q" value="${esc(q)}" placeholder="e.g. SUP-T001"><button type="submit">Search suppliers</button></form><div class="card"><h2>Supplier records</h2><table><thead><tr><th>Record ID</th><th>Supplier</th><th>Status</th><th>Action</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${esc(r.id)}</td><td>${esc(r.name)}</td><td>${esc(r.status)}</td><td><a href="/supplier/${encodeURIComponent(r.id)}">Open ${esc(r.id)}</a></td></tr>`).join('')}</tbody></table>${rows.length?'':'<p>No suppliers found.</p>'}</div>`);
   }
   const id=decodeURIComponent(url.pathname.slice(10));const r=await env.DB.prepare('SELECT * FROM suppliers WHERE id=?').bind(id).first();if(!r)return page('Not found','<h1>Supplier not found</h1>',404);
   if(request.method==='POST'){
    if(request.headers.get('Origin')!==url.origin)return page('Denied','<h1>Origin check failed</h1>',403);
    const f=await request.formData();if(f.get('csrf')!==await sha('csrf|'+s.raw+'|'+id))return page('Denied','<h1>Invalid form token</h1>',403);
    const status=String(f.get('status')||''),notes=String(f.get('notes')||'');const version=Number(f.get('version'));if(!['Pending','Reviewed','On hold'].includes(status)||notes.length>500||!Number.isInteger(version))return page('Invalid','<h1>Invalid fields</h1>',400);
    const conf='CNF-'+crypto.randomUUID().replaceAll('-','').slice(0,16).toUpperCase(),at=now();const result=await env.DB.batch([env.DB.prepare('UPDATE suppliers SET status=?,notes=?,version=version+1,confirmation_id=?,updated_at=?,updated_session_hash=? WHERE id=? AND version=?').bind(status,notes,conf,at,s.token_hash,id,version),env.DB.prepare('INSERT INTO audit_events(event_id,at,kind,record_id,session_hash,details) SELECT ?,?,?,?,?,? FROM suppliers WHERE id=? AND confirmation_id=?').bind(crypto.randomUUID(),at,'supplier_saved',id,s.token_hash,JSON.stringify({confirmation_id:conf,from_status:r.status,to_status:status,notes_sha256:await sha(notes),version:version+1}),id,conf)]);
    if(result[0].meta.changes!==1)return page('Conflict','<h1>This record changed. Reload before editing.</h1>',409);
    return redirect('/supplier/'+encodeURIComponent(id)+'?saved='+encodeURIComponent(conf));
   }
   const saved=url.searchParams.get('saved');return page('Supplier '+id,`<p><a href="/dashboard">← Supplier dashboard</a></p><h1>Supplier record ${esc(id)}</h1><p class="muted">${esc(r.name)}</p>${saved&&saved===r.confirmation_id?`<div class="notice" role="status"><b>Changes saved successfully.</b><br>Confirmation ID: <code id="confirmation">${esc(r.confirmation_id)}</code></div>`:''}<section class="card"><h2>Current saved record</h2><p><b>Record ID:</b> ${esc(r.id)}</p><p><b>Saved status:</b> <span id="saved-status">${esc(r.status)}</span></p><p><b>Saved notes:</b> <span id="saved-notes">${esc(r.notes)||'(none)'}</span></p><p><b>Last confirmation ID:</b> <code>${esc(r.confirmation_id)||'(not saved yet)'}</code></p></section><form class="card" method="post" action="/supplier/${encodeURIComponent(id)}"><h2>Edit supplier</h2><input type="hidden" name="csrf" value="${await sha('csrf|'+s.raw+'|'+id)}"><input type="hidden" name="version" value="${r.version}"><label for="status">Supplier status</label><select id="status" name="status">${['Pending','Reviewed','On hold'].map(x=>`<option${x===r.status?' selected':''}>${esc(x)}</option>`).join('')}</select><label for="notes">Review notes</label><textarea id="notes" name="notes" maxlength="500">${esc(r.notes)}</textarea><button type="submit">Save changes</button></form>`);
  }
  return page('Not found','<h1>Page not found</h1>',404);
 }catch(error){console.error('Fixture request failure:',error?.name||'Error');return page('Unavailable','<h1>Fixture temporarily unavailable</h1><p>No completion should be inferred from this error.</p>',500);}
}};
