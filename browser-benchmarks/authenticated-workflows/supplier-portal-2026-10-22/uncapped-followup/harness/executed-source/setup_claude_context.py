"""Non-scored native GUI login into a dedicated persistent benchmark container."""
from pathlib import Path
import argparse,base64,datetime,json,os,subprocess,sys,time
from fixture_client import Fixture,BASE
ROOT=Path(__file__).resolve().parent
CLAUDE=ROOT.parents[2].parent/'set-up-a-working-benchmark-for/outputs/claude-computer-benchmark'
p=argparse.ArgumentParser();p.add_argument('--socket',required=True);args=p.parse_args();f=Fixture(args.socket)
if (ROOT/'claude-context-setup.json').exists():raise SystemExit('Existing context setup evidence; no automatic repeat')
sys.path.insert(0,str(CLAUDE));os.environ['DOCKER_CONTEXT']='colima-claude-benchmark'
from benchmark import desktop
start=time.monotonic();started=datetime.datetime.now(datetime.timezone.utc).isoformat();report={'started_at_utc':started,'mode':'Non-scored native GUI session setup','image_rebuilt':False,'persistent_context_supported':True,'password_sent_to_agent':False,'provider_generation_requests':0,'setup_actions':[],'password_value_or_cookie_saved_to_evidence':False};before={x['token_hash'] for x in f.json('/__fixture/sessions')['sessions']}
try:
 desktop.start();d=desktop.Desktop();d.ready();d.claim()
 def act(name,args):
  t=time.monotonic();r=d.execute(name,args,timeout=20);report['setup_actions'].append({'action':name,'seconds':time.monotonic()-t,'is_error':r.get('is_error'),'typed_value_redacted':name=='type'});assert not r.get('is_error'),name;return r
 act('key',{'text':'ctrl+l'});act('type',{'text':BASE+'/login'});act('key',{'text':'Return'})
 for _ in range(30):
  title=d.execute('window_title',{},timeout=5)
  if 'Sign in' in title.get('content',''):break
  time.sleep(.5)
 else:raise RuntimeError('Login page did not load')
 act('key',{'text':'Tab'});act('type',{'text':'benchmark-buyer'});act('key',{'text':'Tab'});act('type',{'text':f.key('fixture_password')});act('key',{'text':'Tab'});act('key',{'text':'Return'})
 for _ in range(30):
  title=d.execute('window_title',{},timeout=5)
  if 'Dashboard' in title.get('content',''):break
  time.sleep(.5)
 else:raise RuntimeError('Authenticated dashboard did not load')
 act('key',{'text':'Escape'})
 desktop.docker('exec','-i',desktop.CONTAINER,'xclip','-selection','clipboard','-in',data=b'',timeout=5)
 pic=act('screenshot',{});image=next(b for b in pic['content'] if b.get('type')=='image');(ROOT/'claude-setup-authenticated.png').write_bytes(base64.b64decode(image['source']['data']))
 sessions=f.json('/__fixture/sessions')['sessions'];new=[s for s in sessions if s['token_hash'] not in before and not s['revoked']]
 tiny=ROOT/'tinyfish-profile-setup.json'
 if tiny.exists():
  exclude=json.loads(tiny.read_text()).get('server_session_hash');new=[s for s in new if s['token_hash']!=exclude]
 assert len(new)==1,'Cannot attribute setup session unambiguously';report.update(login_confirmed=True,server_session_hash=new[0]['token_hash'],native_environment=d.identity(),container_left_running_for_sequential_benchmarks=True)
except Exception as e:
 report.update(login_confirmed=False,error_category=type(e).__name__)
 try:desktop.stop()
 except Exception:pass
finally:
 report.update(finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),setup_wall_seconds=time.monotonic()-start,local_infrastructure_cost_usd=None,local_infrastructure_cost_note='Existing Mac/Colima resources; electricity and previous setup unpriced')
 (ROOT/'claude-context-setup.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report.get(k) for k in ('login_confirmed','setup_wall_seconds','error_category')}))
