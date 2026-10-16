"""Run every check that has its inputs, and write one Markdown report."""

from __future__ import annotations

from pathlib import Path

from .label_card import label_card
from .out_of_population import out_of_population
from .pairing import pairing_test
from .result import CheckResult
from .subject_overlap import subject_overlap


def _skip(name, **needed) -> CheckResult | None:
    missing = [k for k, v in needed.items() if v is None]
    if missing:
        return CheckResult(name, "skip", f"Not run: missing {', '.join(missing)}.")
    return None


def run_all(
    df=None, modality_a_cols=None, modality_b_cols=None, label_col=None, model=None,
    df_a=None, df_b=None, subject_col=None, group_col=None, label_card_path=None,
    cv=5, random_state=0,
) -> list[CheckResult]:
    """Run whichever checks have the inputs they need; the others come back as "skip".

    df: the fused, row-aligned training table. df_a / df_b: the separate per-modality tables.
    """
    results = []

    results.append(_skip("pairing_test", df=df, modality_a_cols=modality_a_cols,
                         modality_b_cols=modality_b_cols, label_col=label_col, model=model)
                   or pairing_test(df, modality_a_cols, modality_b_cols, label_col, model,
                                   cv=cv, random_state=random_state))

    results.append(_skip("subject_overlap", df_a=df_a, df_b=df_b, subject_col=subject_col, label_col=label_col)
                   or subject_overlap(df_a, df_b, subject_col, label_col))

    feature_cols = (list(modality_a_cols or []) + list(modality_b_cols or [])) or None
    results.append(_skip("out_of_population", df=df, feature_cols=feature_cols, label_col=label_col,
                         group_col=group_col, model=model)
                   or out_of_population(df, feature_cols, label_col, group_col, model,
                                        cv=cv, random_state=random_state))

    results.append(_skip("label_card", label_card_path=label_card_path) or label_card(label_card_path))
    return results


def _fmt(v) -> str:
    if isinstance(v, float):
        return f"{v:.3f}"
    return str(v).replace("|", "\\|").replace("\n", " ")


def _table(header, rows) -> list[str]:
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(_fmt(c) for c in row) + " |" for row in rows]
    return lines + [""]


def _section(r: CheckResult) -> list[str]:
    lines = [f"## {r.name}", "", f"**Status: {r.status.upper()}**. {r.summary}", ""]
    if r.metrics:
        lines += _table(["Metric", "Value"], r.metrics.items())

    if r.name == "label_card" and "raw" in r.details:
        lines += [f"Label card (`{Path(r.details.get('path', '')).name}`), verbatim:", "", "```yaml", r.details["raw"].rstrip(), "```", ""]
        return lines

    for key, value in r.details.items():
        if isinstance(value, dict) and value and all(isinstance(v, dict) for v in value.values()):
            cols = list(next(iter(value.values())))
            lines += [f"**{key}**", ""] + _table([""] + cols, [[k, *(v[c] for c in cols)] for k, v in value.items()])
        else:
            lines.append(f"- **{key}**: {_fmt(value)}")
    return lines + [""]


def write_report(results, path, title="constructcheck report") -> Path:
    lines = [f"# {title}", ""]
    lines += _table(["Check", "Status", "Summary"], [(r.name, r.status.upper(), r.summary) for r in results])
    for r in results:
        lines += _section(r)
    path = Path(path)
    path.write_text("\n".join(lines).rstrip() + "\n")
    return path
