"""Deterministic public-task checks; no DOM access or browser automation."""

import re
import unicodedata
from urllib.parse import parse_qs, unquote, urlsplit


def title_matches(actual, expected):
    def normalize(text):
        text = unicodedata.normalize("NFKC", text).casefold()
        text = text.replace("—", "-").replace("–", "-")
        text = re.sub(r"\s+-\s+(?:mozilla firefox|firefox(?: esr)?)$", "", text)
        return " ".join(text.split())

    return normalize(actual) == normalize(expected)


def answer_matches(actual, expected, mode="exact"):
    if mode == "single_year":
        return set(re.findall(r"(?<!\d)\d{4}(?!\d)", actual)) == {str(expected)}
    if mode != "exact":
        raise ValueError("unknown answer evaluator")
    return actual.strip().casefold() == str(expected).strip().casefold()


def url_matches(actual, expected):
    observed, target = urlsplit(actual), urlsplit(expected)
    if (observed.scheme, observed.netloc.casefold()) != (target.scheme, target.netloc.casefold()):
        return False
    query = parse_qs(observed.query)
    if query.get("action", ["view"])[0] not in {"view", ""}:
        return False
    path = unquote(observed.path).rstrip("/")
    expected_path = unquote(target.path).rstrip("/")
    if path == expected_path:
        return True
    return (
        path == "/w/index.php"
        and expected_path.startswith("/wiki/")
        and query.get("title", [None])[0] == expected_path.removeprefix("/wiki/")
    )


def redact_public_text(text):
    # Public tasks may retain their answer; never retain recognizable credential tokens.
    return re.sub(r"(?:sk-ant-|sk-)[A-Za-z0-9_-]{12,}", "[REDACTED]", text)


def public_answer(text):
    return redact_public_text(text)[:65536]
