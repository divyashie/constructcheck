# constructcheck

Flag construct mismatch in multimodal health ML datasets before publication.
Companion to the JMIR preprint on construct validity in multimodal mental-health ML.

A model can score well on a "multimodal" dataset whose modalities never described the same
people, or whose labels mean different things in each source. `constructcheck` runs four quick
checks with any scikit-learn estimator and writes one Markdown report.

| Check | Question | Warns when |
|---|---|---|
| `pairing_test` | Does the model need A and B from the *same* person? | Shuffling B relative to A (within each class, by default) drops accuracy by < `min_drop` |
| `subject_overlap` | Do the two modality tables describe the same subjects, labelled the same way? | No shared IDs, different label values, or shared subjects whose labels disagree |
| `out_of_population` | Does performance survive an unseen site/source? | Leave-one-group-out accuracy is > `max_drop` below within-population CV for any group |
| `label_card` | Is it documented who labelled the data, how, with what, in whom, and when? | A required field is missing or empty |

## Install

```bash
pip install git+https://github.com/divyashie/constructcheck
```

Requires Python ≥ 3.10, numpy, pandas, scikit-learn and pyyaml.

## Use

```python
from sklearn.linear_model import LogisticRegression
from constructcheck import run_all, write_report
from constructcheck.datasets import make_mismatched

d = make_mismatched()            # or make_linked() for a dataset that should pass
results = run_all(
    df=d["fused"],                       # the row-aligned table you train on
    modality_a_cols=d["a_cols"], modality_b_cols=d["b_cols"], label_col="label",
    model=LogisticRegression(max_iter=1000),
    df_a=d["a"], df_b=d["b"], subject_col="subject_id",   # the separate modality tables
    group_col="source",
    label_card_path="label_card.yaml",
)
write_report(results, "constructcheck_report.md")
```

Checks without the inputs they need are reported as `skip`. Each check is also callable on its own
and returns a `CheckResult(name, status, summary, metrics, details)`.

Copy the [example label card](src/constructcheck/label_card.example.yaml) to start your own.

### Why the pairing test shuffles within class

Fused datasets are often built by pairing rows from two unrelated cohorts that share a label. Then
modality B carries label information on its own, so an across-class shuffle shows a large drop even
though no person-level pairing exists. The default `shuffle="within_class"` keeps every row's label
and only breaks *which person* the B row came from. Use `shuffle="across"` for the naive version.

## Development

```bash
pip install -e ".[test]"
pytest
```

## Licence

MIT
