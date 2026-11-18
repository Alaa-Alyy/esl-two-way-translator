<div class="cover" markdown="1">
<div class="kicker">ROLE DOCUMENT 06</div>
<div class="title">3D Avatar Engineer</div>
<div class="subtitle">A 3D signer that performs whole sentences smoothly, from real human motion, with facial grammar</div>
<div class="meta">
<div><b>Project:</b> Two-Way Egyptian Sign Language Translation App</div>
<div><b>Owner:</b> ______________________</div>
<div><b>Read with:</b> 00 — Project Master Document</div>
<div><b>Version:</b> 1.0 · November 2026</div>
</div>
</div>

# 1. Your role in one paragraph

You build **the voice of the app for Deaf users**. Many Deaf people in Egypt cannot read Arabic well, so in direction 2 the answer must be signed. Playing recorded clips one after another looks broken, so you build a 3D character that performs a whole sentence as **one continuous movement**, driven by real human motion taken from the dataset's landmarks, with the facial expressions that sign language grammar needs. Your work is part of the project's foundation, not an extra.

# 2. The project in brief

A two-way Android app for one domain (clinic reception):

- **Direction 1:** a Deaf person signs a sentence → the app shows a natural Egyptian Arabic sentence and speaks it.
- **Direction 2:** a hearing person speaks Egyptian Arabic → the app shows the text and **your avatar** signs the sentence smoothly.
- We start with **KArSL-502** signs (landmarks from MediaPipe) and move to Egyptian data later; approved "My Signs" contributions also become avatar animations automatically.

```
 Data (1) ──vocabulary, best takes──> YOU (6)
 CV (2)   ──raw landmarks (C3), smoothing + trimming tools──> YOU (6)
 NLP (5)  ──sign sequences + sentence types (C9)──> YOU (6)
 YOU (6)  ──avatar.glb, animations/*.json, avatar_viewer/ (C10)──> Mobile (4)
```

# 3. Your responsibilities

**Character**

- Choose or build a rigged humanoid character with a full hand skeleton (all finger joints) and facial blendshapes compatible with MediaPipe's 52 (ARKit-style) names. Options: a free/open character with an ARKit-compatible face, adapted in Blender. Check its licence.
- Neutral, friendly, culturally appropriate look; clear contrast between hands, face, and clothes; plain background.
- Export as glTF/GLB, optimized for mobile (polygon count, texture size).

**Retargeting (landmarks → joint rotations)**

- Convert MediaPipe pose and hand landmarks into bone rotations: shoulders, elbows, wrists, and each finger joint (using vectors between keypoints and inverse kinematics where needed).
- Map face blendshapes directly to the character's morph targets.
- Handle MediaPipe's weak hand depth (z): constraints on joint angles, manual correction for difficult signs.

**Cleaning and trimming**

- Smoothing (with CV's filters) to remove jitter.
- Keep only the **core** of each sign: remove the rest pose at the start and end (with CV's trimming tool).
- Choose the best take per sign (with Data and CV).

**Sentence playback**

- Concatenate sign cores with **smooth transitions** (about 150–250 ms blends between the end pose of one sign and the start pose of the next).
- **Facial grammar** by sentence type: raised eyebrows for yes/no questions, furrowed eyebrows for wh-questions, head-shake for negation, neutral for statements.
- **Fingerspelling** of names using alphabet hand shapes.
- Speed control and replay; event when each sign starts (for highlighting the text).

**Viewer**

- `avatar_viewer/`: a three.js page loaded in the app's WebView, with the JavaScript API from contract C10.
- Camera angle options (front, slight side), lighting, performance on a mid-range phone (target 30 fps).

**Automation**

- A script that generates `animations/{sign_id}.json` from landmarks automatically, so new signs (Egyptian data, approved My Signs) become animations without manual work (manual correction optional).

**Evaluation study**

- With Data (1): users watch the same phrases as avatar and as video; measure understanding and rate naturalness and face cues (1–5).

# 4. Inputs you receive

| Input | From | Format | When |
|---|---|---|---|
| Raw landmarks of signs | CV (2) | C3 `.npz` | Month 1 |
| Smoothing + trimming tools | CV (2) | Python | Month 2 |
| Best take per sign, vocabulary | Data (1) | C1, metadata | Month 1 |
| Sign sequences + sentence types | NLP (5) | C9 | Months 2–3 |
| Integration feedback | Mobile (4) | Issues | Months 2–5 |

# 5. Outputs you deliver

| Output | Format | Used by | Due |
|---|---|---|---|
| Spike: one retargeted sign | Video + viewer demo | Team | Week 2 |
| `avatar/avatar.glb` | glTF binary | Mobile | Month 1 |
| `avatar/retarget.py` | Landmarks → animation JSON | You, automation | Month 2 |
| `avatar/animations/{sign_id}.json` (C10) | JSON per sign | Viewer | Months 2–4 |
| `avatar_viewer/` | three.js app + JS API | Mobile | Month 2 (v1), Month 4 |
| Transitions + facial grammar + fingerspelling | In viewer | Mobile | Months 3–4 |
| `docs/avatar_report.md` + user study | Report | Report | Month 5 |

# 6. Contracts you own

**C10 — avatar**

```
avatar/avatar.glb
avatar/animations/{sign_id}.json
{
  "sign_id": "S046", "fps": 30, "source_clip": "S046_K02_11",
  "core_start": 12, "core_end": 58,
  "frames": [ {"bones": {"RightUpperArm": [qx,qy,qz,qw], "RightIndex1": [...], ...},
               "blend": {"browInnerUp": 0.2, "jawOpen": 0.1, ...}}, ... ]
}
```

**Viewer JavaScript API (used by Mobile through WebView)**

```javascript
playSequence({ signs: ["S046","S090"], sentenceType: "wh_question",
               fingerspell: [], speed: 1.0 })
stop()
setCamera("front" | "side")
// callbacks to Android:  Android.onSignStart(index)   Android.onFinished()
```

Missing animation for a sign → call `Android.onMissingAnimation(sign_id)` so the app shows the video fallback.

# 7. Tools and technologies

| Purpose | Tools |
|---|---|
| 3D character | Blender (rigging, blendshapes, export) |
| Format | glTF / GLB |
| Rendering | three.js (inside Android WebView) |
| Retargeting | Python + NumPy + SciPy (rotations / quaternions); optional Blender Python scripts |
| Landmarks | MediaPipe output from CV (C3) |
| Testing | Desktop browser first, then the phone WebView |

Alternatives if WebView is too slow: SceneView/Filament on Android, or Unity as a Library (decide in the week 1–2 spike with Mobile).

# 8. Step-by-step work plan

**Weeks 1–2 (feasibility spike — the most important spike in the project)**

1. Pick a rigged character with hands and ARKit-style face.
2. Take one KArSL sign's landmarks; retarget arms and hands; play it in three.js in a desktop browser.
3. Show it to the team (and if possible a signer): is it understandable? If not, the fallback is trimmed videos with crossfade — the team decides at the end of week 2.

**Month 1**

1. Final character, exported GLB, loaded in Mobile's test WebView.
2. Retargeting for arms and hands; first 5 signs.

**Month 2**

1. `retarget.py` automation; smoothing and trimming with CV's tools.
2. Viewer v1 with `playSequence` for single signs; 20 signs animated.
3. Face blendshapes mapped.

**Month 3**

1. Transitions between signs: sentences play as one continuous motion.
2. Facial grammar by sentence type (with NLP's C9).
3. Animations for the 30–50 most important phrases' signs.

**Month 4**

1. Fingerspelling; speed control; camera options; callbacks for highlighting.
2. Performance on the phone; integration in conversation mode. **Complete product milestone.**

**Month 5**

1. Automatic animations for approved My Signs and any new Egyptian signs.
2. Avatar vs video user study (with Data); `avatar_report.md`.

**Month 6**

1. Freeze; write the avatar chapter; record avatar clips for the presentation.

# 9. Your priorities

| Priority | Items |
|---|---|
| Must | Character, retargeting of arms/hands, viewer with `playSequence`, smooth transitions, video fallback |
| Should | Facial grammar, face blendshapes, fingerspelling, automation script |
| Could | Camera angles, avatar vs video study extended, character customization |

# 10. Definition of done

- The app can take any phrase from `phrases.csv` and the avatar signs it as one smooth sentence that a viewer can understand.
- Sentence type changes the face (question / negation) visibly.
- New signs become animations by running one script.
- Runs smoothly on a mid-range phone.

# 11. Who you work with

| Role | What you exchange | Sync point |
|---|---|---|
| CV (2) | Landmarks, smoothing, trimming — CV supports you most in months 1–3 | Weekly months 1–3 |
| NLP (5) | Sign sequences and sentence types | Month 3 |
| Mobile (4) | Viewer integration, bridge, performance | Months 2–4 |
| Data (1) | Best takes, user study | Months 1, 5 |

# 12. Pitfalls to avoid

- **Perfecting the look before the motion works.** Motion and understanding first, appearance later.
- **Ignoring the face.** Facial expressions are grammar in sign language, not decoration.
- **Noisy finger depth** making hand shapes wrong — use joint limits and check hand shapes visually.
- **Mirror confusion:** the avatar faces the viewer; the signer's right hand must be the avatar's right hand.
- **Heavy models/textures** that make the WebView slow.

# 13. Working with an AI tool

```
I am the 3D Avatar Engineer on a two-way Egyptian Sign Language app (see attached
documents). Input: MediaPipe landmarks (contract C3: pose 33, hands 21 each,
52 face blendshapes). Output: glTF character + per-sign animation JSON + a three.js
viewer with playSequence() (contract C10). Write <task>.
```

# 14. Your report chapter

Why an avatar instead of clips, character design, retargeting method, cleaning and trimming, transitions, facial grammar, fingerspelling, automation for new signs, performance, and the avatar vs video study.
