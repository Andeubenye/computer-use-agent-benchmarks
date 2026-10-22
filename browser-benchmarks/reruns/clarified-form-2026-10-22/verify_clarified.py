"""Offline integrity/cost regrade from independently reviewed final observations.
Manual screenshot observations remain the field evidence; no automated image recognition.
No provider calls, task interaction or credentials.
"""
from pathlib import Path
from decimal import Decimal
import hashlib,json,re,statistics
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
def load(p):return json.loads(p.read_text())
def verify():
 errors=[]
 def check(x,m):
  if not x:errors.append(m)
 data=load(ROOT/'results.json');expected=load(ROOT/'expected-state.json')['fields'];prompt=(ROOT/'clarified-prompt.txt').read_bytes();digest=hashlib.sha256(prompt).hexdigest();cost=Decimal(0);images=htmls=generations=0;grades=[]
 check(digest=='310e61b597776240557a2aed3e5bcbbdaf93a36c26c7c94e52b65d0b576b3007','Clarified prompt changed')
 for agent in ('tinyfish','claude'):
  for n in (1,2,3):
   a=ROOT/agent/f'attempt-{n}';record=load(a/'run-record.json');obs=load(a/'gui-observations.json');grade=load(a/'independent-verification.json');label=f'{agent}-{n}'
   check((a/'task-prompt.txt').read_bytes()==prompt,label+': prompt differs')
   check(record['agent_wall_seconds']<600,label+': exceeded 600 seconds')
   check(record['automatic_restarts']==0,label+': benchmark restart')
   unknown=obs.get('unverified_fields',[]);explicit=obs.get('explicitly_unselected_fields',[]);correct=[];incorrect=[]
   for field,want in expected.items():
    got=obs['fields'][field]
    if field in unknown:continue
    if field in explicit:incorrect.append(field);continue
    same=(re.sub(r'\D','',got)==re.sub(r'\D','',want)) if field=='phone' else got==want
    (correct if same else incorrect).append(field)
   check(len(correct)+len(incorrect)+len(unknown)==10,label+': incomplete grade partition')
   check(len(correct)==grade.get('correct_checks',grade.get('correct_checks_confirmed')),label+': grade mismatch')
   check(correct==grade['correct_fields_confirmed'] and incorrect==grade['incorrect_fields_confirmed'] and unknown==grade['unverified_fields'],label+': field lists mismatch')
   for f in obs['all_screenshots_reviewed']:check((a/f).is_file(),label+': missing reviewed image '+f)
   pics=list(a.rglob('*.png'))+list(a.rglob('*.jpg'));images+=len(pics);htmls+=len(list((a/'html-captures').glob('*.html')))
   row=next(r for r in data['new_attempts'] if r['agent']==agent and r['attempt']==n)
   check(row['confirmed_correct']==len(correct) and row['unverified']==len(unknown) and row['incorrect']==len(incorrect),label+': table grade')
   check(row['client_or_native_seconds']==record['agent_wall_seconds'],label+': table timer')
   if agent=='claude':
    native=next((a/'native-evidence').glob('*/summary.json')).parent;summary=load(native/'summary.json');task=load(native/'task.json');responses=[load(f) for f in sorted((native/'responses').glob('*.json'))];amount=Decimal(0)
    check(task['prompt'].encode()==prompt,label+': actual native prompt')
    check(summary['max_seconds']==600 and summary['max_tokens']==4096,label+': configuration changed')
    check(summary['model_requested']==summary['model_returned']=='claude-sonnet-5-5' and summary['tool_version']=='computer_toolset_20260801',label+': model/tool changed')
    for r in responses:
     u=r['usage'];cache=u.get('cache_creation') or {};one=int(cache.get('ephemeral_1h_input_tokens',0) or 0);five=int(u.get('cache_creation_input_tokens',0) or 0)-one
     amount+=(Decimal(u.get('input_tokens',0))*2+Decimal(u.get('output_tokens',0))*10+Decimal(u.get('cache_read_input_tokens',0))*Decimal('.1')+Decimal(five)*Decimal('2.5')+Decimal(one)*4)/1000000
    check(amount==Decimal(summary['api_cost_usd'])==Decimal(str(record['cost_usd'])),label+': raw token estimate')
    check(len(responses)==summary['api_attempts']==row['generation_requests'],label+': generation inventory')
    check(grade['outcome']=='successful' and len(correct)==10 and not unknown,label+': unsupported full pass')
    check((a/obs['lower_screenshot']).is_file() and obs['fields']['newsletter'] is False and obs['message_exact_match'],label+': lower-state evidence missing')
    check((a/'postrun-wrapper-error-record.json').is_file() and record['postrun_capture_error']=='TimeoutExpired',label+': lost collector failure')
    check((a/'original-response.txt').read_text()==summary['final_answer'],label+': original response changed')
    cost+=amount;generations+=len(responses)
   else:
    payload=load(a/'actual-submission-payload.json');provider=load(a/'provider-run.json');credit=load(a/'wallet-observation.json');last=(a/obs['final_status_html']).read_text()
    check(payload['goal'].encode()==prompt,label+': actual submitted goal')
    prefix='Navigate to '+payload['url']+' to complete the goal: '
    check(provider['goal']==prefix+payload['goal'],label+': provider URL wrapper differs')
    check(payload['browser_profile']=='lite' and payload['use_profile'] is False and provider['profile_attached'] is False,label+': browser profile changed')
    check(payload['agent_config']['max_duration_seconds']==600 and 'max_steps' not in payload['agent_config'],label+': supported config differs')
    check(not obs['newsletter_visible_in_any_capture'] and 'newsletter' in unknown,label+': checkbox inferred')
    check(re.search(r'id="form-status"[^>]*>Not submitted\.',last),label+': missing final status')
    if n==2:
     audit=load(a/'cost-and-stop-audit.json');check(provider['status']=='CANCELLED' and grade['outcome']=='failed' and len(correct)==1 and len(unknown)==2,label+': cancellation grade')
     check(provider['num_of_steps']==0 and len(provider['steps'])==24 and audit['inference_that_run_was_free'] is False,label+': missing activity/billing distinction')
     check(row['comparison_cost_usd'] is None and row['uncertain_cost_reserved_usd']==.465,label+': unresolved cost treated as zero')
    else:
     check(provider['status']=='COMPLETED' and grade['outcome']=='partially_successful' and len(correct)==9,label+': partial overstated')
     amount=Decimal(str(record['cost_usd']));check(amount==Decimal(provider['num_of_steps'])*Decimal('.016')==Decimal(str(credit['delta_usd'])),label+': tariff/wallet mismatch');cost+=amount
   grades.append({'agent':agent,'attempt':n,'confirmed':len(correct),'incorrect':len(incorrect),'unverified':len(unknown),'outcome':grade['outcome']})
 budget=load(ROOT/'reconciled-budget.json');check(cost==Decimal('.984368'),'Known cost reconciliation')
 check(cost+Decimal('.465')==Decimal(str(budget['accounted_total_including_uncertainty_usd']))<2,'Uncertainty-adjusted cap')
 check(images==76 and htmls==47 and generations==26,'Evidence inventory changed')
 check(len(data['new_attempts'])==6,'Six actual attempts required')
 check(data['aggregate']['claude']['verified_full_passes']==3 and data['aggregate']['tinyfish']['verified_full_passes']==0,'Aggregate full passes')
 rejected=load(ROOT/'infrastructure-rejections/tinyfish-before-run-1/submission.json');check(rejected['http_status']==403 and not rejected['body'].get('run_id'),'Pre-agent rejection lost')
 for i in load(ROOT/'source-provenance.json')['files']:
  f=REPO/i['public_file'];check(f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest()==i['public_sha256'],'Public copy hash: '+i['public_file'])
 return {'passed':not errors,'provider_requests':0,'new_actual_agent_runs':6,'claude_raw_generations_audited':generations,'new_images':images,'new_html_captures':htmls,'known_mixed_cost_usd':str(cost),'uncertain_cost_reserved_usd':'.465','budget_accounted_usd':str(cost+Decimal('.465')),'grades':grades,'field_regrade_basis':'Independent manual visual observations plus complete saved traces; code recomputes scores/costs/integrity, not image recognition','errors':errors}
if __name__=='__main__':
 x=verify();print(json.dumps(x,indent=2));raise SystemExit(not x['passed'])
