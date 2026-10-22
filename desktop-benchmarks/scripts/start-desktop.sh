#!/bin/sh
set -eu
Xvfb :1 -screen 0 1024x768x24 -nolisten tcp &
sleep 1
openbox >/tmp/openbox.log 2>&1 &
mkdir -p /home/agent/Desktop/benchmark /home/agent/.config/libreoffice/4/user
cat > /home/agent/.config/libreoffice/4/user/registrymodifications.xcu <<'XML'
<?xml version="1.0" encoding="UTF-8"?>
<oor:items xmlns:oor="http://openoffice.org/2001/registry"><item oor:path="/org.openoffice.Office.Common/Misc"><prop oor:name="ShowTipOfTheDay" oor:op="fuse"><value>false</value></prop><prop oor:name="FirstRun" oor:op="fuse"><value>false</value></prop></item></oor:items>
XML
libreoffice --calc --norestore --nologo --nofirststartwizard >/tmp/libreoffice.log 2>&1 &
app_pid=$!
trap 'kill "$app_pid" 2>/dev/null || true; exit 0' TERM INT
# Keep the desktop alive if the agent closes a document or exits Calc.
while true; do sleep 10; done
