"""Summarize retained run records and independent verification; never executes tasks."""
from pathlib import Path
import json, datetime

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
records=[]
for p in sorted((ROOT/'logs').rglob('run-record.json')):
    x=load(p);x['evidence_folder']=str(p.parent.relative_to(ROOT))
    if x.get('agent')=='sai':continue
    verification=p.parent/'independent-verification.json'
    v=load(verification) if verification.exists() else None
    x['verification']=v
    records.append(x)
def attempt_order(r):
    folder=r['evidence_folder']
    task=int(folder.split('/task-')[1].split('/')[0]) if '/task-' in folder else 1
    attempt=int(folder.rsplit('/attempt-',1)[1]) if '/attempt-' in folder else (2 if folder=='logs/claude-attempt-2' else 1)
    return task,r['agent'],attempt
records.sort(key=attempt_order)
byfolder={r['evidence_folder']:r for r in records}
titles=['Desktop CSV editing','File organization','Document editing','Cross-application reporting','Desktop error recovery']
evaluations=[]
for task,title in enumerate(titles,1):
    for agent in ['claude','openai']:
        base='logs/'+agent if task==1 else f'logs/{agent}/task-{task}'
        if task==1 and agent=='claude':base='logs/claude-attempt-2'
        candidates=[r for r in records if r['evidence_folder']==base or r['evidence_folder'].startswith(base+'/attempt-')]
        run=max(candidates,key=lambda x:int(x['evidence_folder'].rsplit('/attempt-',1)[1]) if '/attempt-' in x['evidence_folder'] else 1) if candidates else None
        if run and run.get('submitted'):
            v=run['verification']
            outcome=v['outcome'] if v else 'UNVERIFIED'
            score=v.get('score') if v else None
        else:outcome='NOT TESTED / BLOCKED';score=None
        evaluations.append({'task':task,'title':title,'agent':agent,'outcome':outcome,'score':score,'run':run})
    if task>1:evaluations.append({'task':task,'title':title,'agent':'sai','outcome':'NOT TESTED / BLOCKED','score':None,'reason':'Authorized control recheck HTTP 403: Not authorized for this machine. No task submitted.','run':None})
known=sum(x.get('estimated_api_cost_usd',0) for x in records)
reserved=sum(x.get('uncertain_cost_reserved_usd',0) for x in records)
ledger={'budget_cap_usd':7,'estimated_total':round(known,7),'uncertain_reserved_usd':round(reserved,7),'remaining_conservative_allowance':round(7-known-reserved,7),'provider_invoice_reconciled':False,'new_paid_infrastructure':0,'assistant_purchases_or_topups':False,'user_credit_topup_did_not_reset_cap':True,'scope':'Desktop benchmark only, including both historical Claude CSV attempts and every additional attempt.','by_agent':{a:round(sum(x.get('estimated_api_cost_usd',0) for x in records if x['agent']==a),7) for a in ['claude','openai','sai']}}
write(ROOT/'logs/cost-ledger.json',ledger)
write(ROOT/'logs/final-evaluations.json',{'planned_evaluations':14,'task_definitions':'TASKS.md','csv_rubric_changed':False,'additional_tasks_reconstructed_with_authorization':True,'evaluations':evaluations})
def cell(e):
    value=e['outcome']+(f" {e['score']}/5" if e['score'] is not None else '')
    if e['agent']=='claude' and e['task']==5:value+=' on labeled retry; first attempt PARTIAL 4/5'
    if e['agent']=='claude' and e['task']==2:value+='; executor interrupted retry'
    return value
def money(n):return f'${n:.7f}'.rstrip('0').rstrip('.')
table=['| Task | Claude | OpenAI | Sai |','|---|---|---|---|']
for n,t in enumerate(titles,1):
    es={x['agent']:x for x in evaluations if x['task']==n}
    table.append('| '+t+' | '+cell(es['claude'])+' | '+cell(es['openai'])+' | '+(cell(es['sai']) if n>1 else 'Earlier access-blocked; no new CSV run')+' |')
comparison='\n'.join(table)
attempts=['| Attempt | Outcome / stop reason | Time seconds | Actions | Images | Estimated API cost |','|---|---|---:|---:|---:|---:|']
for x in records:
    label=x['evidence_folder'].removeprefix('logs/')
    outcome=x['verification']['outcome'] if x['verification'] else ('BLOCKED before submission' if not x.get('submitted') else 'UNVERIFIED')
    secs=x.get('wall_clock_duration_seconds',x.get('duration_seconds'))
    timing=f'{secs:.2f}' if secs is not None else '—'
    if label=='claude-attempt-2':timing='397.54 UTC / 183.18 stopwatch'
    attempts.append(f"| [{label}]({x['evidence_folder']}/run-record.json) | {outcome}; {x.get('reason')} | {timing} | {x.get('actions','—')} | {x.get('screenshots_saved','—')} | {money(x.get('estimated_api_cost_usd',0))} |")
attempt_table='\n'.join(attempts)
result='''# Desktop benchmark results

All task decisions came from the providers' native computer tools. Expected artifacts stayed outside the agent desktops. Independent artifact checks and cited GUI observations determine outcomes; agent claims alone do not count.

'''+comparison+'\n\n## Every attempt and its cost\n\n'+attempt_table+f'''

Estimated cumulative spending: **{money(known)} of $7**. Uncertain request reservations: **{money(reserved)}**. Remaining conservative allowance: **{money(7-known-reserved)}**. These are token-usage estimates, not reconciled invoices. No paid infrastructure was provisioned.

## Evidence and interpretation

- Original responses, native actions, provider usage, errors and screenshots remain under each attempt folder. `independent-verification.json` contains the scored checks and cited GUI evidence. `artifact-verification.json` is a provisional read-only audit and does not replace the final GUI review.
- OpenAI's CSV run is PASS, 5/5: both edits, unchanged original, separate correct CSV, and reopened-file verification. Its actual output is `outputs/openai/orders_corrected.csv`; its parsed values and byte hash match the expected CSV.
- Claude's historical CSV repair attempt remains PARTIAL, 4/5. It saved an exactly correct file but stopped on a token-count timeout at the reopening dialog. Its interim last text is not a completed final response. The earlier HTTP 400 harness failure is retained and charged in the total.
- Mac power logs show sleep/wake events during the historical Claude CSV timeout. They strongly support host sleep as the explanation for most of its 214.36-second clock discrepancy. Preserve both clocks; exclude that run from comparative speed claims. New runs use both clocks and a temporary process-scoped idle-sleep inhibitor.
- The first additional Claude file-organization setup failed before generation due to a staging-directory readiness race. A single announced repair explicitly created the folder; its retry is retained separately. That retry later stopped on an executor drag error. No third attempt was made. Its files and partial work remain in the evidence.
- Claude's first error-recovery attempt saved the correct document and reopened it, but the local $1 request-reservation guard stopped the next generation before the model could review that screenshot. Its workflow remains PARTIAL, 4/5. On resume, one explicitly labeled infrastructure retry used a $1.75 local allowance from the unchanged $7 balance. It completed all five requirements. Both attempts and both costs remain in the tables; the original artifact was not regenerated or replaced.
- OpenAI's cross-application report had already finished when this resume began. Its retained artifact and GUI trace pass all five requirements. It was verified, not rerun. OpenAI's error-recovery run also finished in the previous queue and was verified without rerunning it.
- OpenAI's CSV and organization runs preceded the click-modifier adapter correction. Their outputs and required GUI workflows pass, but optional SHIFT/CTRL clicks were dropped, confounding action counts and duration. Subsequent tasks use the corrected translation. The two early passes were not repeated.
- Sai's authorized direct-control recheck returned HTTP 403, `forbidden`, “Not authorized for this machine.” No additional Sai task was submitted. This is an account/credential access limitation on the tested route, not a measured failure to perform the desktop tasks. No bypass or ownership takeover was attempted.
- Tasks 2–5 were reconstructed and frozen under the user's latest authorization because complete historical definitions were not recovered. Their prompts, fixture hashes and five-point criteria are in TASKS.md. They are not claimed to reproduce unknown earlier files exactly.
- UI-TARS was not operated. Earlier browser evidence and counts are separate and unchanged.

See [methodology](METHODOLOGY.md), [comparison](COMPARISON.md), [cost analysis](COST-COMPARISON.md), [article section](ARTICLE-READY.md), and `logs/final-evaluations.json` for machine-readable results.
'''
(ROOT/'RESULTS.md').write_text(result)
(ROOT/'COMPARISON.md').write_text('# Matched desktop task comparison\n\n'+comparison+'''

Scores describe five task-specific requirements, not general agent accuracy. A correct file can coexist with an unfinished GUI workflow. Access-blocked runs have no score. Infrastructure-interrupted attempts are explicitly identified in RESULTS.md and must not be treated as clean model capability failures.

| Configuration | Requested and returned model alias | Native interface |
|---|---|---|
| Claude | claude-sonnet-5-5 | Messages, computer_toolset_20260801 |
| OpenAI | gpt-6.1-sol | Responses, computer tool |
| Sai | No model task submitted or version exposed | Control route rejected authorization |

These are provider-returned aliases, not independently identified immutable weight snapshots. Per-attempt wall time, raw action counts, screenshots and estimated costs are in RESULTS.md; response counts and token totals are independently reconciled in logs/usage-reconciliation.json.

Both models used Linux Xvfb at 1024×768, Openbox, network-isolated containers, and LibreOffice. The original CSV used the original Calc image; tasks 2–5 used a derivative adding Writer, PCManFM and Zenity. Matched additional tasks used identical frozen inputs and prompts. Recovery screenshots show the same synthetic warning over blank Calc, despite the launcher's requested Writer state. The historical Claude CSV run predates the sleep-inclusive timer repair. OpenAI CSV/organization precede a click-modifier correction. Claude recovery required one separately retained retry with a larger local allowance; this is not a first-attempt pass. This small set cannot establish general superiority, reliability, or stable speed rankings.
''')
cost=['# Cost comparison\n',f'Original cumulative cap: **$7**. Estimated spent: **{money(known)}**. Uncertain reserved: **{money(reserved)}**. Remaining conservative allowance: **{money(7-known-reserved)}**.\n','| Agent | Estimated total, including unsuccessful attempts | Verified PASS tasks | Estimated spend per verified PASS |','|---|---:|---:|---:|']
for a in ['claude','openai','sai']:
    spent=ledger['by_agent'][a];wins=sum(e['agent']==a and e['outcome']=='PASS' for e in evaluations)
    cost.append(f'| {a} | {money(spent)} | {wins} | '+(money(spent/wins) if wins else 'Not calculable; no verified PASS')+' |')
cost.extend(['\n## Per-attempt usage\n',attempt_table,'''\nOpenAI estimates use returned input/output/cache usage at Standard rates of $2/M uncached input, $0.10/M cached input, $2.50/M cache write, and $10/M output for the requested model. Anthropic estimates use the recorded Sonnet rates and returned usage. No cache tokens were reported for the historical Claude CSV attempts. See the [official OpenAI pricing](https://developers.openai.com/api/docs/pricing) and saved provider usage. Invoice reconciliation, taxes and unrelated earlier browser hosting costs are unavailable or outside this budget scope.

Cost per verified PASS includes unsuccessful attempts for the same provider and is descriptive of this small batch. It is not an estimate of production reliability or a matched cost ranking. Sai's denial produced no agent task charge. Local environment preparation used existing hardware and no paid cloud infrastructure; electricity and labor are not measured.
'''])
(ROOT/'COST-COMPARISON.md').write_text('\n'.join(cost))
print(json.dumps({'reports_written':['RESULTS.md','COMPARISON.md','COST-COMPARISON.md'],'estimated_spent':known,'remaining':7-known-reserved,'unverified_submitted_runs':[x['evidence_folder'] for x in records if x.get('submitted') and x['verification'] is None]}))
