"""Create only benchmark inputs and grader-only expected output, never agent output."""
from pathlib import Path
import csv,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
PROMPT="Open orders_to_fix.csv in a desktop spreadsheet application. Find and correct both instances of 'Pendng' to 'Pending'. Do not change any other values or the order of the rows. Save the corrected file as orders_corrected.csv in the same folder, preserving the original file. Reopen the saved file to verify both corrections, then report what you changed and where you saved it. Do not use a web browser, terminal, scripts, or programmatic file-editing tools to complete the task."
ROWS=[
 ['order_id','customer','item','quantity','status','notes'],
 ['ORD-1001','Avery Lane','Notebook','2','Pending','Standard delivery'],
 ['ORD-1002','Jordan Reed','Desk lamp','1','Shipped','Handle with care'],
 ['ORD-1003','Casey Park','Cable, USB-C','3','Pendng','Gift packaging'],
 ['ORD-1004','Morgan Quinn','Folder','4','Delivered','Leave at reception'],
 ['ORD-1005','Riley West','Keyboard','1','Cancelled','Customer cancelled'],
 ['ORD-1006','Taylor Gray','Mouse pad','2','Pending','No changes requested'],
 ['ORD-1007','Sam Ellis','Pen set','5','Pendng','Standard delivery'],
 ['ORD-1008','Alex Rowan','Monitor stand','1','Shipped','Fragile'],
 ['ORD-1009','Jamie Brooks','Stapler','2','Delivered','Complete'],
 ['ORD-1010','Drew Blake','Envelope pack','1','Pending','Standard delivery']]
def write_csv(p,rows):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',newline='',encoding='utf-8') as f:csv.writer(f,lineterminator='\n').writerows(rows)
def main():
 src=ROOT/'inputs/orders_to_fix.csv'
 if src.exists():
  with src.open(newline='') as f:assert list(csv.reader(f))==ROWS,'Preserve an existing different fixture'
 else:write_csv(src,ROWS)
 expected=[r.copy() for r in ROWS]
 for row in expected[1:]:
  if row[4]=='Pendng':row[4]='Pending'
 write_csv(ROOT/'expected/orders_corrected.csv',expected)
 (ROOT/'inputs/task-prompt.txt').write_text(PROMPT,encoding='utf-8')
 manifest={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'expected_sha256':hashlib.sha256((ROOT/'expected/orders_corrected.csv').read_bytes()).hexdigest(),'prompt_sha256':hashlib.sha256(PROMPT.encode()).hexdigest(),'data_rows':10,'status_column':'status','misspelled_status_count':2,'expected_changed_order_ids':['ORD-1003','ORD-1007'],'expected_file_is_grader_only':True,'real_personal_data':False}
 (ROOT/'inputs/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps(manifest))
if __name__=='__main__':main()
