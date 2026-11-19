# avatar/ — 3D Avatar (role 6)

A 3D signer that performs whole sentences smoothly, from real human motion, with facial grammar.

📄 Role document: [EN](../docs/pdf/en/06_3D_Avatar_Engineer.pdf) · [AR](../docs/pdf/ar/06_3D_Avatar_Engineer.pdf)

## Delivers

| Output | Contract | Used by |
|---|---|---|
| `avatar.glb` | C10 | Mobile |
| `animations/{sign_id}.json` | C10 | viewer |
| `viewer/` (three.js page with `playSequence()`) | C10 | Mobile |
| Avatar vs video study | — | report |

## Receives

Raw landmarks (C3) and smoothing / trimming tools from Computer Vision; best takes and vocabulary (C1, C2) from Data; sign sequences + sentence types (C9) from Speech & NLP.

## Layout

```
avatar/
├── character/               # Blender source (large .blend files via Git LFS or a shared drive)
├── avatar.glb
├── retarget.py              # landmarks → joint rotations → animations/{sign_id}.json
├── animations/
├── viewer/                  # index.html + viewer.js (three.js), the C10 JavaScript API
└── tests/
```

## First two weeks (the most important spike in the project)

1. Pick a rigged character with full hands and an ARKit-style face.
2. Retarget one KArSL sign and play it in three.js in a desktop browser.
3. Show it to the team (and a signer if possible): is it understandable? The team decides at the end of week 2.
