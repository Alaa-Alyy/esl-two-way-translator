# Contracts (C1–C11)

Contracts are the exact files and messages each role hands to the others. They let everyone work in parallel: build against the contract, use the example as a mock, and swap in the real thing when it arrives.

**Status:** draft v1. Frozen at the end of week 2 (see `docs/decisions.md`).

**Rule:** changing a contract needs agreement from every role that uses it, a version bump here, and a note in `docs/decisions.md`. CI checks that every example still matches its schema.

| ID | What | Owner (role) | Used by | Version | Spec |
|---|---|---|---|---|---|
| C1 | `data/vocabulary.csv` | 1 Data & Evaluation | everyone | 1 | [below](#c1--datavocabularycsv) |
| C2 | Clips + `data/metadata.csv` | 1 Data & Evaluation | 2, 3, 6 | 1 | [below](#c2--clips-and-metadata) |
| C3 | Raw landmarks `landmarks/raw/{clip_id}.npz` | 2 Computer Vision | 3, 6 | 1 | [below](#c3--raw-landmarks) |
| C4 | Features `features/{clip_id}.npy` + `docs/feature_spec.md` | 2 Computer Vision | 3, 4 | 1 | [below](#c4--features) |
| C5 | Model package `models/v{N}/` | 3 Machine Learning | 4 | 1 | [below](#c5--model-package) · [schemas](schemas/) |
| C6 | Recognition result | 4 Mobile App | 5 | 1 | [schema](schemas/C6_recognition_result.schema.json) · [example](examples/C6_recognition_result.json) |
| C7 | Sentence generation | 5 Speech & NLP | 4 | 1 | [schema](schemas/C7_sentence.schema.json) · [example](examples/C7_sentence.json) |
| C8 | Understanding result | 5 Speech & NLP | 4 | 1 | [schema](schemas/C8_understanding.schema.json) · [example](examples/C8_understanding.json) |
| C9 | Sign sequence for output | 5 Speech & NLP | 4, 6 | 1 | [schema](schemas/C9_sign_sequence.schema.json) · [example](examples/C9_sign_sequence.json) |
| C10 | Avatar animation + viewer API | 6 3D Avatar | 4 | 1 | [below](#c10--avatar) · [schema](schemas/C10_animation.schema.json) |
| C11 | My Signs submission | 4 Mobile App with 1 | 1, 3 | 1 | [schema](schemas/C11_my_signs_submission.schema.json) · [example](examples/C11_my_signs_submission.json) |

Check everything locally: `python scripts/validate_contracts.py`

---

## C1 — `data/vocabulary.csv`

UTF-8 CSV, one row per sign. `sign_id` never changes once given; deleted signs are marked, not removed; `NONE` is reserved for "not a sign".

| Column | Type | Example | Notes |
|---|---|---|---|
| `sign_id` | `S` + 3 digits | `S001` | Stable forever |
| `ar_eg` | text | `دكتور` | Egyptian Arabic, used in the app |
| `ar_msa` | text | `طبيب` | Modern Standard Arabic |
| `en` | text | `doctor` | English |
| `category` | one of `basics, people, places, appointments, time, symptoms, body, tests, payment, numbers, letters` | `people` | Used for context-aware vocabulary |
| `source` | `KArSL`, `EGY-<dataset>`, `MySigns` | `KArSL` | Where the clips come from |
| `esl_verified` | `yes` / `no` | `no` | Checked by an Egyptian interpreter |
| `urgent` | `yes` / `no` | `no` | Triggers the emergency alert |
| `video_file` | file name | `S001.mp4` | Reference video for the dictionary and fallback |
| `has_animation` | `yes` / `no` | `yes` | Avatar animation exists (C10) |

## C2 — clips and metadata

- Clip name: `SignID_SignerID_Take`, e.g. `S001_K01_07`. Signer IDs: `K01–K03` KArSL, `E01…` Egyptian datasets, `U…` approved contributors. No real names anywhere.
- `data/metadata.csv` columns: `clip_id, sign_id, signer_id, take, source, dominant_hand, fps, frames, quality_flag, split_group`
- `quality_flag`: `ok`, `cut`, `hands_out_of_frame`, `blurry`, `other`
- Splits: `data/splits/loso_fold_{signer_id}.json` = `{"train": [clip_ids], "val": [clip_ids], "test": [clip_ids]}`; the test signer never appears in train or val.

## C3 — raw landmarks

`landmarks/raw/{clip_id}.npz` (MediaPipe output, image-normalised coordinates):

| Array | Shape | Notes |
|---|---|---|
| `pose` | `(T, 33, 4)` | x, y, z, visibility |
| `left_hand` | `(T, 21, 3)` | zeros when not detected |
| `right_hand` | `(T, 21, 3)` | zeros when not detected |
| `face` | `(T, 40, 3)` | selected indices listed in `docs/feature_spec.md` |
| `blendshapes` | `(T, 52)` | MediaPipe face blendshapes |
| `mask_left`, `mask_right` | `(T,)` | 1 if the hand was detected |
| `fps` | scalar | |

## C4 — features

`features/{clip_id}.npy`, float32, shape `[48, F]`. The exact order and formula of every column, the MediaPipe version and `.task` model files are in `docs/feature_spec.md`, with a version number. The same logic must exist in `cv/normalize.py` and `Normalizer.kt`; the golden test checks they match (max absolute difference < 1e-3).

## C5 — model package

```
models/v{N}/sign_encoder.tflite   input [1, 48, F] float32 -> output [1, 128] float32, L2-normalised
models/v{N}/prototypes.json       {"S001": [[128 floats], ...], ..., "NONE": [[...]]}
models/v{N}/labels.json           ["S001", "S002", ...]   ordered sign_ids used in training
models/v{N}/thresholds.json       {"accept": 0.75, "ask": 0.45, "none_margin": 0.10}
models/v{N}/model_card.md         data version, feature spec version, LOSO results, date
```

Recognition rule (implemented by Mobile, specified by ML, reference in `ml/reference_recognizer.py`):

```
scores = cosine(embedding, every prototype of every allowed sign); best score per sign; sort
if best_1 is NONE or best_1 < ask:                  -> NONE (ignore)
elif best_1 >= accept and best_1 - best_2 >= margin -> accept best_1
else                                                -> "Did you mean?" top-3
```

## C10 — avatar

- `avatar/avatar.glb` (glTF binary)
- `avatar/animations/{sign_id}.json`: see [schema](schemas/C10_animation.schema.json)
- Viewer JavaScript API (used by the app through a WebView):

```javascript
playSequence({ signs: ["S046","S090"], sentenceType: "wh_question", fingerspell: [], speed: 1.0 })
stop()
setCamera("front" | "side")
// callbacks to Android: Android.onSignStart(index), Android.onFinished(), Android.onMissingAnimation(sign_id)
```
