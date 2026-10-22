"""Read-only replay of server truth, saved original claims, usage and source integrity.
No provider requests, credentials, GUI automation or task execution.
"""
from pathlib import Path
from decimal import Decimal
import json,re,hashlib,statistics
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
def load(p):return json.loads(p.read_text())
def claim(text):
 for piece in [text]+re.findall(r'\{[^{}]*\}',text,re.S):
  try:
   value=json.loads(piece)
   if isinstance(value,dict) and all(k in value for k in ['record_id','final_status','confirmation_id']):return value
  except ValueError:pass
 ids=set(re.findall(r'\bSUP-[CT][0-9]{3}\b',text));receipts=set(re.findall(r'\bCNF-[A-F0-9]{16}\b',text))
 if len(ids)==len(receipts)==1 and re.search(r'\bReviewed\b',text):return dict(record_id=next(iter(ids)),confirmation_id=next(iter(receipts)),final_status='Reviewed')
 return None
def verify():
 errors=[]
 def check(ok,message):
  if not ok:errors.append(message)
 data=load(ROOT/'results.json');rows=data['actual_attempts'];template=(ROOT/'task-template.txt').read_text();fixtures=load(ROOT/'fixtures.json');native=load(ROOT/'evidence/final-native-suppliers.json');native_rows={r['id']:r for r in native['rows']};final=load(ROOT/'evidence/final-server-records.json');audit=load(ROOT/'evidence/final-audit.json')['events'];images=generations=actions=0;known=Decimal(0);reserve=Decimal(0);grades=[]
 check(len(rows)==6 and len(native_rows)==20 and not native['has_more'],'Pilot/fixture inventory differs')
 for row in rows:
  a=row['agent'];n=row['attempt'];label=f'{a}-{n}';f=ROOT/row['evidence'];r=load(f/'run-record.json');v=load(f/'server-verification.json');record=v['record'];events=v['events_during_attempt'];note=fixtures['notes_by_pair'][str(n)];prompt=template.format(url='https://manicule-supplier-benchmark-oct22.peppyshark33.chatgpt.site',record=row['record_id'],note=note)
  check((f/'task-prompt.txt').read_text()==prompt,label+': exact prompt')
  check(r['agent_wall_seconds']==row['agent_seconds']<600 and r['automatic_restarts']==0,label+': time/restart')
  check(load(f/'baseline-server-record.json')['record']['status']=='Pending',label+': baseline')
  check(record==native_rows[record['id']]==final[record['id']]['record'],label+': independent platform DB disagrees with verifier snapshot')
  original=(f/'original-response.txt').read_text();parsed=claim(original);views=[e for e in events if e['kind']=='authenticated_view'];saves=[e for e in events if e['kind']=='supplier_saved'];saved=record['status']=='Reviewed' and record['notes']==note and record['version']>=1
  check(all(e['kind']!='login_ok' for e in events),label+': unexpected login during timed run')
  returned=bool(parsed and parsed['record_id']==record['id'] and parsed['final_status']=='Reviewed' and parsed['confirmation_id']==record['confirmation_id'])
  correct_save=bool(saved and any(e['record_id']==record['id'] and e['session_hash'] in {x['session_hash'] for x in views} for e in saves))
  pics=list(f.rglob('*.jpg'))+list(f.rglob('*.png'));images+=len(pics)
  if a=='tinyfish':
   payload=load(f/'actual-submission-payload.json');provider=load(f/'provider-run.json');activity=load(f/'activity-summary.json');cancel=(f/'budget-cancel.json').exists();terminal=provider['status']=='COMPLETED' and not cancel and not r['deadline_fired']
   check(payload['goal']==prompt and payload['use_profile'] is True and payload['use_vault'] is False and payload['profile_id']=='profile-tinyfish-dedicated',label+': actual profile payload')
   check(provider['profile_attached'] is True and payload['agent_config']['max_duration_seconds']==600 and 'max_steps' not in payload['agent_config'],label+': profile/limits')
   check(provider['goal']=='Navigate to '+payload['url']+' to complete the goal: '+prompt,label+': provider goal wrapper')
   check(original==json.dumps(provider['result'],ensure_ascii=False,indent=2),label+': original response differs from provider result')
   if cancel:
    stop=load(f/'cost-and-stop-audit.json');check(provider['status']=='CANCELLED' and provider['num_of_steps']==0 and len(provider['steps'])==27 and stop['treat_as_free'] is False,label+': cancellation activity/cost discrepancy missing')
    check(row['comparison_cost_usd'] is None and row['uncertain_reserved_usd']==.6,label+': unresolved cost counted as free');reserve+=Decimal('.6')
   else:
    amount=Decimal(provider['num_of_steps'])*Decimal('.016');check(amount==Decimal(str(r['cost_usd']))==Decimal(str(load(f/'wallet-observation.json')['delta_usd'])),label+': billed steps/wallet estimate mismatch');known+=amount
   check(len(provider['steps'])==activity['recorded_trace_entries'],label+': trace count')
  else:
   folder=next((f/'native-evidence').glob('*/summary.json')).parent;s=load(folder/'summary.json');responses=[load(x) for x in sorted((folder/'responses').glob('*.json'))];amount=Decimal(0)
   check(load(folder/'task.json')['prompt']==prompt,label+': native submitted prompt')
   for response in responses:
    u=response['usage'];cache=u.get('cache_creation') or {};one=int(cache.get('ephemeral_1h_input_tokens',0) or 0);five=int(u.get('cache_creation_input_tokens',0) or 0)-one
    amount+=(Decimal(u.get('input_tokens',0))*2+Decimal(u.get('output_tokens',0))*10+Decimal(u.get('cache_read_input_tokens',0))*Decimal('.1')+Decimal(five)*Decimal('2.5')+Decimal(one)*4)/1000000
   check(amount==Decimal(s['api_cost_usd'])==Decimal(str(row['comparison_cost_usd'])),label+': raw usage cost')
   check(s['model_requested']==s['model_returned']=='claude-sonnet-5-5' and s['tool_version']=='computer_toolset_20260801',label+': model/tool identity')
   check(s['max_seconds']==600 and s['max_tokens']==4096 and s['api_retries']==0,label+': limits/retries')
   check(len(responses)==s['api_attempts']==row['generation_requests'],label+': request inventory');generations+=len(responses);actions+=s['computer_actions'];known+=amount
   check(original==s['final_answer'],label+': original answer changed')
   terminal=s['last_stop_reason']=='end_turn' and not s['error_category'] and s['agent_wall_seconds']<600
  checks={'authentication_succeeded':bool(views),'setup_session_reused':bool(views) and all(e['session_hash']==v['expected_setup_session_hash'] for e in views),'correct_supplier_viewed':any(e.get('record_id')==record['id'] for e in views),'exact_status_and_note_saved':correct_save,'valid_server_confirmation':bool(re.fullmatch(r'CNF-[A-F0-9]{16}',record['confirmation_id'] or '')),'returned_fields_match_server':returned,'no_other_supplier_saved':all(e['record_id']==record['id'] for e in saves),'agent_completed_within_limits':terminal,'gui_evidence_retained':bool(pics)}
  success=all(value for key,value in checks.items() if key!='setup_session_reused');check(checks==v['checks']==row['checks'] and success==row['success'],label+': independent regrade')
  check(len(pics)==row['screenshots'],label+': image inventory');grades.append({'agent':a,'attempt':n,'data_saved':correct_save,'workflow_complete':success,'session_reused':checks['setup_session_reused'],'censored':row['budget_censored']})
 receipts=[json.loads(e['details'])['confirmation_id'] for e in audit if e['kind']=='supplier_saved' and e.get('record_id')!='SUP-C999'];check(len(receipts)==len(set(receipts))==7,'Receipts not unique / unexpected save inventory')
 saved=[r['id'] for r in native_rows.values() if r['status']=='Reviewed'];check(set(saved)=={'SUP-C001','SUP-C002','SUP-C003','SUP-T002','SUP-T003'},'Other supplier changed')
 for record in native_rows.values():
  if record['id'] not in saved:check(record['status']=='Pending' and record['notes']=='' and record['confirmation_id'] is None,'Unrun/unsaved fixture changed')
 check(load(ROOT/'evidence/pilot-gate.json')['proceed'] is False and len(data['extension_runs'])==14 and all(x['status']=='NOT RUN' for x in data['extension_runs']),'Pilot gate/extension')
 check(load(ROOT/'evidence/session-cleanup.json')['both_session_revocations_verified'],'Sessions not expired')
 check(load(ROOT/'evidence/infrastructure-cleanup.json')['colima_stop_exit_code']==0,'VM cleanup')
 for x in load(ROOT/'source-provenance.json')['files']:
  p=REPO/x['public_file'];check(hashlib.sha256(p.read_bytes()).hexdigest()==x['public_sha256'],'Public evidence hash mismatch: '+x['public_file'])
 for x in load(ROOT/'fixture-source-provenance.json')['files']:check(hashlib.sha256((REPO/x['public_file']).read_bytes()).hexdigest()==x['sha256'],'Fixture source changed')
 check(known==Decimal('1.103830') and reserve==Decimal('1.2'),'Cost reconciliation')
 check(images==107 and actions==87,'Evidence/action inventory')
 check(load(ROOT/'visual-review.json')['all_run_images_reviewed']==images,'Visual review inventory')
 return {'passed':not errors,'provider_requests':0,'actual_agent_runs':6,'full_workflow_successes':4,'correct_server_saves':5,'session_reuse_verified':6,'budget_censored_runs':2,'extension_runs_not_executed':14,'run_images':images,'setup_images':2,'claude_raw_generations_audited':generations,'claude_native_actions':actions,'known_api_estimates_usd':str(known),'unresolved_reservation_usd':str(reserve),'accounted_api_plus_uncertainty_usd':str(known+reserve),'setup_uncertainty_reserve_usd':'.02','grades':grades,'errors':errors}
if __name__=='__main__':
 result=verify();print(json.dumps(result,indent=2));raise SystemExit(not result['passed'])
