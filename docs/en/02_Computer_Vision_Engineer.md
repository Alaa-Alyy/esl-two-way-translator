<div class="cover" markdown="1">
<div class="kicker">ROLE DOCUMENT 02</div>
<div class="title">Computer Vision Engineer</div>
<div class="subtitle">Turn video into clean features, exactly the same in Python and on the phone</div>
<div class="meta">
<div><b>Project:</b> Two-Way Egyptian Sign Language Translation App</div>
<div><b>Owner:</b> ______________________</div>
<div><b>Read with:</b> 00 — Project Master Document</div>
<div><b>Version:</b> 1.0 · November 2026</div>
</div>
</div>

# 1. Your role in one paragraph

You are **the eyes of the system**. You take video frames and turn them into clean, normalized numbers that describe the body, hands, and face over time. You do this twice: in Python for training, and in Kotlin on the phone for live use, and you prove that both give the same result. You also find where each sign starts and ends in a live stream, check image quality, and help the avatar and sentence work with your landmark tools.

# 2. The project in brief

A two-way Android app for one domain (clinic reception):

- **Direction 1:** a Deaf person signs a sentence → the app shows a natural Egyptian Arabic sentence and speaks it.
- **Direction 2:** a hearing person speaks Egyptian Arabic → the app shows the text and a 3D avatar signs the sentence smoothly.
- The system is **vision-based and pose-driven**: MediaPipe models find keypoints, then a temporal model recognizes the sign.
- We start with **KArSL-502** (3 signers) and move to Egyptian data later; vocabulary 50 → ~100 signs.

```
 Data (1) ──clips──> YOU (2) ──landmarks/raw, features/, feature_spec.md──> ML (3)
                     YOU (2) ──Normalizer.kt, SignSegmenter.kt, QualityChecker.kt──> Mobile (4)
                     YOU (2) ──clean landmarks of best takes, smoothing tools──> Avatar (6)
 Mobile (4) ──camera frames──> YOUR on-device pipeline
```

# 3. Your responsibilities

**Landmark extraction (Python)**

- Run MediaPipe Tasks **Hand Landmarker, Pose Landmarker, and Face Landmarker** on every clip (video mode, timestamps).
- Store raw outputs per clip (contract C3), including 52 face blendshapes.
- Choose the kept points: upper-body pose, 21 points per hand, about 40 face points (eyebrows, eyes, mouth).
- Report per-clip statistics: hand detection rate, missing frames → quality flags for Data (1).
- Batch extraction that runs on Kaggle/Colab and can be resumed.

**Feature engineering**

- Normalization: origin at the shoulder midpoint, scale by shoulder width; hand points also relative to the wrist; mirror left-handed signers.
- Missing hands: interpolate short gaps (≤ 5 frames); otherwise zeros + presence flag.
- Resample each sign to 48 frames; add velocity (frame differences).
- Write `feature_spec.md`: the exact order of every number, its formula, and a version number.

**On-device vision (Kotlin)**

- Run MediaPipe Tasks on Android in live-stream mode on camera frames from Mobile (4).
- Port normalization to `Normalizer.kt` **line by line** from `normalize.py`.
- **Golden test:** for 20 reference clips, Python features and Kotlin features must match (max absolute difference below 1e-3). Add it to CI.
- Measure fps on a mid-range phone; if too slow, run face every N frames or lower resolution.

**Segmentation**

- `SignSegmenter.kt`: motion gate based on wrist position and speed — start when hands leave the rest zone, end when they return.
- Inside sentences: split at short holds / velocity minima.
- Sliding-window fallback for signers who do not pause.
- Tune thresholds on KArSL clips joined together and on live tests.

**Quality checker and framing guide**

- `QualityChecker.kt`: brightness, blur, person in frame, distance (shoulder width in pixels), hands visible.
- Return simple messages for the UI: `MOVE_CLOSER`, `MOVE_BACK`, `MORE_LIGHT`, `HANDS_NOT_VISIBLE`, `OK`.

**Support for other roles**

- **Synthetic sentences (with ML 3):** a tool that joins isolated sign landmark sequences with smooth transitions to create sentence training data.
- **Avatar (with 6):** smoothing filters (e.g. One Euro filter), core-segment trimming (remove rest pose at start and end), best-take selection per sign.

**Pixel baseline (Could)**

- A small CNN (or CNN + GRU) on frames, evaluated with the same LOSO splits, to compare against landmarks.

# 4. Inputs you receive

| Input | From | Format | When |
|---|---|---|---|
| Organized clips + metadata | Data (1) | C2 | Month 1 |
| LOSO splits | Data (1) | `splits/*.json` | Month 1 |
| Camera frames on the phone | Mobile (4) | CameraX `ImageProxy` | Month 1–2 |
| Feature needs (e.g. extra features) | ML (3) | Issue / discussion | Ongoing |
| Animation needs | Avatar (6) | Issue / discussion | Month 1–3 |

# 5. Outputs you deliver

| Output | Format | Used by | Due |
|---|---|---|---|
| `cv/extract_landmarks.py` | Python script | You, Data | Month 1 |
| `landmarks/raw/{clip_id}.npz` (C3) | NumPy archives | ML, Avatar | Month 1 |
| `cv/normalize.py` + `features/{clip_id}.npy` (C4) | Python + `[48, F]` float32 | ML | Month 1 |
| `docs/feature_spec.md` | Versioned spec | ML, Mobile | Week 2 |
| Quality flags | CSV for Data | Data | Month 1 |
| `Normalizer.kt` + MediaPipe Android wrapper | Kotlin module | Mobile | Month 2 |
| Golden test + CI job | Test script + reference files | Everyone | Month 2 |
| `SignSegmenter.kt` | Kotlin module | Mobile | Month 3 |
| `QualityChecker.kt` | Kotlin module | Mobile | Month 3 |
| `cv/synthetic_sentences.py` | Python tool | ML | Month 3 |
| Smoothing + trimming tools | Python | Avatar | Month 2 |
| `docs/cv_report.md` | fps, golden test, segmentation accuracy, pixel vs landmarks | Report | Month 5 |

# 6. Contracts you own

**C3 — raw landmarks:** `landmarks/raw/{clip_id}.npz`

```
pose        (T, 33, 4)  x, y, z, visibility   (normalized image coords from MediaPipe)
left_hand   (T, 21, 3)
right_hand  (T, 21, 3)
face        (T, 40, 3)  selected indices listed in feature_spec.md
blendshapes (T, 52)
mask_left   (T,)  1 if detected
mask_right  (T,)
fps         scalar
```

**C4 — features:** `features/{clip_id}.npy`, float32, shape `[48, F]`. `feature_spec.md` must list for each column: source point, axis, transformation, and the spec version. Any change → new version + tell ML and Mobile.

**On-device API (agreed with Mobile)**

```kotlin
interface VisionPipeline {
    fun process(frame: ImageProxy, timestampMs: Long): FrameLandmarks
}
object Normalizer { fun toFeatures(window: List<FrameLandmarks>): FloatArray /* 48*F */ }
class SignSegmenter { fun push(f: FrameLandmarks): SegmentEvent? /* START, END(segment) */ }
object QualityChecker { fun check(frame: ImageProxy, f: FrameLandmarks): QualityStatus }
```

# 7. Tools and technologies

| Purpose | Tools |
|---|---|
| Landmarks | MediaPipe Tasks (Python and Android), same model versions on both |
| Images/video | OpenCV, FFmpeg |
| Math | NumPy, SciPy (interpolation, filters) |
| Android | Kotlin, Android Studio, MediaPipe Tasks Vision for Android |
| Compute | Kaggle / Colab for batch extraction |
| Testing | pytest, JUnit, GitHub Actions |
| Pixel baseline | PyTorch or TensorFlow |

**Important:** write down the exact MediaPipe version and `.task` model files in `feature_spec.md`; both Python and Android must use the same ones.

# 8. Step-by-step work plan

**Weeks 1–2 (feasibility spike)**

1. Run Hand + Pose + Face together on a mid-range Android phone; measure fps. Report it.
2. Run extraction on 10 KArSL clips; visualize landmarks over the video to check quality.
3. Draft `feature_spec.md` v1 and agree it with ML and Mobile.

**Month 1**

1. Batch extraction for the 50 signs; produce C3 files and quality flags.
2. `normalize.py` and C4 features; share with ML.
3. Help Mobile show live landmarks on the camera preview (milestone).

**Month 2**

1. `Normalizer.kt` + MediaPipe Android wrapper.
2. Golden test on 20 clips; add to CI.
3. Smoothing and trimming tools for Avatar.

**Month 3**

1. `SignSegmenter.kt`, tuned on joined KArSL clips and live signing.
2. `QualityChecker.kt` and framing messages.
3. `synthetic_sentences.py` with ML.
4. Extraction for the extended ~100-sign vocabulary.

**Month 4**

1. Performance tuning on the phone (fps, latency, memory).
2. Support integration of both directions.

**Month 5**

1. Pixel baseline and comparison (Could).
2. Segmentation accuracy measurement; `cv_report.md`.

**Month 6**

1. Freeze; write the vision chapter.

# 9. Your priorities

| Priority | Items |
|---|---|
| Must | Extraction, normalization, feature spec, Kotlin port, golden test, segmentation |
| Should | Synthetic sentence tool, smoothing/trimming tools for Avatar, quality checker |
| Could | Pixel baseline comparison |

# 10. Definition of done

- Python and phone features match on the golden test (in CI, green).
- The phone produces features live at a usable rate (target ≥ 15 fps processing) on a mid-range device.
- The segmenter correctly cuts signs in joined sequences and live tests (accuracy reported).
- `feature_spec.md` is complete enough that someone else could re-implement it.

# 11. Who you work with

| Role | What you exchange | Sync point |
|---|---|---|
| Data (1) | Clips in, quality flags out | Month 1 |
| ML (3) | Features, feature spec, synthetic sentences | Weekly |
| Mobile (4) | Kotlin modules, camera frames, performance | Weekly from month 2 |
| Avatar (6) | Clean landmarks, smoothing, trimming | Months 1–3 (you help them most in months 1–3) |

# 12. Pitfalls to avoid

- **Train/serve skew:** different MediaPipe versions, image orientation, or mirroring between Python and the phone. The front camera is mirrored — decide and document how you handle it.
- **Image vs world coordinates:** use one kind consistently; document it.
- **Changing features without a version bump** silently breaks ML's models.
- **Normalizing by a shoulder width of zero** (person partly out of frame) → guard against division by zero.
- **Assuming left/right labels from MediaPipe** are the signer's left/right: check with the camera mirroring.

# 13. Working with an AI tool

```
I am the Computer Vision Engineer on a two-way Egyptian Sign Language app
(see attached documents). Raw landmarks follow contract C3 and features follow
contract C4 / feature_spec.md v<N>. Write <task>. The Python and Kotlin versions
must produce identical numbers; keep the exact feature order from the spec.
```

# 14. Your report chapter

Why landmarks, MediaPipe setup, feature design and normalization, train/serve parity and the golden test, segmentation, quality checking, on-device performance, and the pixel vs landmarks comparison.
