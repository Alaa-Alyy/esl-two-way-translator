# Project context for AI coding tools

Read this first. It is short on purpose; the full picture is in `docs/en/00_Project_Master_Document.md`.

## What we are building

A two-way **Egyptian Sign Language** translator for Android, for one domain first (clinic reception):
- **Sign → speech:** camera → MediaPipe landmarks → sign encoder (`.tflite`, on the phone) → Egyptian Arabic sentence → voice.
- **Speech → sign:** Egyptian Arabic speech → intent + entities → sign sequence in sign-language order → 3D avatar signs it smoothly.

Graduation project, six people, equal roles, about 6 months. Data starts with **KArSL-502** (Unified Arabic Sign Language, 3 signers); Egyptian data comes later.

## Repo map

| Folder | Role | Role doc |
|---|---|---|
| `data-pipeline/`, `data/` | 1 Data & Evaluation | `docs/en/01_*` |
| `cv/` | 2 Computer Vision | `docs/en/02_*` |
| `ml/` | 3 Machine Learning | `docs/en/03_*` |
| `android/` | 4 Mobile App | `docs/en/04_*` |
| `nlp/` | 5 Speech & NLP | `docs/en/05_*` |
| `avatar/` | 6 3D Avatar | `docs/en/06_*` |
| `docs/contracts/` | everyone | contracts C1–C11 |

## Rules that matter

1. **Contracts are law.** The files and messages between roles are defined in `docs/contracts/` (C1–C11, with JSON Schemas). Do not rename fields, IDs or shapes. A change needs the other roles' agreement, a version bump and an entry in `docs/decisions.md`. Run `python scripts/validate_contracts.py`.
2. **No hard-coded signs.** Everything comes from `data/vocabulary.csv` and the model package.
3. **Train/serve parity.** Features follow `docs/feature_spec.md` exactly, in Python and Kotlin. The golden test must pass.
4. **Only Leave-One-Signer-Out numbers** go in the report.
5. **Egyptian Arabic** on the hearing side (`ar-EG`), and sentence-level translation, never word-for-word.
6. **Never commit** videos, `.npy`/`.npz` data, model checkpoints, `.env`, keys or real names.
7. **No fake results.** No invented data, placeholder outputs presented as real, or silent fallbacks. If something is missing, fail clearly.
8. Small pull requests, reviewed by someone from a different role. `main` always runs.

## Where things are decided

- `docs/decisions.md` — every decision and why
- `docs/contracts/README.md` — C1–C11
- `docs/feature_spec.md` — C4 details
