"""Separate profile-persistent configuration using the existing image, never rebuilding it."""
from pathlib import Path
import json,os,subprocess,time
NAME='claude-session-durability-persistent';VOLUME='manicule-durability-firefox-20261022';IMAGE='claude-benchmark-desktop:v1'
def initialize(desktop):
 # Dedicated volume, no host bind mount. Only initialization gets bounded CHOWN capability.
 desktop.docker('volume','create','--label','app=manicule-session-durability',VOLUME)
 desktop.docker('run','--rm','--user','0','--entrypoint','/bin/sh','--network=none','--cap-drop=ALL','--cap-add=CHOWN','--security-opt=no-new-privileges','--mount',f'type=volume,source={VOLUME},target=/home/agent/profile',IMAGE,'-c','chmod 700 /home/agent/profile && chown 1000:1000 /home/agent/profile')
def start(desktop):
 desktop.docker('run','--detach','--name',NAME,'--init','--cap-drop=ALL','--security-opt=no-new-privileges','--shm-size=256m','--memory=2g','--cpus=2','--pids-limit=256','--label','app=claude-computer-benchmark','--label','benchmark=session-durability','--mount',f'type=volume,source={VOLUME},target=/home/agent/profile',IMAGE)
 d=desktop.Desktop(NAME);d.ready();return d
def stop_remove(desktop,d):
 info=json.loads(desktop.docker('inspect',d.name))[0]
 assert info['Config']['Labels'].get('app')=='claude-computer-benchmark'
 t=time.monotonic();graceful=True
 try:quit_result=d.execute('key',{'text':'ctrl+shift+q'},timeout=10)
 except (subprocess.CalledProcessError,ValueError):quit_result={'is_error':None,'quit_acknowledgment_lost_as_container_exited':True}
 try:desktop.docker('wait',d.name,timeout=25)
 except subprocess.TimeoutExpired:
  graceful=False;desktop.docker('stop','--time','20',d.name,timeout=25)
 desktop.docker('rm',d.name)
 return {'seconds':time.monotonic()-t,'graceful_firefox_quit_requested':True,'quit_action_error':quit_result.get('is_error',False),'exited_without_forced_timeout':graceful,'container_removed':True,'container_id':info['Id'],'mounts':info['Mounts']}
def remove_volume(desktop):
 info=json.loads(desktop.docker('volume','inspect',VOLUME))[0];assert (info.get('Labels') or {}).get('app')=='manicule-session-durability';desktop.docker('volume','rm',VOLUME)
