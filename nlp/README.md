# nlp/ — Speech & NLP (role 5)

The app hears, understands and speaks Egyptian Arabic, and translates sentences in both directions.

📄 Role document: [EN](../docs/pdf/en/05_Speech_and_NLP_Engineer.pdf) · [AR](../docs/pdf/ar/05_Speech_and_NLP_Engineer.pdf)

## Delivers

| Output | Contract | Used by |
|---|---|---|
| Sentence generation (signs → Egyptian sentence) | C7 | Mobile |
| Understanding result (speech → intent + entities) | C8 | Mobile |
| Sign sequence for output (in sign-language order) | C9 | Mobile, Avatar |
| `intents.json`, `phrases.csv`, `sentence_templates.json`, `context_groups.json` | — | Mobile, ML |
| `audio/*.mp3` (Egyptian voice) | — | Mobile |

## Receives

Vocabulary (C1) from Data; speech text and recognised signs (C6) from Mobile.

## Layout

```
nlp/
├── normalize.py             # Egyptian text normalisation (+ Kotlin port for the app)
├── intents.json             # 30–50 clinic intents with many Egyptian paraphrases
├── phrases.csv              # phrase → sign sequence + sentence type
├── sentence_templates.json  # sign sequences → Egyptian / English sentences
├── engine/                  # understanding + sentence engine
├── asr_eval/                # recorded test sentences + WER script
└── tests/
```

Rule: only sign IDs that exist in `vocabulary.csv` may appear in any output.

## First two weeks

1. Record 20 clinic sentences from 3–4 Egyptian speakers; measure `ar-EG` WER on a phone.
2. Try an LLM on 10 sign sequences → Egyptian sentences; judge the quality.
3. Draft the intent list and agree C7–C9.
