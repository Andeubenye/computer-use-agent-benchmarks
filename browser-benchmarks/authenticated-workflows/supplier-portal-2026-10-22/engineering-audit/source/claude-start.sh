#!/bin/sh
set -eu
Xvfb :1 -screen 0 1024x768x24 -nolisten tcp &
sleep 1
openbox >/tmp/openbox.log 2>&1 &
mkdir -p /home/agent/profile
cat > /home/agent/profile/user.js <<'EOF'
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("browser.startup.page", 0);
user_pref("datareporting.policy.dataSubmissionEnabled", false);
user_pref("toolkit.telemetry.enabled", false);
user_pref("browser.tabs.warnOnClose", false);
user_pref("browser.aboutwelcome.enabled", false);
user_pref("browser.sessionstore.resume_from_crash", false);
EOF
firefox-esr --no-remote --profile /home/agent/profile about:blank >/tmp/firefox.log 2>&1 &
browser_pid=$!
trap 'kill "$browser_pid" 2>/dev/null || true; exit 0' TERM INT
wait "$browser_pid"
