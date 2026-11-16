# Requests of S2-A (geo_a: P1 chin, P2 jump, P3 charge, P4 spikes), branch wip/az-pa

## Rpa-1 api: Gen.wave hands the kit front preset tenths, the kit converts again (a 10x front)
- what: `api.Gen.wave` calls `self.fxe('front', el, r0=int(r0 * 10), r1=int(r1 * 10), w=int(band * 10), dur=n)`, but
  `K.fxe` takes blocks and converts to tenths itself (`build_mboss_az_fx._parg` -> `_t`), so the travelling front preset
  of every N10 front (P2, P5, P5b, T1, the Cryo rings) is drawn 10x too large (P2: `{r0:300,r1:1050,w:250}` = 30 -> 105 b).
  Fix: pass blocks (`r0=r0, r1=r1, w=band`). The kit's own demo calls it with blocks (`fxe('front', G, r0=3.0, r1=10.5, ...)`).
- why: Change note 1 makes the travelling front the hazard's own visual (no decal), so it must match the hazard.
- needed by: P2 landing / wave-2 fronts (t20 / t31); pat_geo_a.py p2 "the front preset in tenths r0 30 -> r1 105, w 25".
- applied on wip/az-pa as the smallest change, marked `# REQ pa-1` in api.py (one call line); the integrator keeps one
  copy at I2a (S2-B / S2-S / S2-T fronts get the same fix).
- status: open (local fix on wip/az-pa)
- kit side: see requests/fx.md Rpa-2 (outline-only tele/disc for the P4 landing rings)

## Rpa-3 core (ai.py): a phase-3 P5b (10) repeats right after a P5b
- what: in phase 3 a fore-paw P5 is replaced by 10 in `ai/go` after the pick; `#azLast` then holds 10, so P5's own repeat
  rule (azLast 5) never blocks it and the next fore-paw P5 pick becomes 10 again: 10 -> 10. test_azhdaha `ai` ("no
  immediate repeat except P2 and P5") caught it on wip/az-pa once the real P1-P4 changed the pick sequence
  ((3, 1038, 10), (3, 1143, 10)). Fix: zero P5's candidate weight when `#azLast 10`, phase 3 and the nearest paw is a fore
  paw (one line in ai/cand).
- applied on wip/az-pa as the smallest additive change, marked `# REQ pa-3` in ai.py; the integrator keeps it or replaces it at I2a.
  With it test_azhdaha `ai` is 18 checks, 0 failures on wip/az-pa (6dcf7f3).
- status: open (local fix on wip/az-pa)

## Rpa-4 test (tests_mod, S1-MOD): test_azhdaha trans "transition 2 with live orbs: no new cast" is timing-bound
- what: the check asserts no `cast/leg` over the whole 1300-t window after the floor hit, which also covers the start of
  phase 3; there the AI may legally pick the leg special again once the refreshed orbs ended and the 600-t cooldown ran
  out (on wip/az-pa pair 1: refresh t663, P2 1800-1853, cast host 30 picked at t1869 = after the B3). Ask: limit the
  "no new cast" assertion to the transition (until `#azTr` returns to 0 after the B3 frame, or to the cast host of
  transition 2 itself). Nothing in geo_a can or should change this; it fails only because real P1-P4 move the player
  (knockback) and shift the pick sequence.
- status: open (blocks a green tests_mod `trans` step on wip/az-pa; not edited, shared harness)

## Rpa-5 test (shared M0 harness): mb/int_tests test_guardian "rotation: every normal pattern ran" is random
- what: mcsim's `random value` uses Python's unseeded `random`, so over 5200 t the Guardian may never pick P3 (melee band
  only). It failed in the S2-A gate run (tag pa: normals [1, 2, 4, 5]) and once more by hand, then passed 3 of 3 reruns on
  the same tree; F:mboss/guardian/** is byte-identical to 22ba247 (ident 1). Ask: seed mcsim's RNG in the test (or
  retry the rotation sample). Nothing on wip/az-pa touches the Guardian.
- also: tests_mod gen_check_az uses one fixed scratch dir (tests_mod/tmp_gen); gates of several stages running at once
  delete each other's copy (pa gate: "No module named mboss_azhdaha.geo_b"). Rerun alone on wip/az-pa: 0 failures.
- status: open (not edited, shared harness)

**I2 status (2940a23 on wip/az).** pa-1 served once with ps-1 (api.Gen.wave); pa-3 merged with pt-1 in ai.py (swap_in rule). Rpa-2 served (tele/disc_o for P4 landing rings + resume redraw). Rpa-4 (trans no-new-cast window = transition only) and Rpa-5 (mcsim seeds random at import) fixed in the harness.
