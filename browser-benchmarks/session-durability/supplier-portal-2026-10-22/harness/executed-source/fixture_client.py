"""Owner-authorized fixture administration and independent verification, never agent task execution."""
import urllib.request,urllib.error,json,socket
BASE='https://manicule-supplier-benchmark-oct22.peppyshark33.chatgpt.site'
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):return None
class Fixture:
 def __init__(self,sock):
  self.sock=sock;self.service=self.key('site_service_token');self.admin=self.key('fixture_admin')
 def key(self,name):
  s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
  try:s.connect(self.sock);s.sendall(name.encode());return s.recv(16384).decode()
  finally:s.close()
 def request(self,path,payload=None,method=None,cookie=None,form=False,admin=False):
  import urllib.parse
  h={'OAI-Sites-Authorization':'Bearer '+self.service,'Accept':'application/json','User-Agent':'Manicule-fixture-verifier/1.0'}
  if admin:h['Authorization']='Bearer '+self.admin
  if cookie:h['Cookie']=cookie
  data=None
  if payload is not None:
   h['Origin']=BASE
   if form:h['Content-Type']='application/x-www-form-urlencoded';data=urllib.parse.urlencode(payload).encode()
   else:h['Content-Type']='application/json';data=json.dumps(payload).encode()
  req=urllib.request.Request(BASE+path,headers=h,data=data,method=method or ('POST' if payload is not None else 'GET'))
  try:
   with urllib.request.build_opener(NoRedirect()).open(req,timeout=25) as r:status=r.status;headers=r.headers;raw=r.read()
  except urllib.error.HTTPError as e:status=e.code;headers=e.headers;raw=e.read()
  try:body=json.loads(raw)
  except ValueError:body=raw.decode(errors='replace')
  return status,headers,body
 def json(self,path,payload=None):
  status,headers,body=self.request(path,payload,admin=True)
  if status!=200:raise RuntimeError('Fixture administration returned HTTP '+str(status))
  return body
