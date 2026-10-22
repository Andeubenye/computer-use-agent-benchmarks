from pathlib import Path
import argparse,json,re,urllib.parse,hashlib,datetime
from fixture_client import Fixture
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--socket',required=True);args=p.parse_args();f=Fixture(args.socket)
if (ROOT/'fixture-qa.json').exists():raise SystemExit('QA evidence already exists; do not repeat silently')
checks=[]
def check(name,condition):checks.append({'check':name,'passed':bool(condition)});assert condition,name
status,h,b=f.request('/dashboard');check('Anonymous dashboard redirects to login',status==303 and h['Location'].startswith('/login'))
status,h,b=f.request('/__fixture/sessions');check('Server administration rejects missing fixture admin credential',status==401)
seed={'records':[{'id':'SUP-C999','batch_id':'auth-qa','pair_index':999,'cohort':'claude'}]};f.json('/__fixture/seed',seed)
status,h,b=f.request('/login',{'username':'benchmark-buyer','password':f.key('fixture_password')},form=True);check('Dedicated synthetic login succeeds',status==303 and h['Location']=='/dashboard')
cookie=h['Set-Cookie'].split(';',1)[0];token=cookie.split('=',1)[1]
check('Login cookie is Secure, HttpOnly and SameSite',all(x in h['Set-Cookie'] for x in ('Secure','HttpOnly','SameSite=Lax')))
status,h,b=f.request('/supplier/SUP-C999',cookie=cookie);check('Authenticated detail page loads',status==200 and 'SUP-C999' in b)
csrf=re.search(r'name="csrf" value="([^"]+)"',b)[1]
status,h,b=f.request('/supplier/SUP-C999',{'csrf':'invalid','version':0,'status':'Reviewed','notes':'Fixture QA exact note.'},form=True,cookie=cookie);check('Wrong CSRF cannot save',status==403)
status,h,b=f.request('/supplier/SUP-C999',{'csrf':csrf,'version':0,'status':'Reviewed','notes':'Fixture QA exact note.'},form=True,cookie=cookie);check('Authorized save redirects to unique confirmation',status==303 and 'saved=CNF-' in h['Location'])
confirmation=urllib.parse.parse_qs(urllib.parse.urlsplit(h['Location']).query)['saved'][0]
truth=f.json('/__fixture/verify/SUP-C999');r=truth['record'];check('Independent stored record matches exact status, note and confirmation',r['status']=='Reviewed' and r['notes']=='Fixture QA exact note.' and r['confirmation_id']==confirmation and r['version']==1)
events=[e for e in truth['audit'] if e['kind']=='supplier_saved'];check('Server audit attributes save to authenticated session',len(events)==1 and events[0]['session_hash']==hashlib.sha256(token.encode()).hexdigest())
status,h,b=f.request('/supplier/SUP-C999',{'csrf':csrf,'version':0,'status':'Reviewed','notes':'Stale update should fail.'},form=True,cookie=cookie);check('Stale version cannot overwrite saved data',status==409)
f.json('/__fixture/reset',{'record_id':'SUP-C999'});r=f.json('/__fixture/verify/SUP-C999')['record'];check('Reset restores Pending baseline and clears receipt',r['status']=='Pending' and r['notes']=='' and r['confirmation_id'] is None and r['version']==0)
f.json('/__fixture/expire',{'session_hash':hashlib.sha256(token.encode()).hexdigest()});status,h,b=f.request('/dashboard',cookie=cookie);check('Expired session loses authenticated access',status==303 and h['Location'].startswith('/login'))
f.json('/__fixture/cleanup-qa',{})
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fixture_version':'supplier-auth-v1','qa_record_id':'SUP-C999','checks':checks,'passed':all(c['passed'] for c in checks),'scored_agent_runs':0,'provider_inference_requests':0,'qa_cookie_or_password_saved':False,'qa_record_removed_from_active_dashboard':True,'server_confirmation_validated':True}
(ROOT/'fixture-qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));cookie=token=csrf=None
# Distinct, equivalent records; create once, never overwrite prior benchmark outputs.
records=[{'id':f'SUP-{prefix}{i:03d}','batch_id':'auth-2026-10-22','pair_index':i,'cohort':name} for i in range(1,11) for prefix,name in [('C','claude'),('T','tinyfish')]]
f.json('/__fixture/seed',{'records':records});fixtures={'batch_id':'auth-2026-10-22','records':records,'notes_by_pair':{str(i):f'Reviewed supplier documentation for batch {i:02d}. No changes requested.' for i in range(1,11)},'expected_status':'Reviewed','confirmation_id':'generated server-side at save; never predetermined or fed to agent'};(ROOT/'fixtures.json').write_text(json.dumps(fixtures,indent=2)+'\n');print(json.dumps({'benchmark_records_seeded':len(records),'notes_identical_within_each_pair':True}))
