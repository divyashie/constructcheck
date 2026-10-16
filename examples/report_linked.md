# constructcheck report: make_linked()

| Check | Status | Summary |
|---|---|---|
| pairing_test | PASS | Breaking the A-B pairing (within_class shuffle) drops accuracy by 0.242; pairing carries signal. |
| subject_overlap | PASS | 500 shared subjects (100% of all IDs) with consistent label definitions. |
| out_of_population | PASS | Held-out-group accuracy stays within 0.10 of within-population accuracy for all 2 groups. |
| label_card | PASS | Label card has all required provenance fields. |

## pairing_test

**Status: PASS**. Breaking the A-B pairing (within_class shuffle) drops accuracy by 0.242; pairing carries signal.

| Metric | Value |
|---|---|
| paired_acc | 0.900 |
| shuffled_acc | 0.658 |
| drop | 0.242 |
| modality_a_only_acc | 0.588 |
| modality_b_only_acc | 0.590 |

- **shuffle**: within_class
- **cv**: 5
- **min_drop**: 0.100
- **n**: 500

## subject_overlap

**Status: PASS**. 500 shared subjects (100% of all IDs) with consistent label definitions.

| Metric | Value |
|---|---|
| n_subjects_a | 500 |
| n_subjects_b | 500 |
| n_shared | 500 |
| overlap_fraction | 1.000 |
| label_tvd | 0.000 |
| shared_label_agreement | 1.000 |

- **label_values_a**: ['0', '1']
- **label_values_b**: ['0', '1']
- **label_distribution_a**: {'0': 0.526, '1': 0.474}
- **label_distribution_b**: {'0': 0.526, '1': 0.474}

## out_of_population

**Status: PASS**. Held-out-group accuracy stays within 0.10 of within-population accuracy for all 2 groups.

| Metric | Value |
|---|---|
| within_population_acc | 0.900 |
| leave_one_group_out_acc | 0.888 |
| drop | 0.012 |
| worst_group | site_1 |
| worst_group_drop | 0.020 |
| n_groups | 2 |

**per_group**

|  | n | within_acc | held_out_acc | drop |
|---|---|---|---|---|
| site_2 | 252 | 0.905 | 0.901 | 0.004 |
| site_1 | 248 | 0.895 | 0.875 | 0.020 |

- **group_col**: source
- **max_drop**: 0.100

## label_card

**Status: PASS**. Label card has all required provenance fields.

| Metric | Value |
|---|---|
| n_required | 5 |
| n_missing | 0 |

Label card (`label_card.example.yaml`), verbatim:

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
