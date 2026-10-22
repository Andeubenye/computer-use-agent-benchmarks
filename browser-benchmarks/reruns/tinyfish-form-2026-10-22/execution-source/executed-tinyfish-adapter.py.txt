def submit_marker(folder,payload):
 with (folder/'submitted-once.json').open('x') as f:json.dump({'submitted_at':now(),'payload':payload},f)

def tiny(task):
 agent='tinyfish';reserve=2.4;f=claim(agent,task,reserve)
 if f is None:return True
 payload={'url':TASKS[task]['start_url'],'goal':TASKS[task]['prompt'],'browser_profile':'lite','use_profile':False,'use_vault':False,'agent_config':{'max_duration_seconds':600}}
 submit_marker(f,payload);start=time.monotonic();began=now();state={'run_id':None,'deadline':False};timer=None;final={};error=None;count=None
 def cancel():
  state['deadline']=True
  if state['run_id']:save(f/'cancel.json',api(agent,'/v1/runs/'+state['run_id']+'/cancel',{}))
 timer=threading.Timer(600,cancel);timer.daemon=True;timer.start()
 try:
  r=api(agent,'/v1/automation/run-async',payload,timeout=45);save(f/'submission.json',r)
  if r['http_status'] not in (200,201,202):error='submission_rejected_or_uncertain';return False
  b=r['body'];state['run_id']=b.get('run_id') or b.get('id') or (b.get('data') or {}).get('run_id')
  if not state['run_id']:error='missing_run_id';return False
  log(agent=agent,task=task,event='submitted',run_id=state['run_id'])
  polls=[]
  while time.monotonic()-start<600 and not state['deadline']:
   r=api(agent,'/v1/runs/'+state['run_id'],timeout=min(25,max(1,600-(time.monotonic()-start))))
   if r['http_status']!=200:error='run_read_failed';save(f/'read-error.json',r);cancel();break
   final=r['body'].get('data',r['body']);status=str(final.get('status','')).lower()
   polls.append({'at':now(),'elapsed_seconds':time.monotonic()-start,'status':status,'num_of_steps':final.get('num_of_steps')});save(f/'polls.json',polls)
   if status in {'completed','failed','cancelled','canceled','timed_out','timeout','success','succeeded'}:break
   time.sleep(min(4,max(0,600-(time.monotonic()-start))))
  elapsed=time.monotonic()-start;timer.cancel()
  if state['deadline'] or elapsed>=600:cancel();error='600_second_deadline'
  r=api(agent,'/v1/runs/'+state['run_id']+'?screenshots=base64');raw=r.get('body',{});final=raw.get('data',raw) if isinstance(raw,dict) else final
  raw,ss=image_data(final,f);save(f/'provider-run.json',raw)
  count=final.get('num_of_steps');count=count if isinstance(count,(int,float)) else None
  ans=final.get('result');(f/'original-response.txt').write_text(redact(ans if isinstance(ans,str) else json.dumps(ans,ensure_ascii=False,indent=2)))
  cost=round(count*.016,8) if count is not None else reserve
  save(f/'run-record.json',{'agent':agent,'task':task,'submitted':True,'status':final.get('status','unknown'),'client_error':error,'started_at':began,'agent_wall_seconds':elapsed,'max_seconds_from_submission':600,'deadline_fired':state['deadline'],'run_id':state['run_id'],'actions':count,'action_unit':'provider steps','screenshots':ss,'model':None,'model_limitation':'Revision not exposed','cost_usd':cost if count is not None else None,'cost_basis':'published $0.016 per reported step; not invoice','automatic_restarts':0,'fresh_profile_requested':True,'internal_retries':None})
  ledger(agent+'/'+task,cost,'TinyFish steps × published rate' if count is not None else 'uncertain: full reservation retained')
  log(agent=agent,task=task,event='finished',status=final.get('status'),cost=cost)
  return not state['deadline'] or bool(final.get('finished_at'))
 finally:
  timer.cancel()
  if error and not (f/'run-record.json').exists():
   save(f/'run-record.json',{'agent':agent,'task':task,'status':'failed_submission','submitted':True,'reason':error,'cost_usd':None,'reserved_uncertain_usd':reserve,'automatic_restarts':0});ledger(agent+'/'+task,reserve,'uncertain submission; full reservation retained')
