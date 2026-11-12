# Review H-A (홍련, the fight) — lead rulings (11-11). Findings: `findings_HA.json` (head d7da75e79). Fix lane: `wip/combat-hfa`.

| id | ruling |
|---|---|
| HA-01 | Fix: the forced rings → ult chain checks `#fl` like mx's repeat; a floor reached during the rings ends the pattern and the step starts (no ult). Test at 60 % and 5 %. |
| HA-02 | Fix: `#ctr`, `#flq`, `#a6q` (and anything else that queues a reaction "while she recovers") are cleared at `bal_on` and `bal_off`, and hits during the groggy do not count toward them; after the groggy the 12-t recovery runs first. Test with hits and a skill hit in the last 60 t. |
| HA-03 | Fix: re-time the gauntlet cuts so no blind metronome clears them: for every period 8-30 t and every phase, a press train gets at most 3 perfect parries in G1 and at most 3 in G2 (5 are needed). Keep every gap ≥ 14 t, the judge ticks and the cut counts, the clips and their events where possible (the reappear / glide beats may shift a few ticks), the cue at each lock. Add the check to the suites (real F functions, all periods and phases). Lane HB adds metronome agents to hrfair T7. |
| HA-04 | Fix: after `/reload` (or a resume) during a groggy she is in the `down` loop at once, then the kip-up at 20 left. |
| HA-05 | Fix: `bal_ok` refuses a4's second airborne span (29-37) too; check every pattern's airborne ticks against `bal_ok` with a test that reads the rig's root height, so no break teleports her down. |
| HA-06 | Fix: the parry cue must sound clearly unlike the purple flash: a different vanilla sound family (not amethyst). Keep it short and light. |
| HA-07 | Fix: the cue sparkle must read at F5 distance: ≥ 1.0 b on screen, a colour that stands out on the crimson P2 field (white-gold core), still clearly different from the yellow / purple / blue flashes. Render it at her blade in P1 and P2 and look. |
| HA-08 | Fix: q's grab has no knockback (kb 0); the throw is a pose, not a push; only the last hit of the q chain (the pillar) knocks back. |
| HA-09 | Fix: a forced rings starts only in the near band; from mid she glides in first (the far rule's close), then the rings. No cue for a ring that cannot reach the player? — keep the cues (one rule: every parryable hit has its cue) but make the rings reach: she steps toward the player as designed until h − 7. |
| HA-10 | hrsim's F-lock model and hrfair T7: lane HB. `test_flow.py:171`: the P1 parry check must count unparried hits too (fix lane). |
| HA-11 | Fix README 573 / 920 (the unparriable set of the rebuilt kit, by pattern). |
