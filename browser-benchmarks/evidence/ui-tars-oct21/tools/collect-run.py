import pathlib,json,re,sys,datetime,urllib.parse
r=pathlib.Path(__file__).resolve().parents[1];workspace=r.parent;p=r/sys.argv[1]
sub=json.loads((p/'submission.json').read_text());raw=(workspace/'outputs/ui-tars-desktop-test-reopen-2026-10-21/application-logs/main.log').read_bytes();start=sub['log_offset'];end=len(raw)
for f in r.glob('test-*/submission.json'):
 other=json.loads(f.read_text())['log_offset']
 if start<other<end:end=other
s=raw[start:end].decode(errors='replace')
terminal_end=re.search(r'\[runAgent Totoal cost\]:[^\n]*\n',s)
if terminal_end:s=s[:terminal_end.end()]
c=json.loads((workspace/'work/ui-tars-dev-profile-continuation-2026-10-20/ui_tars.setting.json').read_text())
for value in [c.get('vlmApiKey'),c.get('vlmBaseUrl'),urllib.parse.urlparse(c.get('vlmBaseUrl','')).hostname]:
 if value:s=s.replace(value,'[REDACTED]')
(p/'execution-trace.txt').write_text(s)
responses=re.findall(r'\[GUIAgent\] Response: (.*?)(?=\n\[\d{4}-|$)',s,re.S);(p/'original-responses.txt').write_text('\n\n'.join(responses))
terminal=re.search(r'\[([^\]]+)\] \[info\]\s+\[GUIAgent\] Finally: status (\S+)',s)
end_time=datetime.datetime.fromisoformat(terminal[1]).replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1))) if terminal else datetime.datetime.now(datetime.timezone.utc)
result={'task':sub['task_id'],'elapsed_seconds':round((end_time-datetime.datetime.fromisoformat(sub['submitted_at_utc'].replace('Z','+00:00'))).total_seconds(),3),'terminal':terminal[2] if terminal else None,'actions':re.findall(r'\[GUIAgent\] Action: (\w+)',s),'sdk_invocations':s.count('[UITarsModel] invoke:'),'model_responses':len(responses),'last_model_response':responses[-1] if responses else 'Not measured'}
(p/'latest-metrics.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
