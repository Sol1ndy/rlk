# Requests and notes from stage SR (reward item 화무십일홍 + buff 월하대작), branch `wip/hr-sr`

SR changed only its own hand files (contract §1 SR row). Nothing here asks another stage to change its files before I1;
items 1-3 are for the lead at I1, 4-6 are facts S3 / S2a / S1K rely on, 7-9 are deviations from PLAN §7.4 / §7.5 to log
in contract §7.

## For the lead (I1)

1. **README**: merge `HR/sr/readme_items.md` (등급 규칙 exception under README:858 = PLAN §7.4.1 verbatim, the item
   bullet after README:888, the 조절 지점 row `#hrMoonAtk / #hrMoonCrit / #hrMoonSpd`, the two rows for her section, the
   suite list). Move `HR/tests/test_hwamu.py`, `test_moon.py` and `HR/sr/srsim.py` (+ `render_sr.py`) to
   `tools/dev/sim/hr/{tests,sr}/` (the suites find the helpers at `HERE.parent / 'sr'`, the plan at `HERE.parent /
   'PLAN.md'` and the wiki text at `HERE.parent / 'wiki/w2.txt'` — keep that layout or adjust the three paths).
2. **vBig outside F5 (pre-existing, not SR's file)**: `vBig` is decremented only in `view/ride_tick:13` (F5) and
   `view/sel_xhair:3`, but set in every view mode (room titles 70, gates 66, rewards 72, …). In first person and the
   shoulder view it therefore stays ≥ 1 after the first big title of a run, so the 홍련일섬 edge vignette — skipped while
   `vBig ≥ 1` as PLAN §7.4.5 / the brief require — shows only in F5 (the default view). The cue is optional; if the
   lead wants it in every view, decrement `vBig` once per tick for all players (e.g. in `player/tick`), a `view/` or
   `player/` change outside SR's files. Default: leave as is.
3. **Per-tick budget of `test_m0diff` (known failure, README 0-9)**: the PLAN §7.4.6 lines in `player/take_damage` and
   `player/dash_iframe` cost one command per hit taken when the sword is not held; in `run_all` the three already-failing
   budget figures move by +0.01 / +0.01 / +0.02 commands per tick (force 2 +6.70 → +6.71, force 3 +6.98 → +6.99,
   force 99 +6.57 → +6.59; same 12 failing checks as the D0 base). Nothing to do unless the budget question is settled.

## Facts other stages rely on

4. **S3 (`ev/item`, `ev/buff`, `reward`)** — the exact calls SR's files expect, all as the player (`@s` = the player):
   - raise the star first: `function rlk:items/enh_add {id:"sword_hwamu"}` (0 → 1 = ★☆☆; `enh_add` prints the ★★★ line
     only on the step 2 → 3, so this prints nothing), then
   - capacity check exactly as `F:root/give:4-5`: `execute store result score #ol tmp run data get storage rlk:pinv
     order` and `#ol tmp < @s invCap` → `function rlk:items/give {id:"sword_hwamu"}`; otherwise never `give` (a full
     inventory silently loses it) but `execute at @e[tag=rlk_body,limit=1] run function rlk:items/drop
     {id:"sword_hwamu"}` (SR relies on this check being done by the caller: `items/give` itself does not check).
   - buff: `scoreboard players set @s hrMoon 1` (objective created by SR's `load`); `items/stat_light` applies it within
     2 t, the ◆ 스탯 정보 line appears at the next `player/update_item` (hrMoon is in its change hash).
   - the duplicate rule (PLAN §7.3.1) can read `@s it_sword_hwamu` and `@s hrMoon` as is.
5. **S2a / RP**: the def names `model:"rlk:mboss/scarlet/item_sword"` (`api.ITEM_MODEL`), and `items/give_macro` writes
   it as `minecraft:item_model`. Without that item model in the resource pack the client draws the missing-model cube,
   not the vanilla iron sword (PLAN §7.4.1 says "without it the vanilla sword shows" — not how `give_macro` works). It is
   S2a's RP tree (`RP:items/mboss/scarlet/item_sword.json`), so the RP must ship with the datapack (as for every boss).
6. **S1K**: SR titles the glyph U+EC16 (`api.VIG`) in font `rlk:mboss_hr` (`items/proc/hw_slash_q`): root `{text:""}`
   unstyled, `font` + `shadow_color:0` on the component, `title @s times 0 4 2` (6 t), then `vBig 6`; skipped while
   `vBig ≥ 1` (the brief) and also while `ttlT ≥ 1` (a typed boss line or a subtitle notice is up: a new title would
   reset the title timing and cut that line after 6 t). The glyph has to be edge-only with a clear centre at whatever
   advance S1K gives it.

## Deviations from PLAN §7.4 / §7.5 (for contract §7)

7. **Timers as game-time deadlines** (to meet the brief's ≤ ≈ 12 commands per tick while held; countdowns measured 24
   in a fight): `items/proc/hw_tick` only decrements `#hwWait` (ticks to the next due time) and runs `hw_due` at 0, which
   reads `time query gametime` (pack precedent: `combat/do_swing`) and handles the due deadlines `#hwTEnd` (stacks),
   `#hwCtrEnd`, `#hwSlAt`, `#hwSparkAt` / `#hwCritEnd`, `#hwSlEnd`. `#hwCtrCd` / `#hwSlCd` are 1-while-cooling flags, so
   the PLAN §7.4.6 hook lines are byte-identical. Measured (test_hwamu `perf`, strict count = an `execute … run` counts
   its sub-command): idle 9.0, long fight with HP under 60 % 11.5 per tick; one-off strikes apart (counter 181-259
   commands with the real `combat/apply`, 홍련일섬 ≈ 190 per target). Extra helper files beside the 12 PLAN names (all in
   SR's `F:items/**`): `hw_due`, `hw_stk_end`, `hw_low`, `hw_pulse`, `hw_ctr_fx`, `hw_crit` (`hw_ready` = the ready cue +
   flag release; no `#hwT` / `#hwSlQ` countdowns).
8. **items.md numbers**: PLAN §7.4.4's items.md block writes `6.0초`, `2.0초`, `10.0초`; the tune engine prints a zero
   fraction as an integer (`items/tune/fmt`, as for every item: 불씨의 맹약 shows `12초`), so the mirror says `6초`, `2초`,
   `10초` (test_hwamu checks items.md = the in-game text built by `items/build_display` at ★★★).
9. **Small decisions PLAN leaves open**: `hw_clear` (sold / dropped) clears stacks, hit count, queues, crit time and the
   sidebar but keeps both cooldowns (absolute end times, so they keep running while not held; dropping and picking the
   sword up cannot reset the 40-s 홍련일섬 ICD); the 홍련일섬 ICD is spent at the cast even with no enemy within 20 b (the
   burst happened); the counter cooldown starts only when a target was hit (PLAN). The stat-item line when the buff is
   off is the empty text PLAN §7.5.2 names (one blank last line), and the on-line is
   `{translate:"rlk.hr_moon",fallback:"☾ 월하대작 · 최종 공격력 +%s%% · …",with:[atk,crit,spd]}` so its numbers always
   equal the `load` constants (no item modifier, no string building): please check in game that the fallback renders
   (`%s` = the numbers, `%%` = %).

10. **Gate run notes**: `run_all.sh` was run from SR's copy `HR/sr/sim` (S unchanged so the old-path M0 suites ran: all
    23 pass; the vcheck baselines `lint.txt` / `macro.txt` copied from `S:az/tests_cm/baseline`). Failures = README 0-9's
    list (m0diff's 12 checks as the D0 base, px 4e (18), ident's 10) + `gen_check` 9 in that run only, caused by SR
    editing `items/proc/hw_slash_q` in place while gen_check's variant tree was hard-linked to the worktree; gen_check
    re-run alone: GENERATOR CHECKS PASSED. The run's validator steps compare with the pre-apep `az` baselines (hundreds
    of other bosses' lines "new"); the authoritative checker gate is `HR/tools/checkers.sh` vs 35b82e5: SR's lines are
    the known kinds only (`with storage` macro calls, `time query gametime`, Korean sidebar names, `scoreboard players
    display`, line shifts in `player/update_item`).

## In-game checks for the release note (no bot client on 26.3)

- `/function rlk:items/give {id:"sword_hwamu"}` with the RP: icon, dark_red name, the tooltip (= `HR/renders/sr_tooltip.txt`).
- 4 basic hits → `육참골단` 1 in the sidebar, HP bar −4 %; a hit taken / a dash through an attack → the lilac counter
  slash; a burst → the vignette (F5) and the slash 4 t later on everything within 20 b.
- `/scoreboard players set @s hrMoon 1` → ATK / 치명타 확률 / 이동 속도 rows raised and the ☾ line at the bottom of ◆ 스탯 정보
  (= `HR/renders/sr_stat_item.txt`).
