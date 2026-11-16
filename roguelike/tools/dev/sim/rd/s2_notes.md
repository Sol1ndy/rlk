# Raiden rework: M1 notes for S2-SHOGUN and S2-TENMA

S = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`. The binding plan is `S/rd/plan.md`
(§A.2-A.5, §B.2, §D.2 for your rows; §E for the stages). `S/rd/s0_notes.md` §3-§4 still describes the harness. This
file replaces the "where to work" part of s0_notes and adds the S2 contracts. Do not touch `/home/user/rlk`'s working
tree (another agent works there). Never push.

## 0. Binding rules (from the plan and the user; they apply to every commit)

- **R1.** A floor decal only where the footage shows one (§B.3 kinds). Every other hit is quiet. Cue to hit
  ≥ 12 t, or ≥ 20 t for big or undodgeable hits (area ≥ 100 b² or r ≥ 8, or `nododge`). Every hit shows a visible
  impact effect over its area.
- **R2.** No in-game advice. Allowed: instant-kill warnings and the prompts the real game shows (the two HUD
  messages in §D.2), pattern and form names, phase messages, numbers and voice lines.
- **R3.** Never emit a negative amount to `scoreboard players add/remove`. Never put a glyph font on the first
  element of a text list, unless that font falls back to `minecraft:default`. No rig part, prop or body below the
  floor. No teleport of a player or body into blocks or below the floor.
- **R4.** Raiden textures ≤ 3.0 M px (it is 2.70 M now, so about 0.30 M is left for both stages together).
- Vanilla sounds only. Every `playsound` id must be in `S/rd/tests/sound_ids.txt`; the static check enforces this.
- Generators in `roguelike/tools/`. Never hand-edit a generated output.
- **User decisions in force:**
  - 만겁 is the footage version: free camera and an arena-wide sweep. The camera lock and the judgment rig are gone.
  - 돌진 (18), 수천수만의 염원 (21) and the guard-recovery burst (9) ignore dash i-frames. Each has a warning of
    ≥ 20 t.
- **Commits** end with exactly these two lines and contain no model name:
  `<세션이 정해 준 trailer>`.

## 1. Where to work (plan §E.2: two agents, slot A = SHOGUN, slot B = TENMA)

| stage | worktree | branch (from `wip/rd` 03220f6) | RP sandbox | loadcheck tag |
|---|---|---|---|---|
| **S2-SHOGUN** | `S/rd/wt_shogun` | `wip/rd-shogun` | `S/rd/rp_shogun` | `rd_s2shogun` |
| **S2-TENMA** | `S/rd/wt_tenma` | `wip/rd-tenma` | `S/rd/rp_tenma` | `rd_s2tenma` |
| S3-I (later) | `S/rd/wt` | `wip/rd` (stays at 03220f6 during S2) | `S/rd/rp` (M1 reference, do not build into it) | |

- Build only into **your own** RP sandbox:
  `cd <wt>/roguelike/tools && python3 build_raiden_all.py --resourcepack S/rd/rp_<stage>`. A full build takes 22 s.
  The encounter alone (`python3 build_raiden_encounter.py`) takes under 1 s.
- Do not merge or cherry-pick between the two S2 branches. Do not merge the release branch either: if
  `claude/exciting-pascal-ek1vuy` moves, S3-I merges it, as M1 did.
- Scratch files go in `S/rd/s2/shogun/` or `S/rd/s2/tenma/`. Renders go in `S/rd/renders/s2_<stage>_*`.
- Disk is about 2.7 GB free. Delete scratch copies you no longer need. Every worktree is 153 MB and every RP is 33 MB.

## 2. File ownership (plan §E.0, plus the M1 additions)

| owner | sources | generated outputs (under `F:` = `data/rlk/function/`) |
|---|---|---|
| **S2-SHOGUN** | `raiden_enc/core.py`, `raiden_enc/shogun.py`, `raiden_enc/lines.py`, `build_raiden_illusions.py`, `build_raiden_movement.py`, `S/rd/tests/shogun_tests.py`, `S/rd/tests/plan_table_shogun.json` | core: `init reload spawn setup cleanup bars_hide world pause tick rig_hide rig_shown idle approach bag/* choose close_* finish bars incoming threshold hurt blink* object/* test/* patterns/<id>` (the writer of every pattern file); shogun: `normal_dispatch eyes_*` and the content of patterns 1-10 and 21-28; lines: `caption/* line/*`; `illusion/*`; `movement/*`; new paths under `F:boss/raiden/sg/` |
| **S2-TENMA** | `raiden_enc/tenma.py`, `build_raiden_cinematic.py`, `build_raiden_arena.py`, `S/rd/tests/tenma_tests.py`, `S/rd/tests/plan_table_tenma.json` | `transform_* armor_* exhausted_* normal_return shield_* armor_dispatch clap/* shadow/* stakes_* judgment_* (not judgment_rig) dome_*`, the content of patterns T and 11-20, `camera/*`, `death/*`, `F:room/raiden/**`; new paths under `F:boss/raiden/tm/` |
| frozen during S2 (lead / S3) | `raiden_enc/__init__.py`, `build_raiden_encounter.py`, `build_raiden_all.py`, `check_raiden_pack.py`; the kit (`raiden_kit.py`, `build_raiden_{hazards,hazard_vfx,fx_textures,materials,signature_vfx,object_vfx,orb}.py`, `raiden_obj_cards.py`, `raiden_fx_textures.json`); the rig (`build_raiden_rig.mjs`, `raiden_{geometry,clips,paint}.mjs`, `raiden_rig_manifest.json`, `raiden_rig_api.md`); `README.md`; every file outside the Raiden set (the shared engine is never edited, plan §E.0) | `hazard/** fx/** vfx/** object_vfx/** orb/** rig/** judgment_rig/**` |
| frozen harness (lead) | `S/rd/tests/{test_raiden,rdsim,static_checks,kit_tests,rig_tests,identjudge_rd,plan_table_src}.py`, `plan_table.json`, `baseline/*`, `S/mb/mcsim.py` | |

- If you need a change in a frozen file, write it in `S/rd/s2_issues.md` (§7). Then work around it inside your own
  files. For example, write a new visual with the kit API (`fx()`, `decal()`, `hz()`, `rig/prop/<kind>`) from your own
  module instead of editing a kit generator. S3-I applies the requests.
- **Atlas.** New sprites need a kit-file change, so they are requests. Keep the Raiden total ≤ 3.0 M px.
- **Generated files shared by both stages.** core.py writes `init`, `tick`, `choose`, `pause`, `finish`, `close_in`
  and `test/*` from data that both phase modules hand in. lines.py writes `line/tick`. These files will differ in both
  branches. That is expected: S3-I settles them by rebuilding (§6).
- **The encounter generators never delete stale files.** `core.write` only writes. When you stop generating a file,
  `git rm` it in the same commit. After every build, `git status` must show only the changes you intended.

## 3. Contracts between the two stages (so neither waits on the other)

### 3.1 Data seams (M1 commit 03220f6; the output was byte-identical, so nothing changed in game)

Each phase module hands these to `core.build()` as data. TENMA never edits core.py or lines.py.

| name | in | meaning |
|---|---|---|
| `IDS` | shogun.py `['1..7']`, tenma.py `['11..18']` | Pattern id ranges of the phase: a list of `a..b` or `n`. They drive the tick dispatch (`normal_dispatch` / `armor_dispatch`), the close-in gate (`1..max`), the choose test hooks, `test/request`, `test/apply` and the test help text. To make new ids reachable: SHOGUN sets `['1..10', '21..28']` and TENMA sets `['11..20']`. Each stage still writes its own `*_dispatch` lines for the new ids. |
| `OBJECTIVES` | both | Extra objectives that `init` adds. New names start with `rdSg` (SHOGUN) or `rdTm` (TENMA), for objectives and for `#` fake players alike. |
| `ON_PAUSE` | both | Commands appended to `pause`. **`pause` runs without `@s`** (world calls it), so use `@e[tag=rlk_raiden]` selectors. |
| `ON_FINISH` | both | Commands appended to `finish` (`@s` = the boss). They run after `rdPat`, `rdTime` and `rdAnim` are reset and `rdCool` is set, so they may override `rdCool`. `rdPrev` is the pattern that just ended. |
| `VOICE_LINES` | tenma.py | Merged into `lines.LINES` by `raiden_enc.build()`, with the same tuple format `(text or steps, ticks per step, colour, hold)`. A new key adds a line, for example 어리석군 for 20. An existing **Tenma-owned** key replaces its entry in place. The Tenma-owned keys are `mangeop eternal nothing cleave_all prison cheonsu sever goemyeol pierce`. SHOGUN keeps those entries in lines.py untouched, and keeps `VOICE`, `VOICE2`, `typed()` and the tuple format. |
| (existing) `BAG`, `REACH`, `CHOOSE_RULES`, `TICK_HIDE`, `TICK_TAIL` | as before | `CHOOSE_RULES` lines run in `choose` as the boss, after the bag draw and before the test hooks. They must touch `rdPat` only when `rdPhase` is 2. `TICK_HIDE` sets `#rdHide rd 1` to hide the rig; SHOGUN keeps that meaning when it replaces `rig_hide`. |

### 3.2 Behaviour contracts

1. **Forced weapon switch after the stun (plan §A.1, §A.2).** TENMA's `normal_return` adds
   `tag @s add rlk_rd_switch_due`. SHOGUN's `choose` consumes it: with the tag set, the next phase-0 pick is 28 if she
   holds the sword (sword→polearm) or 27 if she holds the polearm. Then it removes the tag. Until SHOGUN lands this,
   the tag does nothing. `test/to_normal` also calls `normal_return`; SHOGUN decides whether tests switch weapons.
2. **Switch after-effects** (field lightning, blade eyes) run only while `rdPhase` is 0. SHOGUN's tick resets their
   state as soon as it sees `rdPhase` ≠ 0. TENMA does nothing for them.
3. **Pattern-scoped entities.** Every transient entity either stage summons carries `rlk_room`, `rlk_raiden_aux` and
   **`rlk_rd_tmp`** (kit hazards and FX keep their own tags).
   - SHOGUN's `pause` and TENMA's `transform_start`, `exhausted_start` and `death/start` run
     `kill @e[tag=rlk_rd_tmp]` and `function rlk:boss/raiden/hazard/clear`.
   - `finish` (SHOGUN) calls `hazard/finish`.
   - Nobody calls into the other stage to clean up.
4. **Close-in for Tenma (§A.4: "blink if > 8 b", 19 "blink to 10 b in front if outside 6-14").** `REACH[pid] =
   (start, stop)` keeps its meaning: close in before the clock starts (`rdGo`, with `rdTime` held at 0) when the player
   is farther than `start`. TENMA may add two optional dicts in tenma.py:
   - `REACH_SPOT[pid] = d`: the blink lands d blocks in front of the player, toward her.
   - `REACH_MIN[pid] = lo`: she also repositions when the player is nearer than `lo`.

   SHOGUN rewrites `close_in` to be blink-only (no walking, plan §A.2) and reads both dicts with
   `getattr(mod, ..., {})`. Until then the release close-in applies (dash, blink at ≥ 18 b). Shogun rows blink
   *inside* their timeline (t 0-6), which is SHOGUN's own business.
5. **Entry points the other stage calls** must keep existing and keep their meaning. You may change the body, but
   not rename or delete them before S3:
   - SHOGUN keeps `finish`, `hurt`, `cleanup`, `bars_hide`, `caption/clear`, `line/tick`, `line/<every Tenma key>`,
     `illusion/cleanup`, `movement/{arrive,depart,cleanup}` and `object/clear`.
   - SHOGUN keeps the core.py names that tenma.py imports: `DRAIN DRAIN_DEFAULT DRAIN_REACTION EXHAUST FLOWER_BREAK
     SHIELD_CD SHIELD_MAX TRANSFORM_FX TRANSFORM_LEN at anim call caption center end event face flat gated haz obj
     pattern sound target tell write`. Add new helpers under new names rather than changing these.
   - TENMA keeps `transform_start`, `transform_tick`, `armor_tick`, `armor_dispatch`, `exhausted_tick`,
     `normal_return`, `shield_hit`, `dome_tick`, `dome_create`, `death/start`, `death/tick` and
     `camera/release_all` (a no-op from now on, like `camera/hold`).
   - The engine interface of current.md §5 stays for both: the ids, the tags `rlk_raiden`, `rlk_rd_object` and
     `rlk_raiden_arena`, and the scores. `rdPat` 5 and 15 keep their meaning, because `combat/apply` gates on them.
6. **Rig.** Patterns call `rig/play/<clip>` (rdsim records this path as a cue). They take hit ticks from the clip
   events (`raiden_rig_api.md`, plan §C.5); those events are binding and S2 may not move them.
   - `rdAnim` together with `rig/legacy_anim` stays until S3, for the patterns not converted yet.
   - Rig changes are requests.
   - Facing: the giant arm and the glaive are on her **right**, and the thin arms fan out on her left (S1-RIG,
     footage B_v7_06.90 / B_v9_03.30). The plan's "giant left arm" reads the footage from the viewer's side.

## 4. S0/S1 hand-off items, assigned (from `S/rd/s1_issues.md`)

**S2-SHOGUN**
- Rig request: `rig_hide` (core.py) teleports the parts 60 b down. That is a known `tp_below` finding. Replace it
  with `function rlk:boss/raiden/rig/state/hidden` and drop `rig_shown`; the next `rig/play` shows the rig again. Keep
  the `#rdHide` / `TICK_HIDE` meaning.
- `illusion/vanish` does `tp @s ~ ~-100 ~`, a known `tp_below` finding against the no-bodies-below-the-floor rule.
  Hide her with `rig/state/hidden` plus the immune state instead.
- Kit request: `finish` calls `hazard/finish`, so the `detached` flag works. `pause` calls `hazard/clear` and
  `kill @e[tag=rlk_rd_tmp]` (§3.2.3). Adding the kit objectives (`hazard/setup`) to core's list is optional.
- Known R2 tips you own:
  - the `setup` spawn subtitle becomes "라이덴의 이나즈마 전하";
  - the `illusion/hold` hint is removed;
  - the eye HUD message (real game) is added while the single eye lives.
- Plan notes:
  - Pattern 2, disc 1, reaches a player under 12 b within 12 t of the star flash. Make it R1-clean (launch later or
    slower) and record the choice in `plan_table_shogun.json`.
  - The pattern 1 follow-up chance: row 1 says 60 %, row 24 says 50 %. The table uses 60 %; pick one.
  - plan.md has no explicit Shogun bag lists; plan_table infers them from the weapon columns. Write your bags into
    shogun.py and your overlay.
- Rig notes: `stagger` is one 60-tick clip that loops 20-60. The clone props are full-size figures with their pivot
  1.375 b above the feet; `rig/prop/clone_*` already lifts them.
- Plan risk (§F.1): check that the guard parry sees `#icd` / `#skillDmg` from every player attack path, with one
  attack per character in rdsim. The fallback is to parry all hits at ×0.25.

**S2-TENMA**
- Kit request: `transform_start`, `exhausted_start` and `death/start` call `hazard/clear` and
  `kill @e[tag=rlk_rd_tmp]`. Then cue cards no longer outlive a phase change; the `guard_shatter` pillar, for example,
  lasts up to 100 t.
- Kit note: pattern 13's shadow still summons `fx_hazard/after_3`, a compatibility model. Switch it to
  `hz('follow', ..., decal='pool')` (plan row 13).
- Known R2 tips you own:
  - `exhausted_start` becomes "갑주 파괴";
  - `transform_title` loses its subtitle (title only);
  - `judgment_hint` becomes the real-game message 「추모의 꽃다발」에 번개 원소 공격을 가해 보호막을 펼치세요.
- Plan notes:
  - **20 spin**: an annulus 2-7 over the full circle is 141 b², so it counts as big, but it hits 13 t after the glint.
    R1 needs ≥ 20 t. Move the cue earlier, move the hit to ≥ 20, or shrink the area below 100 b².
  - **17**: the slabs reach a player 2.5-4.3 b out in under 12 t, and the wave has no cue tick (the table assumes
    41).
  - **14**: the vajra rings reach a player within 3.6 b of a vajra in under 12 t after the current cue (minor).
  - **19 near-field**: the table gives it the slam's cue (6).

  Fix or justify each one in `plan_table_tenma.json`.
- Rig notes:
  - Death keeps whichever form she is in.
  - `t_collapse` carries the events form 20 and kneel 46.
  - The gauntlet hands stay ≥ 0.58 b above the floor, and no clip animates them yet. Keep every prop you place
    (planted glaive, vajras, palm, dome) at or above the floor (R3).
  - The 만겁 rework drops the judgment rig. Its shims (`judgment_rig/*`, `rig/target_slam_*`) stay until S3; stop
    calling them from `TICK_TAIL` and the patterns.

**Both**
- Loadcheck: `bash S/mcsrv/loadcheck.sh <wt>/roguelike <tag>`. **No `flock`**: the script takes `S/mcsrv/.lock`
  itself, so an outer flock deadlocks. Run it at most once per hour, and always at your stage end.
- Since M1, the old encounter runs without floor warnings: the kit dropped the legacy decals, and only strike
  visuals remain. `--plan` mode stays red for a pattern until you re-author it. That is by design.
- Undodgeable moves raise the dodger DPM by far more than 15 % of the tiny release base (25.6 / 14.4 raw), so judge
  the dodger column as an absolute change. `-k balance` (45 s) is information in S2; the balance pass is S3's.
- Unused sprites and models (fx_weapon/*, judgment, rift, `bolt_d`, ...) are S3's to delete once nothing references
  them. Do not add new references to them.
- File budget: `F:boss/raiden` is at 1275 files / 3.2 MB against a target of ≤ 1100. The rig accounts for 744 of
  them. Report your delta, and prefer macros and tables over per-tick files.
- `build_raiden_all.py` and `check_raiden_pack.py` belong to nobody in S2. Changes to them are requests.

## 5. Tests (all fast; run them with `python3 -I`; `<dp>` = `S/rd/wt_<stage>/roguelike`)

```
python3 -I S/rd/tests/test_raiden.py <dp> --rp S/rd/rp_<stage>            # quick (2 s)
python3 -I S/rd/tests/test_raiden.py <dp> -k <ids> --plan                 # your re-authored patterns vs §B (+ overlay)
python3 -I S/rd/tests/test_raiden.py <dp> -k <other phase ids>            # legacy: the other phase still unchanged
python3 -I S/rd/tests/test_raiden.py <dp> -k shogun | -k tenma            # your own module (run(ctx) contract)
python3 -I S/rd/tests/test_raiden.py <dp> -k kit,rig,budget --rp S/rd/rp_<stage>
python3 -I S/rd/tests/identjudge_rd.py <dp>                               # base is now d765bab (the M1 release)
cd <dp>/tools && python3 check_raiden_pack.py S/rd/rp_<stage> <dp>
```

- **Your own tests** go in `S/rd/tests/shogun_tests.py` / `tenma_tests.py`, which expose `run(ctx)` returning
  `[(name, ok, info)]` (see kit_tests.py). `-k shogun` / `-k tenma` runs them; they are skipped while the file is
  missing. If you need different rdsim behaviour, monkeypatch it inside your own module. Never edit the shared
  files: both agents run them from the same directory at the same time.
- **Plan table.** `plan_table.json` stays as transcribed. Your corrections go into your overlay
  (`plan_table_shogun.json` holds phase-0 rows; `plan_table_tenma.json` holds phase 1/2 rows): `{"patterns": {"<id>":
  <whole row, same format as plan_table.json>}}`. The loader replaces rows by id and refuses a row of the other
  stage's phases. Note why a row differs from plan.md in its `note` fields.
- **Static baseline.** Do not run `--save-baseline`. A known finding you fix prints as fixed and does not fail; a new
  finding fails. S3 re-pins.
- **Legacy.** Re-authored ids leave the legacy group by design. Keep the other phase's legacy ids green: that proves
  your core or tenma changes did not break the patterns you do not own. A change caused by SHOGUN's close-in or idle
  rework must be explained in your result.

## 6. How S3-I will merge (follow it so the merge stays mechanical)

1. In `S/rd/wt`: `git merge --no-ff wip/rd-shogun`. That is a clean fast-forward-like merge, because `wip/rd` has
   not moved.
2. `git merge --no-ff wip/rd-tenma`. Sources do not conflict if §2 was respected. Conflicts in generated files under
   `F:boss/raiden/**` are settled by taking either side, then running
   `build_raiden_all.py --resourcepack S/rd/rp` and `git add -A`.
3. Look for orphans (files no generator writes any more). Run the full `test_raiden`, fold the two overlays into
   `plan_table_src.py`, re-pin `known_static.json`, merge the latest release, then run identjudge with the new base
   and the loadcheck.

So that this works:
- Never commit a hand edit to a generated file.
- Keep every cross-stage need in `S/rd/s2_issues.md`.
- Mention in your result every core.py / lines.py / tenma.py data hook you added.

## 7. Requests and issues

Append to `S/rd/s2_issues.md` under your stage heading. One bullet per item: the target (stage or file), what, why,
and whether you worked around it. Read the other stage's section before you finish; requests addressed to you are
yours to do in S2 when they fit your files.

## 8. M1 record (what you start from)

- `wip/rd` (03220f6) is the sum of four things: S0 2400430, S1-KIT ee223de, S1-RIG f2c0ed0 (merge c4994db), and the
  release d765bab (merge fa7b087: Azhdaha fixes 3086d1e with the hand-written `player/dash_chk_*` change and the
  `rlk:low_top` block tag, plus the mid-boss tip removal d765bab).
  - Both merges had no conflicts.
  - Rebuilding every Raiden generator from the merged tree changed 0 bytes in the datapack.
  - Then came the seam commit (§3.1). Its output is byte-identical too.
- **RP.** `S/rd/rp` is the latest release RP `S/az/rp_az` (it has the kit-font fallback), with its Raiden-generated
  folders removed (`items/raiden`, `models/item/raiden`, `textures/raiden/{fx,fxg,rig}`; the skin is kept) and
  rebuilt by `build_raiden_all.py`. A build over an unpruned copy left 6 orphan model/item pairs that no generator
  writes (`raiden/illusion`, `fx_signature/judgment_strike`, `fx_object/{fade_cross,fade_slash,strike_cross,warn_cross}`).
  Nothing references them, so the clean sandbox drops them. S3 should deliver from a clean RP.
  - `rp_shogun` and `rp_tenma` are copies of it.
- **Checks on 03220f6.** All of these pass:
  - quick: static 7 known / 0 new; table 90 hits; cleanup; perf idle 163 / 162 cmds/t against a budget of ≤ 150,
    with 30 rig parts.
  - legacy: 16/16 ids.
  - kit and rig.
  - budget: files 1275 / 3.2 MB; RP models 170; Raiden 2.70 M px; stitched atlas 10.22 M px.
  - `check_raiden_pack`: 177 models, 0 problems.
  - `identjudge_rd --base d765bab`: 0 files outside the Raiden set.
  - `loadcheck rd_m1`: 0 function load failures.
- **Harness changes by M1:**
  - `identjudge_rd.py` defaults to `--base d765bab`.
  - `test_raiden.py` gained the `shogun` / `tenma` groups (also in `all` / `full`) and the two plan-table overlays.
- `wt_rig` and `rp_rig` are removed (S1-RIG is merged). The branch `wip/rd-rig` is kept.
- The M1 build logs, the per-branch file lists and the RP orphan diff are in `S/rd/m1/`.
