# S2-L requests (leg.py: 31 / 32 / 33 + AZ:xl/**), s2.md 13 / 18.6

## Rpl-1 core: the addon dispatchers stop after a leg body (phase-3 tail bodies of the same point never run)
- what: core.addons() writes the leg lines of `AZ:x/<point>` as `... run return run function .../xl/<point>/<el>`, and
  the tail lines come after them. In phase 3 a point with both a leg and a tail body (chin/impact, jump/land,
  jump/wave2, stomp/w1, stomp/w3, stomp3/s1, stomp3/s3) runs only the leg body: e.g. Pyro + Electro chin slam gets the
  lumps but never the bolt discs; Hydro + Cryo stomp gets the blades but never the frost ring. Fix: drop `return` on the
  leg lines (plain `run function`), as the tail lines already are.
- why: plan 4.5 "Phase 3: ... The leg rule continues" + 4.6 (both columns); s2.md 10.1.
- needed by: every phase-3 addon point with a leg body (S2-T's xt bodies; test_az_flow "the addons per pair and phase").
- not in branch (S2-L is not blocked: pat_leg.py calls the leg bodies through the dispatcher in phase 2).
- status: open

## Rpl-2 core (info): orb/step's high band
- what: `AZ:orb/step` sets only `mbHzY0 2600` while `#azOrbHigh 1` and never restores it (nor sets `mbHzY1`); with the
  normal band 0-2200 that makes the orb harmless rather than "riding at 2.6-4.6", and permanently so after the
  transition. leg.py's `p/orbs/band` (run right after `g.orbit_tick` in 31's bgtick) now owns the band every tick (0 /
  normal 0-2.2, 1 / high 2.6-4.6: transitions + cine, the head-lane eye, over a 42 safe circle, 2 / off: growing /
  fading), so nothing is broken; the core line is redundant and could go (or set both values) at I2a.
- status: open (no change needed for S2-L)

## Rpl-3 kit: outline-only telegraphs for the two S2-L keep rows
- = Rpa-2 (tele/disc; the P1 Hydro geyser swirl r 3.0, tell 22: `xl/chin_impact/hydro_at`) and Rpt-3 (seal8; 32's big
  seal r 5.2, tell 28: `p/meteor/big_hz`), both in requests/fx.md. Until served both are called with the hazard's own
  tell (the fill reaches the rim on the hit), which pat_leg.py accepts (decal = hazard).
- status: open (tracked as Rpa-2 / Rpt-3)

## Note (no request): 33's ambience chain needs Rpt-2
- `p/firefield/amb` re-arms itself every 10 t through `g.after` while any fire field lives (flames over each field with
  the kit `p/fire_field`, the `fire_loop` sound every 20 t). Rpt-2 (S2-T: an after() target that schedules again loses
  its timer) stops that chain after its first run on wip/az; it restarts with the next fire field (`amb_on`, stale
  check). Nothing else depends on it; once Rpt-2 is served the ambience runs continuously.

## Note (no request): P2 Pyro burst with the lump field
- Plan 5 P2 checks "burst <= 2.8 (Pyro: 1.1 + 1.1 + 0.6)". The lumps land at t58 (37 t after the landing at t21) and
  each leaves a fire field whose first tick (fire 0.2, the family group) comes at the landing tick, so the strict rule-2
  sum on a player standing on the landing spot through t21-t60 is 1.1 + 1.1 + 0.6 + 0.2 = 3.0 > 2.9. No tick, size or
  coefficient was changed (S2-L may not); for S2-A's P2 check / the balance fixer.

## Rpl-4 tests (tests_mod/test_azhdaha.py t_brand): the DoT measurement now includes rule 33's fire field
- what: t_brand brands the player with a direct Pyro strike in phase 2 (pair 0, Pyro legs) and then measures the HP lost
  over 21 t as "a DoT tick = 3 % max HP". With the real rule 33 (S2-L `p/firefield/on_brand`, plan 4.7) that strike
  also makes a fire-rule field r 4.5 / 160 t under the player (the punishment for standing in it; exempt from the clear
  melee points), so the standing player takes the field tick too: lost 10 instead of 4 on wip/az-pl. S1-MOD's stub only
  counted the calls (#aq33N), so the test never saw a field. Suggested fix (one line, test only): run
  `function rlk:mboss/azhdaha/fld/clear` (or move the player 6 b away) right after the Pyro brands and before
  `hp0 = ...`; or read the DoT from `#mbDotDmg`. Every other t_brand check passes unchanged.
- why: plan 4.7 / s2.md 9 rule 33 is implemented as specified; the test predates it.
- needed by: tests_mod run_all (step test_azhdaha_brand_shard_field_bg) on any tree with leg.py; the full gate of S2-L.
- not in branch (S2-L may not edit tests_mod). Full gate pl (82db4ce): this is the only test_azhdaha failure
  (`a DoT tick = 3 % max HP (pl_dot)  [(10, 148)]`, 46 of 47 checks pass).
- status: open

## Rpl-5 harness (tests_mod/gen_check_az.py): the scratch copy is one fixed path for every tag
- what: gen_check_az copies the tree to `S:az/tests_mod/tmp_gen` (rmtree first, rmtree in `finally`) whatever the tag, so
  two gates running at the same time (any two stages) wipe or overwrite each other's copy. The S2-L full gate (tag pl,
  20:36-20:50) overlapped AZ-R3b's tests_mod run (tag r3b_dev, gen_check_az at 20:50) and failed 4b / 4c on a foreign
  path `tools/raiden_obj_cards.py` that no az generator writes. Re-run alone on the same tree (82db4ce): 0 failures.
  Fix (one line): use `tempfile.mkdtemp(dir=S/az/tests_mod)` or `tmp_gen_<pid>`.
- needed by: every stage's full gate while stages run in parallel.
- status: open (not in branch; S2-L may not edit the harness)

**I2 status (2940a23 on wip/az).** Rpl-1 served (core.addons leg lines without return; phase-3 tail body runs after the leg body). Rpl-2 served (core orb/step high-band line removed). Rpl-3 served (Hydro geyser disc_o, 32 seal8_o). Rpl-4 (t_brand clears rule-33 field before DoT) and Rpl-5 (gen_check_az mkdtemp per run) fixed in the harness. Perf: the three Pyro lumps of a volley land one tick apart; orb ribbons alternate parity.
