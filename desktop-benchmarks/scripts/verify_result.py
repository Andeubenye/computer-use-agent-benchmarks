"""Read-only independent CSV audit. GUI checks require cited post-run observations."""
from pathlib import Path
import csv,hashlib,json,argparse
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
 with p.open(newline='',encoding='utf-8-sig') as f:return list(csv.reader(f))
def verify(folder,observations=None,submitted=True):
 folder=Path(folder);original=folder/'orders_to_fix.csv';corrected=folder/'orders_corrected.csv';src=ROOT/'inputs/orders_to_fix.csv';expected=ROOT/'expected/orders_corrected.csv';obs=observations or {}
 if not submitted:return {'outcome':'NOT TESTED','score':None,'checks':[None]*5,'reason':'No valid agent task was submitted','corrected_file_exists':corrected.exists()}
 actual=rows(corrected) if corrected.exists() else None;truth=rows(expected);input_rows=rows(src)
 edits=actual is not None and len(actual)==len(truth) and all(len(a)==len(b) for a,b in zip(actual,truth)) and actual[3][4]=='Pending' and actual[7][4]=='Pending' and all(row[4]!='Pendng' for row in actual[1:])
 untouched=False
 if actual is not None and len(actual)==len(input_rows):
  untouched=all(len(a)==len(b) and all(x==y for j,(x,y) in enumerate(zip(a,b)) if not(i in [3,7] and j==4)) for i,(a,b) in enumerate(zip(actual,input_rows)))
 original_preserved=original.exists() and sha(original)==sha(src)
 def evidence_check(name):
  entry=obs.get(name,{})
  return entry.get('verified') is True and bool(entry.get('evidence')) and all((ROOT/p).is_file() for p in entry.get('evidence',[]))
 checks=[evidence_check('opened_csv_in_spreadsheet'),edits,untouched,corrected.exists() and original_preserved,evidence_check('reopened_saved_csv_and_verified')]
 outcome='PASS' if all(checks) else 'PARTIAL' if corrected.exists() and edits else 'FAIL'
 return {'outcome':outcome,'score':sum(bool(x) for x in checks),'checks':dict(zip(['opened_in_spreadsheet','both_status_corrections','other_values_and_row_order_preserved','separate_corrected_csv_and_original_preserved','reopened_saved_file_and_verified'],checks)),'parsed_output_exactly_matches_expected':actual==truth,'original_sha256':sha(original) if original.exists() else None,'expected_original_sha256':sha(src),'corrected_sha256':sha(corrected) if corrected.exists() else None,'gui_observations':obs,'agent_response_used_as_proof':False,'verifier_edits_files':False,'csv_formatting_note':'Compare parsed values, not quoting or line endings; original file must remain byte-identical.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('folder',type=Path);p.add_argument('--observations',type=Path);p.add_argument('--not-submitted',action='store_true');a=p.parse_args()
 obs=json.loads(a.observations.read_text()) if a.observations else None
 print(json.dumps(verify(a.folder,obs,not a.not_submitted),indent=2))
