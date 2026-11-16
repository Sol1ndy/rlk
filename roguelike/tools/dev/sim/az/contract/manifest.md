# Day-0 contract: the Azhdaha rig manifest, schema v1 (`manifest.md`)

Owners: **S1-MOD** (the stub manifest and `check_az_manifest.py`) and **R3 / R3a** (the real manifest written by
`T:build_mboss_azhdaha_rig.mjs`). Readers: S1-CM (the framework compiles hit proxies, capsules and state sets from it,
cm.md §9), S1-MOD (`api.py` clip table, `stub_rig.py`), S1-FX (nothing; the kit never reads it), S2 (through `api.py`
only), Apep (its manifest extends this schema: Apep plan §3.9). Binding inputs: `S:az/plan.md` R1-R11, Rig decision
changes 1-3, §3.1-§3.6, §4.12 (rest anchors), §5 (clip use). Grounded in the committed R1 rig (`wip/az-rig` 7c3e9fe,
`S:az/wt_rig/roguelike/tools/mboss_azhdaha_rig_manifest.json` and `mboss_azhdaha_rig_api.md`).

The schema is **frozen at R3a**; until then additions are allowed only when S1-MOD and R3 agree in this file. Names,
lengths and event ticks of §5 are binding from D0 (a change needs a numbered change note in the plan and re-runs the
affected S2 suites).

---------------------------------------------------------------------------------------------------

## 1. Files

| file | writer | when |
|---|---|---|
| `T:mboss_azhdaha_rig_manifest.json` | the rig builder (R3a: `"source": "rig"`) | on `wip/az-rig`; on `wip/az` from I1 |
| `T:mboss_azhdaha/stub_rig_manifest.json` | S1-MOD's `stub_rig.py` (`"source": "stub"`) | from S1-MOD's first commit; used for every clip the real manifest lacks |
| `T:mboss_cproto_rig_manifest.json` | S1-CM (static, `"source": "stub"`) | cproto's two proxies (cm.md §14) |

Consumers (`api.py` and the framework, cm.md §9.2) read the **same merge**: the real manifest counts only when it has
`"schema": 1` and `"source": "rig"` (the R1 file of `wip/az-rig`@7c3e9fe has no `schema` and counts as absent); clips:
every real clip, plus stub clips only for names the real manifest lacks (`api.FALLBACKS`, printed by the build; the I2b
build asserts it is empty); global keys (`proxies`, `uuids`, `states`, `capsules`, `runtime`, `rest_anchors`,
`torso_hw`, `functions`) from the real file when present, else from the stub. `check_az_manifest.py` validates both
files and the merge.

## 2. Frames and units

- **Rig frame** (R1, unchanged): +x the boss's left, +y up, **+z back** (−z forward), blocks, origin = the floor under the
  centre of the four feet. Used only by `skeleton`, `extents`, `rest_extents`, `cull_overhang`.
- **Local frame** (every gameplay field: `rest_anchors`, `anchors`, `tracks`, `px`, `capsules`, `proxies.rest`):
  **x = s** (+ the boss's left), **y** up, **z = f** (+ forward, toward the head), blocks, origin = the anchor (the body
  husk, on the floor). `local = (rig.x, rig.y, −rig.z)`. The Minecraft command `^x ^y ^z` from the anchor (rotated as
  the anchor) is exactly this frame.
- Ticks are **played** ticks (after RETIME), 0 = the tick the clip starts (the module's pattern clock = the clip tick).
- Yaw: degrees in Minecraft units (added to `Rotation[0]`; + = clockwise from above; turning toward the boss's own
  left is negative).
- Clips carry no horizontal root travel and no root yaw (the module moves and turns the anchor), except the root z
  offset of hidden spans (Rig decision change 1, §4.7).

## 3. Top level

| key | type | content |
|---|---|---|
| `schema` | 1 | |
| `boss` | `"azhdaha"` | |
| `source` | `"rig"` / `"stub"` | |
| `runtime` | object | `{"ns": "rlk:mboss/azhdaha/rig/", "clip_obj": "azRigC", "tick_obj": "azRigT", "state_obj": "azRigState", "legs_obj": "azRigLegs", "tail_obj": "azRigTail"}` — the anchor's objectives: current clip id, the tick of the pose shown this tick (after the rig tick; −1 = queued), visibility state, looks |
| `functions` | object | the rig API (§7) as full function ids |
| `parts` | [object] | R1 part records + `idx` (UUID low byte): `name region uuid idx tag model brightness scale elements`. Part names never start with `p<digit>`, `x`, `ap_`, `fld`, `lock`, `kept`, `pat`, `orbc` or `seal` (the module's `rlk_mb_az_*` tag space, s2.md §12; the R3 builder asserts it) |
| `uuids` | object | `{"block": "524c4b4d-415a-4400-8000-0000000000", "ints": [1380731725, 1096434688, -2147483648], "parts": {name: idx}, "shadow": 64, "proxies": {name: idx}, "props": {"seal_prism": 128, "crater": 129}}` — `parts` is the fixed append-only name → index table (Rig decision change 3; R1's order head 1 … tip 46 is the initial table; a part added in R2, e.g. `tail_skirt` on `wip/az-rig-tail`, is appended from 47 = 0x2F in R3's merge order, never inserted) |
| `skeleton` | object | R1 (`joints` rig frame, `scale_H` 7) |
| `rest_anchors` | {name: [x, y, z]} | local frame, at rest (§4.1) |
| `torso_hw` | number | the torso half-width (3.0 at R1) |
| `proxies` | object | `layout` (§6.1) and `rest` (`{name: [x, z, top]}` local) |
| `states` | object | framework proxy / state sets (§6.2) |
| `capsules` | object | push capsules (§6.3) |
| `flash_groups` | {group: [part]} | R1 (`head front rear tail`) |
| `looks` | object | R1 `legs` / `tail` channels + `functions` incl. `petrify`, `glow_on`, `glow_off` (§7) |
| `clips` | [clip] | §4 |
| `culling` | object | `{"width": 30, "height": 12, "view_range": 3}` |
| `rest_extents`, `budgets`, `objectives`, `textures` | | R1 (+ per-region budgets from R3: `budgets.regions {head:{parts,px}, …}`) |
| `fallbacks` | [str] | stub only: the clip names it provides |

## 4. Clip record

```json
{"id": 12, "name": "chin_slam", "len": 65, "authored": 84, "loop": false, "next": "idle", "mirror_of": null,
 "retime": [[0, 0], [47, 35], [84, 65]],
 "events": {"lift": 2, "rear": 14, "top": 23, "drop": 32, "impact": 35},
 "anchors": {"impact": {"impact": [0.0, 0.0, 6.4], "nose": [0.0, 0.6, 5.6]}},
 "tracks": {},
 "px": {"lerp": true, "keys": {"0": {"head": [0.0, 4.3, 3.05], "chest": [0.0, 2.1, 4.85], "...": []}, "64": {}}},
 "yaw": null, "hidden": [], "root_z": [], "state": [],
 "extents": [[-4.1, 4.1], [-0.35, 9.2], [-6.0, 13.5]], "cull_overhang": null, "keyFiles": 31, "keys": 1400}
```

| field | rule |
|---|---|
| `id` | int, unique in the file (the rig's `clip_obj` value); never hard-coded by the module |
| `name` | §5 names; extra clips are allowed only as `dbg_<name>` (R1 debug poses; ignored by the module and the checks) |
| `len` | played length; the clip shows ticks 0..len−1 and then `next` |
| `authored` | authored length (footage speed) |
| `loop` | true → repeats; `next` must be null |
| `next` | clip name played after the last tick, or null = hold the last pose |
| `mirror_of` | for the 6 mirrors (§5): s → −s, yaw negated, names swapped: proxies `paw_l`↔`paw_r`, `foot_l`↔`foot_r`; anchors `paw_fl`↔`paw_fr`, `foot_hl`↔`foot_hr` (the per-clip `paw` point is mirrored, not renamed) |
| `retime` | `[[authored, played], …]` monotone knots from `[0,0]` to `[authored, len]` (`[]` when authored = len); retime only compresses (plan §0) |
| `events` | `{name: played tick}`, every name of §5; `0 ≤ t ≤ len` (`t = len` = the clip's end, e.g. `landslide.end`) |
| `anchors` | `{event: {point: [x, y, z]}}`: named local points at that event's tick (§4.1) |
| `tracks` | `{"tail_root": [[x, y, z] × len], "tail_tip": [[x, y, z] × len]}` local, one entry per played tick 0..len−1 (required for the clips of §4.3) |
| `px` | `{"lerp": true, "keys": {"<t>": {proxy: [x, z, top]}}}`: every proxy in every key; keys at 0 and len−1 required; `top` = the column top above the floor (margin included), **0 = hidden** (§4.4) |
| `yaw` | null, or `[delta × len]`: the cumulative anchor-yaw delta per played tick (Minecraft units) the module applies (§4.5) |
| `hidden` | `[[t0, t1, "body" | "tail" | "all"]]` inclusive spans (0 ≤ t0 ≤ t1 ≤ len−1) with `visBody` / `visTail` 0; authoritative for the clip's own ticks |
| `root_z` | `[[t0, t1, dz]]` inclusive: local-z (f) offset of the root during a hidden span (§4.7) |
| `state` | `[[t, "normal" | "burrowed" | "tail_only"]]`: the recorded rig state (`azRigState`, what a respawn re-applies) from tick t; `t = len` = applied at the hand-over to `next`. Must agree with `hidden` (`burrowed` ⇔ "all", `tail_only` ⇔ "body", `normal` ⇔ no span) |
| `extents`, `cull_overhang`, `keyFiles`, `keys` | R1 bookkeeping (rig frame) |

### 4.1 Anchors

`rest_anchors` (required; local; R1 numbers in brackets): `nose` (0, 0.85, +5.5), `head_col` (0, 0, +4.3: the head
column's floor point), `head_front` (`head_col` + 2.5 b forward, floor), `chest` (0, 0, +2.1), `hips` (0, 0, −3.4),
`tail_root` (0, 2.85, −4.75), `paw_fl` (+3.15, 0, +2.95), `paw_fr` (−3.15, 0, +2.95), `foot_hl` (+2.5, 0, −2.55),
`foot_hr` (−2.5, 0, −2.55), `back` (0, 4.0, −0.2: the dorsal launch area). Every zone threshold of plan §4.12 is computed
from these by `api.py` (never typed by hand).

Per-clip anchors required (point names in parentheses; floor points have y 0):

| clip | event → points |
|---|---|
| `chin_slam` | `impact` → (`impact` floor point of the chin, `nose`) |
| `jump_slam` | `land` → (`nose`); `wave2` → (`nose`) |
| `spikes` | `launch` → (`launch_1`, `launch_2`, `launch_3`, `launch_4`: the four spike launch points on the back); `launch_last` → (`launch_4`) |
| `stomp_fl/_fr/_hl/_hr` | `slam`, `w1`, `w2`, `w3` → (`paw`: the slamming paw's floor point) |
| `stomp3_fl/_fr` | `s1`, `s2`, `s3` → (`paw`: the paw of that slam, A / B / A) |
| `feint` | `burst` → (`nose`, `tail_root`) |
| `tail_whip_l/_r` | `sweep`, `sweep_end`, `erupt` → (`tail_root`, `tail_tip`) |
| `tail_slam` | `slam`, `impact`, `spikes` → (`tail_root`, `tail_tip`) |
| `tail_cast` | `charge`, `fire` → (`tail_tip`) |
| `roar_low`, `roar_rear` | `roar` → (`nose`) |
| `absorb`, `absorb_p3` | `burst` → (`back`) |
| `p3_sink` | `pillar` → (`tail_root`, `tail_tip`) |
| `tail_pillar_strike` | `strike` → (`tail_tip`) |
| `walk`, `walk_stop`, `turn*` | every plant event → (`paw`: the planted foot's floor point) |

### 4.2 Retime

The rig authors at footage speed and compresses with the shared `RETIME` knots (`mboss_rig_clips.mjs`); `retime` lists the
knots; `events` are played ticks. The module reads played ticks only.

### 4.3 Tracks (required)

`tail_whip_l`, `tail_whip_r`, `tail_slam`, `tail_cast`, `tail_pillar`, `tail_pillar_strike`, `tail_pillar_sink`, `p3_sink`:
`tail_root` and `tail_tip`, every played tick, local frame **in the anchor frame before the yaw schedule** (the module
composes them with `yaw` to get world points). The P7 hazard wedges and their decal union are computed from these
(s2.md §6.3).

### 4.4 Proxy columns

- Every key lists all 12 proxies `[x, z, top]` (local floor point and column top). A proxy whose bone is hidden or whose
  top ≤ 0.3 b is parked by the framework (top written as 0 for hidden bones).
- Keys: at least 0 and len−1; between keys the framework interpolates linearly (`lerp`). R3a writes a key on every tick
  where any proxy differs by > 0.1 b from the interpolation of its neighbours (the framework compiles an update whenever a
  sampled proxy moved > 0.15 b, cm.md §9.3).
- `tail_only` clips (`tail_pillar*`, `p3_sink` from `pillar`): tail1-4 stacked at the anchor (x, z within 0.3 b of 0),
  tops along the pillar; the body proxies hidden (top 0).

### 4.5 Yaw schedules (required)

| clip | schedule (cumulative delta at played tick t) |
|---|---|
| `turn45_l` / `_r` | 0 for t ≤ `yaw0`, monotone to ∓45 at `yaw1`, constant after (`_l` = toward the boss's left = negative) |
| `turn90_l` / `_r` | the same to ∓90 |
| `turn180` | 0 → −180 between `yaw0` and `yaw1` (turns toward its left; the module mirrors the sign when it wants the other way) |
| `tail_whip_l` | 0 for t ≤ 20; smoothstep 0 → **+115** over t20 → 31; **+122** at t35 (harmless overshoot); back to **+115** by t42; constant after. `_l` sweeps the boss's **left** flank (the anchor turns to its right, the tail swings from behind into the left side) |
| `tail_whip_r` | the mirror (negated) |
| `charge_stop` | optional skid yaw, \|delta\| ≤ 30 |

All other clips: `null`.

### 4.6 Hidden spans and states

Required (binding values; the stub writes exactly these, R3a may hide **more** parts inside a span but not fewer ticks):

| clip (len) | `hidden` | `state` |
|---|---|---|
| `burrow_dive` (40) | `[]` (`under` 40 = len: the body vanishes at the hand-over) | `[[40, "burrowed"]]` |
| `burrow_travel` (20) | `[[0, 19, "all"]]` | `[]` (already burrowed) |
| `burrow_breach` (36) | `[[0, 7, "all"], [30, 35, "all"]]` (visible from `burst` 8 to `under` 30 − 1) | `[[8, "normal"], [30, "burrowed"]]` |
| `burrow_emerge` (53) | `[[0, 23, "all"]]` (visible from `fore` 24) | `[[24, "normal"]]` |
| `p3_sink` (66) | `[[40, 65, "body"]]` | `[[40, "tail_only"]]` |
| `tail_pillar` (80), `tail_pillar_strike` (24) | `[[0, len−1, "body"]]` | `[]` |
| `tail_pillar_sink` (20) | `[[0, 17, "body"], [18, 19, "all"]]` | `[[18, "burrowed"]]` |

Every other clip: `hidden []`, `state []` (`intro`: the seal props hide nothing). The px state the module sets is
independent (P9 uses `inv` from `burrow_dive` t30 to `burrow_emerge` `out`; B3 per s2.md §7.1); `px/state` calls a
`vis` function only for `normal` and `tail_only` (§6.2), which the module sets only on visible ticks of these spans.

### 4.7 Root z offset (Rig decision change 1)

While the body is hidden (`hidden` body / all), a clip may carry `root_z` so that the tail-only pillar stands on the
anchor: at the floor cut the pillar base is at local (x, z) within 0.3 b of (0, 0). `root_z` is 0 on every tick where any
body part is visible (the builder and `check_az_manifest.py` assert it). The module keeps one point (the anchor) for the
pillar, the crater, the safe circle on the tail and the emergence.

## 5. Binding clip table (41 entries: 35 authored + 6 mirrors)

Played lengths and events from plan §3.2 (authored → played by RETIME). `next` defaults to `idle`.

| clip | len | authored | loop / next | events (played) |
|---|---|---|---|---|
| `idle` | 80 | 80 | loop | `snarl 30` |
| `walk` | 40 | 40 | loop | `lh 0 lf 10 rh 20 rf 30` |
| `walk_stop` | 16 | 16 | idle | `plant 4` |
| `turn45_l`, `turn45_r` (mirror) | 24 | 24 | idle | `plant_1 10 plant_2 17 yaw0 4 yaw1 18` |
| `turn90_l`, `turn90_r` (mirror) | 36 | 36 | idle | `plant_1 12 plant_2 18 plant_3 24 plant_4 30 yaw0 6 yaw1 30` |
| `turn180` | 60 | 60 | idle | `plant_1 12 plant_2 18 plant_3 24 plant_4 30 plant_5 36 plant_6 42 plant_7 48 plant_8 54 yaw0 6 yaw1 54` |
| `intro` | 150 | 150 | idle | `eyes 25 rise 30 crack1 50 crack2 70 seal 112 land 116 roar 120 blast 130` |
| `pose_ref` | 20 | 20 | loop | — |
| `roar_low` | 40 | 50 | idle | `roar 8 blast 10` |
| `roar_rear` | 82 | 100 | idle | `rise 8 roar 20 drop 62 land 74` |
| `chin_slam` | 65 | 84 | idle | `lift 2 rear 14 top 23 drop 32 impact 35` (head low 35-55) |
| `jump_slam` | 53 | 60 | idle | `crouch 0 takeoff 6 apex 13 land 21 wave2 32` |
| `charge_coil` | 26 | 34 | `charge_run` | `coil 6 launch 24` |
| `charge_run` | 12 | 12 | loop | `plant 6` |
| `charge_stop` | 21 | 24 | idle | `skid 0 stop 8` |
| `spikes` | 40 | 48 | idle | `brace 0 launch 14 launch_last 20 gold_on 0 gold_off 22` |
| `stomp_fl`, `stomp_fr` (mirror), `stomp_hl`, `stomp_hr` (mirror) | 63 | 72 | idle | `lift 5 slam 13 w1 17 w2 32 w3 47` |
| `stomp3_fl`, `stomp3_fr` (mirror) | 85 | 90 | idle | `lift 3 s1 17 s2 40 s3 63` |
| `feint` | 50 | 56 | idle | `sway 0 swayback 12 drop 18 burst 22` |
| `tail_whip_l`, `tail_whip_r` (mirror) | 64 | 64 | idle | `raise 0 cock 12 pivot 20 sweep 23 sweep_end 31 erupt 33 settle 42` |
| `tail_slam` | 70 | 90 | idle | `raise 0 hold 9 slam 36 impact 39 spikes 41` |
| `burrow_dive` | 40 | 44 | `burrow_travel` | `snarl 3 dive 14 under 40` |
| `burrow_travel` | 20 | 20 | loop | — |
| `burrow_breach` | 36 | 36 | `burrow_travel` | `ring 0 burst 8 hit 10 under 30` |
| `burrow_emerge` | 53 | 56 | idle | `rumble 0 burst 8 fore 24 out 38 shake 40` |
| `landslide` | 203 | 270 | idle | `tell 0 w1 57 w2 77 w3 98 w4 118 w5 139 rear 159 w6 179 end 203` |
| `absorb` | 94 | 108 | idle | `press 0 rise 46 burst 47 stamp1 62 stamp2 86 gold_on 0 gold_off 60` |
| `absorb_p3` | 52 | 70 | idle | `orb 0 burst 42 gather 42 gold_on 0 gold_off 50` |
| `p3_sink` | 66 | 80 | `tail_pillar` | `sink 8 under 40 tail 40 pillar 58` |
| `tail_pillar` | 80 | 80 | loop | `pulse 0 pulse2 40` |
| `tail_pillar_strike` | 24 | 24 | `tail_pillar` | `strike 10` |
| `tail_pillar_sink` | 20 | 20 | hold (null) | `gone 18` |
| `tail_cast` | 34 | 40 | idle | `raise 0 charge 12 fire 18 lower 26` |
| `death` | 120 | 120 | hold (null) | `stagger 0 chin 34 tail 66 last 80 head 92 still 96` |

RETIME knots (authored → played): `roar_low` [0,0][10,8][50,40]; `roar_rear` [0,0][20,20][76,62][100,82]; `chin_slam`
[0,0][47,35][84,65]; `jump_slam` [0,0][28,21][60,53]; `charge_coil` [0,0][32,24][34,26]; `charge_stop` [0,0][8,8][24,21];
`spikes` [0,0][18,14][24,20][48,40]; `stomp_*` [0,0][22,17][52,47][72,63]; `stomp3_*` [0,0][22,17][90,85]; `feint`
[0,0][22,22][56,50]; `tail_slam` [0,0][52,39][58,45][90,70]; `burrow_dive` [0,0][18,14][44,40]; `burrow_emerge`
[0,0][40,40][56,53]; `landslide` [0,0][76,57][104,77][132,98][156,118][186,139][212,159][240,179][270,203]; `absorb`
[0,0][12,12][60,46][108,94]; `absorb_p3` [0,0][60,42][70,52]; `p3_sink` [0,0][8,8][50,40][80,66]; `tail_cast`
[0,0][24,18][40,34]; all others none. (`jump_slam` is re-authored at 60: crouch 0-6, take-off 8, apex 18, land 28,
wave 2 39; `tail_whip_*` re-authored at 64; `stomp3_*` new; `tail_cast` replaces motion.md's `tail_shells`.)

Pose notes binding for R3a (the module depends on them): `chin_slam` head column low (top ≤ 3.5) t35-55; `jump_slam`
airborne t6-21 (the module glides the anchor by `mv/leap`, the clip only poses); `landslide` turns nothing (the module
turns the anchor in place t0-45); `absorb*` untargetable windows are the module's.

## 6. Proxies, states, capsules

### 6.1 `proxies.layout` (12 entries, this order; `idx` = UUID low byte, `mbPart` = position + 1)

I1 (2026-10-20): the last two columns are the R3a rig's numbers (`mboss_azhdaha_rig_manifest.json`, wip/az-rig 6635fe1);
the stub (`stub_rig.py`) and `check_az_manifest.py` check both. `rest` stays the pinned R1 column set (`proxies.rest`:
the zone / melee-point reference, `api.P_TAIL_LANE` = tail2's floor point); `rest_pose` (`proxies.rest_pose`) is the
real idle pose, whose tail is curled up over the back (tail1-4 columns at z −5.9 … −4.5, tops 4.5 … 11.7). The runtime
always uses the per-clip `clips[].px` keys, never either of these. R1's `tail5` column stays dropped (12 proxies).

| name | part (R1 bone) | w | top margin | flash | idx | rest `[x, z, top]` (local, R1, pinned) | point (bone-local, rig frame, R3a) | rest_pose `[x, z, top]` (R3a idle) |
|---|---|---|---|---|---|---|---|---|
| `head` | head | 2.8 | 1.6 | head | 0x41 | [0, 4.3, 3.05] | [0, −0.6, −0.6] | [0, 4.3, 3.05] |
| `chest` | chest | 4.6 | 1.5 | front | 0x42 | [0, 2.1, 4.85] | [0, 0, −0.4] | [0, 2.1, 4.85] |
| `belly` | belly | 4.6 | 1.5 | rear | 0x43 | [0, −0.5, 4.85] | [0, 0, 0.2] | [0, −0.5, 4.85] |
| `hips` | pelvis | 4.4 | 1.2 | rear | 0x44 | [0, −3.4, 4.2] | [0, 0, 1] | [0, −3.4, 4.2] |
| `tail1` | t1 | 2.6 | 1.2 | tail | 0x45 | [0, −6.35, 3.94] | [0, 0, 1.2] | [0, −5.863, 4.5] |
| `tail2` | t3 | 2.2 | 1.0 | tail | 0x46 | [0, −10.12, 3.9] | [0, 0, 1] | [0, −8.59, 7.209] |
| `tail3` | t5 | 1.8 | 0.9 | tail | 0x47 | [0, −12.86, 5.81] | [0, 0, 0.9] | [0, −7.898, 10.434] |
| `tail4` | t7 | 1.4 | 0.8 | tail | 0x48 | [0, −11.9, 8.51] | [0, 0, 1.5] | [0, −4.458, 11.736] |
| `paw_l` | paw_l | 1.8 | 2.6 | front | 0x49 | [+3.15, 2.95, 2.8] | [0, −0.3, −0.55] | [+3.15, 2.95, 2.8] |
| `paw_r` | paw_r | 1.8 | 2.6 | front | 0x4A | [−3.15, 2.95, 2.8] | [0, −0.3, −0.55] | [−3.15, 2.95, 2.8] |
| `foot_l` | foot_l | 1.8 | 2.6 | rear | 0x4B | [+2.5, −2.55, 2.92] | [0, −1.18, −0.35] | [+2.5, −2.55, 2.92] |
| `foot_r` | foot_r | 1.8 | 2.6 | rear | 0x4C | [−2.5, −2.55, 2.92] | [0, −1.18, −0.35] | [−2.5, −2.55, 2.92] |

Record keys: `name part point w top_margin tail_only idx uuid flash` (`point` = the bone-local point, rig frame: R1's
until I1, the R3a rig's since). `proxies` = `{layout, rest, rest_pose}` (+ the rig's `note`). R1
columns had a `base`; v1 columns always start at the floor (`base` dropped; `top` from the floor).

### 6.2 `states` (the framework's proxy / state sets; plan §3.3)

```json
"states": {
  "normal":    {"px": ["head","chest","belly","hips","tail1","tail2","tail3","tail4","paw_l","paw_r","foot_l","foot_r"],
                "vis": "normal", "inv": false, "capsules": ["torso", "head"]},
  "jump":      {"px": [], "vis": null, "inv": false, "capsules": []},
  "inv":       {"px": [], "vis": null, "inv": true,  "capsules": []},
  "tail_only": {"px": ["tail1","tail2","tail3","tail4"], "vis": "tail_only", "inv": false, "capsules": []},
  "dead":      {"px": [], "vis": null, "inv": true,  "capsules": []}
}
```

`vis` names a rig visibility state (`functions.state.<vis>`) the framework calls on `px/state`; null = leave the rig
alone (the clips switch visibility themselves). `inv` and `dead` are required in every px manifest (cm.md §9.2).

### 6.3 `capsules` (blocks, local frame)

```json
"capsules": {"torso": {"f0": -3.8, "f1": 2.6, "hw": 2.8},
             "head":  {"f0": 2.6, "f1": 5.4, "hw": 1.6, "px": "head", "top_max": 3.5}}
```

`head` is active only while the head proxy's current top ≤ 3.5 b (the head is low). The framework converts to tenths
(`push[]`, cm.md §13.5); the module decides when the push is on (plan §4.12).

## 7. Rig API (`functions`; all `rlk:mboss/azhdaha/rig/…`, @s = the anchor, at it unless noted)

| key | function(s) | from |
|---|---|---|
| `init`, `spawn`, `tick`, `kill`, `uninstall`, `look_apply` | as R1 | R1 |
| `play` | `play/<clip>` for every §5 clip | R1 → v1 |
| `face` | `face/player`, `face/track` (≤ 2°/call), `face/set {yaw}` | R1 |
| `state` | `state/normal`, `state/burrowed`, `state/tail_only` (visibility) | R1 |
| `look_legs` / `look_tail` | `look/legs/<geo|hydro|pyro>`, `look/tail/<geo|cryo|electro>` | R1 |
| `petrify` | `look/petrify` (base looks at brightness −3 + a gold rim pulse; mandatory) | R3 |
| `glow_on` / `glow_off` | `glow/gold_on`, `glow/gold_off` (gold parts 13 → 15 and back) | R3 |
| `flash` | `flash/<head|front|rear|tail>` (3-t outline of one group) | R1 |

The rig owns no proxy runtime (`px/*` is the framework's). The shadow display (`shadow_radius 4.5`, UUID 0x40) follows the
anchor. Brightness: hide 13, matte gold 13 (15 only through `glow/gold_on`), eyes 15 in every phase.

## 8. Stub manifest rules (`stub_rig.py`, S1-MOD)

Every §5 clip with `len`, `authored`, `loop`, `next`, `retime`, `events`; anchors from `rest_anchors` (chin `impact` =
`nose` floor point + 1.0 b forward; stomp `paw` = the clip's paw; whip / slam points from the stub tracks); tracks from a
parametric tail (root at rest, tip at 12 b behind the root, rotated by the stub yaw schedule for the whips, raised for
`tail_slam` / `tail_cast`, vertical for the pillar clips); `px` keys at 0 and len−1 = rest (hidden spans: top 0;
tail-only clips stacked at the anchor); `yaw` per §4.5; `hidden`, `root_z`, `state` per §4.6 / §4.7; the R1 `states`,
`capsules`, `proxies` as §6; `source "stub"`, `fallbacks` = all names.

- **Stub clip ids are ≥ 1000** (never a rig id; unique in the merged manifest).
- **Rig calls**: the module calls the real rig (`AZ:rig/**`) for every API function the real rig provides (R1 has
  `init spawn tick kill uninstall look_apply`, `face/*`, `state/*`, `look/legs/*`, `look/tail/*`, `flash/*` and only
  `play/<debug pose>`; no `look/petrify`, no `glow/*`, no `play/<§5 clip>`) and S1-MOD's stand-in rig
  `AZ:rig_stub/**` (module-owned) for the rest (`api.rig_fn`; `play/<clip>` goes to the real rig only for clips the real
  v1 manifest has, `api.play_fn`). The stand-in keeps time on the same anchor objectives (`azRigC` = the stub id,
  `azRigT`), so the framework's px key functions of stub clips fire and the proxies follow the stub tracks; no
  generated line references a missing rig function. The I2b build asserts no fallback is left.
- **I1 (2026-10-20)**: with the R3a rig merged every §5 clip and every rig API function is the real rig's (0 clip, 0
  event, 0 function fallbacks; the build prints the list, `api.fallback_list()`). `AZ:rig_stub/**` is then **not
  written** (`api.stub_rig_needed()`; the module's clean removes it) and the module tick calls `rig/tick` only (the stub
  `rig_stub/chain` line returns while a clip still comes from the stub). The stub manifest JSON is still written and
  committed (the core's per-clip merge reads it) and carries the R3a proxy points and `rest_pose` (§6.1).
- The stub manifest is written by `stub_rig.py` into `T:mboss_azhdaha/stub_rig_manifest.json` and **committed** (the core
  reads it before the module generator runs, cm.md §1.2); S1-MOD's first commit (the one that flips `enabled`) contains
  it.

## 9. `check_az_manifest.py` (S1-MOD; in `run_all` from I1)

Schema keys and types; the 41 names (+ `dbg_*` ignored); lengths, authored lengths, `retime` monotone from [0,0] to
[authored, len]; every event of §5 at its tick; anchors of §4.1; tracks of §4.3 with `len` entries; px keys at 0 and
len−1 with all 12 proxies; yaw schedules of §4.5 (whip: 0 at t ≤ 20, |115 − y31| ≤ 1, |122 − y35| ≤ 1, |115 − y42| ≤ 1,
monotone 20 → 31; turns: total at `yaw1`); hidden spans and states of §4.6 (the table, and `state` ⇔ `hidden`
agreement); every rig function referenced by `functions` exists in the rig output (the stub's: only while
`AZ:rig_stub/**` is written; else no module file references `rig_stub/`); `root_z` 0 wherever a body part is visible
and the pillar base within 0.3 b of the anchor; proxy layout (+ the §6.1 points and `rest_pose`, I1), UUIDs (`block + idx`, `idx` = 0x41 + position); the
`states` and `capsules` of §6; mirrors consistent (s negated, names swapped). Exit 1 on any failure.

## 10. R1 → v1 migration (R3a)

1. `px`: R1 per-event `{x, z, base, top, w, hidden}` (rig frame) → per-tick keys `[x, −z, top]` (local), `hidden` → top 0,
   `base` dropped, `w` only in `layout`.
2. Add `schema`, `source`, `runtime`, `functions`, `uuids` (the name table), `rest_anchors`, `torso_hw`, `states`
   (framework sets; the rig's own visibility `states` object becomes `functions.state`), `capsules`.
3. Clips: the §5 list replaces the R1 debug poses (kept only as `dbg_<name>`), each with `authored`, `retime`, `events`,
   `anchors`, `tracks`, `px`, `yaw`, `hidden`, `root_z`, `state`.
4. Re-author `tail_only` with the root z offset (the R1 pose put the pillar 4.4-4.8 b behind the anchor).
5. Events may sit at `t = len` (`end`); the R1 builder check "events inside the clip" becomes `0 ≤ t ≤ len`.

## 11. Decisions (D0)

1. **Gameplay fields use the local frame** (x = s left, z = f forward) under the plan's key names `{x, z, top}`; the rig
   frame (+z back) survives only in R1 bookkeeping fields. Reason: `^x ^ ^z` from the anchor is then literally the
   manifest value; R1's z sign is a trap.
2. **Columns start at the floor**; `top` includes the margin; hidden = top 0.
3. **Anchors are keyed by event** (`anchors.<event>.<point>`), so stomp3's per-slam paws and the spike launch points need
   no extra naming scheme.
4. **Tracks are dense** (one entry per played tick) for the 8 tail clips; px keys may be sparse with `lerp`.
5. **Yaw schedules are dense cumulative deltas in Minecraft units**; `tail_whip_l` = sweeps the boss's left flank with a
   positive delta; `turn*_l` turn toward the boss's left (negative).
6. **Duplicate event names are renamed** (`tail_pillar`: `pulse`, `pulse2`; turns: `plant_<k>`); events may equal `len`.
7. **`burrowed` is a rig visibility state, not a framework proxy set** (plan §3.3 lists normal, jump, inv, tail_only,
   dead); `vis` may be null.
8. **Clip ids** are the rig's (unique per file, never hard-coded); the framework compiles px dispatch from the same file.
9. **R1 debug poses** stay only as `dbg_<name>`.
10. **One merge rule for every consumer** (§1): `api.py` and the framework read the same merged manifest.
11. **Hidden spans are per tick and authoritative**; `state` records what a respawn restores and must agree (§4.6
    table); entries at `t = len` apply at the hand-over.
12. **No line references a rig function that does not exist** (§8): what the current rig lacks is served by the
    module's stand-in `AZ:rig_stub/**`, which keeps clip time on the rig's own objectives.
