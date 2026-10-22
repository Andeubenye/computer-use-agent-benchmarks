"""Read-only final regrade and usage reconciliation. Makes no provider requests."""
from pathlib import Path
from decimal import Decimal
import hashlib, json, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from verify_result import verify
from verify_additional import audit

def load(p): return json.loads(p.read_text())
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def money(u, agent):
    if agent == 'claude':
        return (Decimal(u.get('input_tokens', 0))*2 + Decimal(u.get('output_tokens', 0))*10
                + Decimal(u.get('cache_creation_input_tokens', 0))*4
                + Decimal(u.get('cache_read_input_tokens', 0))*Decimal('.1')) / 1000000
    d = u.get('input_tokens_details') or {}
    cached, written = d.get('cached_tokens', 0), d.get('cache_write_tokens', 0)
    return (Decimal(u.get('input_tokens', 0)-cached-written)*2
            + Decimal(cached)*Decimal('.1') + Decimal(written)*Decimal('2.5')
            + Decimal(u.get('output_tokens', 0))*10) / 1000000

rows, errors, regrades = [], [], []
tasks = load(ROOT / 'inputs/additional/tasks.json')
for number, spec in tasks.items():
    for name, expected_hash in spec['input_files_sha256'].items():
        fixture = ROOT / 'inputs/additional' / f'task-{number}' / name
        if not fixture.is_file() or digest(fixture) != expected_hash:
            errors.append({'attempt': f'canonical task-{number}/{name}', 'check': 'frozen input hash changed'})
for record in sorted((ROOT / 'logs').rglob('run-record.json')):
    r = load(record)
    if r.get('agent') not in ('claude', 'openai'): continue
    agent, folder = r['agent'], record.parent
    rel = str(folder.relative_to(ROOT / 'logs'))
    responses = [load(p) for p in sorted((folder / 'responses').glob('*.json'))]
    usages = [x['usage'] for x in responses if x.get('usage')]
    total = sum((money(u, agent) for u in usages), Decimal(0))
    checks = {
        'response_count_matches_record': len(responses) == r.get('model_requests', 0),
        'raw_usage_matches_record': usages == r.get('usage', []),
        'recalculated_cost_matches_record': abs(total-Decimal(str(r.get('estimated_api_cost_usd', 0)))) < Decimal('.000000001'),
        'no_automatic_retries': r.get('api_retries', 0) == 0 and r.get('automatic_restarts', 0) == 0,
        'within_600_second_wall_limit': r.get('wall_clock_duration_seconds', r.get('duration_seconds', 0)) <= 600,
    }
    config_path = folder / 'configuration.json'
    if config_path.exists():
        config = load(config_path)
        task_number = rel.split('/task-')[1].split('/')[0] if '/task-' in rel else None
        expected_prompt = tasks[task_number]['prompt'] if task_number else (ROOT/'inputs/task-prompt.txt').read_text()
        checks['original_frozen_prompt_used'] = config['prompt'] == expected_prompt
        checks['configured_limit_not_above_600'] = config['task_timeout_seconds'] <= 600
    images = list((ROOT / 'screenshots' / rel).glob('*.png'))
    checks['screenshot_count_matches'] = len(images) == r.get('screenshots_saved', 0)
    events_path = folder / 'events.jsonl'
    events = [json.loads(line) for line in events_path.read_text().splitlines()] if events_path.exists() else []
    maximum_action = max((x.get('index', 0) for x in events if x.get('event') == 'native_action'), default=0)
    # Early records can omit an event for a requested action that failed during execution.
    checks['action_counter_not_below_trace'] = maximum_action <= r.get('actions', 0)
    rows.append({'attempt': rel, 'requested_model': r.get('model_requested'),
        'returned_model_aliases': sorted({x.get('model', 'not exposed') for x in responses}),
        'responses': len(responses), 'actions_requested': r.get('actions', 0),
        'last_logged_action_index': maximum_action, 'images': len(images),
        'input_tokens': sum(u.get('input_tokens', 0) for u in usages),
        'output_tokens': sum(u.get('output_tokens', 0) for u in usages),
        'cache_read_tokens': sum(u.get('cache_read_input_tokens', 0) if agent=='claude' else (u.get('input_tokens_details') or {}).get('cached_tokens', 0) for u in usages),
        'cache_write_tokens': sum(u.get('cache_creation_input_tokens', 0) if agent=='claude' else (u.get('input_tokens_details') or {}).get('cache_write_tokens', 0) for u in usages),
        'estimated_cost_usd': float(total), 'stop_reason': r.get('reason'),
        'wall_seconds': r.get('wall_clock_duration_seconds'), 'stopwatch_seconds': r.get('duration_seconds'),
        'checks': checks})
    for name, passed in checks.items():
        if not passed: errors.append({'attempt': rel, 'check': name})
    vpath = folder / 'independent-verification.json'
    if not vpath.exists():
        errors.append({'attempt': rel, 'check': 'final verification missing'}); continue
    old = load(vpath)
    if not r.get('submitted'): continue
    if '/task-' in rel:
        task = int(rel.split('/task-')[1].split('/')[0])
        obs = load(folder / 'gui-observations.json') if (folder / 'gui-observations.json').exists() else {}
        new = audit(task, ROOT / 'outputs' / rel, obs)
    elif rel == 'claude':
        # The paid original protocol failure collected no artifact. Retain its unscored blocker.
        continue
    else:
        obs = load(folder / 'gui-observations.json')
        # Historical CSV retry retained its original outputs/claude destination.
        destination = 'claude' if rel == 'claude-attempt-2' else rel
        new = verify(ROOT / 'outputs' / destination, obs)
    same = new['outcome'] == old['outcome'] and new['score'] == old['score']
    regrades.append({'attempt': rel, 'outcome': new['outcome'], 'score': new['score'], 'matches_saved_final_grade': same})
    if not same: errors.append({'attempt': rel, 'check': 'regrade disagrees'})

manifest = load(ROOT / 'logs/evidence-manifest.json')
originals = [{'path': x['path'], 'unchanged': (ROOT/x['path']).exists() and digest(ROOT/x['path'])==x['sha256']} for x in manifest['files']]
for x in originals:
    if not x['unchanged']: errors.append({'attempt': x['path'], 'check': 'original evidence changed'})
result = {'provider_requests': 0, 'agent_files_edited': False,
          'estimated_total_usd': float(sum(Decimal(str(x['estimated_cost_usd'])) for x in rows)),
          'invoice_reconciled': False, 'attempts': rows, 'regrades': regrades,
          'original_manifest_checked': len(originals), 'original_manifest_unchanged': all(x['unchanged'] for x in originals),
          'errors': errors, 'passed': not errors}
(ROOT/'logs/usage-reconciliation.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'passed': not errors, 'attempts': len(rows), 'regrades': len(regrades),
                  'estimated_total': result['estimated_total_usd'], 'errors': errors}))
sys.exit(bool(errors))
