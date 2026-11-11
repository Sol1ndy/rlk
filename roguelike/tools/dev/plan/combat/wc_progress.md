# Round W, lane WC (cutscenes) — progress

Branch `wip/w-cam` (from `origin/wip/w` 540f5f68c; merged `origin/wip/w` up to the cine review ca7dc5924+), worktree `<S>/cb/wt_wc`,
pack copy `<S>/rp_wc` (from `<S>/rp_rel3`, the 11-12 release pack); `<S>` = the scratchpad of `w_brief.md`. Contract: `w_brief.md`
§2 "WC" 1–4, §4 "WC, added" 5–7, the cine review `review/w/findings_cine.json` (25 findings), `v_brief.md` §3 "VC" + §4, `h_common.md`.
Commit trailer: w_brief §5 (Opus 5.5). Recordings: `<S>/cb/video3/t3.mp4`, `t4.mp4`; my frame grabs `<S>/cb/video3/wc/`.
Scratch: `<S>/cb/wc/` — scripts `fullregen.sh` (README 0-4 order, twice, hashes), `suite.sh <tag> <tests…>`, `regen.sh` (core + scarlet),
`dbg.sh <her clips> <actor clips>` (debug frames), `shots.sh <seq> <ticks> <out>` (built_shots at FOV 90), `fr.py <seq>` (two-figure
report), `stray.py` (where the idle camera's text showed in the old build), probes `pr_drink.mjs` / `pr_blade*.mjs`; sheets `a_*` =
before, `b_*` = after.

## Steps
- [x] diagnose from t3 / t4 and sheets: drinks, the petal, S5, the stray text, the locks, the aerial duel
- [x] the stray text (§4.7): only the live camera carries a text (`mboss/cam/text`, storage `rlk:mboss camtx`), re-applied at each cut
- [x] FOV 90 the reference for the camera texts (line 36 px at 90; the hint top right); test_cam T1 / T2 at 70 / 90 / 110
- [x] S5 from above (6.5 b, the stage axis across the picture); two-figure check `framing.two_figure_bad` + test_seq F5, `Shot.full`
- [x] the S11 petal falls and is cut on its way down; halves; test_seq P1–P6; the intro petals I3 / I4; S10's petal removed
- [x] the drinks: CS1 S9 rebuilt (solver channels `lipL` / `botW` / `botH`), S9b profile shot; intro I9 cup level → tilt with the head;
      her_tracks `mouth` / `cup` / `bottle`; test_cine drinks
- [x] §4.5 bodies apart: every lock 1.3 b behind the contact for her, the actor's hilt 0.55 b before it (K1 0.95, KE2 2.2, KE5 3.45,
      KG 2.95; the repel she lands at 1.95); test_contact `gap` (torso axes >= 1.5 b in every lock / clash span)
- [x] §4.6 the aerial duel → the exchange on the ground (KA1–KA4 at u 1.25–1.85), close shots, sparks / flash / sound per contact,
      a low spring back (apex 1 b) seen at the landing; the actor's exchange and backing-off
- [x] review: hand-backs under a short black, R8 from 118, I16 as 4-t track segments, fight blade-path cards killed at cutscene starts,
      I7 "wrong pictures" = the user's F5 (README states the F5 assumption)
- [x] final gates on the final tree, push (see "Gates")

## What was wrong (diagnosis) and what is built
- **Stray line (§4.7, T3-/T4-TEXT-STRAY)**: `cam_line` wrote the line on BOTH cameras' texts. The idle camera stands in the world (the
  last shot's place, or the next shot's PRE ticks early) and its billboard text, 3.7 b toward the viewer from that entity, showed in the
  live picture small and far (t3 S11 138–140 s, t4 E16 113–117 s and the coda 126 s: my crop `<S>/cb/video3/wc/t4_stray_crop.jpg`;
  `stray.py` on the old build predicted 338 / 80 / 241 ticks in intro / cs1 / ending). Fix: the text lives in storage; `mboss/cam/text`
  writes it on the live camera's texts (tags `rlk_mb_camx1` / `_camx2`) and blanks the idle camera's; `cam.Track.lines()` calls it at
  every cut; `cam/kill` blanks the store. Tests: test_cam T1 (live only, a cut moves it, kill blanks), test_seq X1 (every held tick of every
  sequence: no text on a non-live camera; the line shown on the live camera on every line tick).
- **Top-down (S5, item 3)**: 5 b up with the axis up the picture: 7 b of floor at FOV 70, the figures 9 b apart outside top and bottom.
  Now 6.5 b up, the axis across the picture (16 x 9 b at 70); both figures head to foot at 70 / 90 / 110 (`b_cs1_s5.jpg`).
- **Petal (item 2)**: hung still before the lens, 0.8-b card at 1.5 b, the cut line 0.9 s before the draw, the blade swept low past it.
  Now: summoned above S11's picture, falls 0.055 b/t with a sway (±0.12 b, 26-t period) for 46 t (in the picture 33 t at FOV 90, entering
  at its top), on her blade's line at the cut tick 647 (her draw raised to a level cut at her waist: `scarlet_cine.mjs` DRAW_GE / DRAW_TH;
  the blade 0.01 b from the petal's centre), card 0.95 (375 px tall at FOV 90, 263 at 110), the glowing line + glint at 647, then two half
  cards (`rlk:hr_cine/petal_half_a` / `_b` on the kit's texture) falling on and apart 17 t. `b_cs1_lock_petal.jpg`.
- **Drinks (item 1, T3-DRINK-1/2)**: CS1 S9 tipped the bottle in the forearm's frame with the arm out to the side: base to the lens beside
  her ear, the rim 0.2–0.35 b off her mouth, a nod hiding her face. Now reach → lift upright to the lips (446–457) → bottle and head tip back
  together (botH 0 → 98°, head 26° back; held with two sips) → upright again (491) → lowered; rim at her mouth 0.066 b; S9b (446) from her
  right front. Intro I9: lifted level to the lips (590–602), cup and head tip together (cup 52–58°), level by 644; rim 0.04–0.06 b. The
  reviewer's I6 / I8 / I9 framing (from behind) is not reframed: I9's drink is now readable only from the side shots — open (see below).
- **Bodies (§4.5, T4-OVERLAP-1)**: torso axes were 0.9–1.2 b apart in every lock (head to head 1.1–1.5). Now K1 1.96, KR 1.82, KE2 2.03,
  KE5 2.16, KA1 2.09, KA2 1.66, KA3 1.99, KA4 2.04 b (test_contact `gap`, GAP_MIN 1.5). The grab / strike / hook / throw / kick of the repel
  stay scripted contacts.
- **Aerial duel (§4.6, T4-AIR-1)**: ~6 s airborne at 6 b. Now 204–310 on the ground, 2.25 b apart: guard 212; a1 228 her diagonal on the
  actor's block; a2 262 her overhead (stepping in to 4.35) on its raised one-hand guard; a3 286 cut on cut (gold); a4 298–304 the X lock;
  pushed off to 5.3; a spring back 314–334 apex 1 b to the landing mark. Shots: E6 the guard (side), a1 her side, the actor, a2 the blades
  low, her wind-up, a3 over her shoulder, a4 the lock (side), E7 the landing; sparks x3 + gold card + arcs at each contact, sparks every 2 t in
  the lock, flashes at a1 / a2 / a3. `b_end_exchange.jpg`, `b_end_a3.jpg`.
- **Hand-backs (T3-HAND-1)**: a short black (in 3 · hold 5 · out 5) over the release of CS0, CS1 and the repel (60 %).
- **I16 chase (T3-CHASE-1)**: per-tick re-aims (3-t interpolation) → 4-tick segments led along her arc (`track`). E7 chase removed.
- **R8 (T4-REPEL-KICK)**: the shot from 118 (11 t before the kick), was 3 frames.
- **T4-LIGHTBAR**: a fight blade-path card (lane VB's `rlk_hr_sw`) left standing: every cutscene start kills them.
- **T3-CAM-WRONG (I7 20.92–22.12 s)**: the user pressed F5 (front → first person → back): the geometry of I7's camera matches both pictures
  (front: 4 b in front of the entity looking back, with the hint visible; first person: at the entity, no text). Not a bug; README says the
  framing assumes F5-back and the server can neither block nor detect F5.
- Text sizes (T3-V-TEXT): measured 24–25 px at FOV 90 → now 36 px (line), 20 px (hint).

## Deviations
- `tools/mboss_scarlet/api.py` (lane VB's file in round V): only the cutscene contact table `CONTACT` (K1, KG, KE2, KE5, KA1–KA4) changed —
  the contact points ARE the staging this lane owns; hr_design.md §4.3 updated with them.
- The aerial duel's event ticks (rise 204, a1 228, a2 262, a3 286, a4 298, off 304, fly 314, land 334) and the ending's length are kept: the
  exchange uses the same beats (no registry / test number had to change).
- KA2: the actor's raised guard is one-handed (two hands could not reach a horizontal blade above the head 0.55 b out).
- The intro head tilt in the drink is 12–13° (the right fist with the cup entered her head box at 17–20°: the builder's guard).
- I6 / I8 / I9 (the intro's pour / toast / drink seen from behind, T3-DRINK-2) are not reframed: out of time; the motions themselves are fixed.
- test_rig: the S10 petal coupling is replaced (S10 has no petal); the big-swing spans of the ending are the exchange's cuts.

## Pack files (all from `tools/build_blank_tex.py`, no new texture: atlas unchanged 13.108 M)
`assets/rlk/items/hr_cine/petal_half_a.json`, `petal_half_b.json`, `assets/rlk/models/item/hr_cine/petal_half_a.json`, `petal_half_b.json`.

## Requests to other lanes
- VB / WB: `api.CONTACT` (cutscene rows) changed as above; `core.py`'s fight blade-path cards are killed at every cutscene start (seq.KILL_FIGHT_FX).
- Lead: the release pack must include the four `hr_cine` files (`build_blank_tex.py --resourcepack`).

## Gates (the final tree; suites from a copy of tools/dev/sim outside the tree)
| gate | result |
|---|---|
| full regeneration (`fullregen.sh`: scarlet rig, hr kit, bossbar, combat fx, player rig + actor, player audio, blank tex, `regen_all.sh --mobs`, bf / fg kits) twice | identical tree hash `cf09524c9f6aba26` and pack hash both rounds |
| test_seq | ALL (572 checks; new F5 two-figure x 5 runs, X1 stray text x 5, P1–P6 the petal) |
| test_cam | ALL (164; T1 live-only texts, T2 sizes at 70 / 90 / 110) |
| ev_dry / test_flow / test_vi | 82 / 82, 40 / 40, 208 / 208 |
| test_cine / test_contact / test_actor / test_rig | 172 / 172 (drinks), 102 / 102 (gap), 157 / 157, 162 / 162 |
| ident_hr / test_scarlet | ALL / 48 / 48 |
| gen_check_hr | 28 / 28 (1466 s) |
| check_mboss_pack | 0 problems |
| loadcheck (26.3 server) | `wc_a` (checkpoint) and `wc_b` (final): 0 function load failures, `Done (` |
| rplint `rp_wc` / atlas_px | 0 problems / 13 107 904 px (13.108 M, unchanged) |
| `diff -rq rp_rel3 rp_wc` | only `assets/rlk/{items,models/item}/hr_cine` (the half petals) |

## Only a person in the game can check
- The stray line gone (S11, E16, the coda): one text, at the bottom.
- The drinks read as drinking (CS1 S9 / S9b, intro I9), the petal falls and is cut, its halves fall (under the red tint at 650+).
- The exchange: blades meeting with sparks at reach, no bodies touching; the low spring back; the hand-back blacks are short enough.
- F5-back only during cutscenes (F5 front / first person show the wrong place until cycled back).
