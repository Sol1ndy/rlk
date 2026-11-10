# Lane B (균형치 · 그로기) — progress

Branch `wip/combat-bal` (from `origin/wip/combat` 6ff826f), worktree `<scratchpad>/cb/wt_b`.

## Steps
- [x] B1 core `bal/**` (generator `tools/build_balance.py`), tiers, regen, sources (burst / reactions), groggy state, head row,
      vanilla + cm families (cm/tick, frz_end guard, rig groggy branches in the ch1 .mjs / ch2 / ch3 generators), boss
      framework (core: fight_tick -> fight_bal, bars #buPip, registry flag `bal`, dispatchers `d/bal_*`, check_mboss_pack
      rule; mboss_lib.BAL_HOOKS), boss bar row (`build_bossbar.py` option `#buPip`), Raiden (rdSgStun 4 stun); suite
      `tools/dev/sim/bal/tests/test_bal.py` (115 checks). Gates: regen x2 identical, check_mboss_pack 0, loadcheck cb_b 0,
      test_bal 115/115, check_refs no new.
- [x] B1 committed 740b624 and pushed.
- [x] B2 committed b4bc206 (adapters for all 11 registry bosses, cost refactor, README).
- [x] Merged origin/wip/combat 4163e8f (lanes R + P) — 34c6dae, no conflicts; regen on the merged tree = no change.
- [x] B3 (commit 3): after the merge the m0diff budget showed +0.5/t over base2 (force 99 / 2 crossed 6.5): the damage path
      had 3 lines per strike (apply amp, apply sources, clear_atkflags reset). Now ONE line in combat/apply_mods
      (`if score @s balMax matches 1.. run function rlk:bal/mods`: groggy -> amp; else burst / reaction sources, not on a
      killing blow); `#burstDmg tmp` = the game time of the burst's damage calc (stale ticks ignored), cleared by
      char/after_hit; combat/apply and clear_atkflags are back to the base. ident_hr: group `combat overhaul B` (no gone files).
      Gates on this tree (all done): regen x2 identical, check_mboss_pack 0, check_refs no new vs base2, loadcheck cb_b 0,
      test_bal 117/117, test_bal_boss 129/129; az/tests_cm run_all = base2's step statuses; m0diff = base2's failures + one:
      A force 2 commands/tick +6.51 (budget 6.5; base2 6.31; the one apply_mods line per strike = +0.2/t; force 99 6.40 and
      force 1 5.75 pass; force 3 6.80 already failed in base2 at 6.61) -> README 0-9, lead's budget decision; 홍련 suites all
      pass (test_scarlet, pat_p1, pat_ghost, test_special_hr, test_reward, test_moon, test_hwamu, test_arena_hr, ident_hr
      with the B group, gen_check_hr 28/28 with an RP copy, test_kit, ev_dry; test_rig 160/161 = base2's: the user's skin
      file is not in the sim copy); lane R's test_rm passes; ar/tests test_cm_ar 65 / test_arena_fl 46 ok, test_kit needs the
      local branch wip/ar-s3 (same on the base; not created: no changes to the main checkout).
- Sim copies with rewritten paths: `cb/b_sim4` (base2 = origin/wip/combat 4163e8f, tree `cb/b_base2`), `cb/b_sim3` (lane B).

## Log
- 11-10 start: baseline `regen_all.sh --mobs` clean (32 s). RP not in the container (no `rlk_hud_resourcepack*`).
- 11-10 video_notes landed (868775813): yellow filled, grey square slot when spent, left-aligned, deplete from the right
  -> glyphs: 7x7 / 5x5 diamonds, empty = 3x3 grey square, pitch glyph + 1 + 2.
- 11-10 RP available (`scratchpad/rp_base`, release b3df6a5f…): copy `scratchpad/rp_b` built with `build_balance.py --resourcepack`.
