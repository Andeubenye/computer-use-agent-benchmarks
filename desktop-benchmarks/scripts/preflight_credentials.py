from common import *
checks={}
for a,path in [('claude','/v1/models/claude-sonnet-5-5'),('openai','/v1/models/gpt-6.1-sol'),('sai','/v1/agents/account')]:
 r=request(a,path);b=r.get('body',{});x={'credential_available':bool(credential(a)),'http_status':r.get('http_status'),'error':r.get('error')}
 if a=='sai' and r.get('http_status')==200:x.update(plan_free=b.get('plan',{}).get('free'),credits_usd=(b.get('credits') or {}).get('usd'),unlimited=b.get('plan',{}).get('unlimited'))
 elif r.get('http_status')==200:x['model']=b.get('id')
 else:x['error_type']=(b.get('error') or {}).get('type') if isinstance(b,dict) and isinstance(b.get('error'),dict) else None
 checks[a]=x
save(ROOT/'preflight/credentials.json',{'time':now(),'checks':checks,'credential_values_saved':False,'model_generation_requests':0})
print(json.dumps(checks))
