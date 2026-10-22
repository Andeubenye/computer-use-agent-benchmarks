"""Offline harness checks. No provider requests, Docker commands, or agent tasks."""
import json
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import run_native as harness

passed = []

# Host sleep must not leave additional execution allowance after waking.
r = object.__new__(harness.Runner)
r.start, r.wall_start, r.limit = 100., 1000., 100.
with patch.object(harness.time, 'monotonic', return_value=105.), patch.object(harness.time, 'time', return_value=1200.):
    assert r.remaining() == 0
passed.append('sleep-inclusive deadline')

# Existing cumulative spend must limit a later run, even below its local cap.
r = object.__new__(harness.Runner)
r.agent, r.count_requests, r.cost, r.uncertain, r.budget = 'openai', 0, 0., 0., 2.5
r.folder = harness.ROOT / 'logs' / 'unsubmitted-offline-check'
r.api = lambda *args: {'input_tokens': 10000}
with patch.object(harness, 'recorded_spend', return_value=6.95):
    try:
        r.count_and_reserve({})
        raise AssertionError('Cumulative budget guard did not stop')
    except RuntimeError as error:
        assert 'Cumulative $7' in str(error)
passed.append('cumulative budget reservation')

# The Responses continuation must return screenshots paired with the native call.
r = object.__new__(harness.Runner)
r.agent, r.actions, r.final, r.reason = 'openai', 0, '', ''
r.tag = 'offline-only'
r.prompt, r.system = harness.PROMPT, harness.SYSTEM
bodies, actions = [], []
responses = iter([
    {'id': 'offline_response', 'status': 'completed', 'output': [
        {'type': 'computer_call', 'call_id': 'offline_call', 'actions': [
            {'type': 'keypress', 'keys': ['CTRL', 'O']}, {'type': 'screenshot'}]}]},
    {'id': 'offline_response_2', 'status': 'completed', 'output': []},
])
def generation(body):
    bodies.append(body)
    return next(responses)
r.generation = generation
r.openai_action = actions.append
r.rawshot = lambda tag: 'offline-screenshot-placeholder'
with patch.object(harness, 'event'):
    r.run_openai('offline-initial-placeholder')
assert bodies[0]['tools'] == [{'type': 'computer'}]
assert bodies[1]['previous_response_id'] == 'offline_response'
output = bodies[1]['input'][0]
assert output['type'] == 'computer_call_output' and output['call_id'] == 'offline_call'
assert output['output']['type'] == 'computer_screenshot' and output['output']['detail'] == 'original'
assert [a['type'] for a in actions] == ['keypress', 'screenshot']
assert r.reason == 'model_finished'
passed.append('native Responses action ordering and screenshot continuation')

r = object.__new__(harness.Runner)
executed = []
r.native = lambda name,args: executed.append((name,args))
r.openai_action({'type':'click','button':'left','keys':['SHIFT'],'x':100,'y':100})
assert executed==[('left_click',{'coordinate':[100,100],'text':'shift'})]
passed.append('native click modifier preserved')

# An executor error must not disappear behind a later screenshot.
r = object.__new__(harness.Runner)
r.watchdog, r.name, r.tag, r.actions = False, 'offline-only', 'offline-only', 0
r.remaining = lambda: 100.
r.screenshot = lambda *args: []
with patch.object(harness, 'docker', return_value=b'{"content":"Desktop action failed", "is_error":true}'), patch.object(harness, 'event'):
    try:
        r.native('key', {'text': 'Return'})
        raise AssertionError('Executor failure was ignored')
    except RuntimeError as error:
        assert 'action error' in str(error)
passed.append('executor error propagation')

# Retained usage must include a charge even if it exceeds its reservation.
r = object.__new__(harness.Runner)
r.agent, r.folder = 'openai', harness.ROOT / 'logs' / 'offline-only'
r.prompt = harness.PROMPT
r.requests, r.cost, r.uncertain, r.usages, r.tag = 0, 0., .001, [], 'offline-only'
r.count_and_reserve = lambda body: None
r.api = lambda *args: {'model': 'offline-model', 'usage': {'input_tokens': 1000, 'output_tokens': 100}}
with patch.object(harness, 'event'), patch.object(harness, 'save'):
    try:
        r.generation({})
        raise AssertionError('Reservation overrun was ignored')
    except RuntimeError as error:
        assert 'usage retained' in str(error)
assert abs(r.cost - .003) < 1e-12 and len(r.usages) == 1
passed.append('returned cost retained on reservation overrun')

print(json.dumps({'offline_checks_passed': len(passed), 'checks': passed,
                  'provider_requests': 0, 'docker_calls': 0,
                  'simulations_are_not_benchmark_results': True}))
