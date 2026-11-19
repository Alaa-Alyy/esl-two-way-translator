# Feature spec (contract C4)

**Version:** 0 (draft — to be completed by Computer Vision with ML and Mobile in week 2)
**Owner:** role 2, Computer Vision

This file is the single source of truth for the numbers the model sees. `cv/normalize.py` and `Normalizer.kt` must follow it exactly, and the golden test checks they agree (max absolute difference < 1e-3). **Any change → bump the version, tell ML and Mobile, add an entry in `docs/decisions.md`.**

## 1. Source

| Item | Value |
|---|---|
| MediaPipe version | _TBD (same in Python and Android)_ |
| Hand model file | _`hand_landmarker.task`, version TBD_ |
| Pose model file | _`pose_landmarker_*.task`, version TBD_ |
| Face model file | _`face_landmarker.task`, version TBD_ |
| Coordinates | _image-normalised or world — choose one_ |
| Front-camera mirroring | _how it is handled_ |

## 2. Points kept per frame

| Group | Indices | Count |
|---|---|---|
| Pose (upper body) | _e.g. 0–24_ | _TBD_ |
| Left hand | 0–20 | 21 |
| Right hand | 0–20 | 21 |
| Face | _list the ~40 indices: eyebrows, eyes, mouth_ | _TBD_ |

## 3. Normalisation

1. Origin: midpoint of the shoulders (pose 11, 12).
2. Scale: divide by shoulder width; guard against width ≈ 0.
3. Hands also stored relative to their wrist.
4. Left-handed signers mirrored so the dominant hand is always on the same side.
5. Missing hands: interpolate gaps ≤ 5 frames; otherwise zeros + presence flag.

## 4. Time

- Resample each sign to **48 frames**.
- Add velocity (frame-to-frame differences).

## 5. Final vector

| Columns | Content |
|---|---|
| _0 … n_ | _list every block in order_ |

**F = _TBD_**
