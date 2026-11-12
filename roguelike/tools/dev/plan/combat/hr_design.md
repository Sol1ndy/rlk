# 홍련 (Scarlet) rebuild on the new combat — design (lane H0, 11-11)

Binding inputs, in priority order: `hr_brief.md` (the lead), `decisions.md` (the user), README 0-6, `video_notes.md` +
`ref/*.jpg` (the user's reference video; times below as `v 215.6` = seconds in it), `tools/dev/sim/hr/PLAN.md` (the old
plan: what the new video lacks, and §7), the code on `wip/combat` (`tools/mboss_scarlet/api.py` = the module contract),
lane C as built (`wip/combat-core`: `c_progress.md`, README §2 / §3) and lane B (`b_progress.md`, README 「균형치 · 그로기」).
This file is the contract for H1 (patterns / AI), H2 (cutscenes / camera / her cinematic clips) and H3 (the player
actor). Design only: nothing here is built yet. Where a number is marked *start*, HI tunes it with `hrfair` (§6.4).
Three sheets were added for the choreography: `ref/hr_repel_5fps.jpg` (v 215.4-222.8), `ref/hr_duel_2_5fps.jpg`
(v 296.2-316.6), `ref/hr_grab_4fps.jpg` (v 246.8-258.4); every tile is labelled with its video time.

Conventions
- 20 t = 1 s. `T+n` = tick n of a pattern, `#sq n` = tick n of a sequence, `h` = a hit tick. Lines are `api.LINES` ids
  (verbatim, never edited). `F:` = `data/rlk/function/`, `T:` = `tools/`.
- New-combat facts this design is built on (lane C / B, as built):
  - **F = parry**. F received p ticks before the hit: p 0-2 = tier 3 (perfect, **PP**): no damage, E-skill cooldown −20 t,
    `bal/hit {n:1}` on her; p 3-5 = tier 2: damage × 0.2; p 6-9 = tier 1: damage × 0.5; tiers 1-2 take no knockback and
    count as landed hits. After a press F is refused for 12 t (`#parGap`); after a press that blocked something only
    2 t (`#parChain`); pressing while refused extends the refusal to now + 4 (`#parRe`). One press blocks one tick's hits.
  - **Dodge** (right click, 3 b in 3 t, cooldown 12 t): against bosses only the perfect dodge (**PD**, input 0-2 t before
    the hit) avoids a hit that finds the player; PD gives +10 energy and no balance damage. Leaving a locked area on
    foot or by the dodge's own travel is always allowed (it is geometry, not a judge).
  - Order at the judge: i-frames > PD > PP > tier 2 > tier 1 > hit. An unparriable hit (`mbHzNP`) skips the parry
    tiers; lane C's automatic gold warning is `mboss/np_glint`, off while `#mbNpOwn mb 1`.
  - **Balance**: boss 12 pips; at 0 a 100-t groggy with damage taken × 1.30; regen +1 per 100 t starting 300 t after
    the last loss; sources: PP 1, a burst hit 2, strong reactions 1-2. Module hooks `bal_ok / bal_on / bal_tick /
    bal_off`; `bal/boss/may` refuses balance damage outside `#mbSt 1`, in `#mbCine 1` and while `#mbBarOff 1`.
- Frames used in §3: **ST** (the stage: origin at the avatar's feet, `f` forward toward her, `r` to the actor's right,
  `u` up), **HR** (her body: origin at her feet, `f` along her facing, `r` her right), **W** (world). A point is written
  `ST(r, u, f)`; generators turn `r` into `^-r`.

---------------------------------------------------------------------------------------------------------------------

## 0. Decisions at a glance

| topic | decision |
|---|---|
| phases | CS0 → **P1** (100 → 60 %) → **CS1** → lead-in 56 t → **G1** gauntlet → deflect: **repel** (−4.5 %) → **P2** at once (no down window); fail: 50 % hit → P2. P2 → 5 % floor → lead-in 116 t → **G2** → deflect: **repel** (kill) → **ending** → coda (PLAN §7); fail: instant death |
| removed | SQ1 and its darkness, the 200-t down window, `lead_down`, the kip-up after CS2, the A13 moon discs and yellow tell, R1 / R2 / R3, the dash-timed pips, the gauntlets' `dark` look (the video's Normal run has none) |
| parry rule | her cuts and sword-qi are parryable; the attacks the video flags with a colour flash (yellow / purple / blue) are unparriable. No text. A parryable hit is announced by a **pink sparkle glint on her blade exactly 7 t before the hit** (the aim-lock tick; the video's own glint → hit is 4-8 t) |
| gauge (5 segments) | outside the gauntlets it charges with her patterns and landed hits and the **space-cut ultimate U** spends it; in a gauntlet it starts full, each **perfect-parried cut** removes one segment, the final dive is judged on it |
| balance | 12 pips (lane B), taken only in P1 / P2; groggy = knocked onto her back 100 t, kip-up in the last 20 t; +3 pips after the first repel (the video's +4 of 20) |
| patterns | P1 14 entries + U, P2 adds 3 (§2); every video pattern P-a … P-q, U is mapped; the old A2 / A4+A5 / A6 stay (old footage, still valid) |
| gauntlets | G1 9 cuts in 220 t, G2 11 cuts in 242 t, every cut counts, ≥ 14 t apart; 5 perfect parries empty the gauge |
| cutscenes | CS0 **1440 t** (72 s; skip → the last 150 t), CS1 **720 t** (36 s; skippable), repel **140 t** ×2, ending **1372 t** + coda 120 t; all locked (spectator on a camera stand), the actor fights in every clash |
| actor | one cinematic rig, scale 1.0 for all 7 characters, one sword; 5 clips (`cs0`, `cs1`, `repel`, `ending`, `coda`) on her `#sq` clock |
| owners of new rig clips | fight clips: H1 (`scarlet_clips.mjs`); cinematic clips: H2 (`scarlet_cine.mjs`); actor clips: H3 |

---------------------------------------------------------------------------------------------------------------------

## 1. Phases, floors, gauge, balance, interrupts

### 1.1 State machine — diff against the current module (`api.PH`, `core.py`)
| state (`#ph`) | now | new | what changes |
|---|---|---|---|
| `intro` 0 | CS0 640 t, no lock | **change** | CS0 1440 t, locked, actor (§3.1); registry `intro` 650 → **1450**; the skip jumps to `#sq` 1290 |
| `p1` 1 | A1-A10 kit, floor 60 % | **change** | the new P1 kit (§2), gauge charge, balance, `#mbNpOwn mb 1` |
| `cs1` 2 | 213 t, `cine`, bars off | **change** | 720 t, locked, actor (§3.2); starts at the next decision after the floor hit, as now |
| `sq1` 3 | 60 t, re-hat, darkness | **replace** → `lead60` 3 | sequence `lead60` 56 t (§3.3): not locked, bars on, gauge 5/5 at its tick 0, no darkness |
| `a8` 4 | 9 dash-timed cuts, judge 194 | **change** | G1: 9 parry cuts, judge 220 (§2.4) |
| `cs2` 5 | repel 104 t, then `down` | **change** | repel 140 t, locked, bars **on**, three true-damage steps 15 / 15 / 15 ‰; then P2 (recovery 20 t), balance +3 |
| `down` 6 | 200 t on her back, kip-up | **remove** | the id stays reserved (unused); `core/down/**`, `DOWN_T`, `DOWN_FLOOR_WAIT`, `KIPUP_RECOVER`, the gold under bar go. Clips `down` / `kipup` stay: the balance groggy uses them |
| `p2` 7 | P1 kit + R1-R3 | **change** | the P1 kit (cooldowns × 0.85, recovery 10-16) + `mx`, `nb`, `q` (§2) |
| `lead` 8 | `lead_stand` 70 / `lead_down` 82 | **change** | `lead5` 116 t at the floor; `lead_re {g}` 60 t for restarts (pause, revive); `lead_down` removed |
| `a13` 9 | 9 cuts + 3 discs, judge 258 | **change** | G2: 11 parry cuts, no discs, no yellow, judge 242 |
| `cs3` 10 | repel, kill at the kick | **change** | repel `{at:5}`: 15 / 15 ‰ then the kill at `kick` 129; the lock continues into the ending |
| `death` 11 | ending 1042 + coda 120 | **change** | ending 1372, locked, actor; coda unchanged (120) under the same lock; registry `death` 1164 → **1494** |
| groggy (lane B `grgT`) | temp adapter: `down` + `kipup` | **change** | §1.4: `grog_in` 12 → `down` loop → `kipup` at 20 left |

Floors: `FLOOR_P1` 600 ‰ and `FLOOR_ULT` 50 ‰ unchanged (the hit reaching a floor stops there; the step starts at the next
decision, a running pattern finishes first; a groggy is cut short by its `kipup` when a step is reserved, §1.5).
Invulnerable (`rlk_mb_inv`): the intro; CS1 → the end of the repel (or the G1 fail); `lead5` → the ending; A6 ticks 0-4;
her ghost form. Not invulnerable any more: the kip-up (it is the groggy's end, she stays hittable).

### 1.2 The 5-segment gauge (`#gau hr`, 0-50 = tenths of a segment; under bar `#buSub` = `#gau / 10`, `#buSubMax 5`, `BU_SHIELD`)
| where | rule |
|---|---|
| shown | from control (CS0 end) to the ending, except CS1 (bars off); the video shows the bar all fight |
| P1 / P2 charge | +3 when a pattern ends (not A6, not U); +5 per hit of hers that lands (a tier-1 / tier-2 parry is a landed hit; PP and PD are not); cap 50; no charge while groggy, in a lead-in, gauntlet or cutscene. *start* values: full after ≈ 60 s of clean play, ≈ 30 s when hit every 6 s (video: 24.5 s and 31 s) |
| spent | U (§2.2) is armed at 50: the next near decision is `rings` → `ult` (from mid she glides in first, §8.8 HA-09; from far she closes first, far rule; a floor reached during the rings ends the chain, no `ult`, §8.8 HA-01); `#gau` → 0 at U's second cut. A PP never lowers it outside a gauntlet (v 127-154: full through 5 PPs) |
| gauntlet start | `lead60` tick 0 (the bars return full, v 203.0) and the lead-ins' `refill` beat: `#gau` = 50 in one step, kit `shield_refill` |
| gauntlet cut | −10 per cut whose hit on the player is judged tier 3 (`#parT tmp 3`), one per cut, kit `pip_break` + its sound. PD, tier 2, tier 1, walking out: nothing. Never below 0. The cut still deals no damage on PP |
| judge | at the final dive (`JUDGE_T` G1 220 / G2 242): `#gau` 0 → deflect → repel; else the fail of §2.4 |
| after | 0 after either outcome; charging resumes in P2 |

Implementation rule for the pip (H1): the counting cut is a normal parryable hazard. Right after the cut's strike the
gauntlet tick (at `#pt` = s and s + 1, as `shield/pip` does now for the tick order) takes a segment when
`#mbDodgeOk mb` is 1 **and** `#parT tmp` is 3, then clears `#mbDodgeOk`. `api.PIP_RULE = 'perfect_parry'`; `PIP_DASH`,
lane C's `PIP_Q` and `PIP_R` go (no distance pad: a parry does not move the body, the cut found the player).

### 1.3 Balance (12 pips) — her rules on top of lane B
| | rule |
|---|---|
| takes balance | only in `p1` / `p2` with `#mbSt 1`. New framework flag **`#mbBalOff mb`** (FN-bal, H1: one line in `bal/boss/may`, zeroed by `fight_vars` / `cleanup_fight`): the module holds it at 1 through the lead-ins and the gauntlets (bars are on there, so `#mbBarOff` cannot do it). CS0 / CS1 / the ending are covered by `#mbSt` / `#mbBarOff`, the repel by `#mbCine` |
| sources | lane B's: PP 1 (lane C calls `bal/hit`), burst 2, strong reactions 1-2. Regen as lane B (the video has none; the user's rule) |
| `bal_ok` (may the groggy start now) | no: a floor step reserved (`#fl`), `#sqn` ≥ 1, replay, revive wait, ghost form, `rlk_mb_inv`, airborne ticks of `a4` (2-20 and its ring hop 28-38, §8.8 HA-05), `a10` (2-22), `nb` (2-46), `q` (16 → its end), `hcut` / `a9` / `kcut` / `blue` from `go` to the cut, `ult` from `cut1` to `cut2`, A6 0-4. Otherwise yes; a refused break is lane B's pending state and starts at the first allowed tick |
| at a floor step | when CS1 or `lead5` starts with a break pending or `bal` 0: pending dropped, `bal` = 3 (she is not broken inside a cutscene and does not come out of it full) |
| after repel `{at:60}` | `bal` = min(12, `bal` + 3), `bal/ui/draw` (the video's single refill, +4 of 20); nothing at CS1, at the 5 % floor or after a G1 fail |

### 1.4 The groggy (100 t, lane B boss tier; damage taken × 1.30)
`bal_on`: `core/cancel_pat0` (hazards, locks, ghost state, her blade look off; an airborne body is put on the floor by
`core/ground`), `#gau` unchanged, clip **`grog_in`** (12 t: the guard is smashed open, she falls onto her back, the hat
lands beside her). `bal_tick`: `#clk`, looks, ambience, `core/inv` (stays hittable), at `grgT` = 88 `play down` (loop),
at `grgT` = 20 `play kipup` (she picks the hat up and puts it on, as the clip already does), `rig/tick`. `bal_off`: 12 t
recovery (`ai/rec_start`), then the AI. Effects (lane B): the break sound and flash; the diamonds row turns orange.
No line, no text. A floor reached during the groggy: `grgT` is cut to 20 (kip-up now), the step starts when it ends.

### 1.5 Interrupts
| interrupt | in P1 / P2 | in a gauntlet | in a locked cutscene |
|---|---|---|---|
| floor reached (60 % / 5 %) | reserve the step (`#fl`); counter and A6 do not start; the pattern finishes; groggy cut to its kip-up | — (invulnerable) | — |
| balance 0 | groggy now, or pending per `bal_ok` | not taken (`#mbBalOff`) | not taken |
| counter trigger (≥ 4 player hits in 40 t while she recovers, ≤ 4.5 b, 70 %) | A1 (beside / behind) or A2 (front), as now | — | — |
| skill trigger A6 (skill / burst hit ≤ 4.5 b, 60 %, cd 400) | back-blink + line 12, not locked | — | — |
| PP on a pattern's last hit (or a single hit) | she plays `flinch` 6 t and the pattern ends 6 t later (`PP_FLINCH`); other hits: the chain goes on | gauge −1 | — |
| pause (player dead / reviving / menu) | pattern frozen by the framework as now | cancelled → on resume `lead_re {g}` → the gauntlet from T0, gauge 5/5; a judged result is kept (deflect → repel, G1 fail → P2, lethal fail pending → lands on return), as PLAN §5.6 | the lock is released at once (§3.0); on resume the sequence jumps to its end state (§3.6) |
| `/reload` | as now | as pause | as pause |
| player dies in G1 from cut damage | normal death path; Ronova → `lead_re {g:a8}` | | |

---------------------------------------------------------------------------------------------------------------------

## 2. Patterns

### 2.1 Common rules (changes to PLAN §4.1 in **bold**)
- Hazards: framework shapes only, quiet, **no floor decal**, Electro 1U, `el 3`. Knockback: last hit of a chain kb 3, single
  hits kb 2, gauntlet cuts 0. Tracking chains re-aim ≤ 10°/t and step 0.3 b (stop at 2.4 b) before each hit.
- Telegraph, counted from the first visible motion: first hit ≥ 12 t (every new clip ≥ 14 t); ≥ 20 t for big hits (the
  whole arena, an area ≥ 100 b², T4, the yellow dash cuts); chain hits ≥ 10 t apart; aims lock at h − 7 (`LOCK_LEAD`). Only wind-ups are stretched; the video's gap ratios inside chains are kept (table column *video*).
- **Parry cue (code P)**: at h − 7 of every parryable hit: kit `glint {c:2}` at `blade_mid` + sound `parry_cue`
  (`block.amethyst_block.chime` 0.6 pitch 1.9; **§8.8 HA-06 / HA-07: `block.note_block.iron_xylophone` 0.7 pitch 1.8 and its
  own white-gold sprite `cue_0`**). Every parryable hazard is made with `hz_opts(noparry=0)` (the default
  rule `np_def` would flag the long lines and big discs). Outcome: PP = no damage, balance −1, `PP_FLINCH` on a last hit;
  tier 2 / 1 = damage × 0.2 / × 0.5, no knockback, gauge +5; PD = no damage; hit = full damage, gauge +5.
- **Unparriable (code N)**: `hz_opts(noparry=1)`; F changes nothing; PD avoids; gauge +5 on a hit. `#mbNpOwn mb 1` for the
  whole fight (set at `spawn`, cleared by `cleanup`): the module draws the flash itself, on her chest (anchor `chest`,
  the cards follow her):
  | flash | kit | look (video §1.6) | sound | tick |
  |---|---|---|---|---|
  | **yellow** | `yellow_tell {t:6}` (exists) | gold sphere-ring Ø 1.6 + horizontal flare | `block.bell.use` 0.6 p 1.5 + `block.beacon.power_select` 0.5 p 1.9 | ≥ 12 t before the hit, per pattern |
  | **purple** | `star4` (exists; PLAN called it a star glint) | lilac ring Ø 1.5 + 4-point star, 3 t | `block.amethyst_block.chime` 0.8 p 2.0 | exactly **12 t** before its cut (video 5-7 t), alone or after a yellow |
  | **blue** | **new** `flash_blue {t}` | a yellow ring 4 t that turns into a translucent blue sphere Ø 1.8 round her | `block.beacon.activate` 0.5 p 1.8 | sphere 15 t, then the lunge |
- Damage tiers unchanged: T1 29, T2 42, T3 62, T4 71, TC 37 (% of the base hit).
- Recovery between patterns P1 8-16 t, P2 10-16 t; tails as now (`TAIL_MOVE` 4). New `PAT_END` values in the table.

### 2.2 Pattern table (ticks on the clip clock; shapes: `sector(r, half°)`, `disc(r)` round her, `line(len, w)`, `pdisc(r)` at the player's locked spot, `dash_line(w)` along her dash, `full` = the whole arena)
| key · name | video → replaces | clip (len) | tell → lock → hit(s) → end | hazard, reach | tier · kb | parry · flash | bands (near ≤ 4.5 / mid ≤ 11 / far), P1 weight · cd; P2 weight · cd (*start*) |
|---|---|---|---|---|---|---|---|
| `a1` 회전 반월참 | P-a = A1 (kept) | `a1` (34) reuse | pivot 0 → cue + lock 7 → **14** → 24 | `sector(4.0, 80)` | T2 · 2 | P | counter (beside / behind), rear rule; 8 / 0 / 0 · 100; P2 trigger only · 85 |
| `a2` 역습 일섬 | old A2 (kept; not in the new video) | `a2` (30) reuse | glint 0 → cue + lock 5 → **12** → 22 | `sector(3.6, 70)` | T2 · 2 | P | counter (front); 8 / 0 / 0 · 100; P2 trigger only · 85 |
| `a3` 오연 반월 | P-e = A3 (kept) | `a3` (96) reuse | glint 0 → locks h − 7 → **14 / 30 / 45 / 57 / 69** → 79; video gaps 15 / 15 / 10 / 10 → 16 / 15 / 12 / 12 | `sector(4.2, 90)`, `sector(4.0, 60)`, `sector(4.0, 50)`, `line(5.0, 1.8)`, `sector(4.6, 70)` | T1 ×4, T2 · 3 last | P ×5 | 30 / 10 (≤ 8 b) / 0 · 140; 25 / 10 / 0 · 120 |
| `a3s` 쌍월참 | P-b, P-f (from mid, with the glide-in), P-l, P-o, v 133.2 → new entry | `a3` reuse, cut after h2 | as `a3` to **14 / 30** → 40 (tail move from 34) | `sector(4.2, 90)`, `sector(4.0, 60)` | T1, T2 · 3 | P ×2 | 30 / 15 (≤ 8 b) / 0 · 80; 30 / 15 / 0 · 70. Same opening as `a3`: the player cannot tell 2 from 5 before tick 38 |
| `d4` 원월 사연 | P-d → new | **`d4`** (80) | chest glint 0 → cue 7 → ring **14** → cue 27 → fan **34** → cue 37 → vertical **44** → cue 47 → slash **54** → 64; video gaps 20 / 8 / 8 → 20 / 10 / 10 | `disc(3.0)`, `sector(4.2, 35)`, `line(5.0, 1.8)`, `sector(3.6, 60)` | T1 ×3, T2 · 3 | P ×4 | 25 / 0 / 0 · 140; 20 / 0 / 0 · 120 |
| `tri` 돌진 삼월참 | P-i → new | **`tri`** (84) | glint 0 → cue + lock 7 → lunge 12-14 (≤ 6 b), **14** → cue 31 → **38** → cue 41 → **48** → cue 53 → **60** → 70; video 24 / 10 / 12 | `line(6.0, 1.6)` along the lunge, then `sector(5.0, 80)` ×3 | T1 ×3, T2 · 3 | P ×4 | 0 / 30 (≤ 10 b; beyond 6 b she glides in 0.3 b/t during 0-12) / 0 · 140; 0 / 20 / 0 · 120 |
| `a4` 월하 낙참 + 공중 원륜 | old A4 + A5 (kept) | `a4` (60) reuse | crouch 0, leap 2 → lock 12, cue 13 → **20** → cue + lock 27 → **34** → 46 | `disc(2.6)` at the landing, `disc(3.0)` | T3 · 0, T1 · 2 | P ×2 | 0 / 20 / 25 · 160; 0 / 15 / 15 · 140 |
| `rings` 회전 월륜 | P-j → new | **`rings`** (78) | glint 0 → cue 7 → **14 / 24 / 34 / 44** (P2 also **54**) → last + 10; cue at each h − 7; video 8-12 t → 10 | `disc(2.6)` round her each (she steps 0.3 b toward the player until h − 7) | T1 each, last T2 · 3 | P ×4 (5) | 20 / 0 / 0 · 160; 20 / 0 / 0 · 140. **Forced** next near pick while `#gau` = 50 (from mid she glides in first, §8.8 HA-09), then `ult` follows |
| `ult` 공간 참 (U) | U → new | **`ult`** (86) | starts 6 t after the last ring: **yellow 0** → **purple 12** → cut1 **24** (white) → web 26-44 → **purple 34** → cut2 **46** (white, burst) → 58; video 0 / 8 / 15 / … / 33 | `full` ×2 | T2 · 0, T3 · 3 | N ×2 (yellow + purple); PD only | never by weight; only after `rings` at a full gauge; `#gau` → 0 at 46 |
| `a9` 황광 원참 | P-c = A9 (kept) | `a9` (64) reuse | ring 4 (cosmetic) → **yellow 8** → **purple 16** (= clip event `star` − 1; PLAN drew it as decoration, it is the warning) → lock 22 → magenta 24 → go 26 → **28** → 40 | `dash_line(2.4)` + `pdisc(4.0)`, one group | T3 · 3 | N | 25 / 10 (≤ 7 b) / 0 · 160; 15 / 10 / 0 · 140 |
| `a10` 황광 낙참 | P-g = A10 (kept) | `a10` (56) reuse | spring 2 → **yellow 10** (in the air) → lock 14 → dive 20 → **22** → 32 | `disc(3.5)` at the lock | T3 · 3 | N | 20 / 20 / 25 · 120; 0 / 15 / 20 · 100 |
| `hcut` 황광 섬월 | P-h → new | **`hcut`** (52) | **yellow 2** → sparkle at her 8-16 → lock 19 → go 24 (≤ 16 b in 2 t, 3 b beyond the lock) → **26** → 38; video 18 t → 24 | `dash_line(3.0)` + `pdisc(4.5)` (a flat disc at knee-waist height), one group | T3 · 3 | N | 0 / 10 (≥ 8 b) / 40 · 160; 0 / 10 / 30 · 140 |
| `blue` 청광 돌파 | P-blue → new | **`blue`** (46) | **yellow ring 0** → **blue sphere 4-19** → lock 15 → lunge 20 (≤ 9 b, 2 b beyond the lock) → **22** → 32; video 15 t sphere | `dash_line(1.8)` | T2 · 2 | N (blue) | 15 / 15 (≤ 7 b) / 0 · 180; 15 / 15 / 0 · 150 |
| `kcut` 황광 난참 | P-k → new | **`kcut`** (50) | crouch 0 → **yellow 3** (big: `yellow_tell` at Ø 2.0) → pink sparkle 9 → lilac body glow 12-19 (`blade lilac`) → lock 15 → dash-through 20 (≤ 10 b) → **22** → 34; video 15 t → 19 | `dash_line(3.0)` + three `line(12, 1.6)` crossing the lock at 0° / 55° / −55°, one group (one hit) | T4 · 3 | N | 20 / 15 (≤ 8 b) / 0 · 200; 20 / 15 / 0 · 170 |
| `a6` 후방 섬보 | old A6 + line 12 (kept) | `a6` (20) reuse | as now; line 12 at 12; not locked | — | — | — | skill trigger only · 400 / 400 |
| `mx` 자광 십자참 | P-m (+ P-y as its retreat) → replaces R3 | **`mx`** (60) | (player < 6 b: 12-t leap back to ≈ 9 b first, no flash: P-y) iai crouch 0 → **purple 4** → lock 9 → streak to 1.6 b from the lock 14-16 → X **16** → cue 21 → dome **28** → 40; video 5-7 t and 4-6 t → 12 / 12 | X: `pdisc(2.8)`; dome: `disc(3.2)` | T3 · 0, T2 · 3 | X: N (purple); dome: P | P2 only: 20 / 25 / 20 · 150. At ≤ 30 % HP it may repeat once at once (`NO_REPEAT` exempt), the video's second X |
| `nb` 낙월 사선 | P-n → new | **`nb`** (66) | crouch 0, leap 2 (5 b up, ≤ 6 b toward the player) → apex 8 → cue + lock 13 → band **20** → 23 → **30** → 33 → **40** → land 46 → 52; video 6-12 t / 8 t → 10 / 10 | `line(16, 3.0)` through the lock, yawed −30° / +30° / 0° to her aim (the diagonal bands) | T2, T2, T3 · 3 | P ×3 | P2 only: 0 / 20 / 25 · 180. In the air 2-46 (44 t, under 2.2 s) |
| `q` 자영 포박 · 천공 낙월 | P-q → replaces R1 | **`q_grab`** (40) then **`q_air`** (96) | far lilac glint 0 → ghost form 4 → cue + lock 13 → ghost lunge 16-20 (≤ 14 b) → grab **20**. **Missed / PD**: reform, end 34. **PP**: flinch, end 40. **Landed** (also tier 1-2): `q_air` at 20: she throws the player back (kb 5; **§8.8 HA-08: kb 0, the throw is her pose**) and rises (2-10) → cue + lock 15 → diagonal beam **22** → cue + lock 31 → dive 34 → **38**, lands 40 → leaps 46, apex 52 → **purple 62** → lock 67 + the sky mark → pillar **74** → drops 78, lands 84 → end 90 (pattern tick 110) | grab `pdisc(2.2)`; beam `line(14, 2.6)`; dive `pdisc(2.6)`; pillar `pdisc(2.4)` | T2 · 0 (the throw: HA-08), T2 · 0, T3 · 0, T3 · 3 | grab P, beam P, dive P (the video's gold deflect), pillar N (purple) | P2 only: 0 / 20 / 30 · 300. The player is not carried into the sky (no lock in the fight; open question 7) |

Notes per pattern
- **`ult`**: clip events `yellow 0, star1 12, cut1 24, web 26, star2 34, cut2 46, settle 56`. cut1: ovl `white` in 0
  hold 2 out 2, then **new** kit `ult_web {t:20}` (12 long `qi_line` cards through the arena + **new** screen overlay glyph
  `web`, chromatic edges, the "shattered glass"); cut2: ovl `white` 0 / 3 / 6 + **new** `ult_burst` (the lines fly outward)
  + `burst_radial {r:60}`. Sounds: yellow chime 0; purple chime 12 and 34; `item.trident.thunder` 0.6 p 1.6 +
  `block.glass.break` 0.7 p 0.6 at 24; `entity.generic.explode` 0.4 p 1.6 + `block.glass.break` 0.8 p 0.5 at 46. Both
  cuts are the purple rule: star → 12 t → cut, so one timing serves both. She is hittable throughout.
- **`q`** sky mark (the only ground mark of the video, v 257.00, shown as it looks there, README 0-6): **new** kit
  `sky_mark` at the lock tick 67: a thin vertical light line from 12 b up to the lock point and a 2-b pink flash line at
  the feet, 7 t; no area decal. Pillar: **new** `sky_pillar {r:24}` (the `light_column` sprite, pink-white) +
  `item.trident.thunder` 0.5 p 1.9. Beam: **new** `qi_beam {len:140}` (the `qi_band` sprite, pitched 35°).
  The grab's ghost form uses R1's helpers (`form ghost`, `rlk_hr_ghost` 4-20: invulnerable there).
- **`mx`**: `star4` at 4; the X is `qi_x {r:25}` at the lock (the first-person offset rule of contract §3.3 stays); dome
  `qi_dome {r:35}`. **`hcut`**: `qi_ring {r:45,c:2}` flat at y + 0.7 swept along the dash + `qi_cut`. **`kcut`**: `qi_cut`
  along the dash + 3 `qi_line {len:120}`; `item.trident.riptide_3` 0.6 p 1.4 at 20. **`blue`**: `afterimage` on the lunge.
- **`rings` / `d4`**: `qi_ring {r:26|30,c:1}` at chest height (y + 1.1) per ring. **`tri`**: `qi_arc {r:50,roll:±30,c:1}`.
  **`nb`**: `qi_beam {len:160}` per band; `afterimage` at 2 / 5 / 8.
- Far rule (player > 8 b for 30 t): P1 `hcut` 45 / `a4` 30 / `a10` 25; P2 `nb` 40 / `q` 30 / `hcut` 30; fallback: glide in
  + `a3s`. Rear rule and the no-empty-band backstep as now. No immediate repeat.
- A full gauge overrides the weights: the next near decision is `rings` (its cooldown ignored), then `ult` (§8.8 HA-09: from
  the mid band she glides in first).

### 2.3 Fight clips: reused and new (owner of the new ones: **H1**, in `scarlet_clips.mjs`; a static placeholder `P(name, pose)` of the contract length goes in first so the rig builds on day 1)
Reused unchanged: `idle idle2 walk glide strafe_l strafe_r backstep flinch a1 a2 a3 a4 a6 a9 a10`, the gauntlet set
`g_brim g_tell g_reform g_dash g_glide g_drop g_run g_ring g_rise g_leap g_sweep g_x g_wrap g_dome g_vert g_dive`, `down`,
`kipup`, `ev_give ev_toast ev_leave`. Unused from now (kept in the rig, no cost): `a7_tell`, `a7_throw`, `g_deflect`.
| new clip | len | events |
|---|---|---|
| `grog_in` | 12 | hit 0, buckle 3, hat_off 6, land 10, end 12 (ends in `DOWN`) |
| `d4` | 80 | glint 0, lock1 7, h1 14, lock2 27, h2 34, lock3 37, h3 44, lock4 47, h4 54, end 80 |
| `tri` | 84 | glint 0, lock0 7, go 12, h0 14, lock1 31, h1 38, lock2 41, h2 48, lock3 53, h3 60, end 84 |
| `rings` | 78 | glint 0, lock1 7, r1 14, lock2 17, r2 24, lock3 27, r3 34, lock4 37, r4 44, lock5 47, r5 54, end 78 |
| `ult` | 86 | yellow 0, star1 12, cut1 24, web 26, star2 34, cut2 46, settle 56, end 86 |
| `hcut` | 52 | yellow 2, sparkle 8, lock 19, go 24, cut 26, end 52 |
| `blue` | 46 | yellow 0, blue 4, lock 15, go 20, hit 22, end 46 |
| `kcut` | 50 | crouch 0, yellow 3, sparkle 9, glow 12, lock 15, go 20, cut 22, end 50 |
| `mx` | 60 | crouch 0, star 4, lock 9, go 14, x 16, lock2 21, dome 28, end 60 |
| `nb` | 66 | crouch 0, leap 2, apex 8, lock1 13, b1 20, lock2 23, b2 30, lock3 33, b3 40, land 46, end 66 |
| `q_grab` | 40 | glint 0, ghost 4, lock 13, go 16, grab 20, end 40 |
| `q_air` | 96 | throw 0, rise 2, apex 10, lock1 15, beam 22, lock2 31, dive 34, hit 38, land 40, leap 46, apex2 52, star 62, lock3 67, pillar 74, drop 78, land2 84, end 96 |
Motion notes: the sword is in her left hand; big swings keyed every tick (≤ 120°/t); no root motion in a clip. `ult`:
iai stance 0-22, the draw at 24, the blade held out through the web, the return cut at 46. `kcut`: low crouch, the blade
behind her, the body glow is the look `blade lilac`. `q_air` 0-10: both arms throw upward, she rises with the motion.

### 2.4 Gauntlets G1 (`a8`, 60 %) and G2 (`a13`, 5 %)
Common: she is a lilac ghost (`rlk_hr_ghost`, invulnerable), one ghost at a time, the field stays crimson (no `dark`
job, no bolts except the 4 decorative ones). Every cut = `api.cut(made, lock, strike, 'TC', 0, 1)`: a `pdisc(3.2)` that
follows the player until lock = strike − 7, parryable, with the **parry cue at the lock tick** (glint at her blade, or
at the reappear point while she is still travelling). The sword-qi shape shows at the strike as now. `g_dome`'s three
cuts in G2 are three plays of the clip. Rows `(t, step, clip, cut made / lock / strike)`:

| G1 `A8_SCRIPT` | | G2 `A13_SCRIPT` | |
|---|---|---|---|
| 0 `g_tell` | — | 0 `g_tell` | — |
| 16 D1 `g_dash` | c1 16 / 23 / 30 | 16 D1 `g_dash` | c1 16 / 23 / 30 |
| 27 `g_ring` | c2 30 / 39 / 46 | 27 `g_ring` | c2 30 / 37 / 44 |
| 37 `g_rise` | c3 46 / 57 / 64 | 35 `g_rise` | c3 44 / 51 / 58 |
| 55 `g_leap` (gone 71) | — | 49 `g_leap` (gone 65) | — |
| 80 D2 `g_glide` | c4 80 / 87 / 94 | 72 D1 `g_dash` | c4 72 / 79 / 86 |
| 91 `g_sweep` | c5 94 / 103 / 110 | 83 `g_ring` (gone 95) | — |
| 104 `g_x` (gone 118) | — | 100 D2 `g_glide` | c5 100 / 107 / 114 |
| 124 D1 `g_dash` | c6 124 / 131 / 138 | 111 `g_sweep` | c6 114 / 121 / 128 |
| 135 `g_ring` | — | 122 `g_x` (gone 136) | — |
| 148 D3 `g_drop` | c7 148 / 157 / 164 | 142 D4 `g_run` | c7 142 / 149 / 156 |
| 161 `g_wrap` | c8 164 / 173 / 180 | 153 `g_wrap` | c8 156 / 165 / 172 |
| 177 `g_dome` | c9 180 / 189 / 196 | 169 / 183 / 197 `g_dome` ×3 | c9 172 / 179 / 186, c10 186 / 193 / 200, c11 200 / 209 / 216 |
| 191 `g_vert` (pink glow 192-195, hidden 209) | — | 211 `g_vert` (hidden 229) | — |
| 214 `g_dive` (normal colours, 6 b up) | — | 236 `g_dive` | — |
| **220 judge** | | **242 judge** | |

Strike gaps: G1 16 / 18 / 30 / 16 / 28 / 26 / 16 / 16, then the dive 24 t later (video G1: 35 / 26 / 21 / 23 / 15, dive
42); G2 14 / 14 / 28 / 28 / 14 / 28 / 16 / 14 / 14 / 16, dive 26 (video G2: 9 / 27 / 10 / 15 / 27, a three-hit dome, dive
40). Every gap ≥ 14 t, so a missed F (12 t refusal) never blocks the next cut. `BOLTS`: G1 34 / 102 / 166 / 218, G2 70 /
160 / 205 / 240. `CUT_IDS` a8 `1`-`9`, a13 `1`-`11`.
- **Judge, gauge 0**: no hazard; in the same tick the core starts `seq/repel {at}` (`REPEL_T` = `JUDGE_T`; the repel's first
  frames are the gold deflect, §3.4). `g_deflect` is no longer played.
- **G1 fail** (unchanged, PLAN §5.5): `ult/fail60` 500 ‰ non-lethal + push, `g_reform` 220-230, P2 decision at 240.
- **G2 fail** (unchanged): the instant death staged at 236 / 239 / 242 (`FAIL5_T`), Ronova's revive → 60 t → `lead_re
  {g:a13}`. The warning banner from `lead5`'s refill beat to the judge, new wording (open question 3):
  `WARN_TEXT` = 「베기를 완벽하게 패링해 실드를 모두 깎으세요 — 실드가 남으면 즉사합니다」, `WARN_HL` unchanged.

### 2.5 Balance of the kit at a glance (for H1's sanity checks)
Parryable hits per pattern: `a1` 1, `a2` 1, `a3` 5, `a3s` 2, `d4` 4, `tri` 4, `a4` 2, `rings` 4-5, `mx` 1, `nb` 3, `q` 3.
Unparriable: `ult` 2, `a9`, `a10`, `hcut`, `blue`, `kcut`, `mx` X, `q` pillar. Heaviest strings if nothing is defended
(% of max HP of the item-less Lv15 player, T1 4.4 / T2 6.3 / T3 9.3 / T4 10.6): `a3` 23.9, `d4` 19.5, `tri` 19.5, `q` 31.2,
`nb` 21.9, `rings` + `ult` 35.1 (P1) — `q` and `rings` + `ult` are the two that decide §6.4's worst-window target.

---------------------------------------------------------------------------------------------------------------------

## 3. Cutscenes (H2 `seq.py` + `cam.py` + `scarlet_cine.mjs`; the actor is H3's)

### 3.0 Common rules
- **Lock** (the brief's facts): while a locked sequence runs the module sets `#mbCam mb 1` every tick and `#mbCamId mb`
  1 (camera A = `rlk_mb_cam1`) or 2 (B = `rlk_mb_cam2`); the framework spectates the live camera every tick (`hold`) and
  releases when the request stops. A hard cut = the other camera, already placed one tick earlier. A move = one `tp`
  per tick on the live camera. Camera points below are **eye points**; H2 measures the stand's eye offset once.
- **Stage** (`rlk_hr_stage`, made at a sequence's tick 0): origin = the avatar's feet on the floor (y `CY`); forward `f` =
  the bearing avatar → her, unless the point `ST(0, 0, FMAX)` fails `mv/ok`, then the bearing avatar → the arena centre
  (FMAX: CS1 10, repel 10, ending 12). The avatar entity stays at the origin, hidden, for the whole sequence; it is
  never teleported (CS0 is the one exception, §3.1). She is moved by the sequence (`mv/glide|leap`, every end point
  through `mv/ok`).
- **Actor**: `char/cine/spawn` at the stage (rotated as the stage), one clip per sequence (`cs0`, `cs1`, `repel`,
  `ending`, `coda`), the module copies `#sq hr` into `#cavT cine` and calls `char/cine/tick` each tick, so the actor runs on
  the sequence clock like every beat of hers (her `intro_end` restarts her clip at `#sq` 1290; the actor's `cs0` does not). The actor's root = the stage origin + the clip's `shift`, yaw = the stage yaw +
  the clip's root yaw. **Displacement limits** (every clip): forward ≤ 2.5 b, backward ≤ 1.5 b (CS0's walk-in alone: 6.0 b), sideways ≤ 1.5 b, up
  0 except the ending's aerial duel (≤ 7.0 b); `shift` is (0, 0, 0) with the feet on the floor at every hand-back tick.
- **Cut masks** (they hide the game-mode switch, the actor's spawn and her placement): CS0 the framework's 1-s arrival
  blindness; CS1 ovl `white` 0 / 2 / 2; repel ovl **`gold`** (new) 0 / 4 / 3 = the deflect's wash; ending ovl `white`
  0 / 2 / 1 (the existing `SEAM_CUT`).
- **HUD**: spectator hides the hotbar and hearts; the actionbar HUD is held (`hudHold 2` every tick) in every locked
  sequence; boss bars off in CS0, CS1, the ending and the coda, **on** in the repels (the video keeps them).
- **Lines**: `fx/hud/line {id}` at the listed tick, on screen for the listed span (≈ the video's spans; `api.LINE_AT`).
- **Clash contact**: each clash names a contact point K in the stage frame (§4.3). Her clip (H2) and the actor's clip
  (H3) both put their blade's centre line through K ± 0.08 b; effects at a clash are placed at K (stage coordinates),
  never at an actor anchor. Blade-lock convention seen from the actor: her blade runs lower-left → upper-right, the
  actor's lower-right → upper-left, both at 45°, hilts 0.3 b below K, hers 0.25 b beyond K, the actor's 0.25 b before it.
- **Hand-back** (every exit: the end, cancel, pause, `/reload`, relog, death / Ronova, cleanup, abort, uninstall):
  `#mbCam` stops → the framework's release (un-spectate, the player to the avatar's place, `rotate` toward her, the
  stored game mode back, the seat again), `char/cine/stop` (actor gone, avatar visible), cameras killed, `hudHold`
  runs out, ovl cleared. The actor's last pose = the avatar's idle (standing, facing her), so nothing pops.
- **Skip** (CS0 and CS1): actionbar 「⊙ 건너뛰기 · Shift 길게」 as now; sneak held 20 t inside the window → ovl `black`
  0 / 20 / 6, the jump under it. While sneak is down the game leaves the camera; the framework re-spectates each tick
  (a flicker inside the skip window is accepted, as the brief says).
- Her rig faces `@e[tag=rlk_body,limit=1]` (the RIGLIB target option) — sequences still set her yaw explicitly.
- **Facing**: unless a row says otherwise she faces the actor (yaw = the stage yaw + 180°) and the actor faces +f.
- **Lock spans and hand-backs**:

  | sequence | locked `#sq` | bars | state handed back |
  |---|---|---|---|
  | CS0 `intro` | 0-1440 (the stage is made and the avatar moved at 0) | off | control: she 6.5 b ahead in her stance, the avatar at `P0` facing her, bars on with the HP ramp |
  | CS1 `cs1` | 0-720 | off | the avatar where it stood, facing her 9.0 b ahead; `lead60` runs unlocked |
  | `lead60` / `lead5` / `lead_re`, G1 / G2 | — (never locked) | on | — |
  | `repel {at:60}` | 0-140 (starts in the judge tick) | on | she stands 9.0 b ahead, P2 after 20 t |
  | `repel {at:5}` → `ending` → coda | 0-129, then 0-1372, then E0-E118 without a break | on, then off | the reward path (the return under the coda's black) |

### 3.1 CS0 — intro (`seq/intro`, 1440 t; video 0-101.5 s = 2030 t)
**Length**: 1440 t = 72 s = 0.71 × the video. The arrival and establishing shots I1-I4 run at 0.43 × (our arena has no
stair approach and the first second is the arrival blindness); every dialogue shot runs at 0.8-0.9 × with each line on
screen ≥ 0.8 × its video span (typed subtitles, no voice, still read at the video's pace); the leap, landing, draw and
stance run at ≈ 1.0 ×. All 20 shots and 11 lines are kept in order. The skip (window `#sq` 20-1270) jumps to 1290 =
shot I18 = line 11, as the original's skip does: 7.5 s remain.
**Stage** (fixed): origin `P0` = `start` + 6.0 b along the bearing start → `SEAT_POS` (7.5°) = W(881.28, 201, 25.55).
At tick 0 the avatar is moved from `start` to `P0` (`tp` + `view/sync`, under the blindness) — the one avatar teleport.
The actor's clip starts 6.0 b behind (`shift` f −6.0 = `start`: the CS0 clip alone may go that far back) and walks in.
Her seat is at `ST(0, 0, 20.73)`; she, the seat and the moon are on the stage axis, so every camera on the axis behind
her target sees her against the moon. Boss invulnerable, bars off, no hazards.

| shot | `#sq` | camera (eye → look) | her (clip `intro`; position `f` on the stage axis) | actor (clip `cs0`) | line · effects · sounds |
|---|---|---|---|---|---|
| I1 arrival | 0-60 | A follow: `ST(0.6, 1.9, −9.0)` → `ST(0.6, 1.7, −4.5)` (linear 20-60), look `ST(0, 1.4, actor f + 3)` | seated on `seat_rock` at f 20.73, back to the actor, facing the moon; cup in the right hand, bottle on the rock, hat worn, sword sheathed | walks in f −6.0 → −3.0 (20-60, 0.075 b/t), the sword low in the right hand, point down | `arrive_rift` behind the actor 0; `cs0_wind`; `ambient_p1`; steps `block.grass.step` 0.25 / 12 t |
| I2 side track | 60-110 | B: `ST(−7.0, 1.2, −3.5)` → `ST(−7.0, 1.2, −0.5)` (60-100), look `ST(0, 1.2, same f)` | — | walks f −3.0 → 0.0 (60-100), stops, looks ahead (100-110) | steps; (the video's bamboo foreground has no counterpart) |
| I3 moon | 110-170 | A: `ST(−3.0, 1.5, 14.0)`, look pans W`MOON_POS` − (6, 0, 0) → `MOON_POS` | — | idle | one `petal_big` (whole) falls through the frame 150-170, 1.5 b before the lens; `block.cherry_leaves.fall` 0.3 at 150 |
| I4 petal on her hand | 170-250 | B: `HR(0.9, 0.75, 0.9)`, look `HR(0.25, 0.62, 0.35)` (the right hand on her knee) → tilt to the hilt `HR(0.3, 0.8, 0.1)` 220-236 → the brim `HR(0, 1.55, 0)` 236-250 | still; the petal lands on her hand 190 (follows `hand_r`), rolls off 206-216 | idle | — |
| I5 profile | 250-320 | A: `HR(1.1, 1.45, 0.25)` → drifts 0.1 b forward, look `HR(0, 1.6, 0.05)` | still, speaks | idle | **1** at 258 (54 t) |
| I6 bottle | 320-410 | B: `HR(−0.55, 0.5, −0.7)`, look `HR(−0.35, 1.05, 0.5)` (the bottle against the moon) | left hand takes the bottle 326 (rock `bare`), lifts 334-350, pours into the cup 352-384, lowers 388-404 | idle | **2** at 340 (60 t); `cs0_pour` 356 |
| I7 cup | 410-460 | A: `HR(0.9, 0.6, 0.5)`, look `HR(0.45, 0.28, 0)` (the rock top) | sets the bottle down 414-424 (rock `bottle`), turns the cup in her right hand 430-456 | idle | `block.decorated_pot.insert` 0.3 p 1.8 at 424 |
| I8 cup to the moon | 460-536 | B: `HR(0.75, 1.0, −0.9)`, look W`MOON_POS` | raises the cup toward the moon 470-500 (the cup crosses the disc), holds | idle | **3** at 462 (60 t); `moon_halo` `p1b` 474-530; `block.amethyst_block.chime` 0.3 p 1.2 at 486 |
| I9 over her shoulder | 536-666 | A: `HR(−1.6, 1.5, −2.2)` → `HR(−1.3, 1.45, −1.8)` (slow push), look `HR(0.2, 1.3, 0.6)` | arm out with the cup 536-590, brings it back 592-600, drinks 600-650 (head back), lowers 650-664 | idle | **4** at 540 (84 t); `entity.generic.drink` 0.35 p 1.3 at 612 |
| I10 the guest | 666-750 | B: `ST(0.45, 1.75, −0.9)`, look `ST(0, 1.5, 20.7)` (over the actor's right shoulder) | (far, tiny) sets the cup down 700-712 (rig `cup none`, rock `set`) | lifts the head toward her 670-690, a half step and stop 690-700 | **5** at 690 (130 t, two pages, runs to 820 over I11 and into I12 as in the video) |
| I11 hand on the sword | 750-790 | A: `HR(0.7, 0.85, 0.6)`, look `HR(0.3, 0.8, 0.1)` | both hands on the sheathed sword at her right hip (the scabbard stays `hip`): the right hand grips its throat 756, the left thumb pushes the guard and slides the blade a hand's width out and back: a white glint 764-786 | idle | `glint {c:5}` at `scabbard_mouth` 770; `item.armor.equip_chain` 0.3 p 1.4 at 758 |
| I12 against the moon | 790-910 | B: `ST(0, 0.25, 16.0)`, look `HR(0, 1.5, 0)` (low, 4.7 b before her: her silhouette inside the moon disc) | stands up on the rock 792-820, turns to the actor 840-880 (yaw by the sequence), hat brim low | idle | **6** at 838 (64 t) |
| I13 smile | 910-970 | A: `ST(0.25, 1.75, 19.3)`, look `HR(0, 1.7, 0)` | `face smile` 912, a small head tilt 930-950 | idle | **7** at 906 (44 t; starts on I12's tail as in the video) |
| I14 the field | 970-1040 | B: W(878, 204.5, 2), look W(858, 203, 14) (the west grove; neither figure in frame) | — | idle | **8** at 980 (44 t); `petals_drift`; `block.cherry_leaves.fall` 0.3 at 990 |
| I15 walk, hat tipped | 1040-1230 | A: `ST(0, 1.3, 9.5)`, look `HR(0, 1.4, 0)` | steps off the rock 1040-1052 (rock and props removed 1052), walks f 20.7 → 13.5 (1052-1148, 0.075 b/t, `walk`) with the right hand on the brim; stops 1148; tips the hat back 1160-1180 (face visible, smiling); the sword stays sheathed at the hip | idle | **9** at 1044 (90 t); **10** at 1140 (70 t); steps |
| I16 leap | 1230-1260 | B: `ST(0.8, 0.3, 8.5)`, look follows her (`facing entity`, eyes) | crouch 1230, `mv/leap` f 13.5 → 6.5 (1234-1258, apex 4.5 b) | head follows her up 1236-1250, a guarded half step back (shift f −0.3) 1250-1258 | `entity.breeze.jump` 0.5 at 1234; `afterimage` 1236 / 1244 |
| I17 landing | 1260-1290 | A: `ST(1.6, 0.5, 4.2)`, look `HR(0, 0.9, 0)` | lands crouched under the hat 1258, one hand on the ground, holds, rises a little 1276-1290 | raises the sword into a middle guard 1262-1284 | `entity.generic.big_fall` 0.4 + `dust_ring {r:12}` at 1258 |
| I18 under the brim | 1290-1350 (`intro_end` 0-60) | B: `HR(0.15, 1.35, 1.0)`, look `HR(0, 1.62, 0)` | speaks; lifts the brim 1330-1346 (eyes) | guard, still | **11** at 1294 (62 t). **Skip target** |
| I19 draw, stance | 1350-1406 | A: `HR(0.4, 1.4, 1.6)` → `HR(0.6, 1.3, 3.2)` (pull back 1350-1400), look `HR(0, 1.3, 0)` | smile 1350; **draws** 1356 (left hand, cross-draw; the blade upright before her 1358-1378); swings into the stance 1380-1400 (sword out low to her left, the hat dipping); the right hand steadies the scabbard at the hip through the draw | steps back to shift 0 by 1400, guard | title 「홍련」 / 「월하곡」 at 1356; `glint {c:5}` at `blade_tip` + `qi_arc {r:18,c:1}` 1356; `item.trident.return` 0.6 p 0.9 at 1352, `entity.player.attack.sweep` 0.6 p 1.4 at 1356 |
| I20 back to the player | 1406-1440 | B: `ST(0.6, 1.8, 3.0)` → `ST(0, 2.6, −3.4)` (arc over the actor 1406-1436 = the F5 camera's place), look `ST(0, 1.5, 6.5)` | stance (`idle`) at f 6.5, facing the actor | ready stance → idle pose 1430-1440 | music 1 at 1420; bars on + the HP ramp at 1440 (control) |
Distances: 26.7 b (I1, from `start`) → 20.7 (I2-I14, from `P0`) → 13.5 (end of I15) → **6.5 b** at control (as today's 6.5-6.8).
Skip: clear lines / wind / props / rock; she → f 6.5 crouched (I17's last pose), `#sq` 1289; the actor clip shows its
tick 1290 (guard) by itself. Reload → `#sq` 1440's end state.

### 3.2 CS1 — the 60 % cutscene (`seq/cs1`, 720 t; video 160.5-203.0 = 850 t, 0.85 ×)
Core: `rlk_mb_inv` from 0 to the end of the repel (or the G1 fail), `cine/start` 0-720, hazards cancelled at 0, bars off,
`#mbFloor` → 5 %. Stage per §3.0 (FMAX 10). At tick 0 under the white mask she is placed at `ST(0, 0, 9.0)` facing the
actor (`mv/ok`; the 3-tick client glide of her move reads as her landing in the wide shot). No damage to the player.
Skip window 40-560 → jumps to `#sq` 566 (the wipe's end, line 15 next), as the original's skip keeps the slash.

| shot | `#sq` | camera | her (clip `cs1`) | actor (clip `cs1`) | line · effects · sounds |
|---|---|---|---|---|---|
| S1 apart | 0-6 | A: `ST(−9.0, 2.2, 4.5)`, look `ST(0, 1.2, 4.5)` | low ready stance at f 9.0, 180° (facing the actor) | ready stance at 0 | ovl `white` 0 / 2 / 2 |
| S2 clash | 6-34 | B: `ST(−2.6, 1.3, 0.8)` → `ST(−1.3, 1.4, 0.8)` (10-22), look K1 = `ST(0, 1.45, 0.75)` | lunges f 9.0 → 1.5 (6-10, `mv/glide {t:4}`), cut stopped at K1 at **10**, lock 10-30 (both hands, leaning in), pushes 24-30 | guard up 6-10, takes the cut on the blade at 10 (two hands), knees bend 10-14, pushes back 24-30 | ovl `gold` 0 / 1 / 2 + `clash_gold` at K1 at 10; `clash_arc` 14-22; `clash_spark` at K1 every 3 t 12-30; `afterimage` 6-10; `entity.phantom.swoop` 0.5 p 1.6 at 6; `block.anvil.land` 0.35 p 1.7 + `item.trident.hit` 0.5 at 10; `entity.lightning_bolt.impact` 0.15 p 2.0 at 14, 18 |
| S3 pushed apart | 34-84 | A: `ST(−13.0, 3.0, 4.0)`, look `ST(0, 1.0, 4.0)` (static wide) | shoved off at 30-34, leaps back f 1.5 → 9.0 (34-50, `mv/leap {t:16,h:12}`), lands low, blade low to her left | slides back shift f 0 → −1.2 (34-44, feet dragging), recovers and steps forward to 0 (60-80) | push sound `entity.player.attack.knockback` 0.6 at 32; `block.grass.step` 0.6 at 50 |
| S4 over the shoulder | 84-180 | B: `ST(0.55, 1.75, −1.3)`, look `ST(0, 1.4, 9.0)` | straightens 90-110, hat on, sword low; a small nod 120-140 | stands, back to the lens, sword lowered | **13** at 110 (52 t) |
| S5 the grass | 180-220 | A: `ST(0, 5.0, 4.5)` looking straight down, screen-up = stage forward (both figures outside the frame) | off screen: sheathes (`sword sheathed` 200), takes the bottle (`bottle hand` 216) | idle | `petals_wind` 180-220; `leaves_dark {n:8}` 186 |
| S6 hat swing | 220-276 | B: `HR(0.5, 1.6, −1.6)`, look `ST(0, 1.2, 0)` (behind her; the actor tiny beyond) | right hand takes the brim 236, sweeps the hat off and round in an arc that fills the frame 240-252, sets it back on 256-262 | stands | **14** at 232 (40 t); `item.armor.equip_leather` 0.5 at 240, 260 |
| S7 the bottle | 276-340 | A: `HR(0.2, 1.45, 1.9)`, look `HR(0, 1.45, 0)` | `face smile` 280; raises the white bottle in her left hand to shoulder height 300-330 | — | — |
| S8 the actor | 340-380 | B: `ST(0.5, 1.5, 1.8)`, look `ST(0, 1.45, 0)` | — | watches her; the sword hand tightens, the blade comes up to a half guard 350-370 | — |
| S9 offer, drink | 380-500 | A: `HR(−0.3, 1.5, 1.5)`, look `HR(0, 1.5, 0)` | eyes-closed smile (`face closed` 384-400), offers the bottle toward the actor, arm out 404-430, looks down 434-452, drinks from the bottle, head back 458-492 | — | `entity.generic.drink` 0.35 p 1.2 at 464, 478 |
| S10 under the brim | 500-610 | B: `HR(0.1, 1.38, 0.95)`, look `HR(0, 1.6, 0)` | bottle gone (`props/none` 500); wipes her mouth with the right forearm 506-566, lowers the arm 568-580; head lowered under the brim | — | **15** at 578 (36 t); `petal_big` (whole) drifts across her face from frame-left 590-606, 0.6 b before it; `block.cherry_leaves.fall` 0.4 at 590 |
| S11 the petal | 610-642 | A: `ST(0.3, 1.5, 2.0)`, look `ST(0.3, 1.5, 2.9)` (a second `petal_big` held there, turning slowly) | off screen: iai stance, left hand on the hilt 610 | idle, half guard | **16** at 618 (36 t, through the slash); the petal's glowing line faint 620, clear 624 (look `cut`); `block.amethyst_block.chime` 0.6 p 2.0 at 624 |
| S12 flashes | 642-648 | (A held) | the draw at 642 | — | ovl `negative` 0 / 3 / 0 at 642 (video 3 t); ovl `pinkwhite` 0 / 3 / 4 at 645 (video 2.5 t); `entity.player.attack.sweep` 1.0 p 0.5 + `item.trident.riptide_3` 0.6 p 1.6 at 642 |
| S13 홍련일섬 | 648-720 | B: `ST(0.4, 2.1, −4.2)`, look `ST(0, 1.2, 4.0)` (wide behind the actor) | post-slash pose at f 9.0: blade swept out low to her left, body twisted; holds; straightens 700-720 | **hit**: the chest snaps back 652, staggers (shift f −0.5) 652-664, drops to one knee with the sword planted 664-694, pushes up 694-716, ready at shift 0 by 718 | petal halves blow off (`split`) 649-664; `scarlet_line {len:600,roll:13}` across the view through `ST(0, 1.3, 0)` at 650; `petal_burst {r:20}` at her 650; ovl `red_tint` 0 / 4 / 20 at 650; arena look `crimson` requested 660; rig `phase p2` 660; `leaves_dark {n:40}` 656-720; `item.trident.thunder` 0.5 p 1.4 + `block.glass.break` 0.5 p 0.6 at 650; music 2 at 676 |
Distances: 9.0 (S1) → 1.5 (lock, K1 0.75 from each) → 10.2 (S3, she 9.0, the actor −1.2) → 9.0 from 80 to the end.
720: release, `seq/lead60` next tick. Reload / resume → the end state (crimson, `phase p2`, music 2, she at f 9.0).

### 3.3 Lead-ins (in the fight: not locked, the player moves; she is invulnerable; `#mbBalOff 1`)
| sequence | len | beats (`#sq`) |
|---|---|---|
| `lead60` (after CS1; replaces `sq1`) | 56 | 0: bars on, `refill` signal (gauge 5/5, `shield_refill`, `block.respawn_anchor.charge` 0.4 p 1.6); 0-20 she straightens from the slash pose, 9 b away; 20-40 stands, blade low; 40 the right hand rises to the brim (`g_brim` hold); 56 = T0 of G1 (video: 2.8 s of stand-off, then the lilac flash) |
| `lead5` (the 5 % floor reached in P2) | 116 | 0-8 a staggering step back; 8-60 she backs off facing the player to 10 b (`backstep` motion, 0.12 b/t, `mv/ok`); 60 `refill` signal + the warning banner on (G2's fail is lethal); 84-98 a lilac glow along the blade; 100 hand to the brim; 116 = T0 of G2 (video: 272.0 backs off, 275.0 refill, 277.8 flash) |
| `lead_re {g}` (restart after a pause / revive) | 60 | 0 she stands 8 b from the player; 10 `refill` (+ the banner for a lethal gauntlet); 44 brim; 60 = T0 |

### 3.4 The repel counter (`seq/repel {at:60|5}`, 140 t; video 215.6-222.6 = 140 t, 1.0 ×; the same for both)
Starts in the judge tick of a gauntlet with the gauge at 0. `cine/start` for its length, she stays `rlk_mb_inv`, bars
**on**, locked. Stage per §3.0 (FMAX 10); at tick 0 she is 1 b above `ST(0, 0, 1.0)` (the dive's end, normal colours).
HP steps through `#sq_sig` as now, at the events `strike` 49, `land` 101, `kick` 129: 15 / 15 / 15 ‰ at 60 %; 15 / 15 / the
kill at 5 % (the sequence stops at 129 there: `death_start` → the ending's tick 0 at the next tick, the lock unbroken).

| beat | `#sq` | camera | her (clip `repel`) | actor (clip `repel`) | effects · sounds |
|---|---|---|---|---|---|
| R0 deflect | 0-4 | A: `ST(−1.2, 0.9, 0.65)`, look KR = `ST(0, 1.55, 0.65)` | drops onto the actor's raised blade, lands at f 1.3 by 6, 180° | high guard, the blade over the head at KR, knees bent | ovl `gold` 0 / 4 / 3; `clash_gold` + `light_column` at KR; `block.anvil.land` 0.6 p 1.4 + `entity.player.attack.crit` 0.8 at 0 |
| R1 blade lock | 4-26 | A → `ST(−1.0, 1.0, 0.65)` (slow push) | presses down, leaning in, hilt above KR | holds, then heaves up 22-26 | `clash_spark` at KR every 3 t; `item.trident.hit` 0.4 at 8, 16 |
| R2 grab | 26-48 | B: `ST(1.9, 1.5, −0.4)`, look `ST(0, 1.3, 0.8)` | her blade is thrown wide 26-30; her sword wrist is seized 36 and yanked up; she rises on her toes, turned side-on, f 1.1 | throws her blade aside 26-30, steps in (shift f +0.5) 30-36, the left hand seizes her wrist 36, holds 36-48 | `item.armor.equip_chain` 0.4 p 0.8 at 36 |
| R3 hat strike | 48-52 | B held | reels from the blow on her hat | the hilt comes down on her hat crown at **49** | `clash_gold` at her `hat_crown` at 49; **hp1**; `entity.player.attack.crit` 0.7 + `block.anvil.place` 0.3 p 1.6 |
| R4 two cuts | 52-68 | A: `ST(−2.2, 1.2, 2.4)`, look `ST(0, 1.2, 0.8)` | staggers under the cuts to f 1.2, still facing the stage origin | rising cut 56, level cut 62 that carries the actor past her right side (shift f 0.5 → 1.8, 62-68) | `qi_arc {r:22,c:5}` at 56, 62 (white: the player's cuts are never lilac); `entity.player.attack.sweep` 0.7 p 1.2 / 1.4 |
| R5 back to back | 68-78 | B: `ST(0, 1.6, 3.6)`, look `ST(0, 1.3, 1.4)` | pressed against the actor's back at f 1.2, tipped backward over its shoulder | at shift f 1.8, back to her, reaches over the right shoulder and hooks her sword arm 70-76 | `block.grass.step` 0.4 at 68 |
| R6 the throw | 78-102 | A: `ST(−2.8, 0.7, 1.8)`, look `ST(0, 1.2, 2.0)` | (HF-B) levered onto the actor's back and rolled over its right shoulder, head first, low: her pelvis 0.34 b over that shoulder at 88 (root arc 0.6 b), the hat comes off 84 (`hat world`), slams onto her back at f 3.0 at **101** | its right fist hooked over her sword forearm 78-96, the left hand round her wrist 86-91; the hips back under her, bowed, the head ducked to the left of her body; lets go 96, straightens 96-102 | `entity.player.attack.knockback` 0.6 at 78; `dust_ring {r:15}` + `entity.generic.big_fall` 0.6 + `block.grass.break` 0.5 at 101; **hp2** |
| R7 over her | 102-128 | B: `ST(1.6, 1.2, 4.6)`, look `ST(0, 0.6, 2.6)` | lies on her back, one hand lifts weakly 112-124 | stands over her at shift f 1.8, the blade pointed down 104-118, draws the leg back 120-128 | `at:5`: `petal_burst {r:10}` 110 |
| R8 the kick | 128-132 | A: `ST(−2.4, 0.8, 2.6)`, look `ST(0, 0.5, 2.8)` | kicked at **129**: slides away (60 %: f 3.0 → 8.0 by 135; 5 %: → 4.2 by 133, inside the ending) | the kick lands at 129 | `kick_flash` at her (kept cards); **hp3** / the kill; `entity.player.attack.strong` 0.8 + `block.anvil.land` 0.4 p 1.2 |
| R9 apart (60 % only) | 132-140 | B: `ST(−5.0, 2.4, −2.0)`, look `ST(0, 1.0, 4.0)` | rolls to her feet 133-140, snatches the hat (`hat worn` 139), stands in her stance at f 9.0 | back-flips to shift 0 (132-139), lands ready | `block.grass.step` 0.5 at 139 |
60 % hand-back at 140: release; `bal` + 3; P2's first decision after a 20-t recovery (no down window: v 222.6 "she is
up"). Distances: 1.3 (lock) → 0.6 (grab) → back to back 0.6 → she lies 1.2 b before the actor → 9.0 at the hand-back.

### 3.5 The ending (`seq/ending`, H = 1372 t; video 296.5-373.1 = 1532 t, 0.90 ×) and the coda
Trigger: the repel's lethal kick → `death_start` (`#mbSt 2`, bars off, `ev/roll`) → `seq/ending`. The lock, the cameras,
the stage and the actor continue from the repel (the actor is not respawned: `char/cine/play {clip:"ending"}`, whose
tick 0 is the repel clip's tick 129 pose at shift f 1.8). When the ending starts without a repel before it (`boss/test/kill`,
a reload inside the 5 % repel) it makes the stage itself (FMAX 12), puts her on her back at `ST(0, 0, 4.2)` and spawns the
actor under its white mask. From E8 on the stage is **ST2**: same origin, forward = the
bearing to her landing mark (9.0 b from the origin toward `MOON_POS` when that passes `mv/ok`, else along ST); the
actor is turned to it by `char/cine/face` during E8.

| shot | `#sq` | camera | her (clip `ending`) | actor (clip `ending`) | line · effects · sounds |
|---|---|---|---|---|---|
| E1 she rises | 0-50 | A: `ST(−3.2, 1.3, 2.6)`, look `ST(0, 1.1, 3.0)` | lies at f 4.2; kips up 6-22 taking the hat (`hat worn` 20); stands at f 4.6; raises the sword 28-42 (`blade violet` 30-48) | steps back to shift f 0.8 (4-16), ready stance | ovl `white` 0 / 2 / 1; `block.respawn_anchor.charge` 0.4 p 1.8 at 30 |
| E2 clash | 50-94 | B: `ST(1.3, 1.5, 2.2)`, look KE2 = `ST(0, 1.5, 2.1)` | lunges to f 2.9 (50-54); her hat is grazed 52; lock at KE2 56-80; shoved back to f 6.0 (80-86) | lunges to shift f 1.3 (50-54), the cut clips her brim 52; lock 56-80; shoved back to −0.6 (80-90) | gold spark (`clash_spark`) at `hat_crown` 52; `clash_spark` at KE2 / 3 t; `clash_gold` + `clash_arc` ×3 + ovl `gold` 0 / 1 / 2 at 70; `block.anvil.land` 0.4 p 1.5 at 56; `entity.lightning_bolt.impact` 0.2 p 1.9 at 70 |
| E3 the actor | 94-150 | A: `ST(1.2, 0.35, 1.2)`, look `ST(0, 1.0, −0.4)`; cut at 118 → B: `ST(−1.8, 0.5, 3.6)`, look `ST(0, 1.1, 1.0)` | off screen: springs back out of reach to f 11 (116-136) | skids back to shift −1.5 (94-104), crouches 104-116, dash-cut forward to +1.0 (118-124) that finds only air, holds the follow-through | `afterimage` + `qi_arc {r:26,c:5}` at 121; `entity.player.attack.sweep` 0.7 p 1.3 at 120; `block.grass.step` at 96, 100 |
| E4 the run | 150-190 | A: `ST(−14.0, 2.2, 5.5)`, look `ST(0, 1.0, 5.5)` | runs in f 11 → 4.0 (150-188, 0.18 b/t), sword back | runs shift f 1.0 → 2.5 (150-188), sword low | steps / 4 t |
| E5 gold flash | 190-204 | B: `ST(1.4, 1.5, 3.3)`, look KE5 = `ST(0, 1.5, 3.25)` | cut meets cut at 190, lock | the same | ovl `gold` 0 / 6 / 6; `clash_gold` at KE5; `block.anvil.place` 0.3 p 1.7 + `entity.player.attack.strong` 0.5 |
| E6 aerial duel | 204-314 | 204 A: `ST(−3.5, 3.0, 2.8)`, look `ST(0, 6.3, 2.8)`; 240 B: `ST(2.6, 6.8, 5.6)`, look `ST(0, 6.4, 2.6)`; 276 A: `ST(−1.6, 6.2, 0.2)`, look `ST(0, 6.5, 2.8)` | both spring up 204-216: she hangs at `ST(0, 6.0, 3.6)` (± 0.8), cuts at **228** (passing), **262** (overhead), **286** (the big one), lock **298**-304, pushed off 304 | rises to shift (0, 6.0, 1.5) (204-216), meets each cut at KA1-KA4 (§4.3), pushed off 304 | `clash_gold` at each K; ovl `gold` 0 / 3 / 6 at 286; `entity.player.attack.sweep` 0.6 at 228 / 262 / 286; `block.anvil.land` 0.5 p 1.3 at 262; `item.trident.thunder` 0.3 p 1.8 at 286 |
| E7 apart | 314-338 | B: `ST(−16.0, 3.0, 2.0)`, look follows her (`facing entity`) | flies back in an arc to her landing mark (`mv/leap {t:20,h:40}`, lands 334, crouched) | falls back to shift (0, 0, 0), lands 330, rises | `petals_wind` 316-338; `entity.generic.big_fall` 0.4 at 330, 334 |
| E8 the field | 338-378 | A: W(880, 206, 30), look W`MOON_POS` | rises, turns to the actor | turned to ST2 (338-350), lowers the sword | — |
| E9 sheathe | 378-470 | B: `ST2(0.8, 1.2, 4.6)`, look `HR(0, 1.3, 0)` (the red moon behind her) | f 9.0; scabbard in the right hand 388; swings it down across her body 398-418; sheathes 426-452 (`sword sheathed` 452) | stands, sword low | **17** at 420 (58 t); `petal_big` crosses 430-438; `block.iron_trapdoor.close` 0.25 p 1.8 at 452; music 3 at 420 |
| E10 her face | 470-556 | A: `HR(0.2, 1.5, 1.3)`, look `HR(0, 1.6, 0)` | `face smile`, head a little tilted | — | **18** at 486 (66 t) |
| E11 the actor | 556-616 | B: `ST2(0.4, 1.5, 1.7)`, look `ST2(0, 1.45, 0)` | — | lifts the left hand half way 566-584, lowers it 590-606 | — |
| E12 turning away | 616-846 | A: `HR(0.5, 1.4, 2.4)`, look `HR(0, 1.35, 0)`; cut at 700 → B: `ST2(−0.8, 1.5, 7.2)`, look `HR(0, 1.4, 0)` | lowers her head 640; turns away, the hat swinging 650-700 (yaw by the sequence, toward the moon); her back 700-760; looks over her left shoulder 760-800; one open hand chest-high 800-820; smiles 820-846 | — | **19** at 628 (42 t); **20** at 716 (118 t) |
| E13 the actor | 846-882 | A: `ST2(−0.4, 1.5, 1.6)`, look `ST2(0, 1.45, 0)` | — | listens, a small nod 860 | — |
| E14 the two | 882-972 | B: `ST2(−2.2, 1.6, −2.6)`, look `ST2(1.2, 1.2, 9.0)` | stands, half turned | left foreground, back to the lens | **21** at 910 (128 t, runs over E15) |
| E15 the moon | 972-1072 | A: `ST2(0.5, 1.6, 8.0)`, look W`MOON_POS` (behind her right shoulder) | faces the moon, looks up (head +15°) 990-1060 | — | `moon_halo` `p2b` 980-1060; `petals_heart` 1020-1050 |
| E16 the greeting | 1072-1212 | B: `ST2(0.6, 1.3, 2.0)`, look `HR(0, 1.3, 0)` | pivots to the actor 1072-1094; walks in f 9.0 → 4.5 (1094-1154, 0.075 b/t); the open-hand "let me see" gesture 1160-1196 | stands | **22** at 1082 (128 t, two pages) |
| E17 the hat tip | 1212-1372 | A: `HR(0.15, 1.5, 1.15)`, look `HR(0, 1.6, 0)` | left hand to the brim 1216-1232; `face closed` 1240; pulls the brim down with a 10° bow 1290-1330 (the hat fills the frame); holds; the face rises under the held brim, eyes open (`face calm` 1360) = `H_POSE` | stands | **23** at 1230 (88 t); `petals_heart` 1300-1330 |
H = 1372: `#sqdone`, the core starts `seq/event` (PLAN §7.3.2, 120 t, unchanged: she is 4.5 b away in `H_POSE`). Under
the same lock: camera B static at `ST2(0.55, 1.75, −1.3)`, look `HR(0, 1.3, 0)`; actor clip `coda` (idle; the thrown
sword / the moonlight still arrive at the avatar's place = the actor's). Release at E118, under the coda's black.
Distances: 3.8 (E1) → 1.6 (E2 lock) → 6.6 → 1.5 (E5) → 2.1 in the air → 9.0 (E7-E15) → **4.5** (E16 to the end).

### 3.6 Pause, reload, limits
| running | pause → resume | `/reload` |
|---|---|---|
| CS0 | release at once; resume: the end state (she at f 6.5, sword drawn, props gone, title shown, bars on) | the same end state |
| CS1 | release; resume: its end state → `lead60` from 0 | the same |
| lead-ins | freeze → restart from 0 | restart from 0 |
| G1 / G2 | as PLAN §5.6 with `lead_re {g}` | as pause |
| repel | release; resume: 60 % → its end (the three HP steps applied, `bal` + 3, P2); 5 % → the kill → the ending | the same |
| ending / coda | release; the framework finishes the death, the reward hook applies the event (PLAN §7.3.4) | the same |
A locked sequence never resumes in the middle: the camera, the actor and her clip would have to be rebuilt at an
arbitrary tick. Registry: `intro` 1450 (CS0 1440 + 10), `death` 1494 (1372 + 120 + 2).

---------------------------------------------------------------------------------------------------------------------

## 4. Clip lists

### 4.1 Her cinematic clips (H2, `scarlet_cine.mjs`; 8 clips; events are contract, `api.CLIPS_PLAN`)
| clip | len (was) | events |
|---|---|---|
| `intro` | 1290 (554) | l1 258, take_bottle 326, pour 352, l2 340, bottle_down 414, l3 462, raise 470, l4 540, drink 600, l5 690, cup_down 700, grip 756, glint 764, stand 792, l6 838, turn 840, l7 906, smile 912, l8 980, off_rock 1040, l9 1044, walk 1052, l10 1140, stop 1148, tip 1160, crouch 1230, leap 1234, land 1258, end 1290 |
| `intro_end` | 150 (86) | l11 4, brim 40, smile 60, draw 66, stance 90, music 130, end 150 (`#sq` − 1290; tick 0 = the skip's target pose: crouched from the landing, hat low) |
| `cs1` | 720 (213) | lunge 6, lock 10, push 30, leap 34, land 50, l13 110, sheathe 200, bottle 216, l14 232, hat_off 240, hat_on 258, smile 280, raise 300, offer 404, drink 458, props_off 500, wipe 506, l15 578, iai 610, l16 618, draw 642, slash 650, recolour 660, music 676, end 720 |
| `lead60` | 56 (new; replaces `sq1`) | rise 0, stand 20, brim 40, end 56 |
| `lead5` | 116 (new; replaces `lead_stand`) | stagger 0, back 8, refill 60, glow 84, brim 100, end 116 |
| `lead_re` | 60 (new) | refill 10, brim 44, end 60 |
| `repel` | 140 (104) | lock 0, heave 22, wide 26, grab 36, strike 49, cut1 56, cut2 62, hook 70, throw 78, hat_off 84, over 88, land 101, lie 104, kick 129, roll 133, hat_on 139, end 140 |
| `ending` | 1372 (1042) | up 6, hat_on 20, raise 28, lunge 50, graze 52, lock 56, burst 70, shove 80, back 116, run 150, clash 190, rise 204, a1 228, a2 262, a3 286, a4 298, off 304, fly 314, land 334, scab_up 388, swing 398, l17 420, music 420, sheathe 426, sheathed 452, l18 486, l19 628, head_down 640, turn 650, l20 716, look_back 760, hand 800, l21 910, gaze 990, pivot 1072, l22 1082, walk 1094, stop 1154, gesture 1160, brim 1216, l23 1230, eyes 1240, pull 1290, open 1360, end 1372 |
Removed: `sq1`, `lead_down`, `lead_stand`. Hand-over poses: `intro` 1290 = `intro_end` 0; `intro_end` 150 = `idle`; `cs1`
720 = `lead60` 0 (the post-slash pose); the three lead-ins end in `g_brim`'s hold (`g_tell` starts from it); `repel` 0 =
`g_dive`'s last pose (head down, blade down, 1 b up; no longer `LOCK`); `repel` 129 = `ending` 0 (on her back, hat
beside her); `repel` 140 = `idle2`; `ending` 1372 = `H_POSE`. Props and states keyed in the clips as today: `cup` /
`bottle` (hand / rock / none), hat (worn / world / hand), sword (hand / sheathed), `face`. The scabbard stays `hip` in
every clip but `ending` (388-452, `hand`). Quiet beats may key every 2-4 t; the draw, the throw, the kip-up, the hat
swing and every cut are keyed every tick.

### 4.2 Actor clips (H3, `tools/player_motion/cine/<id>.json`; 11 parts; the frame is the stage, `shift` = displacement from the stage origin)
| id | len | grip | displacement (`shift` f unless noted) | beats |
|---|---|---|---|---|
| `cs0` | 1440 | right hand, the point down until 1262 | −6.0 → 0 (20-100); −0.3 (1250-1390); 0 from 1400 | 0-20 stands at −6.0 (under the blindness); walk cycle 20-100 (24-t cycle, 0.075 b/t, feet planted: no sliding); 100-110 stops, looks ahead; idle (breathing, key every 40 t) to 666; head up toward her 670-690, weight forward 690-700; idle to 1230; head follows her leap 1236-1250, half step back 1250-1258; raises the sword into a middle guard 1262-1284; steps forward to 0 (1390-1400); guard to 1430; lowers into the avatar's idle 1430-1440 |
| `cs1` | 720 | right hand; **two hands 6-34** | 0; −1.2 (34-44) → 0 (60-80); −0.5 (652-664) → 0 (694-716) | ready 0-6; guard up 6-10; takes the cut at K1 at 10 (elbows give 10-14); lock 10-30, pushes 24-30; shoved back, sliding 34-44; recovers, steps forward 60-80; sword lowered 84-340; half guard 350-370, held; **hit** at 652 (chest back, sword arm flung), stagger 652-664, down on the right knee with the sword planted point-down 664-694 (head lowered), pushes up 694-716, ready 716-720 |
| `repel` | 140 | **two hands 0-30**; left hand free 30-100 | 0 → +0.5 (30-36) → +1.8 (62-68), held; back-flip to 0 (132-139) | high guard at KR 0-4, knees bent; holds 4-22, heaves up 22-26; beats her blade aside 26-30; steps in, left hand to her wrist 36, holds it high 36-48; hilt strike down on her hat 49; rising cut 56, level cut 62 carrying past her right side; back to her 68, right arm reaches back over the right shoulder 70-76; the throw 78-96 (HF-B: the right fist on her sword forearm 78-96, the left hand round her wrist 86-91, the hips back under her, bowed, the head ducked left of her; she goes over the right shoulder), straightens 96-102; looks down at her, the blade pointed at her 104-118; right leg back 120-128, kick 129; back-flip 132-139, lands ready 140. `{at:5}` shows ticks 0-129 only |
| `ending` | 1372 | right hand; two hands at 56-80, 190-204, 262, 298-304; left hand free 556-616 | starts +1.8; +0.8 (4-16); +1.3 (50-54); −0.6 (80-90); −1.5 (94-104); +1.0 (118-124); +2.5 (150-188); up (0, 6.0, 1.5) 204-216 … 304; (0, 0, 0) at 330 and to the end | ready; lunge and the brim graze 50-52; lock at KE2 56-80; shoved back 80-90; skid 94-104; crouch 104-116; dash-cut 118-124, follow-through; run 150-188; clash at KE5 190, lock to 204; springs up 204-216; cuts met at KA1 228, KA2 262 (horizontal guard overhead), KA3 286, lock KA4 298-304; pushed off, falls 304-330, lands in a crouch, rises; turned to ST2 338-350 (by `face`), sword lowered 380-400; left hand half raised 566-584, lowered 590-606; a nod 860; stands to 1372 |
| `coda` | 120 | right hand, sword low | 0 | idle; the right forearm lifts a little 44-56 (the gift arrives), back by 70 |
Rules for H3: scale 1.0 and the same skeleton for all 7 characters (the 3 rig characters reuse their part models, the
other 4 get part models on `rlk:skin/<id>`); one weapon model `cine_sword` for all; the feet never under the floor; no
part turns more than 120° in a tick; the walk and run cycles plant their feet; at ticks marked two hands the left hand
is on the pommel. The clip's root yaw is 0 (facing +f) at every hand-back tick and through `cs0`, `cs1` and `repel` (in
the repel the actor passes her and keeps facing +f, so from 68 she is at its back); only the turns inside a move (the
back-flip, the aerial duel) leave it.

### 4.3 Contacts (stage frame; her clip and the actor clip both meet these; tolerance 0.08 b for blades, 0.12 b for hands and feet)
| id | sequence · ticks | point | what meets |
|---|---|---|---|
| K1 | `cs1` 10-30 | `ST(0, 1.45, 0.95)` | blade lock (the X convention of §3.0); she stands at f 2.25 (round W: a swordfighter's distance) |
| KR | `repel` 0-26 | `ST(0, 1.55, 0.65)` | her blade pressing down on the actor's high guard: her hilt at KR + (−0.25, +0.35, +0.30), the actor's at KR + (+0.35, −0.20, −0.20) |
| KW | `repel` 36-48 | `ST(0.15, 1.95, 0.85)` | the actor's left hand on her sword wrist (her anchor `hand_l` is there) |
| KH | `repel` 49 | `ST(0, 2.20, 1.10)` | the actor's hilt on her hat crown (her anchor `hat_crown` is there) |
| KS | `repel` 70-78 | `ST(0.20, 1.50, 1.60)` | her sword forearm over the actor's right shoulder |
| KT | `repel` 88 / 101 | `ST(0.28, 1.4, 2.0)` / `ST(0, 0.25, 3.0)` | her pelvis over the actor's right shoulder (HF-B: 0.3-0.6 b over it, the actor's hands on her sword forearm) / on the ground (head toward +f) |
| KK | `repel` 129 | `ST(0, 0.35, 2.7)` | the actor's right foot on her flank |
| KG | `ending` 52 | `ST(0, 2.05, 2.95)` | the actor's blade tip on the near edge of her brim |
| KE2 | `ending` 56-80 | `ST(0, 1.5, 2.2)` | blade lock (X) |
| KE5 | `ending` 190-204 | `ST(0, 1.5, 3.45)` | blade lock (X) |
| KA1 | `ending` 228 | `ST(0, 1.45, 3.5)` | round W, on the ground: her diagonal cut on the actor's block |
| KA2 | `ending` 262 | `ST(0, 1.85, 3.05)` | her overhead cut on the actor's raised horizontal guard (she has stepped in to f 4.35) |
| KA3 | `ending` 286 | `ST(0, 1.25, 3.55)` | cut on cut (the big flash) |
| KA4 | `ending` 298-304 | `ST(0, 1.5, 3.45)` | blade lock (X), then both push off |

Round W (lane WC, `w_brief.md` §4.5 / §4.6): every lock / clash keeps a swordfighter's distance — her root 1.3 b beyond the
contact, the actor's hilt 0.55 b before it (`tools/player_motion/cine/clips.mjs` LOCK_OFF): the torso axes >= 1.5 b apart
(test_contact `gap`; the 11-12 locks were 0.9-1.2 b, chest to chest). The aerial duel (E6 204-314) is gone: the exchange
KA1-KA4 is on the ground, 2.25 b apart, in close shots between face and abdomen with sparks at every contact; she springs back
to her mark low (apex 1 b, 314-334), seen at the landing.
`test_contact.py` (HI, after H2 and H3 land): at each row's ticks the distance from the point to her blade's centre line
(from her rig manifest's `hand_l` / `blade_tip` anchors) and to the actor's (from H3's manifest) is within tolerance.

**Mutual rows** (fix lane HF-B, HB-01: each side met its own stage point while the two bodies were 1-2 b apart in the throw).
Both figures' points, her side from `her_tracks.json`, the actor's from its manifest; gates of both builders
(`scarlet_cine.mjs` / `clips.mjs` `MUTUAL`; the rig builder's `--mutual-allow` while one side is being re-authored) and
`test_contact.py`:

| id | `repel` ticks | her | the actor | within |
|---|---|---|---|---|
| KW.grip | 36-48 | sword grip `hand_l` | `hand_l` | 0.20 b |
| KH.hilt | 49 | `hat_crown` | `pommel` / `hilt` | 0.20 b |
| KS.hook | 70-78 | sword forearm (`elbow_l` → `hand_l`) | `shoulder_r` | 0.30 b |
| KT.grip_r | 78-96 | sword forearm | `hand_r` (the fist with the sword hooked over it) | 0.15 b |
| KT.grip_l | 86-91 | sword forearm | `hand_l` (round her wrist; 79-85 it reaches for it, 92-97 it lets go) | 0.15 b |
| KT.over | 84-92, at her highest pelvis | `pelvis` | `shoulder_r` | 0-0.6 b over it, ≤ 0.5 b off it on the floor plane |
| KK.kick | 129 | `pelvis` | `foot_r` | 0.50 b |

The throw (78-101, HF-B): her root arcs only 0.6 b (`seq.py` `toss`); her pelvis rides its own path onto the actor's back and
over its right shoulder, low (0.34 b over it at 88), head first, face up; the actor bends forward with the hips back under
her, rolled left with the head ducked left of her body (≥ 0.38 b off her torso), its right fist hooked over her sword
forearm from the hook to 96 and its left hand round her wrist 86-91, pulling down in front; let go, she drops onto her back
at f 3.0 (101).

---------------------------------------------------------------------------------------------------------------------

## 5. Interfaces

### 5.1 `api.py` (owner H1; H1 lands these names in one **interface commit** before anything else, H2 / H3 branch from it)
- **Removed**: `DOWN_T`, `DOWN_FLOOR_WAIT`, `KIPUP_RECOVER`, `BU_DOWN`, `PIP_DASH`, `PIP_R` (and lane C's `PIP_Q`), `R1`, `R2`,
  `R3`, `R2_TWO_PCT`, `DISC`, `DISC_RELEASE`, `DISC_LOCK`, `DARK_T`, `DARK_CALL_T`, `BRIM_T`,
  `REAPPEAR['tell']`, test ids 11-13, 25, 31; sequences `sq1`, `lead_down`, `lead_stand`. (`DARK_SLICES` / `DARK_LIGHT` and
  the arena's `dark` look stay: the theme reads them; the module no longer requests the look.)
- **Changed**: `PIP_RULE = 'perfect_parry'`; `P1 = ('a1','a2','a3','a3s','a4','a6','a9','a10','d4','tri','rings','ult','hcut',
  'blue','kcut')`, `P2 = ('mx','nb','q','a8','a13')`; `HITS` (§2.2; each tuple gains a 7th field `'P'` / `'N'`); `WEIGHTS`,
  `COOLDOWN`, `MID_MAX` (+ `a3s` 8, `tri` 10, `blue` 7, `kcut` 8), `FAR_RULE`, `PAT_END` (+ `a3s` 40, `d4` 64, `tri` 70, `hcut` 38,
  `blue` 32, `kcut` 34, `mx` 40, `nb` 52, `ult` 58); `A8_SCRIPT`, `A13_SCRIPT`, `CUT_IDS`, `BOLTS` (§2.4); `JUDGE_T = {'a8': 220,
  'a13': 242}`, `REPEL_T = JUDGE_T`; `FAIL60_REFORM_T, FAIL60_P2_T = 220, 240`; `FAIL5_T = {'reappear': 236, 'black': 239,
  'slash': 242}`; `COUNTER_EV = ('strike', 'land', 'kick')` (49 / 101 / 129); `WARN_TEXT` (§2.4); `END_H = {'std': 1372}`;
  `SKIP_T = 1290`, `SKIP_WINDOW = (20, 1270)`; `SEQS = ('intro', 'cs1', 'lead60', 'repel', 'lead5', 'lead_re', 'ending',
  'event')`; `SEQ_ARGS = {'repel': {'at': (60, 5)}, 'lead_re': {'g': ('a8', 'a13')}}`; `SEQ_LEN = {'intro': 1440, 'cs1': 720,
  'lead60': 56, 'repel': 140, 'lead5': 116, 'lead_re': 60, 'ending': 1372, 'event': 120}`; `SEQ_CLIPS`; `LINE_AT` (§3: 1-11
  on `intro` / `intro_end`, 13-16 on `cs1`, 17-23 on `ending`, 12 and 24-25 unchanged); `MUSIC_AT`; `CLIPS_PLAN` (59 clips:
  47 − 3 + 3 lead-ins + 12 fight clips), `CINE_CLIPS`, `CLIP_OWNER` (owners `H1` / `H2` for the new rows); `PH` (3 =
  `lead60`, 6 reserved); `TEST_IDS`: 1 a1, 2 a2, 3 a3, 4 a4, 5 a6, 6 a9, 7 a10, 8 a3s, 9 d4, 10 tri, 11 rings, 12 rings +
  ult (gauge full), 13 hcut, 14 blue, 15 kcut, 16 mx, 17 nb, 18 q, 19 groggy now, 20 cs1 → lead60 → G1, 21 G1 now, 22 G1
  with the gauge at 0 (repel → P2), 23 G1 fail, 24 repel `{at:60}` only, 26 lead5 + G2, 27 G2 now, 28 G2 with the gauge at
  0 (repel → kill → ending → coda), 29 G2 fail, 30 intro replay, 32 look crimson, 33 P2 now, 34 HP = 5 % + 1, 35 intro
  skip at 100, 36 cs1 skip at 100, 37 gauge = 50, 38 balance = 1, 80, 90-92, 99 as now; registry `intro` 1450, `death` 1494.
- **New**: `GAUGE = {'max': 50, 'seg': 10, 'pat': 3, 'hit': 5}`, fake player `#gau`; `BAL = {'after_repel': 3, 'floor_min': 3,
  'grog_in': 12, 'kip': 20}`; `PP_FLINCH = 6`; `CUE_LEAD = 7`, `CUE_KIT = ('glint', {'c': 2})`, `CUE_SND = 'parry_cue'`;
  `FLASH = {'yellow': ('yellow_tell', {'t': 6}), 'purple': ('star4', {}), 'blue': ('flash_blue', {'t': 15})}`,
  `PURPLE_LEAD = 12`; `NP_OWN = ('#mbNpOwn', 'mb')`; `BAL_OFF = ('#mbBalOff', 'mb')`; `STAGE_FMAX = {'cs1': 10, 'repel': 10,
  'ending': 12}`; `CS0_P0 = (881.28, 201.0, 25.55)`, `CS0_BEARING = 7.5`, `CS0_WALK_BACK = 6.0`, `CS0_END_DIST = 6.5`;
  `SKIP = {'intro': {'window': (20, 1270), 'to': 1290}, 'cs1': {'window': (40, 560), 'to': 566}}`; `CONTACT` (§4.3);
  `ACTOR_CLIPS = {'cs0': 1440, 'cs1': 720, 'repel': 140, 'ending': 1372, 'coda': 120}`, `ACTOR_LIMIT = {'fwd': 2.5,
  'back': 1.5, 'side': 1.5, 'cs0_back': 6.0, 'air': 7.0}`; `OVERLAYS` + `gold` 0xEC17 (H2), `web` 0xEC18 (H1), their
  opacity steps U+EC38-EC3F; `KIT_PRESETS` + `flash_blue ['t']`, `ult_web ['t']`, `ult_burst []`, `sky_mark []`,
  `sky_pillar ['r']`, `qi_beam ['len']` (H1); `KIT_SOUND_RECIPES` + `parry_cue`, `flash_blue`, `ult_cut1`, `ult_cut2`,
  `sky_pillar`.
- Helpers: `api.actor(call, **macro)` / `api.actor_ready()` (the actor lines, `''` until H3's manifest exists),
  `api.cam_req()` (the `#mbCam` line). The core ↔ sequence signal stays `#sq_sig hr` = `SIG` (`hp1`-`hp3`, `refill`); a
  sequence still never calls core functions.

### 5.2 Camera and lock (H2; framework change **FN-cam** in `build_mboss_core.py`, helpers in `mboss_lib.py`, sequences use them through `tools/mboss_scarlet/cam.py`)
| name | meaning |
|---|---|
| `#mbCam mb` | the request: `mboss/main` zeroes it at its top, a module's tick (inside it, also the death tick) sets it to 1 while it wants the lock; `F:tick` reads it after `mboss/main`: 1 → `cam/hold`, 0 → `cam/release`. A paused fight runs no module tick, so a pause releases by itself |
| `#mbCamId mb` | 1 = camera A live, 2 = camera B live |
| `rlk_mb_cam1`, `rlk_mb_cam2` | the two marker armour stands (invisible, no gravity, `camera_distance` 0; tags `rlk_room rlk_mb_aux`) |
| `mboss/cam/spawn` | at the executor: both stands (idempotent) |
| `mboss/cam/hold` | `F:tick` while `#mbCam` 1: on the first tick store the game mode (a tag on the player), spectator; every tick `spectate` the live stand; `view/tick` does not re-seat a player carrying that tag |
| `mboss/cam/release` | when `#mbCam` is 0 (a no-op unless the player carries the hold tag) and on every exit path of §3.0: un-spectate, the player to the avatar, `rotate` to the boss body, game mode back, seat again; idempotent |
| `mboss/cam/kill` | removes the stands; the module's `cleanup` / `cancel` call it |
| `cam.cut(seq, t, id, frame, eye, look)` | place camera `id` at tick t − 1 and make it live at t |
| `cam.move(seq, t0, t1, id, frame, eye0, eye1, look0, look1, ease)` | one `tp … facing …` per tick on the live camera (`ease` `l` / `io`) |
| `cam.follow(seq, t0, t1, id, frame, eye, selector)` | the look point is an entity's eyes |
Frames `'ST'`, `'ST2'`, `'HR'`, `'W'`; `ST` / `ST2` run `at` the stage marker (`^-r ^u ^f`), `HR` at her body. Other bosses:
`#mbCam` is never set, so their output changes only by the shared `mboss/main` / `F:tick` lines.

### 5.3 Actor (H3; `F:char/cine/**`, objective `cine`, tags `rlk_cine_root` / `rlk_cine_part`)
| call | executor · position | effect |
|---|---|---|
| `function rlk:char/cine/spawn` | the player, at the stage marker, rotated as the stage | the root and the 11 displays with the current character's skin and `cine_sword`; the avatar hidden (a rig character's own displays too); idempotent |
| `function rlk:char/cine/play {clip:"<id>"}` | any | selects the clip (`#cavC cine`); does not touch `#cavT` |
| `#cavT cine` (fake player) | — | the clip tick to show; the module writes `#sq hr` into it every tick |
| `function rlk:char/cine/tick` | the player | shows tick `#cavT` of the clip (root `shift` and yaw from the stage, the parts); past the length: the last frame |
| `function rlk:char/cine/face {yaw:<deg>}` | any | turns the root to that absolute yaw over 12 t (the ending's ST → ST2); the clip's own root yaw adds to it |
| `function rlk:char/cine/stop` | any, no position | root and parts gone, the avatar visible; idempotent; also called by the framework's release |
H3 also writes `tools/player_motion/cine/manifest.json`: per clip the length and, per tick, the root `shift`, the hilt and
the tip of the blade and the two hands in the stage frame (for `test_contact.py` and H2's framing checks).

### 5.4 Other shared pieces
- **RIGLIB look target** (H2): `mboss_rig_compile.mjs` gains an option (default `@p[gamemode=!spectator]`, so every other
  rig is byte-identical); 홍련 passes `@e[tag=rlk_body,limit=1]`.
- **FN-bal** (H1): `#mbBalOff mb`, one line in `build_balance.py`'s `bal/boss/may`, zeroed in `fight_vars` / `cleanup_fight`.
- **Kit** (`build_mboss_hr_fx.py`, shared): H1 adds its presets, sounds and the `web` overlay; H2 adds the `gold` overlay;
  each in its own marked block; the generated `fx/**` and the manifest are regenerated at the merge, never merged by
  hand. Sprite budget: 22 432 px left; planned `flash_blue` ≤ 4 096 px, everything else reuses sprites.
- **Files**: H1 `tools/mboss_scarlet/{api,ai,p1,p_ghost,core,shield,s3lib}.py`, `scarlet_clips.mjs` (12 fight clips),
  `build_balance.py` (FN-bal), the pattern suites; H2 `tools/mboss_scarlet/{seq,cam}.py`, `scarlet_cine.mjs`,
  `build_mboss_core.py` + `mboss_lib.py` (FN-cam), `mboss_rig_compile.mjs`, `view/tick`'s one guard; H3
  `build_player_rig.mjs` (cine part), `tools/player_motion/cine/**`, `F:char/cine/**`, the RP's actor models. Until the
  other lane lands: H1 runs sequences as the existing stand-ins (wait the length, signals at their events); H2 runs
  with the actor calls guarded by `api.actor_ready()` (`''` until H3's manifest exists), as `api.rig` / `api.K` do.

---------------------------------------------------------------------------------------------------------------------

## 6. Tests and balance

### 6.1 H1 (suites under `tools/dev/sim/hr/tests/`)
- `pat_p1.py` / new `pat_p2.py`: per pattern the hit ticks, shapes, tiers, kb (last hit only), `mbHzNP` per hazard = the
  table's P / N, the cue glint exactly at h − 7 of every P hit and never before an N hit, the flash kit call and tick of
  every N hit (purple exactly 12 t before its cut), chain gaps ≥ 10, lock = h − 7,
  no `tele`, no decal, every end point through `mv/ok`, airborne spans < 45 t (first motion → hit: ≥ 12, new clips ≥ 14,
  big hits ≥ 20).
- `pat_ghost.py` rewritten: both scripts' made / lock / strike, gaps ≥ 14, a PP on cut k takes exactly one segment, PD /
  tier 2 / tier 1 / walking out take none, 5 PPs → the repel starts in the judge tick, 4 → the fail of each gauntlet,
  no balance pip leaves during a gauntlet (`#mbBalOff`), pause / reload cases of PLAN §5.6 with `lead_re`.
- new `test_gauge.py`: charge +3 / +5, cap, no charge in the excluded states, a full gauge forces `rings` → `ult`, 0 after
  cut2, full at `lead60` 0 and at the `refill` beats.
- new `test_bal_hr.py` (replaces her rows of `test_bal_boss.py`): groggy = `grog_in` → `down` → `kipup` at 20 left, 100 t,
  hittable, × 1.30; every `bal_ok` refusal of §1.3 leaves it pending and it starts at the first allowed tick; the floor
  rule; + 3 after the repel; `PP_FLINCH`.
- `test_scarlet.py`: the phase machine of §1.1 (no `down`), the new test ids, cleanup resets `#gau`, `#mbNpOwn`, `#mbBalOff`.
- Gates as every stage: regen ×2 identical, `check_mboss_pack` 0, loadcheck 0, other bosses' outputs unchanged except the
  FN-bal line, `test_rig` with the 59-clip contract.

### 6.2 H2
- new `test_cam.py` (framework): hold / release on each exit path (end, cancel, pause, `/reload`, relog, player death,
  Ronova revive, cleanup, abort, uninstall): the game mode restored, the player at the avatar, seated, no stand left;
  `spectate` re-issued every tick; killing the live stand does not strand the player; other bosses byte-identical apart
  from the shared lines.
- `test_seq.py` rewritten from §3: per sequence its length, the camera id and eye / look point at every cut tick (in
  the stage frame, for a stage at the arena centre and one at radius 24 on four bearings: every eye point and every
  position of hers inside the walk disc or above it, never in a block), each line id at its tick with its verbatim
  text and span, overlays and their ticks, `#sq_sig` at 49 / 101 / 129 and the refill beats, the skip of CS0 (→ 1290) and
  CS1 (→ 566) from any tick of the window, end states after pause / reload (§3.6), her distance to the avatar per beat
  (the *Distances* lines), bars on in the repel and off in the others.
- `test_rig`: the 8 cinematic clips' lengths / events / hand-over poses; the look-target option; ident for other rigs.

### 6.3 H3
- new `test_actor.py`: for each of the 7 characters `spawn` makes 11 parts + the root with that skin and the same
  `cine_sword`; `stop` leaves nothing and shows the avatar, on every exit path and when called twice; each clip's
  length; `shift` inside `ACTOR_LIMIT` at every tick and (0, 0, 0) at each hand-back tick (cs0 1440, cs1 720, repel 140,
  ending 330-1372, coda); feet never under the floor; ≤ 120° per tick; `#cavT` past the end holds; a jump of `#cavT`
  (the skips) shows the right frame; two builds identical; rplint 0; the atlas growth reported (Lumine's skin).
- HI: `test_contact.py` (§4.3) and one render sheet per cutscene (every cut tick, ≤ 640 px) next to the video frames.

### 6.4 Balance targets (PLAN §4.8, measured by `hrfair` 2.0; item-less Lv15 vs her level, seeds 11 / 22 / 33, 3 600 t per phase)
The probes learn the new defences. Agents: **walker** (melee, never presses F or dodges: the old baseline); **parrier σ**
(presses F for every cue, aimed at h − 1 with a normal timing error σ = 0 / 1.5 / 3 t; dodges nothing); **mixed σ**
(parries P hits, perfect-dodges N hits with the same σ); **dodger** (PD only, at h − 1 ± σ); **masher** (F every 4 t);
**sloppy** (F at h − 1 ± 6 t uniform). Gauntlet agents stand, or walk 0.22 b/t outward / sideways / inward, then act.

| # | target | band | change from PLAN §4.8 |
|---|---|---|---|
| T1 | P1 walker intake ÷ 타키 whole (same tool) | 1.00-1.15 | kept; the kit is new, so the weights are re-tuned to it |
| T1b | P1 parrier σ 3 intake ÷ walker | ≤ 0.60 | new: an average parrier is clearly rewarded |
| T1c | P1 mixed σ 0 intake | ≤ 5 % max HP / min | new: everything is answerable (no unavoidable hit) |
| T2 | P2 walker ÷ 타키 | ≤ 1.25 | kept |
| T3 | standing max(P1, P2) ÷ the Guardian standing | ≤ 1.8 | kept |
| T4 | walker's worst 40-t window (the G1 fail hit excluded) | ≤ 40 % | kept; `rings` + `ult` (35 %) and `q` (31 %) are the cases |
| T5 / T5b | every cut on a standing agent: G1 / G2 | ≤ 45 % / ≤ 55 % | G2 has 11 cuts; its fail is the death anyway |
| T6 | parrier σ 0 and σ 1 (stand / walk ×3): segments per timed F, gauntlets cleared | ≥ 95 % / ≥ 90 % | was the six dash agents |
| T7 | sloppy clears; masher clears; dodger clears | ≤ 35 %; 0 %; 0 % (no damage taken) | was the random dasher ≤ 50 % |
| T8 | A6 starts in any 400 t | ≤ 1 | kept |
| T9 | walker kill, fighting time only (cutscenes excluded) Lv5 / 10 / 15 | 150-185 s | was 230-270 s with cutscenes; the cutscenes are now 72 + 36 + 7 + 7 s and reported apart |
| T9b | parrier σ 1.5 kill, fighting time | 125-170 s | new (groggy windows) |
| T10 | groggies per minute of P1 / P2: parrier σ 1.5; walker | 0.8-1.3; ≤ 0.4 | new |
| T11 | U per minute of P1 / P2: walker; mixed σ 0 | 0.8-1.5; 0.6-1.0 | new |
| T12 | dodger σ 1 avoids an N hit it times | ≥ 95 % | new |
| T13 | parrier σ 0 parries every hit of every chain (no refused F) | 100 % | new: the 12-t / 2-t F rules against every chain gap |
Knobs, in this order: weights / cooldowns, recovery (P1 8-16, P2 10-16, ± 4), `GAUGE` rates, tiers ± 20 %, `hp` ± 15 %,
G2's cut count (9-11), `PP_FLINCH` 0-10. The item (`sword_hwamu`) and the buff are not re-tuned here (PLAN §7 unchanged).

**Restated by HB, 11-11 (lead-approved: the HB brief and the lead's message after review H-A).** The table above stays as
written; where these lines differ, they are the targets the balance pass measures (`hrfair2.py`, `hb_progress.md`):
- **Every target per seed.** Each row passes on seed 11, 22 and 33 separately and pooled (the kill runs on all three seeds).
- **T1 / T2: the 타키 reference is measured by the same tool.** hrfair 1.x's 124.0 %/min cannot be reproduced: its walker
  dodged on reaction, hrfair 2.0's never defends. `hrfair2.py base` fights 타키's whole fight with the same walker on the same
  tree (its rift and intro as in the game, real HP at L16, seeds 11 / 22 / 33): **232.3 %/min** (230.3 / 228.6 / 238.0). Bands
  unchanged: T1 = P1 walker ÷ 232.3 in 1.00-1.15, T2 = P2 walker ÷ 232.3 ≤ 1.25.
- **T3: the Guardian standing re-measured** by the same tool (azsim's plaza, Lv15 vs L15, 3 600 t × 3 seeds): **165.1 %/min**
  (the recorded 164.0 is reproduced). Band unchanged (≤ 1.8).
- **T6 σ 1 and T12: a share of the best the window allows.** A 3-tick window around a press aimed at h − 1 with a normal
  error σ 1 t holds P(|e| ≤ 1) = 86.6 % of presses, and a seed has only ~50-90 timed inputs (± 4 % by chance alone). The
  target is now: of the timed inputs whose own error fell inside the window, **≥ 95 %** end as a perfect parry (T6) / a
  perfect dodge (T12) — what the fight (the F lock, the whiff streak, the 18 / 12 t dodge cooldown, the hit timing) takes away
  from the window's best is at most 5 %. The raw rate is reported next to the 86.6 % ceiling. T6's cleared rate (σ 0 ≥ 95 %,
  σ 1 ≥ 90 %) is unchanged.
- **T7m (new, the lead after review H-A): a metronome F** — pressed every p ticks from any phase k (p 8..30, every k, no cue
  read) — clears **neither gauntlet (0 %)**. The gauntlet timing is fix lane HF-A's (`A8_SCRIPT` / `A13_SCRIPT`); G2's cut
  count is not a balance knob for now.
- **The input rules are the game's**: hrsim's world now runs the real `player/f_key` and `dashCool` (review H-A), checked by
  `tests/test_input_hr.py`.

**Relaxed by the lead, 11-11** (binding; next to HB's restatement above):
- **T10**: an average parrier (σ 1.5) may break her **0.8-1.6** times per minute of P1 / P2 overall (the groggy is the parry
  reward; 0.8-1.3 was the lead's design number, not the user's). The walker's ≤ 0.4 is unchanged.
- **The unparriable share of the pick weight**: in every band (near / mid / far) of both phases, and in the far rule, the
  unparriable entries (`a9 a10 hcut blue kcut`; `mx` and `q` count half: one of their two kinds of hit is flashed) take at
  most **35 %** of the weight; the parried chains keep the majority (the user: 「패링 불가 공격: 보스의 일부 큰 공격만」). The
  gauge-forced `rings` → `ult` stays outside the weights. `api.NP_SHARE` / `NP_SHARE_MAX`, checked at every build.

---------------------------------------------------------------------------------------------------------------------

## 7. Open questions (each has the default the build proceeds with)
| # | question | default | switch |
|---|---|---|---|
| 1 | CS0 length. The video is 101.5 s | 72 s (1440 t) with the skip to the last 7.5 s; alternatives: 52 s (dialogue shots at 0.6 ×) or the full 101.5 s | `SEQ_LEN['intro']`, the shot table |
| 2 | May CS1 be skipped (Shift held, as CS0)? | yes: it is 36 s in the middle of the fight and repeats on every attempt; the skip keeps line 15, line 16 and the slash | `SKIP['cs1']` |
| 3 | The 5 % gauntlet's fail stays an instant death under the parry rule, and the banner's wording | kept (the lead); 「베기를 완벽하게 패링해 실드를 모두 깎으세요 — 실드가 남으면 즉사합니다」 | `ULT5_LETHAL`, `WARN_TEXT` |
| 4 | How many cuts in G2, and do tier-2 parries count? | 11 cuts (6 spare), perfect only | `A13_SCRIPT`, `PIP_RULE` |
| 5 | The grab of `q` has no flash in the video. Parryable? | yes (the brief's rule: only flagged attacks are unparriable); the other reading (grabs are unparriable, the user's example) would give it a purple flash | `HITS['q']` |
| 6 | The sky pillar's mark (a light line from the sky + a 2-b flash line at the feet, 7 t before) is the video's only ground mark | shown as in the video (README 0-6 allows what the video shows); off = the purple flash alone | `sky_mark` call |
| 7 | In the video the grab carries Eve into the sky under an in-engine camera | not done: the player stays on the ground and in control; her aerial part plays above them | — |
| 8 | Arlecchino's avatar is 1.4 × the others | the actor is 1.0 × for every character, so every contact point holds | H3 |
| 9 | Lumine has no RP skin | H3 fetches it from the profile texture; if that fails, the nearest skin and a report (the brief) | H3 |
| 10 | Who authors the 12 new fight clips | H1 (they are timed to its patterns); H2 keeps the 8 cinematic clips | `CLIP_OWNER` |
| 11 | P-y (a yellow flash, then she only leaps away) | the leap is kept as `mx`'s retreat, without the flash: a flash that no attack follows would break "yellow = dodge" | `mx` |
| 12 | In the video Eve is not hurt by 홍련일섬; the brief has the actor hit and kneeling | the actor is hit, kneels and rises; no HP is lost | actor clip `cs1` |
| 13 | The parry cue glint on every parryable hit (the video shows it on some) | on, always at h − 7: one learnable rule without text | `CUE_*` |
| 14 | Balance after the first repel | + 3 of 12 (the video: + 4 of 20) | `BAL['after_repel']` |
| 15 | The one sword of the actor | the player rig's existing `sword` model under the id `cine_sword` (0 new atlas px) | H3 |
| 16 | The ending (68.6 s) cannot be skipped, as today | kept | — |

---------------------------------------------------------------------------------------------------------------------

## 8. Lead rulings (11-11) — binding; where they differ from the text above, these win
1. **Open questions**: the defaults of 1-4, 6-9 and 11-16 stand.
2. **Question 5 — the grab of `q` is unparriable.** The user's decision names grabs (`decisions.md`: 「보스의 일부 큰 공격만
   (범위 공격 · 잡기 등)」). `q_grab`: purple flash (`star4`) at tick **8** (12 t before the grab at 20), no parry cue,
   `hz_opts(noparry=1)`; events `glint 0, ghost 4, star 8, lock 13, go 16, grab 20, end 40`. Outcomes: missed / PD / left
   the disc → reform, end 34; landed → `q_air`. The PP branch is gone. §2.5: `q` parryable 2 (beam, dive), unparriable 2
   (grab, pillar).
3. **Question 10 — lanes.** The work is split in five (file owners; nobody edits another lane's source files):
   | lane | branch | owns |
   |---|---|---|
   | H1 | `wip/combat-hr1` | `tools/mboss_scarlet/{api,ai,p1,p_ghost,core,shield,s3lib}.py`, FN-bal (`build_balance.py`'s one line), the pattern / gauntlet / gauge / balance suites, `hrfair` 2.0. New fight clips are placeholders of the contract length, kit calls are guarded |
   | H1c | `wip/combat-hr1c` | the 12 new fight clips in `tools/scarlet_clips.mjs` (§2.3), the H1 block of `build_mboss_hr_fx.py` (presets `flash_blue ult_web ult_burst sky_mark sky_pillar qi_beam`, the sounds, the `web` overlay, `parry_cue`) |
   | H2 | `wip/combat-hr2` | FN-cam (`build_mboss_core.py`, `mboss_lib.py`), the RIGLIB look target, `tools/mboss_scarlet/{seq,cam}.py` (all sequences, shot tables, lines, effects, skips, hand-backs), `view/tick`'s guard; her cinematic clips are placeholders until H2c lands |
   | H2c | `wip/combat-hr2c` | her 8 cinematic clips in `tools/scarlet_cine.mjs` (§4.1, the contacts of §4.3), the `gold` overlay block of the kit |
   | H3 | `wip/combat-hr3` | the actor: `build_player_rig.mjs` (cine part), `tools/player_motion/cine/**`, `F:char/cine/**`, the RP's actor models (§4.2, §4.3, §5.3) |
   Generated outputs (`rig/**`, `fx/**`, manifests, module functions) are never merged by hand: the lead regenerates them
   at each merge. Merge order at HI: H1 → H1c → H2 → H2c → H3.
4. **Interface commit.** H1's first commit (subject starts with `H1 interface`) adds §5.1's names to `api.py` additively
   (the old module keeps building) and is pushed to `wip/combat-hr1` at once. The other lanes take names and numbers
   from this file until it is there, then merge it (`git fetch origin wip/combat-hr1`).
5. **Airborne spans** (타키's lesson, README 0-6): `nb` (44 t) and each half of `q_air` (38 t) are the ceiling; no clip
   may hold her out of reach longer, and none hovers idle.
6. **The sky mark** stays a line (the light line and the 2-b line at the feet): never an area on the floor.
7. Commit trailer for every lane from now on:
   `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_019wi9c7roqDDkFi2TvFWw6G`.

## 8.8 Review H-A fixes (lane HFA, 11-11; `review/rulings_HA.md` on `origin/wip/combat`) — binding where they differ from the above
- **HA-01**: `core/pat_end` starts `ult` after the forced `rings` only `unless #fl` (as `mx`'s repeat): a floor reached during the
  rings ends the chain there; the recovery, then the decision starts CS1 / `lead5`.
- **HA-02**: `on_hit` feeds no reaction while `grgT` runs; `core/trig0` clears `#ctr #flq #a6q #hits` at `bal_on` and `bal_off`:
  after the groggy the 12-t recovery always runs first.
- **HA-04**: the reload hook calls `core/grog_re` during a groggy: `down` at once (> 20 left), else `kipup` from the tick the
  groggy has reached.
- **HA-05**: `bal_ok` refuses `a4` 28-38 too (the ring hop); `test_bal_hr` reads her body height in every pattern.
- **HA-03**: the gauntlet strikes are re-timed (§2.4 rows moved by a few ticks, see `api.A8_SCRIPT` / `A13_SCRIPT` and
  `hfa_progress.md`) so that no blind metronome clears them; `tests/test_metro.py` drives the real F functions. G1 strikes
  30 48 64 91 109 139 163 180 196 (≤ 3 perfect parries for every period 8-30 and start, as ruled); G2 strikes 27 41 58 91 113 128
  152 169 190 206 220 (deviation: an exhaustive search proved that with 11 cuts, gaps ≥ 14 and the moves' own spacing no set
  stays at ≤ 3 for every period; this one reaches 4 only at 16 t / 19 t for a few starts, and 5 at no period 2-40). Bolts G1
  34 99 166 218, G2 70 160 198 240; G2's extra vanish 97.
- **HA-06 / HA-07**: the cue's sound and sprite (above, §2.1).
- **HA-08**: `q`'s grab kb 0.
- **HA-09**: a full gauge forces `rings` in the near band only; from the mid band `ai/ult_close` glides her in (0.3 b/t to 4 b,
  at most 40 t), then the decision starts the rings.

## 8.9 Round V, lane VC (11-11 playtest; `v_brief.md` §3 "VC", `review/v/client_facts.md`) — binding where it differs from §3.0 / §5.2
What §3.0 "Camera", §3.1-§3.5 (shot tables) and §5.2 say about camera STANDS is replaced; the lock's request protocol
(`#mbCam` / `#mbCamId`, hold / release in `rlk:tick`, every exit path) is unchanged. As built: `vc_progress.md`.
- **Camera entity**: an empty `item_display` (no ghost), not a marker armour stand. The game is played in F5: the client looks
  from 4 b behind a non-living camera entity. Every shot is authored as a VIEWPOINT ("eye"); `mboss/cam/fix` puts the placed
  rotation on the 360 / 256 grid and moves the entity 4 b forward. First person and F5-front are not supported in a cutscene.
- **Motion**: keyframes; the client interpolates (`teleport_duration` <= 59, set a tick ahead), one placement per segment.
  `cam.Track.move` (straight segments, <= 59 t, <= 12 degrees each), `track` (her walk / turn: led by `seq.HER`, her moves on
  the stage), `chase` (per tick at 3-tick interpolation, only I16 and E7). No per-tick re-aim anywhere else.
- **Cuts**: the idle camera is prepared 3 ticks ahead (duration 0, the snap at t - 2, the first segment's duration at t - 1)
  and has stood settled for 2 ticks when it goes live; every shot lasts >= 3 ticks.
- **The 4-block line**: for every locked tick the camera entity is in air and the 8-ray pull-back to the viewpoint meets no
  block (test_seq `stages` G5, CS0's fixed stage and five placements of the dynamic one); on a dynamic stage the entity is
  also pulled into the walk disc and kept 0.3 b over the floor (`seq/lib/camin`). Shots that looked steeply down at
  something near were re-aimed (I7 the cup: level; I1 starts at f -7.0).
- **Hold**: interaction ranges 0 by a modifier, the sidebar off, the F5 seat removed for the lock (made again at the
  hand-back with an empty action bar after the mount), `mboss/cam/post` (the reward of a tick advancement, armed per held
  tick) spectating again after the game's own player tick, real re-sends of the camera while asked.
- **Skip**: the jump key held `SKIP_HOLD` ticks (`seq/<name>/skipin`); Shift is no input. The skip's landing = the unskipped
  state (test_seq `skip` K1: her place, yaw and MODEL, the client's picture, the texts, the props, the stage, the actor's
  clock); `seq.RIG_NOW` after every instant move of her body.
- **Lines**: in a locked sequence on the camera's `text_display` (lower third, dark backdrop, >= 28 px at 1080p for a field
  of view of 70-90), typed two syllables per 2 t; the kit's subtitle line only without a held player. The skip prompt on
  the hint text under it.
- **Shot table changes**: CS0 opening mask black 0 / 34 / 8 (the arrival); I1 0-75 (push 24-74), I2 76-109; I5 aimed at her
  shoulder (her face above the line); I7 level; I15 tracked; I16 from the side at r -4.6 (chase); CS1 S10's petal passes
  behind her, S11 cut at 608 with the petal at her waist 1.5 b from the lens; the ending's E7 chased, E9b's petal behind her.

## Round V addendum (lane VP, 11-11): the perfect parry / dodge beat
What this document says about the player's parry / dodge effects (the streak, the 1.5-degree jolt, "does not stop or slow the
server", tier 2's star) is replaced by `v_brief.md` §3 "VP" + §5 as built: README 3 「효과」 · 「박자」 and `vp_progress.md`. For her
fight this means: a perfect parry or perfect dodge of any cut freezes / slows her whole module (pattern clock, rig, gauntlet,
shield and ULT clocks, hazards) through `mboss/main`'s first line and resumes it 5 / 7 ticks later with nothing else changed;
the pips (`q_pf0` / `q_pf1`, `#mbDodgeOk`) read the beat's clock; her effect kit must subtract `#btLag cb` from its game-time
reads (request to lane VB in `vp_progress.md`).

## 9. Round V (11-11, lane VB) — what `v_brief.md` §3 "VB" changed in this design
`v_brief.md` wins over §2 where they disagree. As built (`vb_progress.md`; `tools/mboss_scarlet/blade.py`):
- §2.1 tells: every hit keeps its cue (P) / its flash (N) and gains **the drawn blade path** (a line in the air along the tip's
  way from the wind-up to the hit, its head arriving on the hit tick; white-gold for P, the flash's colour for N) — for a swing
  riding her, for a dash / a plunge the straight line from her to the locked spot (+ a tall mark over the spot for a dash), for a
  gauntlet cut standing at the cut's station. The cue star stands on the blade's middle unless that is low or on her hat (then over
  the hat's crown); the flashes are at her head, larger, with a dark-rimmed star inside.
- §2.2 the kit effects at the hits (`qi_arc`, `qi_vert`, `qi_fan`, `qi_wedge`, `qi_ring`, `qi_line`, `qi_cut`, `qi_band`, `qi_x`,
  `qi_dome`, A4's ribbon and slash line) are replaced by **the slash generated from the blade track**: one sector card per
  <= 45 deg of blade sweep, in the plane of the two blade positions that bound it, born on the tick the sweep is shown, gone 6 t
  later. Impact effects that are not a blade's trail stay (dive_impact, burst_radial, claw_streaks, qi_beam, sky_mark / sky_pillar,
  ult_web / ult_burst, the overlays).
- §2.2 moves: `LEAP_H` a4 / a10 / nb / q 3.4, q2 3.6 (were 6 / 5 / 5 / 5 / 6); A4 and A10 keep 3 b from the player in the air (were
  2 / 1.5); the dash-throughs (A9, HCUT, BLUE, KCUT) stop 2.0 b before the locked spot (the hazard keeps its probed length
  through the spot); the dives (A4, A10, q_air's) land 1.4 b before the locked spot. Hit ticks, shapes, tiers, weights: unchanged.
- §2.3 clips: the wind-ups (reached >= 10 t before a single / first hit, >= 6 t before a chain hit, held): a1 (no fan flourish), a2
  (blend 2), a3 h1 / h2 / h5, a4's apex, d4 h1 / h4, tri h0 / h2, rings r1, blue, mx's dome, nb b2 / b3; the gauntlet's approaches
  hold the next cut's wind-up, every cut's tail ends in the next cut's wind-up, g_rise has no spin, g_vert cuts down from the
  raised blade; `g_dive` = 22 t (appear 0, dive 15, hit 18).
- §2.4 gauntlets: the station = `REAPPEAR['D1']['end']` (2.2 b at +35: the player's front right), fixed 10 t before the strike (an
  approach: at its start) as the marker `rlk_hr_gst`; A8.3 leaps to 1.3 b before the player; the dive reappears 18 t before the
  judge 3 b over a spot 4.5 b before the player (`A8_SCRIPT` 202, `A13_SCRIPT` 224) and ends 1 b over the spot 2 b before them.
- §1.2 the gauge's under bar shows its five segments (dividers; `#buSubSeg bu 5`).

## 10. Round V, the integration (11-12, lane VI) — what the merge of VC / VP / VB added to this design
As built: `vi_progress.md`, `tools/dev/sim/hr/tests/test_vi.py`.
- **Her kit's card clock is the beat's clock** (`build_mboss_hr_fx.py`: `fx/e/make` and `fx/e/world` read the game time minus
  `#btLag cb`, `fx/e/world` only re-schedules itself on a held tick): the cue star, the flashes and every preset card stand still
  with her and stay in step with the hit they announce. The HUD clocks of the kit (the typed line, the overlays) stay on the raw
  game time: they mirror `title` timers of the client, which no beat holds. The sweep cards of §9 need nothing: they are literal
  commands on pattern ticks.
- **Her model after an instant move in the fight** (`s3lib.RIG_NOW` = `rig/follow_now` at the body): the gauntlets' reappearances
  (`p_ghost.tp_spot`), a cancelled leap's landing (`core/ground_to`; `g/ground` uses it), the revive's placing (`core/place8`),
  the replay's seat. Before, the model stayed where she vanished for 3-16 ticks after every reappearance (§8.9's finding, in the
  fight). Incremental moves inside the hook (walk, dash steps) keep the old one-tick trail (<= 0.3 b).
- **The skip**: the core's parked input (`core/skip`, `core/skip_cs1`) reads the jump key too; `api.SKIP_HINT` = ' · Space 길게'.
- **Lead, at the release (11-12): `DMG['T2']` is back at 42.** The pooled T1 on the merged tree is 1.007 (in band); the per-seed 0.97 is accepted like HB's per-seed caveats. The entry below records what the integration measured with 44.
- **§6.4**: `DMG['T2']` 42 -> 44 (raw 6 -> 7). On the merged tree T1 fell to 0.97 on seed 33 (lane VB's moves shift where the next
  pick starts from); a damage tier changes no pick and no clock, so every other row keeps its measured value (the table in the
  README's 홍련 section and `vi_progress.md`).
- **The actor hides lane VP's stand-in rig** (`char/cine/hide`: `rlk_pl` out of view) for the one tick a beat outlives the start of
  a locked sequence.


## 11. Round W (11-12, lane WB) — the blade's trail replaces the drawn path (`w_brief.md` §2 "WB"; `wb_progress.md`)
The user, after round V in play: 「보스의 검로가 보이는건 미리 경로를 보여주라는게 아니라 공격이 좀 더 잘 보이도록 이미 지나온 경로를
표시하라는 거야」. `w_brief.md` wins over §9 where they disagree. As built (`tools/mboss_scarlet/blade.py`):
- §2.1 tells: **nothing shows where the blade is going to go**. §9's drawn path, its running head, the dash / dive target lines, the
  tall mark over a dash's spot, kcut's three lines, nb's band lines and the gauntlet station's standing path are gone (with their
  run-time `core/sw/{aim,march,head}` and the kit card `sw_path`). The telegraph is the wind-up pose, the cue star (P), the colour
  flashes (N) and the sounds, as before.
- §2.2 effects: **the trail of where the blade has been**, generated from the sword part's transform per clip tick as the client
  shows it (the rig's sidecar `scarlet_blade_track.json`: `sp` / `sq` per tick, `f0` = where the clip's blend-in from the pose before
  ends), played at the pattern ticks the pattern plays its clips:
  - the **band** on the blade (lance `sw_band`, 0.26 b, from the guard to the tip) carries the sword part's own translation and
    rotation and is sent the next tick's transform each tick with one tick of interpolation: it moves exactly as the blade does,
    from the first known pose (the first clip's `f0`) to the end of the last hit's follow-through (its swing's b);
  - the **pieces**: the surface the blade sweeps in each tick, in planar pieces of <= 30 deg of blade turn (a wedge `sw_fan` with
    its chord as the bright rim when it turns about a point of its own line, a strip `sw_quad` when it slides sideways), each with a
    rim wall (0.22 b; a swing's 0.30 b) so it reads edge-on; the sweep t -> t + 1 opens on t + 1 (**one tick behind the blade**:
    a planar piece cannot follow the client's curved slerp inside a fast tick without running ahead of it somewhere), rides her
    model for its two ticks and then stays where it was swept; fading frames at +3 / +5, gone 7 t after it began to open;
  - a swing's pieces (a hit's [a, b]) are mixed 55 % toward white with the taller wall: §9's slash IS the trail's brightest stretch;
  - the **ribbon** (`sw_rib`, 0.30 b) behind her where her body carries the blade (A4 / A10 / q_air dives, A9 / HCUT / BLUE / KCUT
    dashes, TRI's lunge, MX's streak, Q's ghost lunge; the gauntlet's D1-D4 approaches, A8.3's leap, the A8.9 dive): from the hand's
    place when the move began, grown each tick to the hand's place one tick back (`core/sw/rib`), fading after the move, 6 t;
  - the **wave**: the struck line of a dash-through (from the dash start along the probed length) and kcut's three crossing lines
    flash ON the hit tick for 4 t (they reach beyond her blade).
  Colour: the hit the blade is on its way to — white-gold `#FFE9A8` (P), the flash's colour (N); every bright core has ink on both
  sides (the white-gold is close to the P1 wheat: ΔE 15). Sizes: every bright core / ribbon >= 0.12 b.
- §1.5 a perfect parry's flinch (`core/pp`) kills the band and fades the rest; `core/pat_end` / `core/g/end` kill whatever of a trail
  is left. The band and the pieces carry `rlk_mb_part` (the perfect parry / dodge beat treats them as her rig's parts); the fight
  hook rides them to the rig's root part after `rig/tick` (`blade.RIDE_CMD`).
- §2.2 moves (review w T3-06, the camera inside her): a stop point must keep her body 1.3 b off the player's camera line (their eyes
  to 4 b behind them along their view, `core/cam_ok`): the dash-throughs' stop (2.0 b before the spot, else 3.5 b, else she cuts from
  where she is), `core/near` (the dives: 1.4 b, else 2.9 b, else the spot), MX's streak, the gauntlet spots' candidates; after a move
  standing in that line she steps 1.8 b out of it in 2 t (`core/cam_clear`: a9, hcut, blue, kcut, tri, a4, a10, mx, q_air's dive).
  Hit ticks, damage, shapes, weights, the wind-up clips, the blade edge, the cue star, the flashes, leap heights, dash stops and the
  gauntlet stations are §9's.
- §6.1 tests: `test_blade.py` (rewritten), `test_vi.py` beatpat (the trail cards beat on = off, frozen on held ticks).
- **§2.4 the gauntlets re-timed** (the user's ruling 11-12, after lane WP removed the whiff ladder: every accepted F locks 12 t, a
  parry of any tier 1 t, an ignored press blocks F 3 t; the lock rule stays and only the cut ticks move): G1 strikes
  **31 45 64 88 108 138 163 181 195** (round V 30 48 64 91 109 139 163 180 196), G2 **28 46 66 89 112 127 151 170 189 205 219**
  (27 41 58 91 113 128 152 169 190 206 220); the judges 220 / 242, the dives' reappearances 202 / 224, the clips and their order
  unchanged; every move keeps its offset from the strike it delivers (`api._g1_rows` / `_g2_rows`: D -14 (D3 -16), ring / wrap /
  dome -3, rise / leap -9, X -6, vert -5), every gap >= 14, a reappearance >= 2 t after the vanish before it; G2's extra vanish
  96 (was 97); bolts G1 34 96 166 218 (99 -> 96: 2 t from c5's lock), G2 70 160 195 240 (198 = c10's lock -> 195). Result
  (`tests/test_metro.py`, the real F functions, every period 1-40 and every start from T - 200): **at most 4 perfect parries in
  either gauntlet** (5 clear). No table keeps every period at 3 under these rules and the moves' spacing (the exhaustive search
  `tools/dev/sim/hr/review/metro/dfs.c -DNOLADDER`: G1 none); the G1 table is the one of the 6 364 sets within 14 t of round V's
  with the fewest periods reaching 4 (4, 15, 19, 25, 33 t), the G2 table the nearest found (distance 23 t; 4 at 3-8, 12-23, 31 t).

## 12. Round W, the integration (11-12, lane WI) — what the merge of WC / WP / WB added to this design
As built: `wi_progress.md`, `tools/dev/sim/hr/tests/test_wi.py` (beside `test_vi.py`).
- **The player's dodge set against her** (§2.1, `test_wi dodgecam`): with the real `player/dash` / move line / back-step / cartwheel in
  every pattern and both gauntlets, three views (on her, frozen, 60° off), the F5 camera (4 b behind the eyes) is never inside her
  and she never moves onto the player; her camera-line step (`core/cam_clear`) was never needed, standing or moving (§11's stops
  already keep her out of the line at the move's end). Her body comes within 1.3 b of the line only when the player's own double
  dodge carries them next to her (a direction-less double dodge goes along the view: a forward cartwheel into her) or her hit's
  knockback throws them across her landing (G1's dive after a missed answer). No rule was changed for it.
- **A dodge in flight when a locked sequence starts** ends one tick into the lock (`player/tick` -> `player/dodge/cut` while the
  player carries `rlk_mb_camh`): no travel of the hidden avatar, the crouch and the cartwheel's stand-in rig gone. `rlk:tick` runs
  the stand-in rig's tick when no beat runs (a mannequin character's plain cartwheel froze it before).
- **Her damage numbers** (review w T3-09): numbers on her body are 2/3 size, beside her as the player sees her (1.1-1.5 b off the
  line to the player, 1.9-2.4 b up; `combat/text_normal_side`); every other target keeps the old numbers.
- **The trail at a sequence start** (`test_wi trailcut`): CS1 (`core/cs1/start`: `kill @e[tag=rlk_hr_p]`), the ending
  (`death_start` -> `core/stop_all`) and the repel (`core/g/end`) leave no trail entity one tick later, with a beat running or not;
  lane WC's `seq.KILL_FIGHT_FX` (round V's `rlk_hr_sw` cards) needs no change.
- **§6.4 on the final tree** (`hrfair2.py`, all 175 runs, log `tools/dev/sim/hr/review/bal/wi_final.log`): every row passes except
  **T1 on seed 33: 0.97** (1.02 / 1.03 / 0.97, pooled 1.01) — as at the 11-12 release (`DMG['T2']` 42, the lead's reading of HB's
  per-seed caveat); no balance value was changed. T6 σ0 / σ1 cleared 100 %, T7 0 / 0 / 0, T13 53 / 53.
