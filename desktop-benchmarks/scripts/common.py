from pathlib import Path
import os,socket,json,re,urllib.request,urllib.error,datetime,hashlib
ROOT=Path(__file__).resolve().parents[1]
_KEYS={}
NAMES={'claude':'ANTHROPIC_API_KEY','openai':'OPENAI_API_KEY','sai':'SAI_API_KEY'}
def credential(agent):
 if agent in _KEYS:return _KEYS[agent]
 v=os.getenv(NAMES[agent]) or (os.getenv('SIMULAR_API_KEY') if agent=='sai' else None)
 if v:
  _KEYS[agent]=v;return v
 path=os.getenv('DESKTOP_BENCH_SECRET_SOCKET')
 if not path:return None
 s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
 try:
  s.connect(path);s.sendall(agent.encode());v=s.recv(16384).decode() or None;_KEYS[agent]=v;return v
 finally:s.close()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def redact(v):
 if isinstance(v,str):
  for a in NAMES:
   k=credential(a)
   if k:v=v.replace(k,'[REDACTED]')
  return re.sub(r'\b(?:sk-(?:proj-|ant-)?|sapi_|bu_|hf_)[A-Za-z0-9_-]{20,}','[REDACTED]',v).replace(str(ROOT.parent),'<PROJECT_ROOT>')
 if isinstance(v,list):return [redact(x) for x in v]
 if isinstance(v,dict):return {k:('[REDACTED]' if re.search(r'authorization|api.?key|cookie|access.?token|refresh.?token',k,re.I) else redact(x)) for k,x in v.items()}
 return v
def save(p,obj):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(redact(obj),indent=2,ensure_ascii=False)+'\n')
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):return None
def request(agent,path,payload=None,method=None,timeout=30,raw=None,extra=None):
 base={'openai':'https://api.openai.com','claude':'https://api.anthropic.com','sai':'https://api.simular.ai'}[agent]
 key=credential(agent)
 if not key:return {'http_status':None,'error':'credential_unavailable'}
 headers={'Accept':'application/json','User-Agent':'Manicule-desktop-benchmark/1'}
 if agent=='claude':headers.update({'x-api-key':key,'anthropic-version':'2023-06-01'})
 else:headers['Authorization']='Bearer '+key
 headers.update(extra or {})
 data=json.dumps(payload).encode() if payload is not None else raw
 if payload is not None:headers['Content-Type']='application/json'
 try:
  req=urllib.request.Request(base+path,data=data,headers=headers,method=method or ('POST' if data is not None else 'GET'))
  with urllib.request.build_opener(NoRedirect()).open(req,timeout=timeout) as r:status=r.status;body=r.read()
 except urllib.error.HTTPError as e:status=e.code;body=e.read()
 except Exception as e:return {'http_status':None,'error':type(e).__name__}
 try:value=json.loads(body)
 except ValueError:value={'non_json_bytes':len(body)}
 return {'http_status':status,'body':value}
def event(agent,kind,**data):
 p=ROOT/'logs'/agent/'events.jsonl';p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('a') as f:f.write(json.dumps(redact({'utc':now(),'event':kind,**data}),ensure_ascii=False)+'\n')
