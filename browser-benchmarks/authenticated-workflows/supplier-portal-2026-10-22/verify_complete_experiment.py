"""Offline independent replay of both protocol phases. No network or task execution."""
from pathlib import Path
from decimal import Decimal
import json,hashlib,re,importlib.util,ast,statistics
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2];NEW=ROOT/'uncapped-followup'
def load(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify():
 spec=importlib.util.spec_from_file_location('supplier_pilots',ROOT/'verify_authenticated.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);pilots=m.verify();errors=['Pilot: '+x for x in pilots['errors']]
 def check(ok,message):
  if not ok:errors.append(message)
 combined=load(ROOT/'combined-results.json');new=load(NEW/'results.json');rows=new['new_attempts'];final=load(NEW/'final-server-records.json');native=load(NEW/'final-native-suppliers.json');db={x['id']:x for x in native['rows']};template=(ROOT/'task-template.txt').read_text();fixtures=load(ROOT/'fixtures.json');known=Decimal(0);images=generations=0;grades=[]
 check(len(rows)==6 and len(db)==20 and not native['has_more'],'New run/DB inventory')
 check([(r['agent'],r['attempt']) for r in rows]==[('tinyfish',4),('tinyfish',5),('tinyfish',6),('claude',4),('claude',5),('claude',6)],'New order differs')
 check(new['per_run_spending_limit_usd'] is None and new['cumulative_spending_limit_usd'] is None,'Custom spending limit remains')
 check((NEW/'task-template.txt').read_text()==template,'New template changed')
 for row in rows:
  label=f"{row['agent']}-{row['attempt']}";f=ROOT/row['evidence'];run=load(f/'run-record.json');v=load(f/'server-verification.json');record=v['record'];note=fixtures['notes_by_pair'][str(row['attempt'])];prompt=template.format(url='https://manicule-supplier-benchmark-oct22.peppyshark33.chatgpt.site',record=row['record_id'],note=note);events=v['events_during_attempt'];views=[e for e in events if e['kind']=='authenticated_view'];saves=[e for e in events if e['kind']=='supplier_saved'];pics=list(f.rglob('*.png'))+list(f.rglob('*.jpg'));images+=len(pics)
  check((f/'task-prompt.txt').read_text()==prompt,label+': prompt changed')
  check(load(f/'configuration.json')['per_run_limit_usd'] is None and load(f/'configuration.json')['cumulative_limit_usd'] is None,label+': custom spending cap')
  check(record==final[record['id']]['record']==db[record['id']],label+': native DB mismatch')
  check(load(f/'baseline-server-record.json')['record']['status']=='Pending',label+': baseline changed')
  check(run['agent_wall_seconds']==row['agent_seconds']<601 and run['automatic_restarts']==0,label+': deadline/restart')
  # Small terminal-poll overhead, if any, is retained; server execution deadline stays 600.
  check(not (f/'budget-cancel.json').exists() and not run.get('budget_stopped'),label+': artificial spending stop')
  original=(f/'original-response.txt').read_text();claim=m.claim(original);returned=bool(claim and claim['record_id']==record['id'] and claim['final_status']=='Reviewed' and claim['confirmation_id']==record['confirmation_id']);saved=record['status']=='Reviewed' and record['notes']==note and record['version']>=1;correct=bool(saved and any(e['record_id']==record['id'] and e['session_hash'] in {x['session_hash'] for x in views} for e in saves));amount=Decimal(0)
  if row['agent']=='tinyfish':
   payload=load(f/'actual-submission-payload.json');provider=load(f/'provider-run.json');terminal=provider['status']=='COMPLETED' and not run['deadline_fired'];check(provider['profile_attached'] and payload['use_profile'] and not payload['use_vault'],label+': profile unavailable')
   check(payload['goal']==prompt and provider['goal']=='Navigate to '+payload['url']+' to complete the goal: '+prompt,label+': actual goal changed')
   check(payload['agent_config']=={'max_duration_seconds':600} and payload['browser_profile']=='lite',label+': provider config changed')
   answer=provider['result'] if isinstance(provider['result'],str) else json.dumps(provider['result'],ensure_ascii=False,indent=2);check(original==answer,label+': original response changed')
   if terminal:
    amount=Decimal(provider['num_of_steps'])*Decimal('.016');check(amount==Decimal(str(row['comparison_cost_usd']))==Decimal(str(load(f/'wallet-observation.json')['delta_usd'])),label+': TinyFish cost mismatch')
   else:check(row['comparison_cost_usd'] is None,label+': uncertain non-completed cost treated as known')
  else:
   native_dir=next((f/'native-evidence').glob('*/summary.json')).parent;s=load(native_dir/'summary.json');responses=[load(x) for x in sorted((native_dir/'responses').glob('*.json'))];generations+=len(responses)
   for r in responses:
    u=r['usage'];cache=u.get('cache_creation') or {};one=int(cache.get('ephemeral_1h_input_tokens',0) or 0);five=int(u.get('cache_creation_input_tokens',0) or 0)-one
    amount+=(Decimal(u.get('input_tokens',0))*2+Decimal(u.get('output_tokens',0))*10+Decimal(u.get('cache_read_input_tokens',0))*Decimal('.1')+Decimal(five)*Decimal('2.5')+Decimal(one)*4)/1000000
   check(amount==Decimal(s['api_cost_usd'])==Decimal(str(row['comparison_cost_usd'])),label+': raw tokens/cost mismatch');check(original==s['final_answer'],label+': original response changed')
   check(s['budget_usd']=='Infinity' and s['max_seconds']==600 and s['max_tokens']==4096,label+': custom spend cap/config changed')
   check(s['model_requested']==s['model_returned']=='claude-sonnet-5-5' and s['tool_version']=='computer_toolset_20260801',label+': model/tool changed')
   check(s['api_retries']==0 and len(responses)==s['api_attempts'],label+': request/retry inventory');terminal=s['last_stop_reason']=='end_turn' and not s['error_category'];check(load(native_dir/'task.json')['prompt']==prompt,label+': actual native prompt')
  known+=amount
  checks={'authentication_succeeded':bool(views),'setup_session_reused':bool(views) and all(e['session_hash']==v['expected_setup_session_hash'] for e in views),'correct_supplier_viewed':any(e.get('record_id')==record['id'] for e in views),'exact_status_and_note_saved':correct,'valid_server_confirmation':bool(re.fullmatch(r'CNF-[A-F0-9]{16}',record['confirmation_id'] or '')),'returned_fields_match_server':returned,'no_other_supplier_saved':all(e['record_id']==record['id'] for e in saves),'agent_completed_within_limits':terminal,'gui_evidence_retained':bool(pics)}
  success=all(value for key,value in checks.items() if key!='setup_session_reused');check(checks==row['checks']==v['checks'] and success==row['success'],label+': independent grade differs')
  check(all(e['kind']!='login_ok' for e in events),label+': timed login occurred');check(len(pics)==row['screenshots'],label+': image count');grades.append({'agent':row['agent'],'attempt':row['attempt'],'full_workflow':success,'correct_save':correct,'session_reused':checks['setup_session_reused']})
 # Seven old non-QA saves plus any new saves; all generated IDs must be distinct.
 audit=load(NEW/'final-audit.json')['events'];receipts=[json.loads(x['details'])['confirmation_id'] for x in audit if x['kind']=='supplier_saved'];check(len(receipts)==len(set(receipts)),'Duplicate generated receipt')
 before=load(ROOT/'evidence/final-server-records.json')
 for key,old in before.items():
  if int(key[-3:])<=3:check(old['record']==final[key]['record'],'Pilot record overwritten: '+key)
  if int(key[-3:])>=7:check(final[key]['record']['status']=='Pending' and not final[key]['record']['notes'],'Unrequested fixture changed: '+key)
 check(len(combined['actual_attempts'])==12 and all(sum(r['agent']==a for r in combined['actual_attempts'])==6 for a in ['tinyfish','claude']),'Unequal attempt totals')
 for phase,items in [('uncapped_followup',rows),('all_attempts',combined['actual_attempts'])]:
  for a in ['tinyfish','claude']:
   rs=[r for r in items if r['agent']==a];ag=combined['aggregate'][phase][a];count=sum(r['success'] for r in rs);cost=sum(Decimal(str(r['comparison_cost_usd'] or 0)) for r in rs)
   check(count==ag['complete_workflows'] and cost==Decimal(str(ag['known_api_cost_usd'])),phase+': aggregate mismatch '+a)
   if count:check(abs(Decimal(str(ag['cost_per_verified_workflow_known_usd']))-cost/count)<=Decimal('.0000005'),phase+': cost/success mismatch '+a)
 check(load(NEW/'session-cleanup.json')['both_session_revocations_verified'],'New sessions not revoked')
 check(load(NEW/'infrastructure-cleanup.json')['colima_stop_exit_code']==0,'Local VM not stopped')
 for x in load(NEW/'source-provenance.json')['files']:check(digest(REPO/x['public_file'])==x['public_sha256'],'New public evidence bytes changed: '+x['public_file'])
 change=load(NEW/'core-change-audit.json');core=NEW/'harness/executed-source/uncapped_core.py';check(digest(core)==change['new_source_sha256'],'Executed new core changed');source=core.read_text();check('spent + reservation > limits.budget_usd' not in source and 'call_cost > reservation or spent > limits.budget_usd' not in source,'Cost-based interruption remains')
 check(load(NEW/'visual-review.json')['all_run_images_reviewed']==images,'New visual review inventory')
 return {'passed':not errors,'provider_requests':0,'actual_agent_runs':12,'new_actual_agent_runs':6,'new_full_workflows':sum(r['success'] for r in rows),'new_correct_saves':sum(r['data_saved'] for r in rows),'new_run_images':images,'new_setup_images':2,'new_claude_generations_audited':generations,'new_known_api_estimates_usd':str(known),'old_known_api_estimates_usd':pilots['known_api_estimates_usd'],'unresolved_pilot_accounting_reserve_usd':'1.20','new_grades':grades,'errors':errors}
if __name__=='__main__':
 result=verify();print(json.dumps(result,indent=2));raise SystemExit(not result['passed'])
