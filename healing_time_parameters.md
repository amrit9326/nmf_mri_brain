# DFU Time-to-Healing Prediction — Parameters, Justification & Data Availability

**Status:** New prediction target proposal for the DFU project (prepared 2026-11-18).
**Target variable:** Continuous **time-to-complete-wound-closure** (days/weeks) in diabetic foot ulcers (DFU).
**Relationship to existing work:** This is a *new, distinct* prediction target from the project's primary Gram-type/antibiotic task. Input variables that are also part of the project's standard intake are flagged **[standard intake]**; this document restates all of them in full (§5) so it is self-contained and can be shared on its own.

> **Evidence transparency.** Every citation below is marked **[verified]** (abstract or full text read this session via PubMed/eutils, IWGDF PDF, or publisher page) or **[unverified]** (asserted from prior project literature notes / background knowledge — confirm the DOI before using in a manuscript). Where a source was read full-text vs abstract-only, this is stated. No DOIs or metrics were fabricated; anything I could not verify is labelled as such.

---

## 1. Outcome definition

Complete wound closure is the clinically accepted primary endpoint in DFU trials: **full epithelialization with no drainage, confirmed and maintained** (the regulatory standard typically requires confirmation at a follow-up visit ~2 weeks later). Three framings are relevant:

| Framing | Definition | Use here |
|---|---|---|
| **Continuous time-to-heal** (primary target) | Days/weeks from baseline assessment to confirmed complete closure | Survival/regression target. Censor non-healers at last follow-up. |
| **Healed-by-12-weeks** (binary surrogate) | Closed vs not closed at 12 weeks | Standard trial endpoint; easiest to source external comparators. |
| **4-week % area reduction (PAR)** (early surrogate) | ≥50% wound area reduction at week 4 (Sheehan's validated cut: **≥53%**) | Validated *early* predictor of eventual healing; usable as an interim label and as a model feature. |

Because time-to-heal is right-censored (some ulcers never heal, some patients drop out), the correct statistical framing is **survival analysis / time-to-event regression** (e.g. Cox, accelerated failure time, or a discrete-time / DeepSurv-style neural model), not plain regression on a complete-only subset.

---

## 2. Parameter set (grouped, with justification and citations)

### 2a. Wound characteristics (strongest, most consistent predictors)

| Parameter | Measurement / format | Effect on healing time | Justification | Citation |
|---|---|---|---|---|
| **Baseline wound area** | cm² (planimetry / calibrated smartphone) | Larger area → longer time-to-heal, lower closure probability | Consistently among the strongest independent predictors across cohorts and trials | Sheehan 2003 **[verified, abstract]**; IWGDF 2023 Wound-Healing guideline **[verified, full PDF]** |
| **Wound duration before assessment** | weeks **[standard intake]** | Longer-standing ulcers heal slower | MEDFUN cohort: duration >1 month OR **0.109** (95% CI 0.030–0.395) for healing | Ezeani/MEDFUN 2020 **[verified, abstract]** |
| **Wound depth / grade** | Wagner 0–5 **[standard intake]**; University of Texas grade/stage | Deeper (tendon/bone) → slower healing | MEDFUN: Wagner grade ≥3 a significant predictor of non-healing | Ezeani/MEDFUN 2020 **[verified]**; IWGDF 2023 Classification guideline **[verified, listing only]** |
| **Probe-to-bone / osteomyelitis** | Yes/No **[standard intake]** | Osteomyelitis → markedly slower/failed healing | MEDFUN: osteomyelitis OR **0.035** (95% CI 0.004–0.332) — *strongest single predictor of non-healing* in that cohort | Ezeani/MEDFUN 2020 **[verified]** |
| **Wound location** | plantar / dorsal / heel / toe **[standard intake]** | Heel and midfoot wounds tend to heal slower | Reported across DFU cohorts; weaker/variable than size & perfusion | IWGDF 2023 Classification **[verified, listing]**; general DFU literature **[unverified]** |
| **Number of wounds** | integer | Multiple ulcers → worse prognosis | Reported in cohort literature | **[unverified]** |
| **Prior ulceration / recurrence at same site** | count of previous DFUs; Yes/No same site | More prior ulcers → harder to heal | Prospective cohort (n=208): each previous DFU OR **1.42** (95% CI 1.01–1.99, P=.04) for a hard-to-heal wound | Mohammad Zadeh 2019, *Int Wound J* (PMID 31418528) **[verified, abstract]** |
| **Exudate level** | none / low / moderate / high (extends exudate *type*) | Higher exudate → inflammation/infection → slower healing | Core scored component of validated wound tools (PUSH, DESIGN-R, DFUAS) | Gardner 2011; Sanada 2011 (see §2h) **[verified]** |

### 2b. Early-healing surrogate (the single most actionable dynamic feature)

| Parameter | Measurement / format | Effect | Justification | Citation |
|---|---|---|---|---|
| **4-week percent area reduction (PAR)** | % change in area from week 0 → week 4 | Strong predictor of 12-week healing | Sheehan: ulcers with **≥53% area reduction at 4 weeks** healed in **58%** of cases by 12 weeks vs **9%** below threshold (P<0.01); healers showed mean 82% reduction vs 25% in non-healers. Gwilym 2022 systematic review (6 DFU studies, 21,430 patients): PAR C-statistic **0.720–0.910**; one study sens **58.5%** / spec **90.5%** — but authors caution PAR *alone* is insufficient as a surrogate. | Sheehan 2003, *Diabetes Care*, DOI 10.2337/diacare.26.6.1879 **[verified, abstract]**; Gwilym 2022, *Adv Wound Care*, DOI 10.1089/wound.2021.0203 **[verified, abstract]** |

> **Design implication:** the 4-week PAR requires at least two timepoints. It is the best argument for a *longitudinal* imaging protocol rather than single-shot photos.

### 2c. Perfusion / vascular (second strongest category)

| Parameter | Measurement / format | Effect | Justification | Citation |
|---|---|---|---|---|
| **PAD (peripheral arterial disease)** | Yes/No; ABI <0.9 **[standard intake]** | Present → slower/failed healing | MEDFUN: PAD OR **0.093** (95% CI 0.028–0.311) for healing | Ezeani/MEDFUN 2020 **[verified]**; IWGDF 2023 PAD guideline **[unverified, referenced]** |
| **Ankle-brachial index (ABI)** | ratio (0.7–0.9 borderline; IWGDF uses these bands) | Low ABI → impaired healing | IWGDF wound-healing guideline references ABI 0.7–0.9 / TcPO2 30–50 mmHg perfusion bands | IWGDF 2023 Wound-Healing guideline **[verified, full PDF]** |
| **Toe systolic pressure / toe-brachial index** | mmHg | <30 mmHg → poor healing | Tay 2019 systematic review+meta-analysis: toe pressure >30 mmHg sens **0.86** / spec **0.58** for healing; separate meta-analysis: toe pressure <30 mmHg RR **2.09** (95% CI 1.37–3.20) for non-healing post-amputation | Tay 2019, *Ann Vasc Surg* (PMID 31220591) **[verified, abstract]**; toe-pressure meta-analysis, *Diab Vasc Dis Res* 2020, DOI 10.1177/1479164120928868 **[verified, abstract]** |
| **TcPO2 (transcutaneous oxygen)** | mmHg | <30–40 mmHg → impaired healing | IWGDF perfusion assessment; widely used threshold | IWGDF 2023 Wound-Healing guideline **[verified, full PDF]** |

### 2d. Infection

| Parameter | Measurement / format | Effect | Justification | Citation |
|---|---|---|---|---|
| **Clinical infection present / severity** | IWGDF/IDSA infection grade 1–4 (1 none, 2 mild, 3 moderate, 4 severe/systemic) | Infection → slower healing | Standard DFU prognostic factor | IWGDF/IDSA 2023 Infection guideline **[verified, listing]** |
| **NERDS / STONEES infection scores** | NERDS /5 (superficial); STONEES /7 (deep) | Higher scores → infection burden → slower healing | Structured bedside infection assessment; STONEES "O" captures probe-to-bone/osteomyelitis | Clinical scoring tool (Sibbald et al.) **[unverified]** |
| **CRP / WBC / ESR / procalcitonin** | mg/L, ×10⁹/L, mm/hr, ng/mL | Elevated inflammatory markers → slower healing (esp. in osteomyelitis) | Inflammatory markers tracked with DFU-osteomyelitis healing time | Tardáguila-García 2020, *J Wound Care* (PMID 31930948) **[verified, title/abstract]** |

### 2e. Metabolic / systemic / laboratory

| Parameter | Measurement / format | Effect | Justification | Citation |
|---|---|---|---|---|
| **HbA1c** | % **[standard intake]** | Poor glycaemic control → impaired healing (evidence mixed on magnitude) | MEDFUN: HbA1c ≥7% a significant predictor of non-healing. Vella 2017 specifically questioned whether baseline HbA1c predicts healing *time* — so treat as supportive, not decisive | Ezeani/MEDFUN 2020 **[verified]**; Vella 2017, *J Am Podiatr Med Assoc* (PMID 28880596) **[verified, title]** |
| **Renal function (eGFR) / dialysis** | mL/min/1.73m² **[standard intake]** | Renal impairment / ESRD → worse healing | MEDFUN: renal impairment + proteinuria significant | Ezeani/MEDFUN 2020 **[verified]** |
| **Anaemia / haemoglobin** | g/dL | Anaemia → negative healing prognosis | MEDFUN: anaemia OR **0.179** (95% CI 0.056–0.571); Giangreco 2024 *Acta Diabetol* identified anaemia as a negative healing prognostic factor | Ezeani/MEDFUN 2020 **[verified]**; Giangreco 2024 (PMID 37848718) **[verified, title]** |
| **Serum albumin / nutrition** | g/L | Low albumin → impaired healing | Established nutritional predictor | general DFU literature **[unverified]** |
| **Diabetes duration** | years **[standard intake]** | Longer duration → worse microvascular status | Covariate in most DFU prognostic models | **[unverified]** |
| **Diabetic retinopathy / known microvascular disease** | Yes/No (often already in chart) | Marker of systemic microvascular damage; plausibly → slower healing | Biologically plausible proxy; **direct quantitative DFU-healing effect NOT found in this session's searches** — include as a low-cost covariate, not a proven predictor | **[unverified / weak evidence]** |
| **Lower-limb oedema** | Yes/No, extent | Oedema impairs local perfusion/diffusion → slower healing | Clinically plausible; **direct quantitative DFU-healing effect NOT found this session** — include as cheap covariate | **[unverified / weak evidence]** |

### 2f. Demographics / behaviour / treatment

| Parameter | Measurement / format | Effect | Justification | Citation |
|---|---|---|---|---|
| **Age** | years **[standard intake]** | Older → modestly slower healing (variable) | Common covariate | **[unverified]** |
| **Smoking status** | never/former/current **[standard intake]** | Current smoking impairs perfusion & healing | Established vascular risk | **[unverified]** |
| **BMI** | kg/m² **[standard intake]** | U-shaped / weak association | Covariate | **[unverified]** |
| **Offloading adherence** | device + adherence | Good offloading → faster plantar-ulcer healing | IWGDF offloading guideline (strong recommendation) | IWGDF 2023 Offloading guideline **[verified, listing]** |
| **Revascularisation** | Yes/No + type | Restores perfusion → enables healing in ischaemic ulcers | IWGDF PAD guideline | **[unverified, referenced]** |

### 2g. Imaging-derived features (the project's differentiator)

| Parameter | Measurement / format | Effect | Justification | Citation |
|---|---|---|---|---|
| **Wound area from photo** | cm² (calibrated smartphone) **[standard intake]** | Core feature; feeds PAR | Smartphone wound-area measurement reported to be within ~±8% of expert measurement | **[unverified — original validation study not confirmed this session; locate before citing]** |
| **Serial area-change velocity** | Δarea / Δtime across visits | Faster shrinkage → shorter time-to-heal | Direct image analogue of Sheehan PAR (serial area is the measurable quantity behind 4-week PAR) | Sheehan 2003 (see §2b) **[verified]**; serial-image healing-prediction claim from project notes attributed to "Cassidy DFUC2022" **could NOT be verified — see ref 19** |
| **Tissue composition (% granulation / slough / necrosis / epithelialisation)** | % per tissue class from segmentation | More granulation/epithelialisation → healing; more slough/necrosis → delay | Tissue-type segmentation is an established wound-imaging technique; tissue composition is a recognised healing indicator | **[unverified — supporting primary source not confirmed this session]** |
| **Peri-wound erythema extent** | cm from edge **[standard intake]** | Larger → infection/inflammation → delay | Clinical + image feature | **[unverified]** |
| **Thermal gradient (optional modality)** | °C peri-wound differential | Higher differential → delayed healing | Nakagami 2010 (pressure ulcers): thermal gradient AUC **0.79** for healing prediction | Nakagami 2010, *Exp Dermatol*, DOI 10.1111/j.1600-0625.2010.01099.x **[unverified — from project notes, confirm]** |

### 2h. Composite wound-assessment scores (optional — one validated number instead of many components)

A validated composite score can be recorded longitudinally as a single feature, capturing size + depth + exudate + tissue type together. Useful statistically (one responsive number vs several correlated rows) but **correlated with image-derived area/tissue features — watch for redundancy / collinearity**.

| Score | What it measures | Evidence for predicting healing | Validated in DFU? | Citation |
|---|---|---|---|---|
| **PUSH (Pressure Ulcer Scale for Healing)** | area + exudate + tissue type | Scores fall as ulcers heal (0.67→2.25 units/week); correlation with healing R=0.76. **But length×width alone R=0.81 ≈ full PUSH** — area may already capture most of the signal | **Yes — validated in DFU** | Gardner 2011, *J Wound Ostomy Continence Nurs*, DOI 10.1097/WON.0b013e31821e4dbd **[verified, abstract]** |
| **DESIGN-R** | depth, exudate, size, inflammation, granulation, necrosis, pocket | Baseline score HR **0.90**/point for healing (AUC 0.81 at 30 days); 1-point weekly improvement HR 1.16–1.33 | Validated in **pressure** ulcers, not DFU | Sanada 2011, *Wound Repair Regen*, DOI 10.1111/j.1524-475X.2011.00719.x; Iizaka 2012, DOI 10.1111/j.1524-475X.2012.00778.x **[verified, abstracts]** |
| **DFUAS (Diabetic Foot Ulcer Assessment Scale)** | DFU-specific composite | Cutoff 12 → sens **89%** / spec **71%**; concurrent validity vs BWAT r=0.92, PUSH r=0.87 | **Yes — DFU-specific** | Arisandi 2016, *Wound Repair Regen*, DOI 10.1111/wrr.12464 **[verified, abstract]** |
| **SINBAD** | Site, Ischaemia, Neuropathy, Bacterial infection, Area, Depth | Prognostic component score used in DFU outcome studies | Yes — DFU classification | Naemi & Abbas 2026, *Int Wound J* (PMID 42565341) **[verified, abstract]** |

> **Recommendation:** If adopting one, prefer **PUSH or DFUAS** (DFU-validated). Given that your model already ingests wound area and tissue composition from images, a composite may add limited *independent* signal — consider it mainly as a human-interpretable longitudinal summary / sanity check rather than a primary feature.

### 2i. Treatment / intervention covariates (confounders — record to avoid biased estimates)

These are **not predictors to maximise** but **time-varying confounders**. In a time-to-event model, omitting the care a patient received means the model may misattribute a treatment's effect (or a clinician's response to a worsening wound) to patient/wound features. Record them as time-varying covariates.

| Covariate | Format | Why it matters |
|---|---|---|
| **Debridement events** | date(s), type (sharp/enzymatic/other) | Resets wound area/tissue; directly alters the healing trajectory you are modelling |
| **Antibiotic courses** | drug/class, start–stop dates | Treats infection → changes healing; also links to the project's primary task |
| **Negative-pressure wound therapy (NPWT)** | Yes/No, dates | Accelerates granulation; strong effect on trajectory |
| **Advanced therapies (skin substitutes, growth factors, HBOT)** | type, dates | Known to shorten time-to-heal in trials; must be adjusted for |
| **Offloading device + adherence** | device type, adherence | Already listed in 2f; central for plantar ulcers |
| **Revascularisation** | Yes/No, date, type | Already listed in 2f; step-changes perfusion mid-trajectory |

> **Modelling note:** these make the problem properly a *time-varying-covariate survival model*. At minimum, record them so healing-time estimates are not confounded; ideally include them as covariates. This is a **correctness** requirement, not an optional feature.

---

## 3. Ranked shortlist — strongest evidence-based predictors of DFU time-to-healing

Ranked by strength and consistency of evidence found this session:

1. **4-week percent area reduction (PAR)** — strongest *dynamic* predictor (Sheehan; Gwilym C-stat 0.72–0.91). Requires ≥2 timepoints.
2. **Baseline wound area** — strongest *static* predictor; feeds PAR.
3. **PAD / perfusion (ABI, toe pressure, TcPO2)** — PAD OR 0.093; toe pressure sens 0.86. Second strongest category.
4. **Osteomyelitis / wound depth (probe-to-bone, Wagner grade)** — osteomyelitis OR 0.035 (strongest single factor in MEDFUN).
5. **Wound duration before treatment** — OR 0.109.
6. **Infection presence/severity + inflammatory markers (CRP)**.
7. **Renal impairment / eGFR**.
8. **Anaemia / haemoglobin** — OR 0.179.
9. **HbA1c / glycaemic control** — significant but magnitude debated (Vella caveat).
10. **Prior ulceration count** — each previous DFU OR 1.42; cheap to collect, consistent signal.
11. **Serial image area-velocity & tissue composition** — the imaging differentiator; strong mechanistic basis, thinner published validation for *continuous* time-to-heal.

> Composite scores (PUSH/DFUAS) and treatment covariates (§2h, §2i) are deliberately **not** ranked here: the composite largely re-encodes area/tissue already captured, and treatment covariates are confounders to adjust for, not predictors to rank.

---

## 4. Data availability verdict

**Honest bottom line: no public dataset supports continuous time-to-heal modelling from wound images + clinical data. The gap is real and is the same bottleneck as the project's primary task.**

| Dataset | Modality | Size | Healing / time-to-heal / longitudinal label? | License / access | Suitable for time-to-heal? |
|---|---|---|---|---|---|
| **DFUC2022** (grand-challenge / Zenodo) | DFU photos | 2,000 train + 2,000 test | **No** — pixel-wise segmentation masks only; not serial per-patient; no outcome labels (confirmed via Yap 2024 *Med Image Anal* benchmark paper, ref 17) | Application / challenge terms | No |
| **DFUC2020 / 2021** | DFU photos | thousands | **No** — detection/classification (ischaemia, infection), not healing-outcome | Challenge terms | No |
| **FUSeg / AZH chronic wound** (uwm-bigdata GitHub) | chronic-wound photos | ~1,000+ | **No** — segmentation masks only; "publicly shared with AZH permission"; no healing outcome | Public via GitHub | No (images only) |
| **MIMIC-IV** (PhysioNet) | EHR tabular + notes | ~300k+ admissions | **Partial/weak** — ICD-coded DFU diagnoses, labs, meds, some notes; **no wound photos, no structured wound assessments or healing-stage documentation**; population-level outcomes only | Credentialed: CITI training + PhysioNet DUA | Clinical-only, weak for wound-specific trajectory |
| **DRIAMS** (Dryad) | MALDI-TOF spectra + AST | large | **No** — microbiology, no wound/healing data | Open (Dryad) | No |
| **Medetec / other image banks** | wound photos | varies | **No** — teaching images, no outcome labels | Varies | No |
| **UK Biobank / registries** | tabular | large | **Rarely** — may hold DFU diagnoses but not standardised serial wound tracking | Application | Weak |

PubMed search for a *public longitudinal DFU image dataset with healing outcomes* returned **zero** results. Published ML wound work is overwhelmingly **segmentation or binary classification** (Yap 2024 DFUC segmentation; Sendilraj 2024 DFUCare smartphone infection/ischaemia). The Cassidy group's verified DFU papers are segmentation/detection/dataset work (*Sci Rep* 2025, *Diabetes Res Clin Pract* 2023, *touchREV Endocrinol* 2021), **not** continuous healing-trajectory prediction. **No published model performs continuous time-to-heal regression from smartphone RGB + clinical data** — confirming this as a genuine, publishable research gap.

---

## 5. What we need to collect (prospective protocol)

Since no suitable dataset exists, continuous time-to-heal modelling requires **prospective longitudinal collection**. The full variable list, imaging SOP, and treatment log below are self-contained — this document can be shared and used on its own, with no companion file required.

### 5.1 Baseline variables (full list)

**Cohort / eligibility & administrative**

| Variable | Format | Note |
|---|---|---|
| Clinic site | site ID | Multi-site model: include as random effect / covariate to absorb site differences in care |
| Clinician ID | ID | Optional; confounder for care quality |
| Consent obtained | Yes/No | Required for enrolment |

**Demographics**

| Variable | Format |
|---|---|
| Patient ID | DFU-XXX |
| Date of visit | DD/MM/YYYY |
| Age | years |
| Sex | Male / Female / Other |
| BMI | kg/m² |
| Diabetes type | Type 1 / Type 2 / Other |
| Diabetes duration | years |

**Mandatory clinical variables**

| # | Variable | Format |
|---|---|---|
| 1 | Prior antibiotic exposure (last 90 days) | Yes/No + class |
| 2 | Prior hospitalisation (last 90 days) | Yes/No |
| 3 | Wound duration | weeks |
| 4 | Wagner grade | 0–5 |
| 5 | Wound depth | Superficial / Deep (tendon/capsule) / Bone (probe-to-bone +ve) |
| 6 | HbA1c | % (1 dp) |
| 7 | CRP | mg/L |
| 8 | WBC count | ×10⁹/L |
| 9 | Peripheral arterial disease (PAD / ABI <0.9) | Yes/No |
| 10 | eGFR | mL/min/1.73m² |

**Recommended clinical variables**

| # | Variable | Format |
|---|---|---|
| 11 | Temperature | °C |
| 12 | ESR | mm/hr |
| 13 | Procalcitonin | ng/mL |
| 14 | Wound area | cm² — **note: upgraded to MANDATORY for time-to-heal, see H1** |
| 15 | Exudate type | Serous / Seropurulent / Purulent |
| 16 | Peri-wound erythema extent | cm from edge |
| 17 | Prior MDR infection history | Yes/No |
| 18 | Neuropathy present | Yes/No |
| 19 | Wound location | Plantar / Dorsal / Heel / Toe / Other |
| 20 | Smoking status | Never / Former / Current |
| 21 | IWGDF/IDSA infection grade | 1 (none) / 2 (mild) / 3 (moderate) / 4 (severe) |
| 22 | NERDS score (superficial infection) | /5 |
| 23 | STONEES score (deep infection) | /7 |

**Healing-specific additions (NEW — required for time-to-heal)**

| # | Variable | Format | Rationale (§ref) |
|---|---|---|---|
| H1 | **Baseline wound area — now MANDATORY** (not optional #14) | cm² (scale-calibrated) | Core predictor + basis of 4-week PAR (§2a, §2b) |
| H2 | **ABI and/or toe systolic pressure** (TcPO2 where available) | ratio / mmHg | Perfusion — second strongest category (§2c) |
| H3 | **Serum albumin** | g/L | Nutritional predictor (§2e) |
| H4 | **Haemoglobin** | g/dL | Anaemia OR 0.179 (§2e) |
| H5 | **Prior ulceration count / same-site recurrence** | integer; Yes/No | Each prior DFU OR 1.42 (§2a) |
| H6 | **Exudate level** (extends #15 type) | None / Low / Moderate / High | Scored wound component (§2a, §2h) |
| H7 | **Diabetic retinopathy / microvascular disease** | Yes/No | Low-cost covariate, weak direct evidence (§2e) |
| H8 | **Lower-limb oedema** | Yes/No, extent | Low-cost covariate, weak direct evidence (§2e) |
| H9 | **Offloading prescribed** | device type | Treatment covariate (§2f, §2i) |
| H10 | **Revascularisation status** | Yes/No, type, date | Step-changes perfusion mid-trajectory (§2f, §2i) |
| H11 | **Composite score (optional)** — prefer PUSH or DFUAS | score | Single longitudinal summary (§2h) |

> Any mandatory variable unavailable → record as **missing** (do not exclude the patient); handle by imputation at training.

### 5.2 Imaging protocol (per visit)

Smartphone RGB photograph of the wound, repeated identically **at every follow-up visit** (not just baseline):

| Step | Action | Why |
|---|---|---|
| 1 | Clean wound gently — remove exudate/dressings | Wound bed must be visible |
| 2 | Place colour calibration card/ruler next to wound | Enables colour correction + **cm² scale (needed for area & PAR)** |
| 3 | Position camera 20–30 cm above wound | Consistent scale and focus |
| 4 | Hold camera perpendicular (90°) to wound surface | Minimise perspective distortion |
| 5 | Ensure wound fills ≥30% of frame | Sufficient detail for CNN |
| 6 | Natural light or overhead white LED — **NO flash** | Flash glare distorts wound colour |
| 7 | Take 3 photos (front, slight left, slight right) | Redundancy; keep best |
| 8 | Name file: `PatientID_Date_View` (e.g. `DFU001_20260901_front.jpg`) | Traceability + links timepoints per patient |
| 9 | Exclude face / identifiable body parts | Privacy |

**Per-visit quality check:** wound bed fully visible ✓, calibration card in frame ✓, no glare/harsh shadows ✓.

> **Critical for time-to-heal:** serial, consistently-calibrated photos across visits are what enable wound-area velocity and 4-week PAR — the strongest dynamic predictors (§2b, §2g).

### 5.2b Treatment-event log (NEW — record every visit)

Record interventions as **time-varying covariates** so healing-time estimates are not confounded (§2i):

| Event | Capture |
|---|---|
| Debridement | date(s), type (sharp/enzymatic/other) |
| Antibiotic course | drug/class, start–stop dates |
| NPWT | Yes/No, dates |
| Advanced therapy (skin substitute / growth factor / HBOT) | type, dates |
| Offloading adherence | device, adherence this interval |
| Revascularisation | date, type |


### 5.3 Follow-up cadence
- **Baseline (week 0), then weekly for the first 4 weeks** (to capture 4-week PAR accurately), then **every 1–2 weeks** until the endpoint.
- Continue until **confirmed complete closure** or a **censoring event** (amputation, death, loss to follow-up, or study end).

### 5.4 Healing endpoint definition (record explicitly)
- **Complete closure** = full epithelialisation, no drainage, **confirmed at a visit ≥2 weeks later** (regulatory-standard confirmation to avoid false "healed" calls).
- Record **date of first observed closure** and **date of confirmation** → time-to-heal = (confirmed-closure date − baseline date).
- Record **censoring reason + date** for non-healers.
- Also derivable: 4-week PAR label and healed-by-12-weeks binary label.

### 5.5 Sample size & duration
- DFU healing studies typically run **12 weeks** minimum follow-up for the binary endpoint; **continuous time-to-heal needs follow-up to actual closure**, often **up to 20–34 weeks** (the IWGDF-reviewed trials spanned follow-up from hours to 34 weeks).
- For a multimodal model, target **n ≥ 300** completed-follow-up patients (consistent with the project's existing n≥300 target), powered for the number of predictors (rule of thumb: ≥10 events per predictor; with ~10–15 predictors and a ~50–70% healing rate, n≈300 is a reasonable floor; **a formal sample-size calculation should be done once the primary model and expected C-index are fixed**).
- Expect **15–24 months** of calendar time at a busy DFI clinic to accrue and follow this cohort (matches the project's data-collection roadmap).

---

## 6. References

Grouped; verification status as used above. **Confirm all DOIs/PMIDs before manuscript submission**, especially those marked [unverified].

**Clinical predictors**
1. Sheehan P, et al. Percent change in wound area of diabetic foot ulcers over a 4-week period is a robust predictor of complete healing in a 12-week prospective trial. *Diabetes Care*. 2003;26(6):1879–82. DOI 10.2337/diacare.26.6.1879. **[verified, abstract]**
2. Gwilym BL, et al. Initial Reduction in Ulcer Size as a Prognostic Indicator for Complete Wound Healing (systematic review). *Adv Wound Care*. 2022. DOI 10.1089/wound.2021.0203. **[verified, abstract]**
3. Ezeani IU, et al. Determinants of wound healing in patients hospitalized for diabetic foot ulcer (MEDFUN study). *Endocr Regul*. 2020. DOI 10.2478/enr-2020-0023 (PMID 32857716). **[verified, abstract]**
4. Tay WL, et al. Toe Pressure in Predicting Diabetic Foot Ulcer Healing: a systematic review and meta-analysis. *Ann Vasc Surg*. 2019 (PMID 31220591). **[verified, abstract]**
5. Toe systolic blood pressure and post-amputation healing (meta-analysis). *Diab Vasc Dis Res*. 2020. DOI 10.1177/1479164120928868. **[verified, abstract]**
6. Vella L, Gatt A, Formosa C. Does Baseline HbA1c Predict Diabetic Foot Ulcer Outcome or Wound Healing Time? *J Am Podiatr Med Assoc*. 2017 (PMID 28880596). **[verified, title]**
7. Giangreco F, et al. Anaemia as a negative healing prognostic factor in diabetic foot patients. *Acta Diabetol*. 2024 (PMID 37848718). **[verified, title]**
8. Tardáguila-García A, et al. Inflammatory markers in healing time of diabetic foot osteomyelitis. *J Wound Care*. 2020 (PMID 31930948). **[verified, title/abstract]**
9. Mohammad Zadeh, et al. Outcome predictors for wound healing in patients with a diabetic foot ulcer. *Int Wound J*. 2019 (PMID 31418528). Prior-ulceration OR 1.42. **[verified, abstract]**

**Composite wound-assessment scores**
10. Gardner SE, et al. A prospective study of the PUSH tool in diabetic foot ulcers. *J Wound Ostomy Continence Nurs*. 2011. DOI 10.1097/WON.0b013e31821e4dbd. **[verified, abstract]**
11. Sanada H, et al. DESIGN-R total score predicts pressure ulcer healing. *Wound Repair Regen*. 2011. DOI 10.1111/j.1524-475X.2011.00719.x. **[verified, abstract]**
12. Iizaka S, et al. Predictive validity of weekly DESIGN-R score change. *Wound Repair Regen*. 2012. DOI 10.1111/j.1524-475X.2012.00778.x. **[verified, abstract]**
13. Arisandi D, et al. Validity of the Diabetic Foot Ulcer Assessment Scale (DFUAS). *Wound Repair Regen*. 2016. DOI 10.1111/wrr.12464. **[verified, abstract]**
14. Naemi R, Abbas A. SINBAD score components as prognostic markers in DFU. *Int Wound J*. 2026 (PMID 42565341). **[verified, abstract]**

**Guidelines**
15. IWGDF. Guideline on interventions to enhance healing of foot ulcers in persons with diabetes (IWGDF 2023-07 Wound-Healing). **[verified, full PDF read via pdftotext]**
16. IWGDF. 2023 Classification, Infection (IWGDF/IDSA), PAD, and Offloading guidelines. iwgdfguidelines.org. **[verified, document index; individual content not all read]**

**Imaging / ML**
17. Yap MH, et al. Diabetic foot ulcers segmentation challenge report: benchmark and analysis. *Med Image Anal*. 2024 (PMID 38569380). **[verified, abstract]**
18. Sendilraj V, et al. DFUCare: deep learning platform for DFU detection, analysis, and monitoring (smartphone). *Front Endocrinol*. 2024 (PMID 39381435). **[verified, abstract]**
19. Cassidy B, et al. — the project notes cite a "Cassidy 2022, *Sci Rep*, DOI 10.1038/s41598-022-07592-2" as a DFU healing-trajectory paper. **This could NOT be verified this session:** that DOI did not resolve to such a paper, and the Cassidy group's verified DFU work is segmentation/detection/dataset-description (*Sci Rep* 2025 DOI 10.1038/s41598-025-03393-x; *Diabetes Res Clin Pract* 2023 DOI 10.1016/j.diabres.2023.110951; *touchREV Endocrinol* 2021 DOI 10.17925/EE.2021.17.1.5), **not** continuous healing-trajectory prediction. **Do not cite the 2022 trajectory claim without finding the actual source.**
20. Nakagami G, et al. Predicting delayed pressure ulcer healing using thermography. *Exp Dermatol*. 2010. DOI 10.1111/j.1600-0625.2010.01099.x. **[unverified — from project notes]**

**Data availability**
21. DFUC2022 dataset — segmentation only, no healing labels (confirmed via ref 17). **[verified]**
22. FUSeg / AZH chronic wound dataset — github.com/uwm-bigdata/wound-segmentation — segmentation only. **[verified, landing page]**
23. MIMIC-IV — physionet.org/content/mimiciv — credentialed (CITI + DUA); no wound imaging/assessments. **[verified, landing page]**
