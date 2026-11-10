# Lane B (균형치 · 그로기) — progress

Branch `wip/combat-bal` (from `origin/wip/combat` 6ff826f), worktree `<scratchpad>/cb/wt_b`.

## Steps
- [x] B1 core `bal/**` (generator `tools/build_balance.py`), tiers, regen, sources (burst / reactions), groggy state, head row,
      vanilla + cm families (cm/tick, frz_end guard, rig groggy branches in the ch1 .mjs / ch2 / ch3 generators), boss
      framework (core: fight_tick -> fight_bal, bars #buPip, registry flag `bal`, dispatchers `d/bal_*`, check_mboss_pack
      rule; mboss_lib.BAL_HOOKS), boss bar row (`build_bossbar.py` option `#buPip`), Raiden (rdSgStun 4 stun); suite
      `tools/dev/sim/bal/tests/test_bal.py` (115 checks). Gates: regen x2 identical, check_mboss_pack 0, loadcheck cb_b 0,
      test_bal 115/115, check_refs no new.
- [ ] B2 boss modules (adapters `bal_ok` / `bal_on` / `bal_tick` / `bal_off` + registry flags) + `test_bal_boss.py`
      (11 bosses in real fights) — built, waiting for the commit after B1 (backup `<scratchpad>/cb/b_mod/`)
- [ ] B3 gates on the full tree (run_all base vs lane B, ar/tests, hr suites), README, renders

## Log
- 11-10 start: baseline `regen_all.sh --mobs` clean (32 s). RP not in the container (no `rlk_hud_resourcepack*`).
- 11-10 video_notes landed (868775813): yellow filled, grey square slot when spent, left-aligned, deplete from the right
  -> glyphs: 7x7 / 5x5 diamonds, empty = 3x3 grey square, pitch glyph + 1 + 2.
