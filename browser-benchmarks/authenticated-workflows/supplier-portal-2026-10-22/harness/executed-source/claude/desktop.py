import json
import math
import subprocess
import time
from pathlib import Path

from .evaluation import url_matches

ROOT = Path(__file__).resolve().parent.parent
IMAGE = "claude-benchmark-desktop:v1"
CONTAINER = "claude-benchmark-desktop"


def docker(*args, data=None, timeout=60):
    return subprocess.run(
        ["docker", *args], input=data, capture_output=True, check=True, timeout=timeout
    ).stdout.decode()


class Desktop:
    def __init__(self, name=CONTAINER):
        self.name = name

    def identity(self):
        info = json.loads(docker("inspect", self.name))[0]
        image = json.loads(docker("image", "inspect", info["Image"]))[0]
        browser = docker("exec", self.name, "firefox-esr", "--version").strip()
        return {
            "container_id": info["Id"],
            "image_id": info["Image"],
            "resolution": "1024x768",
            "architecture": image["Architecture"],
            "browser_version": browser,
        }

    def execute(self, name, args, timeout=310):
        if name in {"wait", "hold_key"}:
            duration = args.get("duration")
            if (
                not isinstance(duration, (int, float))
                or not math.isfinite(duration)
                or not 0 <= duration <= 300
                or duration + 1 >= timeout
            ):
                return {
                    "is_error": True,
                    "content": "Wait/hold duration exceeds action deadline or range.",
                }
        return json.loads(
            docker(
                "exec",
                "-i",
                self.name,
                "python",
                "/opt/desktop/action.py",
                data=json.dumps({"name": name, "input": args}).encode(),
                timeout=timeout,
            )
        )

    def ready(self):
        for _ in range(40):
            try:
                title = self.execute("window_title", {}, timeout=5)
                if not title.get("is_error") and "Firefox" in title["content"]:
                    return
            except (subprocess.SubprocessError, ValueError):
                pass
            time.sleep(0.5)
        raise RuntimeError("Firefox desktop did not become ready")

    def claim(self):
        # Exclusive per-container marker prevents accidental reuse after any smoke/paid run.
        docker(
            "exec",
            self.name,
            "python",
            "-c",
            "from pathlib import Path; Path('/home/agent/.benchmark-used').touch(exist_ok=False)",
        )

    def observe_url(self, expected, timeout=15):
        """Grader only: read the address bar through native keys and the Linux clipboard."""
        deadline = time.monotonic() + timeout

        def remaining():
            return max(0.1, deadline - time.monotonic())

        try:
            for key in ("ctrl+l", "ctrl+c"):
                result = self.execute("key", {"text": key}, timeout=remaining())
                if result.get("is_error"):
                    raise RuntimeError("address-bar observation failed")
            value = docker(
                "exec", self.name, "xclip", "-selection", "clipboard", "-out", timeout=remaining()
            ).strip()
            matches = url_matches(value, expected)
            return {"matches": matches, "verified_url": expected if matches else ""}
        finally:
            self.execute("key", {"text": "Escape"}, timeout=remaining())


def start():
    # Refuse to delete an existing container; each run must explicitly stop its predecessor.
    docker(
        "run",
        "--detach",
        "--name",
        CONTAINER,
        "--init",
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges",
        "--shm-size=256m",
        "--memory=2g",
        "--cpus=2",
        "--pids-limit=256",
        "--label",
        "app=claude-computer-benchmark",
        IMAGE,
    )
    Desktop().ready()


def stop():
    # Only this project's named container; no volume deletion or global pruning.
    info = json.loads(docker("inspect", CONTAINER))[0]
    if info["Config"].get("Labels", {}).get("app") != "claude-computer-benchmark":
        raise RuntimeError("refusing to remove a container not owned by this benchmark")
    docker("rm", "--force", CONTAINER)
