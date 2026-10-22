"""Offline evidence checks only. No provider calls, GUI actions or benchmark runs."""
from pathlib import Path
from decimal import Decimal
import csv, hashlib, importlib.util, io, json, re, subprocess, sys, urllib.parse, zipfile

ROOT=Path(__file__).resolve().parents[2]
ALLOWED={'claude','openai','sai','ui-tars','tinyfish'}
errors=[]
def load(p):return json.loads(p.read_text())
def check(value,message):
    if not value:errors.append(message)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

manifest=ROOT/'verification/public-manifest.json'
if manifest.exists():
    for x in load(manifest)['files']:
        f=ROOT/x['path'];check(f.is_file() and digest(f)==x['sha256'],'Manifest mismatch: '+x['path'])
else:errors.append('Public manifest missing')

links=0
for f in ROOT.rglob('*.md'):
    if '.git' in f.parts:continue
    text=re.sub(r'```.*?```','',f.read_text(),flags=re.S)
    for match in re.finditer(r'!?\[[^\]]*\]\(([^)]+)\)',text):
        url=match.group(1).strip().strip('<>')
        if url.startswith(('https:','http:','mailto:','#')):continue
        target=urllib.parse.unquote(url.split('#')[0]);links+=1
        check((f.parent/target).exists(),'Broken link: '+str(f.relative_to(ROOT))+' -> '+url)

prompts=load(ROOT/'verification/prompt-integrity.json')
for x in prompts:
    f=ROOT/x['file']
    if 'sha256' in x:check(digest(f)==x['sha256'],'Prompt bytes changed: '+x['file'])
    else:
        source=ROOT/x['source']
        task={'csv-editing':1,'file-organization':2,'document-editing':3,'cross-application-reporting':4,'error-recovery':5}[f.stem]
        prompt=source.read_text() if task==1 else load(source)[str(task)]['prompt']
        check(hashlib.sha256(prompt.encode()).hexdigest()==x['embedded_prompt_sha256'] and prompt in f.read_text(),'Frozen desktop prompt changed: '+x['file'])
for x in load(ROOT/'verification/runtime-prompt-variants.json'):
    check(hashlib.sha256(x['prompt'].encode()).hexdigest()==x['sha256'],'Runtime prompt variant hash changed')
    for source in x['sources']:check((ROOT/source).is_file(),'Runtime prompt source missing: '+source)

browser=list(csv.DictReader((ROOT/'browser-benchmarks/results/benchmark-results.csv').open()))
for r in browser:
    check(r['agent'] in ALLOWED,'Outside-scope browser configuration')
    check((ROOT/r['evidence']).is_file(),'Browser record missing: '+r['evidence'])
common=[r for r in browser if r['cohort']=='additional-20']
check(len(common)==16,'Wrong scoped common cohort size')
for status,n in [('PASS',10),('PARTIAL',4),('FAIL',2)]:check(sum(r['status']==status for r in common)==n,'Wrong common outcome count: '+status)
outcomes={'successful':'PASS','partially_successful':'PARTIAL','failed':'FAIL','PASS':'PASS','PARTIAL':'PARTIAL','FAIL':'FAIL'}
for r in common:
    f=(ROOT/r['evidence']).parent/'verification.json'
    check(f.is_file(),'Browser verification missing: '+str(f.relative_to(ROOT)))
    if f.exists():check(outcomes.get(load(f).get('outcome'))==r['status'],'Browser saved grade mismatch: '+str(f.relative_to(ROOT)))
check({f.stem for f in (ROOT/'agents').glob('*.md')}=={'claude','openai','simular-sai','ui-tars','tinyfish'},'Agent index scope mismatch')
check(not any(part.lower() in ('browser-use','browser_use') for f in ROOT.rglob('*') for part in f.relative_to(ROOT).parts),'Outside-scope evaluated-agent directory')

# Separate follow-up cohort: retain the historical browser CSV and desktop counts.
followup_path=ROOT/'browser-benchmarks/reruns/tinyfish-form-2026-10-22/verify_followup.py'
spec=importlib.util.spec_from_file_location('tinyfish_form_followup',followup_path)
followup_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(followup_module)
followup=followup_module.verify()
for error in followup['errors']:errors.append('TinyFish follow-up: '+error)

# Clarified prompt is a distinct six-run configuration, never pooled with originals.
clarified_path=ROOT/'browser-benchmarks/reruns/clarified-form-2026-10-22/verify_clarified.py'
clarified_spec=importlib.util.spec_from_file_location('clarified_form',clarified_path)
clarified_module=importlib.util.module_from_spec(clarified_spec);clarified_spec.loader.exec_module(clarified_module)
clarified=clarified_module.verify()
for error in clarified['errors']:errors.append('Clarified form: '+error)

# Authenticated-workflow pilots and explicitly amended additional runs are separate.
authenticated_path=ROOT/'browser-benchmarks/authenticated-workflows/supplier-portal-2026-10-22/verify_complete_experiment.py'
authenticated_spec=importlib.util.spec_from_file_location('authenticated_supplier',authenticated_path)
authenticated_module=importlib.util.module_from_spec(authenticated_spec);authenticated_spec.loader.exec_module(authenticated_module)
authenticated=authenticated_module.verify()
for error in authenticated['errors']:errors.append('Authenticated workflows: '+error)

# Independent read-only artifact checks; these modules contain no provider execution.
DESKTOP=ROOT/'desktop-benchmarks'
sys.path.insert(0,str(DESKTOP/'scripts'));sys.path.insert(0,str(DESKTOP/'verification'))
try:
    from verify_result import verify
    from verify_additional import audit
except ImportError:
    errors.append('python-docx required for independent DOCX regrade; install documented dependency')
    verify=audit=None
total=Decimal(0);attempts=regrades=0
for path in sorted((DESKTOP/'logs').rglob('run-record.json')):
    r=load(path)
    if r.get('agent') not in ('claude','openai'):continue
    attempts+=1;folder=path.parent;rel=folder.relative_to(DESKTOP/'logs')
    raw=[load(f) for f in sorted((folder/'responses').glob('*.json'))]
    usages=[x['usage'] for x in raw if x.get('usage')];cost=Decimal(0)
    for u in usages:
        if r['agent']=='claude':
            amount=Decimal(u.get('input_tokens',0))*2+Decimal(u.get('output_tokens',0))*10+Decimal(u.get('cache_read_input_tokens',0))*Decimal('.1')+Decimal(u.get('cache_creation_input_tokens',0))*4
        else:
            d=u.get('input_tokens_details') or {};c=d.get('cached_tokens',0);w=d.get('cache_write_tokens',0)
            amount=Decimal(u.get('input_tokens',0)-c-w)*2+Decimal(c)*Decimal('.1')+Decimal(w)*Decimal('2.5')+Decimal(u.get('output_tokens',0))*10
        cost+=amount/1000000
    check(abs(cost-Decimal(str(r.get('estimated_api_cost_usd',0))))<Decimal('.000000001'),'Raw usage cost mismatch: '+str(rel))
    check(len(raw)==r.get('model_requests',0),'Request count mismatch: '+str(rel))
    total+=cost
    if not r.get('submitted') or str(rel)=='claude' or audit is None:continue
    old=load(folder/'independent-verification.json')
    obs=load(folder/'gui-observations.json') if (folder/'gui-observations.json').exists() else old.get('gui_observations',{})
    if '/task-' in str(rel):
        task=int(str(rel).split('/task-')[1].split('/')[0]);new=audit(task,DESKTOP/'outputs'/rel,obs)
    else:new=verify(DESKTOP/'outputs'/('claude' if str(rel)=='claude-attempt-2' else rel),obs)
    check(new['score']==old['score'] and new['outcome']==old['outcome'],'Desktop artifact regrade disagrees: '+str(rel));regrades+=1
check(total==Decimal('3.6676817'),'Cumulative desktop estimate changed')
check(attempts==13 and regrades==11,'Desktop attempt/regrade inventory differs')

# Credential and private-location checks; synthetic demo passwords are task data.
patterns=[re.compile(rb'\bsk-[A-Za-z0-9_-]{24,}'),re.compile(rb'\b(?:sapi_|bu_|hf_|ghp_|gho_|ghu_|ghs_|ghr_|github_pat_)[A-Za-z0-9_-]{24,}'),re.compile(rb'/Users/[A-Za-z][A-Za-z0-9_-]+/'),re.compile(rb'https?://[A-Za-z0-9.-]+\.endpoints\.huggingface\.cloud')]
def scan(data,name):
    for pattern in patterns:
        if pattern.search(data):errors.append('Sensitive-pattern match (value suppressed): '+name);break
files=archives=0
for f in ROOT.rglob('*'):
    if not f.is_file() or '.git' in f.parts or '__pycache__' in f.parts:continue
    data=f.read_bytes();name=str(f.relative_to(ROOT));scan(data,name);files+=1
    if zipfile.is_zipfile(io.BytesIO(data)):
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for member in z.infolist():
                if not member.is_dir():scan(z.read(member),name+'!'+member.filename);archives+=1

history_blobs=0
if (ROOT/'.git').is_dir():
    result=subprocess.run(['git','-C',str(ROOT),'rev-list','--objects','--all'],capture_output=True,text=True)
    objects={line.split(' ',1)[0] for line in result.stdout.splitlines()}
    if objects:
        data=subprocess.check_output(['git','-C',str(ROOT),'cat-file','--batch'],input=('\n'.join(objects)+'\n').encode());offset=0
        while offset<len(data):
            end=data.index(b'\n',offset);head=data[offset:end].split();size=int(head[2]);start=end+1;body=data[start:start+size];offset=start+size+1
            if head[1]==b'blob':scan(body,'Git history blob '+head[0].decode());history_blobs+=1

print(json.dumps({'passed':not errors,'benchmark_requests':0,'tasks_documented':16,'historical_task_definitions':15,'new_authenticated_task_definitions':1,'scoped_browser_common_runs':16,'browser_record_rows':len(browser),'tinyfish_form_followup_runs':followup['new_runs'],'tinyfish_form_followup_cost_usd':followup['cost_usd'],'clarified_form_runs':clarified['new_actual_agent_runs'],'clarified_form_budget_with_uncertainty_usd':clarified['budget_accounted_usd'],'authenticated_workflow_attempts':authenticated['actual_agent_runs'],'authenticated_new_uncapped_runs':authenticated['new_actual_agent_runs'],'desktop_attempts':attempts,'desktop_artifact_regrades':regrades,'desktop_estimated_cost_usd':str(total),'exact_prompt_records':len(prompts),'internal_links_checked':links,'files_scanned':files,'decompressed_document_members_scanned':archives,'git_history_blobs_scanned':history_blobs,'errors':errors},indent=2))
sys.exit(bool(errors))
