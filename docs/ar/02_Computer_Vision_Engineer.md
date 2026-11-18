<div class="cover" markdown="1">
<div class="kicker">وثيقة الدور 02</div>
<div class="title">Computer Vision Engineer</div>
<div class="subtitle">تحويل الفيديو لـ features نضيفة، نفس الحاجة بالظبط في Python وعلى الموبايل</div>
<div class="meta">
<div><b>المشروع:</b> تطبيق الترجمة الفورية في الاتجاهين للغة الإشارة المصرية</div>
<div><b>المسؤول:</b> ______________________</div>
<div><b>تتقري مع:</b> 00 — الوثيقة الرئيسية للمشروع</div>
<div><b>الإصدار:</b> 1.0 · نوفمبر 2026</div>
</div>
</div>

# 1. دورك في فقرة

انت **عين النظام**. بتاخد فريمات الفيديو وتحولها لأرقام نضيفة ومعمولها normalization بتوصف الجسم والإيدين والوش على مدار الوقت. وبتعمل ده مرتين: في Python للتدريب، وفي Kotlin على الموبايل للاستخدام الحقيقي، وبتثبت إن الاتنين بيطلعوا نفس النتيجة. وكمان بتحدد كل إشارة بتبدأ وبتخلص فين في الحركة اللايف، وبتفحص جودة الصورة، وبتساعد الأفاتار وتوليد الجمل بأدوات الـ landmarks بتاعتك.

# 2. المشروع باختصار

تطبيق أندرويد في الاتجاهين لمجال واحد (استقبال العيادة):

- **الاتجاه الأول:** الأصم يعمل جملة بالإشارة ← التطبيق يعرض جملة مصرية طبيعية وينطقها.
- **الاتجاه التاني:** السامع يتكلم مصري ← التطبيق يعرض النص وأفاتار 3D يعمل الجملة بشكل ناعم.
- النظام **vision-based وبيعتمد على pose estimation**: موديلات MediaPipe بتلاقي النقط، وبعدين موديل زمني بيتعرف على الإشارة.
- بنبدأ بـ **KArSL-502** (3 أشخاص) وننتقل للداتا المصرية بعدين؛ عدد الإشارات 50 ← حوالي 100.

```
 Data (1) ──clips──> YOU (2) ──landmarks/raw, features/, feature_spec.md──> ML (3)
                     YOU (2) ──Normalizer.kt, SignSegmenter.kt, QualityChecker.kt──> Mobile (4)
                     YOU (2) ──clean landmarks of best takes, smoothing tools──> Avatar (6)
 Mobile (4) ──camera frames──> YOUR on-device pipeline
```

# 3. مسؤولياتك

**استخراج الـ Landmarks (Python)**

- تشغّل MediaPipe Tasks: **Hand Landmarker، وPose Landmarker، وFace Landmarker** على كل كليب (video mode، بـ timestamps).
- تخزّن الـ output الخام لكل كليب (العقد C3)، ومعاه الـ 52 face blendshape.
- تختار النقط اللي هتتحفظ: الجزء العلوي من الجسم، و21 نقطة لكل إيد، وحوالي 40 نقطة للوش (الحواجب، والعين، والفم).
- تطلّع إحصائيات لكل كليب: نسبة ظهور الإيد، والفريمات الناقصة ← flags جودة للـ Data (1).
- استخراج بالجملة يشتغل على Kaggle/Colab ويقدر يكمّل لو وقف.

**هندسة الـ Features**

- الـ Normalization: الصفر في نص الكتفين، والقسمة على عرض الكتفين؛ ونقط الإيد كمان بالنسبة للرسغ؛ وقلب الأعسر.
- الإيد المش ظاهرة: ملء الفراغات القصيرة (≤ 5 فريمات)؛ وغير كده أصفار + flag.
- تحويل كل إشارة لـ 48 فريم؛ وإضافة السرعة (الفروق بين الفريمات).
- تكتب `feature_spec.md`: ترتيب كل رقم بالظبط، ومعادلته، ورقم إصدار.

**الرؤية على الموبايل (Kotlin)**

- تشغّل MediaPipe Tasks على أندرويد في live-stream mode على فريمات الكاميرا من الـ Mobile (4).
- تنقل الـ normalization لـ `Normalizer.kt` **سطر بسطر** من `normalize.py`.
- **Golden test:** لـ 20 كليب مرجعي، features الـ Python والـ Kotlin لازم يتطابقوا (أقصى فرق أقل من 1e-3). وتضيفه للـ CI.
- تقيس الـ fps على موبايل متوسط؛ ولو بطيء، تشغّل الوش كل N فريم أو تقلل الدقة.

**التقطيع**

- `SignSegmenter.kt`: motion gate على أساس مكان وسرعة الرسغ، يبدأ لما الإيد تخرج من منطقة الراحة، ويخلص لما ترجع.
- جوه الجمل: التقسيم عند الوقفات القصيرة وأقل سرعة.
- sliding window كبديل للي مش بيقف.
- تظبط العتبات على كليبات KArSL متوصلة ببعض وعلى تجارب لايف.

**فحص الجودة وإطار التوجيه**

- `QualityChecker.kt`: الإضاءة، والاهتزاز، والشخص في الكادر، والمسافة (عرض الكتفين بالـ pixels)، والإيدين ظاهرين.
- يرجّع رسايل بسيطة للواجهة: `MOVE_CLOSER`، `MOVE_BACK`، `MORE_LIGHT`، `HANDS_NOT_VISIBLE`، `OK`.

**مساعدة الأدوار التانية**

- **جمل صناعية (مع الـ ML 3):** أداة بتوصّل landmarks إشارات منفصلة بانتقالات ناعمة عشان تعمل داتا جمل للتدريب.
- **الأفاتار (مع 6):** فلاتر smoothing (زي One Euro filter)، وقص قلب الإشارة (شيل وضع الراحة في الأول والآخر)، واختيار أحسن تكرار لكل إشارة.

**Pixel baseline (Could)**

- CNN صغير (أو CNN + GRU) على الفريمات، يتقيّم بنفس الـ LOSO splits، للمقارنة مع الـ landmarks.

# 4. الـ Inputs اللي بتستلمها

| الـ Input | من مين | الشكل | إمتى |
|---|---|---|---|
| الكليبات المتنظمة + الـ metadata | Data (1) | C2 | الشهر 1 |
| الـ LOSO splits | Data (1) | `splits/*.json` | الشهر 1 |
| فريمات الكاميرا على الموبايل | Mobile (4) | CameraX `ImageProxy` | الشهر 1–2 |
| احتياجات features (مثلًا features زيادة) | ML (3) | Issue / نقاش | مستمر |
| احتياجات الحركة | Avatar (6) | Issue / نقاش | الشهر 1–3 |

# 5. الـ Outputs اللي بتسلّمها

| الـ Output | الشكل | مين بيستخدمه | الميعاد |
|---|---|---|---|
| `cv/extract_landmarks.py` | سكريبت Python | انت، والـ Data | الشهر 1 |
| `landmarks/raw/{clip_id}.npz` (C3) | ملفات NumPy | ML، Avatar | الشهر 1 |
| `cv/normalize.py` + `features/{clip_id}.npy` (C4) | Python + `[48, F]` float32 | ML | الشهر 1 |
| `docs/feature_spec.md` | spec بإصدار | ML، Mobile | الأسبوع 2 |
| flags الجودة | CSV للـ Data | Data | الشهر 1 |
| `Normalizer.kt` + wrapper لـ MediaPipe على أندرويد | Kotlin module | Mobile | الشهر 2 |
| Golden test + CI job | سكريبت test + ملفات مرجعية | الكل | الشهر 2 |
| `SignSegmenter.kt` | Kotlin module | Mobile | الشهر 3 |
| `QualityChecker.kt` | Kotlin module | Mobile | الشهر 3 |
| `cv/synthetic_sentences.py` | أداة Python | ML | الشهر 3 |
| أدوات الـ smoothing والقص | Python | Avatar | الشهر 2 |
| `docs/cv_report.md` | الـ fps، والـ golden test، ودقة التقطيع، وpixels مقابل landmarks | الكتاب | الشهر 5 |

# 6. العقود اللي انت مسؤول عنها

**C3 — الـ landmarks الخام:** `landmarks/raw/{clip_id}.npz`

```
pose        (T, 33, 4)  x, y, z, visibility   (normalized image coords from MediaPipe)
left_hand   (T, 21, 3)
right_hand  (T, 21, 3)
face        (T, 40, 3)  selected indices listed in feature_spec.md
blendshapes (T, 52)
mask_left   (T,)  1 if detected
mask_right  (T,)
fps         scalar
```

**C4 — الـ features:** `features/{clip_id}.npy`، float32، شكله `[48, F]`. الـ `feature_spec.md` لازم يحدد لكل عمود: النقطة المصدر، والمحور، والتحويل، وإصدار الـ spec. أي تغيير ← إصدار جديد + تبلّغ الـ ML والـ Mobile.

**واجهة الموبايل (متفق عليها مع الـ Mobile)**

```kotlin
interface VisionPipeline {
    fun process(frame: ImageProxy, timestampMs: Long): FrameLandmarks
}
object Normalizer { fun toFeatures(window: List<FrameLandmarks>): FloatArray /* 48*F */ }
class SignSegmenter { fun push(f: FrameLandmarks): SegmentEvent? /* START, END(segment) */ }
object QualityChecker { fun check(frame: ImageProxy, f: FrameLandmarks): QualityStatus }
```

# 7. الأدوات والتكنولوجيا

| الغرض | الأدوات |
|---|---|
| الـ Landmarks | MediaPipe Tasks (Python وAndroid)، بنفس إصدارات الموديلات في الاتنين |
| الصور والفيديو | OpenCV، FFmpeg |
| الرياضيات | NumPy، SciPy (interpolation، فلاتر) |
| أندرويد | Kotlin، Android Studio، MediaPipe Tasks Vision for Android |
| الحوسبة | Kaggle / Colab للاستخراج بالجملة |
| الاختبار | pytest، JUnit، GitHub Actions |
| Pixel baseline | PyTorch أو TensorFlow |

**مهم:** اكتب إصدار MediaPipe بالظبط وملفات موديلات الـ `.task` في `feature_spec.md`؛ والـ Python والأندرويد لازم يستخدموا نفسهم.

# 8. خطة الشغل خطوة بخطوة

**الأسبوع 1–2 (اختبار الافتراضات)**

1. شغّل Hand + Pose + Face مع بعض على موبايل أندرويد متوسط؛ وقيس الـ fps. وبلّغ التيم.
2. شغّل الاستخراج على 10 كليبات من KArSL؛ وارسم الـ landmarks على الفيديو عشان تتأكد من الجودة.
3. اكتب مسودة `feature_spec.md` v1 واتفق عليها مع الـ ML والـ Mobile.

**الشهر 1**

1. استخراج بالجملة للـ 50 إشارة؛ وطلّع ملفات C3 وflags الجودة.
2. `normalize.py` وfeatures الـ C4؛ وسلّمها للـ ML.
3. ساعد الـ Mobile يعرض الـ landmarks لايف على الكاميرا (milestone).

**الشهر 2**

1. `Normalizer.kt` + wrapper لـ MediaPipe على أندرويد.
2. Golden test على 20 كليب؛ وضيفه للـ CI.
3. أدوات الـ smoothing والقص للأفاتار.

**الشهر 3**

1. `SignSegmenter.kt`، متظبط على كليبات KArSL متوصلة وعلى إشارة لايف.
2. `QualityChecker.kt` ورسايل التوجيه.
3. `synthetic_sentences.py` مع الـ ML.
4. الاستخراج للـ vocabulary الأكبر (حوالي 100 إشارة).

**الشهر 4**

1. تحسين الأداء على الموبايل (الـ fps، والتأخير، والذاكرة).
2. دعم ربط الاتجاهين.

**الشهر 5**

1. Pixel baseline والمقارنة (Could).
2. قياس دقة التقطيع؛ و`cv_report.md`.

**الشهر 6**

1. التجميد؛ وكتابة فصل الرؤية.

# 9. أولوياتك

| الأولوية | البنود |
|---|---|
| Must | الاستخراج، والـ normalization، والـ feature spec، والنقل لـ Kotlin، والـ golden test، والتقطيع |
| Should | أداة الجمل الصناعية، وأدوات الـ smoothing والقص للأفاتار، وفحص الجودة |
| Could | مقارنة الـ pixel baseline |

# 10. إمتى تعتبر خلصت

- features الـ Python والموبايل متطابقة في الـ golden test (في الـ CI، وأخضر).
- الموبايل بيطلّع features لايف بسرعة مناسبة (الهدف ≥ 15 fps معالجة) على جهاز متوسط.
- الـ segmenter بيقطّع الإشارات صح في التسلسلات المتوصلة والتجارب اللايف (والدقة متسجلة).
- `feature_spec.md` كامل لدرجة إن حد تاني يقدر يعيد تنفيذه.

# 11. بتشتغل مع مين

| الدور | بتتبادلوا إيه | إمتى |
|---|---|---|
| Data (1) | كليبات داخلة، وflags جودة طالعة | الشهر 1 |
| ML (3) | الـ features، والـ spec، والجمل الصناعية | أسبوعيًا |
| Mobile (4) | الـ Kotlin modules، وفريمات الكاميرا، والأداء | أسبوعيًا من الشهر 2 |
| Avatar (6) | landmarks نضيفة، وsmoothing، وقص | الشهر 1–3 (انت أكتر حد بيساعدهم في الفترة دي) |

# 12. أخطاء لازم تتجنبها

- **اختلاف التدريب عن الموبايل:** إصدارات MediaPipe مختلفة، أو اتجاه الصورة، أو المراية بين Python والموبايل. الكاميرا الأمامية معكوسة، فقرر وسجّل هتتعامل معاها إزاي.
- **إحداثيات الصورة مقابل إحداثيات العالم:** استخدم نوع واحد بثبات، واكتبه.
- **تغيير الـ features من غير رقم إصدار جديد** بيبوّظ موديلات الـ ML من غير ما حد ياخد باله.
- **القسمة على عرض كتفين بصفر** (الشخص جزء منه برا الكادر) ← احمي من القسمة على صفر.
- **افتراض إن شمال ويمين بتوع MediaPipe** هما شمال ويمين الشخص: اتأكد مع مراية الكاميرا.

# 13. الشغل مع أداة AI

```
I am the Computer Vision Engineer on a two-way Egyptian Sign Language app
(see attached documents). Raw landmarks follow contract C3 and features follow
contract C4 / feature_spec.md v<N>. Write <task>. The Python and Kotlin versions
must produce identical numbers; keep the exact feature order from the spec.
```

# 14. الفصل بتاعك في الكتاب

ليه الـ landmarks، وإعداد MediaPipe، وتصميم الـ features والـ normalization، والتطابق بين التدريب والموبايل والـ golden test، والتقطيع، وفحص الجودة، والأداء على الموبايل، ومقارنة الـ pixels بالـ landmarks.
