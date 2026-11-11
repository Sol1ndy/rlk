# Perfect parry / perfect dodge reference analysis

All frame numbers are 60 fps video frames (frame / 60 = seconds). The recording contains duplicated frames (the game rendered at roughly 40 fps), so single-frame timings carry ±1–2 frames.

**Three things to know first**
- **Only 3 perfect dodges exist in `dodge.mp4`** (you asked for 4 or more). I analysed all three; none appear in `parry.mp4`.
- **The perfect dodge has two body motions.** Two of three are a back handspring; one is a laid-back "Fosbury" float followed by a backward ground roll.
- **The perfect parry "slow-motion" is really a near-freeze** of about 12 frames, not a sustained slow-mo. The perfect dodge has a true slow-mo (about 0.33×) of about 20 frames.

## 0. Tutorial text (Korean, top-right panel)

- **parry.mp4:** title `퍼펙트 패링`; body `적의 공격을 완벽하게 쳐내며 적의 균형에 피해를 줍니다.` ("Perfectly deflects the enemy's attack and damages the enemy's balance."). Key prompt: `E`. Log labels: `E 가드` (Guard), `E 퍼펙트 패링` (Perfect Parry).
- **dodge.mp4:** title `퍼펙트 닷지`; body `적의 공격을 완전히 회피합니다. 퍼펙트 닷지에 성공했을 때 버스트 에너지를 충전하고, ◐을 눌러 추가 일격을 가할 수 있습니다.` ("Completely evades the enemy's attack. On a successful Perfect Dodge, Burst Energy is charged and you can press ◐ [mouse-button icon] for an additional strike."). Key prompt: `SHIFT`. Log labels: `SHIFT 닷지`, `SHIFT→SHIFT 더블 닷지` (Double Dodge), `SHIFT 퍼펙트 닷지`, `1→1 쿼드러플렛` (a skill).
- **Both:** a blue diamond popup `성공` ("Success") appears above the enemy about 17–20 frames after a perfect parry or dodge. This is training-room UI.
- **Top-left menu:** `TAB+1 다시 시작`, `TAB+2 무한 에너지: 꺼짐`, `TAB+3/4 적 행동 설정: 일반 공격`, `TAB+H UI 숨기기`, `TAB+C 훈련 종료`.
- **Gauges:** the BE row gains a pip after a perfect parry (3 → 4 lit). After a perfect dodge the BU (Burst) row reads 3 lit versus 1 at the start of the parry video; this is not a same-clip before/after check, but it fits the tutorial text.

## 1. Event lists

**How I told them apart**
- The input-log panel text (`가드` / `퍼펙트 패링` / `닷지` / `더블 닷지` / `퍼펙트 닷지`).
- The `성공` popup (blue-pixel count spike).
- For the parry: the large orange starburst plus full-screen warm tint and blur.
- For the dodge: the dark vignette (mean luma about 150 → 100–137) plus red-pink character tint.

### parry.mp4

The enemy loops two 3-hit combos about every 5.5–6.5 s:
- **Combo A:** overhead slash → low sweep → sweep.
- **Combo B:** horizontal sweep → second sweep about 0.55 s later → double-blade slash about 1.3 s later.

**Perfect parries: 10.** F0 is my estimate of blade contact; S is the camera-snap frame.

| # | F0 time | S frame | Note |
|---|---|---|---|
| 1 | 21.5 s | 1295 | Combo B hit 2. Analysed in full. |
| 2 | 71.8 s | 4312 | Combo B hit 2 |
| 3 | 91.0 s | 5466 | Combo A hit 1 |
| 4 | 109.95 s | 6601 | Combo B hit 2 |
| 5 | 111.4 s | 6690 | Combo B hit 3; second perfect in a row |
| 6 | 132.95 s | 7982 | |
| 7 | 139.55 s | 8379 | Low contact point |
| 8 | 145.8 s | 8751 | Camera very close |
| 9 | 152.8 s | 9176 | Analysed in full |
| 10 | 165.5 s | 9935 | |

**Normal guards (`가드`):** every other blade contact while E is held. Approximate contact times (s): 2.9, 3.3, 8.3, 8.9, 10.2, 15.4, 15.9, 20.9, 22.9, 28.1, 28.5, 33.6, 34.2, 35.4, 40.6, 41.0, 46.1, 46.7, 47.9, 53.1, 53.5, 58.6, 59.2, 60.5, 65.7, 66.1, 71.2, 73.3, 78.5, 78.9, 84.5, 85.9, 96.8, 97.5, 98.7, 104.0, 104.4, 109.4, 126.8, 127.3, 134.4, 140.2, 145.1, 147.2, 158.2, 158.7, 163.7, 164.3. Not each one was verified individually; between 67 and 98 s some of these hits were answered with plain dodges instead (log `SHIFT 닷지` at about 67.6, 73.0, 80.1, 86.7, 91.1, 92.0, 95.2 s).

**Follow-up variant, seen once:** after perfect parries #4 and #5 back to back, a mouse click at about 115.5 s plays a close-up finisher cinematic on the enemy (frames 6806–7172, 113.4–119.5 s). Presumably this is the enemy's balance breaking; not analysed in detail. A second long orange effect at 169.0–171 s was also not analysed.

### dodge.mp4

Times come from the input log, ±0.3 s.

**Perfect dodges: 3**

| ID | F0 frame | Time | Motion | Camera |
|---|---|---|---|---|
| PD1 | 3252 | 54.2 s | Back handspring | Side view. Pressed right after a double dodge. |
| PD2 | 4025 | 67.1 s | Laid-back float + backward ground roll | Side view. Pressed right after a double dodge. |
| PD3 | 6291 | 104.85 s | Back handspring | Rear view (cleanest). Single dodge against Combo A's overhead slash. |

**Normal single dodges (`닷지`):** about 1.6, 3.0, 6.9, 8.4, 13.1, 14.2, 15.6, 29.3, 45.0, 48.3, 80.4, 106.4, 112.9, 117.9 s.
- Motion: a low dash step (deep forward lean, trailing leg extended), about 15–18 frames, about 1.5–2 body heights of travel.
- Directions seen: sideways-right (8.4 s), back-right (13.1 s), diagonal (40.8 s). Direction keys are not shown, so direction calls are low confidence.

**Double dodges (`더블 닷지`):** about 10.4, 22.8, 27.8, 28.2–28.9, 40.9, 42.3, 46.2, 46.7–47.9, 53.8, 66.5–66.9, 79.3–80.1, 91.8–93.0, 110.8–111.9, 116.6 s. The second press is an aerial cartwheel/side flip; the body is inverted about 24–34 frames after it.

**Other:** `쿼드러플렛` skill at about 99.7–103 s (blue-white burst; not a dodge) and various mouse-click attacks.

## 2A. Perfect parry breakdown

F0 = enemy blade reaches her sword. Full analysis on F0 = 1291 and F0 = 9170; snap and freeze lengths cross-checked on all 10.

### Timing

| Frames | What happens |
|---|---|
| −8…−2 | Enemy swings. Its body glows orange and casts a warm light pool on the floor (the enemy's own tell, not a parry effect). She raises the guard by −2. |
| 0…+3 | Contact and hit-stop: 2–4 identical frames (4 at 9170–9173; two 2-frame pairs at 1291–1294). Clang onset at 0…+2. |
| +4…+6 | The enemy blade is swept off to her lower-left. Camera snap S falls here (+4 for 1291, +6 for 9170); S itself is held 1–3 frames. |
| +7 | Starburst appears at full size (+7 in both analysed events; S+1…+3 in all 10). |
| +6…+17 | Near-freeze. Poses and spark shapes are effectively static (0–0.1×); only a slow camera drift of about 5 px/frame continues. Measured from S on the 10 events: about 11, 12, 14, 15–18, 13, 9–13, 12, n/a, 12, 15 frames, median about 12–13. |
| +16…+18 | Release in one frame straight to 1.0×, with no ramp. |
| +18…+32 | Normal speed. She recovers to a ready guard; the enemy recoils. |
| +50…+60 | Both back to neutral. |

- **Player can act again:** not determinable from the footage; my guess is about +36…+45.
- **Enemy combo timing is not delayed:** the next combo hit landed 81 frames after F0, against 78–80 frames in un-parried runs. The stagger is a short recoil, not a stun. Two perfect parries in a row led to the finisher.

### Character motion

- **Guard pose (−6…0):** feet apart; sword held in front of her face/upper chest, blade roughly vertical to 30° off vertical with the tip up; elbows bent; slight forward lean.
- **Deflect (+3…+6):** blade sweeps across her body from upper-right to lower-left, carrying the enemy blade to her left and down.
- **Freeze pose (+6…+17):** wide lunge with the rear leg stretched back and front knee bent; torso twisted; sword arm thrown up past her head (follow-through); head turned to the clash. Displacement under about 0.2 body heights.
- **Recovery (+18…+34):** stands up into a ready guard, sword diagonal across the body with the tip up toward the enemy. Sword lowers at about +55…+60.
- **Enemy:** at S it is thrown open, weapon arm flung up and back, torso rocked back about 20–30°, with about a half step back (roughly 0.3–0.5 of the player's height; this is a guess). It holds through the freeze, stays staggered with the blade high until about +45…+50, and is neutral by about +55…+62.

### Effects

- **Starburst at the blade contact point.** This is the "yellow light from the sword".
  - Position: slightly above her head height, between the fighters.
  - Colours: core `#FDF7D4` (near-white yellow), rays `#F5C058` (orange-yellow).
  - Size: ray span about 225–310 px wide by 290–350 px tall on a character about 430–470 px tall, so about 0.5–0.7 body heights across. A softer halo reaches about 0.8.
  - Life: full size instantly at +7; static through the freeze; at release it shatters into roughly 40–60 thin spark streaks that fly out about 1 body height and are gone by about +30.
- **Horizontal lens streak** through the starburst centre: full screen width, about 6–10 px thick, pink-orange (`#F5D3CD` near the centre, `#C1AAA8` at the edges). Visible +7…about +22, thinning.
- **Screen warm tint:** from S for about 11 frames. Mean luma rises about 152 → 168–172 (about +10%); the floor shifts `#A2AAB4` → `#E1C7B9`. Fades in 4–6 frames after release.
- **Blur:** strong background/radial blur on everything but the two fighters from S to release; off within one frame.
- **Lightning:** thin white-yellow branching arcs crawl over the enemy and to the floor, about +22…+45.
- **Light on the sword:** the blade reads white-hot around +20…+35. There is no separate lasting sword glow, no after-images, and no ground decal.
- **Brief small black debris specks** near the enemy at contact.

### Camera

- At S: an instant cut-like re-aim that puts the clash point at screen centre horizontally and upper-middle vertically (the character shifts about 80 px).
- Punch-in is small, about 1.05–1.1× (character height about 420 → 450 px).
- Slow push/drift during the freeze.
- At release: a one-frame jump of about 15–20 px (about 1% of the width), then an ease back behind her over about 20 frames. Fully re-centred by about +40.
- No sustained shake.

### Sound

| Frames | Sound |
|---|---|
| −10…0 | Swing whoosh, 150–600 Hz |
| 0…+2 | Sharp broadband metallic clang, about −33 dBFS against about −41 dBFS ambience |
| +7…+25 | Louder, brighter ring at −30…−31 dBFS, with tonal partials around 1.97, 2.2–2.3, 2.6 and 3.26 kHz |
| +25…+45 | Linear decay |

- The ring is about 0.75 s in total.
- No clear ducking: the level at +45…+70 is about 4 dB under the earlier ambience sample, which is not conclusive. There is no music in the room.
- The partials near 1.97 / 2.63 / 3.13 kHz also appear in the perfect dodge. That part is either a shared "perfect" stinger or the training-room `성공` jingle; I could not separate them.

### Normal guard, for contrast (F0 = 171)

- Same guard pose; she stays upright and gets pushed slightly.
- Small yellow starburst at the blade, about 0.25–0.3 body heights across, lasting about 8–10 frames, with a few falling sparks.
- 2–3-frame hitches only. No snap, tint, blur, freeze, streak, lightning or popup.
- The enemy is not staggered and continues its combo.
- Sound: a shorter, thinner "tink", about −35 dBFS, with peaks around 3.7, 5.6 and 7.8 kHz, lasting about 15–20 frames.

## 2B. Perfect dodge breakdown

F0 = trigger frame, where the blade would connect (3252, 4025, 6291).

### Timing

| Frames | What happens |
|---|---|
| 0…+2 | Trigger. Three identical frames in all three events. Vignette starts. |
| +3…+16 | Near-normal speed, measured about 0.9×: the enemy advances 14 normal frames in 16. The evasive step finishes and the blade passes through her ghosted body. |
| +16…about +37 | Slow-mo at about 0.33×. In PD3 the enemy advances 7 normal frames in 21 real frames, and frame-diff drops to about 40% in PD2. Window: +17…+38 (PD3), +16…+33 (PD2), about +16…+32 (PD1). Entry and exit are abrupt (2 frames or fewer). |
| about +37 onward | Normal speed. The flip completes in about 20–28 frames. |
| +57…+65 | Landing: PD3 +57, PD1 +60, PD2 crouch +61…+65. |
| about +72 | Settled. |

- **Player can act again:** a guess of about +60…+66.

### Character motion, back handspring (PD1 side view, PD3 rear view)

| Frames | Pose |
|---|---|
| 0…+14 | Dodge step; body rendered as a smeared ghost |
| +16…+36 (slow) | Upright facing the enemy, both arms raised to head height or above, sword in the right hand, beginning to arch back. In PD1 she is already leaning and arching back with arms overhead. |
| about +37…+39 | Sharp back arch, arms spread; body passes horizontal face-up; feet leave the floor |
| about +39…+47 | Inverted: head and hair near the floor, hands on or near the floor, legs vertical in a wide front-back split. Feet reach about 1.4–1.5 body heights; hips about 0.6–0.7. |
| about +47…+55 | Legs come over one after the other; torso rises |
| +57…+60 | Stands in a T-pose: arms straight out sideways, sword in the right hand with the tip down, facing the enemy |
| to about +72 | Sinks into a low ready stance |

- **Rotation:** 360° backward about her left-right axis. No twist; she ends facing the same way.
- **Travel:** about 1.5–2 body heights straight back, away from the enemy. This is an estimate from floor landmarks, ±0.5.

### Variant C (PD2): laid-back float and backward roll

- **Slow-mo (+16…+33):** she is laid back almost horizontal, face-up, back arched, body about 20–30° off the floor, feet toward the enemy, sword held up overhead in the right hand.
- **+38…+47:** drops onto her shoulders.
- **+48…+58:** tucked backward shoulder roll.
- **+61…+65:** crouch; standing by about +70.
- Same backward travel direction. This is the one that looks like a Fosbury flop.

### Effects

- **Dark vignette** on the top and edges. The sky and corners go `#989EA9` → about `#333843`.
  - In: 2–6 frames.
  - Held: to the end of the slow-mo (33–38 frames).
  - Out: 2–10 frames. PD3 snaps back in about 2 frames at +39/+40; PD1 fades over +36…+46.
- **Floor around her tinted pink** (`#A3ABB6` → `#C3AFB9`–`#D8B3BC`), radius about 1.5–2 body heights.
- **Trigger burst (frames +1…+7):** a radial spray of short pink-red streak particles from her body, radius about 0.6–0.8 body heights.
- **Ghosting (+1…about +14):** her body is one smeared translucent pink-white ghost, a distortion rather than discrete copies.
- **Red tint (about +5 to landing):** the whole character has a red-pink emissive tint. Hair glows red (about `#D67168` highlights, `#7F2D29` body); skin reads `#E6998F`. Drifting red-pink embers surround her. The tint fades over the last about 10 frames of the flip and is gone at landing.
- **Not present:** discrete after-image copies, chromatic aberration.
- **Not part of the dodge:** the yellow streak and sparks belong to the enemy blade. The black blots on the floor in PD3 are leftovers from an earlier skill.

### Camera

- **PD3:** stays behind her and tilts up to a lower angle. The horizon drops from about y = 40 to about y = 300 of 1080, which I estimate at roughly 13–15°. Slow push during the slow-mo.
- **PD1 / PD2:** whip-pan of about 90° in 6–10 frames to a low side view that frames the whole flip, then back behind her around landing (about +56…+62).

### Sound

| Frames | Sound |
|---|---|
| +2 | Broadband whoosh/boom, about −40 → −31 dBFS, with a strong low end (30–500 Hz up 10–15 dB) |
| +8…+25 | Bright chime/ring with partials around 1.97, 2.63 and 3.13 kHz (same caveat as the parry) |
| to about +38 | Decay |
| to about +60 | Low rumble/whoosh, covering the flip and landing |
| about +65…+75 | Back to ambience |

- No measurable ducking.
- A normal dodge has no distinct sound above ambience in this recording, and no slow-mo, tint, vignette or camera change.

## 3. Evidence images

Originals are in `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/cb/video2/ref_pd/` (26 MB; no frame dumps were kept). Re-encoded copies for this review are listed at the end of this file. Strips show every second frame, labelled with the offset from F0. The parry strips run −12…+60, the dodge strips −12…+72, and the normal-guard strip −12…+48.

**Strips**
- `strip_parry_perfect_A_f0=1291.jpg`
- `strip_parry_perfect_B_f0=9170.jpg`
- `strip_parry_normal_guard_f0=171.jpg`
- `strip_dodge_perfect_A_f0=6291_backhandspring_rearview.jpg`
- `strip_dodge_perfect_B_f0=3252_backhandspring_sideview.jpg`
- `strip_dodge_perfect_C_f0=4025_layout_backroll.jpg`

**Full frames**
- `parry_perfect_peak_f1299_full.jpg` and `parry_perfect_peak_f9179_full.jpg`: starburst, streak, tint and blur.
- `dodge_perfect_trigger_burst_f6294_full.jpg`: trigger burst and ghosting.
- `dodge_perfect_peak_f6316_full.jpg`, `dodge_perfect_peak_f3276_full.jpg`, `dodge_perfect_peak_f4050_full.jpg`: slow-mo with vignette and red tint.
- `dodge_perfect_flip_apex_f3298_full.jpg` and `dodge_perfect_flip_apex_f6336_full.jpg`: inverted apex.

Working sheets and scripts are in the originals folder under `work/`.

## 4. Build spec in game ticks (1 tick = 3 frames)

"[guess]" marks anything not measured in the reference.

### Perfect parry (T0 = contact)

| Tick | Avatar | Effects | Time scale | Camera | Sound |
|---|---|---|---|---|---|
| −2…−1 | Guard: both arms raised, sword in front of head (tip up, 0–30° tilt), slight forward lean, feet apart | — | 1 | — | Enemy swing whoosh |
| 0 | Hold guard | Small sparks at blade | Hit-stop 1 tick (ref 2–4 frames) | — | Sharp metallic clang |
| 1 | Sweep sword across body, upper-right → lower-left; enemy blade knocked to player's left/down | — | 1 | — | — |
| 2 | Lunge pose: front knee bent, rear leg straight back, torso twisted, sword arm thrown up past head. Enemy rocked back 20–30°, weapon arm up and back | ON: starburst at blade (about 0.6 body heights across, core `#FDF7D4`, rays `#F5C058`); full-width thin horizontal streak; warm tint (about +10% brightness, toward `#E1C7B9`); background blur | about 0.05 (freeze) | Instant re-aim to clash point, about 1.05–1.1× punch-in, slow push | Bright ring starts (about 2–3.3 kHz partials) |
| 3–5 | Hold both poses | All held static | about 0.05 | Slow drift | Ring sustains |
| 6 | Begin recovery | Blur off instantly; tint fades over 2 ticks; starburst shatters into about 40–60 spark streaks flying about 1 body height over 3–4 ticks; streak fades by tick 7–8 | 1 (instant) | One-frame kick of about 1% of the width, then ease back over about 7 ticks | Ring continues |
| 6–10 | Player rises to ready guard, sword diagonal with tip toward enemy. Enemy staggered: blade arm high, leaning back, about half a step back [guess] | Thin white-yellow lightning arcs on enemy and floor, ticks 7–15 | 1 | Easing back | Ring decays from tick 8, to ambience by tick 15 |
| 10–16 | Hold ready pose; enemy holds stagger to about tick 16 | — | 1 | Default by tick 13 | — |
| 17–20 | Both neutral; sword lowers | — | 1 | — | — |

- Player input probably returns around tick 12–15 [guess].
- Do not delay the enemy's next attack beyond the freeze: in the reference the next combo hit lands on its normal schedule, about 27 ticks after contact.

### Perfect dodge (T0 = would-be contact)

| Tick | Avatar | Effects | Time scale | Camera | Sound |
|---|---|---|---|---|---|
| −2…0 | Normal dodge step starts: low dash, deep lean | — | 1 | — | — |
| 0 | Continue step | Hold 1 tick (ref 3 identical frames). Vignette ON (top and edges to about `#333843`, ramp 1–2 ticks). Pink-red radial streak burst, radius about 0.7 body heights, 2 ticks. Avatar becomes a smeared translucent pink ghost. | Hitch, then 1 | Start tilt-up of about 13–15° / lower angle, or whip to side view (2–3 ticks) | Whoosh/boom with strong low end, at about +2 frames |
| 1–4 | Finish step; enemy blade passes through the ghost | Ghost until tick 4. Red-pink body tint and red-glowing hair from about tick 2. Floor pink within 1.5–2 body heights. Drifting red embers. | about 0.9–1 | Settling | Bright chime from about tick 3 |
| 5–12 | Slow-mo beat: upright facing enemy, both arms raised to head height or above, slowly starting to arch back (only about 2–3 ticks of animation play) | Vignette, tint, embers at full | 0.33 (snap in at tick 5, snap out at tick 12; ref 17–21 real frames) | Slow push-in | Chime rings and decays |
| 12–13 | Arch back hard, arms overhead; body passes horizontal face-up; feet leave the floor | Vignette OFF over 1–3 ticks | 1 | — | Low whoosh |
| 14–15 | Inverted: hands on or near the floor, head down, legs vertical in a front-back split (feet about 1.4 body heights, hips about 0.65) | Red tint still on | 1 | — | — |
| 16–18 | Legs come over one at a time; torso rises | Red tint fades | 1 | Starts returning | — |
| 19 | Landed about 1.5–2 body heights behind the start, facing the enemy, T-pose (arms straight out sideways, sword tip down) | Tint off | 1 | — | Soft landing [guess] |
| 20–24 | Sink to low ready stance | — | 1 | Default by tick 24 | — |

- Control probably returns at tick 20–22 [guess].
- Total rotation is 360° backward about the left-right axis, with no twist.
- **Optional variant C:** during ticks 5–11, lay the body back almost horizontal (face-up, 20–30° off the floor, feet toward the enemy, sword up overhead). Then drop to the shoulders at ticks 12–15, tucked backward roll at ticks 16–19, crouch at tick 20–21, and stand at tick 23.
- On success the reference also charges Burst energy and opens a follow-up strike window on the attack button (per the tutorial text; the follow-up itself was not captured cleanly).

## Caveats

- **Contact frame:** F0 for the parry is my estimate of blade contact, which is 4–6 frames before the unmistakable camera snap. If you would rather key off the snap, shift the parry table by about 1–2 ticks.
- **Parry slow factor:** the 0–0.1× figure is from pose and spark stasis by eye and block-matching; camera drift masks finer measurement.
- **Dodge slow factor:** the 0.33× comes from matching enemy poses against the same combo at normal speed, in one event (PD3). PD2's frame-diff drop is consistent with it; PD1's camera motion prevented a measurement.
- **Sound:** descriptions come from band-energy and spectral analysis only; I could not listen to it.
- **Travel, peak height, enemy knock-back and control-return times** are estimates, as marked.
- **The warm floor light before contact and the orange enemy glow** are the enemy's attack tell and are present on normal hits too.
- **The parry event list leans on the log:** I only looked at about the first 70 s of input-log sheets; the middle and last sheets (which hold the `퍼펙트 패링` rows) I did view. The 10 perfect parries are confirmed visually.

## Evidence copies in this review folder

Re-encoded at JPEG quality 80 (strips downscaled to 1600 px wide, full frames to 1280×720; about 2.5 MB in total). The original names use `f0=<frame>`; the copies use `f0-<frame>`.

**Strips** (every second frame, labelled with the offset from F0)
- [ref_pd/strip_parry_perfect_A_f0-1291.jpg](ref_pd/strip_parry_perfect_A_f0-1291.jpg)
- [ref_pd/strip_parry_perfect_B_f0-9170.jpg](ref_pd/strip_parry_perfect_B_f0-9170.jpg)
- [ref_pd/strip_parry_normal_guard_f0-171.jpg](ref_pd/strip_parry_normal_guard_f0-171.jpg)
- [ref_pd/strip_dodge_perfect_A_f0-6291_backhandspring_rearview.jpg](ref_pd/strip_dodge_perfect_A_f0-6291_backhandspring_rearview.jpg)
- [ref_pd/strip_dodge_perfect_B_f0-3252_backhandspring_sideview.jpg](ref_pd/strip_dodge_perfect_B_f0-3252_backhandspring_sideview.jpg)
- [ref_pd/strip_dodge_perfect_C_f0-4025_layout_backroll.jpg](ref_pd/strip_dodge_perfect_C_f0-4025_layout_backroll.jpg)

**Full frames**
- [ref_pd/parry_perfect_peak_f1299_full.jpg](ref_pd/parry_perfect_peak_f1299_full.jpg)
- [ref_pd/parry_perfect_peak_f9179_full.jpg](ref_pd/parry_perfect_peak_f9179_full.jpg)
- [ref_pd/dodge_perfect_trigger_burst_f6294_full.jpg](ref_pd/dodge_perfect_trigger_burst_f6294_full.jpg)
- [ref_pd/dodge_perfect_peak_f6316_full.jpg](ref_pd/dodge_perfect_peak_f6316_full.jpg)
- [ref_pd/dodge_perfect_peak_f3276_full.jpg](ref_pd/dodge_perfect_peak_f3276_full.jpg)
- [ref_pd/dodge_perfect_peak_f4050_full.jpg](ref_pd/dodge_perfect_peak_f4050_full.jpg)
- [ref_pd/dodge_perfect_flip_apex_f3298_full.jpg](ref_pd/dodge_perfect_flip_apex_f3298_full.jpg)
- [ref_pd/dodge_perfect_flip_apex_f6336_full.jpg](ref_pd/dodge_perfect_flip_apex_f6336_full.jpg)
