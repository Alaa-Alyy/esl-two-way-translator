# data-pipeline/ — Data & Evaluation (role 1)

Clean, versioned data that any new dataset can join in one step, and honest numbers for the report.

📄 Role document: [EN](../docs/pdf/en/01_Data_and_Evaluation_Engineer.pdf) · [AR](../docs/pdf/ar/01_Data_and_Evaluation_Engineer.pdf)

## Delivers

| Output | Contract | Used by |
|---|---|---|
| `data/vocabulary.csv` | C1 | everyone |
| Organised clips + `data/metadata.csv` | C2 | Computer Vision, ML, Avatar |
| `data/splits/loso_fold_{signer}.json` + demo set | C2 | ML, Computer Vision |
| `dataset_adapter.py` (any dataset → our format) | C2 | everyone |
| `docs/data_card.md`, `docs/evaluation_plan.md`, `docs/results.md` | — | report |

## Receives

KArSL-502 (Kaggle mirror `yousefdotpy/karsl-502` and the original source), Egyptian datasets, quality flags from Computer Vision, My Signs submissions (C11) from Mobile.

## Layout

```
data-pipeline/
├── download_karsl.py        # only the selected signs
├── organise_clips.py        # rename to SignID_SignerID_Take, build metadata.csv
├── make_splits.py           # Leave-One-Signer-Out folds + demo set
├── dataset_adapter.py       # import any external dataset
└── tests/
```

Large files (videos, frames) are **not** committed; see [`../data/README.md`](../data/README.md).

## First two weeks

1. Download a small KArSL sample; confirm format, resolution, fps.
2. Read the licence (Kaggle + original KArSL terms); record the answer in `docs/decisions.md`.
3. List the 502 signs and mark the ones that fit clinic reception; report the count.
4. Agree C1 and C2 with the team.
