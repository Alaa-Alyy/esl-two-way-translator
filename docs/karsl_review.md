# KArSL-502 review (week 1 spike, role 1)

**Date:** 2026-11-19 · **Status:** first pass, to be confirmed with the official label file and the author

## 1. What it is

| | |
|---|---|
| Content | 502 isolated signs, **3 professional signers**, 50 repetitions each = 75,300 samples |
| Sign language | Unified Arabic Sign Language (recorded in Saudi Arabia), **not Egyptian** |
| Capture | Microsoft Kinect V2: RGB, depth and skeleton |
| Official site | https://hamzah-luqman.github.io/KArSL/ (raw videos and frames on Google Drive) |
| Paper (must be cited) | Sidig, Luqman, Mahmoud, Mohandes. *KArSL: Arabic Sign Language Database.* ACM TALLIP 20(1), 2021 |

## 2. The Kaggle mirror we checked: `yousefdotpy/karsl-502`

- **25.5 GB**, RGB **frames only** (JPG, 256×256, cropped and resized), no video, depth or skeleton.
- Path: `{signer}/{signer}/{train|test}/{sign_id 0001-0502}/{clip}/{clip}_{frame}.jpg`; the author of KArSL (`hluqman`) is a collaborator on this mirror.
- Frames look clean: seated signer, upper body + face + both hands visible, plain green background. Good for MediaPipe; 256 px is small, so hand detection on fast movement must be tested.

Other KArSL versions on Kaggle (made by third parties): MediaPipe keypoints (44 MB – 963 MB), `.pose` files (18.9 GB). Their extraction settings are unknown, so we **do not** use them for training: our features must come from our own pipeline to match the phone (train/serve parity, `docs/feature_spec.md`).

## 3. Licence and terms: NOT settled

- Kaggle mirror: licence **"unknown"**.
- Official site: no licence; only "available for researchers" and a request to cite the paper.
- Open: is academic use free, may we **show KArSL clips inside the app**, may we share derived landmarks?
- **Action:** email the author, Dr. Hamzah Luqman (hluqman@kfupm.edu.sa), describing the graduation project and asking these three questions. Record the answer in `docs/decisions.md`.

Until then: use KArSL for training and evaluation only; plan the app's reference videos and avatar motion so they can be replaced if display is not allowed.

## 4. Coverage for clinic reception: good

The 502 signs come from 11 chapters of the Unified Arabic dictionary. One of them is **Health (signs 71–159, 89 signs)**, which fits our domain directly. Useful signs also exist in the other chapters: `doctor`, `nurse`, `pharmacist`, `hospital`, `pharmacy`, `Sign language translator`, greetings, numbers, directions and feelings.

Files in this repo:
- [`data/karsl/karsl_502_signs.csv`](../data/karsl/karsl_502_signs.csv): all 502 signs with Arabic, English and chapter.
- [`data/karsl/clinic_candidates.csv`](../data/karsl/clinic_candidates.csv): **112 candidates**, tier 1 = **54** (the first set), tier 2 = 58 (growing to ~100).

| Category | Tier 1 examples |
|---|---|
| basics | welcome, greeting, thanks, here you are, help, call |
| people | doctor, nurse, pharmacist, sick/patient, sign language translator, child, baby |
| places | hospital, pharmacy, laboratory |
| symptoms | pain, headache, fever, cold, diarrhea, constipation, colic, swelling, inflammation, allergy, itch, wound, burn, tired |
| body | chest, face, pharynx (throat), heart, backbone, lungs |
| tests & medicine | blood test, physical examination, X-ray, thermometer, blood pressure, pulse, medicine, capsule |
| numbers | 1–10 |

## 5. Problems found

1. **The third-party label file has translation mistakes.** Examples: #502 "appointment" is تعيين in the *Jobs* chapter (appointing someone to a job, not a clinic appointment); #395 "Before" is إمام in the *Religion* chapter (most likely "Imam"). Both were removed from the candidates.
   **Action:** get the official `KARSL-502_Labels.xlsx` from the author's Drive folder and check every candidate against it.
2. **Important clinic words are missing from KArSL:** yes, no, please, sorry, wait, understand, repeat, today, tomorrow, yesterday, hour, cough, vomiting, dizziness, stomach, eye, ear, tooth, hand, leg, prescription, price, pay, ID card, reception, a medical appointment, emergency.
   **Action:** list them in `vocabulary.csv` with `source=EGY-*` as the first targets for Egyptian data or My Signs; until then, the app covers them with quick buttons and fingerspelling.
3. **Only 3 signers:** LOSO trains on 2 and tests on 1, so the unseen-signer number will be modest. Expected and documented (D-004).
4. **Signers are seated;** app users may stand. Shoulder-based normalisation (C4) handles position and scale; worth checking in the live tests.

## 6. How to work with 25 GB

Do **not** download the whole dataset. Recommended:
- Run the landmark extraction (role 2) **inside a Kaggle notebook** with this dataset attached: no download, free CPU/GPU, and only the small `.npz` landmark files (C3) come out, for the selected signs only.
- Keep a few clips locally for the golden test and the avatar spike (single files can be downloaded with `kaggle datasets download yousefdotpy/karsl-502 -f <path>`).

## 7. Next steps

- [ ] Email the author about the licence (role 1)
- [ ] Get `KARSL-502_Labels.xlsx` and verify the 112 candidates (role 1)
- [ ] Team agrees the final first set from tier 1 → `data/vocabulary.csv` (C1) (everyone)
- [ ] Kaggle notebook: extract landmarks for 20 tier-1 signs as the first test (role 2)
- [ ] Quick baseline on those 20 signs with LOSO (role 3)
