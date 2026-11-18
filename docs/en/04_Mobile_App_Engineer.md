<div class="cover" markdown="1">
<div class="kicker">ROLE DOCUMENT 04</div>
<div class="title">Mobile App Engineer</div>
<div class="subtitle">One fast, simple app that joins every part, usable even by people who cannot read</div>
<div class="meta">
<div><b>Project:</b> Two-Way Egyptian Sign Language Translation App</div>
<div><b>Owner:</b> ______________________</div>
<div><b>Read with:</b> 00 — Project Master Document</div>
<div><b>Version:</b> 1.0 · November 2026</div>
</div>
</div>

# 1. Your role in one paragraph

You build **the product people actually touch**. You design the screens, build the Android app, and integrate the work of every other role: the vision pipeline, the sign model, the language engine, the voice, and the avatar. You make the app fast, offline, and simple, with a Deaf-side interface that works **without reading**. If a person who has never seen the app can hold a full conversation with it without help, you have done your job.

# 2. The project in brief

A two-way Android app for one domain (clinic reception):

- **Direction 1:** a Deaf person signs a sentence → the app shows a natural Egyptian Arabic sentence and speaks it.
- **Direction 2:** a hearing person speaks Egyptian Arabic → the app shows the text and a 3D avatar signs the sentence smoothly.
- Recognition runs on the phone (MediaPipe + `.tflite`). Everything is driven by data files, not hard-coded signs.
- Users can add personal signs and share them ("My Signs").

```
 CV (2)     ──Normalizer.kt, SignSegmenter.kt, QualityChecker.kt──> YOU (4)
 ML (3)     ──sign_encoder.tflite, prototypes, thresholds──> YOU (4)
 NLP (5)    ──intent engine, sentence templates, phrases, audio──> YOU (4)
 Avatar (6) ──avatar.glb, animations, avatar_viewer (three.js)──> YOU (4)
 Data (1)   ──vocabulary.csv, videos──> YOU (4)
 YOU (4)    ──the app, camera frames, My Signs submissions, feedback──> everyone
```

# 3. Your responsibilities

**Design**

- Figma designs for all screens before coding; review them with the team and, if possible, a Deaf tester.
- Deaf-side rules: icons and sign videos instead of words, large touch targets, ✓/✗ confirmation, no screen that requires reading.
- App name, logo, colours (with the team).

**App foundation**

- Kotlin + Jetpack Compose project, navigation, settings, architecture (MVVM), dependency injection (optional Hilt).
- Load all content from data files (`vocabulary.csv`, model package, phrases) — never hard-code signs.
- Offline storage with Room (history, personal signs, settings).

**Direction 1 integration**

- CameraX preview + analysis → CV's `VisionPipeline` → `SignSegmenter` → `Normalizer` → LiteRT interpreter → recognizer rule (from ML) → recognition result (C6).
- Live landmark overlay (debug mode), framing guide using `QualityChecker`.
- "Did you mean?" with **small sign videos/icons** for the top 3.
- Send sign sequence to NLP's sentence generator (C7); show the sentence; ✓ confirmation by the Deaf user; play audio.
- Emergency alert for signs marked `urgent` in the vocabulary.

**Direction 2 integration**

- Microphone with Android SpeechRecognizer (`ar-EG`), text box, quick-question buttons.
- Call NLP's understanding engine (C8) → sign sequence (C9) → avatar viewer `playSequence`.
- Show the text under the avatar; highlight the current sign (`onSignStart`); replay and slower buttons.
- Low-confidence: show the 3 closest phrases to the hearing person.

**Conversation mode (main screen)**

- Split screen: Deaf half (camera + avatar) and hearing half (text + microphone), hearing half rotated 180° for a phone lying on the table.
- Saved conversation history.

**My Signs and calibration**

- Recording flow: word (text or icon) → 5 repetitions with guidance → checks (quality, consistency, conflict) → save locally → works immediately.
- Share flow with explicit consent → Firebase (C11).
- Receive approved shared signs from Firebase without an app update (Remote Config / Firestore sync).
- Calibration screen ("Teach the app your signing").

**Other screens**

- Home, dictionary (browse signs with video/avatar), settings (language, voice, avatar speed, privacy), emergency, WASEL hand-over button.
- "Wrong translation?" button that stores the sample only with permission.

**Performance and quality**

- Measure time from end of signing to text/voice (target < 1.5 s), fps, memory, battery, APK size on a mid-range phone.
- Background threads for vision and inference; no UI freezes.

# 4. Inputs you receive

| Input | From | Format | When |
|---|---|---|---|
| Vision modules | CV (2) | Kotlin (`VisionPipeline`, `Normalizer`, `SignSegmenter`, `QualityChecker`) | Months 2–3 |
| Model package | ML (3) | C5 | Month 1 (dummy), Month 2+ |
| Recognizer rule + Python reference | ML (3) | Spec + script | Month 2 |
| Understanding + sentence engines | NLP (5) | Kotlin library or API (C7, C8, C9) | Months 2–4 |
| Audio files | NLP (5) | `audio/*.mp3` | Month 3 |
| Avatar | Avatar (6) | `avatar.glb`, `animations/`, `avatar_viewer/` (C10) | Months 2–4 |
| Vocabulary + videos | Data (1) | C1 + `videos/` | Month 1 |

# 5. Outputs you deliver

| Output | Format | Used by | Due |
|---|---|---|---|
| Figma file | All screens | Team | Month 1 |
| App skeleton with live landmarks | APK | Team | Month 1 |
| Integrated app, direction 1 | APK | Team | Month 3 |
| Complete two-way app | APK | Team, testers | Month 4 |
| My Signs (personal + sharing) | In app | Data, ML | Months 4–5 |
| `docs/performance_report.md` | Latency, fps, memory, battery, size | Report | Month 5 |
| Final `app-release.apk` | APK | Defense | Month 6 |

# 6. Contracts you own or use

**C6 — recognition result (you produce, NLP uses)**

```json
{"signs": [{"sign_id": "S045", "confidence": 0.91, "top3": ["S045","S012","S077"]}],
 "context": "ASK_PAIN_LOCATION"}
```

**C11 — My Signs submission (you produce with Data)**

```json
{"submission_id": "...", "word_ar_eg": "...", "embeddings": [[...], ...],
 "landmarks_files": ["..."], "video_consent": false, "region": "Cairo",
 "app_version": "1.2.0", "model_version": "v3"}
```

**You use:** C1 (vocabulary), C5 (model package), C7/C8/C9 (language engine), C10 (avatar API).

**Avatar bridge (WebView)**

```kotlin
webView.evaluateJavascript("playSequence(${json})", null)   // json = C9 signs + sentenceType + speed
// JS -> Kotlin via @JavascriptInterface: onSignStart(index), onFinished()
```

**Suggested app modules**

```
android/
  app/            screens, navigation (Compose)
  core-vision/    CV modules
  core-model/     LiteRT + recognizer + prototypes
  core-language/  NLP engine wrapper
  core-avatar/    WebView + three.js assets
  core-data/      Room, vocabulary loader, Firebase sync
```

# 7. Tools and technologies

| Purpose | Tools |
|---|---|
| IDE / language | Android Studio, Kotlin, Jetpack Compose |
| Camera | CameraX |
| Vision | MediaPipe Tasks Vision (Android) |
| Model | LiteRT (`.tflite`) |
| Video | Media3 ExoPlayer |
| Avatar | WebView + three.js (assets from Avatar 6) |
| Speech | Android SpeechRecognizer (`ar-EG`), TextToSpeech fallback |
| Storage | Room |
| Backend | Firebase Auth, Firestore, Storage, Remote Config |
| Design | Figma |
| Profiling | Android Profiler |

# 8. Step-by-step work plan

**Weeks 1–2 (feasibility spike)**

1. One test app with CameraX + MediaPipe + a three.js WebView showing a cube/character at the same time. Measure fps.
2. Load a dummy `.tflite` from ML and run it.
3. Agree contracts C5–C11 interfaces.

**Month 1**

1. Figma for all screens.
2. Project structure and modules; live landmark overlay (milestone).
3. Vocabulary loader.

**Month 2**

1. Integrate CV's Normalizer and the model package v1; recognizer rule; compare with ML's Python reference.
2. First direction 2 screen: speech → text → dummy phrase → video playback.
3. Load the first avatar in WebView.

**Month 3**

1. Segmenter + "Did you mean?" + sentence display + audio (direction 1 complete on the phone).
2. Framing guide; emergency alert.

**Month 4**

1. Conversation mode; avatar playing C9 sequences with highlighting.
2. My Signs personal flow; history; settings.
3. Performance pass (latency < 1.5 s target). **Complete product milestone.**

**Month 5**

1. My Signs sharing + receiving approved signs; calibration screen; context-aware restriction.
2. Fixes from user tests; WASEL button; dictionary.
3. `performance_report.md`.

**Month 6**

1. Feature freeze in week 1; bug fixes only; final APK; demo build on two phones.

# 9. Your priorities

| Priority | Items |
|---|---|
| Must | Both directions integrated, conversation mode, Did you mean, offline recognition, audio, avatar playback |
| Should | Text-free Deaf UI, My Signs, emergency alert, framing guide |
| Could | Calibration, WASEL hand-over, dictionary, history export |

# 10. Definition of done

- A person who has never seen the app completes a clinic conversation without help.
- No hard-coded signs: swapping the model package and vocabulary changes the app's signs.
- Latency, fps, memory measured on a mid-range phone and reported.
- The app works with airplane mode on (except optional online features).

# 11. Who you work with

| Role | What you exchange | Sync point |
|---|---|---|
| CV (2) | Vision modules, camera, performance | Weekly from month 2 |
| ML (3) | Model package, recognizer, calibration/My Signs | Every model version |
| NLP (5) | Language engine, audio, quick buttons | Months 2–4 |
| Avatar (6) | Viewer, animations, bridge | Months 2–4 |
| Data (1) | My Signs review flow, user tests | Months 4–5 |

# 12. Pitfalls to avoid

- **Running vision on the UI thread** → freezes.
- **Front camera mirroring and rotation** handled differently from Python → wrong features. Agree with CV.
- **Integrating everything at the end.** Integrate early with dummy modules, replace them as real ones arrive.
- **Text everywhere on the Deaf side.** Test each screen with the question "can someone who cannot read use this?"
- **Feature creep in month 6.** Freeze means freeze.

# 13. Working with an AI tool

```
I am the Mobile App Engineer on a two-way Egyptian Sign Language Android app
(see attached documents). Kotlin + Jetpack Compose + CameraX + MediaPipe Tasks +
LiteRT. Model package follows contract C5, language engine C7-C9, avatar API C10.
No sign may be hard-coded; everything loads from vocabulary.csv. Write <task>.
```

# 14. Your report chapter

App requirements and users, UX design (especially the text-free Deaf interface), architecture and modules, integration of vision, model, language, voice and avatar, My Signs flow, offline design, performance results, and usability findings.
