# S2-T requests (tail.py: 41-46 + AZ:xt/**), s2.md 13 / 18.6

## Rpt-1 core: phase-3 replacements never picked (P4 -> 45 / 46)
- what: ai.py builds the candidate weights only for a pattern's own phases. P4's phases are (1, 2), so #azC4 is 0 in
  phase 3 and ai/go never swaps in 45 / 46 (P5 -> P5b is unaffected: P5 runs in phase 3). Fix (ai.emit): wt() gives a
  pattern its weights in a phase outside its own phases when a replacement of it runs there; the no-immediate-repeat line
  also blocks #azC4 after 45 / 46 (#azLast holds the replacement id after ai/go).
- why: plan 4.12 "Phase 3: 4 -> 45 / 46 with the same weights"; s2.md 2.1 `replaces 4`.
- needed by: every phase-3 fight; pat_tail.py static check "P4's weights reach phase 3".
- in branch: REQ pt-1 in tools/mboss_azhdaha/ai.py (wt() + the no-repeat block), wip/az-pt.
- status: open

## Rpt-2 core: an api.after target that schedules again loses its timer
- what: aft/run_k frees slot k, runs the target, then kills @e[tag=rlk_az_aft<k>]. A target that calls g.after again (a
  per-tick chain) is given the freed slot k, and its new marker is killed right after it returns: the timer fires with
  no marker, so the target never runs. Fix (core.after): re-tag the due marker rlk_az_aftrun before the target runs and
  kill that tag afterwards.
- why: per-tick chains in addon bodies (the Cryo frost-ring growth 1.5 -> 6 b at 0.75 b/t, plan 4.6; the whip/end arcs);
  any S2 author chaining after().
- needed by: xt/cring/step, xt/whip_end/arc; pat_tail.py "the front grows 1.5 -> 6 b" (4 points).
- in branch: REQ pt-2 in tools/mboss_azhdaha/core.py after() (aft/run_k), wip/az-pt. test_azhdaha's addon / after
  checks stay green with it.
- status: open

## Rpt-3 kit: an outline-only option for the seal telegraphs (heptagram, starseal, hexagram)
- filed in requests/fx.md (Rpt-3), the seal counterpart of Rpa-2 (tele/disc).

## Note (no request): Gen.wave's front preset
- = Rpa-1 / Rps-1 (Gen.wave hands K.fxe('front') tenths, the kit converts again). S2-T does not use g.wave (the Cryo
  rings are addon bodies with their own growth chain and call K.fxe('front', 4, ...) in blocks).

## Note (no request): 42's safe circles for the orbit rule of 31
- 42's safe circles are markers `rlk_mb_hzsafe rlk_mb_az_p42s` (mbS = the rim id, mbHzSG = the round's mask), alive
  from the markers (round - 48) to the strike + 1. Plan 5 31 "during a 42 marker window an orb that would cross a safe
  circle rides high over it" belongs to orb/step (core / S2-L) and can test them.

## Note (harness, no change made): gen_check_az's fixed scratch dir races between concurrent gates
- tests_mod/gen_check_az.py always uses `az/tests_mod/tmp_gen`; two stage gates in group 2 at the same time (S2-A `i1pa`
  and S2-T `i1pt`, 20:21) wiped each other's copy (pt: FileNotFoundError in rmtree; pa: ModuleNotFoundError geo_b).
  S2-T re-ran that one step alone afterwards: 6/6 ok. A per-tag dir (`tmp_gen_<pid>` or the tag) would avoid it.

**I2 status (2940a23 on wip/az).** pt-1 merged with pa-3 (ai.py swap_in rule; out-of-phase weights kept). pt-2 kept (core.after re-tag). Rpt-3 served (41 heptagram_o, 45 starseal_o, 46 hexagram_o with resume redraws).
