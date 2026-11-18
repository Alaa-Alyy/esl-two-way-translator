<div class="cover" markdown="1">
<div class="kicker">وثيقة الدور 03</div>
<div class="title">Machine Learning Engineer</div>
<div class="subtitle">موديل إشارات بيشتغل مع أي حد، مش بس مع اللي اتدرب عليهم</div>
<div class="meta">
<div><b>المشروع:</b> تطبيق الترجمة الفورية في الاتجاهين للغة الإشارة المصرية</div>
<div><b>المسؤول:</b> ______________________</div>
<div><b>تتقري مع:</b> 00 — الوثيقة الرئيسية للمشروع</div>
<div><b>الإصدار:</b> 1.0 · نوفمبر 2026</div>
</div>
</div>

# 1. دورك في فقرة

انت **مخ الاتجاه الأول**. بتستلم features نضيفة من الـ Computer Vision وبتدرّب الموديل اللي بيتعرف على الإشارات. التصميم الأساسي بتاعك هو **sign encoder** بيحوّل كل إشارة لـ embedding ("بصمة")، والتعرف بيقارنها بـ prototypes متخزنة. التصميم ده لوحده بيدّي المشروع التعرف، ورفض الحركات اللي مش إشارات، والـ calibration الشخصي، وميزة "إشاراتي". بتقيس كل حاجة بـ Leave-One-Signer-Out وبتسلّم موديل `.tflite` صغير وسريع للموبايل.

# 2. المشروع باختصار

تطبيق أندرويد في الاتجاهين لمجال واحد (استقبال العيادة):

- **الاتجاه الأول:** الأصم يعمل جملة بالإشارة ← التطبيق يعرض جملة مصرية طبيعية وينطقها.
- **الاتجاه التاني:** السامع يتكلم مصري ← التطبيق يعرض النص وأفاتار 3D يعمل الجملة بشكل ناعم.
- التعرف بيشتغل على الموبايل من landmarks الـ MediaPipe. بنبدأ بـ **KArSL-502** (3 أشخاص) وننتقل للداتا المصرية بعدين؛ عدد الإشارات 50 ← حوالي 100.
- المستخدمين يقدروا يضيفوا إشارات شخصية فورًا ويشاركوها ("إشاراتي").

```
 Data (1) ──splits, vocabulary──> YOU (3)
 CV (2)   ──features [48,F], feature_spec, synthetic sentences──> YOU (3)
 YOU (3)  ──sign_encoder.tflite, prototypes.json, labels.json, thresholds.json──> Mobile (4)
 YOU (3)  ──results──> Data (1)
```

# 3. مسؤولياتك

**الـ Baselines**

- Random Forest / SVM على الـ features المفرودة عشان تتأكد إن الداتا سليمة (الأسبوع 2).
- GRU classifier بسيط كأول deep baseline.

**الـ Sign encoder (الموديل الأساسي)**

- تقارن بين architectures زمنية صغيرة: GRU بطبقتين، و1D-CNN/TCN، وTransformer encoder صغير.
- تدرّب بـ classification loss **و** metric-learning loss (زي ArcFace أو supervised contrastive أو prototypical) عشان embeddings نفس الإشارة تتجمع جنب بعض.
- الـ output: embedding بـ 128 رقم، L2-normalized.
- تعمل `prototypes.json`: prototype أو أكتر لكل إشارة (متوسط embeddings التدريب، وممكن كذا واحد للإشارة لو ليها أشكال مختلفة).
- التعرف = cosine similarity مع الـ prototypes؛ والـ confidence = similarity متظبطة / الفرق بين الأول والتاني.

**class الـ NONE (الرفض)**

- تدرّب بحركات مش إشارات: الانتقالات بين الإشارات، والراحة، وحك الوش، وتظبيط اللبس (من الفراغات في الداتا ومن negatives صناعية).
- تظبط هامش الرفض عشان الحركات العشوائية تترفض.

**Augmentation للأشخاص الجداد**

- تدوير وإزاحة وتكبير بسيط؛ وتغيير السرعة (time warping)؛ وnoise على المفاصل؛ وحذف فريمات؛ و**تغيير نسب الجسم** (طول الدراع، وعرض الكتاف، وحجم الإيد).
- تقيس تأثير كل augmentation على الـ LOSO.

**التقييم**

- LOSO على كل الـ folds: accuracy، وmacro-F1، وtop-3، وconfusion matrix، ونتيجة لكل إشارة، والمعروفين مقابل الجداد.
- تجربة عدد الإشارات: 50 / 100 / 200.
- تلاقي أزواج الإشارات اللي بتتلخبط وتبلّغ بيها (مفيدة للـ context-aware vocabulary والواجهة).

**العتبات والثقة**

- تختار عتبات `accept` و`ask`: فوق `accept` ← اعرض الإشارة؛ بينهم ← "قصدك...؟" بأقرب 3؛ تحت `ask` ← NONE.

**التعرف المتصل (Should)**

- تدرّب موديل تسلسل CTC على الجمل الصناعية من أداة الـ CV؛ وتقارنه بطريقة "قطّع وبعدين اتعرف".

**الـ Context-aware vocabulary (Should، مع الـ NLP 5 والـ Mobile 4)**

- تدعم حصر الـ prototypes المرشحة في مجموعة (مثلًا أجزاء الجسم) وقت التعرف؛ وتقيس مكسب الدقة.

**الـ Calibration الشخصي وإشاراتي (مع الـ Mobile 4)**

- الـ Calibration: من 2–3 تكرارات للمستخدم، تضيف prototypes خاصة بيه (أو تعدّل الموجودة).
- إشاراتي: من 5 تكرارات، تحسب prototype جديد؛ وفحص الثبات (التكرارات قريبة من بعض)؛ وفحص التعارض (قريبة جدًا من إشارة موجودة).
- سكريبت إعادة تدريب بيدمج الإشارات العامة المعتمدة (≥ 3 مساهمين) في الموديل.

**التصدير**

- التحويل لـ LiteRT `.tflite`؛ وquantization بـ float16 وint8؛ ومقارنة الدقة قبل وبعد؛ وقياس وقت التشغيل مع الـ Mobile.
- تكتب `model_card.md` لكل إصدار.

**Transfer learning (لما الداتا المصرية تيجي)**

- Pretrain على KArSL، وfine-tune على المصري؛ ومقارنة بالتدريب من الصفر؛ والتقييم على أشخاص مصريين بس.

# 4. الـ Inputs اللي بتستلمها

| الـ Input | من مين | الشكل | إمتى |
|---|---|---|---|
| الـ Features | CV (2) | C4 `[48, F]` float32 | الشهر 1 |
| `feature_spec.md` | CV (2) | spec بإصدار | الأسبوع 2 |
| الـ Landmarks الخام (للـ augmentation في 3D) | CV (2) | C3 | الشهر 1 |
| الـ Splits والـ vocabulary | Data (1) | `splits/`، C1 | الشهر 1 |
| الجمل الصناعية | CV (2) | تسلسلات + labels | الشهر 3 |
| التوقيت على الموبايل | Mobile (4) | تقرير | الشهر 2+ |
| مجموعات السياق (أنهي إشارات تناسب أنهي سؤال) | NLP (5) | JSON | الشهر 4 |

# 5. الـ Outputs اللي بتسلّمها

| الـ Output | الشكل | مين بيستخدمه | الميعاد |
|---|---|---|---|
| نتايج الـ Baseline | جدول في `results.md` | Data، التيم | الأسبوع 2 / الشهر 2 |
| `.tflite` وهمي بنفس شكل الـ input والـ output | C5 | Mobile | الشهر 1 |
| حزمة `models/v{N}/` (C5) | tflite + json + model card | Mobile | الشهر 2 (v1)، 3، 4 |
| `ml/train.py`، `ml/evaluate.py`، configs | كود | التيم | مستمر |
| مواصفات منطق الـ calibration وإشاراتي | وثيقة + Python مرجعي | Mobile | الشهر 4 |
| `ml/retrain_with_contributions.py` | سكريبت | Data | الشهر 5 |
| `docs/ml_report.md` | كل التجارب | الكتاب | الشهر 5 |

# 6. العقود اللي انت مسؤول عنها

**C5 — حزمة الموديل**

```
models/v{N}/sign_encoder.tflite   input  [1, 48, F] float32  (F from feature_spec v<k>)
                                  output [1, 128] float32, L2-normalized
models/v{N}/prototypes.json       {"S001": [[128 floats], ...], ..., "NONE": [[...]]}
models/v{N}/labels.json           ["S001", "S002", ...]
models/v{N}/thresholds.json       {"accept": 0.75, "ask": 0.45, "none_margin": 0.10}
models/v{N}/model_card.md         data version, feature spec version, LOSO results, date
```

**قاعدة التعرف (الـ Mobile بينفذها، وانت بتحددها)**

```
scores = cosine(embedding, every prototype of every allowed sign)
best   = max score per sign; sort
if best_1 is NONE or best_1 < ask:                 -> NONE (ignore)
elif best_1 >= accept and best_1 - best_2 >= margin -> accept best_1
else                                                -> "Did you mean?" top-3
```

اعمل تنفيذ مرجعي بـ Python (`ml/reference_recognizer.py`) عشان الـ Mobile يقارن بيه.

# 7. الأدوات والتكنولوجيا

| الغرض | الأدوات |
|---|---|
| الـ Framework | PyTorch (تصدير عن طريق ONNX ← LiteRT، أو ai-edge-torch) أو TensorFlow/Keras (LiteRT مباشرة)، اختار في الأسبوع الأول على أساس أسهل طريق للتصدير |
| ML تقليدي | scikit-learn |
| تتبع التجارب | Weights & Biases أو TensorBoard |
| الحوسبة | GPUs على Kaggle / Colab |
| المقاييس | scikit-learn، NumPy، matplotlib |
| التصدير | LiteRT converter، وأدوات الـ quantization |

نصيحة: لو محدش في التيم عنده خبرة قوية في تحويل PyTorch للموبايل، **TensorFlow/Keras أقصر طريق لـ `.tflite`**.

# 8. خطة الشغل خطوة بخطوة

**الأسبوع 1–2 (اختبار الافتراضات)**

1. baseline سريع على 20 إشارة بأي features موجودة (حتى الـ landmarks الخام): نتيجة LOSO.
2. اختار الـ framework على أساس طريق التصدير؛ وصدّر موديل وهمي وسلّمه للـ Mobile.
3. اتفق على C5 مع الـ Mobile.

**الشهر 1**

1. الـ Baselines (RF/SVM، GRU) على الـ 50 إشارة؛ وأول أرقام LOSO.
2. كود التدريب والتقييم بـ configs وتتبع تجارب.

**الشهر 2**

1. Sign encoder v1 بـ metric learning؛ والـ prototypes؛ والعتبات.
2. حزمة الموديل v1 للـ Mobile؛ وقارن الـ reference recognizer بنتايج الموبايل.

**الشهر 3**

1. دراسة الـ augmentation؛ وclass الـ NONE؛ ومقارنة الـ architectures.
2. الـ vocabulary ← حوالي 100 إشارة؛ وموديل v2.
3. ابدأ موديل CTC على الجمل الصناعية (Should).

**الشهر 4**

1. منطق الـ calibration وإشاراتي مع الـ Mobile.
2. الحصر حسب السياق مع الـ NLP؛ وقيس المكسب.
3. الـ Quantization؛ وموديل v3 للمنتج الكامل.

**الشهر 5**

1. تجربة عدد الإشارات (50/100/200)؛ والأزواج اللي بتتلخبط؛ والـ LOSO النهائي.
2. سكريبت إعادة التدريب بالمساهمات المعتمدة.
3. تجربة الـ transfer learning لو فيه داتا مصرية.

**الشهر 6**

1. ثبّت الموديل النهائي؛ واكتب فصل الـ ML.

# 9. أولوياتك

| الأولوية | البنود |
|---|---|
| Must | Baseline، وsign encoder + prototypes، وNONE، والعتبات، وتقييم LOSO، والتصدير لـ tflite |
| Should | دراسة الـ augmentation، وCTC على الجمل الصناعية، والحصر حسب السياق، ومنطق إشاراتي |
| Could | الـ Calibration، ومنحنى عدد الإشارات، وتجربة الـ transfer learning |

# 10. إمتى تعتبر خلصت

- الموديل شغال على الموبايل وبيدّي نفس توقعات الـ Python المرجعي.
- نتايج LOSO (المعروفين مقابل الجداد) متسجلة للموديل النهائي.
- الحركات العشوائية اللي مش إشارات بتترفض في اختبار لايف.
- كل نتيجة ممكن تتعاد من config، وإصدار داتا، وإصدار feature spec.

# 11. بتشتغل مع مين

| الدور | بتتبادلوا إيه | إمتى |
|---|---|---|
| CV (2) | الـ Features، والـ spec، والجمل الصناعية | أسبوعيًا |
| Data (1) | Splits داخلة، ونتايج طالعة | كل تجربة |
| Mobile (4) | حزمة الموديل، وقاعدة التعرف، والتوقيت | كل إصدار موديل |
| NLP (5) | مجموعات السياق؛ وتسلسلات الإشارات المتعرف عليها | الشهر 4 |

# 12. أخطاء لازم تتجنبها

- **تقدّم دقة التدريب أو random split** كنتيجة. الـ LOSO بس هو اللي بيتحسب.
- **موديل كبير جدًا** على الداتا: مع 3 أشخاص، الموديلات الصغيرة بتعمّم أحسن.
- **قلب شمال ويمين كـ augmentation** من غير ما تتأكد: بعض الإشارات معناها بيتغير. الأحسن قلب اليد المسيطرة بتاع الـ CV.
- **تغيير شكل الـ input** من غير ما تحدّث C5 وتبلّغ الـ Mobile.
- **نزول الدقة بعد الـ quantization** من غير ما يتقاس.

# 13. الشغل مع أداة AI

```
I am the Machine Learning Engineer on a two-way Egyptian Sign Language app
(see attached documents). Input features are [48, F] float32 (contract C4).
The model package must follow contract C5: an encoder producing a 128-d
L2-normalized embedding, with prototypes and thresholds. Evaluation is
Leave-One-Signer-Out only. Write <task>.
```

# 14. الفصل بتاعك في الكتاب

تصميم الموديل (encoder + prototypes)، والـ loss functions، وclass الـ NONE، والـ augmentation، ونتايج LOSO، والمعروفين مقابل الجداد، ومنحنى عدد الإشارات، واللخبطة بين الإشارات، وموديل التسلسل، والـ calibration وإشاراتي، والـ quantization والأداء على الموبايل.
