# constructcheck report: make_mismatched()

| Check | Status | Summary |
|---|---|---|
| pairing_test | WARN | Breaking the A-B pairing (within_class shuffle) changes accuracy by only +0.01 (threshold 0.10); the modalities may not be contributing jointly. |
| subject_overlap | WARN | Possible construct mismatch: the two tables share no subject IDs. |
| out_of_population | WARN | Accuracy drops by 0.40 when group 'site_2' is held out (threshold 0.10). |
| label_card | PASS | Label card has all required provenance fields. |

## pairing_test

**Status: WARN**. Breaking the A-B pairing (within_class shuffle) changes accuracy by only +0.01 (threshold 0.10); the modalities may not be contributing jointly.

| Metric | Value |
|---|---|
| paired_acc | 0.906 |
| shuffled_acc | 0.898 |
| drop | 0.008 |
| modality_a_only_acc | 0.882 |
| modality_b_only_acc | 0.672 |

- **shuffle**: within_class
- **cv**: 5
- **min_drop**: 0.100
- **n**: 500

## subject_overlap

**Status: WARN**. Possible construct mismatch: the two tables share no subject IDs.

| Metric | Value |
|---|---|
| n_subjects_a | 500 |
| n_subjects_b | 500 |
| n_shared | 0 |
| overlap_fraction | 0.000 |
| label_tvd | 0.248 |
| shared_label_agreement | None |

- **label_values_a**: ['0', '1']
- **label_values_b**: ['0', '1']
- **label_distribution_a**: {'0': 0.524, '1': 0.476}
- **label_distribution_b**: {'1': 0.724, '0': 0.276}

## out_of_population

**Status: WARN**. Accuracy drops by 0.40 when group 'site_2' is held out (threshold 0.10).

| Metric | Value |
|---|---|
| within_population_acc | 0.906 |
| leave_one_group_out_acc | 0.532 |
| drop | 0.374 |
| worst_group | site_2 |
| worst_group_drop | 0.404 |
| n_groups | 2 |

**per_group**

|  | n | within_acc | held_out_acc | drop |
|---|---|---|---|---|
| site_1 | 250 | 0.904 | 0.560 | 0.344 |
| site_2 | 250 | 0.908 | 0.504 | 0.404 |

- **group_col**: source
- **max_drop**: 0.100

## label_card

**Status: PASS**. Label card has all required provenance fields.

| Metric | Value |
|---|---|
| n_required | 5 |
| n_missing | 0 |

Label card (`src/constructcheck/label_card.example.yaml`), verbatim:

```yaml
# constructcheck label card
# One card per label column. Every field below is required; fill each in plainly.
# If two modalities were labelled differently, write one card per modality.

annotator: >-
  Two board-certified psychiatrists, blind to the wearable data;
  disagreements resolved by a third rater.
method: >-
  Structured clinical interview at enrolment; label = current mood episode
  (euthymia / depression / mania) on the interview date.
instrument: SCID-5-RV, with YMRS and MADRS severity scores
population: >-
  Adult outpatients (18-65) with a DSM-5 bipolar I/II diagnosis,
  recruited from two university clinics.
date_collected: 2024-03 to 2025-01

# Optional, but useful for reviewers
label_values:
  0: euthymia
  1: depression
  2: mania
notes: Label refers to the episode at interview, not to each sensor window.
```
