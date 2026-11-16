# Requests and notes from AP-P1 (phase-1 patterns P1-P6, R, M sounds; E, D — `tools/mboss_apep/p1.py`, `seq.py`, branch `wip/ap-p1`)

Protocol: `S:ap/ap_contract.md` §0.11 (append-only, `## R<stage>-<n> <type>: <title>`, what / why / needed by, status).
Every workaround below lives in AP-P1's own files behind a `TODO(I2)` marker; nothing outside `api.OWN['p1']` /
`['seq']` was written. Suite: `S:ap/tests/pat_p1.py` (exports `TABLE`).

## RP1-1 api: a yaw-schedule rebase helper for a turn inside a yaw clip (P5)

- what: `Gen.yaw_rebase()` (or a `start_yaw` argument of `AP:play/<clip>`): set the running yaw schedule's start
  (`#apYaw0`) from the body's current Rotation.
- why: P5 turns its back to the player over t1-8 (<= 5 deg/t, plan 8.1) while `tail_p1x2` already plays; the core's
  `yaw/tick` pins Rotation to `#apYaw0 + schedule[t]` every tick, so a plain turn is undone. `p/tail/turn` writes
  `#apYaw0` itself (marked `TODO(I2) RP1-1`): a core score written by a pattern file.
- needed by: AP-I2 (replace the one line). status: open.

## RP1-2 core: tick the org objects (RORG-3); P2 steps its stalks meanwhile

- what: run `AP:om/objects_tick` once per tick while any Heart / dome / stalk / wall display exists (requests/org.md
  RORG-3), then drop P2's own `om/stalk/tick` span.
- why: nothing calls `om/objects_tick` on `wip/ap` d15e500, so the stalk clips (`leg_rise` / `leg_slam` / `leg_sink`)
  would not advance. P2 calls `function AP:om/stalk/tick` on t36-99 itself (`TL.span` in `p1.py emit_hands`, marked
  `TODO(I2) RP1-2`). If the core starts ticking the objects without removing that span, the stalks step twice per tick
  (half-length clips, the slam hit at the wrong tick).
- needed by: AP-I2 (one of the two, together). status: open.

## RP1-3 api: `api.wedges()` misses slivers of the lane when the tail root moves

- what: build each swept wedge so it covers the lane the tail line swept since the last tick, not only the angle range
  about this tick's root. `p1.py swept()` does it for P5: each wedge keeps its root and grows to every point of the
  previous tick's tail line seen from that root from 3 b out, radius <= reach + 1.5 (`API_WEDGES*` vs `WEDGES*`).
- why: the `tail_p1x2` root swings ~1.2 b per tick round the anchor; with the bare api wedges a standing player 4-6 b in
  front was crossed by swing 1 between t34 and t35 without being inside either wedge (pat_p1 P5f / P5j, before the fix:
  no hit). The widened wedges overlap the previous one inside the same volley group (still one hit per swing).
- needed by: AP-I2 (move the widening into `api.wedges`, e.g. an option); AP-P3's Q4 uses the same api and likely has
  the same gap. status: open.

## RP1-4 plan: decisions inside the plan's latitude for the I2 change note

- what (plan 8.1 rows, no tick / size / coefficient change):
  1. P1: the shadow glides at the predictive lock (lead 10, re-aimed at t23 / 26 / 29) as fast as the distance needs
     to reach it by t32 (the 10-20 rule: the shadow on the lock 12 t before the burst); the plan's "<= 0.7 b/t" cannot
     reach a player more than ~6 b away. The anchor stops with the rig's burst anchor (3.13 b ahead) on the lock; the
     burst disc sits there (= the lock unless the r 18 clamp moved the anchor). The `p1_ring` sound stays at t32 (audio).
  2. P2: the plunge disc is centred on the rig's `hands` plunge anchor (4.22 b ahead, where the hands go in), not on
     the anchor; the stalks stand 6.6 b from the lock at +-60 deg (near, the boss side) and +-140 deg (far) of the
     lock -> boss direction, slams R-L-L-R = near right, far left, near left, far right (v1 H); a root beyond r 25.3
     steps toward the lock. Strips 3-4 are made at t41 (tells 34 / 41 instead of 35 / 42): the four crack decals and
     strips in one tick next to the rising stalks passed the 3000-command budget.
  3. P3: the slams land on the rig's slam anchor (4.22 b ahead of the anchor parked at the centre); the carpet and the
     wheels start there; the blade rays 1 t after the slam (perf). The two homing wheels leave the carpet front at
     +-12 deg of the player's bearing and steer (8 deg/t) from their 2nd tick while riding at 0.75 b/t for 6 t, then
     0.5 b/t: with "ride 6 t, then home" a player 6-11 b from the slam point was out of reach (the 3.6-b turn radius
     is larger than the gap; v1 G shows the wheels curving back onto the player). A wheel reaches a standing player up
     to ~14 b out; both may hit together (2 x 0.15; one shares the carpet's group).
  4. P5: the pre-swing turn puts the tail root (the back) toward the player. With the rig's yaw schedule swing 1 sweeps
     the start frame's front (-61 .. +89 deg) and swing 2 its back (-94 .. -227 deg); a BACK player meets swing 2, a
     front player swing 1. A second tail-tip flash + cue at cock 2 (t48) marks swing 2 (the recoil from t37 is its
     readable start, 15 t).
  5. P6: hit 4's disc is 7.2 b ahead of where the 2.5-b lunge glide (inside r 16) ends.
- why: plan 14 asks for a dated change note on any change; these fill gaps of the rows (anchors, directions, perf).
- needed by: AP-I2 (plan.md §14 note). status: open.

## RP1-5 kit (RI1-1 follow-up): where the outline-only crack lands in P2

- what: when `K.tele_crack(..., fill=False)` (requests/fx.md RI1-1) exists, switch P2's two call sites: the strips
  (`Gen.decal('keep', K.tele_crack(...))` in `p1.py emit_hands`) and the resume redraw macro `AP:p/hands/crack`
  (`$function K.FN/tele/crack {...}`, a macro line written in p1.py). P4 keeps its filling disc; P1 needs no outline
  (the `shadow_glide` preset is its marker).
- needed by: AP-I2. status: open.

## AP-I2 status (2026-10-21, `wip/ap` f588262; plan §14 "AP-I2 integrate", contract §3)

- RP1-1: done f588262: `Gen.yaw_rebase()` = `AP:yaw/rebase`; `p/tail/turn` calls it (no `#apYaw0` write in p1.py).
- RP1-2: done f588262: the core's `AP:obj/tick` steps the stalks (and every org object) before the slot; P2's own
  `om/stalk/tick` span dropped; `leg_slam` played 5 t before each slam (the hit key 4 lands on the slam tick); pat_p1 P2h / P2i.
- RP1-3: done f588262: `api.wedges(..., swept=True)` (identical wedges for P5; Q4 uses it too).
- RP1-4: done f588262: plan §14 AP-I2 note, item 5.
- RP1-5: done f588262: `tele/crack_o` for the strips and the resume macro `p/hands/crack`.
