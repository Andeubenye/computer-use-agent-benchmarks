"""Offline scan. Reports paths/counts only; never emits matched credentials."""
from pathlib import Path
import argparse, io, json, re, sys, zipfile
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from common import credential

parser=argparse.ArgumentParser()
parser.add_argument('folders', nargs='+', type=Path)
parser.add_argument('--output', type=Path, required=True)
args=parser.parse_args()
keys=[v.encode() for a in ('openai','claude','sai') if (v:=credential(a))]
patterns=[re.compile(rb'\bsk-[A-Za-z0-9_-]{24,}'),
          re.compile(rb'\b(?:sapi_|bu_|hf_|ghp_|gho_|ghu_|ghs_|ghr_|github_pat_)[A-Za-z0-9_-]{24,}')]
hits=[]; files=members=0
def inspect(data, name):
    count=sum(data.count(k) for k in keys)
    probable=sum(len(p.findall(data)) for p in patterns)
    if count or probable:hits.append({'path':name,'known_credential_occurrences':count,'credential_pattern_matches':probable})
for folder in args.folders:
    for path in sorted(folder.rglob('*')):
        if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts:continue
        if path.resolve()==args.output.resolve():continue
        data=path.read_bytes();files+=1
        name=folder.name+'/'+str(path.relative_to(folder))
        inspect(data,name)
        if zipfile.is_zipfile(io.BytesIO(data)):
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                for entry in archive.infolist():
                    if entry.is_dir():continue
                    members+=1;inspect(archive.read(entry),name+'!'+entry.filename)
result={'provider_requests':0,'credential_values_written':False,'known_credentials_loaded_in_memory':len(keys),
        'files_scanned':files,'decompressed_zip_members_scanned':members,'matches':hits,
        'passed':not hits,'scope':'Current files including decompressed DOCX/ZIP members; excludes Git internals and Python caches. Linux task screenshots contain synthetic desktop content; cited screenshots were visually reviewed separately.'}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':not hits,'files':files,'archive_members':members,'matches':hits,'known_keys_loaded':len(keys)}))
sys.exit(bool(hits))
