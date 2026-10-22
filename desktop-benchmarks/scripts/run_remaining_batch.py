"""Sequential, single-attempt queue. No task actions are chosen here."""
import json, subprocess, sys, time, os
from pathlib import Path
from common import ROOT, save, now
from run_native import recorded_spend

RUNTIME=os.environ.get('BENCHMARK_DOC_PYTHON',sys.executable)
queue=[('openai',2),('claude',3),('openai',3),('claude',4),('openai',4),('claude',5),('openai',5)]
marker=ROOT/'logs/remaining-batch-started.json'
if marker.exists():raise SystemExit('Existing batch marker: refuse automatic queue restart')
save(marker,{'utc':now(),'queue':queue,'api_retries':0,'automatic_benchmark_restarts':0})
previous=ROOT/'logs/claude/task-2/attempt-2/run-record.json'
until=time.time()+650
while not previous.exists():
    if time.time()>until:raise SystemExit('Prior attempt did not stop; no overlapping test started')
    time.sleep(1)
records=[]
for agent,task in queue:
    tag=agent+'/task-'+str(task)
    if 7-recorded_spend()<.15:
        records.append({'agent':agent,'task':task,'outcome':'BLOCKED','reason':'Insufficient remaining budget'});continue
    cap=min(.70,7-recorded_spend())
    save(ROOT/'logs/remaining-batch-progress.json',{'utc':now(),'active':tag,'completed':records,'estimated_spent_before':recorded_spend(),'next_run_cap':cap})
    log=ROOT/'logs'/(agent+'-task-'+str(task)+'-launcher.log')
    with log.open('xb') as output:
        try:
            result=subprocess.run([sys.executable,str(ROOT/'scripts/run_additional.py'),agent,str(task),'--budget',str(cap)],stdout=output,stderr=subprocess.STDOUT,timeout=650)
        except subprocess.TimeoutExpired:
            records.append({'agent':agent,'task':task,'outcome':'BLOCKED','reason':'Outer infrastructure timeout; stop batch to avoid uncertain spending'})
            break
    run=ROOT/'logs'/tag/'run-record.json'
    record={'agent':agent,'task':task,'process_exit':result.returncode,'record_present':run.exists()}
    if run.exists():
        x=json.loads(run.read_text());record.update(submitted=x['submitted'],reason=x['reason'],estimated_api_cost_usd=x['estimated_api_cost_usd'])
        args=[RUNTIME,str(ROOT/'verification/verify_additional.py'),str(task),str(ROOT/'outputs'/tag)]
        if not x['submitted']:args.append('--not-submitted')
        check=subprocess.run(args,capture_output=True,text=True,timeout=30)
        if check.returncode==0:
            value=json.loads(check.stdout);value['gui_review_pending']=True
            save(ROOT/'logs'/tag/'artifact-verification.json',value)
        else:save(ROOT/'logs'/tag/'artifact-verification-error.json',{'error':'Independent verifier process failed','exit':check.returncode})
    records.append(record)
    save(ROOT/'logs/remaining-batch-progress.json',{'utc':now(),'active':None,'completed':records,'estimated_spent':recorded_spend()})
save(ROOT/'logs/remaining-batch-complete.json',{'utc':now(),'records':records,'estimated_total_spent':recorded_spend(),'automatic_restarts':0})
