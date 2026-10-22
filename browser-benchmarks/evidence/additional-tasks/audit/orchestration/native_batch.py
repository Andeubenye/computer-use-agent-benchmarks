"""Reuse original native tools/executors; isolated batch adapters, zero request retries."""
import argparse, asyncio, importlib.util, json, logging, os, subprocess, sys, time, types
from decimal import Decimal
from pathlib import Path
from common import *

CLAUDE=Path('<LOCAL_HOME>/Documents/Codex/2026-10-17/set-up-a-working-benchmark-for/outputs/claude-computer-benchmark')
OPENAI=Path('<LOCAL_HOME>/Documents/Codex/2026-10-16/i-want-to-benchmark-openai-s/outputs')
logging.disable(logging.CRITICAL)

def claude_task(task):
 agent='claude';reserve=.8;f=claim(agent,task,reserve)
 if f is None:return True
 sys.path.insert(0,str(CLAUDE));os.environ['DOCKER_CONTEXT']='colima-claude-benchmark'
 import anthropic
 from benchmark import core,desktop
 core.SYSTEM=core.SYSTEM.replace("user's read-only public-web task", "user's public-web or synthetic benchmark task")
 started=False;rec=None;row=None;submitted=False
 try:
  # Only the benchmark-owned container; do not rebuild an image or alter original files.
  try:desktop.stop()
  except subprocess.CalledProcessError:pass
  desktop.start();started=True;d=desktop.Desktop();d.ready();d.claim()
  limits=core.Limits(Decimal(str(reserve)),60,300,4096,600)
  rec=core.Recorder(f/'native-evidence');spec={'id':task,'prompt':TASKS[task]['prompt'],'record_public_evidence':True,'evaluation':'manual_batch'}
  save(f/'submitted-once.json',{'submitted_at':now(),'model':core.MODEL,'tool':core.TOOL_VERSION});submitted=True
  with anthropic.Anthropic(api_key=KEYS[agent],max_retries=0,timeout=60,base_url='https://api.anthropic.com') as client:
   row=core.run(client,d,spec,limits,rec)
  if row is None:row=json.loads((rec.directory/'summary.json').read_text())
  # Grader-only final observation is never sent back to the model.
  pic=d.execute('screenshot',{},timeout=15)
  if not pic.get('is_error'):rec.screenshot(pic['content'],'independent-final')
  cost=float(row.get('api_cost_usd',0));uncertain=float(row.get('uncertain_cost_reserved_usd',0))
  (f/'original-response.txt').write_text(row.get('final_answer',''))
  save(f/'run-record.json',{'agent':agent,'task':task,'submitted':True,'status':row.get('status'),'agent_wall_seconds':row.get('agent_wall_seconds'),'wall_seconds':row.get('wall_seconds'),'max_seconds_from_submission':600,'actions':row.get('computer_actions'),'action_unit':'native computer actions including screenshots/zoom','screenshots':row.get('screenshots'),'model':row.get('model_returned') or core.MODEL,'tool_version':core.TOOL_VERSION,'cost_usd':cost,'uncertain_cost_reserved_usd':uncertain,'cost_basis':'recorded tokens × standard model rates; not invoice','errors':row.get('errors'),'api_retries':row.get('api_retries'),'automatic_restarts':0,'fresh_desktop':True,'evidence_directory':str(rec.directory.relative_to(OUT))})
  ledger(agent+'/'+task,cost+uncertain,'model token estimate plus uncertain request reservation');log(agent=agent,task=task,event='finished',status=row.get('status'),cost=cost)
 except Exception as e:
  save(f/'run-record.json',{'agent':agent,'task':task,'submitted':submitted,'status':'failed' if submitted else 'blocked','reason':type(e).__name__,'cost_usd':None if submitted else 0,'automatic_restarts':0})
  ledger(agent+'/'+task,reserve if submitted else 0,'uncertain request reservation' if submitted else 'no model request');log(agent=agent,task=task,event='error',error=type(e).__name__)
 finally:
  if started:
   try:desktop.stop()
   except Exception as e:save(f/'cleanup-error.json',{'error':type(e).__name__})

 return row is not None

def build_openai_adapter(task,f):
 source=(OPENAI/'benchmark.py').read_text()
 # Replace only task-specific validation and request loop; keep original native action executor.
 a=source.index('    async def request(self, client, **body):');b=source.index('    async def route(self, route):',a)
 request='''    async def request(self, client, **body):
        count = await client.responses.input_tokens.count(model=MODEL, tools=[{'type':'computer'}], instructions=TASK, **body)
        self.event('input_tokens_counted', input_tokens=count.input_tokens)
        # Worst standard cache-write rate, full output cap, plus 20% input allowance.
        rate = 5.0 if count.input_tokens > 272000 else 2.5
        output_rate = 15.0 if count.input_tokens > 272000 else 10.0
        reservation = ((count.input_tokens * 1.2 + 4096) * rate + 4096 * output_rate) / 1000000
        spent = estimate_cost(self.usages)['estimated_usd']
        if spent + reservation > self.args.budget_usd:
            raise RuntimeError('Budget guard: next request not sent')
        n=len(self.requests)+1
        entry=dict(number=n,attempt=1,started_at=utc_now(),model=MODEL,reserved_usd=reservation)
        self.requests.append(entry)
        self.event('api_request_started',**entry)
        self.uncertain_reservation=reservation
        response=await client.responses.create(model=MODEL,tools=[{'type':'computer'}],instructions=TASK,max_output_tokens=4096,service_tier='default',**body)
        raw=response.model_dump(mode='json',exclude_none=True)
        write_json(self.root/'responses'/f'{n:03d}.json',raw)
        if raw.get('usage'):
            self.usages.append(raw['usage'])
            self.uncertain_reservation=0
        entry.update(status='success',response_id=response.id,returned_model=response.model,usage=raw.get('usage'))
        self.event('api_request_completed',**entry)
        if raw.get('error') or response.status!='completed':raise RuntimeError('Response not completed: '+str(response.status))
        if response.model!=MODEL:raise RuntimeError('Unexpected returned model; no fallback')
        return response

'''
 source=source[:a]+request+source[b:]
 source=source.replace("allowed = host == 'github.com' or host.endswith('.githubassets.com') or host.endswith('.githubusercontent.com')","allowed = host == 'github.com' or host.endswith('.githubassets.com') or host.endswith('.githubusercontent.com') or host.endswith('.wikipedia.org') or host.endswith('.wikimedia.org') or host.endswith('.chatgpt.site') or host.endswith('.oaiusercontent.com')")
 a=source.index('                            text = self.final_text.strip()');b=source.index("                            self.status = 'completed_unverified'",a)
 source=source[:a]+'''                            try:
                                self.final=json.loads(self.final_text)
                            except (ValueError,TypeError):
                                self.final=None
'''+source[b:]
 # A separate grader-only DOM snapshot of the synthetic form after the agent stops.
 needle='''            # Stop timed work before cleanup; retain all observations and raw usage.
            elapsed = time.monotonic()-self.started'''
 replacement=needle+'''
            try:
                if self.page:
                    if 'chatgpt.site' in self.page.url:
                        state=await self.page.evaluate("Object.fromEntries(Object.entries(localStorage).filter(([k])=>k.startsWith('manicule:')))")
                        write_json(self.root/'independent-fixture-state.json',{'grader_only':True,'state':state,'provided_to_agent':False})
                    await self.page.screenshot(path=str(self.root/'screenshots'/'independent-final.png'),full_page=True,timeout=10000)
            except Exception as e:
                self.event('grader_observation_error',category=type(e).__name__)'''
 assert source.count(needle)==1;source=source.replace(needle,replacement)
 source=source.replace("estimated_cost=estimate_cost(self.usages),","estimated_cost=estimate_cost(self.usages), uncertain_cost_reserved_usd=getattr(self,'uncertain_reservation',0),")
 module=types.ModuleType('batch_openai_adapter');module.__file__=str(HERE/'openai-adapter-source.py')
 # Save the exact adapted code for reproducibility; task and keys are runtime values only.
 (HERE/'openai-adapter-source.py').write_text(source)
 exec(compile(source,module.__file__,'exec'),module.__dict__)
 module.TASK=TASKS[task]['prompt'];module.START_URL=TASKS[task]['start_url']
 return module

def openai_task(task):
 agent='openai';reserve=.8;f=claim(agent,task,reserve)
 if f is None:return True
 submitted=False
 try:
  module=build_openai_adapter(task,f);os.environ['OPENAI_API_KEY']=KEYS[agent]
  args=argparse.Namespace(results=str(f/'native-evidence'),max_seconds=600,max_steps=80,headless=True,budget_usd=reserve)
  save(f/'submitted-once.json',{'submitted_at':now(),'model':module.MODEL,'tool':'computer'});submitted=True
  runner=module.Benchmark(args);asyncio.run(runner.run())
  raw=json.loads((f/'native-evidence/openai_run_1.json').read_text());cost=raw['estimated_cost']['estimated_usd'];uncertain=raw.get('uncertain_cost_reserved_usd',0)
  (f/'original-response.txt').write_text(redact(raw.get('final_output_text','')))
  save(f/'run-record.json',{'agent':agent,'task':task,'submitted':True,'status':raw['status'],'agent_wall_seconds':raw['wall_clock_seconds'],'max_seconds_from_submission':600,'actions':raw['computer_actions'],'action_unit':'native computer actions','screenshots':len(list((f/'native-evidence/screenshots').glob('step_*.png')))+len(list((f/'native-evidence/screenshots').glob('initial.png'))),'model':raw['model'],'tool_version':'computer','cost_usd':cost,'uncertain_cost_reserved_usd':uncertain,'cost_basis':'recorded tokens × standard model rates; not invoice','errors':raw['errors'],'error':raw['error'],'api_retries':raw['retries'],'automatic_restarts':0,'fresh_profile':True,'browser':raw['browser']})
  ledger(agent+'/'+task,cost+uncertain,'model token estimate plus uncertain request reservation');log(agent=agent,task=task,event='finished',status=raw['status'],cost=cost)
 except Exception as e:
  save(f/'run-record.json',{'agent':agent,'task':task,'submitted':submitted,'status':'failed' if submitted else 'blocked','reason':type(e).__name__,'cost_usd':None if submitted else 0,'automatic_restarts':0});ledger(agent+'/'+task,reserve if submitted else 0,'uncertain request reservation' if submitted else 'no request');log(agent=agent,task=task,event='error',error=type(e).__name__)

 return (f/'native-evidence/openai_run_1.json').exists() and (raw.get('responses_succeeded',0)>0 or not raw.get('error')) if 'raw' in locals() else False

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('agent',choices=['claude','openai']);args=a.parse_args()
 for index,task in enumerate(TASKS):
  if not (claude_task if args.agent=='claude' else openai_task)(task):
   for remaining in list(TASKS)[index+1:]:save(OUT/'runs'/args.agent/remaining/'run-record.json',{'agent':args.agent,'task':remaining,'status':'blocked','submitted':False,'reason':'configuration/access failure on first attempt; no troubleshooting or restart','cost_usd':0})
   break
