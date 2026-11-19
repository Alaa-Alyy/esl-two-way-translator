# android/ — Mobile App (role 4)

One fast, simple app that joins every part, usable even by people who cannot read.

📄 Role document: [EN](../docs/pdf/en/04_Mobile_App_Engineer.pdf) · [AR](../docs/pdf/ar/04_Mobile_App_Engineer.pdf)

## Delivers

| Output | Contract | Used by |
|---|---|---|
| The Android app (both directions, conversation mode, My Signs) | — | everyone |
| Recognition result | C6 | Speech & NLP |
| My Signs submission | C11 | Data, ML |
| `docs/performance_report.md` (latency, fps, memory, battery) | — | report |

## Receives

Vision modules (C4) from Computer Vision, model package (C5) from ML, language engine + audio (C7–C9) from Speech & NLP, avatar viewer (C10) from Avatar, vocabulary (C1) from Data.

## Layout (Kotlin + Jetpack Compose)

```
android/
├── app/              # screens, navigation
├── core-vision/      # CameraX + MediaPipe + Normalizer.kt (from Computer Vision)
├── core-model/       # LiteRT + recognizer + prototypes
├── core-language/    # Speech & NLP engine wrapper
├── core-avatar/      # WebView + three.js viewer assets
└── core-data/        # Room, vocabulary loader, Firebase sync
```

Rule: no sign is hard-coded; everything loads from `vocabulary.csv` and the model package.

## First two weeks

1. One test app with CameraX + MediaPipe + a three.js WebView running together; measure fps.
2. Load a dummy `.tflite` from ML and run it.
3. Agree the C5–C11 interfaces.
