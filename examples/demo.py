"""Run every check on the two synthetic datasets and write one report for each.

    python examples/demo.py

Writes examples/report_linked.md (should pass) and examples/report_mismatched.md (should warn).
"""

import os
from importlib.resources import files
from pathlib import Path

from sklearn.linear_model import LogisticRegression

from constructcheck import run_all, write_report
from constructcheck.datasets import make_linked, make_mismatched

OUT = Path(__file__).parent
# The example card ships with the package; a relative path keeps the report free of local paths.
LABEL_CARD = os.path.relpath(files("constructcheck") / "label_card.example.yaml")

for name, make in [("linked", make_linked), ("mismatched", make_mismatched)]:
    d = make()
    results = run_all(
        df=d["fused"],
        modality_a_cols=d["a_cols"], modality_b_cols=d["b_cols"], label_col="label",
        model=LogisticRegression(max_iter=1000),
        df_a=d["a"], df_b=d["b"], subject_col="subject_id",
        group_col="source",
        label_card_path=LABEL_CARD,
    )
    path = write_report(results, OUT / f"report_{name}.md", title=f"constructcheck report: make_{name}()")
    print(f"{path}: " + ", ".join(f"{r.name}={r.status}" for r in results))
