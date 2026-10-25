# Session 1 data: the Home BP Coaching Trial (fictional)

All values are simulated. Kestrel Valley Health does not exist.

| File | What it is |
|---|---|
| `enrollment.csv` | One row per randomized participant, **as received**, with problems left in on purpose (Lab 1) |
| `visits.csv` | One row per clinic visit at weeks 0, 4, 8, and 12, **as received**, with problems left in on purpose (Lab 1). A missed visit has no row. |
| `analysis_s1.csv` | The cleaned table, one row per participant (the Lab 1 result and the Lab 2 starting point) |

## enrollment.csv

| Column | Meaning |
|---|---|
| `participant_id` | Study ID, KV1001 to KV1240 |
| `site` | Clinic: North or South |
| `arm` | Randomized group: coaching or usual care |
| `randomization_date` | Date randomized (YYYY-MM-DD) |
| `age` | Age in years |
| `sex` | F or M |
| `bmi` | Body mass index (kg/m²); blank if not recorded |
| `diabetes` | yes or no |
| `smoker` | Current smoker, yes or no; blank if not asked |
| `n_bp_meds` | Number of BP medications at baseline |

## visits.csv

| Column | Meaning |
|---|---|
| `participant_id` | Study ID |
| `visit_week` | 0 (baseline), 4, 8, or 12 |
| `visit_date` | Date of the visit |
| `sbp`, `dbp` | Systolic and diastolic office BP (mmHg) |
| `weight` | Weight (kg) |

## analysis_s1.csv

The enrollment columns, plus `sbp_w0`, `dbp_w0` (baseline) and `sbp_w12`, `dbp_w12` (week 12), in mmHg.
