"""One JSON action on stdin; one JSON result on stdout. Never execute shell input."""

import base64
import io
import json
import math
import subprocess
import sys
import time
from contextlib import contextmanager

from PIL import Image

WIDTH, HEIGHT = 1024, 768


def command(*args, data=None):
    return subprocess.run(
        list(args), input=data, capture_output=True, check=True, timeout=15
    ).stdout


def point(value):
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("coordinate must have two integers")
    x, y = value
    if type(x) is not int or type(y) is not int or not (0 <= x < WIDTH and 0 <= y < HEIGHT):
        raise ValueError("coordinate outside display")
    return str(x), str(y)


def move(value):
    command("xdotool", "mousemove", "--sync", *point(value))


def key_parts(text):
    aliases = {
        "ctrl": "Control_L",
        "shift": "Shift_L",
        "alt": "Alt_L",
        "super": "Super_L",
        "CTRL": "Control_L",
    }
    if not isinstance(text, str) or not text or len(text) > 200 or text.startswith("-"):
        raise ValueError("invalid keys")
    return [aliases.get(k.lower(), k) for k in text.split("+")]


@contextmanager
def modifiers(text):
    keys = key_parts(text) if text else []
    if any(k not in {"Control_L", "Shift_L", "Alt_L", "Super_L"} for k in keys):
        raise ValueError("click and scroll support only modifier keys")
    try:
        for key in keys:
            command("xdotool", "keydown", key)
        yield
    finally:
        for key in reversed(keys):
            command("xdotool", "keyup", key)


def bounded(value, low, high):
    if not isinstance(value, (int, float)) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError("numeric input outside supported range")
    return value


def execute(name, args):
    if name in {"screenshot", "zoom"}:
        png = command("scrot", "--overwrite", "/tmp/frame.png")
        del png
        with Image.open("/tmp/frame.png") as source:
            image = source.copy()
        if name == "zoom":
            region = args["region"]
            if not isinstance(region, list) or len(region) != 4:
                raise ValueError("invalid zoom region")
            point(region[:2])
            x1, y1 = region[2:]
            if (
                type(x1) is not int
                or type(y1) is not int
                or not region[0] < x1 <= WIDTH
                or not region[1] < y1 <= HEIGHT
            ):
                raise ValueError("invalid zoom bounds")
            image = image.crop(tuple(region))
            scale = min(WIDTH / image.width, HEIGHT / image.height)
            image = image.resize((round(image.width * scale), round(image.height * scale)))
        out = io.BytesIO()
        image.save(out, format="PNG")
        return [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": base64.b64encode(out.getvalue()).decode(),
                },
            }
        ]
    if name == "window_title":  # grader only, never advertised to Claude
        active = command("xdotool", "getactivewindow").decode().strip()
        return command("xdotool", "getwindowname", active).decode().strip()
    if name == "cursor_position":
        return command("xdotool", "getmouselocation", "--shell").decode()
    if name == "type":
        text = args["text"]
        if not isinstance(text, str) or len(text) > 20000:
            raise ValueError("invalid text")
        # Clipboard supports Unicode; its contents stay only inside this disposable desktop.
        proc = subprocess.Popen(
            ["xclip", "-selection", "clipboard", "-in"],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        proc.communicate(text.encode(), timeout=5)
        if proc.returncode:
            raise ValueError("clipboard failed")
        command("xdotool", "key", "--clearmodifiers", "ctrl+v")
    elif name == "key":
        repeat = args.get("repeat", 1)
        if type(repeat) is not int or not 1 <= repeat <= 100:
            raise ValueError("invalid repeat")
        command(
            "xdotool",
            "key",
            "--clearmodifiers",
            "--repeat",
            str(repeat),
            "+".join(key_parts(args["text"])),
        )
    elif name in {"hold_key", "wait"}:
        duration = bounded(args["duration"], 0, 300)
        keys = "+".join(key_parts(args["text"])) if name == "hold_key" else None
        try:
            if keys:
                command("xdotool", "keydown", keys)
            time.sleep(duration)
        finally:
            if keys:
                command("xdotool", "keyup", keys)
    elif name == "mouse_move":
        move(args["coordinate"])
    elif name in {"left_mouse_down", "left_mouse_up"}:
        command("xdotool", "mousedown" if name.endswith("down") else "mouseup", "1")
    elif name == "left_click_drag":
        move(args["start_coordinate"])
        with modifiers(args.get("text")):
            try:
                command("xdotool", "mousedown", "1")
                move(args["coordinate"])
            finally:
                command("xdotool", "mouseup", "1")
    elif name in {
        "left_click",
        "right_click",
        "middle_click",
        "double_click",
        "triple_click",
        "scroll",
    }:
        if args.get("coordinate") is not None:
            move(args["coordinate"])
        count, button = 1, {"right_click": 3, "middle_click": 2}.get(name, 1)
        if name == "scroll":
            button = {"up": 4, "down": 5, "left": 6, "right": 7}[args["scroll_direction"]]
            count = args["scroll_amount"]
            if type(count) is not int or not 1 <= count <= 100:
                raise ValueError("invalid scroll count")
        elif name in {"double_click", "triple_click"}:
            count = 2 if name == "double_click" else 3
        with modifiers(args.get("text")):
            command("xdotool", "click", "--repeat", str(count), "--delay", "100", str(button))
    else:
        raise ValueError("unsupported computer action")
    time.sleep(0.2)
    return "OK"


if __name__ == "__main__":
    try:
        request = json.load(sys.stdin)
        result = {"content": execute(request["name"], request.get("input", {})), "is_error": False}
    except Exception as error:
        # Raw command errors can contain typed text; return only an error category.
        result = {"content": f"Desktop action failed ({type(error).__name__})", "is_error": True}
    print(json.dumps(result))
