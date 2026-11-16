# 홍련 (Scarlet): gameplay video analysis for the combat overhaul

Source: 「[4K] 스텔라블레이드(Stellar Blade) - 보스 홍련 (feat. 레이븐모드)」 (the user's Google Drive file; 380.7 s, 1920 × 804
letterboxed, 60 fps). The audio was not used. Subtitles are burned in: white Korean with a dark outline, bottom centre.
Written for lane H (`plan.md`) and for lanes C / B (player-side parry / dodge / flashes, balance gauge). It sits next to
`decisions.md` and the boss plan `R:tools/dev/sim/hr/PLAN.md` (§1 footage, §3 cutscenes, §4 patterns). PLAN.md was
built from a different recording.

Conventions:
- **Times** are seconds from the video start (s.ms). 1 s = 20 t (game ticks) = 60 f.
- **Sheets** under `ref/` are committed next to this file. They are ≤ 640 px wide and every tile is labelled with its
  time. The scratch-only sheets (not committed) are under `S:cb/video/`, where `S:` =
  `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`: `ovs/ov_NNN.jpg` (1 fps overview, 20 s per
  sheet), `f4s/s_NNNN.N.jpg` (4 fps, 7.5 s per sheet), `dz/*.jpg` (dense 10-30 fps passes, named below) and
  `shots/*_sheet.jpg`. The specs that rebuild `ref/` are in `S:cb/tools/refspec/`, and the builder is `S:cb/tools/ref.py`.
- **Line ids 1-23** are PLAN.md §3.0's ids. Id 12 (the bark) does not occur in this video.

---------------------------------------------------------------------------------------------------------------------

## 0. What this recording is, and the key findings

**The run.** The result panel at 379.5 reads, verbatim: 「도전 성공 / 胜利 / 일반 모드 / 홍련 / 월하곡 / 최고 기록 달성! /
02:22.04 / 사용한 세팅: 이브 프리셋 - 최대(새로운 게임+) / 받은 피해 21,798 / 퍼팩트 패링 횟수 24 / 퍼팩트 닷지 횟수 5 / 사용한
탄환 수량 0 / 사용한 전투 소모품 수량 0 / 사용한 회복제 수량 4 / [R] 재도전 [SPACE] 나가기」 (`ref/cs_ending.jpg` 379.50).
- It is **Normal mode**. PLAN.md's recording was Hard, no-hit and all perfect parries. Here the player is hit 13 times
  and heals 4 times, so this video also shows hits, guards, low-HP and heals.
- **레이븐모드**: the player character wears Raven's look (black hair with cyan-glowing tendrils, black suit; a skin or
  mod). The HUD is a retro dot-matrix skin: boss name 「:: Scarlet ::」, bars drawn as white squares, player rows
  `BU / BE / HP / SH`. The bar colours are the skin's. The yellow balance diamonds and every in-world effect are the
  game's own.
- **Nothing was skipped.** The intro (0-101.5) and the 60 % cutscene (160.5-203.0) play in full, with subtitles. PLAN.md
  only had the post-skip ends of both.

**Timeline.**

| span | what | HUD |
|---|---|---|
| 0.00-101.50 | **CS0 intro** (lines 1-11) | off; it fades in from 100.5, the boss HP bar fills 101.0-102.5 |
| 101.0-160.5 | **P1**: 100 → 61.0 % | on |
| 160.50-203.00 | **CS1** (60 %; lines 13-16, 홍련일섬, the field turns crimson) | off |
| 203.0-215.6 | **ghost gauntlet 1** (5-segment gauge full → 0 by perfect parries) | on |
| 215.6-222.4 | **repel counter 1** (in-engine cinematic, −4.1 %, then +4 diamonds) | **on** |
| 222.6-272.0 | **P2 regular patterns**: 55.7 → 5.3 % (the floor) | on |
| 275.0-290.0 | **ghost gauntlet 2** (gauge refilled at the floor → 0 by perfect parries) | on |
| 290.0-296.5 | **final repel counter** (5.3 → 0 %) | on |
| 296.5-373.1 | **ending** (duel, aerial duel, lines 17-23, the hat tip) | off |
| 373.1-380.7 | white flash → 胜利 glyph → result panel | — |

**Key findings.**
1. **Perfect parry**: a thin gold-orange streak spans the whole screen width through the contact point for 0.1-0.3 s.
   With it come a gold-white starburst at the player's blade, a ≈0.1 s hit-stop, and yellow lightning arcs crawling on
   the ground for ≈0.5 s. The boss loses one diamond 0.2-0.35 s later.
2. **Guard (not perfect)**: only a small gold spark at the blade. There is no streak, no hit-stop, no diamond loss and no
   visible HP loss.
3. **Perfect dodge**: a red-orange wash over the attacker and the dodger, with near-freeze slow motion for ≈0.35 s
   (7 t) and a red afterimage.
4. **Warning flashes**: there are three kinds, and all of them sit on her chest or body.
   - **Yellow**: a gold sphere-ring with a long horizontal flare.
   - **Purple**: the same ring in lilac with a 4-point star.
   - **Blue**: a blue sphere, seen once.

   None of the flagged attacks was ever parried. They were dodged, or they hit.
5. **Balance gauge**: **20** yellow diamonds under the boss HP bar. Only perfect parries remove them, one each. There is
   no regeneration over time; the only refill is **+4** in one step after the first repel counter. The video never
   shows a balance break or groggy (the minimum is 9/20).
6. **The second boss bar** has 5 segments. It is full at the start of each ghost gauntlet, loses one segment per
   perfect parry, and at 0 the final dive is deflected. Outside the gauntlets it fills while she lands hits, and her
   **space-cut ultimate** spends it.
7. **P2 has a full regular moveset**, which PLAN.md says the footage lacked. It includes a grab → aerial → sky-pillar
   combo, the space-cut ultimate (also in P1), purple X-crosses and huge diagonal bands. **There is no "down" window
   after the first repel**: she is back on her feet at once.
8. **The gauntlets here have no darkness**: the field stays crimson. Gauntlet 2 has no yellow tell and no moon discs.
   (This is Normal mode; PLAN.md's footage was Hard.)

---------------------------------------------------------------------------------------------------------------------

## 1. Player-side combat effects

### 1.1 Perfect parry (PP): `ref/parry_tiers.jpg`; dense `S:cb/video/dz/e9c.jpg`, `pp1.jpg`, `np1.jpg`, `g4b.jpg`
**What appears, in order** (A3 hit 1 at 117.1-117.6 is the clearest; `parry_tiers.jpg` 117.10-117.50):

| t from contact | effect |
|---|---|
| 0 (117.15-117.20) | Her lilac blade or sword-qi meets the player's blade. A **gold-white starburst** (≈0.5-1 m, 4-8 rays) appears at the contact point on the player's blade, between the two fighters and closer to the player. A **thin horizontal gold-orange streak** (a 1-3 px bright core with a soft glow) crosses the **entire screen width** at the height of the contact point. That is usually the player's chest height on screen; the measured y is 300-610 of 804, depending on the camera. |
| +0 to +0.07 s | The camera jolts (1-2 frames of radial motion blur, a slight punch-in). Frame-difference energy spikes at 117.15-117.22. |
| +0.07 to +0.17 s | **Hit-stop**: both fighters nearly freeze for ≈0.1 s (2 t; 117.25-117.32). |
| +0.1 to +0.3 s | The streak fades. Measured streak lengths: 100-300 ms, typically 230-270 ms (≈5 t). |
| +0.2 to +0.35 s | The boss loses one yellow diamond (the right-most lit one turns into a grey empty slot; §1.7). The player's BE row flashes a white cell (113.0, 117.6, 207.6; §1.8). |
| +0.1 to +0.7 s | Orange sparks scatter, and thin **yellow lightning arcs** crawl over the ground round the player (103.6-104.2, 113.0-113.4, 150.5-150.9, 151.9-152.3, 207.6-208.2, 280.0-280.4). |

- **No other slow motion and no screen-wide colour change**, except at the final-dive deflect (below).
- **Everything that was perfect-parried was an unflagged lilac sword-qi hit**: wrap crescents, verticals, flat rings, the
  ghost's cuts and diagonals. No yellow-, purple- or blue-flagged attack was ever parried.
- **PP log.** Flash time, then the attack, then the diamond step. P1: 103.43 (turning crescent, 20→19 at 103.6) ·
  112.57 (flat ring, →18 at 112.9) · 113.93 (vertical, →17 at 114.3) · 117.20 / 117.97 / 118.70 (A3 hits 1-3, →16 / 15 / 14
  at 117.4 / 118.3 / 119.0) · 133.67 (vertical, →13 at 133.9) · 150.13 / ≈150.6 / ≈151.0 / 151.6-151.8 (the ring combo, →12 /
  11 / 10 / 9 at 150.6 / 150.9 / 151.3 / 151.9). Gauntlet 1 (the gauge, not diamonds): 207.20 · 208.93 · 210.27 · 211.33 ·
  ≈212.77, and a further flash at 213.50 after the gauge is already 0. P2: 262.85 (ring, 13→12 at 263.1). Gauntlet 2:
  279.67 · 281.03 · 281.53 · 282.27 · 283.60, and 287.97 after 0. The two final deflects are 215.60 and 290.00. This is
  consistent with the panel's 24: 11 + 5 + 1 + 1 + 5 + 1. Whether the two after-zero flashes count is unclear.
- **Final-dive deflect** (the end of each ghost gauntlet; `parry_tiers.jpg` 215.70 / 290.25): the strongest version.
  - The **whole frame washes gold-white** for ≈0.25 s (215.60-215.85; 290.00-290.45), with the full-width streak and a
    large starburst between the two.
  - Then the camera cuts to the in-engine repel counter (§2.5).
  - Before it, the camera has already moved to a close two-shot (215.0-215.4, 289.4-289.8).
  - The same full-frame gold flash appears at the CS1 clash (160.80) and at the ending's clashes (300.4, 308.3-309.2,
    314.4).

### 1.2 Normal guard / imperfect parry: `ref/parry_tiers.jpg` 104.85, 149.10; dense `dz/ng1.jpg`, `dz/ng2.jpg`
- Instances: 104.82-104.95 (a big vertical crescent), 148.30 and 149.08-149.18 (two of the three big crescents), and
  263.2-264.2 (the later rings of the P2 ring combo).
- Look: a **small gold-white spark burst (≈0.3-0.5 m)** at the player's blade at the contact point, lasting ≈0.1-0.15 s,
  with a few orange sparks. The player slides back a little.
  - There is **no screen streak, no hit-stop, no lightning arcs and no diamond loss**.
  - **There is no visible HP loss**: the HP strip is identical at 147.9 and 149.5 (`S:cb/video/hud/sh_seq.png`).
- The video cannot separate the original's "imperfect" guard from a plain block. Both look like this.

### 1.3 Guard damage and hits taken
- **Chip / guard damage**: one candidate only. At 254.15-254.35 the aerial dive (P2 grab combo, §2.2 P-q) ends in a
  big orange-gold burst like a parry, but HP drops 100 → 97 % and no diamond or gauge is spent. It reads as an imperfect
  parry with chip damage. That is an inference; `ref/parry_tiers.jpg` 254.20, `ref/p2_aerial_grab.jpg` 254.20.
- **Being hit**: the hit spark on the player is **pink-magenta** (her sword-qi), never gold. There is no screen streak.
  The player staggers or is knocked down. The HP bar drops at once; there is no delayed "white" damage segment in this
  HUD skin.
- **Low HP**: at ≤ ≈40 % the screen edges pulse **red** at ≈1 Hz (127.55, 128.60, 129.55), and the HP squares turn pink
  (`ref/balance_ui.jpg` 127.30).
- **Hits taken** (13 HP losses; values are % of max HP read off the HUD):

| t | attack (§2.2) | HP |
|---|---|---|
| 113.60 | P-d rising fan | 100 → 87 |
| 119.5-120.0 | P-e A3 hits 4 + 5 | 87 → 62 |
| 125.5 | P-f leap-in diagonal | 62 → 53 |
| 126.6-127.0 | P-g yellow plunge | 53 → 38 |
| 133.50 | vertical crescent (the one before the PP at 133.67) | 100 → 87 |
| 153.0 | U space-cut ultimate | 87 → 76 |
| 159.1-160.0 | P-k yellow multi-cut | 76 → 57 |
| 212.50 | ghost wrap crescent (gauntlet 1) | 100 → 89 |
| 226.0-226.5 | P-l rising double crescent | 89 → 62 |
| 257.70 | P-q sky pillar | 97 → 79 |
| 261.5-262.0 | P-n diagonal bands | 79 → 37 |
| 265.5 | U space-cut ultimate (2nd) | 37 → 21 |
| 270.10 | P-o crescent (the player was starting a skill) | 100 → 93 |
| 285.0-286.0 | ghost dome (gauntlet 2), 3 steps | 94 → 35 |

- **Heals** (the panel's 4 회복제): 130.0, 206.6-207.0, 229.4-230.0 and 268.2-268.6. Each is a green or gold glow on the
  player for ≈0.5 s, with HP → 100 %.

### 1.4 Perfect dodge (PD): `ref/perfect_dodge.jpg`; dense `dz/pd5.jpg` (30 fps), `dz/pd1.jpg`, `S:cb/video/hud/pdx.jpg`
**Two certain cases.**
- **135.62-136.00** (the second yellow plunge, P-g):
  - The plunge lands at 135.55-135.62, and the player's body and surroundings are **washed red-orange / pink**.
  - The player's silhouette turns red; a **red afterimage** of the body is left behind by 136.00.
  - No HP loss.
- **146.95-147.30** (her lunge just before the triple crescents):
  - A **red wash covers the attacker**: her body, hat and blade are tinted pinkish-red, as if frozen, and a red haze
    fills the air round both.
  - Motion **nearly stops for ≈0.35 s** (146.95-147.30 = 21 f ≈ 7 t; frame-difference energy falls to 2-5 from ≈10-20).
    This is the slow motion.
  - The player slides past underneath. Normal speed returns with motion blur at 147.28-147.32, and the red fades over
    ≈0.2 s.
  - No HP loss.

**One probable case.** 136.90-137.40: thin red-orange arc trails curve round the player while the yellow → blue sphere
is up (`ref/unblockable_flashes.jpg` 136.88-137.25). No HP loss.

**Not visible.** The panel counts 5 PDs. The remaining ones are probably in P2 (the dodged dash cut at 232.2 and the
yellow leap at 242.6-243.2), where the crimson field hides a red tint.

**In short**: a red wash with near-freeze slow motion for ≈7 t, then a red afterimage. It happens at the moment the
attack would have hit. There is no HUD text.

### 1.5 Normal dodge: `dz/pd6.jpg` (243.78-243.98), `dz/nd2.jpg` (232.65-232.75)
A quick side-step or back-step with heavy motion blur and the skin's cyan particle streaks. There is no tint, no slow
motion, no HUD change and no camera effect. Of the dodged unflagged attacks, the P-c full-screen burst at 106.7 shows no
red wash, so it was a normal dodge or simply out of range.

### 1.6 Warning flashes on unblockable attacks: `ref/unblockable_flashes.jpg`; dense `dz/nd1.jpg`, `dz/bl1.jpg`, `dz/mix.jpg`, `dz/stars.jpg`
None of the three colours is ever parried in this video. Every flagged attack was dodged or hit the player. The footage
shows no colour legend.

**Yellow** (11 times).
- **Look**: a translucent **gold sphere-ring** (Ø ≈ 1.2-1.8 m) with a thin **horizontal flare line** ≈4-5 × the ring's
  width through its centre.
- **Position**: centred on her chest. When she is airborne it is on her body.
- **Timing**: it flashes in bright and fades over **0.2-0.3 s (4-6 t)**.

| yellow at | follow-up | yellow onset → hit |
|---|---|---|
| 106.20-106.45 | → purple → full-screen magenta burst (P-c) | 0.50 s (10 t) |
| 126.35-126.50 (in the air) | plunge (P-g) | 0.25 s (5 t) |
| 129.0 (far) | flat dash cut (P-h) | ≈0.9 s |
| 134.55-134.85 (in the air) | plunge (P-g), perfect-dodged | 1.0 s (20 t) |
| 136.80-137.00 | turns **blue** (below) | — |
| 151.93-152.10 | → purple → space-cut ult (U) | 0.75 s to the first white |
| 158.35-158.60 (big, close) | multi-cut (P-k) | 0.75 s |
| 231.20-231.30 (far) | flat dash cut (P-h) | 0.9 s |
| 237.00-237.25 | (the player's beta skill pre-empts it) | — |
| 242.60-242.85 | she glows gold and leaps away (P-y) | — |
| 264.40-264.60 | → purple → space-cut ult (U) | 0.6 s |

**Purple** (7 times).
- **Look**: the **same construction in lilac-magenta**: a thin ring (Ø ≈ 1.5 m) with a **4-point star** (long vertical
  and horizontal spikes).
- **Position**: on her chest.
- **Timing**: 0.10-0.15 s (2-3 t).
- **Instances**: 106.50-106.65, 152.35-152.45, 153.35-153.45 (inside the ultimate), 236.25-236.35 (small), 244.40-244.55,
  245.55-245.65 and 264.80-264.90. It always comes either 0.25-0.35 s after a yellow (just before P-c and U), or alone
  0.25-0.35 s before an X-cross (P-m).
- PLAN.md §4.3 A9 has this as decoration ("a lilac 4-point star + thin circle at her chest", `star4`). It is the purple
  warning (§3).
- It is easy to tell from her ordinary tells (pink sparkles at the chest or blade, 112.40, 133.0, 225.6, 231.4), which
  have no ring and no long spikes (`ref/unblockable_flashes.jpg` 112.40, 133.00).

**Blue** (once).
- At 136.80 a yellow ring appears on her. At 137.00-137.15 it **turns blue** and becomes a **translucent blue sphere
  enclosing her** (Ø ≈ 1.6 m), brightening at 137.45-137.60 and gone by 137.85 as she lunges. The player is not hit.

**What the colours mean.**
- **Shown here**: all three are attached to her big or multi-hit moves, and none is parried.
  - The yellow-flagged attacks were dodged (106.7, 129.9, 135.6, 232.2, 243.0) or hit (126.6, 153.0, 159.1, 265.5).
  - The purple-flagged X-crosses were avoided.
  - The blue lunge was avoided.
- **Not shown** (outside knowledge, consistent with the user's wiki text in `decisions.md` #12): in the original, all
  three are unparryable and can all be dodged; blue invites a dodge *through* (Blink) and purple a repulse.

**Not warnings**: the pink-lilac **sparkle glint** on her chest or blade before ordinary slashes (112.40, 129.2-129.6,
133.0, 225.60, 231.4-231.8). These attacks are parryable and were parried.

### 1.7 Balance gauge (yellow diamonds): `ref/balance_ui.jpg`; `S:cb/video/hud/dia_hi.png`, `dia_seq1.png`, `dia_p2.png`, track `S:cb/video/dia_track.txt` (10 fps)
**Layout.** One row of **20 yellow diamonds** sits directly under the boss bars, left-aligned with them. It spans ≈40 %
of the HP bar's width: diamonds ≈7 px wide at 10.5 px pitch, at 1920 px width. An emptied diamond stays as a **dim grey
square slot**, so the row always shows the maximum. The row appears with the HUD at 102.6, full.

**Depletion.**
- **Only perfect parries** remove diamonds: exactly one each, from the **right end**, 0.17-0.35 s after the PP flash.
  - P1: 20 → 9 (11 PPs; §1.1 log).
  - P2: 13 → 12 (one PP at 262.85).
- The player's normal attacks, beta skills (142-143, 226-229, 237-239, 240-241, 270-271) and the burst (159.8-160.4) took
  **no** diamonds.
- During the ghost gauntlets PPs drain the 5-segment gauge instead (§1.8). The diamonds stay at 9 through 203-222. The
  apparent dips at 214.7-219.0 are camera flashes.

**Refill.**
- **There is no passive regeneration**: 14 held for 15 s (119.0-133.9), 9 held from 151.9 through CS1 to 222.2 (70 s),
  13 held 222.3-263.0 (41 s), and 12 held 263.1-296.5.
- **The single refill is +4 in one step at 222.3** (9 → 13), right after repel counter 1, when normal play resumes.
- Nothing refills at the 60 % transition (203.0: 9) or at the 5 % floor (275.0: still 12).

**Balance break / groggy: not shown.** The minimum reached is 9/20. The video gives no groggy pose, duration or effect.
The user's decision (경직 + 받는 피해 증가, then refilled to full) has to be staged without a reference.

**Original vs the user's rule.** The original boss shows 20 diamonds. The user fixed **12** for bosses (4 grunt, 7
elite), so this is only a visual reference.

### 1.8 The boss's 5-segment gauge (the ultimate shield): `ref/balance_ui.jpg`; `S:cb/video/hud/bar2_hi.png`, `b2_p1g.png`; track `S:cb/video/b2_track.txt`
**Layout.** The boss HUD stack from the top is: name 「:: Scarlet ::」, the HP bar (two rows of white squares), then a
**second bar of 5 segments × ≈18 squares**, then the diamonds.

**Track.**

| span | gauge |
|---|---|
| 102.5 | empty |
| P1 | fills in ≈½-segment steps at 106.5, 107.0, 110.5, 113.5-114.5, 119.5, 120.0, 125.5 and 127.0 (full). These coincide with her big moves and her hits on the player (113.6, 119.5-120, 125.5, 126.6). |
| 127.0-153.9 | full |
| **154.0** | emptied at the end of the space-cut ultimate (U, 151.9-155.2) |
| 203.0 | **full** when the HUD returns after CS1 |
| gauntlet 1 | **−1 segment per PP**: 207.4, 209.0, 210.4, 211.4 and 212.7 → 0. The final dive is **deflected** at 215.6. |
| 213-226 | 0 |
| 226.0-252.5 | refills slowly (0 → 1.3 segments) |
| 253.0 | +1.5 (the aerial grab combo) |
| 257.5 | full |
| **266.5** | emptied by the second space-cut ultimate |
| 269.5 | 0.5 |
| **275.0** | **full in one step** when she sits at the 5 % floor |
| gauntlet 2 | −1 per PP: 279.5, 280.9, 281.5, 282.3 and 283.5 → 0. The final dive is deflected at 290.0. |

**Reading.**
- Inside the gauntlets this is PLAN.md §5's 5-pip shield: one segment per perfect parry, judged at the final dive.
- Outside them it charges while she lands hits and is spent by the space-cut ultimate. That is an inference; the HUD skin
  gives no label.

### 1.9 Player gauges (`ref/balance_ui.jpg` bottom tiles; `S:cb/video/hud/phud_seq.png`, `bu_seq.png`)
- **BU** (burst): ≈10 small cells, orange-lit when charged. It is emptied by the burst at 159.8-160.4 (a pale
  negative-like flash, then a white-cyan pillar).
- **BE** (beta): up to ≈16 cells drawn as 2×2 blocks, white when charged. Each PP adds or flashes one (113.0, 117.6,
  207.6). Beta skills spend them: white-cyan crescents, lightning rings and a white light pillar (142.2-143.2,
  226.2-229.0, 237.6-238.8, 240.2-241.2, 270.0-271.2).
- **HP**: two rows of white squares, pink when low.
- **SH**: a row of small cells. No change could be read at the guards.
- There is no on-screen text on a parry or dodge: no "Perfect" label and no numbers.

---------------------------------------------------------------------------------------------------------------------

## 2. The boss 홍련

### 2.1 Phases and HP thresholds (track `S:cb/video/hudt_track2.txt`, 2 fps)
| t | boss HP | event |
|---|---|---|
| 101.0-102.5 | 0 → 100 % | the bar fills as control begins |
| 122-143 | 99.8 → 76 % | the player's combos and a beta skill (142.5: −6.7 %) |
| 160.0 | **61.0 %** | the player's burst. **CS1 starts at 160.50**, cutting straight from the burst, with no pattern finishing first. |
| 203.0 | 59.8-60.0 % | the HUD returns. **The threshold is 60 %.** |
| 219.0 / 221 / 222 | 57.8 / 56.5 / 55.7 % | repel counter 1: −4.1 % in 3 steps |
| 226-243 | 53 → 16.9 % | the player's beta skills (226-229: −19 %) |
| 243-260 | 16.9 % | held through the grab and aerial combo |
| 271.0 | 6.5 % | |
| **272.0** | **5.3 %, floor** | held 272.0-292.0 although she is hit |
| 293.0 / 294.0 | 4.5 / 0 % | the final repel counter |

**Phases.**
- **P1**: 100 → 60 %.
- **CS1**.
- **P2**: gauntlet 1 → repel 1 → regular patterns → 5 % floor → gauntlet 2 → final repel.
- **Ending.**

**Arena looks.**
- **P1**: silver-white grass under a white full moon. The moon gate has glyph towers, stone stairs, stone lanterns,
  bamboo and cherry trees.
- **CS1** recolours the grass white → crimson.
- **P2**: crimson grass under a dark sky, with a **blood-red moon** in some P2 shots (254.8, 260.8-262.2, 291.8).
- **No darkness** at either gauntlet.
- **No floor decals** before any attack. The one ground mark is a brief vertical light line from the sky with a pink
  horizontal flash line at the player's feet at 257.00, 0.4-0.7 s before the sky pillar (P-q).

### 2.2 Attack patterns: `ref/tells_p1.jpg`, `ref/tells_p2.jpg`, `ref/ult_space_cut.jpg`, `ref/p2_aerial_grab.jpg`, `ref/gauntlet_repel.jpg`; dense `dz/mix.jpg`, 5 fps `dz/p5_*.jpg`
Colour of every sword-qi: **lilac-magenta** with a white-pink rim. "Parryable" means it was parried or guarded in this
video, or it carries no flag. Reach is read through a moving camera (±30 %); she is ≈1.7 m tall.

**P1**

| id | name (PLAN id) | times | tell → hit | structure, reach | parry |
|---|---|---|---|---|---|
| P-a | turning wrap crescent (A1) | 103.05-103.45 | she turns with a hat swing, magenta glow along the blade 103.05 → a huge **wrap-around crescent** (a near-vertical half-dome Ø ≈ 3-4 m round her, taller than the player) 103.20. **≈0.38 s (8 t)** from the first glow. | 1 hit | PP at 103.43 |
| P-b | vertical crescent pair | 104.6-105.4 | two big vertical crescents, the hit at 104.82 | 2 hits | guarded |
| P-c | yellow grand slash (A9) | 106.0-107.0 | a flat lilac ring round her waist 106.00-106.15 → **yellow** 106.20-106.45 → **purple** 106.50-106.65 → **full-screen magenta** 106.70-107.0 with a big flat ring explosion and RGB-split edges. **Yellow → burst 0.5 s (10 t).** | screen-wide | flagged; dodged |
| P-d | chest glint → flat ring → rising fan → vertical | 112.40-114.8 | pink sparkle on her chest 112.40 → **flat ring** at chest height 112.62 → **rising vertical fan** 113.60 → vertical crescent 114.00 → contact 114.4 → small slash 114.8. Glint → ring 0.22 s. | 4-5 hits, gaps 0.4-1.0 s; ring Ø ≈ 4 m | PP, hit, PP |
| P-e | five-crescent combo (A3) | 117.1-119.8 | h1 117.20, h2 117.97, h3 118.70, h4 119.20, h5 119.6-119.8 (a pink X / rising diagonal). Gaps **0.77 / 0.73 / 0.50 / 0.50 s = 15 / 15 / 10 / 10 t**. | 5 vertical / diagonal crescents, ≈3-4 m | PP ×3, then hit by h4 + h5 |
| P-f | leap-in diagonal | 125.2-125.55 | a short leap in 125.2, a diagonal slash 125.40, a second 125.55 | 2 hits | hit |
| P-g | yellow plunge (A10) | 125.95-126.9; 134.4-136.5 | she rises with a pink trail → **yellow in the air** (126.35-126.50; 134.55-134.85) → hangs (≈5-6 m up; the low-angle shot at 135.0) → a vertical pink plunge onto the player's spot (126.60; 135.55) → a ground burst (126.7-126.9; 135.6, with a second burst 136.0-136.5). Yellow → hit 0.25 s / 1.0 s. | burst Ø ≈ 4 m | flagged; hit / perfect-dodged |
| P-h | far yellow → flat dash cut | 129.0-130.2 (and P2 231.2-232.6) | small **yellow** far away (≈15 m) → lilac sparkle at her 129.2-129.6 (231.4-231.8) → slash 232.0 → a **huge flat elliptical disc of sword-qi** (Ø ≈ 8-10 m) sweeps at knee-to-waist height through the player's position (129.8-130.2; 232.15-232.6). **Yellow → cut ≈0.9 s.** | a gap closer from far | flagged; avoided |
| P-blue | blue lunge | 136.80-137.85 | a yellow ring on her 136.80 → **blue** 137.00 → blue sphere to 137.75 → lunge ≈137.8 | 1 lunge | flagged; avoided (probably a PD) |
| P-i | lunge + triple big crescents | 146.9-149.4 | a lunge at 147.0 (perfect-dodged), camera low → three **big crescents** sweeping across the frame at 148.2, 148.6-148.8 and 149.2-149.4 | 3 hits, ≈0.5 s apart | guarded ×2 |
| P-j | spinning ring combo | 150.0-151.9 (P2: 262.6-264.2) | flat lilac **rings** at her chest height, Ø ≈ 4-5 m, one every 0.4-0.6 s while she spins | 4 rings (P2 ≥ 5) | PP ×4 (P2: PP ×1 + guards) |
| U | **space-cut ultimate** | 151.93-155.2 (P2: 264.40-267.6) | always right after P-j. **Yellow** 151.93-152.10 → **purple** 152.35-152.45 → slash 152.60 → **white full screen** 152.68-152.77 → a **web of long pink-white straight cut lines across the whole screen** with chromatic fringes ("shattered glass") 152.85-153.5 → purple star again 153.35-153.45 → **second white** 153.60-154.2 → the cut lines burst outward → faded by 155.2. **Yellow → first white 0.75 s.** The 5-segment gauge empties at the end. | screen-wide; 1 hit landed (153.0 / 265.5) | flagged; unavoidable here |
| P-k | yellow multi-cut | 158.20-159.30 | crouch 158.20 → **yellow, big and close** (ring ≈ the player's height) 158.35-158.60 → the flare collapses into a pink sparkle 158.65 → a lilac charge glow on her body 158.80-158.95 → she dashes through: **several long pink straight cut lines** cross the screen 159.05-159.30. **Yellow → cuts ≈0.75 s.** | dash-through, multi-hit | flagged; hit |

**P2** (in addition to P-h, P-j, U and the gauntlets)

| id | name | times | tell → hit | structure | parry |
|---|---|---|---|---|---|
| G | ghost gauntlet (A8 / A13) | 205.8-215.6; 277.8-290.0 | §2.5 | | PP on each cut |
| P-l | rising double crescent (A2-like) | 225.60-226.00 | a pink glow low at her blade 225.60 → a rising lilac crescent 225.80 → a second 226.00. **Glint → hit 0.2 s (4 t).** | 2 hits | hit (−27 %) |
| P-m | purple X-cross | 236.25-236.9; 244.40-246.2 | **purple** star 236.25 → two crossing crescents + a star burst (an **X**) 236.60 → a dome 236.80-236.90 (→ yellow 237.0-237.25, pre-empted). Purple 244.40 → X 244.6-245.0; purple 245.55 → X 246.0 → flat slash 246.2. **Purple → X 0.25-0.35 s.** | 1-2 X's, Ø ≈ 3 m | flagged; avoided |
| P-y | yellow leap-away | 242.60-244.0 | **yellow** 242.60-242.85, then she glows gold and leaps up and away, landing far (≈12 m) at 243.5-244.0 | reposition | — |
| P-q | **grab → aerial combo → sky pillar** | 247.0-258.2 | a small lilac glint far off 247.00 → a lilac **ghost lunge (the grab)** 247.40-247.60 → the in-engine camera (HUD on): she clinches the player and throws her upward 247.8-249.4 → a purple-sky void, the player high in the air 249.6-250.6 → a mid-air blade lock 250.8-251.6 → a lilac ghost silhouette bursts 252.0-252.6 → a **huge diagonal magenta beam** 252.80-253.20 → a sparkle cloud 253.4-253.8 → she **dives** (a vertical pink blade line) 254.00-254.10 → **gold deflect, −3 %** 254.15-254.35 → the player falls back to the field under the blood moon 254.6-255.0 and stands 255.2-255.8 → she floats high 256.4-257.2 → a light line from the sky + a pink flash line at the player's feet 257.00 → a **pink-white light pillar** slams the player 257.40-257.80 (−18 %) → lilac shards 258.0-258.2 | P2 only | grab: no flag; dive: (imperfect) deflect; pillar: hit |
| P-n | diagonal bands | 261.00-262.05 | two **huge diagonal magenta bands** from the upper left (261.0-261.6), then a third (262.0). The camera shows the blood moon. | 3 hits | hit (−42 %) |
| P-o | crescents | 269.40-270.10 | a vertical crescent 269.40 → a big crescent 270.00 | 2 hits | hit (−7 %) |

**Not seen in this video**:
- A6, the back-blink with the bark 「거기가 아닐세.」. No subtitle appears anywhere in the fight.
- A4 + A5 as a separate leap dive + aerial ring spin. The leaps seen are P-g and P-y.
- R2's moon discs.
- A long downed state.

### 2.3 CS0: the intro (0.00-101.50): `ref/cs_intro.jpg`; `S:cb/video/dz/in1.jpg` … `in4.jpg`, `shots/intro_sheet.jpg`
Hard cuts at 11.83, 16.37, 29.38, 33.32, 38.82, 42.20, 46.27, 54.73, 59.85, 62.18, 70.70, 74.68, 80.03, 91.68 and 94.83.
The other transitions are continuous camera moves or dissolves. There is no name title card and no skip prompt (not
skipped). The player never guards, clashes or attacks in the intro.

| shot | t (dur) | framing | Eve (player) | 홍련 | line (subtitle verbatim, on-screen span) |
|---|---|---|---|---|---|
| I1 | 0.00-11.83 (11.8) | gameplay-style follow cam behind Eve, then wide | climbs the stone stair to the moon gate (0-5.3), walks into the moonlit silver-grass field toward the gate (5.3-11.8) | — | — |
| I2 | 11.83-16.37 (4.5) | side tracking shot through bamboo stalks | walks left → right through the grass, a lantern behind | — | — |
| I3 | 16.37-≈22.0 (5.6) | sky: the full moon + a cherry branch, slow pan; a single pink petal falls (21.3-22.5) | — | — | — |
| I4 | ≈22.0-29.38 (7.4) | macro, continuous from I3 | — | the petal lands on **her gloved hand resting on her knee** (seated, 24.7-25.3) and rolls off; rack focus to the sheathed hilt and the hat brim (26-29) | — |
| I5 | 29.38-33.32 (3.9) | ECU, her face in profile under the brim (eyes hidden), hilt in the foreground | — | seated, still | **1** 「꽃 속에 술 한 병 놓고,」 29.9-32.6 |
| I6 | 33.32-38.82 (5.5) | low close-up of her hand and a white plum-blossom sake bottle against the moon | — | lifts and pours the bottle | **2** 「벗 없이 혼자 술잔 드네.」 34.6-37.9 |
| I7 | 38.82-42.20 (3.4) | close-up: the bottle set down beside a small white cup on the rock | — | puts down the bottle, picks up the cup (40-41.3) | — |
| I8 | 42.20-46.27 (4.1) | her arm raises the cup toward the full moon (the cup over the moon) | — | raises the cup | **3** 「잔 들어 밝은 달 맞이하니,」 41.4-44.6 |
| I9 | 46.27-54.73 (8.5) | over the shoulder from behind-left; seated on the rock, hat on, back half to camera | — | arm out with the cup to the moon (46-49), brings it back and drinks (49.3-54.5) | **4** 「달과 나와 그림자 셋이 되었네...」 46.2-50.7 |
| I10 | 54.73-59.85 (5.1) | close, behind Eve's shoulder (the cyan glow of her hair-pin) | **looks up the lantern-lit stair toward the gate** (she has arrived) | (off-screen) | **5** 「그리고 이제 친구가 와 주었으니 월하독작이 아니라, 대작이 되겠구만.」 56.7-63.5 (one subtitle, not split) |
| I11 | 59.85-62.18 (2.3) | ECU: her hands on the sheathed sword | — | grips and slides the scabbard; a white glint along the blade (60-61.3) | (5 continues) |
| I12 | 62.18-70.70 (8.5) | low-angle wide: she stands on top of a rock / the gate, a small silhouette against the huge moon | — | stands, turns toward Eve (64-70) | **6** 「낭자, 내 말하지 않았던가?」 66.1-69.6 |
| I13 | 70.70-74.68 (4.0) | close-up of her face under the brim, smiling | — | smiles at Eve | **7** 「곧 또 보게 될 것 같다고.」 70.2-72.3 (starts on I12's tail) |
| I14 | 74.68-80.03 (5.4) | static wide of the empty field: bamboo, cherry, the gate tower | — | — | **8** 「아름다운 곳이지 않나?」 75.2-77.1 |
| I15 | 80.03-91.68 (11.7) | medium-wide front before the moon among bamboo → medium (87.3-91) | — | walks toward the camera with her right hand on the hat brim (80-87), tips the hat back (86-87); face visible, smiling | **9** 「신세진 것도 있겠다, 이 달 아래서...」 80.2-85.0; **10** 「한 수 가르침을 청하고 싶네만.」 85.3-88.8 |
| I16 | 91.68-≈93.3 (1.6) | low angle up the gate tower into a misty sky | — | **leaps** high off the gate (91.8-92.8), drops toward the camera (93.2); dissolve | — |
| I17 | ≈93.3-94.83 (1.5) | medium, low in the grass | — | **lands** crouched under the hat (93.5-94.5) | — |
| I18 | 94.83-≈97.2 (2.4) | ECU under the brim (only the mouth) | — | speaks, lifts the brim (96.8-97.2), revealing her eyes | **11** 「낭자 생각은 어떤가?」 95.1-98.4 |
| I19 | ≈97.2-≈99.9 (2.7) | medium close → medium, continuous | — | smiles with the **drawn sword held upright** before her (97.5-98.6), then swings into her stance (98.8-99.8: sword out low to the side, the hat dipping) | — |
| I20 | ≈99.9-101.5 | the camera swings back behind Eve into the gameplay camera (wide) | stands ready in the grass, facing her ≈6-8 m away | stance | — (HUD fades in 100.5-102.5) |

The intro lasts 101.5 s and the lines span 29.9-98.4.

### 2.4 CS1: the 60 % cutscene (160.50-203.00, 42.5 s, HUD off): `ref/cs1_60pct.jpg`; `S:cb/video/dz/cs1a.jpg`, `cs1b.jpg`, `cs1c.jpg` (30 fps)
Trigger: at 61.0 % HP, right after the player's burst (159.8-160.4). Hard cuts at 160.55, 160.77, 165.85, 171.55, 175.07,
177.82, 182.30, 184.83, 192.78 and 200.52. The player's HP is the same before and after, and CS1 deals no damage.

| shot | t (dur) | framing | Eve | 홍련 | line / effects |
|---|---|---|---|---|---|
| S1 | 160.50-160.77 (0.3) | wide | apart | apart | — |
| S2 | 160.77-161.85 (1.1) | side two-shot → close-up on the crossed blades and hands | **clashes**: blade lock, pushing | **lunges in**, blade lock | **full-frame gold clash flash** 160.80 (≈0.1 s) + orange lightning; sparks through the lock |
| S3 | 161.85-165.85 (4.0) | static wide toward the moon gate | tiny figure | tiny figure far away (pushed apart) | — |
| S4 | 165.85-171.55 (5.7) | **over Eve's shoulder** (Eve right foreground, back to the camera) | stands | ≈8 m away, facing Eve, hat on, sword low | **13** 「낭자, 대단하구만.」 168.1-170.7 |
| S5 | 171.55-175.07 (3.5) | high overhead shot of the grass in the wind | — | — | — |
| S6 | 175.07-177.82 (2.8) | behind her (Eve tiny, far) | — | **swings her hat**, which fills the frame (176.5-177.3) | **14** 「진심으로 가겠네.」 176.0-177.5 |
| S7 | 177.82-182.30 (4.5) | medium close-up, front | — | smiles, **raises the white sake bottle** (179.5-181.5) | — |
| S8 | 182.30-184.83 (2.5) | Eve medium close-up beside a stone lantern | watches her, hand at her weapon | — | — |
| S9 | 184.83-192.78 (8.0) | her close-up | — | eyes-closed smile (185), **offers the bottle toward Eve** (186-187), looks down (187.5-188.5), **drinks from the bottle** (189-191.5) | — |
| S10 | 192.78-≈198.9 (6.1) | ECU under the brim (only the mouth) | — | **wipes her mouth with her forearm** (193-196.5), lowers the arm (197); a big pink petal drifts across her face from frame-left (198.0-198.6) | **15** 「천지만물을 벤다는 건...」 197.3-199.1 |
| S11 | ≈198.9-200.52 (1.6) | ECU of the petal (focus); a thin glowing line already crosses it | — | — | **16** 「이런 것일세.」 199.7-201.5 |
| S12 | 200.52-200.80 (0.28) | full-frame overlays | — | — | **negative** frame 200.52-200.67 (0.15 s = 3 t: an inverted cyan-white field with a dark diagonal band lower-left → upper-right), then **pale pink-white** 200.68-200.80 (0.12 s ≈ 2.5 t) with a thin dark-red → gold diagonal line |
| S13 | 200.80-203.00 (2.2) | wide behind Eve in the white grass | stands (silhouette); not hurt | far (a petal burst at her) | the cut petal's halves blow away (200.82); a **red slash line crosses the screen at Eve's chest height**, lower-left → upper-right (200.85-201.3), with a pink petal burst at her; the grass recolours **white → crimson** (201.3-202.0); HUD back 203.0 |

### 2.5 The ghost gauntlets and the repel counters: `ref/gauntlet_repel.jpg`; 5 fps `S:cb/video/dz/p5_203.0.jpg`, `p5_210.2.jpg`, `p5_217.4.jpg`, `p5_275.0.jpg` … `p5_289.4.jpg`; 30 fps `dz/pp1.jpg`, `dz/g4b.jpg`
**Gauntlet 1** (HUD on, crimson field, no darkness, no warning banner).
- She stands far (≈20 m) from 203.0 to 205.6.
- 205.80: a **lilac flash on her (ghost form)**, then a lilac burst at 206.0.
- 206.6-206.8: the translucent **lilac ghost** dashes in from the player's right.

Cuts:

| t | cut | result |
|---|---|---|
| 207.20 | ring cut | PP; the ghost spins and rises 207.6-208.2, vanishes and reappears at 208.4 |
| 208.95 | ring cut | PP; reforms 209.4-209.8 |
| 210.27 | ring | PP; a rising diagonal follows 210.8-211.2 |
| 211.33 | diagonal | PP; the ghost bursts upward 211.6-212.0 |
| 212.45-212.6 | wrap crescent | **hit**, −11 % |
| 212.77 | low ring | PP (faint); the gauge is 0 from 212.7 |
| 212.8-213.2 | **spin dome** round the player | — |
| 213.50 | vertical crescent | PP |

The ending of the gauntlet:
- 214.0-214.4: the ghost rises.
- 214.60: a **lilac light column** with yellow lightning (the dive).
- 215.0-215.4: a close in-engine camera; she is in her normal colours.
- **215.60: the gold deflect** (§1.1).

Cut spacing: 1.1-1.75 s between counted cuts (207.20 → 208.95 → 210.27 → 211.33 → 212.77), which is 22-35 t.

**Repel counter 1** (215.6-222.4; the **HUD stays on**; an in-engine cinematic).

| t | beat |
|---|---|
| 215.8-216.6 | blade lock, close |
| 216.8-217.8 | Eve **grabs** her, the bodies pressed together |
| 218.00 | a **gold-white burst on her hat** (Eve's strike) |
| 218.2-218.8 | Eve's cyan slashes |
| 219.0-219.6 | she is tipped over |
| 219.8-220.6 | she is **thrown over Eve's shoulder** (the hat flips) |
| 220.8-221.0 | she **lands on her back** |
| 221.2-221.8 | Eve stands over her |
| 222.00 | a **gold-white impact burst** (Eve's finishing kick) |
| 222.2-222.4 | Eve flips back |
| 222.6 | normal play: she is up and ≈12 m away by 224.0 (**no down window**) |

Boss HP: −2.0 % at 219.0, −1.3 % at 221 and −0.8 % at 222. Diamonds **+4** at 222.3.

**Gauntlet 2** (from the 5 % floor).
- At 272.0 she backs off to the floor HP. The gauge refills to full at **275.0**. She stands near the player, hat on,
  from 275 to 277.
- 277.80: the lilac flash (ghost form).
- 278.0-278.6: lilac mist; 278.6-279.0: the ghost dashes in from the right.

Cuts:

| t | cut | result |
|---|---|---|
| 279.2 | ring | — |
| 279.67 | ring | PP |
| 281.03 | ring | PP |
| 281.53 | diagonal | PP |
| 282.27 | diagonal | PP |
| 283.60 | ring | PP → gauge 0 |
| 283.8-284.4 | the ghost spins and rises | — |
| 284.6-286.0 | **pink dome** | hits the player 3 times (−59 %) |
| 285.6-287.6 | further ghost cuts, a dome / ring | — |
| 287.97 | — | PP |

The ending of the gauntlet:
- 289.0-289.2: a lilac column (the dive).
- 289.4-289.8: close camera, normal colours.
- **290.00: the gold deflect.**

There is no yellow tell, no moon discs and no darkness.

**Final repel counter** (290.0-296.5, HUD on).

| t | beat |
|---|---|
| 290.6-291.2 | blade lock close-up, sparks |
| 291.4-291.6 | she is grabbed |
| 291.8-292.4 | the blood moon behind them |
| 292.6 | clash sparks |
| 293.0-294.6 | she is tipped and thrown; the hat flies |
| 295.0 | she lands on her back |
| 295.4-296.2 | Eve stands over her |
| 296.4 | the last kick; the HUD goes off at 296.5 |

The boss HP falls 5.3 → 4.5 → 0 % over 293-294. It is the same choreography as repel 1.

### 2.6 The ending (296.5-380.7): `ref/cs_ending.jpg`; `S:cb/video/dz/en1.jpg` … `en3.jpg`, `shots/ending_sheet.jpg`
| shot | t (dur) | framing | Eve | 홍련 | line / effects |
|---|---|---|---|---|---|
| E1 | 296.5-299.6 (3.1) | medium two-shot | faces her | rises from the ground (296.4), sword raised (297.7-298.4) | — |
| E2 | 299.6-301.7 (2.1) | clash close-up | **blade lock** | blade lock | a gold spark on her hat (299.1); **gold lightning burst** between the blades (300.4); push (301.0-301.7) |
| E3 | 301.7-305.7 (4.0) | low angles on Eve | slashes and dashes past (a cyan streak, 303.0) | — | — |
| E4 | 305.7-308.3 (2.6) | wide | runs at her | runs at Eve | two tiny figures |
| E5 | 308.3-309.2 (0.9) | full frame | — | — | **gold clash flash** |
| E6 | 309.2-315.3 (6.1) | **aerial duel** in a purple sky | trades blows in the air | trades blows in the air | clashes 311.1, 313.1 (a vertical gold line), 314.4 (a big gold flash), 315.0; the blood moon (310.4) |
| E7 | 315.3-316.4 (1.1) | wide | flies apart | flies apart | in front of the blood moon and the gate tower |
| E8 | 316.4-320.1 (3.7) | static wide: crimson field, gate, blood moon (empty) | — | — | — |
| E9 | 320.1-≈324.7 (4.6) | medium-wide | — | standing, **sheathes** (a swing 321-322, sheathing 322.4-323.7), the blood moon behind | **17** 「낭자, 여기까지 하세.」 322.2-325.1 |
| E10 | ≈324.7-329.0 (4.3) | close-up of her face under the brim | — | smiles | **18** 「대단하네, 좋은 수련이 되었어.」 325.9-329.2 |
| E11 | 329.0-332.9 (3.9) | Eve medium close, front | raises a hand, then lowers it, looking at her | — | — |
| E12 | 332.9-≈345.0 (12.1) | medium front → her back → over her shoulder | — | **turns away** (the hat swings, 333-338), her back to the camera (336-338), looks back over her shoulder (339-344) | **19** 「이제 정말 가야겠네.」 333.5-335.6; **20** 「다음 번에 만나면, 그땐 같이 한잔 하면 좋을 텐데...」 337.9-343.8 |
| E13 | ≈345.0-346.9 (1.9) | Eve medium close, front | listens | — | — |
| E14 | 346.9-351.8 (4.9) | wide: Eve left foreground, her ≈10 m right | stands | stands | **21** 「달빛과 바람을 안주 삼아... 말일세.」 348.3-354.7 |
| E15 | 351.8-≈357.5 (5.7) | behind her shoulder: the huge **blood moon** fills the right half | — | **looks up at the moon** | (21 continues) |
| E16 | ≈357.5-≈364.7 (7.2) | medium-wide front in the crimson grass | — | faces Eve and gestures with an open hand (359-361) | **22** 「어디 보자, 낭자네에선 이렇게 인사한다고 들었는데...」 358.0-364.4 |
| E17 | ≈364.7-373.1 (8.4) | close-up | — | raises her **left hand to the brim** (365-366), eyes closed (367), **pulls the brim down over her eyes** (a bow, 368-372; the pink-lit hat fills the frame); fades to black 372.4-372.87 | **23** 「당신의 기억이 이어지기를.」 365.4-369.8 |
| — | 372.87-373.10 | black (0.23 s) | | | |
| — | 373.13 → 373.8 | a **white flash** (luminance 238) fading over 0.65 s | | | |
| — | 374.10 | a pale-pink full screen, the **胜利** glyph zooming in | | | |
| — | 374.5-380.7 | the result panel over a dark blurred background: a purple glow, 「도전 성공」, a large 「胜利」, a yellow tag 「일반 모드」, 「홍련」 / 「월하곡」, 「최고 기록 달성!」, the time and the stats (§0) | | | |

The lines match PLAN.md §3.0 ids 13-23 exactly, including line 15's 「...」 and line 16's period. No line appears outside
CS0, CS1 and the ending.

---------------------------------------------------------------------------------------------------------------------

## 3. Differences from PLAN.md

### 3.1 Footage and effects (PLAN §1)
1. **The recording itself.** PLAN §1.1 used one Hard, no-hit, perfect-parry run with the intro and CS1 skipped.
   - This one is **Normal** (「일반 모드」), with 13 hits and 4 heals, and **nothing skipped**.
   - The player is in a Raven skin, and the HUD is a retro skin that labels the boss 「:: Scarlet ::」.
   - The panel's clear time is 02:22.04; PLAN's run was 01:20.52.
2. **The purple warning is real.** PLAN treats A9's "lilac 4-point star + thin circle at her chest" as a star glint
   (`star4`). It is the **purple warning flash**: it has the same ring-and-flare structure as the yellow one, comes
   before P-c, U and the P2 X-crosses, and appears 7 times.
3. **There is a blue warning** (137.00-137.75), which PLAN does not have.
4. **The diamond row is not decoration.** PLAN §1.6 drops it ("balance gauge 20 → 24 pips, Q-A11"). The user now wants a
   balance gauge (decisions.md #7). This video shows:
   - **20** diamonds (not 24);
   - **one per perfect parry**, from the right;
   - **no regeneration over time**;
   - **+4 after the repel counter**;
   - **gauntlet PPs drain the 5-segment gauge, not the diamonds**;
   - **no groggy reached** (min 9).
5. **The 5-segment gauge is not only a gauntlet shield.** It is visible all fight, fills as she lands hits, is spent by
   the space-cut ultimate, is full at each gauntlet start and drains one per PP.
6. **The parry feedback is confirmed** for PLAN §1.3's "orange / gold screen-wide parry streaks". Added here:
   - a ≈0.1 s hit-stop;
   - the yellow ground arcs after a PP;
   - the much smaller guard spark;
   - the full-frame gold wash at the final-dive deflect.
7. **The perfect dodge is a red wash with ≈0.35 s of near-freeze**, not just the "pale afterimage" PLAN §1.3 lists.
8. **No floor decals**, which agrees with PLAN §1.4. The one ground mark is the sky pillar's flash line at the player's
   feet (257.00, 0.4-0.7 s before the hit; P2 only).

### 3.2 Phase structure (PLAN §0, §4.6)
9. **P2 has many regular patterns.** PLAN §0.1 q5 and Q-A1 assumed the footage had none. P2 here includes:
   - P-l rising double crescent;
   - P-h yellow dash cut;
   - P-m purple X-cross (×3);
   - P-y yellow leap-away;
   - **P-q grab → aerial → dive → sky pillar**;
   - P-n diagonal bands;
   - P-j ring combo;
   - **U space-cut ultimate**;
   - P-o crescents.

   This replaces the "P1 kit + R1-R3 cut from the gauntlets" default, at least as reference.
10. **The space-cut ultimate (U) is a regular move in both phases**, always right after the ring combo:
    yellow → purple → white → glass web → white. PLAN has no such move in the fight. Its white / web look resembles
    PLAN's CS1 overlays, but here it is a gameplay attack.
11. **The yellow multi-cut (P-k)** in P1 is not in PLAN.
12. **There is no down window after the first repel.** PLAN §3.5 has her lying ≤ 200 t with normal damage, then a
    kip-up. Here she is standing and far away within 2 s (222.6-224.0), and P2's regular fight starts.
13. **The first gauntlet comes right after CS1, with no SQ1 or darkness.** PLAN §3.3 / §6.5 plays SQ1 (the re-hat, the
    stand-off, the darkness at T0 − 17, the hand to the brim). Here: the HUD returns at 203.0, she stands far for
    2.8 s, then the lilac flash at 205.8. The field stays crimson, and there is no warning banner.
14. **The 5 % gauntlet is the same moveset as the 60 % one.** PLAN's A13 has a yellow tell, three moon discs and a run-in.
    Here (Normal mode) gauntlet 2 has no yellow, no discs and no darkness. Its lead-in matches PLAN's `lead_stand`
    loosely: at the floor (272.0) she steps back, the gauge refills at 275.0 and the ghost comes 2.8 s later. Gauntlet
    2's dome hit the player for −59 % — a real threat even without a fail branch.
15. **The repel counters keep the HUD on**, unlike PLAN §3.4's HUD-off convention for CS2 / CS3.
    - Repel 1 deals −4.1 % in 3 steps (PLAN: −4.5 %).
    - Its choreography matches PLAN's R0-R8 (blade lock, grab, strike on the hat, tip, throw over the shoulder, she
      lands on her back, kick).
    - The final repel takes the boss from the 5.3 % floor to 0 before the ending (PLAN: 5.2 → 2.3 %, then a lethal hit).
16. **The CS1 trigger** is the hit that crosses 60 %, here the player's burst. CS1 starts at once (160.50), without
    "the running pattern finishes first" (PLAN §3.2), though she was not mid-pattern here.

### 3.3 Cutscenes (PLAN §3)
17. **CS0 differs from PLAN §3.1's staging of lines 1-10.**
    - **Matches**: she sits on a rock with a white sake bottle and a cup, pours, raises the cup to the moon, drinks
      (lines 1-4).
    - **Differs**:
      - The real intro opens with **Eve's arrival** (I1-I2, 16 s) and the moon (I3).
      - Line 5 plays over **Eve looking up the stair**, then her hand on the sword.
      - For line 6 she is **standing on the rock or gate against the moon**.
      - Lines 9-10: she walks toward the camera tipping her hat.
      - Then she **leaps off the gate and lands near Eve** (I16-I17) before line 11.

      PLAN has her rise, turn and walk in (E5-E10) instead; the leap is new.
    - The draw is shown as the sword already upright at 97.5 (I19), followed by the stance.
    - **No name title card** appears; PLAN puts 「홍련」 / 「월하곡」 at the draw.
    - Real length: 101.5 s (lines 29.9-98.4); PLAN's CS0 is 640 t = 32 s.
18. **CS1 is 42.5 s** (PLAN: 213 t = 10.7 s).
    - **Matches PLAN**: the lunge → gold clash → blade lock (C0-C1), apart (C2-C3), line 13 / 14, the petal (C5), the
      **negative** (3 t) + **pink-white with the diagonal line** (2.5 t) (C6-C7), and the red slash across the
      player's chest + the field turning crimson (C8). The real C6 / C7 are 3 / 2.5 t (PLAN: 4 / 4 t).
    - **Added**: an overhead grass shot (S5), the hat swing (S6), the **drinking beat** (S7-S9: she raises the bottle,
      offers it to Eve, drinks, wipes her mouth) and Eve close-ups (S8).
    - **Absent**: PLAN's C4 black overlay.
19. **The ending matches PLAN §3.7's beats.** It also opens with a ground-level duel and a wide run-in (E1-E5) before
    the aerial duel (E6). PLAN's E1b ground slash (A12) and the △ moment are not seen in this cut. The end card: a fade
    to black, 0.23 s of black, a white flash, then 胜利 and the result panel — PLAN's coda replaces this anyway.
20. **No bark 「거기가 아닐세.」** and no A6 back-blink in this run. The line is footage-only in PLAN, so this
    recording neither confirms nor removes it.

### 3.4 Timings worth reusing (as references for the telegraph rule)
- **Unflagged slashes**: glint → hit 0.2-0.4 s (4-8 t). A3's chain gaps are 15 / 15 / 10 / 10 t.
- **Yellow onset → hit**: 0.25-1.0 s (5-20 t): plunge 5 / 20, A9 burst 10, multi-cut and U 15, dash cut 18.
- **Purple → hit**: 0.25-0.35 s (5-7 t).
- **Blue sphere**: ≈0.75 s (15 t) to the lunge.

These are faster than PLAN's telegraph floor (≥ 12 t, ≥ 20 t for big or yellow), so PLAN's stretching stays necessary.

---------------------------------------------------------------------------------------------------------------------

## 4. Notes for lanes C / B / H (observations mapped onto `decisions.md`)
- **Parry tiers** (decisions #6, #8). The original's two visible tiers are the gold full-width streak with a hit-stop
  (perfect) and the small gold spark (guard). Tier 1 / tier 2 of the pack have no separate original look. A natural
  mapping:
  - **tier 3** = streak + starburst + 2-t hit-stop + ground arcs;
  - **tier 2** = a larger spark burst with a short streak segment;
  - **tier 1** = a small spark.
  The perfect parry's diamond step lands 4-7 t after the flash in the original.
- **Perfect dodge** (decisions #9): a red wash over the attacker and the player with ≈7 t of slow motion, then a red
  afterimage. Nothing appears on the HUD.
- **Flashes** (user decision): a ring + flare (yellow), a ring + 4-point star (purple), a sphere (blue). They sit on the
  boss's chest, last 2-6 t, and come 5-20 t before the hit. No text.
- **Balance UI** (decisions #7): a row of yellow diamonds under the HP bar, left-aligned. Spent slots stay as dim grey
  squares, and they are removed from the right. The original refilled +4 only after a scripted counter. The user's
  rule (time regeneration, refill to full after groggy) is the pack's own.
- **Cutscene camera references for H** (decisions #1, #10). Most shots are close-ups or ECUs of her (face under the
  brim, hands, bottle, cup) and over-the-shoulder shots from behind Eve. Wide shots are kept for establishing (the
  moon, the gate, the field). Eve's acting:
  - **CS0**: arrives, looks up.
  - **CS1**: blade lock, stands, watches.
  - **Repel**: grab, throw, kick.
  - **Ending**: duel, aerial clashes, listens.

---------------------------------------------------------------------------------------------------------------------

## 5. Files
**Committed `ref/`** (each ≤ 640 px wide, ≈1.3 MB in total):

| file | content |
|---|---|
| `parry_tiers.jpg` | the PP sequence (117.10-117.50), PP on a ring and on a ghost cut, guards, a hit taken, the aerial chip deflect, the two final-dive deflects |
| `perfect_dodge.jpg` | the two certain PDs (135.55-136.00, 146.95-147.30) and the probable one (136.95) |
| `balance_ui.jpg` | the boss HUD (HP / 5-segment gauge / 20 diamonds) at 15 moments, and the player HUD (BU / BE / HP / SH) |
| `unblockable_flashes.jpg` | yellow ×8, purple ×4, the yellow → blue sequence, and two non-warning glints |
| `cs_intro.jpg` | CS0, 24 key frames |
| `cs1_60pct.jpg` | CS1, 21 key frames, including the negative and pink-white frames |
| `gauntlet_repel.jpg` | ghost gauntlet 1 + repel counter 1 |
| `ult_space_cut.jpg` | the space-cut ultimate, P1 and P2 |
| `p2_aerial_grab.jpg` | the P2 grab → aerial → sky pillar |
| `tells_p1.jpg` | P1 pattern tells P-a … P-j |
| `tells_p2.jpg` | P-k, P2 tells P-l … P-o, gauntlet 2 |
| `cs_ending.jpg` | the final repel, the ending shots, the end card and the result panel |

**Scratch only** (`S:cb/video/`, not committed):
- the overview sheets `ovs/ov_000…380.jpg` (1 fps) and `f4s/s_0100.0…0317.5.jpg` (4 fps, 100-320 s);
- the dense sheets `dz/*.jpg`: `e9a/e9b/e9c` (the yellow → blue sequence), `u1/u2` (147-155), `c0` (158-162), `pp1`,
  `np1`, `g1`-`g8`, `g4b`, `pd1`-`pd6`, `nd1`, `nd2`, `ng1`, `ng2`, `bl1`, `mix`, `stars`, `cs1a/b/c`, `in1`-`in4`,
  `en1`-`en3`, and `p5_*` (5 fps P1 / P2);
- the shot sheets in `shots/`; the HUD crops in `hud/`;
- the HUD tracks: `hudt_track2.txt` (boss HP, 2 fps), `dia_track.txt` (diamonds, 10 fps), `b2_track.txt` (the
  5-segment gauge, 10 fps), `phud_track.txt` (player bars, 2 fps);
- the frame metrics `metrics.npy` and `streak.npy` (20 / 30 fps).

The dense frame dumps were deleted after reading.
