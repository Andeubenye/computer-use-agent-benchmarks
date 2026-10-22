"""Offline audit of grader failure cases; synthetic test outputs are temporary only."""
import tempfile,csv,shutil,json
from pathlib import Path
from verify_result import ROOT,verify,rows
n=0
with tempfile.TemporaryDirectory() as d:
 p=Path(d);shutil.copyfile(ROOT/'inputs/orders_to_fix.csv',p/'orders_to_fix.csv')
 assert verify(p)['outcome']=='FAIL';n+=1
 shutil.copyfile(ROOT/'expected/orders_corrected.csv',p/'orders_corrected.csv')
 v=verify(p);assert v['outcome']=='PARTIAL' and v['score']==3;n+=1 # GUI workflow cannot be inferred from a correct file.
 rr=rows(p/'orders_corrected.csv');rr[1][1]='Unrequested change'
 with (p/'orders_corrected.csv').open('w',newline='') as f:csv.writer(f).writerows(rr)
 assert not verify(p)['checks']['other_values_and_row_order_preserved'];n+=1
 rr=rows(ROOT/'expected/orders_corrected.csv');rr[1],rr[2]=rr[2],rr[1]
 with (p/'orders_corrected.csv').open('w',newline='') as f:csv.writer(f).writerows(rr)
 assert not verify(p)['checks']['other_values_and_row_order_preserved'];n+=1
 shutil.copyfile(ROOT/'expected/orders_corrected.csv',p/'orders_to_fix.csv')
 assert not verify(p)['checks']['separate_corrected_csv_and_original_preserved'];n+=1
 assert verify(p,submitted=False)['score'] is None;n+=1
print(json.dumps({'offline_verifier_cases_passed':n,'agent_model_calls':0,'temporary_files_not_agent_outputs':True}))
