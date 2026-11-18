<div class="cover" markdown="1">
<div class="kicker">ROLE DOCUMENT 03</div>
<div class="title">Machine Learning Engineer</div>
<div class="subtitle">A sign model that works for anyone, not only for the people it was trained on</div>
<div class="meta">
<div><b>Project:</b> Two-Way Egyptian Sign Language Translation App</div>
<div><b>Owner:</b> ______________________</div>
<div><b>Read with:</b> 00 — Project Master Document</div>
<div><b>Version:</b> 1.0 · November 2026</div>
</div>
</div>

# 1. Your role in one paragraph

You are **the brain of direction 1**. You receive clean features from Computer Vision and train the model that recognizes signs. Your main design is a **sign encoder** that turns each sign into an embedding ("fingerprint"); recognition compares it with stored prototypes. This one design gives the project recognition, rejection of non-signs, personal calibration, and the "My Signs" feature. You measure everything with Leave-One-Signer-Out evaluation and deliver a small, fast `.tflite` model for the phone.

# 2. The project in brief

A two-way Android app for one domain (clinic reception):

- **Direction 1:** a Deaf person signs a sentence → the app shows a natural Egyptian Arabic sentence and speaks it.
- **Direction 2:** a hearing person speaks Egyptian Arabic → the app shows the text and a 3D avatar signs the sentence smoothly.
- Recognition runs on the phone from MediaPipe landmarks. We start with **KArSL-502** (3 signers) and move to Egyptian data later; vocabulary 50 → ~100 signs.
- Users can add personal signs instantly and share them ("My Signs").

```
 Data (1) ──splits, vocabulary──> YOU (3)
 CV (2)   ──features [48,F], feature_spec, synthetic sentences──> YOU (3)
 YOU (3)  ──sign_encoder.tflite, prototypes.json, labels.json, thresholds.json──> Mobile (4)
 YOU (3)  ──results──> Data (1)
```

# 3. Your responsibilities

**Baselines**

- Random Forest / SVM on flattened features to check the data is sound (week 2).
- Simple GRU classifier as the first deep baseline.

**Sign encoder (main model)**

- Compare small temporal architectures: 2-layer GRU, 1D-CNN/TCN, small Transformer encoder.
- Train with classification loss **plus** a metric-learning loss (e.g. ArcFace / supervised contrastive / prototypical) so embeddings of the same sign cluster together.
- Output a 128-dimensional L2-normalized embedding.
- Build `prototypes.json`: one or more prototype embeddings per sign (mean of training embeddings, optionally several per sign for variants).
- Recognition = cosine similarity to prototypes; confidence = calibrated similarity / margin between top-1 and top-2.

**NONE class (rejection)**

- Train with non-sign movements: transitions between signs, rest, scratching, adjusting clothes (generated from data gaps and synthetic negatives).
- Tune the rejection margin so random movements are rejected.

**Augmentation for unseen signers**

- Small rotation, shift, scale; speed change (time warping); joint noise; frame dropping; **body-proportion changes** (arm length, shoulder width, hand size).
- Measure the effect of each augmentation on LOSO.

**Evaluation**

- LOSO on all folds: accuracy, macro-F1, top-3, confusion matrix, per-sign scores, known vs unseen signers.
- Vocabulary-size experiment: 50 / 100 / 200 signs.
- Find confusable sign pairs and report them (useful for context-aware vocabulary and UI).

**Thresholds and confidence**

- Choose `accept` and `ask` thresholds: above `accept` → show the sign; between → "Did you mean?" with top 3; below `ask` → NONE.

**Continuous recognition (Should)**

- Train a CTC sequence model on synthetic sentences from CV's tool; compare with segment-then-recognize.

**Context-aware vocabulary (Should, with NLP 5 and Mobile 4)**

- Support restricting the candidate prototypes to a subset (e.g. body parts) at inference time; measure the accuracy gain.

**Personal calibration and My Signs (with Mobile 4)**

- Calibration: from 2–3 user repetitions, add user-specific prototypes (or adjust existing ones).
- My Signs: from 5 repetitions, compute a new prototype; consistency check (repetitions close to each other); conflict check (too close to an existing sign).
- Retraining script that merges approved shared signs (≥ 3 contributors) into the model.

**Export**

- Convert to LiteRT `.tflite`; float16 and int8 quantization; compare accuracy before/after; measure inference time with Mobile.
- Write `model_card.md` per version.

**Transfer learning (when Egyptian data arrives)**

- Pretrain on KArSL, fine-tune on Egyptian; compare with training from scratch; evaluate only on Egyptian signers.

# 4. Inputs you receive

| Input | From | Format | When |
|---|---|---|---|
| Features | CV (2) | C4 `[48, F]` float32 | Month 1 |
| `feature_spec.md` | CV (2) | Versioned spec | Week 2 |
| Raw landmarks (for augmentation in 3D) | CV (2) | C3 | Month 1 |
| Splits, vocabulary | Data (1) | `splits/`, C1 | Month 1 |
| Synthetic sentences | CV (2) | Sequences + labels | Month 3 |
| On-device timing | Mobile (4) | Report | Month 2+ |
| Context groups (which signs fit which question) | NLP (5) | JSON | Month 4 |

# 5. Outputs you deliver

| Output | Format | Used by | Due |
|---|---|---|---|
| Baseline results | Table in `results.md` | Data, team | Week 2 / Month 2 |
| Dummy `.tflite` with correct input/output shapes | C5 | Mobile | Month 1 |
| `models/v{N}/` package (C5) | tflite + json + model card | Mobile | Month 2 (v1), Month 3, Month 4 |
| `ml/train.py`, `ml/evaluate.py`, configs | Code | Team | Ongoing |
| Calibration + My Signs logic spec | Doc + reference Python | Mobile | Month 4 |
| `ml/retrain_with_contributions.py` | Script | Data | Month 5 |
| `docs/ml_report.md` | All experiments | Report | Month 5 |

# 6. Contracts you own

**C5 — model package**

```
models/v{N}/sign_encoder.tflite   input  [1, 48, F] float32  (F from feature_spec v<k>)
                                  output [1, 128] float32, L2-normalized
models/v{N}/prototypes.json       {"S001": [[128 floats], ...], ..., "NONE": [[...]]}
models/v{N}/labels.json           ["S001", "S002", ...]
models/v{N}/thresholds.json       {"accept": 0.75, "ask": 0.45, "none_margin": 0.10}
models/v{N}/model_card.md         data version, feature spec version, LOSO results, date
```

**Recognition rule (implemented by Mobile, specified by you)**

```
scores = cosine(embedding, every prototype of every allowed sign)
best   = max score per sign; sort
if best_1 is NONE or best_1 < ask:                 -> NONE (ignore)
elif best_1 >= accept and best_1 - best_2 >= margin -> accept best_1
else                                                -> "Did you mean?" top-3
```

Provide a reference implementation in Python (`ml/reference_recognizer.py`) so Mobile can test against it.

# 7. Tools and technologies

| Purpose | Tools |
|---|---|
| Framework | PyTorch (export via ONNX → LiteRT, or ai-edge-torch) or TensorFlow/Keras (direct LiteRT) — choose in week 1 based on the easiest export path |
| Classic ML | scikit-learn |
| Tracking | Weights & Biases or TensorBoard |
| Compute | Kaggle / Colab GPUs |
| Metrics | scikit-learn, NumPy, matplotlib |
| Export | LiteRT converter, quantization tools |

Recommendation: if nobody on the team has strong PyTorch-to-mobile experience, **TensorFlow/Keras gives the shortest path to `.tflite`**.

# 8. Step-by-step work plan

**Weeks 1–2 (feasibility spike)**

1. Quick baseline on 20 signs with whatever features exist (even raw landmarks): LOSO result.
2. Choose the framework based on export path; export a dummy model and give it to Mobile.
3. Agree C5 with Mobile.

**Month 1**

1. Baselines (RF/SVM, GRU) on the 50 signs; first LOSO numbers.
2. Training/evaluation code with configs and experiment tracking.

**Month 2**

1. Sign encoder v1 with metric learning; prototypes; thresholds.
2. Model package v1 to Mobile; check reference recognizer vs phone results.

**Month 3**

1. Augmentation study; NONE class; architecture comparison.
2. Vocabulary → ~100 signs; model v2.
3. Start CTC model on synthetic sentences (Should).

**Month 4**

1. Calibration and My Signs logic with Mobile.
2. Context-aware restriction with NLP; measure the gain.
3. Quantization; model v3 for the complete product.

**Month 5**

1. Vocabulary-size experiment (50/100/200); confusable pairs; final LOSO.
2. Retraining script for approved contributions.
3. Transfer learning experiment if Egyptian data exists.

**Month 6**

1. Freeze the final model; write the ML chapter.

# 9. Your priorities

| Priority | Items |
|---|---|
| Must | Baseline, sign encoder + prototypes, NONE, thresholds, LOSO evaluation, tflite export |
| Should | Augmentation study, CTC on synthetic sentences, context-aware restriction, My Signs logic |
| Could | Calibration, vocabulary-size curve, transfer learning experiment |

# 10. Definition of done

- The model runs on the phone and gives the same predictions as the Python reference.
- LOSO results (known vs unseen signers) are reported for the final model.
- Random non-sign movements are rejected in a live test.
- Every result can be reproduced from a config, a data version, and a feature-spec version.

# 11. Who you work with

| Role | What you exchange | Sync point |
|---|---|---|
| CV (2) | Features, spec, synthetic sentences | Weekly |
| Data (1) | Splits in, results out | Every experiment |
| Mobile (4) | Model package, recognizer rule, timing | Every model version |
| NLP (5) | Context groups; recognized sign sequences | Month 4 |

# 12. Pitfalls to avoid

- **Reporting training or random-split accuracy** as the result. Only LOSO counts.
- **Too big a model** for the data: with 3 signers, small models generalize better.
- **Flipping left/right as augmentation** without checking: some signs change meaning. Prefer CV's dominant-hand mirroring.
- **Changing input shape** without updating C5 and telling Mobile.
- **Quantization accuracy drop** not measured.

# 13. Working with an AI tool

```
I am the Machine Learning Engineer on a two-way Egyptian Sign Language app
(see attached documents). Input features are [48, F] float32 (contract C4).
The model package must follow contract C5: an encoder producing a 128-d
L2-normalized embedding, with prototypes and thresholds. Evaluation is
Leave-One-Signer-Out only. Write <task>.
```

# 14. Your report chapter

Model design (encoder + prototypes), loss functions, NONE class, augmentation, LOSO results, known vs unseen signers, vocabulary-size curve, confusions, sequence model, calibration and My Signs, quantization and on-device performance.
