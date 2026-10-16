"""Check 4: label card. Who labelled the data, how, with what instrument, in which population, when."""

from __future__ import annotations

from pathlib import Path

import yaml

from .result import CheckResult

REQUIRED_FIELDS = ("annotator", "method", "instrument", "population", "date_collected")


def _is_empty(value) -> bool:
    return value is None or (isinstance(value, (str, list, dict)) and len(value) == 0) or (
        isinstance(value, str) and not value.strip()
    )


def label_card(path) -> CheckResult:
    path = Path(path)
    if not path.exists():
        return CheckResult("label_card", "skip", f"No label card found at {path}.")

    raw = path.read_text()
    card = yaml.safe_load(raw) or {}
    if not isinstance(card, dict):
        return CheckResult("label_card", "warn", "Label card is not a YAML mapping.", details={"raw": raw})

    missing = [f for f in REQUIRED_FIELDS if _is_empty(card.get(f))]
    metrics = {"n_required": len(REQUIRED_FIELDS), "n_missing": len(missing)}
    details = {"path": str(path), "missing_fields": missing, "card": card, "raw": raw}

    if missing:
        return CheckResult(
            "label_card", "warn", f"Label card is missing or empty: {', '.join(missing)}.", metrics, details
        )
    return CheckResult("label_card", "pass", "Label card has all required provenance fields.", metrics, details)
