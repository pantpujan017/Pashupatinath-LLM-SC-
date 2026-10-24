# Data dictionary

Three derived output files from the LLM-SC extraction pipeline, joinable on `review_id`. They hold the records behind the counts reported in the paper.

## Provenance and what is not released

These files contain derived extraction records only. The review texts were obtained from Tripadvisor through a third-party API and are not redistributed, because reuse and redistribution rights for them have not been established. For the same reason, the longer text spans produced during extraction (supporting quotes for entities, evidence for aspect judgements and descriptions of relations) are not released.

`review_id` values are pseudonymous surrogate keys (`R00001` … `R02491`), consistent across all three files. The original platform identifiers are not included. Entity names and relation endpoints are short phrases as they appear in the reviews, so a distinctive phrase could still be matched to its source review by searching for it.

## Licence

No licence is granted for the files in this folder; see `../LICENSE`.

---

## `entity_mentions.csv` — 11,286 rows

One row per extracted entity mention (2,485 reviews).

| Column | Type | Description |
|---|---|---|
| `review_id` | string | Pseudonymous review key |
| `year` | int | Year of review publication (2008–2026) |
| `period` | string | Temporal period: `early_period`, `growth_period`, `pre_covid_peak`, `covid_onset`, `covid_deep`, `recovery_early`, `recovery_late`, `post_recovery` |
| `trip_type` | string | `solo`, `couples`, `friends`, `family`, `business` or `unknown` |
| `entity_name` | string | Surface form of the extracted entity |
| `entity_type` | string | One of the 12 taxonomy types (see `../taxonomy/`) |
| `rating` | int | Star rating 1–5 |

## `relations.csv` — 5,590 rows

One row per extracted relation record (2,433 reviews). After node names are normalized (leading and trailing spaces removed, case-folded, internal whitespace collapsed), the records form a relation network of 5,110 nodes. They yield 5,341 typed edge groups (5,325 with one of the four expected labels and 16 with the out-of-schema label `cultural_rule`) and 5,221 connections in the unweighted undirected projection. Section 3.5 of the paper defines these counts and Section 4.6 reports them.

| Column | Type | Description |
|---|---|---|
| `review_id` | string | Pseudonymous review key |
| `year` | int | Year of review publication |
| `source_node` | string | Source entity name |
| `target_node` | string | Target entity name |
| `relation` | string | `co_occurrence`, `description`, `causal`, `contrast`, or the out-of-schema label `cultural_rule` |

## `aspect_sentiments.csv` — 6,232 rows

One row per aspect-level sentiment judgement (2,487 reviews; mean 2.51 per review).

| Column | Type | Description |
|---|---|---|
| `review_id` | string | Pseudonymous review key |
| `year` | int | Year of review publication |
| `trip_type` | string | As above |
| `aspect` | string | One of nine: `service`, `facility`, `environment`, `ritual_experience`, `spiritual_authenticity`, `access_fairness`, `sacred_atmosphere`, `crowd_management`, `cultural_sensitivity` (7 records carry other labels) |
| `sentiment` | string | `positive`, `neutral` or `negative` (11 records carry other labels) |
| `score` | float | Model-assigned score from 0.0 to 1.0, on the scale anchored in the extraction prompt |
| `rating` | int | Star rating 1–5 |

---

## Redactions

A third party's personal name appeared in entities extracted from five reviews. It is replaced with `[NAME REDACTED]` in the `entity_name` field of those 5 rows. A telephone number in one supporting quote was also redacted; supporting quotes are not released. All other values are as produced by the extraction pipeline.

The dataset was screened for telephone numbers, email addresses, URLs and social handles; this was the only match.

## Known schema violations

Some model outputs violated the prompt's controlled vocabularies. They are retained here as produced:

| Violation | Count |
|---|---|
| Sentiment labels outside the three classes (`mixed` 10, `dual_valence` 1) | 11 |
| Aspect labels outside the nine dimensions (`general_sentiment` 5, `problem` 1, `scenic_spot` 1) | 7 |
| Relation label outside the four types (`cultural_rule`) | 16 |

Section 3.3.3 of the paper reports them; Sections 3.4 and 3.5 describe how they are treated in the evaluation and in the network analysis.
