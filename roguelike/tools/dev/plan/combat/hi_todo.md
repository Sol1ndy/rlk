# HI (홍련 integration) — open items collected from the lane reports (lead, 11-11)

Lanes done: H1 `wip/combat-hr1` c1e53b116 · H1c `wip/combat-hr1c` 14470c79c · H2 `wip/combat-hr2` 8ab741163 · H3 `wip/combat-hr3`
0c762626b (H2 already merged H1 + H3) · H2c running. Merge order: H1 → H1c → H2 → H2c → H3; generated output regenerated, never merged by hand.
The 11-11 release (전투 개편, stamp c9eed47) is on the release branch; HI starts from `wip/combat` aec999f05 + the lanes.

## From the reports
1. kcut's big yellow tell: H1 passes `yellow_tell {t:10}`; H1c's kit reads t >= 100 as the Ø 2.0 tell for t − 100 ticks → `{t:110}`.
2. `rings` in P1 (4 rings) plays to tick 54 while the clip's fifth turn starts at 49: switch to the stance at clip tick 49 in P1.
3. test_kit's 8 failures: the old judge drew the deflect starburst / column a second time for first person; first person is gone
   (dev mode only) → drop those pins (or draw the dev-mode form), decide at HI.
4. gen_check_hr: a stray file in `p/r1/` (H1 removed r1 by hand; the generator owns current keys only) — delete it.
5. test_rig: the cinematic rows (`sq1`, `lead_down`, `lead_stand`), the intro seat, the dump covering 56 / 59, the skin source
   missing in the container; its cinematic section crashes → rebase after H2c.
6. README: the 홍련 section (2247-2339 and around) rewritten for the rebuild; lines citing the old `ev_dry` counts (≈ 421 / 2600 /
   2612); README 0-4 and the pack README: the player rig build also builds the actor (H3); the new generators / suites in 0-8.
7. hrfair 2.0 (H1, column B): T9 Lv10 191 s (≤ 185), T9b 184 s (125-170), T10 1.50 groggies / min (0.8-1.3), T11 walker 2.06 U / min
   (0.8-1.5) miss. T1 / T2 have no 타키 baseline in this tool (use T3). T6 σ1 / T12 are unattainable with a 3-t window and a 1-t
   error (max ≈ 86.6 %): restate those targets. Knobs in hr_design §6.4 (a3 weight → a3s, `GAUGE['hit']`, the groggy's pay-off).
8. Things only the user can check in the game (collect for the final reply): lane reports H1 / H1c / H2 / H3 "only a person in the game".

## From H2c (done: `wip/combat-hr2c` 2fdfa2405; merged H1 + wip/combat b327762e5, not H2 / H1c)
9. Intro 1290-1296 (shot I18): her low brim passes 0.13 b in front of the lens → lower the eye or start the shot a few ticks later.
10. test_rig's cinematic rows (states, hand-overs, big-swing spans, the intro stone check) still use the 11-06 events: replace with
    `test_cine.py`'s §4.1 versions. test_kit's sound-count pin (104 → H1's additions).
11. Small, reported: hat switch jumps 0.19-0.20 b at repel 84 / 139; the brim 1.7 mm into the head's corner at cs1 236; the sheathed
    hilt 1-2 cm off the scabbard pivot at intro 787-788; the lying fist 0.046 b off its target (limit 0.04) in the hat pick-up.
12. H2's white overlay stand-in for the deflect becomes the `gold` glyph now that H2c's kit block exists (check after the merge).
