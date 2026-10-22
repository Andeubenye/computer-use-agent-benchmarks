"""Offline regrade of independently reviewed observations, not automated image recognition.
No provider calls, task execution, GUI editing or credentials required.
"""
from pathlib import Path
from decimal import Decimal
import hashlib,json,re,statistics
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
def load(p):return json.loads(p.read_text())
def verify():
 results=load(ROOT/'results.json');expected=load(ROOT/'expected-state.json')['fields'];errors=[]
 def check(x,m):
  if not x:errors.append(m)
 canonical=(ROOT/'../../prompts/exact/test-3-form.txt').resolve().read_bytes();cost=Decimal(0);times=[];images=htmls=steps=0
 for n in (2,3,4):
  a=ROOT/f'attempt-{n}';r=load(a/'run-record.json');provider=load(a/'provider-run.json');obs=load(a/'gui-observations.json');saved=load(a/'independent-verification.json');config=load(a/'configuration.json');payload=load(a/'actual-submission-payload.json')
  check((a/'task-prompt.txt').read_bytes()==canonical,f'{n}: prompt changed')
  check(hashlib.sha256(canonical).hexdigest()==config['prompt_sha256']==results['prompt_sha256'],f'{n}: prompt hash')
  check(payload['goal'].encode()==canonical,f'{n}: actual submitted prompt')
  check(payload['agent_config']['max_duration_seconds']==r['max_seconds_from_submission']==600,f'{n}: deadline differs')
  check(payload['use_profile'] is False and payload['use_vault'] is False and provider['profile_attached'] is False,f'{n}: profile mismatch')
  check(provider['browser_config']['proxy_enabled'] is False,f'{n}: proxy differs')
  correct=[];incorrect=[];unverified=[]
  for field,want in expected.items():
   got=obs['fields'][field]
   if got is None:unverified.append(field)
   elif (re.sub(r'\D','',got)==re.sub(r'\D','',want) if field=='phone' else got==want):correct.append(field)
   else:incorrect.append(field)
  check(len(correct)==saved['strict_score_confirmed']==8,f'{n}: strict score')
  check(incorrect==saved['incorrect_fields_confirmed']==['message'],f'{n}: mismatch list')
  check(unverified==saved['unverified_fields']==['newsletter'],f'{n}: unverified list')
  check(obs['fields']['message']=='This is a benchmark.' and saved['sensitivity_score_confirmed']==9,f'{n}: sensitivity')
  check(not saved['full_task_completion_verified'] and saved['outcome']=='partially_successful',f'{n}: completion overclaim')
  check(obs['agent_response_used_as_field_evidence'] is False and not obs['verification_data_sent_to_agent'],f'{n}: verification separation')
  check(not obs['newsletter_visible_in_any_capture'],f'{n}: observability record changed')
  html=(a/obs['final_status_html']).read_text()
  check(bool(re.search(r'id="form-status"[^>]*>Not submitted\.',html)),f'{n}: non-submission final status')
  check(not obs['trace_submission_action_observed'] and not obs['trace_reload_after_submission_observed'],f'{n}: submission observation')
  check(not r['client_error'] and not provider['error'] and not r['deadline_fired'] and r['status']=='COMPLETED',f'{n}: execution status')
  check(r['automatic_restarts']==0,f'{n}: restart')
  check(r['agent_wall_seconds']<600,f'{n}: runtime exceeded')
  check(r['actions']==provider['num_of_steps'],f'{n}: step count')
  check(Decimal(str(r['cost_usd']))==Decimal(r['actions'])*Decimal('.016')==Decimal(str(load(a/'wallet-observation.json')['delta_usd'])),f'{n}: cost mismatch')
  ni=len(list((a/'screenshots').glob('*.jpg')));nh=len(list((a/'html-captures').glob('*.html')))
  check(ni==r['screenshots']==len(obs['all_screenshots_reviewed']),f'{n}: images not all reviewed')
  check(nh==ni,f'{n}: capture inventory')
  rows=[x for x in results['attempts'] if x['agent']=='TinyFish' and x['attempt']==n]
  check(len(rows)==1 and rows[0]['confirmed_correct']==8 and rows[0]['unverified']==1 and rows[0]['cost_usd']==r['cost_usd'],f'{n}: comparison row')
  images+=ni;htmls+=nh;steps+=r['actions'];cost+=Decimal(str(r['cost_usd']));times.append(r['agent_wall_seconds'])
  check((a/obs['final_screenshot']).is_file(),f'{n}: missing final image')
 check(cost==Decimal('.624') and steps==39 and images==htmls==36,'Follow-up totals')
 check(abs(statistics.mean(times)-results['new_rerun_aggregate']['mean_client_seconds'])<1e-9,'Mean timer')
 check(Decimal(str(results['budget']['baseline_committed_usd']))+cost==Decimal(str(results['budget']['committed_or_reserved_usd'])),'Budget reconciliation')
 check(results['new_rerun_aggregate']['strict_verified_full_successes']==0,'Unsubstantiated full success')
 # Historical results remain reference-only and unchanged.
 originals=ROOT/'../../evidence/additional-tasks/runs'
 check(load(originals/'tinyfish/test-3-form/verification.json')['correct_checks_confirmed']==5,'Historical TinyFish grade')
 check(load(originals/'claude/test-3-form/verification.json')['correct_checks']==10,'Historical Claude grade')
 # Check copied evidence against sanitized-public hashes, not private source paths.
 for item in load(ROOT/'source-provenance.json')['files']:
  f=REPO/item['public_file']
  check(f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest()==item['public_sha256'],'Copied evidence hash: '+item['public_file'])
 return {'passed':not errors,'benchmark_requests':0,'new_runs':3,'strict_confirmed_per_rerun':8,'unverified_per_rerun':1,'new_screenshots':images,'new_html_captures':htmls,'new_provider_steps':steps,'cost_usd':str(cost),'observation_basis':'Independent manual image review; offline code regrades observations and checks trace/capture/cost integrity, not screenshot recognition','errors':errors}
if __name__=='__main__':
 result=verify();print(json.dumps(result,indent=2));raise SystemExit(not result['passed'])
