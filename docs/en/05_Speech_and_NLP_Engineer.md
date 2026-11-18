<div class="cover" markdown="1">
<div class="kicker">ROLE DOCUMENT 05</div>
<div class="title">Speech & NLP Engineer</div>
<div class="subtitle">The app hears, understands, and speaks Egyptian Arabic, and translates sentences in both directions</div>
<div class="meta">
<div><b>Project:</b> Two-Way Egyptian Sign Language Translation App</div>
<div><b>Owner:</b> ______________________</div>
<div><b>Read with:</b> 00 — Project Master Document</div>
<div><b>Version:</b> 1.0 · November 2026</div>
</div>
</div>

# 1. Your role in one paragraph

You own **language** in the project. In direction 2 you turn Egyptian Arabic speech into text, understand its meaning, and convert it into a sign sequence in sign-language order for the avatar. In direction 1 you turn the recognized sequence of signs into a natural Egyptian Arabic sentence and give it a voice. Sign language has its own grammar, so neither direction is word-for-word: your layer is what makes the app translate **sentences**, not words.

# 2. The project in brief

A two-way Android app for one domain (clinic reception):

- **Direction 1:** a Deaf person signs a sentence → the app shows a natural Egyptian Arabic sentence and speaks it.
- **Direction 2:** a hearing person speaks Egyptian Arabic → the app shows the text and a 3D avatar signs the sentence smoothly.
- Signs are identified by IDs (`S001`…) in `vocabulary.csv`; Egyptian Arabic, MSA, and English are just columns.
- We start with KArSL signs (Unified Arabic Sign Language) and move to Egyptian Sign Language later. The **hearing side is Egyptian from day one** — that is your part.

```
 Data (1)   ──vocabulary.csv──> YOU (5)
 Mobile (4) ──speech text, recognized signs (C6)──> YOU (5)
 YOU (5)    ──understanding (C8), sign sequence (C9), sentence (C7), audio──> Mobile (4)
 YOU (5)    ──sign sequences + sentence types (C9)──> Avatar (6)
 YOU (5)    ──context groups (which signs fit which question)──> ML (3)
```

# 3. Your responsibilities

**Speech recognition (ASR)**

- Use Android SpeechRecognizer with locale `ar-EG` as the primary engine (with Mobile).
- Record a test set of clinic sentences from several Egyptian speakers, in quiet and noisy rooms; measure word error rate (WER) with jiwer.
- Compare with Whisper models fine-tuned on Egyptian Arabic (server/Colab) as a research comparison.

**Text normalization**

- Rules for Egyptian text: أ/إ/آ → ا, ة/ه, ى/ي, removing diacritics and elongation (ـ), numbers in words and digits, filler words (يعني، اه، طيب).
- Python version for development and a Kotlin (or shared) version for the app.

**Domain language design**

- Define **30–50 intents** for clinic reception (ASK_DURATION, ASK_PAIN_LOCATION, ASK_ALLERGY, BOOK_APPOINTMENT, ASK_ID_CARD, GIVE_PRESCRIPTION, REQUEST_WAIT, …).
- Define entities: BODY_PART, SYMPTOM, SEVERITY, TIME, DAY, NUMBER, NAME.
- Collect **many Egyptian paraphrases per intent** (aim 15–30): «من امتى؟»، «بقالك قد ايه؟»، «الموضوع ده من امتى؟».
- Quick-question buttons for the hearing person (the most common 10–15 questions).

**Understanding engine (direction 2)**

- Intent matching: rapidfuzz + sentence embeddings (multilingual or Arabic models); optional fine-tuned Arabic classifier.
- Entity extraction: dictionaries of Egyptian words per entity + fuzzy matching.
- Output C8 with confidence and 3 alternatives.

**Sign ordering (direction 2)**

- `phrases.csv`: for each phrase, the sign sequence in sign-language order and the sentence type (statement, yes/no question, wh-question, negation).
- Templates with entity slots: `ASK_DURATION(SYMPTOM=x)` → `[x] [HOW-LONG]` + wh-question face.
- Names and unknown words → fingerspelling list; out-of-domain → "not supported". Never invent signs.
- Optional LLM conversion of free text to sign IDs, restricted to the vocabulary, with validation that every output ID exists.
- Get sign orders reviewed by an Egyptian interpreter when possible.

**Sentence generation (direction 1)**

- Templates that turn sign sequences into natural Egyptian Arabic: `[ME] [HEADACHE] [FEVER] [YESTERDAY]` → «عندي صداع وسخونية من امبارح», plus English.
- Optional LLM rewrite (online) with strict rules: use only the meaning of the given signs, add nothing, keep Egyptian dialect; template fallback offline.
- Output C7.

**Voice**

- Pre-generate Egyptian Arabic audio for all fixed phrases and template outputs where possible (e.g. Azure `ar-EG` voices); Android TTS for dynamic sentences.

**Context groups (with ML and Mobile)**

- For each question intent, list the sign categories expected in the answer (ASK_PAIN_LOCATION → body parts). Used for context-aware vocabulary.

# 4. Inputs you receive

| Input | From | Format | When |
|---|---|---|---|
| Vocabulary | Data (1) | C1 | Week 2 / Month 3 |
| Speech text | Mobile (4) | String from SpeechRecognizer | Month 2 |
| Recognized signs | Mobile (4) | C6 | Month 3 |
| Interpreter review of sign orders | Interpreter (via Data 1) | Notes | Months 3–5 |
| Avatar needs (sentence types, timing) | Avatar (6) | Discussion | Month 3 |

# 5. Outputs you deliver

| Output | Format | Used by | Due |
|---|---|---|---|
| ASR test set + WER results | Audio + transcripts + table | Report | Month 1–2 |
| `nlp/normalize` (Python + Kotlin) | Code | Mobile | Month 2 |
| `nlp/intents.json` | Intents, paraphrases, entities | Team | Month 1 (v1) |
| `nlp/phrases.csv` | Phrase → sign sequence + sentence type | Mobile, Avatar | Month 2 (v1), Month 3 |
| `nlp/sentence_templates.json` | Signs → Egyptian/English sentences | Mobile | Month 3 |
| Understanding + sentence engine | Kotlin library (preferred, offline) or FastAPI service | Mobile | Months 2–4 |
| `audio/*.mp3` | Egyptian voice files | Mobile | Month 3 |
| `nlp/context_groups.json` | Intent → expected sign categories | ML, Mobile | Month 4 |
| `docs/nlp_report.md` | WER, intent accuracy, F1, entity P/R, sentence ratings | Report | Month 5 |

# 6. Contracts you own

**C7 — sentence generation (direction 1)**

```json
input : {"signs": ["S100","S045","S046","S120"], "context": null}
output: {"text_ar_eg": "عندي صداع وسخونية من امبارح",
         "text_en": "I have had a headache and fever since yesterday",
         "audio_file": null, "method": "template", "confidence": 0.86}
```

**C8 — understanding (direction 2)**

```json
{"text": "بقالك قد ايه عندك السخونية دي؟", "intent": "ASK_DURATION",
 "entities": {"SYMPTOM": "FEVER"}, "phrase_id": "P017", "confidence": 0.82,
 "alternatives": ["P018", "P020"]}
```

**C9 — sign sequence for output**

```json
{"phrase_id": "P017", "signs": ["S046", "S090"], "sentence_type": "wh_question",
 "fingerspell": [], "text_ar_eg": "بقالك قد ايه عندك السخونية؟"}
```

`sentence_type` values: `statement`, `yes_no_question`, `wh_question`, `negation`, `command`, `emergency`.

**`phrases.csv`**

```
phrase_id,intent,template_signs,sentence_type,text_ar_eg_template,text_en_template,verified
P017,ASK_DURATION,{SYMPTOM} S090,wh_question,بقالك قد ايه عندك {SYMPTOM}؟,How long have you had {SYMPTOM}?,no
```

# 7. Tools and technologies

| Purpose | Tools |
|---|---|
| ASR | Android SpeechRecognizer (`ar-EG`); Whisper / faster-whisper with Egyptian fine-tunes from Hugging Face |
| Metrics | jiwer (WER), scikit-learn (accuracy, F1) |
| Normalization | PyArabic, CAMeL Tools, custom rules |
| Matching | rapidfuzz, sentence-transformers (multilingual / Arabic models) |
| Optional models | Fine-tuned MARBERT / CAMeLBERT classifier; an LLM API for sentence rewriting |
| Voice | Azure Speech `ar-EG` voices (pre-generated), Android TextToSpeech |
| Backend (optional) | FastAPI |

Design preference: **the core engine runs offline on the phone** (rules + fuzzy matching + small embeddings or precomputed vectors). LLM and Whisper are online extras.

# 8. Step-by-step work plan

**Weeks 1–2 (feasibility spike)**

1. Record 20 clinic sentences from 3–4 Egyptian speakers; measure `ar-EG` WER on the phone.
2. Try an LLM on 10 sign sequences → Egyptian sentences; judge quality.
3. Draft the intent list and agree C7–C9.

**Month 1**

1. `intents.json` v1 (30–50 intents, first paraphrases, entities).
2. Quick-question list with Mobile.
3. Full ASR test set; WER table (quiet vs noisy).

**Month 2**

1. Normalization (Python + Kotlin).
2. Understanding engine v1 (intent + entities) → C8; first `phrases.csv` → C9.
3. Deliver to Mobile for the first direction 2 screen.

**Month 3**

1. Sentence templates for direction 1 → C7; integration with recognized signs.
2. Audio generation for fixed phrases.
3. Sentence types for the avatar's facial grammar (with Avatar 6).

**Month 4**

1. Paraphrase robustness: expand to 15–30 paraphrases per intent; test set of unseen paraphrases.
2. Context groups for context-aware vocabulary.
3. Optional LLM layer with template fallback.

**Month 5**

1. Evaluation: WER, intent accuracy, macro-F1, entity P/R, sentence naturalness ratings by Egyptian speakers.
2. Whisper comparison.
3. `nlp_report.md`.

**Month 6**

1. Freeze; write the language chapter.

# 9. Your priorities

| Priority | Items |
|---|---|
| Must | ASR integration, normalization, intents + entities, understanding engine, phrases with sign order, sentence templates, voice |
| Should | Paraphrase robustness set, context groups, sentence types for the avatar, quick-question buttons |
| Could | LLM rewriting, Whisper comparison, fine-tuned Arabic classifier |

# 10. Definition of done

- Any normal Egyptian way of asking a supported clinic question is understood correctly or answered with "Did you mean?".
- Every recognized sign sequence in the domain produces a natural Egyptian sentence and audio.
- No output ever contains a sign ID that is not in the vocabulary.
- Works offline (LLM/Whisper only as online extras).

# 11. Who you work with

| Role | What you exchange | Sync point |
|---|---|---|
| Mobile (4) | Engine integration, audio, quick buttons | Months 2–4 |
| Avatar (6) | Sign sequences, sentence types, fingerspelling | Month 3 |
| ML (3) | Context groups | Month 4 |
| Data (1) | Vocabulary words; interpreter review | Months 1, 3–5 |

# 12. Pitfalls to avoid

- **Word-for-word mapping** Arabic → signs. Always go through meaning (intent + entities) and sign-language order.
- **Testing only on sentences you wrote yourself.** Collect paraphrases from other people.
- **Writing MSA** instead of Egyptian in outputs.
- **LLM adding information** ("since yesterday" when no time sign exists). Validate every output.
- **Depending on internet** for the core flow.

# 13. Working with an AI tool

```
I am the Speech & NLP Engineer on a two-way Egyptian Sign Language app
(see attached documents). Hearing-side language is Egyptian Arabic (ar-EG).
Outputs follow contracts C7 (signs -> Egyptian sentence), C8 (understanding),
C9 (sign sequence in sign-language order). Only sign IDs from vocabulary.csv
may appear. Write <task>.
```

# 14. Your report chapter

Egyptian Arabic challenges, ASR choice and WER, normalization, intent and entity design, paraphrase robustness, sign ordering and sentence types, sentence generation in both directions, voice, and evaluation results.
