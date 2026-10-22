import hashlib,json,re,tarfile,zipfile
from pathlib import Path
root=Path.cwd();out=root/'outputs/manicule-benchmarks-tasks-2-5';keys=json.loads((root/'work/manicule-batch-2-5/private-credentials.json').read_text());changes=[]
capnames={'liveurl','liveviewurl','cdpurl','websocketdebuggerurl','recordingurl','videourl','streamingurl'}
def clean(x):
 if isinstance(x,dict):return {k:('[REDACTED CAPABILITY URL]' if re.sub(r'[_-]','',k.lower()) in capnames and isinstance(v,str) and v and not v.startswith('[REDACTED') else clean(v)) for k,v in x.items()}
 if isinstance(x,list):return [clean(v) for v in x]
 if isinstance(x,str) and ('X-Amz-' in x or 'X-Goog-' in x):
  return re.sub(r'https?://[^\s\"<>\\]+',lambda m:m.group(0).split('?',1)[0]+'?[SIGNED_QUERY_REDACTED]' if '?' in m.group(0) and ('X-Amz-' in m.group(0) or 'X-Goog-' in m.group(0)) else m.group(0),x)
 return x
for p in out.rglob('*.json'):
 original=p.read_bytes()
 try:d=json.loads(original)
 except ValueError:continue
 revised=clean(d)
 if revised!=d:
  p.write_text(json.dumps(revised,indent=2,ensure_ascii=False)+'\n');changes.append({'file':str(p.relative_to(out)),'before_sha256':hashlib.sha256(original).hexdigest(),'after_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'redaction':'capability URL fields or signed-query metadata; no task answer changed'})
(out/'audit/capability-url-redactions.json').write_text(json.dumps(changes,indent=2))
findings=[];pattern=re.compile(rb'(?:sk-[A-Za-z0-9_-]{15,}|bu_[A-Za-z0-9_-]{15,}|sapi_[A-Za-z0-9_-]{15,})')
for p in out.rglob('*'):
 if not p.is_file():continue
 b=p.read_bytes()
 if any(v.encode() in b for v in keys.values()) or (p.suffix in {'.json','.md','.txt','.log','.py','.jsonl'} and pattern.search(b)):findings.append(str(p.relative_to(out)))
 if p.name.endswith('.tar.gz'):
  with tarfile.open(p) as t:
   for m in t.getmembers():
    if m.isfile():
     b=t.extractfile(m).read()
     if any(v.encode() in b for v in keys.values()) or pattern.search(b):findings.append(str(p.relative_to(out))+'!'+m.name)
assert not findings,'Credential scan failed; values suppressed'
# Historical snapshot text intentionally keeps its original relative links; validate active Markdown files.
broken=[]
for p in out.rglob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if target.startswith(('http:','https:','#','mailto:')):continue
  target=target.split('#',1)[0];q=Path(target) if target.startswith('/') else p.parent/target
  if not q.exists():broken.append({'file':str(p.relative_to(out)),'link':target})
assert not broken,json.dumps(broken)
old=root/'outputs/manicule-computer-use-2026-10-17';before=json.loads((out/'preparation/original-evidence-hashes.json').read_text());assert all(hashlib.sha256((old/k).read_bytes()).hexdigest()==v for k,v in before.items())
validation={'credential_scan_passed':True,'credential_findings':0,'active_markdown_links_valid':True,'original_evidence_files_unchanged':len(before),'new_task_submissions':20,'automatic_new_benchmark_restarts':0,'package_contains_credentials':False,'screenshot_decoding':'audit/image-validation.json','metrics_and_cost_checks':'audit/metrics-validation.json','capability_url_redaction_files':len(changes)}
(out/'audit/final-validation.json').write_text(json.dumps(validation,indent=2))
manifest={str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file() and p.name!='evidence-manifest.json'}
(out/'evidence-manifest.json').write_text(json.dumps({'hash_algorithm':'SHA-256','files':manifest},indent=2))
archive=root/'outputs/manicule-complete-benchmarks-2026-10-17.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for base in [out,old]:
  for p in sorted(base.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(root/'outputs'))
 z.write(root/'outputs/MANICULE-BENCHMARK-INDEX.md','MANICULE-BENCHMARK-INDEX.md')
with zipfile.ZipFile(archive) as z:assert z.testzip() is None;count=len(z.infolist())
sha=hashlib.sha256(archive.read_bytes()).hexdigest();archive.with_suffix('.sha256.txt').write_text(sha+'  '+archive.name+'\n')
print(json.dumps({'archive':str(archive),'archive_bytes':archive.stat().st_size,'archive_files':count,'new_evidence_files':len(manifest),'prior_files_unchanged':len(before),'credential_scan':'passed','local_links':'passed','zip_integrity':'passed'},indent=2))
