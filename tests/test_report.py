from pathlib import Path

import pytest

import constructcheck
from constructcheck import run_all, write_report

EXAMPLE = Path(constructcheck.__file__).parent / "label_card.example.yaml"


@pytest.mark.parametrize("data, expected", [("linked", "pass"), ("mismatched", "warn")])
def test_run_all_and_report(data, expected, model, request, tmp_path):
    d = request.getfixturevalue(data)
    results = run_all(df=d["fused"], modality_a_cols=d["a_cols"], modality_b_cols=d["b_cols"],
                      label_col="label", model=model, df_a=d["a"], df_b=d["b"],
                      subject_col="subject_id", group_col="source", label_card_path=EXAMPLE)
    status = {r.name: r.status for r in results}
    assert status == {"pairing_test": expected, "subject_overlap": expected,
                      "out_of_population": expected, "label_card": "pass"}

    text = write_report(results, tmp_path / "report.md").read_text()
    assert text.startswith("# constructcheck report")
    assert "| pairing_test | " + expected.upper() in text
    assert EXAMPLE.read_text().strip().splitlines()[-1] in text  # card copied verbatim


def test_missing_inputs_skip(tmp_path):
    results = run_all()
    assert [r.status for r in results] == ["skip"] * 4
    assert "missing df" in results[0].summary
    write_report(results, tmp_path / "r.md")
