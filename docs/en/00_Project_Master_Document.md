<div class="cover" markdown="1">
<div class="kicker">GRADUATION PROJECT · MASTER DOCUMENT</div>
<div class="title">Two-Way Egyptian Sign Language Translation App</div>
<div class="subtitle">Real-time sentence translation between Deaf signers and hearing speakers, on a phone, in Egyptian Arabic</div>
<div class="meta">
<div><b>Document:</b> 00 — Project Master Document (the full picture)</div>
<div><b>Audience:</b> every team member, supervisors, and the AI tools we work with</div>
<div><b>Version:</b> 1.0 · November 2026</div>
<div><b>Companion documents:</b> 01–06, one per role</div>
</div>
</div>

# 0. How to use this document

This is the **single source of truth** for the project. It explains what we are building, why, how every part works, which tools we use, how the work is split, and how we will be evaluated.

- **Everyone reads this document fully once.** Then each person works mainly from their own role document (01–06), which repeats the parts they need and adds their exact tasks, inputs, and outputs.
- **Section 19 (Interfaces and contracts)** is the most important technical section for teamwork. It defines the exact files each role hands to the others. If you change a contract, the roles that use it must agree first.
- **Working with an AI tool?** Paste this document and your role document into it as context before asking for help. Both were written so that an AI tool can understand the whole project from them.
- The Markdown sources live in the GitHub repo under `docs/`. The PDFs are generated from them with `python docs/build.py`. **Change the Markdown, never the PDF.**

| Doc | Title |
|---|---|
| 00 | Project Master Document (this one) |
| 01 | Data & Evaluation Engineer |
| 02 | Computer Vision Engineer |
| 03 | Machine Learning Engineer |
| 04 | Mobile App Engineer |
| 05 | Speech & NLP Engineer |
| 06 | 3D Avatar Engineer |

# 1. The project at a glance

**What it is.** A mobile app (Android) that lets a Deaf person and a hearing person have a real conversation face to face, without a human interpreter, in a real-life situation. The first situation (domain) is **clinic reception**.

**Direction 1 — Sign to speech.** The Deaf person signs a sentence in front of the phone camera. The app recognizes the sequence of signs, turns it into a **natural Egyptian Arabic sentence**, shows it on the screen, and **speaks it aloud** (the hearing person may be busy and not looking at the screen).

**Direction 2 — Speech to sign.** The hearing person speaks Egyptian Arabic. The app shows the text and a **3D signing avatar performs the sentence in sign language** as one smooth, continuous movement — because many Deaf people in Egypt cannot read Arabic well, text alone is not enough.

**Key principles**

1. **Sentences, not words.** Both directions translate full, connected, understandable sentences.
2. **Egyptian first.** The hearing side is Egyptian Arabic end to end (speech recognition, understanding, text, voice). The sign side starts with public Arabic sign data and moves to Egyptian Sign Language (ESL) as Egyptian data becomes available.
3. **Works for anyone.** We measure accuracy on people the model has never seen, not only on the people it was trained on.
4. **Honest.** When the app is not sure, it asks ("Did you mean…?") instead of guessing. It never invents a translation.
5. **Data-agnostic.** No sign is hard-coded. Replacing the dataset only means retraining, not rewriting the app.
6. **On-device and private.** Recognition runs on the phone, offline. Video never leaves the phone without explicit consent.

# 2. The problem

Sign language is the main language of Deaf people, but most hearing people do not know it. In Egypt a Deaf person usually needs a human interpreter at the clinic, the pharmacy, the bank, or a government office. Interpreters are rare, expensive, and often not available at the exact moment they are needed.

Egypt's **WASEL** app (Ministry of Communications and Information Technology) connects Deaf users by video call to live interpreters. It is valuable, but every call needs a human interpreter, so it does not cover the quick, everyday, face-to-face moment — the receptionist or pharmacist standing right in front of the Deaf person. **Our app covers that moment, and can hand over to a live WASEL interpreter when it is not enough.**

Two facts shape our design:

- **Literacy.** Many Deaf people in Egypt have limited Arabic reading ability because of unequal access to education. A text-only answer does not reach them. This is why direction 2 must output **sign language**, and why the Deaf side of the interface must work **without text** (icons, sign videos, ✓/✗). Any statistic we quote about this must have a source.
- **No Egyptian data.** Egyptian Sign Language has almost no public digital resources. Estimates of the number of hearing-impaired people in Egypt range from about 7 million to more than 10 million; always quote a source.

# 3. Vision, goals, and scope

## 3.1 Vision

A national, community-built Egyptian sign language translator: a phone app that any Deaf person and any hearing person can use instantly, that grows its own Egyptian sign dictionary with the help of the Deaf community, and that works alongside human interpreters instead of replacing them.

## 3.2 Goals for the graduation version

- A working two-way **sentence** translator for **one domain** (clinic reception) on an Android phone.
- Direction 1: signed sentence → Egyptian Arabic text + voice.
- Direction 2: Egyptian Arabic speech → text + continuous 3D avatar signing.
- A target vocabulary of **about 100 signs** (built in steps: 50 → 100), chosen for the domain.
- Measured accuracy on **unseen signers** (Leave-One-Signer-Out evaluation).
- Response time under about **1.5 seconds** from the end of a sentence to the output, on a mid-range phone.
- "My Signs": users can add personal signs and submit them for approval to the shared dictionary.
- Tested with real users, ideally including Deaf users.

## 3.3 Out of scope for v1 (stated clearly in the defense as future work)

- Fast, fully fluent continuous signing as used between two Deaf people.
- Open-domain translation of anything a person may say.
- Other domains (banking, government services), iOS, and fully automatic model retraining.

# 4. Key concepts in simple words

| Concept | Meaning | Why it matters to us |
|---|---|---|
| Sign language is its own language | ESL has its own grammar and word order; it is not Arabic on the hands | Translation is never word-for-word |
| Manual and non-manual features | Hands (shape, movement, location) plus face, eyebrows, mouth, head, body | We track hands, body, and face; the avatar must use the face |
| Isolated vs continuous signing | One sign at a time vs signs flowing in a sentence | Our data is isolated; our app must handle sentences |
| Gloss | A written label for a sign, e.g. DOCTOR | We use sign IDs (S001…) as glosses |
| Landmarks / keypoints | Coordinates of body, hand, and face points found by a vision model | Our main input features |
| Signer-independent | Tested on people not seen in training | The real test of "works for anyone" |
| LOSO | Leave-One-Signer-Out: train on all signers but one, test on that one, repeat | Our main evaluation protocol |
| Embedding | A vector "fingerprint" of a sign | Lets us add new signs without retraining (My Signs, calibration) |
| Fingerspelling | Spelling a word letter by letter with hand shapes | Used for names and unknown words |
| Intent / entities | The meaning of a sentence (ASK_DURATION) and its details (SYMPTOM = FEVER) | How we understand spoken Arabic |

# 5. What we learned from previous work

| Work | Data | Result | Lesson |
|---|---|---|---|
| KArSL (Sidig et al., 2021) | 502 Arabic signs, 3 signers, Kinect | 76–89% on known signers, 8–28% on a new signer | Few signers → models fail on new people. Always test on new signers |
| Alyami et al., Transformer + landmarks | KArSL-100, LSA64 | 99.7% known signers, 68.2% new signers | Landmarks + face help; new signers stay hard |
| Egyptian CNN-LSTM (Elhagry & Elrayes) | 9 Egyptian words, 2 signers | 90% / 72% | Egyptian data is tiny |
| MediaPipe + SVM studies | Static alphabets and numbers | 96–99% | Landmarks are light and fast on phones |
| Sign Language Transformers, STMC | German weather domain | ~21–25 BLEU-4 | Free sentence translation is still unsolved → we use a closed domain |
| Egyptian datasets (AAST 55 words, Ibrahim et al. 2025), Tafahom app | Small Egyptian sets | — | Egyptian data is a recognized gap |

**Gaps we target:** most systems are one-direction, word-level, hands-only, tested on the same signers they were trained on, never tested with Deaf users, and output text that many Deaf users cannot read.

# 6. What makes our project different

| Feature | Why it is special |
|---|---|
| **Sentence-level, two-way translation** | Most student projects stop at single words, one direction |
| **Continuous 3D avatar output** | Direction 2 reaches Deaf users who cannot read; smooth sentences, not clips one after another |
| **Facial grammar in the avatar** | Question faces, negation head-shake, driven by real face blendshapes |
| **Works on unseen signers, measured honestly** | LOSO numbers reported, not training accuracy |
| **Synthetic sentence data** | We build sentence training data from isolated signs — a research contribution |
| **Context-aware vocabulary** | The app narrows the candidate signs to what fits the moment, keeping accuracy high as the vocabulary grows |
| **My Signs (community contributions)** | Users add personal signs instantly and submit them for approval; the community builds the Egyptian dictionary |
| **Personal calibration** | "Teach the app your signing" in a few repetitions |
| **Text-free interface for the Deaf side** | Designed for users with limited literacy |
| **Egyptian Arabic end to end** | Egyptian speech recognition, Egyptian sentences, Egyptian voice |
| **Confidence, rejection, and emergency alerts** | Safe in a medical setting |
| **Offline and private** | Runs on the phone; video stays on the phone |
| **Hand-over to a human interpreter** | Complements the national WASEL service |

# 7. System overview

## 7.1 Architecture

```
 DIRECTION 1: SIGN -> SPEECH
 Camera -> Vision (MediaPipe: hands, body, face) -> Normalization -> Segmentation
        -> Sign encoder (on-device model) -> Sign IDs + confidence
        -> Confidence check / "Did you mean?" -> Sentence generation (Egyptian Arabic)
        -> Text on screen + Egyptian voice

 DIRECTION 2: SPEECH -> SIGN
 Microphone -> Speech recognition (ar-EG) -> Text cleaning -> Understanding (intent + entities)
        -> Sign sequence in ESL order (+ fingerspelling for names)
        -> 3D avatar: smooth continuous signing + facial grammar
        -> Text on screen under the avatar

 SHARED, LANGUAGE-INDEPENDENT LAYER
 vocabulary.csv : sign_id -> Egyptian Arabic / MSA / English / category / media
 phrases.csv    : phrase_id -> sign sequence + Egyptian sentence templates
```

## 7.2 The data-agnostic principle

Nothing about specific signs lives in the code. Everything is driven by:

- `vocabulary.csv` — the list of signs and their words in each language,
- the trained model files and their `labels.json`,
- `phrases.csv`, `intents.json`, and sentence templates,
- the avatar animation files.

When Egyptian data arrives, we update these files and retrain. **The app code does not change.** This is a design decision we defend in the presentation.

## 7.3 Where computer vision fits

The project is a **vision-based, pose-driven** system. Computer vision models (MediaPipe: palm detection, hand landmark CNN, BlazePose, face landmarker) read the camera frames and output body, hand, and face keypoints. A temporal model then understands the movement over time. We use keypoints instead of raw pixels because they ignore background, clothes, lighting, and skin tone, need far less data, run fast on phones, and protect privacy. We also train a pixel-based baseline to prove this choice with numbers.

# 8. Direction 1 in detail: sign → text + voice

1. **Capture.** CameraX delivers frames (target 30 fps, at least 15 fps for processing).
2. **Quality check.** Before translating, the app checks lighting, blur, whether the person is in frame and at a good distance, and whether both hands are visible. It guides the user ("move closer", "more light").
3. **Landmarks.** MediaPipe Hand, Pose, and Face Landmarkers run on each frame and output keypoints.
4. **Normalization.** Coordinates are centred on the middle of the shoulders and divided by shoulder width; hand points are also stored relative to the wrist; left-handed signers are mirrored so the dominant hand is always on the same side. Short gaps are interpolated; a "hand present" flag is added.
5. **Segmentation.** A motion gate watches the wrists: signing starts when the hands leave the rest position and ends when they return. Inside a sentence, short holds and velocity minima split the stream into individual signs. A sliding-window fallback handles signers who do not pause.
6. **Recognition.** Each segment is resampled to 48 frames, motion features are added, and the **sign encoder** produces an embedding. The embedding is compared with stored sign prototypes. The result is a sign ID and a confidence. A **NONE** class rejects non-sign movement (scratching, fixing glasses).
7. **Context-aware filtering.** If the conversation context is known (e.g. the hearing person asked "where does it hurt?"), the candidate list is narrowed to body parts first.
8. **Confidence check.** Below the threshold, the app shows the top 3 candidates as **small sign videos with icons**, not as Arabic words, and the user taps the right one.
9. **Sentence generation.** The sign sequence is turned into a natural Egyptian Arabic sentence. Example: `[ME] [HEADACHE] [FEVER] [YESTERDAY]` → «عندي صداع وسخونية من امبارح». Two methods: templates (reliable, offline) and an optional LLM (more natural, online, must not add information). The Deaf user confirms with ✓ before the sentence is spoken.
10. **Output.** Large text on the hearing person's half of the screen and Egyptian Arabic voice.
11. **Emergency.** Signs such as EMERGENCY or CHEST_PAIN trigger a large alert telling staff to get help immediately, in addition to the translation.

**Continuous signing, honestly stated.** Our training data contains isolated signs. To recognize sentences we (a) segment the stream into signs and recognize each one (Must), and (b) train a sequence model on **synthetic sentences** made by joining isolated sign landmarks with smooth transitions (Should). Version 1 targets natural signing with small pauses, not very fast fluent signing.

# 9. Direction 2 in detail: speech → text + sign

1. **Input.** The hearing person speaks, types, or taps a **ready-made question button** (common clinic questions — fast and reliable in noisy rooms).
2. **Speech recognition.** Android SpeechRecognizer with locale `ar-EG` (primary). Whisper models fine-tuned on Egyptian Arabic are evaluated on a server as a comparison.
3. **Text cleaning.** Normalize Egyptian text (أ/إ/آ → ا, ة/ه, ى/ي, numbers, filler words).
4. **Understanding.** Match the sentence to an **intent** and **entities**: «بقالك قد ايه عندك السخونية دي؟» → `ASK_DURATION`, `SYMPTOM = FEVER`. Many Egyptian paraphrases map to the same intent.
5. **Sign ordering.** Map intent + entities to a validated sign sequence **in sign-language order**, not Arabic word order: `[FEVER] [HOW-LONG] (wh-question face)`. Optional LLM conversion of free text into sign IDs, restricted to signs in the vocabulary.
6. **Unknown words.** Names → fingerspelling by the avatar. Out-of-domain → a clear "not supported" icon. **The system never invents a sign.**
7. **Confirmation.** If understanding confidence is low, the hearing person sees the 3 closest phrases and picks one.
8. **Avatar output.** The avatar performs the whole sequence as one continuous movement with the correct facial expression for the sentence type. The text appears under it; the current sign is highlighted; buttons for replay and slower speed.

# 10. The 3D signing avatar

Playing recorded clips one after another does not work for sentences: each clip starts and ends at rest, the framing and signer change between clips, and the result is slow and broken. A full-sentence video would be natural, but requires an interpreter to record every sentence, which we do not have. **The avatar is therefore the main output of direction 2.**

How it works:

- **Motion source.** For each sign we take the landmarks of the best repetition from the dataset.
- **Retargeting.** Landmarks are converted into joint rotations for a rigged 3D character (body, arms, all fingers, face).
- **Cleaning.** Smoothing removes jitter; difficult signs (finger depth) are corrected by hand.
- **Core trimming.** Only the core of each sign is kept; the rest pose at the start and end is removed.
- **Transitions.** A smooth blend (about 150–250 ms) connects the end of one sign to the start of the next, so a sentence is one continuous motion.
- **Facial grammar.** MediaPipe face blendshapes drive the face; sentence-level rules add raised eyebrows for yes/no questions, furrowed eyebrows for wh-questions, and a head-shake for negation.
- **Rendering.** Character built in Blender (glTF/GLB), displayed in the app with three.js inside a WebView; controllable speed and camera angle.
- **Fallback.** A recorded sign video is shown for any sign without a clean animation.

Limits we state honestly: the avatar is less natural than a human signer and some transitions may look mechanical. We measure understanding with users (avatar vs video study).

# 11. My Signs: community-built dictionary

Users can add a sign that the app does not know.

**Personal sign (instant, on the user's phone only)**

1. The user types the word in Egyptian Arabic (or picks an icon/picture if they cannot write).
2. The user performs the sign **5 times**, at slightly different distances and angles.
3. The app checks quality (hands visible, lighting), consistency (the 5 repetitions match), and conflict (too similar to an existing sign → "this looks like DOCTOR, are you sure?").
4. The average embedding is stored on the phone. The sign works immediately, offline, with no retraining.
5. In direction 2, the user's own recording is shown for that word on their phone.

**Shared sign (for all users, after approval)**

1. The user taps "Share this sign" with explicit consent; landmarks are sent, and the video only if the user agrees.
2. Reviewers — a certified interpreter and Deaf partners, not only the team — check that the sign is correct and Egyptian, tag the region, and reject duplicates or offensive content.
3. Approved signs are added to the shared vocabulary and delivered to all users **without an app update**.
4. A sign enters the shared recognition model only after **at least 3 different contributors** have submitted it; until then it is marked "waiting for contributors".
5. The avatar animation is generated automatically from the approved landmarks.
6. The shared model is retrained periodically (manual script in v1).

This feature turns the app into a **community-built Egyptian sign dictionary**, and it is the long-term answer to the lack of Egyptian data.

# 12. Safety and trust features

- **Assistive-tool statement.** The app states clearly that it does not replace a human interpreter in serious situations.
- **Show and confirm.** The app always shows what it understood and lets the user confirm before anything is spoken or acted on.
- **Confidence threshold and "Did you mean?"** instead of wrong answers.
- **NONE class** to reject movements that are not signs.
- **Emergency signs** trigger an explicit alert to call staff.
- **Never invent.** Unsupported input gets a clear "not supported" message.
- **Hand-over to a human.** A button opens WASEL to reach a live interpreter.

# 13. Data strategy

## 13.1 Phase A — KArSL (now)

We start with **KArSL-502** (Arabic Sign Language database, 502 signs, 3 signers, ~50 repetitions each, Kinect recordings; Kaggle mirror: `yousefdotpy/karsl-502`). Its signs follow the **Unified Arabic Sign Language** dictionary and were recorded in Saudi Arabia. It lets us build and test the full pipeline, models, and app now.

Before use we verify: the exact format of the Kaggle mirror (videos, frames, or skeleton), the licence and terms of use (academic use, showing clips in the app), and how many of its words fit the clinic domain.

**Known limitations**

- It is **not Egyptian Sign Language**: many signs differ. Each sign has an `esl_verified` flag checked with an Egyptian interpreter.
- **Only 3 signers**: LOSO means training on 2 and testing on 1, so the unseen-signer number will be modest. We report it honestly and rely on normalization, augmentation (especially body-proportion changes), and personal calibration.

## 13.2 Phase B — Egyptian data (when available)

- Candidate sources: AAST Egyptian Sign Language dataset (55 words, Mendeley Data), Ibrahim et al. 2025, new datasets, Deaf associations, and approved My Signs contributions.
- A `dataset_adapter.py` converts any new dataset into our file structure in one step.
- We pretrain on KArSL and fine-tune on Egyptian data, and compare with training from scratch, always evaluating on Egyptian signers.

## 13.3 Vocabulary size

- Build the pipeline on **50 signs**, grow to **~100** as the product target, and run an experiment on **200 / all** signs for the report.
- We plot accuracy on unseen signers against vocabulary size; this answers "why this number?" with evidence.
- Context-aware vocabulary keeps accuracy high as the vocabulary grows.
- The avatar covers the most important 30–50 phrases first; the rest use video fallback.

## 13.4 Vocabulary groups (clinic domain, chosen from what KArSL contains)

| Group | Examples |
|---|---|
| Basics | hello, thank you, sorry, please, yes, no, help, wait, understand, repeat |
| People & places | doctor, nurse, patient, reception, clinic, laboratory, pharmacy |
| Appointments & time | appointment, today, tomorrow, yesterday, time, days, numbers |
| Symptoms | pain, headache, fever, cough, vomiting, dizziness, allergy |
| Body parts | head, eye, ear, throat, chest, stomach, back, hand, leg, tooth |
| Tests & payment | blood test, X-ray, prescription, medicine, price, pay |
| Fingerspelling | Arabic alphabet for names |

# 14. Computer vision and features

- **Landmarks per frame:** upper-body pose points, 21 points per hand, about 40 face points (eyebrows, eyes, mouth), plus 52 face blendshapes.
- **Normalization:** shoulder-centre origin, divide by shoulder width; hands also relative to wrist; mirror left-handed signers.
- **Missing data:** interpolate short gaps; otherwise zeros + presence flag.
- **Fixed length:** resample each sign to 48 frames; add frame-to-frame differences (velocity).
- **Feature vector size F** is defined exactly in `feature_spec.md` (version-controlled).
- **Train/serve parity:** the same MediaPipe model versions and the same normalization must run in Python (training) and Kotlin (phone). A **golden test** compares both on the same clips; any difference breaks the model on the phone.
- **Quality checker and framing guide** in the app.
- **Pixel baseline** (small CNN on frames) to compare against landmarks.

# 15. Machine learning

- **Baseline:** Random Forest / SVM on flattened features — proves the data is sound.
- **Sign encoder:** a small temporal model (GRU, 1D-CNN/TCN, or small Transformer — compared) trained with a classification + metric-learning objective so that it outputs a good **embedding**. Recognition = nearest prototype. This single design gives us recognition, NONE rejection, personal calibration, and My Signs.
- **NONE class:** trained on non-sign movements and transitions.
- **Augmentation:** small rotations, shifts, scaling, speed changes, joint noise, frame dropping, and **body-proportion changes** (arm length, shoulder width).
- **Evaluation:** LOSO; accuracy, macro-F1, top-3, confusion matrix, known vs unseen signers.
- **Sequence model (Should):** CTC model trained on synthetic sentences.
- **Export:** LiteRT (.tflite), float16/int8 quantization, accuracy before/after, speed on a real phone.
- **Experiment tracking:** Weights & Biases or TensorBoard; every result reproducible from a config file.

# 16. Speech and language (Egyptian Arabic)

- **ASR:** Android SpeechRecognizer `ar-EG`; Whisper Egyptian fine-tunes as comparison; word error rate (WER) measured on our own recorded clinic sentences, including noisy rooms.
- **Normalization:** PyArabic / CAMeL Tools style rules.
- **Intents:** 30–50 clinic intents, many Egyptian paraphrases each; matching with rapidfuzz + sentence embeddings; optional fine-tuned Arabic model.
- **Entities:** body part, symptom, severity, time, day, number, name.
- **Sentence generation (direction 1):** templates in Egyptian Arabic; optional LLM rewrite with strict "do not add information" rules and template fallback offline.
- **Sign ordering (direction 2):** templates mapping intent + entities to sign sequences; optional LLM restricted to the vocabulary.
- **Voice:** pre-generated Egyptian Arabic audio (e.g. Azure `ar-EG` voices) for fixed phrases; phone TTS as fallback.
- **Quick-reply buttons** for the hearing person.

# 17. The mobile app

| Screen | What it does |
|---|---|
| Home | Choose the situation (domain), language, and mode |
| Conversation mode (main) | Phone on the table; split screen: Deaf half (camera, avatar) and hearing half (text, microphone, upside down) |
| Sign → speech | Live camera with framing guide, recognized text, confidence, "Did you mean?" with sign videos, speak button |
| Speech → sign | Microphone, text box, quick-question buttons, avatar with replay/slow, text under it |
| My Signs | Record, check, save, and share personal signs |
| Calibration | "Teach the app your signing" |
| Dictionary | Browse signs with video and avatar |
| Emergency | Large ready messages, call, share location |
| Settings | Language, voice, avatar speed, privacy, consent |

**Deaf-side design rules:** icons and sign videos instead of words, large touch targets, ✓/✗ confirmation, no screen that requires reading.

**Technology:** Kotlin + Jetpack Compose, CameraX, MediaPipe Tasks, LiteRT, Media3 ExoPlayer, WebView + three.js for the avatar, Room for offline storage, Firebase for accounts, contributions, and dictionary updates.

# 18. Technology stack

| Area | Tools |
|---|---|
| Languages | Python 3.11+, Kotlin, JavaScript |
| Vision | MediaPipe Tasks (Hand, Pose, Face Landmarker), OpenCV |
| ML | NumPy, pandas, scikit-learn, PyTorch or TensorFlow/Keras, Weights & Biases |
| Compute | Kaggle / Google Colab GPUs (free) |
| On-device model | LiteRT (.tflite); ONNX Runtime Mobile as alternative |
| Speech | Android SpeechRecognizer (ar-EG), Whisper (Egyptian fine-tunes), jiwer for WER |
| Language | PyArabic, CAMeL Tools, rapidfuzz, sentence-transformers, optional LLM API |
| Voice | Azure Egyptian Arabic voices (pre-generated), Android TTS fallback |
| Avatar | Blender, glTF/GLB, three.js |
| App | Android Studio, Kotlin, Jetpack Compose, CameraX, Media3, Room |
| Backend | Firebase (Auth, Firestore, Storage, Remote Config); optional FastAPI server |
| Design | Figma |
| Teamwork | GitHub (monorepo, Projects, Issues, Actions), Markdown docs |
| Hardware | Team laptops, 2–3 mid-range Android test phones, tripod, ring light |

# 19. Team roles and interfaces (contracts)

## 19.1 The six roles

| # | Role | One-line mission |
|---|---|---|
| 1 | Data & Evaluation Engineer | Clean, versioned data and honest, strong numbers |
| 2 | Computer Vision Engineer | Video → clean features, identical in Python and on the phone |
| 3 | Machine Learning Engineer | A sign model that works for anyone |
| 4 | Mobile App Engineer | One fast, simple app that joins everything, usable without reading |
| 5 | Speech & NLP Engineer | The app hears, understands, and speaks Egyptian, in both directions |
| 6 | 3D Avatar Engineer | A 3D signer that performs whole sentences smoothly |

All roles are equal. Every member also writes their chapter of the report, reviews pull requests from other roles, and joins the weekly demo.

## 19.2 Who hands what to whom

```
 1 Data & Evaluation ──vocabulary, clips, metadata, splits──> 2, 3, 5, 6
 2 Computer Vision   ──landmarks, features, Normalizer.kt──> 3, 4, 6
 3 Machine Learning  ──sign_encoder.tflite, prototypes, thresholds──> 4
 5 Speech & NLP      ──intent engine, phrases, templates, audio──> 4, 6
 6 3D Avatar         ──avatar.glb, animations, avatar_viewer──> 4
 4 Mobile App        ──the app, camera frames, feedback samples──> everyone
```

## 19.3 Contracts (frozen in week 2, version-controlled)

**C1 — `data/vocabulary.csv`** (owner: 1)

```
sign_id,ar_eg,ar_msa,en,category,source,esl_verified,urgent,video_file,has_animation
S001,دكتور,طبيب,doctor,people,KArSL,no,no,S001.mp4,yes
S023,وجع في صدري,ألم في الصدر,chest pain,symptom,KArSL,no,yes,S023.mp4,yes
```

**C2 — clips and metadata** (owner: 1) — clip name `SignID_SignerID_Take` (e.g. `S001_K01_07`); `data/metadata.csv` columns: `clip_id, sign_id, signer_id, take, source, dominant_hand, fps, frames, quality_flag, split_group`.

**C3 — raw landmarks** (owner: 2) — `landmarks/raw/{clip_id}.npz` with arrays `pose (T,33,4)`, `left_hand (T,21,3)`, `right_hand (T,21,3)`, `face (T,40,3)`, `blendshapes (T,52)`, `mask_left (T)`, `mask_right (T)`, and scalar `fps`.

**C4 — features** (owner: 2) — `features/{clip_id}.npy`, float32, shape `[48, F]`; exact order and formulas in `docs/feature_spec.md` with a version number. Same logic in `normalize.py` and `Normalizer.kt`.

**C5 — model package** (owner: 3)

```
models/v{N}/sign_encoder.tflite   input [1,48,F] float32 -> output [1,128] L2-normalized embedding
models/v{N}/prototypes.json       {"S001": [[...128 floats...], ...], "NONE": [...]}
models/v{N}/labels.json           ordered sign_ids used in training
models/v{N}/thresholds.json       {"accept": 0.75, "ask": 0.45, "none_margin": 0.1}
models/v{N}/model_card.md         data version, F version, LOSO results
```

**C6 — recognition result** (owner: 4, used by 5)

```json
{"signs": [{"sign_id": "S045", "confidence": 0.91, "top3": ["S045","S012","S077"]}],
 "context": "ASK_PAIN_LOCATION"}
```

**C7 — sentence generation** (owner: 5) — input: list of sign IDs + context; output:

```json
{"text_ar_eg": "عندي صداع وسخونية من امبارح", "text_en": "I have had a headache and fever since yesterday",
 "audio_file": null, "method": "template", "confidence": 0.86}
```

**C8 — understanding result** (owner: 5)

```json
{"text": "بقالك قد ايه عندك السخونية دي؟", "intent": "ASK_DURATION",
 "entities": {"SYMPTOM": "FEVER"}, "phrase_id": "P017", "confidence": 0.82,
 "alternatives": ["P018", "P020"]}
```

**C9 — sign sequence for output** (owner: 5, used by 4 and 6)

```json
{"phrase_id": "P017", "signs": ["S031", "S090"], "sentence_type": "wh_question",
 "fingerspell": [], "text_ar_eg": "بقالك قد ايه عندك السخونية؟"}
```

**C10 — avatar** (owner: 6) — `avatar/avatar.glb`; `avatar/animations/{sign_id}.json` (`fps`, `core_start`, `core_end`, per-frame joint rotations and blendshapes); viewer JavaScript API: `playSequence({signs, sentenceType, speed})`, `stop()`, events `onSignStart(index)` and `onFinished()`.

**C11 — My Signs submission** (owner: 4 with 1)

```json
{"submission_id": "...", "word_ar_eg": "...", "embeddings": [[...], ...], "landmarks_files": ["..."],
 "video_consent": false, "region": "Cairo", "app_version": "1.2.0", "model_version": "v3"}
```

**Rule:** a contract change needs agreement from every role that uses it, a version bump, and a note in `docs/decisions.md`.

# 20. Plan and timeline (6 months)

## 20.1 Weeks 1–2: feasibility spikes (before locking the plan)

| Role | Question to answer | If the answer is "no" |
|---|---|---|
| 1 | What is the exact KArSL format? Does the licence allow our use? How many clinic words exist? | Change the domain or data source |
| 2 | Do Hand + Pose + Face run together on a mid-range phone, at what fps? | Lower fps, run face every N frames |
| 3 | Does a quick baseline on 20 signs give a reasonable unseen-signer result? | Revisit features before continuing |
| 4 | Do CameraX + MediaPipe + a three.js WebView run together in one app? | Change the avatar renderer |
| 5 | What is the ar-EG WER on 20 recorded clinic sentences? Can an LLM write good Egyptian sentences from sign IDs? | Rely more on templates |
| 6 | Can one KArSL sign be retargeted to an avatar and still be understood? | Fall back to trimmed videos with crossfade |

End of week 2: contracts C1–C11 frozen (v1), targets set, plan confirmed.

## 20.2 Month by month

| Month | Main work | Milestone at the end |
|---|---|---|
| 1 | Spikes, contracts, 50 signs selected, data downloaded, feature spec, app skeleton, Figma, ASR test, avatar rig | Camera shows live landmarks in the app |
| 2 | Baseline + first encoder, LOSO, intents v1, sentence templates, first retargeted signs | Dummy model runs in the app; first real unseen-signer number |
| 3 | Better encoder, augmentation, NONE, segmentation, voice, avatar transitions, vocabulary → 100 | Direction 1 works on the phone with a real model |
| 4 | Both directions joined, conversation mode, Did you mean, facial grammar, speed tuning, My Signs (personal) | **Complete end-to-end product (foundation done)** |
| 5 | My Signs sharing + review, context-aware vocabulary, calibration, user tests, experiments | Stable version + evaluation results |
| 6 | **Feature freeze in week 1**, fixes, report, paper draft, demo video, defense rehearsal | Ready for submission |

# 21. Priorities (MoSCoW)

| Priority | Features |
|---|---|
| **Must** | Both directions at sentence level; avatar with smooth transitions; Egyptian text and voice; confidence + Did you mean + NONE; offline recognition; conversation mode; LOSO evaluation |
| **Should** | My Signs (personal + sharing + review); context-aware vocabulary; text-free Deaf interface; facial grammar; emergency alerts; synthetic-sentence sequence model |
| **Could** | LLM sentence generation; personal calibration; quality checker; WASEL hand-over; pixel baseline; accuracy-vs-vocabulary curve |
| **Won't (v1)** | Fast fluent continuous signing; other domains; iOS; fully automatic retraining |

**Rule: no Should work starts before the Must items are complete and stable.**

# 22. Evaluation plan

| What | How |
|---|---|
| Recognition | Accuracy, precision, recall, macro-F1, top-3, confusion matrix — per sign and overall |
| Generalization | Known signers vs unseen signers (LOSO); the gap is reported |
| Vocabulary size | Unseen-signer accuracy at 50 / 100 / 200 signs |
| Features | Landmarks vs pixel baseline |
| Sentences | Sign error rate on synthetic and real signed sentences |
| Speed | Time from end of signing to text/voice on a mid-range phone (target < 1.5 s); fps; memory; battery |
| Speech side | WER (jiwer), intent accuracy and macro-F1, entity precision/recall, paraphrase robustness |
| Sentence quality | Fluent Egyptian speakers rate generated sentences (meaning, naturalness, 1–5) |
| Avatar | Fluent signers rate understanding, naturalness, face cues (1–5); avatar vs video comparison |
| Usability | Task success, time, corrections, System Usability Scale (SUS) with Deaf and hearing users |

Exact targets are set after the baseline (end of week 2 / month 2). All splits, preprocessing, and configs are published in the repo so results can be reproduced.

# 23. Risks and how we handle them

| Risk | Handling |
|---|---|
| KArSL is not Egyptian | `esl_verified` flag, interpreter review, adapter ready for Egyptian data, honest statement in the defense |
| Only 3 signers → weak on new people | LOSO, normalization, body-proportion augmentation, calibration, My Signs |
| Train/serve feature mismatch | Shared feature spec, golden test in CI |
| Phone too slow | Spike in week 1, lower fps, quantization, face every N frames |
| Avatar looks unnatural | Early spike, facial grammar, user study, video fallback |
| Wrong translation in a medical setting | Confidence threshold, confirmation, NONE, emergency alerts, assistive-tool statement |
| Sign order copying Arabic order | Templates validated by fluent signers |
| Privacy of faces | On-device processing, landmarks instead of video, explicit consent |
| Too many features | MoSCoW, feature freeze in month 6 |
| No Deaf users for testing | Contact associations and schools for the Deaf from month 1 |
| Live demo fails in the hall | Rehearsal in the room, backup phone, recorded demo video |

# 24. Ethics and privacy

- Written informed consent from every person whose data we record or test with.
- University ethics approval for user studies if the university requires it.
- Compliance with Egypt's Personal Data Protection Law (No. 151 of 2020): purpose, consent, the right to delete contributions.
- Landmarks are stored instead of video wherever possible; video is uploaded only with explicit consent.
- No real names in data files; signer IDs only.
- Licence terms of every external dataset are respected and cited.

# 25. How we work together

- **One GitHub monorepo:** `data-pipeline/`, `cv/`, `ml/`, `android/`, `nlp/`, `avatar/`, `docs/`.
- **GitHub Projects board:** every task is an issue with an owner, a label for the role, and a milestone for the month.
- **Pull requests:** every change goes through a PR reviewed by someone from a different role; `main` is always runnable.
- **Weekly demo:** every member shows what actually works (5 minutes each), not slides.
- **`docs/decisions.md`:** every important decision, the date, and why.
- **`docs/contracts/`:** contracts C1–C11 with versions.
- **CI (GitHub Actions):** run tests and the golden test on each PR.
- **Experiment tracking:** every model result linked to a config and a data version.
- **Help rule:** whoever finishes early takes a task from someone who is behind.

# 26. Demo and defense plan

- **Demo scenario (fixed from day one):** a Deaf patient at clinic reception; 6–8 sentences in each direction, including one "Did you mean?" moment, one emergency sign, and one My Signs addition live.
- **Story of the presentation:** problem → literacy insight → two-way sentence translation → avatar → works for anyone (LOSO numbers) → community-built dictionary → path to Egyptian data and national use with WASEL.
- **Backup:** rehearse in the actual hall, backup phone, recorded demo video.
- **Paper:** candidates for publication — synthetic sentence data from isolated signs, avatar understanding study, context-aware vocabulary.

# 27. Future work

- Egyptian Sign Language data from Deaf partners and approved contributions; regional variants.
- More domains as downloadable packs (pharmacy, bank, civil registry, transport, emergency).
- Fluent continuous signing with Transformer methods.
- Integration with WASEL and installation as a desk tablet at public service counters.
- Automatic retraining pipeline, iOS version, public release of the dataset with signers' consent.

# 28. Main references

- Sidig, Luqman, Mahmoud, Mohandes. *KArSL: Arabic Sign Language Database.* ACM TALLIP, 2021. https://doi.org/10.1145/3423420
- Alyami et al. *Isolated Arabic Sign Language Recognition Using a Transformer-based Model and Landmark Keypoints.* ACM TALLIP. https://doi.org/10.1145/3584984
- Elhagry, Elrayes. *Egyptian Sign Language Recognition Using CNN and LSTM.* https://arxiv.org/abs/2107.13647
- Camgoz et al. *Sign Language Transformers.* CVPR 2020. https://arxiv.org/abs/2003.13830
- Yin, Read. *Better Sign Language Translation with STMC-Transformer.* COLING 2020. https://aclanthology.org/2020.coling-main.525
- Abbas et al. *A Multimodal Dataset for Arabic Sign Language Production.* JKSU-CIS, 2024. https://doi.org/10.1016/j.jksuci.2024.102165
- Latif et al. *ArASL: Arabic Alphabets Sign Language Dataset.* Data in Brief, 2019. https://doi.org/10.1016/j.dib.2019.103777
- Ibrahim, Ghantous, Sharaf. *Dataset Generation for Egyptian Arabic Sign Language.* ICAART 2025.
- AAST. *Egyptian Sign Language (55-word dataset).* Mendeley Data, 2025. https://doi.org/10.17632/39tbt2jd7r.2
- Alyami et al. *Isharah: A Large-Scale Multi-Scene Dataset for Continuous Sign Language Recognition.* https://arxiv.org/abs/2506.03615
- KArSL-502 Kaggle mirror: https://www.kaggle.com/datasets/yousefdotpy/karsl-502
- WASEL app (MCIT Egypt): https://play.google.com/store/apps/details?id=com.mcit.wasel
- MediaPipe: https://ai.google.dev/edge/mediapipe/solutions/guide · LiteRT: https://ai.google.dev/edge/litert · Whisper: https://github.com/openai/whisper
