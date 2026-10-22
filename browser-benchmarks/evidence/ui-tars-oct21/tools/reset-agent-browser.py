import sys,subprocess,pathlib,json,signal,os,time,datetime
parent=sys.argv[1];dest=pathlib.Path(sys.argv[2]);log=pathlib.Path(sys.argv[3]).read_text()
if log.rfind('[GUIAgent] Finally: status') < log.rfind('runAgent\n'):
 raise SystemExit('Refusing browser reset while an agent run may be active')
events=[]
for line in subprocess.run(['ps','-axo','pid=,ppid=,args='],capture_output=True,text=True).stdout.splitlines():
 p=line.split(None,2)
 if len(p)==3 and p[1]==parent and p[2].startswith('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome ') and '--user-data-dir=/var/folders/' in p[2] and 'puppeteer_dev_chrome_profile-' in p[2]:
  os.kill(int(p[0]),signal.SIGTERM);events.append({'pid':int(p[0]),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'action':'closed only stopped UI-TARS temporary Chrome','personal_browser_untouched':True})
dest.write_text(json.dumps(events,indent=2)+'\n');time.sleep(.4)
print('Fresh-session reset recorded; agent-owned browsers closed:',len(events))
