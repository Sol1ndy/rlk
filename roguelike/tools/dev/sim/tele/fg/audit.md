# Ground-telegraph audit: 실험성 역장 발생 장치 (module `fieldgen`, mid-boss 3)

Scope: every hazard the module can emit at release HEAD 039b911 (read-only: `roguelike/tools/mboss_fieldgen/*.py`,
`build_mboss_fg_fx.py`, `build_mboss_core.py`, the generated `roguelike/data/rlk/function/mboss/fieldgen/p/**` for
cross-checks), against the reference footage `mb3/src/v1..v4.mp4` under THE RULE (footage ground marker → KEEP/TRIM; no
footage ground marker → REMOVE).

Ticks below are the real values the module builds with (read from the rig manifest through `api.ev_or`, printed from the
module): C1 bombs drop 12..54 (strike +6), finisher slam clip at 57, impact 74; C2 impact 17; C3 fire 22, off 155;
C4 launches 23..37, impacts 51..65; C5 rim 3, blast 48; C6 band 38, bursts 55..97 (6 t), throws 100..132 (8 t);
F1 decals 22..231, strikes +15; F2 band 8/16, bursts 25..67, throws 65..97; waves impacts 24 / 92 / 175 (charges 24 / 24 / 40),
triple fronts +6 / +12.

## 0. Framework state (all hazards are already quiet)

* Every `hz/*` call of the module is made with `#hzQuiet 1` and `#hzSfx 0` (checked on the generated output: 61 files,
  50 `hz/disc`, 4 `hz/line`, 4 `hz/ring`, every one preceded by `#hzQuiet mb 1`). So there is **no framework outline,
  progress outline or strike flash anywhere**; the pre-hit ground telegraphs are all **kit decals**
  (`fx/tele/disc|line|mline|wave`, 57 + 8 + 4 + 5 calls in the generated output) plus four ground presets
  (`p/column_base`, `p/dark_disc`, `p/erupt_tell`, `p/rim_flare`).
* Projectiles (`pj/launch`, the slabs) draw nothing of their own; their only telegraph is the dmg-0 throw line + kit lane.
* Entrance, field open / warp, break, groggy, pack-up and death emit no hazard (no `hz_`/`pj_` call in `seq_c.py`,
  `seq_f.py`, `core.py`).
* Every hazard already has its own impact visual on `#hzEv 1` (bomb_burst, slam, laser beam + laser_spot, missile_impact,
  blast + rocks, floor_burst, erupt, wave_band / wave_burst, slab_throw / slab_impact), so removing decals needs **no new
  impact visual**.

## 1. Table

| id | pattern | hazard | current pre-hit telegraph | footage (video, times checked) | decision | what the player reads instead / wind-up (first tell → hit) |
|---|---|---|---|---|---|---|
| C1-bomb | 1 bomb (일점 상쇄) | 20 bombs, `hz/disc` r 1.3, tell 10 (made drop−4, strike drop+6), groups of 4, light KB, `c1` | quiet; kit `tele_disc` r 1.3 Geo (fill + rim + progress edge) 10 t under each bomb, redrawn after pause (`c_redraw` 11..13) | v1 6.20–8.60 (5 fps sheet), 6.50 and 7.10 full crops: bombs drop from the ports onto bare floor, nothing under any landing point except the boss's moving shadow; impacts are gold spike bursts | **REMOVE** (`tele_disc`, its redraw) | turn + 16° nose-down pitch + `breeze.whirl` at 0, port glows + `bomb_port` at 10, straight glide along the route locked at 0; each bomb visibly falls 6 t from its port (`bomb_drop`), `bomb_burst` at the hit. Pattern tell → first hit **18 t** (ports → first hit 8 t; the fall itself 6 t). OK |
| C1-slam | 1 bomb (finisher) | `hz/disc` r 5 at the glide destination (≤ 6 b toward the re-lock), tell 17 (57 → 74), feet to 2.0 b, heavy KB, `c1s` | quiet; kit `tele_disc` r 5 Geo 17 t; `p/column_base` at the destination from +3 (gold floor glow r 0.6→2.6 for 15 t, spark flare at +12, end_rod); the rig's gold column under the gliding device | v1 8.40–9.60 (10 fps), 8.55 / 8.80 / 9.05 crops: the face-down core projects a ≈1 m gold column to the floor (8.45–9.10 = 13 t), no r 5 area marker anywhere; the column foot is under the caption bar until the base flare at ≈9.10 (3 t before the plunge) | **TRIM**: remove `tele_disc` r 5 (+ redraw id 12) and the 15 t floor glow of `column_base` at the not-yet-reached lock; keep the rig column (boss-body precursor that points at the slam point) and a base flare at the column foot after the glide (≈ +12) | slam clip (face-down core, column) + `column_tell` at 57, beacon `power_select` 63, `plunge` fx + sound 70, impact 74 → **17 t**; `slam` (shock ring r 5) + `dust_puff` at the hit. OK |
| C2-slam | 2 slam (내려찍기) | same `hz/disc` r 5 at the lock, tell 17, `c2` | as C1-slam (`tele_disc` r 5 17 t + `column_base` + rig column) | not shown on its own: only the caption v1 7.4–13.4 "내려찍기는 단독으로도 사용한다"; it is the same move as the C1 finisher (frames above) | **TRIM** (as C1-slam) | face/player + `column_tell` at 0, beacon 8, plunge 13, impact 17 → **17 t**; `slam` at the hit. OK |
| C3-beam | 3 laser (코어) | 2 `hz/line` r 3.0–5.8 (w 1.0 → 0.6), tell 22, active 133 t, re-aimed every tick, re-armed 10 t, `c3` | quiet; kit moving lanes `tele_mline` 0/1 on the floor r 3.0–5.8, filling over 22 t then held in the flash colour for the whole 133 t, turning with the beams (`mline_aim` every tick, `relane` after pause); `aim_line` 2 t at 20; `laser_spot` during the fire | v1 14.0–15.2 (5 fps), 15.0–17.4 (2.5 fps): pods drop and spark, thin white aim lines pod → floor at ≈15.0 (1–2 frames), then two beams with scorch/spark spots; no floor lane before or during the sweep | **REMOVE** the lanes (`tele_mline`, `mline_aim`, `mline_end`, `relane`); keep `aim_line` (= footage aim lines, a beam precursor), `laser_fire`, `laser_spot` (the beam's own floor hit) | pods drop + sound 0, `laser_charge` sparks every 5 t + whine 4, chime 14, aim line + `respawn_anchor.charge` 20, fire 22 → **22 t**; afterwards the beams are visible lines sweeping 5°/t. OK |
| C4-missile | 4 missile (바위 폭탄) | 10 `hz/disc` r 1.5 at the late lock (+14), strike +28 (tell 14), 2 volley groups, `c4` | quiet; kit `tele_disc` r 1.5 Geo 14 t at each lock (redraw id 41) | v1 27.9–29.1 (10 fps), 28.15 and 28.28 crops: the drill missiles dive in a cluster; the floor round the player is clean before every impact; impacts = gold spike bursts | **REMOVE** | tip flares + sound 0, vent shaft 8 / 15, launches 23..37 (fx + sound each), the missile prop + smoke trail every 3 t, a 13 t dive onto the lock, dive whistle at the first lock of each group, `missile_impact` at the hit. Pattern tell → first hit **51 t**; per missile lock → hit **14 t** with the missile visibly diving (non-ground precursor = the projectile, present). OK |
| C5-blast | 5 burst (지면 충격) | `hz/disc` r 12 made at +3, tell 45, blast +48, feet to 0.5 b, heavy KB, `c5` | quiet; kit `tele_disc` r 12 Geo from +3 (rim + translucent fill + bright progress edge reaching the rim at +48); `p/dark_disc` r 3.5 → 12 (+7..+33, held to +49); `p/rim_flare` at +36; marker sound at +3 | v4 2.6–5.0 (5 fps): thin pale-gold rim at the final radius from ≈2.70 (+3), dark disc grows from ≈2.90 (+7) to the rim by ≈4.2 (+33), rim brightens and flares 3.8–4.6 (+36..+41), blast 4.95 (+48) | **KEEP, TRIM**: drop the `tele_disc` fill and progress edge (the footage has one dark fill, ours shows two); keep a thin pale-gold rim at R from +3 to +48 (rim only), `dark_disc`, `rim_flare` | unchanged: spark 0 → blast **48 t** (rim from +3, dark disc +7..+33, up-beam 29, rim flare 36, column 41); `blast` + `rocks` at the hit |
| C6-burst | 6 rock (파쇄) | 8 `hz/disc` r 1.8, tell 10 (placed at the arc walker 10 t before), feet to 1.2 b, heavy KB, bursts 7–8 one group, `c6` | quiet; kit `tele_disc` r 1.8 Geo 10 t (redraw 61); a positional `amethyst_block.resonate` at each point 10 t before | v3 19.7–22.1 (10 fps), 19.92 / 21.08 / 21.70 crops: each burst erupts from clean floor (no mark before), the bursts walk in an arc onto the player; burst 8 hits her at 22.13 (8529) | **REMOVE** | dip 0, vent flare 12, tower 20, flame band 38 (+47) + `flame_charge` 44 → first burst 55: **17 t**; then a visible chain of `floor_burst`s 6 t apart walking onto the player, plus the positional resonate sound 10 t before each point. No per-burst precursor at the burst point (same as the footage) |
| C6-slab | 6 rock (파쇄) | 5 blade pj (1.5 b/t, life 24, reach 1.5 b), throws 100..132, at most 2 slab hits, `c6s` | quiet dmg-0 `hz/line` w 2.4 (vis 62) + kit `tele_line` lane 10 t from the slab's floor point to the locked feet + `chain.hit` sound | v3 22.3–24.1 (5 fps): glowing-rim slabs hover, then are flung one at a time with streak trails; no lane / line on the floor | **REMOVE** the lane and the dmg-0 line hazard (it exists only as the telegraph) | the slab hovers in view from its burst (rises 12 t, ≥ 30 t before its throw), `chain.hit` 10 t before, `slab_throw` streaks + `slab_trail` in flight, `slab_impact` on landing. Sound tell → hit ≥ **10 t**, but the only 10 t cue is a quiet sound: see flag 1 |
| F1-zone | 11 fzone (감소 영역) | per event 1–4 `hz/disc` r 2.8, tell 15, height to 3.5 b, KB 3, one group per event, `f1` | quiet; violet kit `tele_disc` el 9 r 2.8 (fill + rim + progress) 15 t + `p/erupt_tell` (dark disc with an amber rim and gold cracks, fades in over 6 t, life 16) + `erupt_tell` sound | v3 3.3–4.2 (6.67 fps) and 10.95: dark translucent discs with a thin pale-gold rim, 15 t before the eruption (3.30 → 4.03, 10.70 → 11.43), no progress fill; v2 4.55 (field form, night): same dark disc with a thin amber rim | **KEEP, TRIM**: drop the violet `tele_disc` (progress fill, violet rim); keep `erupt_tell` (it matches the footage) held to the strike | unchanged: dark disc **15 t**; `erupt` at the hit, debris after |
| F2-burst | 12 frock (파쇄, field) | 8 `hz/disc` r 1.8, tell 10, feet to 1.2 b, KB 4, bursts 7–8 one group, `f2` | quiet; violet kit `tele_disc` el 9 r 1.8 10 t + positional resonate sound | v3 take C 25.1–26.5 (6.67 fps, dusk take that v4 0.0–1.3 continues in field form): bursts from clean floor walking onto the player | **REMOVE** | vent flare 0, flame band 8 / 16 + `flame_charge` 10 → first burst 25: **17 t**; then the walking chain 6 t apart (as C6-burst) |
| F2-slab | 12 frock (파쇄, field) | 5 blade pj (1.5 b/t), throws 65..97, cap 2, `f2s` | quiet dmg-0 `hz/line` w 2.4 + violet kit `tele_line` 10 t + `chain.hit` | v3 take C 27.2–29.0 (5 fps): slabs flung with streaks, no lane on the floor | **REMOVE** the lane and the dmg-0 line | as C6-slab (flag 1) |
| W-front | 21 waves (「인력 충격파」 ×3) | `hz/ring` 0 → 2.5 at the strike, then grown 0.55 b/t for 36 t, band 2.5 b, height 0.7 b, `#hzNoDodge`, KB 3, `wave`; charges 24 / 24 / 40 (opening and closing) | quiet; violet kit `tele_wave`: a start disc r 2.5 filling on the floor under the device over the whole charge (pre-hit ground decal), then a front ring + inner edge travelling with the hazard; `wave_band` (3-D fire band) from S−1; `wave_fire` every 3 t | v2 16.5–18.3 and 19.6–21.4 (5 fps), 17.10 and 20.50 crops: charge sphere at the core; the floor under the device shows only the arena's gold emblem and the device's shadow; the ring appears with the beam / burst and travels as a burning band | **REMOVE** `tele_wave` (its pre-strike start disc is a ground telegraph the footage does not have; its travelling rings only duplicate `wave_band`, which is the footage's burning band) and the `rd_tell` redraw | charge sphere + `wave_charge` hiss from the charge start (24 t; 40 t third), `wave_pulse` every 8 t, `wave_charge2` at S−10, beam + burst at S, then the visible fire band; a player at r is hit at S + (r − 2.5)/0.55. Tell → hit **≥ 24 t**. OK |
| W-tri | 21 waves (below 50 % HP) | 2 extra fronts 6 t after the third (tell 10 each), as W-front | quiet; `tele_wave` tell 10 each | not in the footage (PDF only); v2 shows the 3rd wave single | **REMOVE** (uncertain / not visible) | `mkx` at S3+6m−10: `wave_charge2` + a `wave_pulse` at the core, then beam / burst / band → **10 t** each; one low-gravity jump clears all three (spec Q2). OK at the floor |

## 2. Evidence (`tele/fg/evidence/`, 19 jpgs)

| file | what it shows |
|---|---|
| `v1_6.50_C1_bomb_falling_no_decal.jpg`, `v1_7.10_C1_bombs_landing_no_decal.jpg` | bombs in the air over bare floor; no decal under the landing points |
| `v1_8.4-9.6_C1_slam_column_sheet.jpg`, `v1_8.80_C1_slam_column_foot_hidden.jpg` | the face-down core's column (13 t), no r 5 area marker; the column foot under the caption bar |
| `v1_14.0-15.2_C3_charge_aimlines_no_lane.jpg`, `v1_15.0-17.4_C3_sweep_no_lane.jpg` | laser charge, aim lines at 15.0, beams + floor spots, no floor lanes |
| `v1_27.9-29.1_C4_dive_impacts_sheet.jpg`, `v1_28.15_C4_floor_before_impacts_clean.jpg` | missile dive and impacts; clean floor right before them |
| `v4_2.6-5.0_C5_rim_and_dark_disc.jpg` | 지면 충격: rim at the final radius, dark disc growing to it, rim flare, blast |
| `v3_19.7-20.9_C6_bursts_no_decal_sheet.jpg`, `v3_21.08_C6_floor_before_burst5_clean.jpg` | floor bursts from clean floor, walking in an arc |
| `v3_22.3-24.1_C6_slab_throws_no_lane.jpg`, `v3_27.2-29.0_F2takeC_slab_throws_no_lane.jpg` | slab throws with streaks, no lane on the floor |
| `v3_25.1-26.5_F2takeC_bursts_no_decal.jpg` | take C bursts, no marks before them |
| `v3_3.3-4.2_F1_dark_discs_then_eruption.jpg`, `v3_10.95_F1_disc_under_player.jpg`, `v2_4.55_F1_field_form_dark_disc_amber_rim.jpg` | 감소 영역: dark discs with a thin pale-gold / amber rim, 15 t, then the eruption |
| `v2_16.5-18.3_W_charge_beam_ring_sheet.jpg`, `v2_20.50_W_charge_no_floor_disc.jpg` | wave charge (sphere at the core), no floor disc under the device; the ring starts at the burst |

The analysis notes agree (v1 §3 A/L/M, v2 §3 A2/B, v3 §2 Z/R, v4 §3 G). Frame dumps were deleted after the audit.

## 3. Flags

1. **Readability fix needed, C6-slab / F2-slab**: without the lane, the only cue 10 t before a throw is the quiet
   `block.chain.hit` (0.5 / 0.8) at `rk_tt<j>` / `throw_tell<j>`; the slab then reaches the feet in a few ticks at
   1.5 b/t. The footage's read is the hovering, glowing slab (the throws there are much faster), so ours has it, but to
   keep a visual 10 t tell add a small fx **on the slab itself** at the lock tick (a glint / flare from the kit's existing
   presets, e.g. `p/spark` or a glow card on the slab; it is fx on the projectile, not a ground marker).
2. **REMOVE hazards that appear away from the boss** (list as required): C6-burst / F2-burst have no precursor at the
   burst point, in the footage either; the footage's non-ground precursors (flame band under the ring, the tower, the
   walking chain) are all present in ours, so nothing is invented. C4-missile: the missile prop + smoke trail + dive
   whistle are present (its 16 b apex can be off-screen in the shoulder view; the 13 t dive is the read, as in the
   footage). C1-bomb: the falling bomb card from the port is present.
3. **Ambiguous footage, C1-slam / C2-slam**: in v1 the column foot is under the caption bar from 8.45 to ≈9.10, and the
   stand-alone slam is never shown; by the rule the 15 t floor glow of `column_base` at the lock goes; keep the rig
   column and a late base flare at its foot (the notes record a base flare at 9.10, 3 t before the plunge).
4. **Not in the footage, W-tri** (the below-50 % triple third wave): removed with the other wave decals; its 10 t
   core-pulse + `wave_charge2` tell stays at the floor.
5. **Kit work for the C5 trim**: the kit has no rim-only ground telegraph (`tele_disc` = fill + rim). The trim needs a
   rim-only variant (a flag on `tele/disc` or a static rim card in `build_mboss_fg_fx.py`) in pale gold, and C5's pause
   redraw (`c_redraw` id 51) must redraw only that rim (and ideally the dark disc, which is an fx card, not a decal).
6. **F1 trim and pause**: the kept marker `p/erupt_tell` is an fx card with a fixed 16 t life; `p/fzone/rd` currently
   redraws the violet `tele/disc` after a pause; it must redraw `erupt_tell` instead (with the remaining tell, so it may
   need a life argument), or the marker vanishes after a pause.
7. **Redraw paths to clean up** when the decals go: `c_redraw` of bomb (11..13 incl. the slam 12), slam (21), missile
   (41), rock (61, 62); frock `rd` / `rd_line`; waves `rd_tell` (`rd` keeps redrawing `wave_band` for moving fronts);
   laser `relane` and `tele_mline_end` calls in `off` / `cancel`.
8. **dmg-0 throw lines** (`rk_tl` vis 62, frock `tl_line` tag `p12y`) exist only to carry the lane; remove them with it.
9. **Dead code**: `api.rocks()` (old helper, unused) builds non-quiet bursts with `tele_line`; leave it unused or delete it.
10. **Tests** in `mb3/tests` assert the decal pairing (`pat_cruise.py` C1 / C2 / C4 / C3-lane checks, `pat_field.py`
    W ring-decal checks incl. the triple and the pause redraw, `test_fieldgen.py` decal-count lines); they need updating.
    The "every damaging hazard made ≥ 10 t before it can hit" checks still hold (no hazard timing changes).
11. No balance change is needed for readability: every hazard keeps a ≥ 10 t tell from a clip pose / sound to the hit
    (C1-bomb 18, slams 17, C3 22, C4 51 / 14, C5 48, bursts 17, F1 15, waves ≥ 24, triple 10). The fieldgen damage
    raise (`api.DMG`) is the separate part of the request and is not affected by this audit.
