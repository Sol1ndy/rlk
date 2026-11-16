# 실험성 역장 발생 장치 (nameplate 브레게 프로토타입): pattern and sequence implementation specs

These are the stage-2 specs for the third mid-boss. Each file is one pattern or sequence. It gives:
- the per-tick timeline, aligned to the rig clip and its events;
- the AI (bands, approach, facing, aim locks);
- the body travel;
- telegraphs ≥ 10 t;
- the exact damage shapes as `g.hz_*` / `g.pj_*` calls, with sizes, groups, caps, knockback, element and coefficient;
- projectiles;
- fx per tick (kit presets);
- sound per tick (kit recipes and vanilla layers);
- the dodge windows (walking, half-speed walking during swings, jumping with and without low gravity, dashing);
- an ASCII diagram;
- an implementation sketch against the module API, and the test cases to add.

Every place where `plan.md` (binding) disagrees with the footage, the rig or the stage-1 stubs is flagged in the
file's §1 as **F1, F2, …** with a proposed fix. §5 below collects them as open questions with a recommended answer.

What these specs were written against:
- **Binding design:** `mb3/plan.md`.
- **Research:** `mb3/understand/v1..v4.md` (footage, frame-timed), `model.md` (the model and motion),
  `mb3/code/adapt.md` (the framework hooks).
- **Module core and stage-1 stubs:** `mb3/fg_contract.md`, `mb3/wt_core` (`tools/mboss_fieldgen/{api,core,cruise,
  field}.py`, commit 1dfa2f6).
- **Fx kit:** `mb3/fg_fx_api.md`, `mb3/wt_fx` (`tools/build_mboss_fg_fx.py`, manifest
  `tools/mboss_fg_fx_manifest.json`).
- **Rig:** `wip/fg-rig` 0f7c0e8 (`mb3/wt_rig`): `tools/mboss_fieldgen_rig_api.md` and
  `tools/mboss_fieldgen_rig_manifest.json`. All clip ticks quoted here are this manifest's, and code must read them
  with `ev()` / `ev_or()` / `clip_len()` (§3).

I re-checked these frames myself:
- v1 `sheet_slam_key_crop_8.40-9.80.jpg`: the finisher drifts after the player and lands 2-3 b behind her (C1 F1);
- v2 `pf_wave3_impact_24.70-25.65.jpg`: the 3rd wave's burst, then the drop onto the floor (W F2);
- v3 `sheet_rock_burst_positions.jpg`: the burst arc across the device's front, the last one on the player (C6 F1);
- `renders/fx_hud.png`: the HUD lines (S5).

## 0. Index

| file | id | name | clip(s) (len) | owner |
|---|---|---|---|---|
| [E_entrance.md](E_entrance.md) | — | entrance (dormant → unfold → rise) | `entrance` (130) | core `intro/*` |
| [C1_bomb_run.md](C1_bomb_run.md) | 1 | 중력 시스템·일점 상쇄 (폭격) + slam finisher | `bomb_run` (58) + `slam` (45) = 103 | `cruise.py` |
| [C2_slam.md](C2_slam.md) | 2 | 내려찍기 (slam alone) | `slam` (45) | `cruise.py` |
| [C3_lasers.md](C3_lasers.md) | 3 | 중력 시스템·코어 (레이저 빔) | `laser` (175) | `cruise.py` |
| [C4_missiles.md](C4_missiles.md) | 4 | 중력 시스템·바위 폭탄 (미사일) | `missiles` (64) | `cruise.py` |
| [C5_ground_impact.md](C5_ground_impact.md) | 5 | 중력 시스템·지면 충격 (중력 폭발) | `coreup` (130) | `cruise.py` |
| [C6_rock_tower.md](C6_rock_tower.md) | 6 | 중력 시스템·파쇄 (바위 날리기, tower) | `tower_throw` (157) | `cruise.py` |
| [S1_field_enter.md](S1_field_enter.md) | 20 | 역장 생성: warp, unfold, low gravity | `warp_out` (34) + `warp_in_field` (24) | core service |
| [W_gravity_waves.md](W_gravity_waves.md) | 21 | 「인력 충격파」 ×3 (single; triple below 50 %) | `wave` (40) ×2 + `wave_long` (56) / `wave_drop` (84) | `field.py` (service) |
| [F1_reduction_zone.md](F1_reduction_zone.md) | 11 | 중력 시스템·감소 영역 (바닥 뜯기) | `field_erupt` (40); pattern 260 | `field.py` |
| [F2_field_rocks.md](F2_field_rocks.md) | 12 | 중력 시스템·파쇄 in the field form | `frock` (110) | `field.py` |
| [S2_field_end.md](S2_field_end.md) | 21 + 22 | field end, unbroken: closing waves + pack-up | waves + `field_end` (102) | `field.py` + core service |
| [S3_break_groggy_recover.md](S3_break_groggy_recover.md) | — | 역장 붕괴 (20 hits) → groggy 200 t → recover | `break` (34), `groggy` (loop), `recover` (15) | core |
| [S4_death.md](S4_death.md) | — | death | `death` (110) | core |
| [S5_meter_hud.md](S5_meter_hud.md) | — | the 20-hit meter and the HUD | — | core + kit HUD |

## 1. Conventions

### 1.1 Notation

- **Points.**
  - S = the body (the husk on the floor under the ring axis; the rig anchor and the hitbox).
  - P = the player's feet (`@e[tag=rlk_body]`).
  - C = the arena centre (200, 201, 8); floor y 201.
- **Ticks.** The pattern clock `#fgPT` = the clip tick of the pattern's clip (the core plays it at clock 0). Service
  clocks are the service's own; the core states use `#fgT`; the intro and death use `#mbT`.
- **Body frame.** `execute at S rotated as S rotated ~ 0`, then `^x ^y ^z`: x = the device's **left**, y up,
  z forward.
- **Rig anchors.** Rig coordinates are x left, y up, **−z forward** (`mboss_fieldgen_rig_api.md` §6), so the
  body-frame point is `^x ^y ^-z`.
  - Cruise: ring 4.5, core 4.5, eye `^ ^4.5 ^1.375`, ports at y 3.86 on r 2.74, spike tips `^±5.33 ^4.55 ^0`, vents
    `^2.81 ^4.88 ^-1.16` / `^-2.81 ^4.88 ^1.16`, pendulum tip 0.55.
  - Field: ring 5.8, core **4.1**, medallions `^±3.85 ^4.1 ^0`, violet column end 2.15, pendulum tip 0.3.
  - Read them from `form_states.<form>.rest_anchors` and `clips[].anchors[event]`.
- **Yaw.** MC yaw grows clockwise from above. The rig's azimuth az (from the front toward the left) maps to yaw =
  Y − az (C3).
- **Kit calls.** `K.fx(name, **args)`, `K.snd(name)`, `K.tele_disc(r, tell, el=5)`, `K.tele_line(len, w, tell)`,
  `K.tele_wave(r0, r1, w, tell, dur)`, `K.tele_mline(id, len, w, tell, hold, back)` / `_aim` / `_end`,
  `K.hud(name)`, `K.prop(name)` (`fg_fx_api.md` §8; K = `tools/build_mboss_fg_fx.py`).
  - `el=5` is the Geo palette (cruise patterns); `el=9` the field violet (waves, F1, F2).
  - Every hit is Geo whatever the decal colour.
- **Sound.** `g.sound(event, v, p)`: one vanilla `playsound … hostile @a[tag=player]` with the shared minVolume. All
  sounds are vanilla and mechanical (no creature voices).

### 1.2 Hazards, projectiles and groups (framework)

- `g.hz_opts(...)` then `g.hz_disc(r, tell, dmg)` / `hz_ring(r0, r, tell, dmg)` / `hz_line(len, w, tell, dmg)`,
  positioned on the floor, rotated = the aim. `tell` = ticks to the strike; `dmg` = % of the registry base hit
  (atk 12 × dmgMul 110: **100 = 13 raw**).
- Defaults:
  - act 1, element = the registry's (Geo 5), KB 3 (0.6 b);
  - height −0.5..3.5;
  - sfx 1;
  - quiet 0.
- Every hazard paired with a kit decal sets `quiet=1` (the kit draws it) and `sfx=0` (the specs compose the sounds).
- **Raw damage** (before defence and level): 0.5 = 6, 0.8 = 10, 0.9 = 11, 1.1 = 14, 1.2 = 15, 1.3 = 17, 1.4 = 18,
  2.2 = 29. 1.0 is about 11 % of an item-less player's max HP (butterfly scale).
- **Knockback** steps (`player/knockback`): KB 2 = 0.3 b, KB 3 = 0.6 b, KB 4 = 1.0 b (0.1 b × (n + … + 1)). Heavy KB
  does **not** push a player out of a 2 b disc; caps must come from groups (C6 F1).
- **Volley group:** `g.GRP_NEW`, then `grp=True` on each member; one hit per group.
  - FW-4: every member must exist before the group's first strike. Each spec checks this per group.
- **Options (new for this boss):**
  - `nododge=1` (`#hzNoDodge`: the dash i-frames do not help; **the waves only**);
  - `rearm=N` (C3);
  - `hz/aim` (C3);
  - `hz/resize` / `resize_s` (C3 width, the wave front).
- **Blade projectile** (`pj_opts(shape=1)`): reach = hr + 0.65 b (FW-1). The slabs use hr 0.8 → reach 1.45, matched
  by a line telegraph w 2.4. Speed 1.5 b/t is a whole number of sub-steps (FW-2 does not apply).

### 1.3 Player kinematics (for the dodge windows)

| move | value |
|---|---|
| walk | 0.22 b/t |
| walk while swinging (shoulder view / F5: `swHold`, half speed) | **0.11 b/t**; first person walks at full speed but cannot jump |
| sprint | 0.28 b/t |
| jump (vanilla) | apex 1.25 b, 12 t; feet > 0.5 / 0.7 b on press +2..+9, > 1.0 on +3..+8, > 1.2 on +5..+6 |
| **jump (low gravity: gravity ×0.5, jump ×1.19)** | apex **2.96 b**, 25 t; feet > 0.7 b on **+2..+22**, > 1.2 on +3..+21, > 2.0 on +5..+18 |
| jump while swinging | **impossible** (the swing hold ×0 wins over low gravity); a dash ends the swing at once (`dash_go`: `atkCD 0`) |
| dash | 3 b in 3 t; **6 t of i-frames from the press** (press P covers P..P+5); 2 charges, 1 regen / 20 t |
| body pad | 0.3 b on every shape (the blade: see §1.2) |

The arcs are simulated per tick as `y += vy; vy = (vy − g) × 0.98` (vanilla g 0.08, v0 0.42; low gravity g 0.04, v0 0.4998).

### 1.4 Arena (plaza)

- Centre (200, 201, 8). Walkable r 21, wall ring r 21-22 (y 201-207). The barrier cap is only over the wall; the
  light layer y 206 has no collision.
- The body is clamped to **r ≤ 16.5** (`u/okb`, the leash). Ground targets on the player are pulled into the walk disc
  **r 20.3** (`g.lockp()` / `g.clamp_walk()`). Points the body moves to: `g.lockb()` / `g.clamp_body()`.
- There is no upper gallery (Genshin's "2층 활용" refuge): the jump is the only answer to the waves.

### 1.5 Telegraph rules

- ≥ 10 t from the decal to the strike for every damaging hit. The shortest here is 10 t: C1 bombs, C6 / F2 bursts and
  throw lines. The longest is 45 t (C5).
- Each kit decal is made in the same tick as its hazard, with the same tell; its fill reaches the rim on the strike
  tick and flashes.
- Aim locks:
  - C1 and C2 lock once (C1 again for the finisher);
  - C4, C6 and F2 lock late per projectile / burst (that is the design: late locks trail a moving player);
  - C3 never aims at the player (a fixed orbit);
  - C5 and the waves are centred on the device.

## 2. Global table

Ticks are pattern clocks (= clip ticks of the real rig). "tell → strike" is decal → hit.

| id | pattern | clip, len | bands (w) | approach | aim lock | tell → strike | shape(s) | coef | KB | worst case standing |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | C1 일점 상쇄 + slam | bomb_run 58 + slam 45 = **103** | mid 1, far 2 | the run: glide 45 t ≤ 0.55 b/t on a line locked at 0; finisher glide ≤ 6 b (58-67) | route t0; finisher t58 (`lockb`) | bombs d−4 → **d+6** (10 t; d = 12 … 54); slam 58 → **74** (16 t) | 20 × disc r 1.3 (offsets ±1.05 / 0), groups of 4; disc r 5, y ≤ 2.0 | 0.8 / 1.4 | 2 / 4 | 2 × 0.8 + 1.4 = **3.0** |
| 2 | C2 내려찍기 | slam **45** | melee 2, mid 1 | glide 10 t onto the lock | t0 (`lockb`) | 0 → **16** | disc r 5, y ≤ 2.0 | 1.4 | 4 | **1.4** |
| 3 | C3 레이저 | laser **175** | melee 2, mid 2 | none; **yaw frozen** | none (orbit from the rig: E at Y−90 +5°/t, G at Y+90 −5°/t) | 0 → **25**, active 25-157 | 2 lines r 3.0-5.8, w 1.0 (25-27) → 0.6, y ≤ 2.0; one group, re-arm 10 | 0.5 / touch | 2 | ≈ 4 hits = **2.0** |
| 4 | C4 미사일 | missiles **64** | far 3 only | none | each missile at L+14 (`lockp`) | L+14 → **L+28** (14 t); impacts 50-63 | 10 × disc r 1.5; 2 groups | 0.9 | 3 | **1.8** |
| 5 | C5 지면 충격 | coreup **130** | melee 2, mid 1 | none | none (on S) | 3 → **48** (45 t) | disc r 12, **y ≤ 0.5** (jump), dash ok | 2.2 | 4 | **2.2** |
| 6 | C6 파쇄 | tower_throw **157** | mid 2, far 1 | dip glide ≤ 2.4 b (0-11) | arc point per burst; feet per throw | bursts −10 → **55 + 6k**; throws −10 → **95 + 8j** (+ about 6 t of flight) | 8 × disc r 1.8, y ≤ 1.2, bursts 7-8 one group; 5 blade pj 1.5 b/t, reach 1.45, ≤ 2 hits | 1.3 / 1.1 | 4 / 3 | 1.3 + 2.2 = **3.5** (4.8 within 4.7 b) |
| 11 | F1 감소 영역 | field_erupt 40, pattern **260** | all | none (centre) | per event: player + random (disc 1 at 2-3 b) | 15 t; strikes 37, 87, 117, 135, 156, 185, 196, 235, 246 | 1-4 × disc r 2.8 per event (one group), not jumpable | 1.2 / event | 3 | 1 per event (**10.8** if never moving; 0-2 moving) |
| 12 | F2 파쇄 (field) | frock **110** | all | none (centre) | as C6 | bursts −10 → **25 + 6k**; throws −10 → **65 + 8j** | as C6, violet decals; **low-gravity jump clears the bursts** | 1.3 / 1.1 | 4 / 3 | **3.5** |
| 21 | W 인력 충격파 | wave 40 ×2 + wave_long 56 (opening) / wave_drop 84 (closing); **213-231** | service | none | none (on C) | charges 25 / 25 / 41 (40) → impacts **25, 93, 176**; triple +6 / +12 (rec.) | ring band 2.5 deep at 0.55 b/t, y ≤ 0.7, **#hzNoDodge** | 1.2 / front | 3 | **3.6** (6.0 triple) |
| 20 | field opening | warp_out 34 + warp_in_field 24 → **57** | service | warp to C at 13 | — | — | — | — | — | — |
| 22 | pack-up | field_end **102** | service | — | — | — | — | — | — | — |

### 2.1 Dodge summary

| pattern | leave the area | jump | dash (press window) | ignores the i-frames |
|---|---|---|---|---|
| C1 bombs | step 2.7 b sideways off the line (walk 12 t, half 25 t) | no | 0-5 t before a bomb | no |
| C1 / C2 slam | 5.3 b in 16 t: sprint + dash | no (y ≤ 2.0) | strike −5..strike | no |
| C3 lasers | r < 2.7 or r > 6.1; cross right after a beam passes | no | covers one pass | no |
| C4 missiles | keep walking (14 t lock) | no | impact −5..impact | no |
| C5 blast | 12.3 b in 45 t (walk from ≤ 4 b, sprint from under it) | **vanilla press 39-46** | **43-48** | no |
| C6 bursts | keep moving; 2.1 b in 10 t | vanilla press strike −6..−5 (hard) | strike −5..strike | no |
| C6 / F2 slabs | sidestep 1.5 b (walk 7 t, half 14 t) | no (blade) | impact −5..impact | no |
| F1 discs | step 0.1-1.1 b out of disc 1 (half speed ok) | no (y ≤ 3.5) | eruption −5..eruption | no |
| F2 bursts | as C6 | **low gravity: strike −21..−3** | strike −5..strike | no |
| W fronts | impossible | **low gravity: T−17..T−2** (triple G 6: T−5..T−2) | — | **yes** |

## 3. Rig clip events: stub vs real rig vs footage

The core reads events with `ev_or(clip, event, default)`: the defaults are the stub manifest's numbers. With the real
manifest present (`api.STUB` False), the real numbers rule. The `FGANIM` task (another agent) is re-authoring the
clips again, so **never hard-code a tick**: every timeline row moves with its event. Re-run the per-pattern cases
after any rig merge.

| clip | stub (core defaults) | real rig 0f7c0e8 | footage | spec |
|---|---|---|---|---|
| `entrance` | 112, risen 110 | **130**, clank 16, pods 24, unfold 30, eye 54, turn 60, rise 80, risen 110, face 115 | clank 16, risen 110 | real |
| `bomb_run` | 58, run 12 | 58, turn 0, ports 10, run 12, end 56 | run 12.3 | real |
| `slam` | 45, impact **17** | 45, column 0, plunge 13, impact **16**, rise 23 | impact +16.5 after the column | real (tell 16) |
| `laser` | 174, fire **24** | **175**, drop 0, charge 4, aim 23, fire **25**, off 158, retract 159, `orbit` | fire 23.6 | real |
| `missiles` | **70**, launch **21** | **64**, flare 0, vent 8, launch **22**, last 35 | launch 25-39 | real, flight 28 t (C4 F1) |
| `coreup` | **110** | **130**, spark 0 … blast 48, sink 81 | blast 48 | real |
| `tower_throw` | 157 | 157, burst 55, throw 95, revert 142 | bursts 60, throws 101 | real |
| `warp_out` | 34, out 13 | 34, flip 0, **hide 12**, out 13 | pillar 13 | flash at `hide` (S1 F1) |
| `warp_in_field` | 24 | 24, in 0, unfold 1, field 17, banner 22 | unfold 35-51, banner 53-57 | real |
| `wave` | **36**, impact **24** | **40**, impact **25** | charge 23-24 | real |
| `wave_long` / `wave_drop` | — | 56 (impact 41) / 84 (drop 36, land 40, impact 40, lift 60, risen 80) | 3rd charge 40-42, drop after the impact | opening / closing 3rd wave (W F1) |
| `field_erupt` | 40, erupt 22 | 40, activate 0, lock 12, erupt 22 | first eruption 37 | real |
| `frock` | — | 110, vent 0, flame 8, burst 25, throw 65, end 100 | — | F2 clip (fallback `field_erupt`) |
| `field_end` | **78**, lances **22** | **102**, lift 0, rise 2, lances 20, horiz 40, pack 50, dock 72, packed 96 | compact 102 t after the 3rd impact | real (`look/idle` at dock) |
| `break` / `recover` | 34 / 15 | 34 (burst 5, wobble 14) / 15 (flip 6) | burst 4.7, flip 46-55 | real |
| `death` | **106**, out **90** | **110**, drop 20, sink 40, land 60, out 70, gone 110 | — | real; the last fade fx ≤ 82 |

Three clips are not in the task's list of 19: `wave_long`, `wave_drop`, `frock`. Code takes them with
`'x' if 'x' in CLIPS else <fallback>`, so the stub build still works. `api.NEED_CLIPS` stays at 19.

## 4. Lessons from the butterfly review applied (`mb2/review/core_findings.json`)

| finding | how these specs avoid it |
|---|---|
| S1 / perf-1: kept markers never killed | Every lock goes through `g.keep(tag)` (the core kills the tag's old marker and every `rlk_mb_fg_kept` at `p/finish` / `p/cancel`). Every marker a pattern summons itself carries `rlk_mb_fg_pat` and is killed before its summon (C1 route / Dst, C4 `p4t<i>`, C6 walker / locks, F1 placement). |
| S2: `g.release` froze the AI | `g.release()` only hides the bar (C5 at 49); the core never stops the AI on it. |
| FW-1: the blade reaches hr + 0.65 | The slabs use hr 0.8 (reach 1.45) with a line w 2.4 (±1.5 padded). If BFFIX changes the blade to hr + 0.3, raise hr to 1.15 (Q16). |
| FW-2: 0.75 / 1.75 b/t fly a sub-step fast | The only pj speed is 1.5 b/t. |
| FW-4: a group member made after the group struck | Every group is checked in its spec (C1 groups of 4, C3 pair, C4 2 × 5, C6 / F2 bursts 7-8, F1 events). Slab throws are never grouped for this reason (the C6 cap instead). |
| perf-2: the card ager's first tick | Fixed in the kit (`fg_fx_api.md` §2.3). |
| perf-5: the last death fx cut by the cleanup | `death_fade` at 70 and 82 only; every card ends by 109 (S4 F2). |
| PL-1: cards at the first-person eye | Pebbles at the feet; the meter glint at the core; flashes and pops on the title line. No card at the player's eyes. |
| S3 / S8 (rig form after cuts; groggy cut) | Core behaviour (`test/cut` re-derives the form; a cut groggy keeps the counters); unchanged. |

## 5. Open questions, with a recommended answer

**Q1. The rig clips are still moving (FGANIM re-authors them).**
- **Recommended:** every row is keyed to `ev(clip, event)`; no absolute tick in code. Re-run the per-pattern cases
  after each rig merge.
- The specs quote the 0f7c0e8 numbers only as today's values.

**Q2. The triple wave below 50 % HP: 9 t apart (plan) vs 6 t (proposed).** W F3. With the body pad a front sits on a
standing player for 6 t, and a low-gravity jump stays above the band for 21 t. Three fronts 9 t apart (24 t) can
never all be jumped, not even with two jumps.
- **Recommended: 6 t** (impacts 176, 182, 188). One jump pressed 2-5 t before the first front clears all three, which
  is what the plan intended ("one low-gravity jump").
- If 9 t is kept, document "a standing player takes one front"; walking inward while jumping also works.

**Q3. The 3rd wave's clip.**
- **Recommended:** opening `wave_long` (charge 41, no drop), closing `wave_drop` (the footage's drop belongs to the
  closing sequence). The hazard is made at the clip start with `tell = ev(clip,'impact')`; stub fallback `wave`.

**Q4. The C1 finisher hits nothing where the stub places it** (the end of a 24.75 b route, 10-15 b past the player).
- **Recommended:** re-lock the player at 58 (`lockb`) and glide up to 6 b toward it over 10 t. The slam disc sits at
  that destination (tell 16). The footage drifts after the player during the column.

**Q5. C3 geometry:** the stub's beams are 90° off the rig's orbit, 1.0 wide for the whole firing time, and the body
may yaw.
- **Recommended:** start E at Y − 90 (+5°/t) and G at Y + 90 (−5°/t), generated from the manifest `orbit`.
- Band r 3.0-5.8; width 1.0 for 25-27, then 0.6.
- No turning from 0 to 175.

**Q6. C4 flight:** the stub's is 20 t, the footage's 28 t.
- **Recommended:** rise 14 t (two `teleport_duration` segments), lock at L+14 (tell 14), dive 13 t, impact L+28. It
  still ends inside the 64 t clip.

**Q7. C6 / F2 bursts all land on a standing player (7.8)** because `api.rocks` walks onto the player and KB 4 moves
them only 1 b.
- **Recommended:**
  - the arc walker (offsets 90 → 0° at the player's distance);
  - bursts 7-8 in one volley group;
  - at most 2 slab hits per run (`pj_end` counts hits; the remaining slabs crumble).

  That gives ≤ 3.5 per run for a standing player.

**Q8. F1 event ticks:** the stub's gaps are tighter than the footage's.
- **Recommended:** the footage's ticks: decals at 22, 72, 102, 120, 141, 170, 181, 220, 231 (gaps 11-50 as the plan),
  end 260.

**Q9. F2's clip:** the stub uses `field_erupt` with its own ticks.
- **Recommended:** the rig's `frock` (bursts 25, throws 65, end 110); fallback `field_erupt`.

**Q10. No settle before the opening waves** (the first front about 26 t after the banner).
- **Recommended:** `field/opened` sets `#fgCool 40` (one core constant). The footage spends about 75 t on the banner,
  the core flip and gold streaks before the first charge. The player learns the jump and lands the first hits.

**Q11. The warp-out flash at `out` 13 leaves one empty tick** (the rig hides at 12).
- **Recommended:** the flash (fx + sound) at `ev('warp_out','hide')`; the teleport stays at `out`.

**Q12. C5 "clamp R inside the arena".**
- **Recommended:** no clamp and no glide to the centre. The part of the r 12 disc past the wall is inside solid blocks
  (nothing to see or hit), and the far side always leaves open floor.

**Q13. Meter integration** (both sides draw parts of it).
- **Recommended:**
  - the kit's `meter_hit` calls `crack/<n>` (drop the core's rig call; keep `#fgCrack`);
  - `meter_hit` positioned at the manifest's field core (4.1, not 3.84);
  - the core's name line drops its own "역장" while the meter is open and its own "· 그로기";
  - the sub-line ends with `put_sub`, rebuilt on `#fkHudV` changes.

**Q14. Pack-up look.**
- **Recommended:** keep the meter / low-gravity / cut ending at pack-up 0, but move `look/idle` to `dock` (72), so the
  violet fades with the pack as in the footage and the rig note. One lift-off flash only (in `wave_drop`).

**Q15. Death tilt 30° (rig) vs 40° (plan).**
- **Recommended:** keep the rig (the low rim rests on the floor either way). `death_fade` only at 70 and 82.

**Q16. The blade reach if BFFIX fixes FW-1** (`hr + 0.3`).
- **Recommended:** derive the slab hr from the reach. Today hr 0.8 (reach 1.45); after the fix, hr 1.15. Keep the line
  telegraph w 2.4.

**Q17. Groggy sparks:** the core fires every 20 t, the kit recipe says 30-40.
- **Recommended:** every 40 t (`#fgK40`).

**Q18. Merge order.** The core never calls the kit today, and the stubs use vanilla particles.
- **Recommended:** merge `wip/fg-fx` and `wip/fg-rig` into the module branch before the stage-2 patterns (as the
  butterfly did). Delete `stub_rig.py` / `stub_rig_manifest.json` and the kit's stub rig. Rerun the generators in the
  documented order, then implement these specs.
- If a pattern lands before the kit, guard every `K.*` line behind `HAVE_KIT = manifest exists` and keep the stub's
  vanilla lines in the other branch.

**Q19. F1 punishes standing still hard (9 × 1.2).**
- **Recommended:** accept. Disc 1 is always 0.1-1.1 b from its edge for a standing player, with a 15 t lead: one
  half-speed step while attacking. That is the field's pressure while the meter is filled.

**Q20. Sounds not yet used elsewhere in the pack** (`block.vault.*`, `block.crafter.craft`, `block.trial_spawner.*`,
`block.heavy_core.place`, `item.mace.smash_ground_heavy`, `block.copper_bulb.*`, `block.sniffer_egg.crack`,
`item.spyglass.use`, `block.copper.fall`, `block.chain.fall`).
- **Recommended:** keep them. They are all vanilla 1.20 / 1.21 sound events that the kit already uses. Verify once in
  26.3; the fallbacks are `block.iron_trapdoor.*`, `block.piston.*`, `block.anvil.*`, `block.chain.*`.

**Q21. The closing tail is about 40 t longer than the footage** (`wave_drop` + `field_end`).
- **Recommended:** accept (a harmless hover after the closing waves). The rig author may shorten `field_end`'s first
  20 t.

**Q22. `wave_drop` drops before its impact** (the footage: impact, then the drop 5 t later).
- **Recommended:** keep the rig ("it slams into the floor and the ring leaves it"); the hit is at the clip's
  `impact`.

**Q23. C2's glide in the mid band reaches 0.8 b/t.**
- **Recommended:** accept. It is short (10 t), and it is the device "swooping over" the column point; the decal is at
  the destination from 0.

## 6. FX list (kit presets and props used, `fg_fx_api.md` §7)

| preset / prop | used in |
|---|---|
| `awake`, `unfold`, `crown_flare`, `eye_open`, `rise`, `spark`, `flash` | E (and `spark` / `flash` across specs) |
| `ports_glow`, `bomb_drop {h}`, `bomb_burst`, `column_tell {h}`, `plunge`, `slam`, `dust_puff` | C1, C2 |
| `pods_drop`, `laser_charge`, `aim_line {len}`, `laser_fire {len}`, `laser_spot`, `laser_end` | C3 |
| `tip_flare`, `vent_shaft`, `missile_launch`, `missile_trail`, `missile_impact`, prop `missile` | C4 |
| `core_spark`, `core_lift`, `dark_disc {r0,r,grow,life}`, `up_beam`, `rim_flare {r}`, `column_down {h}`, `floor_hit`, `blast {r}`, `rocks` | C5 |
| `dip`, `vent_flare`, `tower_up`, `flame_band`, `floor_burst`, `slab_rise`, `slab_throw`, `slab_trail`, `slab_impact`, `revert`, prop `slab` | C6, F2 |
| `halo_flip`, `warp_out`, `glitch`, `warp_in`, `warp_pillar`, `field_unfold`, `field_idle`, `pebbles`, `gold_streaks` | S1, the field idle |
| `wave_charge {t}`, `wave_pulse`, `wave_band {r0,r1,w,dur}`, `wave_beam {h}`, `wave_burst`, `wave_fire {r}`, `lift_off` | W, S2 |
| `erupt_tell`, `erupt`, `debris` | F1 |
| `pack_up` | S2 |
| `meter_glint`, `bubble_crack` (via `hud/meter_hit`), `bubble_glow`, `break_burst`, `break_ring`, `sink_dust`, `groggy_sparks`, `recover` | S5, S3 |
| `death_flicker`, `death_fall`, `death_fade` | S4 |

Telegraphs:
- `tele/disc`: C1, C2, C4, C5, C6, F1, F2;
- `tele/line`: C6 / F2 throws;
- `tele/mline` + `_aim` + `_end`: C3;
- `tele/wave`: W.

HUD (`hud/*`):
- `meter_open`, `meter_hit`, `meter_close`;
- `hint_on` / `hint_off`;
- `lowg_on` / `lowg_off`;
- `banner_field` / `banner_end`;
- `groggy_on` / `groggy_off`;
- `pop_break`, `flash_gold`, `flash_white` (optional);
- `put_extra` / `put_sub`;
- `clear`.

Not used: the props `laser_core` / `laser_glow` (the rig draws the beams), `column` / `ousia_col` (rig parts),
`charge` / `muzzle` / `bubble0..3` (the rig's `core_glow` / `core_shell` and the presets cover them), `bomb` (the
`bomb_drop` card instead), `pebble` / `chunk` (the presets).

Budgets (kit measurements, cap 64 fx / 40 telegraph cards): C1 32 / 16, C3 24 / 10, C4 35 / 20, C5 27 / 2,
C6 30 / 14, waves with the triple 59 / 10, F1 47 / 14 (8 ambient skips), break 19, entrance 12, field warp 14.

## 7. Sound list

### 7.1 Kit recipes (`fx/snd/<name>`, `fg_fx_api.md` §6)

| recipe | used in |
|---|---|
| `awake_clank`, `unfold`, `gear_click`, `eye_open`, `rise_hum` | E (`rise_hum` also S2) |
| `bomb_port`, `bomb_drop`, `bomb_fall`, `bomb_burst` | C1 |
| `column_tell`, `plunge`, `slam` | C1, C2 |
| `pods_drop`, `laser_charge`, `laser_fire`, `laser_loop`, `laser_stop` | C3 |
| `tip_flare`, `missile_vent`, `missile_launch`, `missile_dive`, `missile_impact` | C4 |
| `core_flip`, `core_spark`, `core_lift`, `up_beam`, `column_down`, `blast`, `rocks_hover`, `debris_land` | C5 (`core_flip` also S2, S3; `debris_land` also C4, C6, F1, F2) |
| `dip`, `vent_flare`, `tower_up`, `flame_charge`, `floor_burst`, `slab_lift`, `slab_throw`, `slab_impact`, `revert` | C6, F2 (`revert` also S2) |
| `halo_flip`, `warp_out`, `glitch`, `warp_in`, `field_unfold`, `field_hum`, `field_banner` | S1 |
| `wave_charge`, `wave_charge2`, `wave_beam`, `wave_burst`, `wave_ring`, `lift_off` | W |
| `erupt_tell`, `erupt` | F1 |
| `pack_up` | S2 |
| `meter_tick`, `bubble_crack` | S5 |
| `break_glow`, `break_burst`, `groggy_wobble`, `groggy_spark`, `recover` | S3 |
| `death`, `death_fall`, `death_fade` | S4 |

### 7.2 Extra vanilla layers (all `hostile`, minVolume rule)

| event v/p | used in |
|---|---|
| `block.respawn_anchor.ambient` 0.6/0.6, `block.beacon.ambient` 0.4/0.6, `block.piston.extend` 0.6/0.8, `block.grindstone.use` 0.3/0.6, `block.beacon.activate` 0.5/1.3 | E |
| `entity.breeze.whirl` 0.5/0.9, `entity.breeze.charge` 0.6/0.6 | C1 |
| `block.beacon.power_select` 0.5/1.2 | C1, C2 |
| `block.piston.contract` 0.6/0.8 + `entity.breeze.wind_burst` 0.4/0.9 | C1, C2 (rise) |
| `block.amethyst_block.chime` 0.4/1.8, `block.respawn_anchor.charge` 0.5/1.9, `block.amethyst_block.resonate` 0.4/1.6, `block.piston.contract` 0.6/0.9 | C3 |
| `block.fire.ambient` 0.6/0.9 | C4 |
| `block.respawn_anchor.set_spawn` 0.6/0.6, `block.beacon.power_select` 0.6/0.6, `block.crafter.craft` 0.6/1.0 and 0.5/1.0, `block.amethyst_block.resonate` 0.7/0.6, `block.amethyst_cluster.break` 0.7/0.7, `entity.generic.explode` 0.4/1.3, `block.piston.contract` 0.6/0.9, `block.chain.place` 0.5/1.0 | C5 |
| `block.amethyst_block.resonate` 0.3/1.4 (burst decal cue), `block.chain.hit` 0.5/0.8 (throw tell) | C6, F2 |
| `block.piston.contract` 0.5/0.9 | F2 |
| `block.beacon.power_select` 0.8/1.2, `block.beacon.activate` 0.5/0.7 | S1 |
| `block.heavy_core.place` 0.8/0.6, `block.anvil.land` 0.5/0.6 | W (`wave_drop` landing) |
| `block.beacon.activate` 0.7/1.3, `block.conduit.activate` 0.6/1.2, `block.crafter.craft` 0.6/0.7, `block.chain.place` 0.5/1.2 and 0.6/0.9, `block.copper_trapdoor.close` 0.6/0.9 | F1 |
| `block.chain.place` 0.6/0.9, `block.chain.step` 0.6/0.7, `block.crafter.craft` 0.5/1.1 | S2 |
| `block.chain.step` 0.5/0.6, `block.beacon.deactivate` 0.8/0.7, `block.anvil.place` 0.3/0.5 | S3 |
| `block.beacon.deactivate` 0.5/1.6 and 0.4/1.8, `block.chain.fall` 0.6/0.8, `block.copper.fall` 0.5/0.8, `block.anvil.place` 0.6/0.5, `block.chain.step` 0.5/0.6 | S4 |

At most 4 layers on one tick. No creature voice anywhere (`deathSnd` false; the device is a machine).

## 8. Validation to run with the implementation

The harness of `mb3/tests/run_all.sh <worktree>/roguelike [tag]` (the shape of `mb2/tests/run_all.sh`):
- the fieldgen suites (`test_fieldgen.py`, with the per-pattern cases of each spec's §13, or a `pat_cruise.py` /
  `pat_field.py`), `test_e2e_fieldgen.py`, `test_fwopts.py`;
- the butterfly and Guardian suites, `gen_check.py` (order, second run, reverse order, wipe), `ident.py`;
- the kit's `fxtests/test_fg_fx.py`;
- the validators compared with `mb3/tests/baseline/`:
  - `check_refs`;
  - `check_macro` (from the datapack root);
  - `check_nbtpath` (0 invalid);
  - `tools/check_mboss_pack.py` (0 problems);
  - `lint_mc`.
