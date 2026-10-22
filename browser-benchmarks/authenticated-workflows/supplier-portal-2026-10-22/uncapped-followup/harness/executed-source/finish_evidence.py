from pathlib import Path
import argparse,json,datetime,urllib.request
from fixture_client import Fixture
p=argparse.ArgumentParser();p.add_argument('--socket',required=True);a=p.parse_args();f=Fixture(a.socket);root=Path(__file__).resolve().parent
def save(n,v):(root/n).write_text(json.dumps(v,indent=2)+'\n')
save('final-audit.json',f.json('/__fixture/audit'))
save('final-server-records.json',{rid:f.json('/__fixture/verify/'+rid) for rid in [f'SUP-{c}{n:03d}' for c in 'CT' for n in range(1,11)]})
save('sessions-before-cleanup.json',f.json('/__fixture/sessions'))
results=[]
for name in ['tinyfish-profile-setup.json','claude-context-setup.json']:
 h=json.loads((root/name).read_text())['server_session_hash'];response=f.json('/__fixture/expire',{'session_hash':h});results.append({'provider':name.split('-')[0],'response':response})
sessions=f.json('/__fixture/sessions');save('sessions-after-cleanup.json',sessions)
hashes={json.loads((root/name).read_text())['server_session_hash'] for name in ['tinyfish-profile-setup.json','claude-context-setup.json']}
revoked=all(x['revoked'] for x in sessions['sessions'] if x['token_hash'] in hashes)
save('session-cleanup.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'only_dedicated_synthetic_sessions_expired':True,'both_session_revocations_verified':revoked,'results':results,'agent_recovery_experiment':False})
req=urllib.request.Request('https://agent.tinyfish.ai/v1/wallet',headers={'X-API-Key':f.key('tinyfish')})
try:
 with urllib.request.urlopen(req,timeout=25) as r: wallet=json.load(r)
 save('final-wallet-private.json',wallet)
 print(json.dumps({'evidence_saved':True,'session_revocations_verified':revoked,'wallet_read':True,'wallet_top_level_keys':list(wallet)}))
except Exception as e: print(json.dumps({'evidence_saved':True,'session_revocations_verified':revoked,'wallet_read':False,'error_type':type(e).__name__}))
