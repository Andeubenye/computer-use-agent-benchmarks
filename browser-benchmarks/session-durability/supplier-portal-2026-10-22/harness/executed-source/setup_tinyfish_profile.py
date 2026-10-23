"""Non-scored, supported CDP login/profile save. No supplier task is executed."""
from pathlib import Path
import asyncio,argparse,datetime,hashlib,json,time,urllib.request,urllib.error,os,subprocess
from fixture_client import Fixture,BASE
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--socket',required=True);args=p.parse_args();fixture=Fixture(args.socket);key=fixture.key('tinyfish')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(name,x):(ROOT/name).write_text(json.dumps(x,indent=2)+'\n')
def api(path,payload=None):
 r=urllib.request.Request('https://agent.tinyfish.ai'+path,headers={'X-API-Key':key,'Content-Type':'application/json'},data=json.dumps(payload).encode() if payload is not None else None)
 try:
  with urllib.request.urlopen(r,timeout=30) as f:return f.status,json.load(f)
 except urllib.error.HTTPError as e:return e.code,{}
async def main():
 from playwright.async_api import async_playwright
 if (ROOT/'tinyfish-profile-setup.json').exists():raise SystemExit('Existing setup attempt retained; no automatic repeat')
 profile=json.loads((ROOT/'tinyfish-profile-create-private.json').read_text())['body']['id'];start=time.monotonic();started=now();_,wallet0=api('/v1/wallet');session=None;saved=False;browser=None
 report={'started_at_utc':started,'operation':'Fresh durability-test profile setup, no scored browser task','local_setup_python_pid':os.getpid(),'profile_id':profile,'browser_profile_for_scored_runs':'lite','password_in_agent_goal':False,'cookies_written_to_evidence':False,'vault_enabled':False,'synthetic_account_only':True}
 try:
  code,b=api('/v1/profiles/'+profile+'/setup-session',{'url':BASE+'/login','timeout_seconds':300});report['setup_http_status']=code
  if code not in (200,201):raise RuntimeError('Profile setup unavailable')
  session=b['session_id'];report['setup_session_created']=True
  async with async_playwright() as play:
   browser=await play.chromium.connect_over_cdp(b['cdp_url'],timeout=30000);context=browser.contexts[0];page=context.pages[0] if context.pages else await context.new_page();await page.goto(BASE+'/login',wait_until='domcontentloaded',timeout=30000)
   await page.get_by_label('Username',exact=True).fill('benchmark-buyer');await page.get_by_label('Password',exact=True).fill(fixture.key('fixture_password'));await page.get_by_role('button',name='Sign in',exact=True).click();await page.wait_for_url('**/dashboard',timeout=30000);report['login_confirmed']=await page.get_by_text('Signed in as Benchmark Buyer',exact=False).is_visible()
   cookies=await context.cookies(BASE);token=next(c['value'] for c in cookies if c['name']=='__Host-supplier_session');report['server_session_hash']=hashlib.sha256(token.encode()).hexdigest();token=None;cookies=None
   await page.screenshot(path=str(ROOT/'tinyfish-setup-authenticated.png'));code,body=api('/v1/profiles/'+profile+'/save',{'session_id':session});report['save_http_status']=code;report['save_result']={k:body.get(k) for k in ('domains_updated','domains_failed','cookie_count','pages_captured','target_reads_skipped','domains_skipped')};saved=code==200 and bool(body.get('cookie_count'));report['profile_saved']=saved
   if not saved:raise RuntimeError('Authenticated profile not saved')
   try:await browser.close()
   except Exception:pass
 except Exception as e:report['error_category']=type(e).__name__;report['profile_saved']=False
 finally:
  if session and not saved:
   status,_=api('/v1/profiles/'+profile+'/setup-session/cancel',{'session_id':session});report['setup_cancel_status']=status
  _,wallet1=api('/v1/wallet');report.update(finished_at_utc=now(),setup_wall_seconds=time.monotonic()-start,observed_credit_delta_usd=round(float(wallet0['available_balance'])-float(wallet1['available_balance']),8),cost_basis='Account delta during dedicated browser setup; Browser tariff $0.002/min; not invoice',browser_session_urls_retained_in_public_evidence=False)
  dump('tinyfish-profile-setup.json',report);print(json.dumps({k:report.get(k) for k in ('profile_saved','login_confirmed','setup_http_status','save_http_status','setup_wall_seconds','observed_credit_delta_usd','error_category')}))
asyncio.run(main());key=None
