"""Wait for six terminal attempts, then collect truth and stop only owned test resources."""
from pathlib import Path
import json,time,argparse,subprocess,sys,os,datetime
P=Path(__file__).resolve().parent;a=argparse.ArgumentParser();a.add_argument('--socket',required=True);args=a.parse_args()
while True:
 path=P/'benchmark-status.json'
 if path.exists():
  try:
   d=json.loads(path.read_text())
   if len(d.get('completed',[]))==6:break
  except ValueError:pass
 time.sleep(2)
r=subprocess.run([sys.executable,str(P/'finish_evidence.py'),'--socket',args.socket],capture_output=True,text=True,timeout=250)
(P/'final-collection-status.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':r.returncode,'summary':r.stdout,'error_category':None if r.returncode==0 else 'collection_failed','stderr_values_retained':False},indent=2)+'\n')
sys.path.insert(0,str(P.parents[2].parent/'set-up-a-working-benchmark-for/outputs/claude-computer-benchmark'));os.environ['DOCKER_CONTEXT']='colima-claude-benchmark'
from benchmark import desktop
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};desktop.stop();result['owned_container_removed']=True
stop=subprocess.run(['colima','stop','--profile','claude-benchmark'],capture_output=True,text=True,timeout=60);result['colima_stop_exit_code']=stop.returncode
status=subprocess.run(['colima','status','--profile','claude-benchmark'],capture_output=True,text=True);result.update(colima_status_exit_code=status.returncode,colima_status_text=status.stdout+status.stderr)
(P/'infrastructure-cleanup.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'six_attempts_terminal':True,'collection_exit_code':r.returncode,'owned_container_removed':True,'vm_stop_exit_code':stop.returncode}),flush=True)
