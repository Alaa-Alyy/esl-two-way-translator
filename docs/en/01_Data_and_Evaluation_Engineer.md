<div class="cover" markdown="1">
<div class="kicker">ROLE DOCUMENT 01</div>
<div class="title">Data & Evaluation Engineer</div>
<div class="subtitle">Clean, versioned data that any new dataset can join in one step, and honest, strong numbers for the defense</div>
<div class="meta">
<div><b>Project:</b> Two-Way Egyptian Sign Language Translation App</div>
<div><b>Owner:</b> ______________________</div>
<div><b>Read with:</b> 00 — Project Master Document</div>
<div><b>Version:</b> 1.0 · November 2026</div>
</div>
</div>

# 1. Your role in one paragraph

You own **the data and the truth about how well the system works**. Every other role builds on the files you produce: the vocabulary, the organized clips, the metadata, and the signer-based splits. You also make sure that when Egyptian data appears, it can join the project by running one script. At the end, you own the evaluation plan and the user studies, so that every number we present in the defense is correct, reproducible, and convincing.

# 2. The project in brief

A two-way Android app for one domain (clinic reception):

- **Direction 1:** a Deaf person signs a sentence → the app shows a natural Egyptian Arabic sentence and speaks it.
- **Direction 2:** a hearing person speaks Egyptian Arabic → the app shows the text and a 3D avatar signs the sentence smoothly.
- Recognition runs on the phone from body, hand, and face **landmarks** (MediaPipe). Nothing about specific signs is hard-coded: everything is driven by `vocabulary.csv`, model files, and phrase tables.
- We start with **KArSL-502** (Unified Arabic Sign Language, 3 signers) and move to Egyptian data later. Target vocabulary: 50 → ~100 signs.
- Users can add their own signs ("My Signs") and share them for approval.

```
 YOU (1) ──vocabulary.csv, clips/, metadata.csv, splits/──> CV (2), ML (3), NLP (5), Avatar (6)
 CV (2) ──landmarks / features──> you use them for data quality checks
 Mobile (4) ──My Signs submissions──> you run the review and merge flow
```

# 3. Your responsibilities

**Dataset**

- Select the signs from KArSL together with the team, starting with 50 and growing to ~100, and keep `vocabulary.csv` as the master list.
- Count how many KArSL words fit the clinic domain; propose replacements where a needed word is missing.
- Download **only** the selected signs; organize clips with fixed names `SignID_SignerID_Take`.
- Create `metadata.csv` for every clip (signer, take, dominant hand, fps, frame count, quality flag).
- Flag bad clips (cut signs, hands out of frame) with help from CV's quality checks.
- Version the data: `v1` = KArSL-50, `v2` = KArSL-100, `v3` = + Egyptian data, and so on.

**Splits and evaluation protocol**

- Create **Leave-One-Signer-Out (LOSO)** splits and freeze them in `splits/`.
- Keep a small fixed "demo set" that is never used in training.
- Write `evaluation_plan.md`: metrics, how each is computed, which data, which targets (targets set after the baseline).
- Collect the final numbers from every role into one results table for the report.

**Egyptian data readiness**

- Search for and review Egyptian datasets (AAST 55-word set on Mendeley, Ibrahim et al. 2025, any new ones): signers, words, quality, licence.
- Write `dataset_adapter.py`, which converts any external dataset into our clip naming, folder layout, and metadata format.
- Map Egyptian words to `vocabulary.csv` (shared, new, conflicting).
- Coordinate with an Egyptian sign language interpreter to fill the `esl_verified` column.

**My Signs review flow (with Mobile)**

- Design the review workflow: submission → review by interpreter / Deaf partners → approve / reject → merge.
- A simple review page (web) listing submissions, with play, approve, reject, region tag.
- Merge approved signs into the vocabulary; apply the "at least 3 contributors before entering the shared model" rule.

**User studies**

- Plan the user tests: tasks, scenario, consent form, System Usability Scale (SUS) questionnaire, timing, error counting.
- Contact Deaf associations / schools for the Deaf early (month 1) for testers and reviewers.
- Run the sessions in month 5 with the team and write the results.

# 4. Inputs you receive

| Input | From | Format | When |
|---|---|---|---|
| KArSL-502 raw data | Kaggle (`yousefdotpy/karsl-502`) and original KArSL source | Videos / frames / skeleton (to be confirmed) | Week 1 |
| Egyptian datasets | Mendeley, papers, associations | Various | Any time |
| Quality flags and landmark statistics | Computer Vision (2) | CSV / report | Month 1–2 |
| My Signs submissions | Mobile App (4) via Firebase | C11 JSON + landmarks | Month 4–5 |
| Interpreter decisions | Egyptian interpreter / Deaf partners | Notes → `esl_verified` | Ongoing |
| Results from every role | Roles 2, 3, 4, 5, 6 | Reports | Months 2–5 |

# 5. Outputs you deliver

| Output | Format | Used by | Due |
|---|---|---|---|
| `data/vocabulary.csv` (contract C1) | CSV, UTF-8 | Everyone | Week 2 (v1), Month 3 (v2) |
| `data/clips/` + `data/metadata.csv` (C2) | Files + CSV | CV, ML, Avatar | Month 1 |
| `data/splits/` | One file per LOSO fold + demo set | ML, CV | Month 1 |
| `docs/data_card.md` | Description of each data version | Everyone, report | Month 1, updated |
| `data-pipeline/dataset_adapter.py` | Python script + README | Everyone | Month 2 |
| `docs/egyptian_datasets_review.md` | Comparison table | Team, report | Month 2 |
| `docs/evaluation_plan.md` | Document | Everyone | Week 2, updated |
| Review page for My Signs | Small web page on Firebase | Reviewers | Month 5 |
| User study materials and results | Consent form, tasks, SUS, report | Report | Month 5 |
| `docs/results.md` | All final numbers in one place | Report, slides | Month 6 |

# 6. Contracts you own

**C1 — `data/vocabulary.csv`**

```
sign_id,ar_eg,ar_msa,en,category,source,esl_verified,urgent,video_file,has_animation
S001,دكتور,طبيب,doctor,people,KArSL,no,no,S001.mp4,yes
S023,وجع في صدري,ألم في الصدر,chest pain,symptom,KArSL,no,yes,S023.mp4,yes
```

Rules: `sign_id` never changes once given; new signs get new IDs; deleted signs are marked, not removed; `NONE` is reserved for "not a sign".

**C2 — clips and metadata**

```
clip name:  S001_K01_07        (sign S001, signer K01 from KArSL, take 07)
metadata.csv:
clip_id,sign_id,signer_id,take,source,dominant_hand,fps,frames,quality_flag,split_group
S001_K01_07,S001,K01,7,KArSL,right,30,84,ok,K01
```

Signer IDs: `K01–K03` for KArSL, `E01…` for Egyptian datasets, `U…` for approved contributors. No real names anywhere.

**Splits:** `splits/loso_fold_K01.json` = `{"train": [...clip_ids], "val": [...], "test": [...]}`; the test signer never appears in train or val.

# 7. Tools and technologies

| Purpose | Tools |
|---|---|
| Scripting | Python, pandas, NumPy |
| Video handling | FFmpeg, OpenCV |
| Data download | Kaggle API (`kaggle datasets download`) |
| Versioning | Git + Git LFS or DVC for large files; or a shared drive with a version log |
| Review page | Firebase (Firestore, Storage, Hosting) + plain HTML/JS |
| Evaluation | scikit-learn metrics, Google Forms for SUS |
| Documents | Markdown in `docs/` |

# 8. Step-by-step work plan

**Weeks 1–2 (feasibility spike)**

1. Download a small sample of KArSL. Confirm the exact format (video, frames, skeleton), resolution, fps.
2. Read the licence on Kaggle and the original KArSL terms. Write the answer in `docs/decisions.md`.
3. Export the full list of 502 KArSL signs and mark which fit the clinic domain. Report the count to the team.
4. Agree contracts C1 and C2 with the team and freeze them.

**Month 1**

1. Finalize the first 50 signs with the team; build `vocabulary.csv` v1.
2. Download the selected signs, rename clips, build `metadata.csv`.
3. Build the LOSO splits and the demo set.
4. Write `data_card.md` and the first `evaluation_plan.md`.
5. Contact Deaf associations / schools and an Egyptian interpreter.

**Month 2**

1. Write `dataset_adapter.py` and test it on one Egyptian dataset (e.g. AAST).
2. Write `egyptian_datasets_review.md`.
3. Clean data using CV's quality flags; record removed clips and why.
4. Collect the first baseline numbers from ML into `results.md`.

**Month 3**

1. Extend vocabulary to ~100 signs (`v2`); update metadata and splits.
2. Prepare the 200 / all-sign subset for the vocabulary-size experiment.
3. Start the interpreter review of `esl_verified`.

**Month 4**

1. Design the My Signs review flow and data model with Mobile.
2. Prepare user study materials: consent form, tasks, SUS form, observer sheet.
3. Book sessions with the association / school.

**Month 5**

1. Build the review page; run a test review cycle end to end.
2. Run the user studies; compute task success, time, corrections, SUS.
3. Merge approved contributions; run the adapter for any Egyptian data obtained.

**Month 6**

1. Freeze data versions; finalize `results.md` and the data/evaluation chapters of the report.
2. Prepare result charts for the slides.

# 9. Your priorities

| Priority | Items |
|---|---|
| Must | vocabulary.csv, organized clips + metadata, LOSO splits, evaluation plan, results table |
| Should | dataset_adapter.py, Egyptian datasets review, My Signs review flow, user studies with Deaf users |
| Could | 200-sign experiment subset, interpreter review of all signs |

# 10. Definition of done

- Any team member can train a model from your data **without asking you a question**.
- Any new dataset joins with **one command** of `dataset_adapter.py`.
- No test signer ever appears in training data (checked by a script).
- Every number in the report can be traced to a data version, a split, and a config.

# 11. Who you work with

| Role | What you exchange | Sync point |
|---|---|---|
| Computer Vision (2) | You give clips; they return landmarks and quality flags | Weekly in month 1–2 |
| Machine Learning (3) | You give splits; they give results | Every experiment |
| Mobile (4) | My Signs submission format and review flow | Month 4–5 |
| Speech & NLP (5) | Vocabulary words in Egyptian Arabic; phrases use sign IDs | Month 1, 3 |
| 3D Avatar (6) | Best take per sign for animation | Month 1–2 |

# 12. Pitfalls to avoid

- **Signer leakage:** a clip of the test signer in training makes results look great and false.
- **Changing sign IDs** after others have used them breaks models and phrase tables.
- **Using the whole KArSL** "just in case": huge downloads, slow work. Take only what you need.
- **Ignoring the licence:** check before showing any KArSL clip in the app.
- **Waiting for Deaf partners until month 5:** contact them now.

# 13. Working with an AI tool

Paste document 00 and this document, then use a prompt like:

```
I am the Data & Evaluation Engineer on a two-way Egyptian Sign Language
translation app (details in the attached documents). Contracts C1 (vocabulary.csv)
and C2 (clips + metadata.csv) define my outputs. Write a Python script that
<task>, following those formats exactly. Do not change the column names.
```

Always check AI-written code against the contracts before committing.

# 14. Your report chapter

Data sources and licences, vocabulary selection, data cleaning, data card, LOSO protocol, the adapter, the Egyptian data review, the My Signs review process, user study design and results, and the final results summary.
