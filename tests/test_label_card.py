from pathlib import Path

import constructcheck
from constructcheck import label_card

EXAMPLE = Path(constructcheck.__file__).parent / "label_card.example.yaml"


def test_example_card_passes():
    r = label_card(EXAMPLE)
    assert r.status == "pass"
    assert r.details["card"]["instrument"].startswith("SCID-5")


def test_missing_and_empty_fields_warn(tmp_path):
    p = tmp_path / "card.yaml"
    p.write_text("annotator: ''\nmethod: interview\ninstrument:\npopulation: adults\n")
    r = label_card(p)
    assert r.status == "warn"
    assert r.details["missing_fields"] == ["annotator", "instrument", "date_collected"]


def test_missing_file_skips(tmp_path):
    assert label_card(tmp_path / "nope.yaml").status == "skip"
