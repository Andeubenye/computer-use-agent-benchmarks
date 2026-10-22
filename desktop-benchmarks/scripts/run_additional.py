"""One additional native-tool attempt. Staging and collection never solve the task."""
import argparse, hashlib, json, subprocess, tarfile, io, time
from pathlib import Path
import run_native as native
from common import ROOT, save, event, now

SYSTEM = '''You control an isolated Linux desktop at 1024 x 768 pixels. The task folder is /home/agent/Desktop/benchmark. Use only the native computer tool for task work. Open, inspect, edit, save and verify through graphical desktop applications. No terminal, browser, shell, code, scripts, macros, filesystem tools, network or programmatic editing. Spreadsheet formulas entered in the spreadsheet GUI are allowed for calculations. End each action batch with a screenshot and observe the result before proceeding. Expected outputs and grader references are not available. Do not inspect unrelated files, sign in, change settings or install software. If blocked, stop and describe the blocker. You have ten minutes from submission.'''

def run(agent, task, attempt, budget):
    specs = json.loads((ROOT/'inputs/additional/tasks.json').read_text())
    spec = specs[str(task)]
    folder = ROOT/'inputs/additional'/('task-'+str(task))
    for rel, digest in spec['input_files_sha256'].items():
        if hashlib.sha256((folder/rel).read_bytes()).hexdigest()!=digest:
            raise RuntimeError('Frozen fixture hash mismatch')
    tag = agent+'/task-'+str(task) + ('' if attempt==1 else '/attempt-'+str(attempt))
    allocation=ROOT/'preflight/budget-allocation.json'
    if allocation.exists():
        caps=json.loads(allocation.read_text()).get('task_caps_usd',{})
        configured=float(caps.get(str(task),budget))
        effective=min(max(configured,budget),7-native.recorded_spend())
        save(ROOT/'logs'/tag/'budget-allocation.json',{'queue_requested_cap':budget,'configured_initial_task_cap':configured,'effective_run_cap':effective,'cumulative_cap':7,'same_task_cap_for_both_agents':attempt==1 and budget<=configured,'explicit_repair_allowance':budget>configured,'reason':'Released allowance from earlier completed tasks; no budget reset'})
        budget=effective
    def setup(_):
        name='manicule-additional-'+agent+'-'+str(task)+'-'+str(attempt)
        if subprocess.run(native.DOCKER+['inspect',name],capture_output=True).returncode==0:
            raise RuntimeError('Existing container: no automatic restart')
        native.docker('run','--detach','--name',name,'--network','none','--init','--cap-drop','ALL','--security-opt','no-new-privileges','--memory','2g','--cpus','2','--pids-limit','256','--shm-size','256m','--label','app=manicule-desktop-csv','desktop-additional-benchmark:2026-10-21')
        runner.name=name
        for _ in range(40):
            try:
                native.docker('exec',name,'xdotool','getdisplaygeometry');break
            except subprocess.SubprocessError:time.sleep(.5)
        buf=io.BytesIO()
        with tarfile.open(fileobj=buf,mode='w') as t:
            for p in sorted(folder.rglob('*')):
                if p.is_file():t.add(p,arcname=str(p.relative_to(folder)))
        native.docker('exec',name,'mkdir','-p',native.REMOTE)
        native.docker('exec','-i',name,'tar','-xf','-','-C',native.REMOTE,data=buf.getvalue())
        # Initial application selection is environment setup only; no input opened.
        if spec['starting_app'] in ['writer','writer-interrupted']:
            native.docker('exec',name,'sh','-c','libreoffice --writer --norestore --nologo >/tmp/writer.log 2>&1 &')
        elif spec['starting_app']=='file-manager':
            native.docker('exec',name,'sh','-c','pcmanfm /home/agent/Desktop/benchmark/Inbox >/tmp/file-manager.log 2>&1 &')
        time.sleep(2)
        # Common dimensions and placement, chosen before the task timer starts.
        ids=native.docker('exec',name,'xdotool','getactivewindow').decode().strip()
        native.docker('exec',name,'xdotool','windowsize',ids,'1024','740')
        native.docker('exec',name,'xdotool','windowmove',ids,'0','0')
        if task==5:
            native.docker('exec',name,'sh','-c','(zenity --warning --title="Synthetic interruption" --text="A temporary application interruption occurred. Dismiss this notice to continue. No files were changed."; echo $? > /tmp/interruption-exit) >/tmp/interruption.log 2>&1 &')
            time.sleep(1)
            native.docker('exec',name,'xdotool','search','--name','Synthetic interruption')
        save(ROOT/'logs'/tag/'environment.json',{'utc':now(),'image':'desktop-additional-benchmark:2026-10-21','task':task,'starting_app':spec['starting_app'],'network':'none','fixtures_validated':True,'expected_output_exposed':False,'initial_interruption':task==5,'provenance':spec['provenance']})
        return name
    native.setup=setup
    runner=native.Runner(agent,seconds=600,budget=budget,tag=tag,prompt=spec['prompt'],system=SYSTEM,collect_all=True)
    if task==5:
        def observe(name):
            result=subprocess.run(native.DOCKER+['exec',name,'cat','/tmp/interruption-exit'],capture_output=True,text=True,timeout=10)
            save(ROOT/'logs'/tag/'interruption-evidence.json',{'read_after_agent_stopped':True,'read_before_container_shutdown':True,'notice_exit_recorded':result.returncode==0,'notice_exit_code':result.stdout.strip() if result.returncode==0 else None,'harness_dismissed_notice':False,'initial_notice_required_by_setup':True})
        runner.post_run_observer=observe
    runner.run()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('agent',choices=['claude','openai']);p.add_argument('task',type=int,choices=[2,3,4,5]);p.add_argument('--attempt',type=int,choices=[1,2],default=1);p.add_argument('--budget',type=float,default=.65);a=p.parse_args()
    if not 0<a.budget<=2.5:raise SystemExit('Invalid local budget')
    run(a.agent,a.task,a.attempt,a.budget)
