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
- [ ] B2 (commit 2): boss module adapters (`bal_ok` / `bal_on` / `bal_tick` / `bal_off`) + registry flag `bal` on all 11
      entries, own groggies call `bal/refill`; cost refactor (no extra command per boss fight tick: the boss clock in the
      existing mob/tick line, paused with the fight; groggy routing as `unless score @s grgT matches 1..` on the d/tick lines
      + a last `d/bal_tick` line; the boss row = second component of the bossui bossbar name, `brow` starts with a -200 px
      space, so `bossui/draw` / `build_bossbar.py` are back to the base); README; render `<scratchpad>/cb/b_balance_ui.jpg`.
      Gates so far: regen x2 identical, check_mboss_pack 0, check_refs no new, loadcheck cb_b 0, test_bal 116/116,
      test_bal_boss 129/129, az/tests_cm run_all = the baseline's step statuses (m0diff: same 40 failures, force 1 +6.48 < 6.5;
      the others +0.5/t over their base; C draw unchanged), RP: `rp_b` = rp_base + 9 new files (font/bal.json, 8 PNGs),
      rplint 0, atlas 12.919 M unchanged, RP hash twice b04a12f6…. Running: hr suites base vs B, ar/tests base vs B.
- Sim copies with rewritten paths: `cb/b_sim` (base runs + az run_all), `cb/b_sim2` (lane B hr / ar runs); base tree `cb/b_base`.

## Log
- 11-10 start: baseline `regen_all.sh --mobs` clean (32 s). RP not in the container (no `rlk_hud_resourcepack*`).
- 11-10 video_notes landed (868775813): yellow filled, grey square slot when spent, left-aligned, deplete from the right
  -> glyphs: 7x7 / 5x5 diamonds, empty = 3x3 grey square, pitch glyph + 1 + 2.
- 11-10 RP available (`scratchpad/rp_base`, release b3df6a5f…): copy `scratchpad/rp_b` built with `build_balance.py --resourcepack`.
