import base64, datetime, fcntl, json, os, re, threading, time, urllib.request, urllib.error
from pathlib import Path
from decimal import Decimal
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=ROOT/'outputs/manicule-benchmarks-tasks-2-5'
TASKS=json.loads((OUT/'preparation/tasks.json').read_text())
KEYS=json.loads((HERE/'private-credentials.json').read_text())
BASE={'tinyfish':'https://agent.tinyfish.ai','browser-use':'https://api.browser-use.com','sai':'https://api.simular.ai'}
LEDGER=OUT/'budget-ledger.json'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def redact(x):
 if isinstance(x,str):
  for k in KEYS.values():x=x.replace(k,'[REDACTED]')
  return re.sub(r'(?:sk-[A-Za-z0-9_-]{15,}|bu_[A-Za-z0-9_-]{15,}|sapi_[A-Za-z0-9_-]{15,})','[REDACTED]',x)
 if isinstance(x,list):return [redact(v) for v in x]
 if isinstance(x,dict):return {k:('[REDACTED]' if k.lower() in {'authorization','api_key','apikey','access_token','refresh_token'} else '[REDACTED CAPABILITY URL]' if any(z in k.lower() for z in ['streaming_url','liveurl','live_url','videourl','video_url','recordingurl','recording_url','cdpurl']) and v else redact(v)) for k,v in x.items()}
 return x
def save(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(redact(v),indent=2,ensure_ascii=False)+'\n')
def log(**v):print(json.dumps({'time':now(),**redact(v)}),flush=True)
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*a,**kw):return None
def api(agent,path,payload=None,method=None,timeout=25,binary=False):
 headers={'Accept':'application/json','User-Agent':'Manicule-benchmark/2'}
 if agent=='tinyfish':headers['X-API-Key']=KEYS[agent]
 elif agent=='browser-use':headers['X-Browser-Use-API-Key']=KEYS[agent]
 else:headers['Authorization']='Bearer '+KEYS[agent]
 data=json.dumps(payload).encode() if payload is not None else None
 if data:headers['Content-Type']='application/json'
 try:
  with urllib.request.build_opener(NoRedirect()).open(urllib.request.Request(BASE[agent]+path,data=data,headers=headers,method=method or ('POST' if data is not None else 'GET')),timeout=timeout) as r:code,raw=r.status,r.read()
 except urllib.error.HTTPError as e:code,raw=e.code,e.read()
 except Exception as e:return {'http_status':None,'transport_error':type(e).__name__}
 if binary:return {'http_status':code,'body':raw}
 try:body=json.loads(raw)
 except ValueError:body=raw.decode(errors='replace')[:1000]
 return {'http_status':code,'body':body}
def ledger(key,amount,finish=None):
 """Cross-process reservation includes uncertainty; never recycle uncertain spend."""
 with (HERE/'budget.lock').open('a+') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  d=json.loads(LEDGER.read_text()) if LEDGER.exists() else {'authorized_usd':10,'authorization':'User approved up to $10 additional provider usage across 20 runs including promotional credits; no purchases/top-ups','entries':{}}
  entries=d['entries'];total=sum(Decimal(str(v['charged_or_reserved_usd'])) for v in entries.values())
  if finish is None:
   if key in entries:return False,'already_reserved_or_attempted'
   if sum(v['state']=='active' for v in entries.values())>=3:return False,'concurrency'
   if total+Decimal(str(amount))>10:return False,'remaining_budget'
   entries[key]={'state':'active','reserved_usd':amount,'charged_or_reserved_usd':amount,'reserved_at':now()}
  else:
   entries[key].update(state='finished',charged_or_reserved_usd=amount,cost_basis=finish,finished_at=now())
  d['committed_or_reserved_usd']=float(sum(Decimal(str(v['charged_or_reserved_usd'])) for v in entries.values()));d['remaining_uncommitted_usd']=round(10-d['committed_or_reserved_usd'],8)
  save(LEDGER,d)
  return True,None
def claim(agent,task,reserve):
 folder=OUT/'runs'/agent/task;folder.mkdir(parents=True,exist_ok=True)
 key=agent+'/'+task
 while True:
  ok,why=ledger(key,reserve)
  if ok:break
  if why=='concurrency':time.sleep(2);continue
  save(folder/'run-record.json',{'agent':agent,'task':task,'status':'blocked','reason':why,'submitted':False,'attempts':0,'cost_usd':0});return None
 (folder/'task-prompt.txt').write_text(TASKS[task]['prompt'])
 save(folder/'configuration.json',{'agent':agent,'task':task,'max_seconds_from_submission':600,'automatic_benchmark_restarts':0,'reserved_usd':reserve,'prompt_sha256':TASKS[task]['prompt_sha256'],'expected_answers_provided':False})
 return folder
def image_data(x,folder,prefix='screenshot'):
 """Extract data-URI screenshots before saving raw provider JSON."""
 count=0
 def walk(v):
  nonlocal count
  if isinstance(v,str) and v.startswith('data:image/') and ';base64,' in v:
   typ,data=v.split(';base64,',1);ext='png' if 'png' in typ else 'jpg';p=folder/'screenshots'/f'{prefix}-{count:03d}.{ext}';p.parent.mkdir(exist_ok=True);p.write_bytes(base64.b64decode(data));count+=1;return {'saved_image':str(p.relative_to(folder))}
  if isinstance(v,dict):return {k:walk(z) for k,z in v.items()}
  if isinstance(v,list):return [walk(z) for z in v]
  return v
 return walk(x),count
