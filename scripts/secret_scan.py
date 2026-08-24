#!/usr/bin/env python3
"""Pre-commit secret scanner. Scans staged files, blocks on real secrets.

Usage (as git pre-commit hook):
    python scripts/secret_scan.py
    # exit 1 + message if a staged file contains a real secret pattern

Design rules:
- Only staged files (git diff --cached), never the whole tree -> fast.
- Real secret patterns only; placeholders (sk-xxxx, YOUR_TOKEN_HERE,
  example.com) are ignored so the hook never blocks legit commits.
- Allowlist for files whose secret-looking strings are intentional demo/
  terminal-aesthetic content.
"""
import re
import subprocess
import sys

_ALLOWLIST = {
    "src/suckz/render.py",
    "content/tech_solutions/huggingface-gated-model-401.yaml",
}

_BINARY_EXT = {".mp4", ".wav", ".jpg", ".jpeg", ".png", ".gif", ".srt",
               ".mov", ".avi", ".atlas", ".gguf", ".onnx", ".exe", ".dll"}

# value is a placeholder if it's mostly x/* or contains the usual markers
_PLACEHOLDER_RE = re.compile(
    r"^[*xX]+$|YOUR[_-]?|PLACEHOLDER|EXAMPLE|CHANGE_ME|REDACTED|"
    r"<\w+>|TODO|DUMMY|your[_-]?token|your[_-]?key|\.env\b|xxx",
    re.IGNORECASE,
)

_PATTERNS = [
    ("Google API Key", r"AIza[0-9A-Za-z_\-]{35}"),
    ("Google OAuth token", r"ya29\.[0-9A-Za-z_\-]{10,}"),
    ("GitHub PAT", r"ghp_[0-9A-Za-z]{36}|github_pat_[0-9A-Za-z_]{20,}"),
    ("GitLab PAT", r"glpat-[0-9A-Za-z_\-]{20,}"),
    ("Slack token", r"xox[baprs]-[0-9A-Za-z\-]{10,}"),
    ("AWS access key", r"AKIA[0-9A-Z]{16,20}"),
    ("HuggingFace token", r"hf_[A-Za-z0-9]{15,}"),
    ("OpenAI/Anthropic key", r"sk-[0-9A-Za-z]{20,}|sk-ant-[0-9A-Za-z]{20,}"),
    ("Private key", r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"),
    ("client_secret", r"[\"']?client_secret[\"']?\s*[=:]\s*[\"'][^\"']{8,}[\"']"),
    ("password", r"[\"']?password[\"']?\s*[=:]\s*[\"'][^\"']{8,}[\"']"),
    ("generic token", r"[\"']?(?:api[_-]?key|secret|token)[\"']?\s*[=:]\s*[\"'][^\"'\s]{12,}[\"']"),
]


def _staged_files():
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM", "-z"],
        capture_output=True, text=True, check=True,
        encoding="utf-8", errors="replace",
    ).stdout
    return [f for f in out.split("\0") if f]


def _read_staged(path):
    out = subprocess.run(
        ["git", "show", f":{path}"], capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    if out.returncode != 0:
        return None
    return out.stdout


def _is_placeholder(value):
    if not value:
        return True
    return bool(_PLACEHOLDER_RE.search(value))


def _scan():
    findings = []
    for path in _staged_files():
        low = path.lower()
        if low.endswith(tuple(_BINARY_EXT)):
            continue
        if path in _ALLOWLIST:
            continue
        content = _read_staged(path)
        if content is None:
            continue
        for lineno, line in enumerate(content.splitlines(), 1):
            for name, pat in _PATTERNS:
                for m in re.finditer(pat, line):
                    value = m.group(0)
                    if _is_placeholder(value):
                        continue
                    findings.append(f"{path}:{lineno}: {name} (possible {pat[:20]}...)")
    return findings


def main():
    findings = _scan()
    if not findings:
        return 0
    print("BLOCKED: possible secrets staged for commit:", file=sys.stderr)
    for f in findings:
        print(f"  {f}", file=sys.stderr)
    print("\nRemove the secret (or add the path to scripts/secret_scan.py ALLOWLIST "
          "if it's a deliberate placeholder) and re-commit.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
