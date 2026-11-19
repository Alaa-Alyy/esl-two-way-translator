# cv/ — Computer Vision (role 2)

Turn video into clean features, exactly the same in Python and on the phone.

📄 Role document: [EN](../docs/pdf/en/02_Computer_Vision_Engineer.pdf) · [AR](../docs/pdf/ar/02_Computer_Vision_Engineer.pdf)

## Delivers

| Output | Contract | Used by |
|---|---|---|
| `landmarks/raw/{clip_id}.npz` | C3 | ML, Avatar |
| `features/{clip_id}.npy` + [`docs/feature_spec.md`](../docs/feature_spec.md) | C4 | ML, Mobile |
| `Normalizer.kt`, `SignSegmenter.kt`, `QualityChecker.kt` | C4 | Mobile |
| Golden test (Python vs phone features) | C4 | CI |
| Synthetic sentence tool, smoothing / trimming tools | — | ML, Avatar |

## Receives

Clips + metadata + splits (C2) from Data; camera frames from Mobile.

## Layout

```
cv/
├── extract_landmarks.py     # MediaPipe Hand + Pose + Face → C3
├── normalize.py             # C3 → C4 (the reference implementation)
├── segment.py               # motion gate for finding signs in a stream
├── synthetic_sentences.py   # join isolated signs into sentence data
├── golden/                  # reference clips + expected features for the golden test
└── tests/
```

The Kotlin versions live in `android/` (core-vision module) and must match `normalize.py` number for number.

## First two weeks

1. Run Hand + Pose + Face together on a mid-range Android phone; measure fps.
2. Extract 10 KArSL clips and draw the landmarks on the video to check quality.
3. Write `docs/feature_spec.md` v1 with ML and Mobile.
