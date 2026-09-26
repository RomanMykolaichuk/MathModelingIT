from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "web" / "books" / "t1_l1" / "index.html"

text = HTML.read_text(encoding="utf-8")

checks = {
    "MathJax script": "tex-svg.js" in text,
    "display open delimiter": r"\[" in text,
    "display close delimiter": r"\]" in text,
    "inline open delimiter": r"\(" in text,
    "inline close delimiter": r"\)" in text,
    "no placeholder leakage": "MMITMATH" not in text,
    "no known broken literal": r"[ t = \text{час}. ]" not in text,
}

failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise SystemExit("MiniBook math rendering checks failed: " + ", ".join(failed))

display_count = text.count(r"\[")
inline_count = text.count(r"\(")
if display_count < 10:
    raise SystemExit(f"Too few display-math delimiters after build: {display_count}")
if inline_count < 10:
    raise SystemExit(f"Too few inline-math delimiters after build: {inline_count}")

print(
    f"MiniBook math rendering: PASS "
    f"(display={display_count}, inline={inline_count})"
)
