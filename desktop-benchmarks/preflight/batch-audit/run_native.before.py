"""Native computer tools only. Docker translates model actions; never chooses edits."""
import argparse,base64,json,math,subprocess,time,threading,hashlib,sys
from pathlib import Path
from common import ROOT,credential,request,save,event,now
DOCKER=['docker','--context','colima-claude-benchmark']
REMOTE='/home/agent/Desktop/benchmark'
PROMPT=(ROOT/'inputs/task-prompt.txt').read_text()
SYSTEM=f'''You control an isolated Linux desktop at 1024 x 768 pixels. LibreOffice Calc is open with a blank spreadsheet. The benchmark folder is {REMOTE}; its only task file is orders_to_fix.csv. Use only the native computer tool for all task work. No web browser, terminal, code, scripts, shell, filesystem or programmatic spreadsheet tools. Do not type code or formulas to perform file editing. Open, inspect, edit, save and reopen using the spreadsheet GUI. End each batch with a screenshot and use it to observe the result before proceeding. Do not inspect unrelated files, sign in, change settings, install software or access the network. The expected-output file and grader references are not available to you. If blocked, stop and describe the blocker. You have 10 minutes from task submission.'''
MODELS={'claude':'claude-sonnet-5-5','openai':'gpt-6.1-sol'}

def require_unpaused():
 if (ROOT/'preflight/user-pause.json').exists():
  raise RuntimeError('Benchmark paused: exposed keys must be rotated and securely configured before any provider requests. No automatic resume.')

def docker(*args,data=None,timeout=30):
 return subprocess.run(DOCKER+list(args),input=data,capture_output=True,check=True,timeout=timeout).stdout

def setup(agent):
 name='manicule-desktop-'+agent+'-20261021'
 # Never replace/restart an existing run/container.
 if subprocess.run(DOCKER+['inspect',name],capture_output=True).returncode==0:raise RuntimeError('Container already exists; refuse restart')
 docker('run','--detach','--name',name,'--network','none','--init','--cap-drop','ALL','--security-opt','no-new-privileges','--memory','2g','--cpus','2','--pids-limit','256','--shm-size','256m','--label','app=manicule-desktop-csv','desktop-csv-benchmark:2026-10-21')
 for _ in range(40):
  try:
   ids=docker('exec',name,'xdotool','search','--name','LibreOffice Calc').decode().splitlines()
   if ids:break
  except subprocess.SubprocessError:pass
  time.sleep(.5)
 else:raise RuntimeError('Calc startup failed')
 docker('exec',name,'xdotool','windowsize',ids[0],'1024','740')
 docker('exec',name,'xdotool','windowmove',ids[0],'0','0')
 docker('exec','-i',name,'python','-c',"import sys;from pathlib import Path;p=Path('/home/agent/Desktop/benchmark/orders_to_fix.csv');p.write_bytes(sys.stdin.buffer.read())",data=(ROOT/'inputs/orders_to_fix.csv').read_bytes())
 return name

class Runner:
 def __init__(self,agent,attempt=1,seconds=600,budget=2.5):
  self.agent=agent;self.tag=agent if attempt==1 else agent+'-attempt-'+str(attempt);self.limit=seconds;self.budget=budget;self.folder=ROOT/'logs'/self.tag;self.pics=ROOT/'screenshots'/self.tag
  self.folder.mkdir(parents=True,exist_ok=True);self.pics.mkdir(parents=True,exist_ok=True)
  if (self.folder/'run-record.json').exists() or (self.folder/'submitted-once.json').exists():raise RuntimeError('Existing run evidence: no automatic restart')
  self.start=None;self.actions=0;self.requests=0;self.count_requests=0;self.nshots=0;self.cost=0.;self.uncertain=0.;self.usages=[];self.errors=[];self.final='';self.reason='';self.name=None;self.watchdog=False
 def remaining(self):return max(.01,self.limit-(time.monotonic()-self.start))
 def screenshot(self,contents,tag):
  result=[]
  for b in contents:
   if b.get('type')=='image':
    self.nshots+=1;path=self.pics/f'{self.nshots:03d}-{tag}.png';path.write_bytes(base64.b64decode(b['source']['data']));result.append(str(path.relative_to(ROOT)))
  return result
 def native(self,name,args):
  if self.watchdog or self.remaining()<.1:raise TimeoutError('Task deadline')
  r=json.loads(docker('exec','-i',self.name,'python','/opt/desktop/action.py',data=json.dumps({'name':name,'input':args}).encode(),timeout=min(20,self.remaining())))
  images=self.screenshot(r.get('content',[]) if isinstance(r.get('content'),list) else [],name)
  event(self.tag,'native_action',index=self.actions,name=name,arguments=args,is_error=r.get('is_error',False),screenshots=images)
  return r
 def rawshot(self,tag):
  r=self.native('screenshot',{});b=r['content'][0]['source']['data'];return b
 def api(self,path,body,kind):
  require_unpaused()
  if self.watchdog or self.remaining()<.1:raise TimeoutError('Task deadline')
  r=request(self.agent,path,body,timeout=min(60,self.remaining()))
  event(self.tag,kind,http_status=r.get('http_status'),transport_error=r.get('error'))
  if r.get('http_status')!=200:
   save(self.folder/f'{kind}-error.json',r);raise RuntimeError(kind+' HTTP '+str(r.get('http_status'))+' '+str(r.get('error','')))
  return r['body']
 def count_and_reserve(self,body):
  self.count_requests+=1
  if self.agent=='claude':x=self.api('/v1/messages/count_tokens',{k:v for k,v in body.items() if k!='max_tokens'},'count');n=x['input_tokens']
  else:x=self.api('/v1/responses/input_tokens',{k:v for k,v in body.items() if k not in ['max_output_tokens','service_tier']},'count');n=x['input_tokens']
  # No caching is explicitly enabled. Use a conservative cache-write input rate plus 20% and 4096-token margin.
  reserve=((n*1.2+4096)*2.5+2048*10)/1e6
  if n>100000:raise RuntimeError('Input context guard')
  if self.cost+self.uncertain+reserve>self.budget:raise RuntimeError('Next-request budget guard; generation not sent')
  event(self.tag,'request_reservation',input_tokens=n,reserved_usd=reserve,spent_estimate_usd=self.cost)
  self.uncertain=reserve
 def generation(self,body):
  self.count_and_reserve(body)
  if not (self.folder/'submitted-once.json').exists():save(self.folder/'submitted-once.json',{'first_generation_at':now(),'model':MODELS[self.agent],'automatic_restarts':0,'exact_prompt_sha256':hashlib.sha256(PROMPT.encode()).hexdigest()})
  self.requests+=1
  x=self.api('/v1/messages' if self.agent=='claude' else '/v1/responses',body,'generation')
  save(self.folder/'responses'/f'{self.requests:03d}.json',x)
  u=x.get('usage')
  if not u:raise RuntimeError('Missing usage; preserve request reservation')
  if self.agent=='claude':cost=(u.get('input_tokens',0)*2+u.get('output_tokens',0)*10+u.get('cache_creation_input_tokens',0)*4+u.get('cache_read_input_tokens',0)*.1)/1e6
  else:
   details=u.get('input_tokens_details') or {};cached=details.get('cached_tokens',0);write=details.get('cache_write_tokens',0)
   cost=((u.get('input_tokens',0)-cached-write)*2+cached*.1+write*2.5+u.get('output_tokens',0)*10)/1e6
  if cost>self.uncertain:raise RuntimeError('Observed charge exceeded reservation; stop')
  self.cost+=cost;self.uncertain=0;self.usages.append(u)
  event(self.tag,'model_response',number=self.requests,returned_model=x.get('model'),usage=u,cost_estimate_usd=cost)
  return x
 def deadline(self):
  self.watchdog=True;event(self.tag,'deadline_fired',seconds=self.limit)
  if self.name:
   subprocess.run(DOCKER+['stop','-t','2',self.name],capture_output=True,timeout=15)
 def run_claude(self,shot):
  messages=[{'role':'user','content':[{'type':'text','text':PROMPT},{'type':'image','source':{'type':'base64','media_type':'image/png','data':shot}}]}]
  for _ in range(50):
   x=self.generation({'model':MODELS[self.agent],'system':SYSTEM,'tools':[{'type':'computer_toolset_20260801'}],'messages':messages,'max_tokens':2048})
   blocks=x.get('content',[]);messages.append({'role':'assistant','content':blocks});texts=[b.get('text','') for b in blocks if b['type']=='text']
   if texts:self.final='\n'.join(texts);(self.folder/'original-response.txt').write_text(self.final)
   calls=[b for b in blocks if b['type']=='tool_use']
   if not calls:
    self.reason='model_finished';return
   outputs=[]
   for b in calls:
    self.actions+=1
    if self.actions>250:raise RuntimeError('Action limit')
    if b.get('toolset_name')!='computer':raise RuntimeError('Non-computer tool requested')
    result=self.native(b['name'],b.get('input',{}));content=result.get('content','')
    outputs.append({'type':'tool_result','tool_use_id':b['id'],'toolset_name':b['toolset_name'],'is_error':result.get('is_error',False),'content':content if content else 'Action executed.'})
   messages.append({'role':'user','content':outputs})
  raise RuntimeError('Model turn limit')
 def openai_action(self,a):
  typ=a['type']
  if typ=='screenshot':return self.native('screenshot',{})
  if typ=='type':return self.native('type',{'text':a['text']})
  if typ=='keypress':
   aliases={'CTRL':'ctrl','CONTROL':'ctrl','SHIFT':'shift','ALT':'alt','ENTER':'Return','RETURN':'Return','ESC':'Escape','ESCAPE':'Escape','BACKSPACE':'BackSpace','DELETE':'Delete','SPACE':'space','ARROWUP':'Up','ARROWDOWN':'Down','ARROWLEFT':'Left','ARROWRIGHT':'Right','TAB':'Tab','HOME':'Home','END':'End','PAGEUP':'Prior','PAGEDOWN':'Next','META':'super','SUPER':'super'}
   return self.native('key',{'text':'+'.join(aliases.get(k.upper(),k) for k in a['keys'])})
  if typ in ['click','double_click','move']:
   name='mouse_move' if typ=='move' else 'double_click' if typ=='double_click' else {'left':'left_click','right':'right_click','middle':'middle_click','wheel':'middle_click'}.get(a.get('button','left'))
   if not name:raise RuntimeError('Unsupported button')
   return self.native(name,{'coordinate':[a['x'],a['y']]})
  if typ=='scroll':
   results=[]
   for axis,plus,minus in [('scroll_y','down','up'),('scroll_x','right','left')]:
    v=a.get(axis,0)
    if v:results.append(self.native('scroll',{'coordinate':[a['x'],a['y']],'scroll_direction':plus if v>0 else minus,'scroll_amount':min(100,max(1,math.ceil(abs(v)/100)))}))
   return results
  if typ=='wait':return self.native('wait',{'duration':min(1,self.remaining())})
  if typ=='drag':
   path=a['path'];self.native('mouse_move',{'coordinate':[path[0]['x'],path[0]['y']]});self.native('left_mouse_down',{})
   try:
    for p in path[1:]:self.native('mouse_move',{'coordinate':[p['x'],p['y']]})
   finally:self.native('left_mouse_up',{})
   return
  raise RuntimeError('Unsupported native action: '+typ)
 def run_openai(self,shot):
  body={'model':MODELS[self.agent],'tools':[{'type':'computer'}],'instructions':SYSTEM,'input':[{'role':'user','content':[{'type':'input_text','text':PROMPT},{'type':'input_image','image_url':'data:image/png;base64,'+shot}]}],'max_output_tokens':2048,'service_tier':'default'}
  for _ in range(50):
   x=self.generation(body);outs=x.get('output',[])
   texts=[c.get('text','') for b in outs if b.get('type')=='message' for c in b.get('content',[]) if c.get('type')=='output_text']
   if texts:self.final='\n'.join(texts);(self.folder/'original-response.txt').write_text(self.final)
   if x.get('status')!='completed':raise RuntimeError('Incomplete model response: '+str(x.get('status')))
   calls=[b for b in outs if b.get('type')=='computer_call']
   if not calls:self.reason='model_finished';return
   returns=[]
   for c in calls:
    if c.get('pending_safety_checks'):raise RuntimeError('Provider safety approval required; not bypassed')
    for a in c.get('actions',[]) or ([c['action']] if c.get('action') else []):
     self.actions+=1
     if self.actions>250:raise RuntimeError('Action limit')
     event(self.tag,'provider_action',index=self.actions,action=a);self.openai_action(a)
    shot=self.rawshot('computer-call-output')
    returns.append({'type':'computer_call_output','call_id':c['call_id'],'output':{'type':'computer_screenshot','image_url':'data:image/png;base64,'+shot,'detail':'original'}})
   body={'model':MODELS[self.agent],'tools':[{'type':'computer'}],'instructions':SYSTEM,'previous_response_id':x['id'],'input':returns,'max_output_tokens':2048,'service_tier':'default'}
  raise RuntimeError('Model turn limit')
 def run(self):
  require_unpaused()
  if not credential(self.agent):raise RuntimeError('Missing credential')
  timer=None
  try:
   self.name=setup(self.tag)
   save(self.folder/'configuration.json',{'model':MODELS[self.agent],'system':SYSTEM,'prompt':PROMPT,'task_timeout_seconds':self.limit,'budget_usd':self.budget,'output_token_cap':2048,'api_retries':0,'computer_tool':'computer_toolset_20260801' if self.agent=='claude' else 'computer','execution_environment':'Linux / LibreOffice Calc / Xvfb 1024x768 / network none','expected_output_exposed':False})
   self.start=time.monotonic();timer=threading.Timer(self.limit,self.deadline);timer.daemon=True;timer.start();shot=self.rawshot('initial')
   event(self.tag,'task_start',prompt_sha256=hashlib.sha256(PROMPT.encode()).hexdigest())
   (self.run_claude if self.agent=='claude' else self.run_openai)(shot)
  except Exception as e:
   self.reason='infrastructure_or_protocol_error' if self.requests==0 else 'execution_error';self.errors.append(str(e));event(self.tag,'error',category=type(e).__name__,detail=str(e))
  finally:
   duration=time.monotonic()-self.start if self.start else 0
   if timer:timer.cancel()
   if self.name:
    try:
     if not self.watchdog:self.rawshot('independent-final')
    except Exception as e:event(self.tag,'final_screenshot_error',error=type(e).__name__)
    # Grader-only file retrieval AFTER the timed model/GUI loop; no edits or reopening.
    out=ROOT/'outputs'/self.agent;out.mkdir(parents=True,exist_ok=True)
    for filename in ['orders_to_fix.csv','orders_corrected.csv']:
     r=subprocess.run(DOCKER+['cp',self.name+':'+REMOTE+'/'+filename,str(out/filename)],capture_output=True)
     event(self.tag,'post_run_file_collection',file=filename,retrieved=r.returncode==0)
    docker('stop','-t','2',self.name)
   save(self.folder/'run-record.json',{'agent':self.agent,'submitted':self.requests>0,'model_requested':MODELS[self.agent],'reason':self.reason,'errors':self.errors,'duration_seconds':duration,'actions':self.actions,'action_unit':'native computer-tool actions; includes screenshot/zoom when requested','model_requests':self.requests,'token_count_requests':self.count_requests,'screenshots_saved':self.nshots,'usage':self.usages,'estimated_api_cost_usd':self.cost,'uncertain_cost_reserved_usd':self.uncertain,'api_retries':0,'automatic_restarts':0,'watchdog_fired':self.watchdog,'complete_final_response_file':'original-response.txt' if self.final else None,'container_stopped':bool(self.name),'original_response_is_unverified':True})
   print(json.dumps({'agent':self.agent,'reason':self.reason,'model_requests':self.requests,'seconds':round(duration,2),'cost_estimate_usd':self.cost,'uncertain_reserved_usd':self.uncertain,'actions':self.actions,'errors':self.errors}))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('agent',choices=['claude','openai']);p.add_argument('--attempt',type=int,default=1);p.add_argument('--seconds',type=float,default=600);p.add_argument('--budget',type=float,default=2.5);a=p.parse_args();assert 0<a.seconds<=600 and 0<a.budget<=2.5;Runner(a.agent,a.attempt,a.seconds,a.budget).run()
