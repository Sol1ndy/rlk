# Guardian (파수꾼・타락, module `guardian`): ground-telegraph audit

Scope: every hazard the Guardian module can emit, at release HEAD `039b911` (`/home/user/rlk`, read only), checked
against the reference footage under THE RULE: keep a pre-hit ground telegraph only when the footage shows one (and
trim it to what the footage shows); otherwise remove it (`#hzQuiet 1`, no module decal) and let the player read the
motion, the sound and the non-ground fx.

- Code: `roguelike/tools/mboss_guardian/{core,p12,p34,p56}.py`, framework `roguelike/tools/build_mboss_core.py`
  (`hz/make`, `hz/init`, `hz/tick`, `hz/draw`, `hz/strike`, `hz/flash`, `opts_reset`), `mboss_lib.hz_opts`.
- Ticks are **played** ticks on the pattern clock `#gdPT`, computed from `tools/mboss_guardian_rig_manifest.json`
  via `api.ev` / `api.rt` (retimed clips).
- Footage: `S/mboss/src/m1.mp4` … `m4.mp4` and `guide.pdf`. `S` is the scratchpad
  `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`. Frames were extracted with
  ffmpeg at the times listed and viewed; the evidence sheets are in `S/tele/gd/evidence/`.
- Framework behaviour: a hazard without `#hzQuiet 1` draws a dust outline and a progress outline every 4 t until
  the hit (`hz/draw`), then a strike flash (`hz/flash`: white outline, fill and explosion particles). `#hzVis N`
  routes create/strike/end events to the module's decal (`p/<key>/vis`).

## Result table

| id | pattern | hazard | current pre-hit telegraph | footage (ground before the hit) | decision | what the player reads instead; tell → hit |
|---|---|---|---|---|---|---|
| ENT | entrance (core `intro/*`) | disc r 3.6 at the spear plant, 100 % (intro 34) | **Framework outline + progress outline + strike flash** (not quiet), from intro 16 (18 t). Also a star glint card 7.4 b above the plant spot, a chime and a power-select sound | **Never filmed.** All four videos start mid-fight (m1/m2/m3/m4 at 0.05 s; ev 16). PDF p.73 says she appears "어떤 표시도 남기지 않은 상태에서" (with no marker at all, ev 17) | **REMOVE** (`#hzQuiet 1`) | The hit lands away from the boss, who is hidden until the clip starts. Non-ground precursor: the sky glint at 16, then the spear falling from 7 b (clip 20-34) with its gold dust trail and the beacon-deactivate whistle. **Glint → hit 18 t** (≥ 12). Impact visual exists: burst, a ground ring card growing to ≈ r 3.3, 8 radial shards, gold block debris. The player arrives 17.5 b from the plant. |
| P1a | P1 공간 찌르기, thrust 1 (`p12` lock1) | line 9.3 × 2.9 b from the coil spot C through T, 100 % (21) | Quiet hazard + **module lane decal** vis 11: translucent gold fill, gold rims and caps, an amber bar growing over 10 t, then a white flash. Shown from lock 11 (10 t) | m1 0.20-1.62 s: the charge streak runs along the spear, glint at 1.17, lunge 1.55, hit 1.62. **No ground marker** (ev 01) | **REMOVE** | Wind-up pose with sweep and riptide sounds at 0. Charge streak on the spear from 3, with shimmer and chimes at 5, 7, 9 and 11. She stops tracking at 11. Glint and chime at 14, coil back 15-19, a 3 b lunge 19-21. **Clip start → hit 21 t; streak → hit 18 t; glint → hit 7 t.** Impact visual exists (`hit_fx`): burst, glow, shock ring, dust, cubes, debris. |
| P1b | P1 thrust 2 (`p12` lock2) | line 8.4 × 2.7 b from the dive spot D through U, 115 %, KB 4 (46) | Quiet + **lane decal** vis 12 (as above), from lock 34 (12 t) | m1 2.00-3.15 s: she flies up and back and hovers 4-6 m away, pointing the spear down at the player, then dives. **No ground marker** (ev 02) | **REMOVE** | She rises at 31 (flap and riptide) and glides to D in the air from 34 to 42, facing the locked point. Flap at 37. Dive-charge dust runs along the spear from 39 with a power-select sound. Dash 44-46 with a sweep sound. **Rise → hit 15 t; relocation → hit 12 t** (the plan's 12 t floor). Impact visual exists: big `hit_fx`, the dive streak along the lane at 45-46 lingering to 52, cubes. |
| P2 | P2 공간 투창 (`p12` javelin) | line 1.2 b wide from the glyph point to the arena edge, 130 %, over 27-28 | Quiet + **lane decal** vis 21 (fill, rims, an amber bar to `#gp2Len`), from lock 17 (10 t) | m1 6.00-7.65 s: the glyph floats in the air at chest height (6.30-6.87), a vertical beam at 7.03, the launch disc in the air at 7.55, the projectile at 7.65. **No ground line** (ev 03) | **REMOVE** | Spin and whooshes 0-8, vanish flash at 9. The **air glyph** (a spinning star at her right-front, chest height) 10-19 with resonate and chimes. She stops turning at 17. **Beam** at 20 with beacon-activate, the spear re-forms at 22, release burst at 26 (throw, firework blast, attack line). **Glyph → hit 17 t; beam → hit 7 t.** Every non-ground precursor in the footage (glyph, beam, launch disc, flying spear) is in the game. Impact visual exists: a hot streak along the whole lane at 27-28, debris every 2 b, trail cubes, the visual spear. |
| P3 | P3 공간을 집행하는 시련, slam (`p34`) | disc r 6 centred 3.5 b ahead, 160 % (20) | **Framework outline + progress outline + strike flash** (not quiet), plus **module** vis 31: a thin gold ring card widening 0.86 → 1.0 and a faint amber dust fill (17 points every 2 t). From 7 (13 t) | m1 11.42-12.25 s: a **ground ring** appears at 11.42 small, is full by ≈ 11.70 and stays: thin gold rim, faint translucent amber fill, **no progress or inner ring**. Impact 12.21-12.30, a 17-18 t lead (ev 04, 05) | **TRIM** | Keep the vis-31 ring card and the faint amber fill. Remove the framework outline, progress outline and strike flash (`#hzQuiet 1`). The module already has its own impact (pillar, white-gold flash glow over the ring, shock ring, blades). Optional fidelity: start the ring at ≈ 0.4 and grow it to full over 5-6 t. **Raise 0 → hit 20 t; ring → hit 13 t.** |
| P4-pull | P4 어둠 속에서 퍼지는 공간, pull (not damaging) | undodgeable relocation 1 b in front of her (24), no damage | A cage of black, red-edged cubes stacking up the player from 7, a red aura, a screen vignette and flash | m1 15.50-17.05 s: the same cage of cubes at the player's feet and up the legs, plus the screen effects (`understand/m1/sheet_pull_cage_*`) | **KEEP** (a mechanic marker in the footage, not a ground decal, not a hit) | Aura 0, cage 7, flash 20 → relocation 24 (24 t ≥ 20). Unchanged. |
| P4-s1 | P4 swing 1 (`p34`) | 360° sector r 6.8, 120 % (51) | **Framework outline (full circle) + progress circle + strike flash** (not quiet), plus **module** vis 41: a gold ring card at r 6.8 that turns. From the swing-clip start 36 (15 t) | m1 22.00-23.55 s: wind-up 22.6, hold 22.9-23.45, swing 23.55. **No ground marker** (ev 06) | **REMOVE** (`#hzQuiet 1`, drop `#hzVis 41` and its ring card) | Relocation at 24. Swing clip at 36: the spear is laid behind her shoulders and the wing raised, with a riptide sound. At 41 a hold glint star, chime and power-select, with gold motes on the spear. Riptide and knockback sounds at 49, swing at 51. **Clip start → hit 15 t; hold glint → hit 10 t; relocation → hit 27 t.** Impact visual exists: gold crescents following the tip at r 6.65, a dust ring at r 5.7, sweep particles, dark cubes. |
| P4-s2 | P4 swing 2 (`p34`) | 360° sector r 6.8, tilted, 120 % (64) | As s1, created at 49 (15 t) with vis 42 | m1 23.70-24.30 s: only the **fading lower edge of swing 1's crescent trail** (it appears after swing 1, the hit's own residue). **No new marker before swing 2** (ev 07) | **REMOVE** (`#hzQuiet 1`, drop vis 42) | It always follows swing 1. The spear is carried to her right side (60-64), riptide and knockback sounds at 62. **Swing 1 → swing 2 13 t** (source gap 14-15 t). Impact visual exists: two layers of tilted crescents, dust ring. |
| P5 | P5 하늘을 심판하는 자, fly-slam (`p56`) | disc r 5.5 locked under the player at take-off + 1, 180 % (31) | Quiet + **module** decal: 28 gold rim bars growing r 1 → 5.5 over 16-21, a translucent amber glow fill, a gold 4-point star emblem at the centre, **a gold dust progress circle growing to the rim** (every 3 t, 17-30), sky sparkles from 19, descent pillar 29-31. From 15 (16 t) | m1 27.42-28.62 s: a **ground ring** under the player from 27.50 (small), full at 27.75: bright gold rim, translucent amber fill, **a gold 4-point star emblem at the ring centre** (not on the floor at 27.10, so it is part of the decal), sparkles falling from the sky. **No progress circle** (ev 08, 09) | **TRIM** | Keep the rim bars, the glow fill, the star emblem, the sparkles and the pillar. Remove the dust progress circle (`p56.py` ≈ l. 265-270). **Glint 5 / beam 12 / take-off 14; ring → hit 16 t.** Impact visual exists. |
| P6g | P6 gold sweep (guard timeout, `p56` sweep_g) | 200° front arc r 6 as 5 blade slices at 15-19, 165 % | Quiet + **module rim decal** from clip 0: 20 gold-block arc bars on black under-bars and 2 edge spokes that flash white as the blade passes, plus **a saturated progress arc** growing from her to the rim (reached at 14). 15 t | m2 8.20-9.60 s: guard aura, the big pale-gold chest sigil at 8.50, wind-up 8.80-9.28, sweep 9.38. **No ground marker** (ev 10) | **REMOVE** (drop `rim0`, the per-slice rim flash and kill lines, and the progress arc) | Gold swell from guard end − 11, the 4-point **chest sigil** and power-select at guard end − 4, then the sweep wind-up (spear lifted high and cocked behind her right shoulder) with a riptide-2 swell at 9; slices at 15. **Clip start → first slice 15 t; sigil → first slice 19 t** (source: 19 t). Impact visual exists: gold slabs along the arc, two crescent cards, a dust ribbon, crystal spikes along the arc edge, chips, cubes. |
| P6e | P6 enchanted sweep (record complete, `p56` sweep_e) | same arc, slices at 16-22, 250 % + the element, KB 4 | Quiet + **module rim decal** in the element colour (rim1-4) + progress arc. 16 t | m2 14.82-15.95 s (guard I) and 23.95-25.20 s (guard II): record starburst, enchant line, violet glow on the wind-up, sweep. **No ground marker** (ev 11, 12) | **REMOVE** (drop `rim1`-`rim4` and the progress arc) | Record starburst with a zap at R (clip 0). Enchant line and waist ring at 3 with a beacon thump and sonic charge. Element glow and particles on the spear 5-15, riptide at 11, slices at 16. **Record → first slice 16 t.** Impact visual exists: element slabs, strike fx (bolts, flames, splashes, ice), lingering ground fx. |
| FAIL | chaos fail spears, ×1-2 (`p56` fail) | disc r 3.4, 220 % + the star's element; decal 19 → hit 37 (+23 for spear 2) | **Framework outline + progress outline + strike flash** (not quiet), plus **module** decal: a red concave 4-point star (crimson fill, black rim, arms opening ±3.2 → ±11.4 b in 6 t, pink light streaks on the rims), plus **a crimson ring at r 3.4 on a black outline (24 bars)**. 18 t | m4 1.55-3.00 s (spear 1) and 3.20-4.55 s (spear 2): a gold cube column in the air, then a **red concave 4-point star decal** centred on the player (translucent crimson fill, dark-red rim, pink streaks) whose arms open. **No inner circle, no progress** (ev 13, 14, 15). Leads 22 t and 16 t | **TRIM** | Keep the star decal, the streaks, the column and the giant spear. Remove the framework outline, progress outline and flash (`#hzQuiet 1`), and the crimson r 3.4 damage ring (`p56.py` l. 868-874, `RING_N`), which the footage does not show. **Column → hit 20 t; decal → hit 18 t.** Impact visual: flash column, starburst rays, dome, X beams, a per-kind field. See flag F2 on showing the r 3.4 size at the hit. |

Every REMOVE row keeps at least the old wind-up floor from a distinguishable tell (clip pose + sound) to the hit:
10 t for P1a / P2 / P4 / P6, 12 t for P1b, 12 t for the entrance. Every REMOVE row also keeps an impact visual of
its own at the hit tick, so the framework strike flash is not needed anywhere. No damage, size or timing changes
are needed.

## Implementation pointers (generators only; rebuild after)

- ENT: `core.py` `intro/tell` (l. 350-356): add `sc_set('#hzQuiet', 1)` (or `*g.hz_opts(quiet=1)`) before the
  `hz_disc` at l. 353. Keep the glint card, the sounds, `intro/fall` and `intro/trail`.
- P1a / P1b: `p12.py` l. 395 and 457: drop `vis=11` / `vis=12` from `hz_opts` (keep `quiet=1`). Drop
  `tl.at(lock1 + 1, *bar_grow(...))` (l. 398), `tl.at(lock2 + 1, ...)` (l. 464) and the `decal_files(...)` call
  (l. 522). `cancel` keeps killing `rlk_mb_gd_p1`.
- P2: `p12.py` l. 612: drop `vis=21`. Drop `tl.at(lock + 1, *bar_grow(...))` (l. 620) and `decal_files(...)`
  (l. 730). `#gp2Len` stays: it is still needed for the hazard length and the streak.
- P3: `p34.py` l. 205-209: add `scoreboard players set #hzQuiet mb 1` before `hz_disc`. Keep `#hzVis 31` and
  `p/slam/vis`.
- P4: `p34.py` l. 566-575: replace `#hzVis 41` / `42` with `#hzQuiet 1`. Drop the ring-card merges at `t0 + 1`
  (l. 576-579) and `p/pull/vis` (l. 706-714).
- P5: `p56.py` l. 265-270: drop the "progress circle" loop. Keep the sparkles and whistle lines in the same block.
- P6: `p56.py` `sweep()`: drop the `rim{e}` files (l. 431-448; keep `slice_of`, l. 427-432, because the slab fx
  use it), the start calls (l. 582-585), the per-slice rim flash (l. 487), the rim kills (l. 518, 522) and the
  progress-arc block (l. 465-475).
- FAIL: `p56.py` l. 853: `g.hz_opts(sfx=0, kb=KB['default'], linger=2, quiet=1)`. Drop the damage-ring loop
  (l. 868-874) and `RING_N`. Optionally add the impact ring (F2).
- The `p/vis` dispatcher in `core.py` (l. 628-632) is generated from the pattern `vis` files. P1, P2 and P4 then
  have no vis file; P3 keeps its own.

## Evidence (`S/tele/gd/evidence/`)

| file | what it shows |
|---|---|
| `01_P1a_m1_0.20-1.62s_no_ground_marker.jpg` | thrust 1: streak on the spear, glint, lunge; plain floor |
| `02_P1b_m1_2.00-3.15s_no_ground_marker.jpg` | thrust 2: she hovers and aims from the air, then dives; plain floor |
| `03_P2_m1_6.00-7.65s_air_glyph_beam_only.jpg` | javelin: air glyph, vertical beam, launch disc, projectile; no ground line |
| `04_P3_m1_11.10-12.25s_ground_ring.jpg` | slam: thin gold ground ring + faint fill until the impact |
| `05_P3_m1_11.42-11.70s_ring_onset_grows.jpg` | slam ring onset: it appears small and grows to full in ≈ 6 t |
| `06_P4_m1_21.20-24.25s_swings_no_ground_marker.jpg` | swings: wind-up, hold, swing 1, swing 2; no ground marker |
| `07_P4_m1_23.70-24.03s_swing1_residue_only.jpg` | the thin gold line between the swings is swing 1's fading trail |
| `08_P5_m1_27.10-28.62s_ground_ring.jpg` | fly-slam ring under the player, growing, full, then the impact |
| `09_P5_m1_27.10-28.35s_star_emblem_is_decal.jpg` | full-res crops: no star on the floor at 27.10; a gold star at the ring centre at 27.75 and 28.00 |
| `10_P6gold_m2_8.20-9.60s_no_ground_marker.jpg` | gold sweep: chest sigil, wind-up, sweep; no ground marker |
| `11_P6ench_m2_14.82-15.95s_no_ground_marker.jpg` | electro sweep (guard I): starburst, enchant line, wind-up, sweep |
| `12_P6ench2_m2_23.95-25.20s_no_ground_marker.jpg` | electro sweep (guard II), same |
| `13_FAIL1_m4_1.55-3.00s_star_decal.jpg` | fail spear 1: cube column, red star decal on the player, impact |
| `14_FAIL_m4_1.90-2.60s_decal_star_only_no_ring.jpg` | full-res decal crops: a star with streaks; no inner circle, no progress |
| `15_FAIL2_m4_3.20-4.55s_star_decal.jpg` | fail spear 2: decal and blue impact |
| `16_ENT_m1-m4_0.05s_no_entrance_filmed.jpg` | every video starts mid-fight; the entrance is never shown |
| `17_ENT_guide_pdf_p73_no_marker_text.jpg` | PDF p.73: "어떤 표시도 남기지 않은 상태에서 나온다 … 바닥에 내리꽂히는 창에 맞아도 피해" |

Other frames checked (not kept): P5 crops at 27.10, 27.75, 28.00 and 28.35 s; P4 at 23.50, 23.55, 24.08 and 24.15 s;
fail crops at 1.90, 2.30 and 2.60 s.

## Flags

- **F1 (ENT: REMOVE with an off-boss hit; footage absent).** The entrance is never filmed (all four videos start
  mid-fight) and the PDF says she appears with no marker, so the ground disc goes. The hit lands away from the
  still-hidden boss. The readable precursor that stays is in the air: the sky glint at intro 16, then the spear
  falling from 7 b with its gold trail and the whistle (18 t). Keep these; they are not ground decals. Practical
  risk is low: the player arrives 17.5 b from the plant.
- **F2 (FAIL: readability after the trim).** Removing the crimson r 3.4 ring (not in the footage) leaves the star
  decal, which is about 23 b across. The real hit (r 3.4) is learned only at the impact, and the impact dome (r 1.74)
  shows less than the hit. Recommendation: at the hit tick, add an impact ring (a Navia `ring` card or a dust ring
  scaled to r 3.4, flat on the floor, 4-6 t). That is an impact visual, not a telegraph. Escape is unchanged:
  18 t of tell covers 3.9 b on foot and 5 b sprinting.
- **F3 (P3 shape fidelity, optional).** The footage ring grows from small to full in ≈ 6 t (m1 11.42 → 11.70).
  Ours starts at 86 % and widens over 11 t. Starting at ≈ 40 % and growing over 5-6 t would match. No gameplay change.
- **F4 (P4 swing 2, tight but within the floor).** With its ring gone, swing 2's tell is swing 1 itself, the spear
  carry (60-64) and the sound at 62. That is 13 t after swing 1's hit, but only 9 t after swing 1's active window
  ends (55). This is the source rhythm (14-15 t) and stays at or above the 10 t floor counted from swing 1's hit.
  No change proposed.
- **F5 (P1a / P2: the aim-lock moment is now marked only by motion).** The decal used to appear at the lock (P1a
  11, P2 17). The lock is now readable as "she stops turning". For P2 the beam at 20 (3 t after the lock) and for
  P1a the glint at 14 (3 t after) are the clear cues. Tell → hit stays ≥ 10 t; no fix needed. A test should check
  that `face/track` stops at the lock.
- **F6 (docs and tests).** Update README `파수꾼・타락 모듈`:
  - l. 522 등장 (it describes the 18 t ground telegraph as a deliberate deviation);
  - l. 529 ("모든 바닥 공격은 맞기 전에 10틱 이상 예고되고 … 예고가 나타나는 순간 조준이 고정된다");
  - l. 531 P1 and l. 532 P2 (lane decals);
  - l. 534 P4 (ring);
  - l. 535 P5 (progress circle);
  - l. 541 휘두르기 (rim and progress arc);
  - l. 552 파괴 실패 창 (피해 원).

  Also update `S/mboss/gd_contract.md` l. 158 (K4) and the README section `mboss/hz` notes as needed. The mcsim
  suites (`S/mb/tune_tests/test_guardian.py` and the mb2/mb3 harness copies) may assert on vis ids, decal entities or
  outline draws.
- **Ambiguous footage:** none. Every filmed hazard was seen clearly before its hit. The only hazard never filmed is
  the entrance, which is REMOVE by the rule and backed by the PDF text.

## Ground fx that are not hazards (untouched)

- Guard-entry discs and the flat gold ground ring (no damage; in the footage at m2 2.4-2.9 s).
- The chaos landing ring card and red particles (landing impact; no damage).
- Cube streams, ambient, no damage. Their heads spiral down to the player's feet and burst.
- The groggy crimson pool (in the footage; no damage).
- Death fly-away (no damage).
