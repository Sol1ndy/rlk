# Requests and notes from AP-FX (the Apep fx kit, `tools/build_mboss_ap_fx.py`, branch `wip/ap-fx`)

Protocol: `S:ap/ap_contract.md` §0.11 (append-only, `## R<stage>-<n> <type>: <title>`, what / why / needed by, status).
The kit is built to `S:ap/ap_fx_api.md` §0 without a change; §1-§14 there describe what was built. Nothing here blocks
another stage.

## RFX-1 note: `hud/heart_bar` added (FN-24 fallback) — for AP-CORE

- what: a new kit function `AP:fx/hud/heart_bar` (no args) and `K.heart_bar(v)`: it writes `rlk:apkit hud.hbar` = a text
  component of 20 gold / dim cells with caps (glyphs U+E930-E933 in `rlk:mboss_ap`) from `#apHt mb` (0..10000). The core
  appends `{nbt:"hud.hbar",storage:"rlk:apkit",interpret:true}` to its boss-bar line and calls the function whenever
  `#apHt` changes. Api doc §9.3.
- why: ap_fx_api.md §0.9 puts the Heart progress bar on the framework bossui (`#buHpCol`, `#buNoNum`, FN-24); if FN-24
  lands without those options the bar needs another source. No §0 name changed.
- needed by: AP-CORE (only if FN-24 lacks the options). status: done (kit side).

## RFX-2 note: `#apHt` drives two kit outputs — for AP-CORE / AP-REV

- what: `snd/heart_gain` picks its chime pitch from `#apHt mb` (11 steps, a semitone apart, an octave up at 10000) and
  `hud/heart_bar` reads it too. Keep `#apHt` (0..10000, objective `mb`) current before calling either.
- needed by: AP-CORE, AP-REV. status: open (informational).

## RFX-3 note: dome markers and the flood — for AP-ORG / AP-REV

- what: `p/flood` skips each 7.5 b flood cell whose **centre** is within 7.5 b of a live `rlk_mb_ap_dome` entity
  (3D distance from the cell centre at the executor's y). Summon the dome markers at the floor (y 201, within ≈ 2 b) or
  the skip test misses them. With 3 domes 34 of the 44 cells are drawn (`ap_dress_flood.png`).
- why: the skip is evaluated per cell, so the flood tiles can overlap a dome's rim by up to ≈ 0.75 b (cell side) / 2.3 b
  (cell corner): deliberately conservative (a tile may look dangerous inside the safe radius, but no unflooded floor is
  ever shown outside it). Safety itself is the framework's `rlk_mb_hzsafe` group, not the tiles. `K.DOME_SKIP` is the
  one knob if the org stage prefers a wider hole.
- needed by: AP-ORG (dome marker placement), AP-REV (Q2 t156). status: open (informational).

## RFX-4 note: telegraph budget edges — for AP-P1 / AP-P3

- what: (a) P5: swing 1's last wedge holds its 3 t (`hold` default) and overlaps swing 2's stack at t39 for one tick
  (18 telegraph cards; per swing 16 as §0.11 budgets). Pass `hold=0` on the last wedge of swing 1, or stack swing 2 one
  tick later, if a strict 16 matters. (b) Q5: the two leaf-blade lanes (t52, 5 cards each) overlap volley B's landing
  discs (strike t55, 24 cards) for t53-54: 34 telegraph cards. Telegraph calls are **skipped from 34 live cards**, so a
  further decal in those two ticks (e.g. an organism cone) would not draw. Draw order matters: call the lanes before any
  extra decal, or delay it past t58. (c) Budget any shape with `K.sector_cards(r, a)` / `K.piece_geometry(F, r)`: a sector
  at r ≤ 3.5 b of ≤ 64° is 2 cards, above that 2n + 2 with n = ⌈2a / 32°⌉ (64° at r ≤ 3.5).
- needed by: AP-P1 (P5, P6), AP-P3 (Q4, Q5), AP-ORG (O1, O6b). status: open (informational).

## RFX-5 note: homing wheel props — for AP-P1

- what: `prop/thorn_wheel_homing` dresses a module display (Ø 2.05, camera-facing); run `p/homing_trail` **as that
  display** every 2 t: it leaves the gold-orange dust and turns the wheel a quarter turn (`prop/e/spin`; nothing happens
  when `@s` is not an item_display). Keep `teleport_duration:1` on the display while the module moves it.
- needed by: AP-P1 (P3 homing `pj`). status: open (informational).

## RFX-6 note: the kit's pack needs the fg kit's sprites — for AP-I1

- what: 13 kinds reference `rlk:mboss/fg_kit/*` (glow, glint, mote, streak, ripple, spark, smoke and the fg telegraph
  rims / fills / bars / lane). `build_mboss_ap_fx.py --resourcepack` refuses to write unless those sprites exist with the
  fg kit's sizes and are in the item atlas, so in the generator order the fg kit's pack build comes first (as in
  `rp_final9`). The kit adds 77 atlas entries and the `mboss_ap` font; nothing else in the pack changes
  (`S:ap/fxtests/run_kit.sh` step `rp_scope`).
- needed by: AP-I1 (generator order, release pack). status: open (informational).

## RI1-1 request (AP-I1, for I2 / a kit fixer): outline-only *keep* decals and a small O1 hit preset

- what: a no-fill variant of `tele/disc` (the pale rim / outline only, no progress fill toward the hit) for the *keep* rows
  Q1 burst (leaf ring), Q3 shell 1 and Q3s (the pale target disc, held to the impact) and P1's shadow marker, and a
  no-lane-fill variant of `tele/crack` for P2's strips (plan §14 10-20 table, `ap_fx_api` §15; user rule: a floor
  telegraph only where the footage shows one, outline-like, sized to the hazard). P4's disc keeps its 23-t fill (the
  footage fills it). Plus a small impact preset for O1 (the basic organism's melee cone has no impact visual).
- why: §15 of `ap_fx_api.md` lists it as the one kit change the rule needs; it was never filed. Azhdaha's I2 served the
  same request (outline-only keep telegraphs).
- how the pattern stages proceed meanwhile: call the decal through `Gen.decal('keep', K.tele_disc(...))` /
  `K.tele_crack(...)` as today and mark the row's `tele: 'keep'` in `TABLE`; I2 switches those calls to the outline form
  (a keyword on the Python builder, e.g. `fill=False`, so the pattern code changes by one argument).
- needed by: AP-P1 (P1 marker, P2 strips), AP-P3 (Q1, Q3 L1, Q3s), AP-REV (O1 hit fx). status: open.

## AP-I2 status (2026-10-21, `wip/ap` f588262)

- RI1-1: done f588262: `tele/disc_o`, `tele/crack_o` (`fill=0` on `K.tele_disc` / `K.tele_crack`) and the preset `o1_hit`
  (ap_fx_api §16). Also `p/flood_part` (ap-p3.md RP3-3).
