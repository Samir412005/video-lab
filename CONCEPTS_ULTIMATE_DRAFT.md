# ULTIMATE ANIMATION — Phase 3 concept drafts (DRAFT ONLY)

Status: DRAFT. Do NOT present to the user until the Phase 2 capability
test results are in (brief condition 8: no final production before the
best path is proven by tests). Each concept lists the test gates it needs.

## Concept 1 — «النور» (The Light)

Logline: A lone hooded survivor walks a rain-soaked Algiers street at
night, following a single point of golden light that grows into a rising
sun over the bay.
- Style: cinematic 3D, dark + gold, HDRI studio lighting, AgX, DOF f/2.8,
  compositor Vector Blur.
- Shots: (1) dolly-in on the figure in the rain (Quaternius + UAL walk
  clip); (2) ember particles rising past the camera; (3) Mantaflow smoke
  curling around street lamps; (4) pull-back reveal of the sun over the
  Martyrs' Memorial (real photo integrated as a 3D card).
- Sound: CC0 desert ambience + rain (synthesized), Piper kareem VO,
  beat-synced cuts (librosa), slay LUT grade.
- Needs to pass: capability test A (cinematic PBR/HDRI/DOF/embers),
  test B (smoke bake), character import + UAL retarget.
- Risk: heaviest concept; smoke + character in one film is the most
  render-expensive path. Fallback: drop the smoke shot, keep embers.

## Concept 2 — «الجزائر من فوق» (Algeria From Above)

Logline: Algeria builds itself in front of the camera — sand dunes rise
into mountains, the sea pours in, and the Martyrs' Memorial assembles
from light.
- Style: procedural motion graphics + real photography. Blender geometry
  (displaced plane morphs), Ken Burns on real Pexels photos (Martyrs,
  dunes, Casbah), Manim typography, match cuts on the beat.
- Shots: (1) dune field morphs into a topographic map; (2) photo cards
  fly in on beat cuts; (3) flag wave (proven in Algeria10); (4) gold
  title card close.
- Sound: Piper kareem VO, CC0 birds ambience over the dunes, beat-sync.
- Needs to pass: photo/zoompan + Manim + beat-sync — ALL already proven
  (Algeria10 v2, time-film v2). Lowest risk.
- Risk: least "studio CGI" of the three; relies on editing craft rather
  than 3D spectacle. Strongest if the character/smoke tests fail.

## Concept 3 — «الساعة» (The Clock)

Logline: A talking narrator — a realistic face built from a portrait —
tells the story of a city where time is running out, while a clock tower
of light assembles itself behind him.
- Style: hybrid — SadTalker talking head (realistic portrait + VO) cut
  against Blender 3D (the tower from «الوقت», rebuilt with HDRI + OIDN).
- Shots: (1) talking head, close, shallow DOF; (2) tower assembly
  (golden cubes, dolly + orbit); (3) clock face close-up, particles;
  (4) narrator + tower in one frame, calm ending.
- Sound: the narrator IS the sound — Chatterbox or Piper VO driving the
  lips; ambience under.
- Needs to pass: SadTalker Docker run (talking head must actually move
  and speak), Blender 4.2 + OIDN path, Chatterbox Colab test (optional).
- Risk: SadTalker has failed 3 times already (Colab x3, Docker x2); if
  run #3 fails, this concept dies and the narrator becomes a Manim
  title card instead.

## How the choice is made

- If A + B + SadTalker pass: Concept 1 (most ambitious) with Concept 3
  as the opening.
- If A + B pass but SadTalker fails: Concept 1 alone.
- If character/smoke fail but photo/Manim pass: Concept 2.
- Present all three to the user with one-tap choice AFTER the test
  results land; do not start production before his pick.
