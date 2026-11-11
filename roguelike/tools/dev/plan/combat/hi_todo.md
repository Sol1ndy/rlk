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
