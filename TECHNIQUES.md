# Video Techniques — دليل التقنيات (مفتوحة المصدر ومجانية فقط)

كل تقنية هنا مجانية ومفتوحة المصدر (أو مجانية الاستعمال)، بدون اشتراكات وبدون
دفع. العمود «أين تشتغل» يوضح هل تعمل على GitHub Actions (سحاب CPU) أو تحتاج
GPU مجاني (Google Colab / Kaggle) أو تعمل محلياً.

## 1. إنسان واقعي يتكلم (Talking Head)

| التقنية | ماذا تفعل | أين تشتغل | الرخصة | الحالة |
|---|---|---|---|---|
| **SadTalker** | صورة بورتريه + صوت → فيديو إنسان واقعي يتكلم (حركة رأس، ملامح، غمزات) | Colab T4 GPU | Apache 2.0 | ✅ دفتر جاهز: `colab/SadTalker_Talking_Head.ipynb` — اختبار قيد التشغيل |
| **LivePortrait** | تحريك صورة من فيديو قيادي — جودة أعلى وحفظ أفضل للهوية | Colab T4 GPU | **MIT** (مؤكدة من LICENSE؛ المستودع انتقل إلى `KlingAIResearch/LivePortrait`) | 📋 موثّقة — التفاصيل في §9.3 (أوزان `KlingTeam/LivePortrait`؛ Colab أولاً ثم Docker) |
| **Wav2Lip** | أدق مزامنة شفاه — إعادة دبلجة فيديو موجود بصوت جديد | Colab T4 GPU | غير تجاري فقط | 📋 موثّقة |
| **MuseTalk** | رأس متكلم شبه فوري (8GB+ VRAM) | Colab T4 GPU | مفتوح المصدر | 📋 موثّقة |
| **LatentSync / InfiniteTalk** | مزامنة شفاه وحركة رأس+جسم لمقاطع طويلة | Colab/Kaggle GPU | Apache 2.0 | 📋 موثّقة |

## 2. توليد فيديو بالذكاء الاصطناعي

| التقنية | ماذا تفعل | أين تشتغل | الرخصة | الحالة |
|---|---|---|---|---|
| **Wan 2.1 / 2.2** | نص/صورة → فيديو؛ نسخة 1.3B تعمل على T4 | Colab T4 / Kaggle | Apache 2.0 | 📋 دفتر جاهز: `colab/Wan21_Test.ipynb` (UNTESTED) — المساحة الرسمية معطّلة (RUNTIME_ERROR) 2026-11-08، Colab هو الطريق (§9.2) |
| **HunyuanVideo** | أفضل حركة بشرية وثبات وجه — يحتاج 24GB+ | Kaggle / Colab Pro | مفتوح المصدر | 📋 موثّقة |
| **LTX-Video** | توليد فيديو سريع ومناسب لـ T4 | Colab T4 | مفتوح المصدر | 📋 موثّقة |
| **CogVideoX 5B** | نص → فيديو، نسخة مكمّمة تعمل على Colab المجاني (~30 دقيقة للمقطع) | Colab T4 | Apache 2.0 | 📋 موثّقة |
| **FLUX.1** | صور واقعية / أوراق شخصيات (للشخصيات قبل تحريكها) | Colab T4 | مفتوح المصدر | 📋 موثّقة |

## 3. تحسين الفيديو: تكبير + تنعيم حركة

| التقنية | ماذا تفعل | أين تشتغل | الرخصة | الحالة |
|---|---|---|---|---|
| **Video2X** | الكل في واحد: تكبير Real-ESRGAN / Real-CUGAN / Anime4K + استيفاء إطارات RIFE | GPU Vulkan (محلي أو Colab) | AGPL-3.0 | 📋 دفتر جاهز: `colab/Video2X_Upscale.ipynb` (UNTESTED) — 6.4.0 AppImage لينكس 220 MB؛ مسار Colab هو pip Real-ESRGAN (§9.2) |
| **Real-ESRGAN** | تكبير AI حتى 4x — النموذج المرجعي الذي تستعمله أغلب الأدوات | GPU Vulkan / CPU بطيء | BSD-3-Clause | 📋 دفتر جاهز: `colab/Video2X_Upscale.ipynb` (UNTESTED) — PyPI 0.3.0 + وزن x4plus (§9.2) |
| **RIFE / Flowframes** | توليد إطارات وسيطة — 24fps ← 60fps أو حركة بطيئة ناعمة | GPU Vulkan | مفتوح المصدر | 📋 موثّقة |
| **REAL-Video-Enhancer** | واجهة خفيفة تجمع Real-ESRGAN + RIFE | Windows/Mac/Linux | مفتوح المصدر | 📋 موثّقة |
| **Upscayl** | تكبير صور حتى 16x (للبورتريهات والخلفيات قبل التركيب) | GPU Vulkan | مفتوح المصدر | 📋 موثّقة |

## 4. لقطات وصور وموسيقى مجانية (بدون مفتاح)

| المصدر | ماذا يعطي | المفتاح | الرخصة | الحالة |
|---|---|---|---|---|
| **Openverse API** (`api.openverse.org`) | 800M+ صورة وصوت برخص مفتوحة | **لا يحتاج مفتاحاً** | CC0 / CC BY | ✅ سكربت جاهز: `scripts/fetch_stock.py` — مجرّب ويعمل |
| **Pexels / Mixkit / Coverr** | فيديوهات بشر حقيقيين | تنزيل مباشر من الموقع، بلا API | Pexels/Mixkit License (تجاري مسموح) | 📋 موثّقة |
| **Pixabay API** | فيديو + صور + موسيقى + مؤثرات | مفتاح مجاني بالتسجيل بالبريد | تجاري مسموح، بلا نسبة | ⏳ الربط معلّق على تسجيل الدخول |
| **Unsplash API** | صور فقط | مفتاح مجاني بالتسجيل بالبريد | Unsplash License | ⏳ الربط معلّق على تسجيل الدخول |
| **Internet Archive** | لقطات تاريخية مجال عام | لا يحتاج مفتاحاً | مجال عام (حسب العنصر) | 📋 موثّقة |

> ملاحظة: Pexels أوقفت إصدار مفاتيح API جديدة منذ أكتوبر 2026 — التنزيل
> المباشر من الموقع هو البديل.

## 5. خط الإنتاج السحابي (موجود في هذا المستودع)

| التقنية | ماذا تفعل | أين تشتغل | الحالة |
|---|---|---|---|
| **Blender** (Cycles CPU) | مشاهد 3D — افتتاحيات، عناوين ذهبية، كاميرا متحركة | GitHub Actions | ✅ مجرّب — فيديو اختبار ناجح |
| **Manim Community** | رسوم متحركة برمجية (محرك 3Blue1Brown) | GitHub Actions | ✅ مجرّب — فيديو اختبار ناجح |
| **faster-whisper** | تحويل الكلام إلى ترجمة SRT (عربي + 99 لغة) | GitHub Actions | ✅ مجرّب — ترجمة صحيحة |
| **Piper TTS (kareem)** | تعليق صوتي عربي طبيعي — يعمل محلياً وعلى Actions | GitHub Actions | ✅ مستعمل في أفلام «الجزائر» و«الوقت» |
| **FFmpeg** | تجميع، تدرج لوني (LUT)، قص على الإيقاع، J/L cuts، ترجمة محروقة | GitHub Actions | ✅ مستعمل في كل الإنتاج |
| **VapourSynth** | فلاتر فيديو برمجية (حدة، مستويات) | GitHub Actions | ✅ مجرّب — اختبار #2 ناجح (فيديو 720p/24fps موثّق) |
| **SadTalker (Docker)** | وجه متكلم واقعي من صورة + صوت — في بيئة بايثون 3.10 مثبّتة داخل Docker | GitHub Actions | 📋 جاهز للاختبار — `docker/sadtalker/Dockerfile` + سير عمل `video-lab-sadtalker.yml` (الحل الجذري لفشل Colab: numpy/basicsr) |
| **Natron** | تركيب VFX بنظام العقد (بديل Nuke المجاني) | محلي / Actions لاحقاً | 📋 موثّقة — لاحقاً |
| **Remotion** | فيديو برمجي بـ React/TypeScript | Actions لاحقاً | 📋 موثّقة — لاحقاً |

## 6. GPU مجاني (لتقنيات الذكاء الاصطناعي)

| الخدمة | GPU المجاني | الحدود | الاستعمال |
|---|---|---|---|
| **Google Colab** | T4 (15GB VRAM) | جلسات محدودة زمنياً، GPU غير مضمون دائماً | SadTalker، Wan 2.1 1.3B، LTX، CogVideoX |
| **Kaggle Notebooks** | T4 / P100، 30GB RAM | الأفضل لنماذج الفيديو | HunyuanVideo، Wan 2.1 14B |
| **Hugging Face Spaces** | عروض مجانية (ZeroGPU) | تجربة سريعة فقط | تجربة Wan 2.1 وغيره قبل التثبيت |

## كيف تُضاف تقنية جديدة

1. جرّبها أولاً (دفتر Colab أو سكربت) وثبّت أنها تعمل.
2. أضف ملفاتها هنا (`scripts/` للسكربتات، `colab/` للدفاتر).
3. حدّث هذا الملف: صف جديد في الجدول المناسب + الحالة ✅.
4. لا تضف أي تقنية مدفوعة أو تحتاج اشتراكاً بدون موافقة صريحة.

## 7. جولة البحث 6 — تقنيات جديدة (2026-11-08)

| التقنية | ماذا تفعل | الرخصة | GPU / مفتاح | الحالة |
|---|---|---|---|---|
| **Z-Image Turbo** | صور أشخاص واقعية جداً (مدخل لـ SadTalker) — 6B، 8 خطوات، GGUF أقل من 8GB VRAM | Apache 2.0 (تجاري مسموح) | T4 مجاني | 📋 الدفتر مُصلح في الجولة 8 (§9.2): GGUF الصحيح `unsloth/Z-Image-Turbo-GGUF` Q4_K_M (المستودع القديم `MrFakeName/...` اختفى) + بناء sd.cpp Vulkan — ما زال UNTESTED على Colab |
| **Chatterbox Multilingual V3** | تعليق صوتي عربي أفضل من Piper — 23 لغة، استنساخ صوت من مقطع قصير | MIT (كود + أوزان) | T4 أو CPU | 📋 الالتزام `5de7a54` و`mtl_tts.py` وPyPI 0.1.7 كلها مؤكدة في الجولة 8 (§9.2) — الخطوة التالية: اختبار سطر عربي واحد ومقارنته بـ kareem |
| **Freesound API + Free Music Archive** | أصوات طبيعية وموسيقى حقيقية بدل النغمات الصناعية | حسب الملف — فلتر CC0 فقط | لا GPU؛ Freesound يحتاج مفتاح مجاني؛ FMA التنزيل عبر الموقع (JS) — لم يُتحقق من رابط MP3 مباشر، مفتاح API المجاني هو الطريق الموثوق | ✅ مجرّب جزئياً — معاينات Freesound محظورة من هذا الجهاز (403)؛ ملفا أجواء CC0 حقيقيان في `assets/ambience-desert/` و`assets/ambience-birds/` (عبر Openverse) |
| **slay LUTs** | 5 تدرجات سينمائية `.cube` — تدرج فيلمي حقيقي بدل فلتر `eq` | CC BY 4.0 (مع ذكر المصدر) | CPU، بلا مفتاح | ✅ مجرّب — الملفات في `assets/luts/`؛ `lut3d=file=assets/luts/slay-04-film.cube` يعمل في FFmpeg (مختبَر على صورة المقام) |
| **librosa beat-sync** | قص على إيقاع الموسيقى (شرط المونتاج الاحترافي) | (مثبّتة أصلاً) | CPU | ✅ مجرّب — `scripts/beat_cut.py` يعمل (112.3 BPM، 15 نبضة، نقاط قص على النبضات) |
| **rembg** | إزالة خلفية الصور/الفيديو للتركيب | MIT (الكود) — **النموذج الافتراضي BRIA غير تجاري! استعمل `u2net` أو `birefnet-general`** | CPU (ONNX) | ✅ مجرّب — `scripts/remove_bg.py` يعمل بنموذج u2net (بورتريه 804×1024، 54٪ شفافية) — ملاحظة: يحتاج `rembg[cpu]` (onnxruntime) |
| **Auto-Editor** | قص الصمت تلقائياً من المقاطع | Unlicense (ملك عام) | CPU | 📋 موثّقة — خطوة في سير العمل قبل التجميع |
| **FLUX.2 [klein] 4B** | توليد/تحرير صور — ثبات الشخصية عبر 4 صور مرجعية | Apache 2.0 | T4 (~8.4GB) | 📋 موثّقة — دفتر Colab |
| **HF ZeroGPU + Lightning AI** | GPU مجاني إضافي عند انسداد Colab/Kaggle | مجاني | ZeroGPU: 5 دقائق/يوم؛ Lightning: ~22 ساعة T4/شهر | 📋 موثّقة — جرّب مساحات SadTalker/Wan الجاهزة أولاً |
| **AnimateDiff** | تحريك صورة ثابتة إلى مقطع ~2 ثانية | Apache 2.0 | T4 | 📋 موثّقة — ComfyUI على Colab |

**GFPGAN يبقى** مرمّم الوجوه المعتمَد (Apache 2.0، مدمج في SadTalker).

### ⚠️ فخاخ الرخص — لا تستعملها تجارياً
- **Coqui XTTS-v2**: الأوزان غير تجارية (رخصة Coqui العامة) — للفيديو غير التجاري فقط.
- **CodeFormer / GPEN**: ترميم وجوه ممتاز لكن رخصهما غير تجارية.
- **rembg النموذج الافتراضي BRIA RMBG 2.0**: غير تجاري — استعمل `u2net`.
- **FLUX.1 [dev]**: غير تجاري — استعمل `[schnell]` أو FLUX.2 klein.
- **Bark**: لا يدعم العربية أصلاً.
- **Jamendo**: الاستعمال التجاري يحتاج اتفاقية مدفوعة.
- **Freesound / FMA**: فلتر CC0/CC BY فقط — تجنّب BY-NC.

## 8. جولة البحث 7 — مسار الإنتاج السينمائي (المرحلة 1 من الإنتاج الاستوديو)

**الخلاصة: الترقية الأعلى قيمة هي التبديل من Blender 4.0.2 (apt، بلا OIDN) إلى الحزمة الرسمية من blender.org (4.2 LTS)** — تأتي مع OpenImageDenoiser + Grease Pencil 3 + Cycles أحدث. مجانية، بلا تسجيل. (~300MB).

| المجال | المسار المختار | ملاحظات |
|---|---|---|
| **Blender** | الحزمة الرسمية 4.2 LTS من blender.org (بدل apt) | OIDN للتنعيم، بلاطات 32×32 للمعالج، عينات 64–128 مع OIDN |
| **الإضاءة** | HDRI من Poly Haven بدقة 2K عبر API | 3 ملفات في `assets/hdri/` (استوديو/ليل/نهار)، CC0، ~19MB |
| **الخامات** | Poly Haven + ambientCG (CC0، PBR بدقة 2K) | ambientCG يعطي ملف `.blend` جاهزاً |
| **الشخصيات** | Quaternius CC0 + مكتبة UAL (بدون تسجيل، بدون إعادة استهداف) | البديل: Mixamo FBX (حساب Adobe مجاني)؛ Rigify مدمج في Blender |
| **الدخان/النار** | Mantaflow غاز بدقة 64 + Noise 3×، ≤96 إطاراً للمشهد | الخبز ~2–5 دقائق؛ السوائل (FLIP) ممنوعة على هذا المعالج |
| **الكاميرا** | دوللي/رافعة بمفاتيح + Defocus/Vector Blur في المؤلّف | DoF/motion blur الحقيقيان في Cycles للمشاهد البطولية فقط |
| **التركيب** | مؤلّف Blender المدمج أولاً | Natron (AppImage 2.6) مختبري فقط — هش بدون واجهة |
| **إدارة اللون** | AgX (مدمج في Blender 4.0+) | بدل Filmic القديم |
| **2D/Web** | Remotion/Three.js للطبقات العلوية فقط | ليس المحرك البطولي للـ 3D السينمائي على CPU |
| **ميزانية الرندر** | 720p24، مشاهد ≤10 ثوانٍ، موزعة على تشغيلات | Eevee للمعاينة والمشاهد غير البطولية |

**المستبعد:** Unreal Engine 5 (يحتاج GPU)، DaVinci Resolve (GPU + واجهة)، After Effects (مدفوع، لا لينكس)، Topaz (مدفوع)، KHAOS/EmberGen (مدفوعان).

## 9. جولة البحث 8 — سدّ النواقص ودمجها (2026-11-08)

كل بند هنا إمّا نُزّل وتحقّق منه محلياً، أو تحقّقت روابطه عبر API رسمي، أو
سُجّل كمحظور بسببب موثّق. لا شيء هنا مدفوع أو يحتاج حساباً.

### 9.1 ما نُزّل وتحقّق منه (VERIFIED — ملفات حقيقية في المستودع)

| البند | المصدر والرخصة | المسار المحلي | التحقق |
|---|---|---|---|
| **Blender 4.2 LTS** (مع OIDN) | blender.org — مجاني | `scripts/blender42_install.sh` (سكربت تثبيت جاهز لسير العمل) | URL-CHECKED: أحدث إصدار 4.2.23، HEAD 200، 350,707,672 بايت (~334 MB). السكربت يتحقق من OIDN بتعيين `cycles.denoiser = 'OPENIMAGEDENOISE'` |
| **شخصيات RPG** — 6 شخصيات متحركة (Cleric, Monk, Ranger, Rogue, Warrior, Wizard) + 7 أسلحة، FBX/OBJ/Blend + خامات | Quaternius عبر OpenGameArt — **CC0 1.0** (نص الرخصة داخل الأرشيف) | `assets/characters/rpg_characters/` (68 ملفاً) + `rpg_characters_nov_2020.zip` (12,852,133 بايت) | VERIFIED: ZIP سليم، رؤوس FBX `Kaydara FBX Binary` صحيحة |
| **UAL1 — مكتبة الحركات الموحّدة** (45 مقطعاً: Idle/Walk/Jog/Sprint/Crouch/Sitting/Jump/Roll/Death/Hit/Punch/Sword/Pistol/Spell/Swim) | مرآة GitHub `IAFahim/quaternius.universalAnimationLibrary.standard` — **CC0 1.0** (رخصة GitHub + ملف LICENSE) | `assets/mocap/UAL1_Standard.fbx` (24,908,124 بايت) + `LICENSE_UAL_CC0.txt` | VERIFIED: رأس FBX صحيح؛ 30 اسم مقطع ظهرت بمسح `strings` (منها Crouch — كان ناقصاً في الحزمة السابقة) |
| **خامات PBR للشقة** (2K: diffuse + roughness + normal) — أرضية خشب داكن، جدار جص بيج، بلاط مطبخ أزرق، قماش قطن | Poly Haven API — **CC0** | `assets/pbr/apartment/` (12 ملف JPG) | VERIFIED: كلها 2048×2048 عبر PIL (القطن 2048×2050 كما يصدرها Poly Haven) |
| **أثاث الشقة** — كرسي خشبي، أريكة، طاولة قهوة (glTF 2K + خامات) | Poly Haven API — **CC0** | `assets/models/apartment/{WoodenChair_01,Sofa_01,CoffeeTable_01}/` | VERIFIED: كل manifest صالح JSON؛ حجم `.bin` يطابق `byteLength` تماماً؛ 1 mesh / 3 صور / 1 مادة لكل نموذج |
| **HDRI** (استوديو/ليل/نهار) | Poly Haven — **CC0** | `assets/hdri/` (3 ملفات، ~19 MB) | VERIFIED: كلها Radiance HDR صالح (رأس `#?RADIANCE`)، جاهزة للرفع |

ملاحظة عن الشقة: زميل آخر يبني أرضية الشقة في `workspace/game-apk/algiers-apartment/`
(خامات 1K + HDRI شروق البندقية + `apartment.glb` جاهز). مواد جولة 8 **مكمّلة لا مكررة**:
خامات 2K + خرائط خشونة/نورمال + الأثاث الثلاثي الذي لا تملكه تلك الأرضية بعد.

### 9.2 ما تحقّقت روابطه ولم يُشغَّل بعد (URL-CHECKED — يحتاج تشغيل Colab)

| البند | التحقق | ما زال يحتاجه |
|---|---|---|
| **Chatterbox TTS عربي** | الالتزام `5de7a54` موجود فعلاً (رسالة "Update ChatterboxNano (#542)"، 2026-07-21)؛ `mtl_tts.py` موجود في ذلك الالتزام؛ PyPI `chatterbox-tts` 0.1.7 موجود؛ الدفتر JSON صالح (6 خلايا) | تشغيل Colab واحد: سطر عربي + مقارنة مع Piper kareem |
| **Z-Image بورتريه** | **إصلاحان مطبّقان على الدفتر:** (1) مستودع `MrFakeName/Z-Image-Turbo-GGUF` **اختفى** — استُبدل بـ `unsloth/Z-Image-Turbo-GGUF` (987,201 تنزيل، Apache 2.0، ملف `z-image-turbo-Q4_K_M.gguf` 3,671 MB) مع بديل `jayn7/...`؛ مستودع `Tongyi-MAI/Z-Image-Turbo` موجود لكن بلا GGUF (صيغة diffusers) فلا يصلح كبديل. (2) sd.cpp **ألغى بناء Linux CUDA** (آخر 5 إصدارات بلا أصل CUDA) — الدفتر الآن ينتقل إلى بناء Linux Vulkan (39 MB) ثم البناء العادي | تشغيل Colab واحد: توليد البورتريه 1024×1024 |
| **Video2X / Real-ESRGAN** | `Video2X` 6.4.0: AppImage لينكس 220 MB موجود؛ `Real-ESRGAN` v0.3.0 بلا ثنائيات — المسار الصحيح pip: `realesrgan` 0.3.0 موجود على PyPI، وزن `RealESRGAN_x4plus.pth` يردّ 302 (يحلّ)؛ RIFE ncnn 20221029 ثنائي Ubuntu 411 MB موجود | تشغيل Colab: دفتر جديد `colab/Video2X_Upscale.ipynb` (7 خلايا، UNTESTED) — تكبير x4 لمقطع اختبار 640×360 |
| **Wan 2.1** | النموذج `Wan-AI/Wan2.1-T2V-1.3B` موجود (89,891 تنزيل)؛ الرخصة **Apache 2.0** منصوص عليها في README؛ المساحة الرسمية `Wan-AI/Wan2.1` حالتها **RUNTIME_ERROR (معطّلة الآن)** — Colab هو الطريق | تشغيل Colab: دفتر جديد `colab/Wan21_Test.ipynb` (7 خلايا، UNTESTED) — 33 إطاراً 832×480 |

### 9.3 LivePortrait — تحديث مهم (نُقل المستودع + الرخصة مؤكدة)

- المستودع انتقل من `KwaiVGI/LivePortrait` إلى **`KlingAIResearch/LivePortrait`**
  (الرابط القديم يحوّل 301). 19,432 نجمة، آخر دفع 2026-06-01.
- **الرخصة: MIT** — مؤكدة من ملف `LICENSE` (حقوق 2024 لـ Kuaishou Visual
  Generation and Interaction Center). آمنة تجارياً.
- التثبيت (Colab T4): بيئة Python 3.10 + `torch==2.3.0` (cu118) +
  `pip install -r requirements.txt`، ثم الأوزان:
  `huggingface-cli download KlingTeam/LivePortrait --local-dir pretrained_weights --exclude "*.git*" "README.md" "docs"`
  ثم `python inference.py` (صورة مصدر + فيديو قيادي).
- **Docker مقابل Colab:** Colab أسهل للاختبار الأول (نفس بيئة SadTalker)؛
  Docker على Actions يصلح لاحقاً للإنتاج المتكرر بلا طابور GPU — لكنه يحتاج
  بناء صورة Python 3.10 مثل SadTalker (الأوزان ~2 GB داخل الصورة).

### 9.4 ما تعذّر (BLOCKED — بسبب موثّق، لا يعاد المحاولة بلا حل جديد)

- **أجواء صوتية جديدة (مدينة/بحر) من Openverse:** كل نتائج الصوت من Freesound
  تردّ **403** من هذا الجهاز (نفس حظر الجولة 6)؛ ومحاولة فلترة المصدر عبر
  API (`source=wikimedia` / `wikimedia_commons`) تردّ **400**. المكتبة الحالية
  تبقى: صحراء + طيور فقط. الحل البديل لاحقاً: مفتاح Freesound المجاني (يحتاج
  تسجيلاً) أو تسجيل أصوات ميدانية.
- **Kaggle GPU:** معلّق على تأكيد المستخدم على هاتفه (خارج نطاق هذه الجولة).
- **Pixabay / Unsplash:** معلّق على تسجيل الدخول (خارج نطاق هذه الجولة).

### 9.5 أدوات الجولة

- `scripts/fetch_round8.py` — سكربت الجلب والتحقق (يعيد تنزيل كل أصول 9.1
  ويتحقق من رؤوس الملفات والأحجام؛ أصلح خلال الجولة: ملفات `.bin` الخاصة
  بـ glTF ليست JPEG).
- `scripts/blender42_install.sh` — تثبيت Blender 4.2 LTS + فحص OIDN.
- `colab/Video2X_Upscale.ipynb` + `colab/Wan21_Test.ipynb` — دفتران جديدان،
  UNTESTED (يحتاجان تشغيل Colab).
