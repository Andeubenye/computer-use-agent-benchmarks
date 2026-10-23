"""Fresh controller process: receives no portal password, cookie or local browser state."""
from pathlib import Path
import argparse,ast,json,sys,datetime,time,os,subprocess
from fixture_client import Fixture,BASE
ROOT=Path(__file__).resolve().parent;PROJECT=ROOT.parents[1];payload=json.loads(sys.stdin.readline());key=payload.pop('tinyfish');owner=payload
class RAMFixture(Fixture):
 def key(self,name):return owner[name]
f=RAMFixture(None)
def dump(n,d):(ROOT/n).write_text(json.dumps(d,indent=2)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
out=ROOT/'tinyfish';out.mkdir(exist_ok=False);(out/'task-prompt.txt').write_bytes((ROOT/'task-prompt.txt').read_bytes())
setup=json.loads((ROOT/'tinyfish-profile-setup.json').read_text());assert setup['profile_saved'] and setup['login_confirmed'];before=f.json('/__fixture/audit');dump('tinyfish-before-audit.json',before);ids={e['event_id'] for e in before['events']}
ns={'__file__':str(PROJECT/'work/manicule-batch-2-5/common.py'),'KEYS':{'tinyfish':key}};tree=ast.parse((PROJECT/'work/manicule-batch-2-5/common.py').read_text());tree.body=[n for n in tree.body if not(isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='KEYS' for t in n.targets))];exec(compile(tree,'reused_common.py','exec'),ns)
src=(PROJECT/'work/manicule-batch-2-5/cloud_batch.py').read_text();tree=ast.parse(src);code='\n\n'.join(ast.get_source_segment(src,n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['tiny','submit_marker']);exec(compile(code,'reused_tinyfish_adapter.py','exec'),ns);api0=ns['api'];save=ns['save']
def api(a,path,data=None,**kwargs):
 if path=='/v1/automation/run-async':
  data=dict(data);data.update(use_profile=True,profile_id=setup['profile_id'],use_vault=False,proxy_config={'enabled':False},capture_config={'screenshots':True,'html':False});save(out/'actual-submission-payload.json',data)
 return api0(a,path,data,**kwargs)
ns.update(api=api,claim=lambda *a:out,ledger=lambda *a:(True,None),TASKS={'session-durability':{'prompt':(ROOT/'task-prompt.txt').read_text(),'start_url':BASE+'/dashboard'}})
save(out/'controller-identity.json',{'pid':os.getpid(),'started_at':now(),'setup_process_pid':setup['local_setup_python_pid'],'setup_process_exited_before_this_controller':not Path('/proc/'+str(setup['local_setup_python_pid'])).exists() if sys.platform=='linux' else subprocess.run(['ps','-p',str(setup['local_setup_python_pid'])],capture_output=True).returncode!=0,'local_portal_password_supplied':False,'cookies_or_browser_files_supplied':False,'new_controller_process':True,'vault_enabled':False,'custom_spending_limit':None})
ns['tiny']('session-durability')
after=f.json('/__fixture/audit');sessions=f.json('/__fixture/sessions');events=[e for e in after['events'] if e['event_id'] not in ids];views=[e for e in events if e['kind']=='authenticated_view'];record=json.loads((out/'run-record.json').read_text());provider=json.loads((out/'provider-run.json').read_text());raw=(out/'original-response.txt').read_text();restored=bool(views) and all(e['session_hash']==setup['server_session_hash'] for e in views)
save(out/'server-verification.json',{'events_during_run':events,'setup_session_hash':setup['server_session_hash'],'setup_session_still_valid':next((s for s in sessions['sessions'] if s['token_hash']==setup['server_session_hash']),None),'authentication_restored':restored,'new_login_during_agent_task':any(e['kind']=='login_ok' for e in events),'supplier_saved_during_agent_task':any(e['kind']=='supplier_saved' for e in events),'profile_attached':provider.get('profile_attached'),'agent_result':provider.get('result'),'provider_status':provider['status'],'original_response_preserved':True,'verification_sent_to_agent':False})
print(json.dumps({'agent':'tinyfish','terminal_status':provider['status'],'authentication_restored':restored,'agent_seconds':record['agent_wall_seconds'],'cost_estimate_usd':record['cost_usd'],'steps':record['actions']}),flush=True);key=None;owner.clear()
