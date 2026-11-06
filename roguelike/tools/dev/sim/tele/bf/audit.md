# Ground-telegraph audit: 달빛 환영 나비 (module `butterfly`, human + butterfly forms)

Rule (user, 2026-10-20): a pre-hit ground telegraph only where the reference footage shows one; otherwise the player
reads the boss's motion and sound. Read-only audit of release HEAD 039b911 (`/home/user/rlk`, nothing changed).

Sources checked: `mb2/src/v1..v4.mp4`, `mb2/understand/v1..v4.md` + `model.md`, `mb2/plan.md`, `mb2/spec/*`,
`roguelike/tools/mboss_butterfly/{api,core,human,wing,seq_b,seq_h}.py`, `build_mboss_bf_fx.py` (tele/* and presets),
`build_mboss_core.py` (hz/make, hz/init, hz/tick, hz/draw, hz/strike, hz/flash, pj/*). Timing constants were read by
importing the generator package (no build): played ticks after the RETIME wind-up tuning.

## Summary

* **The footage never shows a ground telegraph for this boss.** The analysis notes say so for v2 ("no telegraph decals
  are ever drawn on it") and v4 ("no telegraph decals are drawn by the boss"), and the frames I extracted for every
  attack in v1-v4 show none before any hit. Ground light that does appear is either the attack itself at or after
  impact (H1 hit-2 ground burst, B1 slash band, B2 landing splashes, B3 eruption, B4 ground blades) or an effect at
  the boss's own feet (H3 charge glow, B5 ground flash).
* **Today every damaging hazard is a quiet framework hazard (`#hzQuiet 1`, `#hzSfx 0`)** paired in the same tick with a
  kit floor decal (`fx/tele/disc|sector|line`: static rim + progress fill + flash on the hit). There is no framework
  outline or strike flash anywhere, so those stay off. There are also a few extra pre-hit markers that are not decals:
  * H2: a knee-high dust ring at r 3;
  * H2: a floating glint over the disc target;
  * H3 and H4: telegraph-only `tell_line` hazards (dmg 0);
  * B4: a dust "shadow" ring under the orbs;
  * B5: an end_rod "safe line" at r 10.5.
* **Decisions:** 12 hazards REMOVE, 1 TRIM (the B3 flame trail keeps its red ember line, which is in the footage, and
  loses its disc decal), and 1 KEEP (달빛 고치: unavoidable, and nothing on the ground before it).
* **Wind-up floor used:** 10 t. The plans' 12 t telegraphs were cut to 10 t by the user's wind-up tuning
  (`api.tell_rt`, plan "User feedback after the 10-18 release"). Measured from the first distinguishable tell (clip pose
  or body fx plus sound) to the hit, every hazard meets 10 t except **H1 hit 1**. Once its decal at clock -2 goes, it
  has only 8 t of motion: readability fix needed, see flags.
* **Systemic catch:** after a pause, the core `resume` hook redraws a kit decal for every quiet hazard still in its tell
  (`core.py` 325-351, `u/redraw`). B2's `p/barrage/resume` + `redraw` do the same for its landing markers. Both must go,
  or the removed decals come back after every pause.
* **Impact visual at the hit tick:** every hazard already has one from the module or the kit (listed per row), so
  `#hzQuiet 1` needs no added strike visual.

## Table

Clock = pattern clock `#bfPT` = played clip tick (H1 starts at -2). "Tell → hit" is the first distinguishable tell
(clip pose or body fx plus sound) to the damaging tick; the aim-lock time is given where it differs.

| id | hazard (shape, coef, hit tick) | current pre-hit telegraph | footage (video, s) | decision | player reads instead | tell → hit | impact visual at hit |
|---|---|---|---|---|---|---|---|
| H1-a | 달빛 발차기 hit 1: lane 4.0 × 2.4 (back 0.5) at A + disc r 1.5 at A+1.2, one group, h1a 55, clock 8 | quiet hz + kit `tele_line` + `tele_disc` (Dendro rim + fill) from -2 = 10 t; amethyst resonate cue at -2 (`human.py` 188-193) | v1 9.80-10.20 (hit 10.15): no floor marker; tell = burst-run with chambered knee 9.87-10.07, foot sparkles 10.07, ground spark burst ~1 m ahead 10.133 (1 t before) | REMOVE | burst-run 0-5 (breeze jump, moss steps, sweep), foot sparkles t5, glint t6, ground spark t7 (footage) | motion 0→8 = **8 t < 10**; only the sound cue at -2 gives 10 → **fix** | `kick_rise` crescent, streak, leaf blades, `kick_impact` at 8 |
| H1-b | hit 2: half disc r 5 (sector ±90) + ground wave line 6 × 2 at B, one group, h1b 70, clock 32 | quiet hz + `tele_sector` + `tele_line` from lock 21 = 11 t; resonate cue (`human.py` 241-247) | v1 10.87-11.73 (hit 11.73): hops, leap, foot swirl; no floor marker; ground burst + streak only with the hit (11.73-11.97) | REMOVE | foot glow from 17, side hops 19/22, aim snap 21, leap to B 25, foot ripple + resonate 28, glint 30 | foot glow 17→32 = 15 t; lock 21→32 = 11 t ✓ | `kick_axe`, burst, flash, `ground_wave` at 32 |
| H2-a | 달빛 점프 sweep: disc r 3 round her, act 4, feet ≤ 1.0 (jumpable), h2a 45, clock 10 | quiet hz + `tele_disc` r 3 from 0 = 10 t; **knee-high dust ring r 3** (`h_ring_dust`, y 0.5) at 6 and 8; resonate at 0 (`human.py` 312-317) | v1 25.30-26.03 + v4 28.45-29.40: arm shard glows, pivot, knee band; no ring on the floor or at knee height before | REMOVE (decal + both knee rings; keep the post-sweep dust ring at 11 and the foot streak at 7) | `shard_tell` on her arm + snd at 0, arm dust / end_rod 0-9, chime 4, foot streak + resonate 7 | 0→10 = 10 t ✓ | kit `sweep`, double crescents, leaves 10-14 |
| H2-b | kicked Dendro disc: disc r 2.5 locked under the player at 32 (walk-disc clamp), h2b 70, KB heavy, impact 42 | quiet hz + `tele_disc` r 2.5 from 32 = 10 t; **glint card 3 b above the target** for 10 t; amethyst-cluster sound at the target (`human.py` 346-352) | v1 27.53-28.13 (impact 28.133) + v4 30.60-31.13: floor at the player clear (only her real shadow); orb carried overhead, star flash ~3 m over the player 4 t before, disc visibly falling 2 t | REMOVE (decal + floating target glint; the footage's star = our `orb_star` at 38). The target sound stays (sound) | spiral jump at the player 22, orb at her foot 34, star 38, kick + `disc_fall` 39-42 (visible falling disc) | jump 22→42 = 20 t; lock 32→42 = 10 t ✓ | `disc_impact`, glow, flash, dust, leaves at 42 |
| H3 | 달빛 돌진 kick disc r 1.5 at D+1.2 (clock 11) + ring r 3.5 at D (clock 15, act 3), one group, h3 130; dash lane S→D | quiet hz + `tele_disc` 1.5 (10 t) + `tele_disc` 3.5 (14 t) from lock 1; **telegraph-only lane** = `tell_line` dmg 0 + `tele_line` 0.8 wide, 5 t (`human.py` 410-436) | v2 3.90-4.75: motes and a faint floor glow at **her own feet** (charge), coil, dash, kick, ring; nothing at D or along the lane | REMOVE (both decals; the dmg-0 lane hazard and its decal entirely: `ln/*`, `lane` dispatch, `dist`). Keep `dash_charge` (its floor glow is at her feet, in the footage) | mote charge + glow + snd 0, converging motes 3-5, rising chimes, foot glint 4, `dash_streak` 6-8, sweep 10 | charge 0→11 = 11 t (ring 15); lock 1→11 = 10 t ✓ | burst, glow, flash at 11; `kick_burst` ring, ripple, crescents, ring dust at 15 |
| H4 | 광폭한 진공 blade: pj blade hr 1.5, 0.75 b/t, no homing, h4 120, spawned at 13 | lane = `tell_line` dmg 0 (3 b wide, her → wall) + `tele_line`, from the glint 5, tell 10-60 (fill tracks the blade) (`human.py` 503-512, `edge_search`) | v2 13.20-14.40 + 22.70-23.40: leg glow, flame spike + glint at the foot, stomp flare at her foot, blade rises and travels; no lane on the floor (a scar appears only behind the blade) | REMOVE (lane hazard + decal, `edge_search`, `lane` dispatch) | `vac_crouch` leg glow 0, `vac_glint` + snd 5, rear-up 8-10, stomp flare 12, the visible blade (trail, debris, pass sound) | crouch 0→spawn 13 + travel; glint 5→reach ≥ 10 t for any lane ≥ 2 b ✓ | blade itself; spark at the player on hit (`hit`) |
| TF | 달빛 고치 at the transformation sphere: 20 % current HP, non-lethal, unavoidable (no hz) | none before; floor dust rings r 3/4/5 at 8-10 come **after** the sphere at 5 (`seq_b.py` transform) | v2 24.10-24.65: sheath, wings open, sphere, HP drop at 24.50, ripple rings after; no floor marker | KEEP (nothing to change) | n/a (cannot be dodged); sheath glow 0, wings 3, core flash 4, sphere 5 | n/a | `tf_sphere`, flash, curse chime at 5; ripples 8-10 |
| B1 | 우아한 날개: lane 10 × 3.5 from her spot S + sector r 4 ±60 at L, one group, b1 70, clock 11 | quiet hz + `tele_line` + `tele_sector` from lock 1 = 10 t; resonate cue (`wing.py` 176-189) | v2 35.25-35.93 (hit 35.93): flap, bank, dive; no floor marker; the ground slash band appears with and after the hit (35.93-36.13, v3 replay 0.0-0.3) | REMOVE | bank 0-4 + flap snd 1, wingtip dust, swoop glide 4-11 toward L (`wing_dive`, streaks, phantom swoop 8) | clip 0→11 = 11 t; lock 1→11 = 10 t ✓ | wing crescents at her, burst + leaves at L at 11; `wing_band` + lane bands 12-13 |
| B2 | 화염 날개의 습격 crescents: pj, 5 per swing × 4, splash r 1.2, b2 35, one hit per swing; land s+2+i+5+D (D 7-60) | Pyro `tele_disc` r 1.2 at each target from the swing (W 14-77 t), fill reaching the rim at landing; redrawn after a pause (`wing.py` 290-304, 379, 439-446) | v3 8.30-8.95 + 9.60-10.16: crescents fan out and dive through the air; floor clear before landings; splashes and vertical flame streaks only at landing (8.70-8.95, 9.95-10.16) | REMOVE (`tele/*`, `tele/pick`, the `tele/pick` call in `dive*`, `resume` / `redraw`) | wind-up turn + wingtip embers + flap/sweep at s-4, flame sheet at s, each crescent visible from s+2+i with its flame tail, dive hiss | s-4 → earliest landing s+14 = 18 t ✓ | `fire_land` splash + 2.5 b flame streak + scorch + sound |
| B3-fan | 날개 휩쓸개 eruption: sector r 4.5 ±90 at P, 2.5 tall, act 5 (21-25), b3 80 | quiet hz + Pyro `tele_sector` from lock 11 = 10 t; firecharge cue (`wing.py` 487-496) | v3 12.33-13.07 (eruption 12.95): flaps, rise, dive, wingtip flame crescents at slam 12.85, flame sweeping along the floor 12.88-12.92 (part of the attack, 1 t before); nothing on the floor earlier | REMOVE | V-up wings + Pyro rim glow + `flap_big` 0, wingtip flames, downstroke 4, lock cue 11, dive 13, `flame_slam` 19, floor flame streaks 20 (footage) | 0→21 = 21 t; lock 11→21 = 10 t ✓ | `flame_fan` sheet + roar at 21, embers, scorch |
| B3-trail | flame trail: 4 discs r 1 under her at 27/29/31/33, strike +10, act 8, b3t 20, max 2 (two groups), KB 0 | Pyro `tele_disc` r 1 (10 t) **plus** a dark-red ember streak card on the floor (life 18) + ember dust (`wing.py` 520-526) | v3 13.30-13.68: red flame lines trail on the floor behind her glide, fading by ~13.6; whether they damage is unconfirmed (v3.md) | TRIM: drop the disc decal; keep the red ember streak (the footage's flame line, the trail's own visual) and the strike flare | the red line she lays down as she glides; flare 10 t later | line visible 10 t before its strike ✓ | `flame_trail` flare, flame tongues, crackle (hz_vis) |
| B4-orb | 달빛 축복 orb contact: pj 0.25 b/t, steers 9°/t for 40 t, hr 0.8, b4 100, own group per orb; launched 14 / 34 | no decal; **lime dust "shadow" ring on the floor under the orb every 10 t** of flight + hum (`wing.py` 637, 642-644) | v3 21.30-21.55 (orb 1), 22.60-22.80 (orb 2): glowing orbs, no shadow ring or marker | REMOVE (the shadow dust ring; keep the hum sound and every effect on the orb itself) | wing-wrap charge 3 (`orb_charge` + snd), orb 1 at 14; cocoon ball 22-30, re-charge, orb 2 at 34; the slow glowing orb | wrap 3→14 = 11 t; ball 22→34 = 12 t ✓ | `pop` → `orb_burst` + flash on contact |
| B4-burst | orb burst: disc r 2.8 under the stopped orb, strike at orb age 50 (stops at 40), b4 100 (orb's group), KB 3 | quiet hz + Dendro `tele_disc` r 2.8 from age 40 = 10 t; beacon sound (`wing.py` 626, 645-648) | v3 21.55-21.80 (orb 1 sinks, camera swings, then radial ground blades; medium confidence) + 22.73-22.87 (orb 2 flash + radial ground blades): no marker before either burst | REMOVE (orb 1 partly ambiguous → remove) | the orb stops at 40 and pulses (scale 1.95 / 1.7 / 1.95 at 41/44/47, effects on the projectile), beacon sound at 40 | stop 40→50 = 10 t ✓ | `orb_burst` radial blades + flash at 50 |
| B5 | 달빛 해제 dome: disc r 10 at R, b5 130, KB heavy, E = 40 | quiet hz + Dendro `tele_disc` r 10 from the cup 23 = 17 t; **end_rod safe-line ring r 10.5** at 31 and 35; HUD caption "달빛 해제" at 0 (`wing.py` 751-769) | v3 33.60-36.27 (E 36.267) + v4 replay 0.70-7.57: fold, swoop, whirl + star flare, cup (E-22), **ground flash** = lime mist cone 2-3 m under her (E-18..-16), X glint, ring cage round her body, pod, white flash, dome; no r 10 marker in any frame | REMOVE (r 10 decal + safe-line ring). Keep `rel_ground_flash` at 26 (in the footage, local, under her = the centre) and the caption (HUD) | caption 0, fold + swoop past the player to R 3-~11, whirl + flare + charge sound 14-22, cup 23 (anchor charge, beacon), ground flash 26, X glint + cage 28/31, pod 33, sonic charge 37 | cup 23→40 = 17 t; caption 0→40 ✓ | `rel_dome` r 10, boom, white then lime screen flash |

Not hazards (no rows): the entrance (cocoon floor disc `cocoon_disc` is footage-shown and deals no damage), the groggy,
the 달빛 이슬 orbs, the cure, death (no damage). The body never deals contact damage.

Footage-shown effects that stay (they are not telegraphs):
* H1: the ground spark `burst` card at clock 7, 1 t before hit 1 (footage 10.133).
* H3: the `dash_charge` floor glow at her feet (footage 4.00).
* B3: the floor flame streaks at 20, 1 t before the fan (footage 12.88-12.92).
* B5: `rel_ground_flash` (footage E-18).

## What changes in code (for the implementer)

* `human.py` `pair()` and `wing.py` `hz_tele()`: keep the hazard with `quiet=1, sfx=0` and drop the `tele_*` line.
* Delete these extra pre-hit markers:
  * H2: `h_ring_dust` at SWEEP-4 and SWEEP-2 (`human.py` 316-317);
  * H2: the glint `~ ~3 ~` at L (`human.py` 350-351);
  * H3: `lane` / `dist` / `ln/*` (`human.py` 410-436);
  * H4: `edge` / `lane` / `ln/*` / `edge_search` (`human.py` 503-512, 600+);
  * B2: `tele/*`, `tele/pick`, the `tele/pick` call in `dive*` (keep the `mbT` bookkeeping), `resume` and `redraw`;
  * B4: `shadow` (keep `g.snd('orb_fly')` elsewhere in the orb tick);
  * B5: the `safe` lines.
* `core.py` `resume` hook: drop the `u/redraw` call and the `u/redraw` function. No butterfly hazard keeps a decal
  after this change, so nothing needs redrawing. The kit `tele/clear` calls in pause/cancel/death are harmless and can
  stay.
* H1 hit 1: add a body tell at clock -2 (see flag 1). No other timing, size or damage changes are needed for
  readability.

## Evidence

Contact sheets and crops (time-stamped cells) in
`/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/tele/bf/evidence/`:

| file | what it shows |
|---|---|
| `H1a_v1_09.80-10.30.jpg` | H1 hit 1 lead-in: no floor marker before 10.15 |
| `H1b_v1_11.00-11.70.jpg` | H1 hit 2 wind-up + leap: floor clear until the hit at 11.70 |
| `H2sweep_v1_25.30-26.00.jpg`, `H2sweep_v4_28.40-29.20.jpg` | shard tell → sweep, no ring (the ring round the player's feet in v4 is the player's shield) |
| `H2disc_v1_floor_26.80-28.13.jpg` | floor crops at the player: clear until the disc lands at 28.13 |
| `H2disc_v4_30.60-31.10.jpg` | second instance: star flash → disc, no marker |
| `H3_v2_03.90-04.70.jpg`, `H3charge_v2_crop_03.90-04.45.jpg` | mote charge with faint glow at her feet; nothing at D or along the lane |
| `H4_v2_13.30-14.40.jpg`, `H4_v2_22.70-23.40.jpg` | crouch, glint, stomp, blade; no lane |
| `TF_coc_v2_24.10-24.60.jpg` | transformation sphere, no floor marker |
| `B1_v2_35.30-35.90.jpg` | bank + dive; no lane / arc before the hit |
| `B2_v3_floor_08.45-08.76.jpg`, `B2_v3_09.60-10.10.jpg` | crescents in the air; no floor markers before landings |
| `B3fan_v3_12.33-13.07.jpg` | flaps → dive → slam → eruption; floor clear before |
| `B3trail_v3_13.20-13.70.jpg` | the red flame lines on the floor behind the glide (the trail itself) |
| `B4orb1_v3_crop_21.50-21.71.jpg`, `B4orb2_v3_22.53-22.87.jpg` | orbs and their ground-blade bursts; no marker before |
| `B5_v3_34.90-36.17.jpg`, `B5_v4replay_05.55-07.10.jpg` | whirl, ground flash (local, under her), ring cage round her, pod; no r 10 floor marker |

## Flags

1. **H1 hit 1 needs a readability fix.**
   * Without the clock -2 decal, the first pose tell is the clip's burst-run at 0, which is 8 t before the hit at 8
     (floor 10).
   * Fix without a timing change: at -2 add a body tell. For example, the kit's `snd/kick_whoosh` (described as the
     "H1 hit 1 lead-in", currently unused), plus a `glint` / glow on her kicking foot (the footage's chambered knee).
2. **The pause redraw would bring the removed decals back.**
   * `core.py` `resume` → `u/redraw` redraws a kit decal for every `rlk_mb_hzq` hazard still in its tell (lines
     325-351).
   * B2's `p/barrage/resume` + `redraw` do the same for its landing markers.
   * Both must be removed or gated.
3. **The H3 dash lane and the H4 blade lane are telegraph-only framework hazards** (`tell_line`, dmg 0). Remove the
   hazards and their helper functions, not only the decals.
4. **Non-decal pre-hit markers also go:**
   * H2: the knee-high dust ring r 3 (clocks 6, 8);
   * H2: the floating glint 3 b over the disc target (32-42). It is a mid-air target marker that is not in the footage;
     the footage's star flash is our `orb_star` at 38;
   * B4: the orb "shadow" dust ring;
   * B5: the r 10.5 end_rod safe line.
5. **Ambiguous: B3 flame trail.**
   * The footage's red lines (v3 13.30-13.68) are the trail itself, and their damage is unconfirmed.
   * Decision TRIM: drop the r 1 disc decal and keep our red ember streak (the footage line), which stays visible 10 t
     before the flare.
6. **Ambiguous: B4 orb 1 burst.** The camera swings at v3 21.55-21.70 and the notes give medium confidence. No marker is
   visible, so REMOVE (the rule: uncertain means remove).
7. **Borderline: the B4 orb shadow ring** reads as a depth cue rather than an area marker. The footage has none, so
   REMOVE. The orb's own glow and particles remain the cue.
8. **Hazards that land away from the boss all have a visible precursor**, as the footage does:
   * H2 disc: orb overhead, star flash, falling disc;
   * B2: the flying crescents;
   * B4 burst: the stopped, pulsing orb.

   None needs anything added.
9. **Optional, B5:** the hardest hit (1.3×) loses its r 10 decal, so the radius is learned only from the dome. The
   wind-up is long (cup → E 17 t, caption → E 40 t) and a dash at E works. An optional hint on the existing HUD caption
   is allowed (HUD is not a telegraph). No ground decal should be invented.
10. **Docs and tests describe the decals and will need updating:**
    * README butterfly section (lines ~617-629, the `resume` sentence in ~645);
    * the `human.py` / `wing.py` docstrings, plan.md "Telegraphs", bf_contract.md;
    * the scratchpad tests `mb2/tests/pat_human.py`, `pat_wing.py`, `test_human.py` (long-fight telegraph rule),
      `test_fixes.py` (FX-1 pause redraw), `test_butterfly.py`.
11. Kept as sound, not marker: the H2 amethyst-cluster sound played at the disc target, and every resonate / firecharge
    "tell cue" sound at the old decal ticks. These are sounds, which the rule keeps.
