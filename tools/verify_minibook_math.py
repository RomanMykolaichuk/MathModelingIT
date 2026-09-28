from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK_IDS = ("t1_l1", "t1_l2", "t1_l3", "t1_l4", "t2_l1", "t2_l2", "t2_l3", "t2_l4", "t2_l5", "t2_l6", "t2_l7")

failures: list[str] = []

for book_id in BOOK_IDS:
    html = ROOT / "web" / "books" / book_id / "index.html"
    if not html.exists():
        failures.append(f"{book_id}: відсутній згенерований HTML")
        continue

    text = html.read_text(encoding="utf-8")
    checks = {
        "MathJax script": "tex-svg.js" in text,
        "display open delimiter": r"\[" in text,
        "display close delimiter": r"\]" in text,
        "inline open delimiter": r"\(" in text,
        "inline close delimiter": r"\)" in text,
        "no placeholder leakage": "MMITMATH" not in text,
        "no known broken literal": r"[ t = \text{час}. ]" not in text,
    }

    for name, ok in checks.items():
        if not ok:
            failures.append(f"{book_id}: {name}")

    display_count = text.count(r"\[")
    inline_paren_count = text.count(r"\(")
    inline_dollar_count = text.count("$") // 2
    inline_count = inline_paren_count + inline_dollar_count
    if display_count < 8:
        failures.append(f"{book_id}: too few display-math delimiters ({display_count})")
    if inline_count < 1:
        failures.append(
            f"{book_id}: відсутні роздільники вбудованих формул MathJax "
            f"(paren={inline_paren_count}, dollar_pairs={inline_dollar_count})"
        )

    print(
        f"{book_id}: MathJax PASS "
        f"(display={display_count}, inline={inline_count})"
    )

if failures:
    raise SystemExit(
        "Перевірки відображення формул у мінікнизі не пройдено:\n- " + "\n- ".join(failures)
    )

print(f"MiniBook math rendering: PASS for {len(BOOK_IDS)} books")
