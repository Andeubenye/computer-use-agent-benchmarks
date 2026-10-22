"""Static source inventory only. Never imports integration modules or contacts providers."""
from pathlib import Path
import ast,hashlib,io,json,tokenize
ROOT=Path(__file__).resolve().parents[1]
UNITS=[
 ('TinyFish','async adapter','harness/executed-source/tinyfish-adapter-original.py',None),
 ('TinyFish','provider wrapper slices','uncapped-followup/harness/executed-source/run_workflows.py',[(46,47),(62,92)]),
 ('TinyFish','authenticated profile setup','uncapped-followup/harness/executed-source/setup_tinyfish_profile.py',None),
 ('Claude','effective instrumented native core','uncapped-followup/harness/executed-source/uncapped_core.py',None),
 ('Claude','Docker bridge and lifecycle','harness/executed-source/claude/desktop.py',None),
 ('Claude','native GUI action executor','harness/executed-source/claude/native-action.py',None),
 ('Claude','authenticated context setup','uncapped-followup/harness/executed-source/setup_claude_context.py',None),
 ('Claude','provider wrapper slices','uncapped-followup/harness/executed-source/run_workflows.py',[(48,52),(93,119)]),
 ('Claude','desktop startup script','engineering-audit/source/claude-start.sh',None),
 ('Claude','desktop image recipe','engineering-audit/source/claude-Dockerfile',None),
 ('Claude','imported grading and redaction helpers','engineering-audit/source/claude-evaluation.py',None),
 ('Shared','legacy initialization and HTTP/redaction/capture utilities actually reused','harness/executed-source/common-original.py',[(1,7),(9,38),(66,76)]),
 ('Shared','owner verifier and setup credential client','uncapped-followup/harness/executed-source/fixture_client.py',None),
 ('Shared','RAM credential broker','harness/executed-source/credential-broker.py',None),
 ('Shared','remaining batch driver incl prompt/verification','uncapped-followup/harness/executed-source/run_workflows.py','complement'),
 ('Historical Claude only','earlier Mac provisioning recipe; not rerun','engineering-audit/source/claude-setup-mac.sh',None),
]
def measure(path,ranges=None):
 text=path.read_text();lines=text.splitlines();selected=set(range(1,len(lines)+1)) if ranges is None else {i for a,b in ranges for i in range(a,b+1)}
 is_python=path.suffix=='.py';statements=None
 if is_python:
  tree=ast.parse(text);doclines=set()
  for node in ast.walk(tree):
   if isinstance(node,(ast.Module,ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)) and node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str):doclines.update(range(node.body[0].lineno,node.body[0].end_lineno+1))
  ignored={tokenize.COMMENT,tokenize.ENCODING,tokenize.NL,tokenize.NEWLINE,tokenize.INDENT,tokenize.DEDENT,tokenize.ENDMARKER};bearing=set()
  for token in tokenize.generate_tokens(io.StringIO(text).readline):
   if token.type not in ignored:bearing.update(i for i in range(token.start[0],token.end[0]+1) if i not in doclines)
  statements=sum(isinstance(n,ast.stmt) and n.lineno in selected and not (isinstance(n,ast.Expr) and n.lineno in doclines) for n in ast.walk(tree))
 else:bearing={i for i,s in enumerate(lines,1) if s.strip() and not s.lstrip().startswith('#')}
 return {'physical_lines_including_blanks_comments':len(selected),'code_bearing_physical_lines':len(selected&bearing),'python_ast_statements':statements,'selected_ranges':ranges or [[1,len(lines)]],'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
def inventory():
 rows=[];provider_ranges=[(46,52),(62,92),(93,119)]
 for provider,role,file,ranges in UNITS:
  if ranges=='complement':
   excluded={i for a,b in provider_ranges for i in range(a,b+1)};ranges=[(i,i) for i in range(1,len((ROOT/file).read_text().splitlines())+1) if i not in excluded]
  rows.append(dict(provider=provider,role=role,file=file,**measure(ROOT/file,ranges)))
 totals={p:{'source_units':sum(r['provider']==p for r in rows),'physical_lines':sum(r['physical_lines_including_blanks_comments'] for r in rows if r['provider']==p),'code_bearing_physical_lines':sum(r['code_bearing_physical_lines'] for r in rows if r['provider']==p),'python_ast_statements':sum(r['python_ast_statements'] or 0 for r in rows if r['provider']==p)} for p in ['TinyFish','Claude','Shared','Historical Claude only']}
 return {'method':'Unique effective source slices; physical lines, tokenizer-based Python code-bearing lines excluding comments/docstrings, nonblank noncomment shell/Docker lines. AST statement counts are separate. No production-minimum or labor-hour claim.','new_agent_requests':0,'units':rows,'totals':totals,'not_in_totals':['Shared portal, schema and build/deployment sources','Report packaging, graders and publication scripts','SDK/dependency implementation code','Historical bootstrap is separately subtotaled; existing lockfile/manifest/CLI are not active runtime code','Old pilot core is not double-counted with effective uncapped core','Other providers and obsolete common.py ledger/claim are excluded']}
if __name__=='__main__':print(json.dumps(inventory(),indent=2))
