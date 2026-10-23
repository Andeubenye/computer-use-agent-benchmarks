"""Offline checks of saved durability evidence; never sends requests or controls a browser."""
from pathlib import Path
from decimal import Decimal
import json,hashlib,ast,re
ROOT=Path(__file__).resolve().parent

def verify():
 errors=[];checks=0
 def check(ok,msg):
  nonlocal checks
  checks+=1
  if not ok:errors.append(msg)
 def load(p):return json.loads(p.read_text())
 def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
 result=load(ROOT/'results.json');prompt=(ROOT/'task-prompt.txt').read_bytes();check(digest(ROOT/'task-prompt.txt')==result['same_task_prompt_sha256'],'Frozen prompt hash');cost=Decimal(0)
 for kind,expected in [('tinyfish',True),('claude-existing',False),('claude-persistent',True)]:
  folder=ROOT/'runs'/kind;row=load(folder/'run-record.json');v=load(folder/'server-verification.json');check((folder/'task-prompt.txt').read_bytes()==prompt,kind+' prompt differs');check(v['authentication_restored']==expected,kind+' server restoration outcome');check(not v['new_login_during_agent_task'] and not v['supplier_saved_during_agent_task'],kind+' non-read-only events');check(row['agent_wall_seconds']<600,kind+' deadline');events=v.get('events_during_run',v.get('events_during_agent_task',[]));views=[e for e in events if e['kind']=='authenticated_view'];check(bool(views)==expected,kind+' authenticated views');check(all(e['session_hash']==v['setup_session_hash'] for e in views),kind+' wrong session attribution')
  answer=(folder/'original-response.txt').read_text();match=re.search(r'\{[\s\S]*?\}',answer);obj=json.loads(match.group());check(obj['authenticated']==expected,kind+' answer status');check(obj.get('page_heading')=='Supplier dashboard' and 'Benchmark Buyer' in obj.get('signed_in_account_label','') and obj.get('supplier_record_id')=='SUP-C001' if expected else obj.get('sign_in_heading')=='Sign in to supplier review',kind+' visible evidence answer')
  if kind=='tinyfish':
   payload=load(folder/'actual-submission-payload.json');check(payload['goal'].encode()==prompt and payload['use_profile'] and payload['use_vault'] is False,'TinyFish payload/profile/Vault');check(v['profile_attached'] is True,'Profile not attached');identity=load(folder/'controller-identity.json');check(identity['setup_process_exited_before_this_controller'] and identity['new_controller_process'] and not identity['local_portal_password_supplied'] and not identity['cookies_or_browser_files_supplied'],'TinyFish controller boundary');amount=Decimal(row['actions'])*Decimal('.016');check(amount==Decimal(str(row['cost_usd'])),'TinyFish step cost');check(Decimal(str(load(ROOT/'evidence/wallet-reconciliation.json')['observed_credit_delta_usd']))==amount,'TinyFish wallet mismatch')
  else:
   life=load(folder/'lifecycle.json');check(life['old_container_id']!=life['new_identity']['container_id'] and life['new_container_id_differs'],'Container identity did not change');mounts=life['new_container_mounts'];check(bool(mounts)==expected,kind+' mounts mismatch')
   if expected:check(mounts[0]['Name']==life['shutdown']['mounts'][0]['Name'] and mounts[0]['Destination']=='/home/agent/profile','Persistent mount mismatch')
   session=v['server_setup_session_valid_before_agent'];check(session['revoked']==0 and life['server_setup_session_valid_before_agent'],'Setup session invalid before diagnostic');native=next((folder/'native-evidence').glob('*/task.json'));check(load(native)['prompt'].encode()==prompt,'Native request prompt differs');responses=[load(f) for f in sorted(native.parent.glob('responses/*.json'))];check(len(responses)==4,'Native request count');amount=Decimal(0)
   for response in responses:
    u=response['usage'];amount+=(Decimal(u.get('input_tokens',0))*2+Decimal(u.get('output_tokens',0))*10+Decimal(u.get('cache_read_input_tokens',0))*Decimal('.1')+Decimal(u.get('cache_creation_input_tokens',0))*4)/Decimal(1000000)
   check(amount==Decimal(row['api_cost_usd']),'Native raw usage cost');check(row['api_retries']==0 and row['errors']==0,'Native retries/errors changed');check(row['status']=='needs_review','Raw manual-review status overwritten')
  cost+=amount
 check(cost==Decimal('0.165142'),'Total new diagnostic cost');check(result['actual_new_agent_runs']==3,'Paid run count');check(all(c['diagnostic_task_correct'] for c in result['cases']),'Diagnostic grade');check(load(ROOT/'evidence/supplier-records-comparison.json')['unchanged'],'Supplier rows changed');check(load(ROOT/'evidence/runtime-cleanup.json')['final_status']=='Stopped','VM not stopped');check(load(ROOT/'evidence/portal-restoration.json')['original_password_hash_and_metadata_restored'],'Portal config not restored');check(load(ROOT/'evidence/portal-restoration.json')['deployment_status']=='succeeded','Original config not applied');check(load(ROOT/'evidence/persistent-volume-cleanup.json')['removed'],'Volume not removed')
 cleanup=load(ROOT/'evidence/experiment-session-cleanup.json');check(len(cleanup['sessions'])==3 and all(s['response']['expired'] for s in cleanup['sessions']),'New sessions not revoked');check(result['vault']=='NOT TESTED' and result['expired_session_reauthentication']=='NOT TESTED','Untested scope changed')
 images=[f for f in ROOT.rglob('*') if f.suffix.lower() in ['.png','.jpg']];check(len(images)==13,'Screenshot inventory')
 for p in load(ROOT/'source-provenance.json')['files']:
  check(digest(ROOT/p['public_file'])==p['public_sha256'],'Published source digest '+p['public_file'])
 return {'passed':not errors,'checks':checks,'actual_new_agent_runs':3,'diagnostic_tasks_correct':3,'authentication_restored_configurations':2,'screenshots':len(images),'total_new_agent_api_estimate_usd':str(cost),'benchmark_requests':0,'errors':errors}
if __name__=='__main__':
 r=verify();print(json.dumps(r,indent=2));raise SystemExit(not r['passed'])
