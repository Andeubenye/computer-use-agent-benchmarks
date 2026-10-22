"""One Sai task on the existing free account; no benchmark restart or new purchase."""
import datetime
import json
import threading
import time
import urllib.parse
from safe_api import request, save, OUT, WORK

folder = OUT / 'agents/sai'
marker = WORK / 'sai-submission-started.json'
if marker.exists():
    raise SystemExit('Submission marker exists; refusing another benchmark.')
account = json.loads((OUT/'audit/sai-account.json').read_text())['body']
assert account['plan']['free'] is True and account['credits']['usd'] > 0
machines = json.loads((OUT/'audit/sai-machines.json').read_text())['body']['machines']
assert len(machines) == 1 and machines[0]['kind'] == 'cloud'
machine = machines[0]['machineId']
session_response = request('sai', '/v1/agents/new-session', {'machineId': machine, 'channel': 'api'})
save(folder/'fresh-session.json', session_response)
if session_response.get('http_status') != 200:
    save(folder/'run-record.json', {'status': 'blocked_before_agent_start', 'reason': session_response, 'benchmark_submissions': 0})
    raise SystemExit('Sai session unavailable; stopped without retry.')
session = session_response['body']['sessionId']
started = time.monotonic()
started_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
state = {'deadline_fired': False, 'abort': None}
lock = threading.Lock()

def stop(reason):
    with lock:
        if state['abort'] is not None:
            return
        result = request('sai', '/v1/agents/abort', {'sessionId': session}, timeout=20)
        state['abort'] = result
        save(folder/'abort.json', {'reason': reason, 'elapsed_seconds': time.monotonic()-started, 'response': result})

def deadline():
    state['deadline_fired'] = True
    stop('600-second task deadline')

timer = threading.Timer(600, deadline)
timer.daemon = True
payload = {'message': (OUT/'task-prompt.txt').read_text(), 'machineId': machine, 'sessionId': session, 'wait': False,
           'options': {'recordTrajectory': True, 'idempotency_key': 'manicule-github-bugs-2026-10-17-one-authorized-run'}}
save(folder/'request-without-credentials.json', payload)
save(marker, {'sessionId': session, 'started_at_utc': started_utc})
timer.start()
result = None
turn = None
status = 'unknown'
reason = None
try:
    submission = request('sai', '/v1/agents/message', payload, timeout=45)
    save(folder/'submission.json', submission)
    if submission.get('http_status') not in (200,202):
        status, reason = 'blocked_at_submission', submission
    else:
        turn = submission['body'].get('turnId')
        cursor = None
        poll = 0
        while time.monotonic()-started < 600 and not state['deadline_fired']:
            remaining = 600-(time.monotonic()-started)
            wait = min(30,max(0,int(remaining)-2))
            query = {'sessionId': session, 'wait': wait}
            if cursor: query['since'] = cursor
            event = request('sai', '/v1/agents/events?'+urllib.parse.urlencode(query), timeout=min(40,max(1,remaining)))
            poll += 1
            save(folder/'events'/f'{poll:03d}.json', event)
            if event.get('http_status') != 200:
                status, reason = 'failed_event_read', event
                stop('event read failure; no retry')
                break
            body = event['body']
            cursor = body.get('cursor')
            status = body.get('status','unknown')
            print(json.dumps({'elapsed_seconds':round(time.monotonic()-started,3),'status':status,'event_count':len(body.get('events',[]))}),flush=True)
            if status == 'needs_approval':
                reason = body.get('approval') or 'Required approval unavailable under no-new-consent conditions'
                stop('required approval; stopped without asking user or bypassing')
                status = 'blocked_required_approval'
                break
            if status in ('idle','error'):
                result = body
                break
            if wait == 0: break
        else:
            status = 'timeout'
        if state['deadline_fired'] or time.monotonic()-started >= 600:
            status = 'timeout'
            stop('600-second task deadline')
        if turn:
            final_turn = request('sai', '/v1/agents/turns/'+urllib.parse.quote(turn,safe=''))
            save(folder/'provider-turn.json', final_turn)
            trajectory = request('sai', '/v1/agents/turns/'+urllib.parse.quote(turn,safe='')+'/trajectory')
            save(folder/'provider-trajectory.json', trajectory)
    if result is not None:
        save(folder/'final-event.json', result)
        (folder/'original-response.txt').write_text(result.get('text',''))
except Exception as error:
    status, reason = 'harness_error', type(error).__name__+': '+str(error)
    stop('harness exception')
finally:
    timer.cancel()
    if status not in ('idle','error','blocked_at_submission') and state['abort'] is None:
        stop('cleanup after nonterminal exit')
    elapsed = time.monotonic()-started
    save(folder/'run-record.json', {'status':status,'reason':reason,'sessionId':session,'turnId':turn,'started_at_utc':started_utc,
         'finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'client_elapsed_seconds':elapsed,'time_limit_seconds':600,
         'elapsed_includes_machine_startup_and_final_evidence_reads':True,'benchmark_submissions':1,'automatic_benchmark_restarts':0,
         'deadline_fired':state['deadline_fired'],'abort_response':state['abort'],'agent_model_requested':'session default (auto)',
         'paid_plan_or_purchase_initiated':False,'original_response_present':bool(result and result.get('text')),'task_success_independently_verified':False})
    save(folder/'account-after.json',request('sai','/v1/agents/account'))
    print(json.dumps({'final_status':status,'elapsed_seconds':elapsed,'turnId':turn}),flush=True)
