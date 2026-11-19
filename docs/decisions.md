# Decision log

Every important decision: what, when, why. Newest at the bottom. A contract change always gets an entry here.

Format: `D-NNN · YYYY-MM-DD · decision` — then *Why* and *Consequences*.

---

### D-001 · 2026-11-18 · One domain first: clinic reception
**Why:** a small, real vocabulary lets us reach high accuracy and test with real users.
**Consequences:** other domains are future work; the vocabulary is chosen for the clinic.

### D-002 · 2026-11-18 · Start with KArSL-502, move to Egyptian data later
**Why:** no Egyptian dataset of usable size is available now; KArSL lets us build and test the whole pipeline.
**Consequences:** signs are Unified Arabic Sign Language for now. `esl_verified` in C1 tracks what an Egyptian interpreter confirmed. `dataset_adapter.py` must make Egyptian data a one-command import.

### D-003 · 2026-11-18 · Landmarks, not raw pixels
**Why:** ignore background, clothes, light and skin tone; need far less data; fast on phones; private.
**Consequences:** MediaPipe Hand + Pose + Face; a pixel baseline is trained only for comparison.

### D-004 · 2026-11-18 · Evaluate with Leave-One-Signer-Out only
**Why:** accuracy on people seen in training says nothing about real users.
**Consequences:** only LOSO numbers go in the report; the known-vs-unseen gap is reported.

### D-005 · 2026-11-18 · Sign encoder + prototypes, not a fixed classifier
**Why:** one design gives recognition, NONE rejection, personal calibration and My Signs without retraining.
**Consequences:** C5 is an embedding model plus `prototypes.json`.

### D-006 · 2026-11-18 · The 3D avatar is the main output of speech → sign
**Why:** clips played one after another look broken for sentences, and many Deaf users cannot read Arabic well.
**Consequences:** recorded videos are only the fallback; the avatar spike in weeks 1–2 is the highest-risk check.

### D-007 · 2026-11-18 · Vocabulary grows 50 → ~100 signs; 200 only as an experiment
**Why:** accuracy on unseen signers drops as classes grow; context-aware vocabulary keeps it high.
**Consequences:** the report includes an accuracy-vs-vocabulary-size curve.

### D-008 · 2026-11-19 · Monorepo with one folder per role and written contracts C1–C11
**Why:** six people work in parallel; contracts and mocks remove waiting.
**Consequences:** contracts are frozen at the end of week 2; changes need the users' agreement, a version bump and an entry here. CI validates contract examples.

### D-009 · 2026-11-19 · Check free-tier limits before building on any external service
**Why:** in a previous project, free AI quotas turned out smaller and less reliable than advertised.
**Consequences:** every external service gets a real test of its limits in the week 1–2 spikes, and a backup is chosen before we depend on it.

### D-010 · 2026-11-19 · Process KArSL inside Kaggle notebooks; extract our own landmarks
**Why:** the Kaggle mirror is 25.5 GB of frames; third-party keypoint sets use unknown extraction settings, which would break train/serve parity.
**Consequences:** landmark extraction (role 2) runs in a Kaggle notebook with the dataset attached; only C3 `.npz` files leave Kaggle. Details in `docs/karsl_review.md`.

### D-011 · 2026-11-19 · Verify every sign label against the official KArSL file
**Why:** the third-party label file has translation mistakes (e.g. #502 "appointment" = job appointment, #395 "Before" = Imam).
**Consequences:** `data/karsl/clinic_candidates.csv` is a draft until checked against `KARSL-502_Labels.xlsx`; missing clinic words are listed as Egyptian-data targets.

---

## Open decisions (to settle in weeks 1–2)

- [ ] KArSL licence: does it allow our academic use and showing clips in the app? (role 1)
- [ ] PyTorch or TensorFlow, by the easiest path to `.tflite` (role 3)
- [ ] Avatar renderer: three.js WebView, SceneView, or Unity (roles 4 + 6)
- [ ] Final list of the first 50 signs (everyone)
