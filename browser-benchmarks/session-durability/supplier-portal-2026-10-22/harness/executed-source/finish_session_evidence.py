"""Owner-only post-run verification and experiment-session cleanup; no agent requests."""
from pathlib import Path
import json,sys,re,urllib.request,datetime
from fixture_client import Fixture
ROOT=Path(__file__).resolve().parent;owner=json.loads(sys.stdin.readline())
class RAMFixture(Fixture):
 def key(self,n):return owner[n]
f=RAMFixture(None)
def save(n,d):(ROOT/n).write_text(json.dumps(d,indent=2)+'\n')
for kind in ['tinyfish','claude-existing','claude-persistent']:assert (ROOT/kind/'server-verification.json').exists(),kind+' not verified yet'
save('final-audit-before-cleanup.json',f.json('/__fixture/audit'));save('final-sessions-before-cleanup.json',f.json('/__fixture/sessions'))
hashes=[json.loads((ROOT/'tinyfish-profile-setup.json').read_text())['server_session_hash']]+[json.loads((ROOT/k/'setup.json').read_text())['setup_session_hash'] for k in ['claude-existing','claude-persistent']]
results=[{'session_hash':h,'response':f.json('/__fixture/expire',{'session_hash':h})} for h in hashes]
save('experiment-session-cleanup.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'post_test_revocation_only':True,'expired_session_reauthentication_tested':False,'sessions':results});save('final-sessions-after-cleanup.json',f.json('/__fixture/sessions'))
journal=Path('${PRIVATE_AUTHORIZED_CHAT_HISTORY}');key=None
for line in journal.open():
 ms=re.findall(r'sk-tinyfish-[A-Za-z0-9_-]{20,}',line)
 if ms:key=ms[-1]
assert key
req=urllib.request.Request('https://agent.tinyfish.ai/v1/wallet',headers={'X-API-Key':key})
with urllib.request.urlopen(req,timeout=25) as response:wallet=json.load(response)
save('wallet-after-private.json',wallet)
before=json.loads((ROOT/'wallet-before-private.json').read_text())['body'];delta=float(before['available_balance'])-float(wallet['available_balance'])
save('wallet-reconciliation.json',{'observed_credit_delta_usd':round(delta,9),'new_web_agent_step_estimate_usd':.048,'setup_observed_delta_usd':0,'invoice_reconciled':False,'account_balance_or_identifier_published':False,'other_account_activity_cannot_be_excluded':True})
print(json.dumps({'three_new_sessions_revoked':all(x['response'].get('expired') for x in results),'tinyfish_wallet_delta_usd':round(delta,9),'agent_requests':0}))
key=None;owner.clear()
