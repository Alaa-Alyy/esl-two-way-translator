# ml/ — Machine Learning (role 3)

A sign model that works for anyone, not only for the people it was trained on.

📄 Role document: [EN](../docs/pdf/en/03_Machine_Learning_Engineer.pdf) · [AR](../docs/pdf/ar/03_Machine_Learning_Engineer.pdf)

## Delivers

| Output | Contract | Used by |
|---|---|---|
| `models/v{N}/` (encoder `.tflite`, prototypes, labels, thresholds, model card) | C5 | Mobile |
| `reference_recognizer.py` (the recognition rule in Python) | C5 | Mobile, tests |
| Experiment results (LOSO, known vs unseen signers) | — | Data, report |

## Receives

Features + feature spec (C4) and synthetic sentences from Computer Vision; splits and vocabulary (C1, C2) from Data; context groups from Speech & NLP.

## Layout

```
ml/
├── configs/                 # one YAML per experiment (data version, feature spec version, model)
├── train.py
├── evaluate.py              # Leave-One-Signer-Out only
├── export_tflite.py         # + quantization, accuracy before/after
├── reference_recognizer.py
├── models/                  # small exported packages only; large checkpoints stay out of git
└── tests/
```

Every reported number must be reproducible from a config + data version + feature spec version.

## First two weeks

1. Quick baseline on 20 signs; first LOSO number.
2. Choose PyTorch or TensorFlow by the easiest path to `.tflite`; give Mobile a dummy model with the right shapes.
3. Agree C5 with Mobile.
