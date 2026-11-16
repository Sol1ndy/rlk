# 홍련 (Scarlet, special boss) — stage briefs (hand each section verbatim to a fresh agent)

Coordinator block (each brief below repeats what its agent needs; this block is only for the lead):
`S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`, `HR` = `S:hr`. Base branch `wip/hr-d0`
= **5d2c3ac** on the 11-03 handover head `35b82e5` (the D0 commit `52b86b9`: `tools/mboss_scarlet/{__init__,api}.py`,
`stub_rig_manifest.json`, empty `seq.py` / `p_ghost.py` / `reward.py`, the registry entry `scarlet` with `enabled:false`,
`arenas.hr_field` with its stub arena functions and dispatcher lines, every other generator output byte-identical; then
the D0 fixes `5d2c3ac`: the FN-f wrapper names `mboss/bars_off` / `bars_on`, the ownership hand-overs — contract §7). Order
(PLAN §9.7): D0 → (S1 ∥ S2a) → (S3 ∥ S2a → S2b) → (S4 ∥ S2b) → (SR ∥ S1K) → I1 → R → F → S5 → V. Bases: S1, S1K, S2a, SR
from `wip/hr-d0`; **S3 from `wip/hr-s1`, S2b from `wip/hr-s2a`, S4 from `wip/hr-s3`** (the head the earlier stage
reported). The lead creates each worktree before handing the brief over:
`git -C /home/user/rlk worktree add S:hr/wt_<s> -b wip/hr-<s> <base>` (S written out in full), at most **two** stage
worktrees at once (`df -h /` ≥ 800 MB first): remove `HR/wt_d0` before the first two, and remove a stage's worktree (and
its RP copy once nobody copies from it) as soon as the stage has reported — its branch keeps the commits until I1 merges
it (waiting for the merge would put three worktrees on the disk). RP copies only for S2a / S2b / S1K:
`cp -r S:ar/rp_i1 HR/rp_<s>` (the 11-03 release RP, ≈ 48 MB, never hard links). The Minecraft EULA consent was **not**
recorded when these briefs went out (README 0-2 2 ②, 0-8; PLAN §0.1 question 8): no stage starts the local test server;
every report says "loadcheck pending the user's EULA consent". **11-05: the user consented (README 0-8, 0d65e87); the
lead runs loadcheck on each stage branch as it reports and at I1 / V / the release.** The eight PLAN §0.1 questions run on their defaults (contract header).
Helpers for every stage: `bash HR/tools/regen_d0.sh <wt>/roguelike` (every registry-reading Python generator in the
documented order + the bf / fg kits `--skip-rp`, then `git status --short`) and `bash HR/tools/checkers.sh
<wt>/roguelike` (check_refs, check_macro, check_nbtpath, mb/lint_mc vs the 35b82e5 results in `HR/tools/base_35b82e5/`;
D0 already accounts for +1 refs / +4 macro instances in `mboss/ar/hr_field/{full_rim,tp_in}`, the arena template's known
false positives).

---------------------------------------------------------------------------------------------------------------------

## S1 — special-boss framework: FN-a / FN-b / FN-c / FN-e / FN-f

**① 너는 (you are)** extending the special-boss framework of a Minecraft Java 26.3 roguelike datapack (namespace `rlk`,
Korean UI; repository `/home/user/rlk`, datapack root `roguelike/`) for its new special boss 홍련 (Scarlet; module id
`scarlet`, registry n 21, function root `boss/scarlet`, arena `hr_field` n 5; reached through a room rift like 타키).
Worktree `S:hr/wt_s1` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/hr/wt_s1`, branch
`wip/hr-s1`, base `wip/hr-d0` = **5d2c3ac** (if the worktree is missing: `git -C /home/user/rlk worktree add
/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/hr/wt_s1 -b wip/hr-s1 5d2c3ac`; never touch
`/home/user/rlk` otherwise). Abbreviations: `S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`,
`HR` = `S:hr`, `R:` = `<worktree>/roguelike`, `F:` = `R:data/rlk/function`, `T:` = `R:tools`. 20 t = 1 s.

**② 먼저 읽을 것 (read first)**: `R:README.md` chapter 0 (0-2 rules, 0-4 generators / regeneration, 0-5 gates, 0-6 user
rules, 0-7 pipeline, 0-8 test tools) and the sections 특수 보스 (`mboss/sp/`), 균열, 타키 → 파일 · 생성 순서, 중간보스 →
공용 라이브러리, 챕터 보스 → 시험 명령; `HR/PLAN.md` §0 + §0.1, §3.2-§3.3 (CS1 hides the boss bars, SQ1 shows them),
§7.0-§7.2 and §7.6 (the **fw** checks), §8, §9 (all), §11 (FE-1, FE-4, FE-6, FE-11); `HR/contract.md` (all; §3.1 is your
interface, §5 the I1 allow-list); `T:mboss_scarlet/api.py` §1 and §9 / §9b (`FN_FIELDS`, `WIN_WORD`, `RW_HOOK_LINE`,
`BARS_FLAG`, `BARS_FNS`, `bars()`, `music()`); `HR/understand/framework.md` (the framework facts behind FN-a…f with
file:line references); the code you change: `T:build_mboss_core.py` (`snbt_entry` ≈ :143, `w('death_finish')` ≈ :1181,
`w('sp/reward')` ≈ :4478, `w('test/swon')` ≈ :4643, the literal-line technique of `sp/gate` / `sp/prep` ≈ :4324, `world`,
`fight_vars`, `cleanup_fight`, `bars`), `T:mboss_lib.py` (`load_registry` special branch ≈ :131-141, `SPECIAL_HOOKS`,
`MUSIC_TRACKS` + `music_len` and the ar S1 comment on how a pool was measured), `T:check_mboss_pack.py` (hook loop ≈ :49,
specials ≈ :142); the 타키 S1 precedent `S:tk/contract.md` and `S:tk/stage_briefs.md` (S1).

**③ 목표 (goals)** — your files: `T:build_mboss_core.py`, `T:mboss_lib.py`, `T:mboss_registry.json` (only the fields
below), `T:check_mboss_pack.py`; outputs: everything the core writes (`F:mboss/**` except `F:mboss/arena/**` and the
module trees, `F:boss/test/**`); `HR/tests/test_special_hr.py`; `HR/tests/lib/**` (you create it, ⑤; S3 takes it over
after your report — `api.HANDOVER`); `HR/s1/readme_special.md` (your scratch is `HR/s1/`).
1. **FN-a** `winWord` (PLAN §7.1.3, verbatim lines there): validation in `load_registry` (special entries only, non-empty
   string ≤ 12 chars); `snbt_entry` appends `winWord:"…"` only for entries that set it; `sp/reward` line 8 becomes the
   guarded 처치 line (today's text, only guarded with `execute unless data storage rlk:mboss cur.winWord`) + the
   `winWord` line; `test/swon` gets its first line and the new `test/swon_msg_w` (`도전 성공! 균열 자리에 …`).
2. **FN-b** `rwHook` (§7.1.4): `mboss_lib.SPECIAL_OPT_HOOKS = {'rwHook': 'reward'}` beside `SPECIAL_HOOKS` (optional
   hooks, required only when the entry sets the flag; no macro); validation (bool, special only); in `sp/reward`, after
   the `sp/lvup` line and before `#spPk`, one comment line `# hr FN-b: per-special reward hooks (registry rwHook)` and,
   for every **enabled** special with the flag, exactly `api.RW_HOOK_LINE` (= `execute if data storage rlk:mboss
   cur{id:"scarlet"} as @a[tag=player,limit=1] run function rlk:boss/scarlet/reward`). While `scarlet` is disabled the
   line does not exist (no reference to a missing function).
3. **FN-c** `poof` (§7.1.5): `if b.get('poof') is False: parts.append('poof:0b')`; `death_finish` runs its poof particle
   only `unless data storage rlk:mboss cur{poof:0b}` (+ comment); `kill @s` unchanged.
4. **FN-e**: measure the `minecraft:music.overworld.cherry_grove` pool (26.3, asset index as the ar S1 did; the jar /
   version JSON under `S:mcjar`) into `MUSIC_TRACKS`; registry music 1 `len` = `mboss_lib.music_len(...)`, music 3 stays
   0 (played once). If the assets cannot be reached keep `len 0` and write a request.
5. **FN-f** (PLAN FE-6): flag `#mbBarOff mb` zeroed in `fight_vars` and `cleanup_fight`; `mboss/world` (≈ :26) skips
   `mboss/bars` while it is 1; two **new** functions `F:mboss/bars_off` (`scoreboard players set #mbBarOff mb 1` then
   `function rlk:mboss/bars_hide`) and `F:mboss/bars_on` (`scoreboard players set #mbBarOff mb 0` then `function
   rlk:mboss/bars_show`); `mboss_lib.bars(on)` returns **exactly one line** = `api.BARS_FNS[int(on)]` (`function
   rlk:mboss/bars_off` / `function rlk:mboss/bars_on`). The existing `F:mboss/bars_hide` / `bars_show` stay
   **byte-identical** (they are called by `death_start`, `pause_tick`, `cleanup_fight`, `init`, `main`, `tick`, `start_go`
   and `mboss/bars`: if they set the flag, a death pause would hide every boss's bars for the rest of its fight). Every
   other boss's bars behave as before.
6. Registry: add exactly `api.FN_FIELDS` (`"winWord": "도전 성공", "rwHook": true, "poof": false`) to the `scarlet` entry
   and the music 1 length; keep `enabled:false` (I1 flips it); adjust only the `_doc` line about 홍련.
7. `check_mboss_pack.py`: optional hooks (`hooks += [h for f, h in L.SPECIAL_OPT_HOOKS.items() if b.get(f)]`) for
   enabled entries, the exact FN-b line in `mboss/sp/reward` for each such entry, `mboss/test/swon_msg_w` among the frozen
   runtime names; 0 problems on your tree.
8. README fragment `HR/s1/readme_special.md` (rows for 특수 보스: `winWord` / `rwHook` / `poof` / the bars flag; one line
   for 시험 명령); the lead merges it at I1.
Contract names you use: `api.ID`, `api.N`, `api.AID`, `api.FN_FIELDS`, `api.WIN_WORD`, `api.RW_HOOK_LINE`,
`api.BARS_FLAG`, `api.BARS_FNS`.

**④ 건드리지 말 것 (do not touch)**: `T:mboss_scarlet/**` (the lead's contract and the other stages' stubs),
`F:boss/scarlet/**`, `T:build_mboss_arena.py`, kit / rig / arena-theme files, other bosses' modules and generators,
`tools/dev/**`, the player avatar files (`T:build_player_rig.mjs`, `T:player_motion/**`, `F:char/**`, `F:player/**`),
`R:README.md` and the RP README (fragments only). Anything else you need: `HR/requests/s1.md`.

**⑤ 시험 (tests)**: `HR/tests/test_special_hr.py`, in the harness style of `R:tools/dev/sim/ar/tests` (`check(id, cond,
detail)`), vendoring `R:tools/dev/sim/az/tests_cm/lib` (mcsim ← fgsim ← azsim ← cmsim) unchanged with md5s in
`HR/tests/lib/README.md` plus a generic `HR/tests/lib/hrsim.py` (`HR/tests/lib/**` is yours until your report, then S3's:
S3 extends `hrsim.py`, the other stages only read it); run it from outside the datapack
(`R:tools/dev/sim/README.md` §1). Checks (PLAN §9.3 + §7.6 fw): registry validation (`winWord` / `rwHook` / `poof` only
where allowed, `picks 1` / `lvup 1` / `xp 0` pass, `hr_field` arena), her record has `winWord:"도전 성공"` + `poof:0b`;
타키 / spproto records and `boss/tachy/**`, `mboss/spproto/**` byte-identical; `sp/reward` (guarded 처치 line == today's
line, the `winWord` line, exactly one hook line after `sp/lvup` and before `#spPk`, only for an enabled `scarlet`),
`death_finish` gating, `test/swon_msg_w`; FN-f (bars stay off while `#mbBarOff 1`, cleared by `fight_vars` /
`cleanup_fight`, every other boss's bars unchanged); the rift roll share 10 : 10 (seeded, ≈ 50 %); music pool length;
`check_mboss_pack` 0. Use spproto and a **local forced `enabled:true` copy** of the registry in a variant tree (never
commit `enabled:true`).

**⑥ 그림 (renders)**: none (framework only).

**⑦ 게이트 (gates)**: loadcheck — **pending the user's EULA consent** (do not start the server; say so in the report);
`bash HR/tools/regen_d0.sh <wt>/roguelike` twice → the second run changes nothing, `git status` shows only your files;
`python3 tools/check_mboss_pack.py` → 0 problems; `python3 tools/mboss_scarlet/api.py --check` green (it must keep
passing with your registry fields); 타키 / spproto outputs byte-identical and every changed shared output on the I1
allow-list (`HR/contract.md` §5); `R:tools/dev/sim/az/tests_cm/run_all.sh` from a copy → no failure beyond README 0-9's
known list; `bash HR/tools/checkers.sh <wt>/roguelike` → no new finding; your suite green; the standing rules: no
negative literals in `scoreboard players add/remove`, no glyph-font inheritance, lowercase ids, nothing below the floor,
no teleport into blocks, held props the right way, one display card per projectile, `summon` ignores the execute
rotation; never hand-edit generated outputs (generator → regenerate).

**⑧ 커밋 (commit)** on `wip/hr-s1` in your worktree only; never push. The message ends with exactly these two lines and
names no model anywhere else:
`<세션이 정해 준 trailer>`
Disk is tight (≈ 1.7 GB free): delete scratch you do not need; no large renders.

All stages, always: never hand-edit generated outputs (change the generator, regenerate); the real-game traps — no negative literals in `scoreboard players add/remove`, no glyph-font inheritance, lowercase resource ids, nothing below the floor, no teleport into blocks, held props pointing the right way, one display card per projectile, `summon` does not take the execute rotation; originality (PLAN §1.5): names stay neutral (`scarlet` / `hr`), never name a part, texture, model, function or file after the original game's costume or level pieces; the EULA consent is not recorded, so the local test server is never started.

**⑨ 보고 (report)**: your head commit (S3 branches from it), files owned, the generated diffs of `sp/reward`,
`test/swon`, `test/swon_msg_w`, `death_finish`, `register`, `world`, `fight_vars`, `cleanup_fight`, `bars_off` /
`bars_on` (and that `bars_hide` / `bars_show` did not change), the measured cherry-grove track lengths, test counts,
`run_all.sh` / checker results, "loadcheck pending the user's EULA consent", requests (`HR/requests/s1.md`), and what S3
must know (the exact bars lines, the reward-hook context, the `HR/tests/lib` you hand over).

---------------------------------------------------------------------------------------------------------------------

## S1K — kit (effects / sounds / HUD) + arena `hr_field` 「달빛 억새밭」

**① 너는 (you are)** building the effects / sound / HUD kit and the arena theme of the special boss 홍련 (Scarlet; module
`scarlet`, function root `boss/scarlet`, arena `hr_field` n 5) in a Minecraft Java 26.3 roguelike datapack (namespace
`rlk`, Korean UI; repository `/home/user/rlk`, datapack root `roguelike/`) and its resource pack (not in git). Worktree
`S:hr/wt_s1k` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/hr/wt_s1k`, branch
`wip/hr-s1k`, base `wip/hr-d0` = **5d2c3ac** (if missing: `git -C /home/user/rlk worktree add
/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/hr/wt_s1k -b wip/hr-s1k 5d2c3ac`; never
touch `/home/user/rlk` otherwise). Your RP: `cp -r S:ar/rp_i1 S:hr/rp_s1k` (the 11-03 release RP; plain copy, never hard
links; `df -h /` ≥ 800 MB first). Abbreviations: `S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`,
`HR` = `S:hr`, `R:` = `<worktree>/roguelike`, `F:` = `R:data/rlk/function`, `T:` = `R:tools`, `RP` = `HR/rp_s1k`.

**② 먼저 읽을 것 (read first)**: `R:README.md` chapter 0 (0-2, 0-4 incl. the RP block, 0-5, 0-6, 0-7) and the sections
아를레키노 / 타키 (모습 · 효과 · 경기장, 파일 · 생성 순서), 챕터 보스 → 경기장; the RP's `README.md` (§1-§4: atlas, font
code-point bands — 홍련 takes U+EC00-ECFF, element rules); `HR/PLAN.md` §1.3-§1.5 (whose effects, no decals, the
originality rule), §3 (every effect / sound / overlay / line beat), §4.1 (colours), §4.3-§4.5 (effects per move), §5.2
and §5.5 (pip break, the warning banner), **§6 (the arena, all)**, §7.3.2 (the coda's 8 presets + 7 sounds), §7.4.5
(`vig`), §9.2 (Kit + the sprite table), §9.3 (`test_kit.py`, `test_arena_hr.py`), §9.4-§9.5, §11 (FI-2, FI-14, FE-3,
FE-15); `HR/contract.md` (§2-§5; §3.3 kit, §3.4 arena); `T:mboss_scarlet/api.py` §1 (`ARENA_SPEC`, `MOON_POS`,
`MOON_BEARING`, `SEAT_POS`, `LOOK_ID`, `arena_look`, `look_job`, `deco`, `DECO_DEFAULT`), §3 (`DARK_SLICES`,
`DARK_LIGHT`, `WARN_TEXT`, `WARN_HL`, `SKIP_*`), §5 (`LINES`, `LINE_AT`, `LINE_COLOR`), §8 (all: `KIT_PRESETS`,
`KIT_PROPS`, `KIT_SOUND_RECIPES`, `KIT_HUD`, `OVERLAYS`, `VIG`, `KIT_FIXED`, caps, `KIT_SPRITES`, `K`), §9b (`EV_T`);
the closest kits `T:build_mboss_kn_fx.py` + `T:mboss_kn_fx_paint.py` (아를레키노: card engine, pools, ager, `--skip-rp`,
lines with letter reveal, the banner bossbar) and `T:build_mboss_tk_fx.py`; the arena framework `T:build_mboss_arena.py`
(theme contract, `look_lines`, slices: one per tick, fill ≤ 32 768, ≤ 8 000 commands per slice, ≤ 40 slices; the refusal
of a look call while a job runs) and the closest themes `T:mboss_arena_fl_ruins.py` (block dome sky lit from inside, the
crimson look) and `T:mboss_arena_tk_lift.py`; `HR/understand/arena.md`; the sheets `HR/ref/arena_*.jpg` for mood, sizes
and light only (`arena_glyph_*.jpg` = what NOT to build).

**③ 목표 (goals)** — your files: new `T:build_mboss_hr_fx.py` (+ `--skip-rp`), `T:mboss_hr_fx_paint.py`,
`T:mboss_hr_fx_manifest.json` (generated), new `T:mboss_arena_hr_field.py`; outputs `F:boss/scarlet/fx/**`, RP
`assets/rlk/{textures,models/item,items}/mboss/hr_kit/**` + atlas entries, the font `rlk:mboss_hr` (+ its glyph textures),
`F:mboss/arena/hr_field/**` and the `hr_field` lines the same generator then adds to `F:mboss/arena/job_tick` (1) and
`F:mboss/arena/abort` (2) (all written by the unchanged `build_mboss_arena.py` from your theme); `HR/tests/test_kit.py`,
`HR/tests/test_arena_hr.py` (`HR/tests/lib` is S3's: read it; your own sim helpers go in `HR/s1k/`);
`HR/s1k/readme_kit.md` (+ `rp_readme_kit.md` for the RP README rows; your scratch is `HR/s1k/`).
1. The kit generator (copy-adapt the 아를레키노 engine; no shared-file hooks): **every** name of `api.KIT_PRESETS` (50, incl.
   the 8 `ev_*` of PLAN §7.3.2) with exactly its macro args, `api.KIT_PROPS` (`disc` one card per projectile, summoned then
   rotated; `petal_big {look}` whole / cut / split; `moon_halo {look}` p1 / p2 / off; `lotus {look}` bud / bloom;
   `seat_rock {look}` bottle / bare / set — `look` is a quoted name; @s = the card / marker the caller summoned, calling
   again re-looks it), `api.KIT_SOUNDS` (104: one recipe each from `api.KIT_SOUND_RECIPES`, vanilla ids only, the
   `mboss_lib.sound` min-volume rule; tune volumes only by request), `api.KIT_HUD` (`line {id}` for ids 1-25 with the
   Raiden letter reveal — two syllables per 2 t with `block.note_block.hat` 0.3 — held for `api.LINE_AT[id][2]` t, colour
   `#F2D0E8`, overlay-aware: while an overlay is up the line re-sends the overlay glyph on the title; `ovl {g,in,hold,out}`
   with the six glyphs of `api.OVERLAYS` ≈ 144 × 81 as Apep's, `vBig` = in + hold + out; `warn {on}` = bossbar
   `rlk:hr_warn` with `api.WARN_TEXT`, white with 「즉사」 in `#FF3A55`; `skip {s}` = the actionbar 「⊙ 건너뛰기」 + 「 ·
   Shift 길게」 (`api.SKIP_TEXT` + `SKIP_HINT`, grey `#A8A8B0`) at brightness step 0-4, `hudHold` 2, `s:5` clears it;
   `clear`), `api.KIT_FIXED` (`card cardx look clear uninstall`). Glyph `vig` = `api.VIG` U+EC16 (an edge-only dark
   vignette, centre clear). Values in tenths of a block / degrees / ticks; `c` 1 lilac `#C97EDD` (rim `#FFE6FA`), 2
   pink-magenta, 3 yellow `#FFE14A`, 4 crimson, 5 white; `scarlet_line`'s roll > 0 rises toward the player's right. Caps
   96 fx cards / 48 ambient (the ager kills the oldest); `afterimage` = one translucent lilac silhouette card per frame, ≤ 4
   alive, fading over 6 t (no rig copy). Sprites exactly `api.KIT_SPRITES` (assert their sum ≤ `api.KIT_SPRITE_CAP`
   0.26 M); gate icon `rlk:mboss/hr_kit/gate_icon` (a red lotus over a long blade, ≤ 5 000 px). The font: glyph roots empty
   and unstyled, every component names its font, the font ends with a `minecraft:default` reference. In-game demos
   `fx/test/<name>` on a vanilla stand-in. Only boss-side effects (PLAN §1.3: never Eve's); the gold clash bursts only for
   blade-on-blade beats.
2. The arena theme `T:mboss_arena_hr_field.py` (PLAN §6, an ORIGINAL composition): the walk disc r 25 of flat full blocks
   at y 200 (no slab, no obstacle, nothing overhead below y 226 except the light layer y 206), barrier ring r 26-27; the
   lotus pond to the north (r 27-36, irregular), the one old pine (322°, r 38), the lotus stone lantern on its rock islet
   (28°, r 31), the moon disc r 5 at bearing 12° / elevation 22° (centre `api.MOON_POS`) in open sky, side walls with
   small lanterns, bamboo, six cherry trees, the south gap at the arrival, the beyond band, the block dome r 46 lit from
   inside, the light grid; **no stair, no pair of tall masses framing the moon, no glyphs, no monoliths**. Looks `moon`
   (default), `crimson`, `dark` (§6.3-§6.5) through `look_lines(look)` = **absolute spans** of every cell any look changes
   (block-exact from any source look), 4 real slices per job; `dark` puts two empty padding slices after each real one so
   its real slices land 3 t apart (`api.DARK_SLICES`); `api.DARK_LIGHT` false = fallback B (dome / moon / lanterns only).
   `SENTINEL`, `CHECK`, `POINTS` as `fl_ruins`; a `DECO` dict with the shape of `api.DECO_DEFAULT` (`moon_halo` point, 8
   `lotus` points on your water, `seat_rock` = `api.SEAT_POS`) — `api.deco()` hands it to S3.
3. Regenerate the arena through `python3 tools/build_mboss_arena.py` (its stub functions become your slices).
Contract names you use: the §8 tables, `api.K`, `ARENA_SPEC`, `MOON_POS`, `SEAT_POS`, `DECO_DEFAULT`, `DARK_SLICES`,
`DARK_LIGHT`, `LOOK_ID`, `LINES`, `LINE_AT`, `WARN_TEXT`, `SKIP_TEXT`, `SKIP_HINT`, `EV_T`.

**④ 건드리지 말 것 (do not touch)**: the registry, the core and `mboss_lib`, `T:build_mboss_arena.py`,
`T:mboss_scarlet/**`, the rig files, other kits / themes / bosses, `tools/dev/**`, the player avatar files
(`T:build_player_rig.mjs`, `T:player_motion/**`, `F:char/**`, `F:player/**`), README / RP README (fragments only). Requests:
`HR/requests/s1k.md`.

**⑤ 시험 (tests)** (harness of `R:tools/dev/sim/ar/tests`, vendored sims; run from outside the datapack):
`HR/tests/test_kit.py` — every contract name with the right macro args; caps 96 / 48 and the ager; the sprite table vs
`api.KIT_SPRITES` (sum ≤ 0.26 M); a line during an overlay keeps the overlay on the title, `ttl_blank` after it; the warn
bossbar lifecycle; the skip prompt (`hudHold` set, cleared by `s:5`, text = 「⊙ 건너뛰기」 verbatim + the hint); pause
clear; uninstall leaves nothing; vanilla sound ids only (`R:tools/dev/sim/rd/tests/sound_ids.txt`); glyph root rule; lines
equal `api.LINES` 1-25 verbatim. `HR/tests/test_arena_hr.py` — walk disc flat full blocks; plants only `#rlk:dash_pass`;
nothing overhead below y 226 except the light layer; barrier closed; all six transitions `moon` ↔ `crimson` ↔ `dark`
block-exact and a look call issued while a job runs (the request waits, then runs); `dark`'s real slices 3 t apart;
slices / fill / command limits; light ≥ 12 (moon, crimson) and ≥ 6 (dark) on the walk disc; every plant on a valid
support in every look; the moon disc unobstructed from C and from `start`; no stairway within ± 20° of the moon's
bearing; no two block masses ≥ 8 b tall mirrored about it within ± 25°; no text display or glyph column anywhere; every
`DECO` point valid (lotus on water, halo before the moon, seat on the field).

**⑥ 그림 (renders)** (≤ 640 px jpg, `HR/renders/`, delete intermediates): `s1k_sprites.jpg` (sprite sheet), one strip
per preset / prop (`s1k_presets*.jpg`), `s1k_overlays.jpg` (glyph sheet incl. `vig`), `s1k_arena_moon.jpg`,
`s1k_arena_crimson.jpg`, `s1k_arena_dark.jpg` (top-down + a perspective from `start` + one from C at the moon, beside
`HR/ref/arena_keyframes.jpg` and `arena_palette_p1/p2.jpg`). Renderers: `S:ar/s1k/render/` (kit), the arena tools of the
ar S1 / tk S1K precedents.

**⑦ 게이트 (gates)**: loadcheck — **pending the user's EULA consent** (do not start the server; say so); `python3 -I
tools/dev/rplint.py HR/rp_s1k` → 0 problems; your generator twice → identical (datapack and the RP hash
`(cd RP && find . -type f -print0 | sort -z | xargs -0 sha1sum) | sha1sum`); `bash HR/tools/regen_d0.sh <wt>/roguelike`
→ only your files change; `python3 tools/check_mboss_pack.py` → 0; `python3 tools/mboss_scarlet/api.py --check` green;
atlas: kit ≤ 0.26 M, gate icon ≤ 0.005 M, the stitched atlas ≤ 13.2 M (`python3 -I tools/dev/atlas_px.py HR/rp_s1k`);
`bash HR/tools/checkers.sh <wt>/roguelike` → no new finding; your suites green; the standing rules: no negative literals
in `scoreboard players add/remove`, no glyph-font inheritance, lowercase ids, nothing below the floor, no teleport into
blocks, one display card per projectile facing its flight, `summon` ignores the execute rotation (rotate after),
vanilla sounds only, no floor decal, no tip text; never hand-edit generated outputs.

**⑧ 커밋 (commit)** on `wip/hr-s1k` in your worktree only; never push; the RP stays out of git (report its hash). The
message ends with exactly these two lines and names no model anywhere else:
`<세션이 정해 준 trailer>`
Disk is tight (≈ 1.7 GB free): one RP copy, delete render intermediates.

All stages, always: never hand-edit generated outputs (change the generator, regenerate); the real-game traps — no negative literals in `scoreboard players add/remove`, no glyph-font inheritance, lowercase resource ids, nothing below the floor, no teleport into blocks, held props pointing the right way, one display card per projectile, `summon` does not take the execute rotation; originality (PLAN §1.5): names stay neutral (`scarlet` / `hr`), never name a part, texture, model, function or file after the original game's costume or level pieces; the EULA consent is not recorded, so the local test server is never started.

**⑨ 보고 (report)**: commit, preset / prop / sound / HUD counts, sprite px + gate icon px, the RP hash, function count,
block counts per slice and the commands per look job, render paths, test counts, "loadcheck pending the user's EULA
consent", requests (`HR/requests/s1k.md`), the `DECO` points you chose.

---------------------------------------------------------------------------------------------------------------------

## S2a — the rig (model + the 36 fight / gauntlet clips + the 3 event clips + `item_sword`)

**① 너는 (you are)** building the display-entity rig of the special boss 홍련 (Scarlet; module `scarlet`, function root
`boss/scarlet`) — an ORIGINAL design of a Joseon wandering swordswoman with a red-lotus motif — in a Minecraft Java 26.3
roguelike datapack (namespace `rlk`, Korean UI; repository `/home/user/rlk`, datapack root `roguelike/`) and its resource
pack. Worktree `S:hr/wt_s2a` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/hr/wt_s2a`,
branch `wip/hr-s2a`, base `wip/hr-d0` = **5d2c3ac** (if missing: `git -C /home/user/rlk worktree add
/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/hr/wt_s2a -b wip/hr-s2a 5d2c3ac`; never
touch `/home/user/rlk` otherwise). Your RP: `cp -r S:ar/rp_i1 S:hr/rp_s2a` (plain copy, never hard links; `df -h /` ≥
800 MB first). Abbreviations: `S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`, `HR`
= `S:hr`, `R:` = `<worktree>/roguelike`, `F:` = `R:data/rlk/function`, `T:` = `R:tools`, `RP` = `HR/rp_s2a`. S2b continues
from your branch (the 8 cinematic clips).

**② 먼저 읽을 것 (read first)**: `R:README.md` chapter 0 (0-4 incl. the RP block and the rig rules, 0-5, 0-6, 0-7 step 4: the
U1 sheet goes to the user early) and the 타키 / 아를레키노 sections (모습, 파일); the RP's `README.md` (§3 rig rules, §4
element rules: elements inside −16..32, one rotation axis of −45 / −22.5 / 0 / 22.5 / 45); `HR/PLAN.md` **§1.5** (the
originality rule and its table), **§2 (all)**, §4.3-§4.5 (what each clip does), §5.4 (the deflect), §7.3.2 (`ev_give`,
`ev_toast`, `ev_leave`, the toss, `item_sword`), §9.2 (Rig), §9.3 (`test_rig.py`), §9.4-§9.5, §11 (FI-15, FE-16);
`HR/contract.md` (§1-§4; §3.2 is your interface); `T:mboss_scarlet/api.py` §6 (`RIG_UUID`, `TAGS`, `RP_RIG`,
`GHOST_MODEL`, `ITEM_MODEL`) and §7 (`PARTS`, `PARENTS`, `REPARENT`, `LOOKS`, `HANDS`, `PROP_STATES`, `ANCHORS`,
`RIG_CALLS`, `RIG_MACRO_CALLS`, `CLIPS`, `CLIPS_PLAN`, `CLIP_OWNER`, `check_manifest`, `stub_manifest`) and
`T:mboss_scarlet/stub_rig_manifest.json`; `HR/understand/model.md` (proportions, states, hand / prop usage) and
`patterns.md`; the templates `T:build_arlecchino_rig.mjs` + `T:arlecchino_*.mjs`, `T:build_tachy_rig.mjs` + `T:tachy_*.mjs`,
`T:tachy_rig_api.md`, on the shared RIGLIB `T:mboss_rig_compile.mjs`, `mboss_rig_clips.mjs`, `mboss_model_lib.mjs`,
`mboss_shape_lib.mjs`, `mboss_paint_lib.mjs`, `mboss_rig_math.mjs` (all unchanged); the sheets `HR/ref/model_*.jpg`
(proportions and states only — `model_colors.jpg` is the palette NOT to reproduce) and the pattern sheets of PLAN §10;
the renderer `S:az/understand/rigtech_render.py` (wrapper style `S:ap/rigwork/r1/r.sh`, the ar S2 scripts `S:ar/s2/*.sh`).

**③ 목표 (goals)** — your files: new `T:build_scarlet_rig.mjs`, `T:scarlet_{pose,geometry,paint,clips}.mjs`,
`T:scarlet_rig_manifest.json` (generated), `T:scarlet_rig_api.md`; outputs `F:boss/scarlet/rig/**` (owned, rebuilt from
scratch), RP `assets/rlk/{textures,models/item,items}/mboss/scarlet/**` + atlas entries; `HR/tests/test_rig.py`;
`HR/s2a/readme_rig.md` (+ `rp_readme_rig.md`; your scratch is `HR/s2a/`). After your report S2b takes over `test_rig.py`, the
manifest, the rig outputs and the RP `mboss/scarlet` files it regenerates with your unchanged generator (`api.HANDOVER`).
1. The model of PLAN §2.1-§2.4 and the paint guide §2.2: 29 parts (`api.PARTS`, UUIDs `api.RIG_UUID` NN = order, tags
   `rlk_room rlk_mb_aux rlk_mb_part rlk_hr_part rlk_hr_<part>`) + the shadow (nn 0x40, r 0.9); billboard fixed, view
   range 2, culling 8 × 8, brightness 13 (`sword_glow` 15); 2.55 b to the head top, the flat brim Ø 1.60 as four squares
   at 0 / 22.5 / 45 / −22.5° stacked 0.003 b apart, each painting only its own wedges (no coplanar faces, no stacked
   translucency); every part has its ghost model (same geometry, `rlk:mboss/scarlet/ghost` texture); hands
   `api.HANDS`; the props `cup` / `bottle` (`api.PROP_STATES`). Objectives `hrRig*` only. Every call of `api.RIG_CALLS`
   + `play/<clip>` / `start/<clip>` for all 47 clips + `face/set {yaw}` + `anchor/<name>` (moves the one `rlk_hr_anchor`
   marker). The look states and re-parenting of `api.REPARENT` (hat worn / back / hand / world / gone, scabbard hand /
   hip / gone with the sheathed hilt, …). **Originality**: nothing of the original costume (PLAN §1.5 "not reproduced"
   column); neutral names only (`scarlet`, `hr`, the role names of §2.3) — never name a part, texture or model after the
   original game's pieces; base paints keep ΔE ≥ 10 from the model.md §2 values the test lists.
2. The **39 clips owned `S2a`** in `api.CLIP_OWNER` (the fight / gauntlet clips and `ev_give` / `ev_toast` / `ev_leave`)
   with exactly `api.CLIPS` (len, loop, events; a clip's end is its length). Big swings keyed every tick (≤ 120° per
   tick); quiet beats every 2-4 t; blade low across her front in idle / walk / guard (tip ≥ 0.10 b over the floor); held
   props right from the side; root motion never in a clip (the module moves the body).
3. The 8 cinematic clips (`intro`, `intro_end`, `cs1`, `sq1`, `repel`, `lead_down`, `lead_stand`, `ending`) belong to
   S2b's `T:scarlet_cine.mjs`: your generator imports that module when it exists and otherwise uses a **built-in
   placeholder** (static poses with the contract lengths / events) so the manifest always carries all 47 clips. Do not
   create `T:scarlet_cine.mjs` yourself.
4. The model `rlk:mboss/scarlet/item_sword` (`api.ITEM_MODEL`): the rig's own sheathed sword + scabbard as one piece, same
   texture (0 extra px), gui / hand / ground / fixed transforms (points the right way, nothing below the floor).
5. `T:scarlet_rig_manifest.json` = the stub schema + transforms / models / budgets / sprites; `api.check_manifest` passes.
   Build gates in the generator: no part / blade tip / scabbard tip / brim / hair / skirt below the floor at any compiled
   tick, ≤ 120° per tick, atlas ≤ 0.15 M px (plan ≈ 0.09 M), elements at rest ≤ 6 500, models inside −16..32.
Contract names you use: `api.PARTS`, `PARENTS`, `REPARENT`, `LOOKS`, `HANDS`, `PROP_STATES`, `ANCHORS`, `RIG_CALLS`,
`RIG_MACRO_CALLS`, `CLIPS`, `CLIP_OWNER`, `RIG_UUID`, `SHADOW_NN`, `TAGS`, `RP_RIG`, `GHOST_MODEL`, `ITEM_MODEL`,
`check_manifest`.

**④ 건드리지 말 것 (do not touch)**: `T:mboss_scarlet/**` (incl. `api.py`, the stub manifest, `seq.py`), registry, core,
kit, arena, other bosses' rigs and RIGLIB, the player avatar files (`T:build_player_rig.mjs`, `T:player_motion/**`,
`F:char/**`, `F:player/**`) — read-only; `T:scarlet_cine.mjs` (S2b's). Requests: `HR/requests/s2a.md`.

**⑤ 시험 (tests)**: `HR/tests/test_rig.py` (style of `R:tools/dev/sim/ar/tests/test_rig.py`, run from outside the
datapack): manifest vs contract (`api.check_manifest`, 47 clips); floor-dip and ≤ 120°/t over every clip tick (blade tip,
scabbard tip, brim, hair, skirt); hat states; the brim squares not coplanar; ghost models use only the ghost texture;
UUIDs / tags; `rig/kill` + `uninstall` leave nothing; `look/*` idempotent; the palette-distance check of PLAN §1.5 (ΔE ≥ 10
from hat top `#E6DCCF`, bodysuit `#E4E2E8`, thigh-highs `#CFCBD3`, tasset `#8E6CB4`, gold strip `#CDB78C`, hair
`#DDD7E2` for the same roles); the model `item_sword` (gui / hand / ground / fixed transforms, rig texture only).

**⑥ 그림 (renders)** (≤ 640 px jpg in `HR/renders/`, delete intermediates): `s2_U1.jpg` (front / side / back / ¾ of the
normal form, the P2 accents, the ghost form, the five hat states and the iaido stance, beside a 1.8 b player stand-in) and
`s2_orig.jpg` (the originality sheet: per PLAN §1.5 row the reference crop `HR/ref/model_hat_top.jpg`, `model_front.jpg`,
`model_back.jpg`, `model_legs.jpg`, `model_sword_hilt.jpg`, `model_sword_scab.jpg`, `model_colors.jpg` beside your part,
captioned with what differs) — **send both paths to the lead as soon as they exist** (they go to the user early); clip
strips every 2 t `s2_clip_<clip>.jpg` (beside the PLAN §10 pattern sheets of that move); `s2_props.jpg`, one side render per
held-prop pose (blade low in idle, iaido stance, the draw, the sheathe, the scabbard at the hip and in the hand, the hat in
the hand and on the back); `s2_brim.jpg`, a close side view of the brim at rest and tilted; `s2_item_sword.jpg`, the
`item_sword` model in gui, hand and ground transforms. Your render names all start with `s2_` (S2b uses `s2b_`).

**⑦ 게이트 (gates)**: loadcheck — **pending the user's EULA consent** (do not start the server; say so); `python3 -I
tools/dev/rplint.py HR/rp_s2a` → 0; the rig build twice → identical (datapack and the RP hash); `bash
HR/tools/regen_d0.sh <wt>/roguelike` → only your files change (`build_player_rig.mjs` outputs untouched);
`python3 tools/check_mboss_pack.py` → 0; `python3 tools/mboss_scarlet/api.py --check` green; budgets (rig ≤ 0.15 M px,
elements at rest ≤ 6 500, the stitched atlas ≤ 13.2 M with `python3 -I tools/dev/atlas_px.py HR/rp_s2a`); `bash
HR/tools/checkers.sh <wt>/roguelike` → no new finding; your suite green; the standing rules: no negative literals in
`scoreboard players add/remove`, lowercase ids, nothing below the floor, no teleport into blocks, held props right from the
side, big swings keyed every tick, `summon` ignores the execute rotation; never hand-edit generated outputs.

**⑧ 커밋 (commit)** on `wip/hr-s2a` in your worktree only; never push; the RP stays out of git (report its hash). The
message ends with exactly these two lines and names no model anywhere else:
`<세션이 정해 준 trailer>`
Disk is tight (≈ 1.7 GB free): one RP copy, delete render intermediates.

All stages, always: never hand-edit generated outputs (change the generator, regenerate); the real-game traps — no negative literals in `scoreboard players add/remove`, no glyph-font inheritance, lowercase resource ids, nothing below the floor, no teleport into blocks, held props pointing the right way, one display card per projectile, `summon` does not take the execute rotation; originality (PLAN §1.5): names stay neutral (`scarlet` / `hr`), never name a part, texture, model, function or file after the original game's costume or level pieces; the EULA consent is not recorded, so the local test server is never started.

**⑨ 보고 (report)**: your head commit (S2b branches from it), part / clip / element / px numbers, function count, the RP
hash, render paths (U1 + originality first), fidelity notes per clip, test counts, "loadcheck pending the user's EULA
consent", requests (`HR/requests/s2a.md`), and for S2b: how the generator imports `scarlet_cine.mjs` (the export shape).

---------------------------------------------------------------------------------------------------------------------

## S2b — the 8 cinematic clips + the sequences (CS0 / CS1 / SQ1 / CS2-CS3 / lead-ins / CS4 / the event coda)

**① 너는 (you are)** making the cinematic clips and the sequence bodies of the special boss 홍련 (Scarlet; module
`scarlet`, function root `boss/scarlet`) in a Minecraft Java 26.3 roguelike datapack (namespace `rlk`, Korean UI;
repository `/home/user/rlk`, datapack root `roguelike/`). Worktree `S:hr/wt_s2b` =
`/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/hr/wt_s2b`, branch `wip/hr-s2b`, base =
**the head of `wip/hr-s2a`** that S2a reported (`git -C /home/user/rlk rev-parse wip/hr-s2a`; if the worktree is missing:
`git -C /home/user/rlk worktree add /tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/hr/wt_s2b
-b wip/hr-s2b wip/hr-s2a`; never touch `/home/user/rlk` otherwise). Your RP: `cp -r S:hr/rp_s2a S:hr/rp_s2b` if S2a's copy
still exists, else `cp -r S:ar/rp_i1 S:hr/rp_s2b` and rebuild the rig into it (plain copies, never hard links; `df -h /` ≥
800 MB first). Abbreviations: `S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`, `HR` =
`S:hr`, `R:` = `<worktree>/roguelike`, `F:` = `R:data/rlk/function`, `T:` = `R:tools`.

**② 먼저 읽을 것 (read first)**: `R:README.md` chapter 0 (0-4, 0-5, 0-6, 0-7) and the 타키 / 아를레키노 sections; `HR/PLAN.md`
**§3 (all: §3.0 the division of work, the tools, the lines table; §3.1-§3.8 every beat)**, §1.2-§1.5, §2.4-§2.7, §5.4-§5.5
(the deflect, the fail staging), §7.1.2 and **§7.3.2-§7.3.3** (the event coda, both branches, texts), §9.2 (Sequences,
Event hand-off), §9.3 (`ev_dry.py`, the cinematic part of `test_rig.py`), §9.4, §11 (FI-1, FI-5, FI-6, FI-8-FI-12, FI-20,
FI-23); `HR/understand/cutscenes.md` (shot by shot) and `critic.md`; `HR/contract.md` (§1-§4; §3.5 sequences and the
signal, §3.7 the event); `T:mboss_scarlet/api.py` §5 (`SEQS`, `SEQ_CLIPS`, `SEQ_ARGS`, `SEQ_EXTRA`, `SEQ_LEN`,
`SEQ_SIGNAL`, `SIG`, `LINES`, `LINE_AT`, `MUSIC_AT`), §3 (`COUNTER_EV`, `SKIP_*`, `ULT60_LETHAL`, `ULT5_LETHAL`,
`DARK_*`), §7 (`CLIPS`, `CLIP_OWNER`, `rig`, `play`, `ev`), §8 (`K`), §9 (`Service`, `Writer`, `OWN['S2b']`, `music`),
§9b (`EVENT`, `EV_T`, `EV_TEXT`, `TAGS['ev']`, `ITEM_MODEL`, `ev_apply`, `ev_title`); S2a's `T:scarlet_rig_api.md`,
`T:build_scarlet_rig.mjs` (how it imports `scarlet_cine.mjs`) and the ar S2 sequence precedent
`T:mboss_arlecchino/seq.py`; the sheets of PLAN §10 (Intro CS0, CS1, SQ1, CS2 / CS3, Down + lead-in, CS4, Subtitles).

**③ 목표 (goals)** — your files: new `T:scarlet_cine.mjs` (the 8 clips owned `S2b` in `api.CLIP_OWNER`: `intro` 554,
`intro_end` 86, `cs1` 213, `sq1` 60, `repel` 104, `lead_down` 82, `lead_stand` 70, `ending` 1042, exactly `api.CLIPS`),
`T:mboss_scarlet/seq.py`; `HR/tests/ev_dry.py` (+ the cinematic checks in `HR/tests/test_rig.py`, which you take over from
S2a, `api.HANDOVER`); `HR/s2b/readme_seq.md` (your scratch is `HR/s2b/`).
You also rebuild S2a's unchanged generator (`node tools/build_scarlet_rig.mjs --resourcepack HR/rp_s2b`) and commit the rig
outputs / manifest it changes because of your clips (never S2a's sources).
1. The 8 cinematic clips beat by beat (PLAN §3.1-§3.7: the poses, the hat / sword / scabbard / face states at their
   events, big swings keyed every tick, nothing below the floor), matched against the footage sheets.
2. `seq.py`: `SERVICES` = one `api.Service` per `api.SEQS` (`intro`, `cs1`, `sq1`, `repel`, `lead_down`, `lead_stand`,
   `ending`, `event`); each `build(W)` writes only `seq/<name>/{start,tick,cancel}` (+ `seq/intro/skip`) with
   `W = api.Writer('S2b', api.OWN['S2b'])`, clock `#sq hr`, `#sqdone hr 1` at the end, `cancel` idempotent; `repel
   {at:60|5}`, `lead_stand {g:"a8"|"a13"}`. Every effect on a clip event (`api.ev`); rig only via `api.rig` /
   `api.play`; effects / sounds / props / lines / overlays only via `api.K` (`api.lines(...)`; lines with
   `K.hud('line', id=…)` at `api.LINE_AT`); titles via `mboss_lib.title(*api.TITLE)` (intro_end `draw`); music via
   `api.music(ph)` at `api.MUSIC_AT`; push rings via `mboss_lib.push_ring` (no damage); body moves via `mboss/mv/*` +
   `mv/ok`; the look requests via `api.arena_look` (`crimson` in CS1 at `recolour` 173, `dark` at the SQ1 / lead-in
   `dark` event); the warning banner `K.hud('warn', on=1)` at that same event only when the gauntlet's fail is lethal
   (`api.ULT60_LETHAL` for A8, `api.ULT5_LETHAL` for A13); the staging marker `rlk_hr_stage` at tick 0 (the player's
   position and yaw).
3. **Never call core functions**: signal the core through `#sq_sig hr` = `api.SIG` in the beat's tick (`repel`: `hp1` /
   `hp2` / `hp3` at `api.COUNTER_EV` flash 24 / land 75 / kick 102 — the core applies the true damage, at 5 % the kill;
   the lead-ins: `refill` at their `refill` event — the core arms the shield). The core owns invulnerability, cine, the
   bars, the shield, floors, phase switches, the intro skip input (it calls your `seq/intro/skip`, which clears the intro
   under the black, stands her ≤ 7 b from the player and jumps to `intro_end` with line 11 on the black).
4. `seq/event` (PLAN §7.3.2, both branches, 120 t from H): `ev_give` / `ev_toast` / `ev_leave`, the thrown sword
   (`item_display` of `api.ITEM_MODEL`, summoned then rotated, one end-over-end turn ≤ 30°/t, never below the floor,
   arriving in front of the player wherever they stand) or the moonlight orb (`marker`), both tagged `rlk_room rlk_mb_aux
   rlk_hr_ev`; the kit's 8 `ev_*` presets and 7 `ev_*` sounds; lines 24 / 25 at E4 (only if `api.EVENT['lines']`), cleared
   by E52; the grant and the title at **E56 only through `api.ev_apply()` / `api.ev_title()`**; E40 `state/hidden`; E110
   `K.ovl('black', 10, 12, 0)`. `seq/ending` sets `#sqdone` at H = 1042 (the core then starts `seq/event`).
Contract names you use: `api.SEQS`, `SEQ_*`, `SIG`, `CLIPS`, `ev`, `rig`, `play`, `K`, `LINES`, `LINE_AT`, `MUSIC_AT`,
`TITLE`, `music`, `arena_look`, `COUNTER_EV`, `ULT60_LETHAL`, `ULT5_LETHAL`, `EVENT`, `EV_T`, `ITEM_MODEL`, `TAGS`,
`ev_apply`, `ev_title`, `Service`, `Writer`, `OWN`.

**④ 건드리지 말 것 (do not touch)**: `T:mboss_scarlet/{api,__init__,core,ai,shield,p1,s3lib,reward,p_ghost}.py`, the stub
manifest, S2a's sources (`T:build_scarlet_rig.mjs`, `T:scarlet_{pose,geometry,paint,clips}.mjs`, `T:scarlet_rig_api.md`),
registry, core, kit, arena, the player avatar files (`T:build_player_rig.mjs`, `T:player_motion/**`, `F:char/**`,
`F:player/**`). `F:boss/scarlet/seq/**` is generated by S3's generator (not on your branch): build `seq.py` in your tests
with a dummy Writer into a scratch tree and do not commit `seq/**`. Requests: `HR/requests/s2b.md`.

**⑤ 시험 (tests)**: `HR/tests/ev_dry.py` (with S1K's kit names; both branches 120 t; every kit call exists in the contract;
lines cleared before E56; title at E56, black at E110, subtitle cleared before it; the sword prop's rotation set after
summon, never below the floor, arriving in front of the player from 8 player positions incl. 20 b away; rig hidden at E40;
cancel leaves nothing); the cinematic part of `test_rig.py` (the 8 clips vs the contract, floor-dip and ≤ 120°/t, hat
states at their events); `seq.py` builds with a dummy Writer and writes only `seq/**`; every tick a sequence uses exists in
its clip; no function reference outside `seq/**`, `rig/**`, the kit (through `api.K`) and the framework; CS4: her distance
to an unmoving player over 300-1042 stays 3.5-6 b.

**⑥ 그림 (renders)** (≤ 640 px jpg in `HR/renders/`, delete intermediates): the cinematic strips `s2b_<clip>.jpg` every 4 t
(`intro`, `intro_end`, `cs1`, `ending`) and every 2 t (`sq1`, `repel`, `lead_down`, `lead_stand`), next to the footage sheets
`v1s_intro_*`, `v2f_cs_*`, `v2f_c*` / `v3r_c*`, `v3r_a_kipup`, `v3r_e_*`, `v4k_*`, `v5e_*` (incl. CS1's two petal cards and
the CS4 walk-in).

**⑦ 게이트 (gates)**: loadcheck — **pending the user's EULA consent** (do not start the server; say so); `python3 -I
tools/dev/rplint.py HR/rp_s2b` → 0; the rig build twice → identical (datapack and RP hash); `bash HR/tools/regen_d0.sh
<wt>/roguelike` → only your files and the rig outputs your clips change; `python3 tools/check_mboss_pack.py` → 0;
`python3 tools/mboss_scarlet/api.py --check` green; `bash HR/tools/checkers.sh <wt>/roguelike` → no new finding; your
suites green; the standing rules: no negative literals in `scoreboard players add/remove`, no glyph-font inheritance,
lowercase ids, nothing below the floor, no teleport into blocks, held props right from the side, big swings keyed every
tick, one display card per projectile, `summon` ignores the execute rotation; on-screen text only her 25 lines (verbatim
`api.LINES`), the names, the intro's skip prompt, §7's item / buff names / numbers / notices; no camera, no input lock;
never hand-edit generated outputs.

**⑧ 커밋 (commit)** on `wip/hr-s2b` in your worktree only; never push; the RP stays out of git (report its hash). The
message ends with exactly these two lines and names no model anywhere else:
`<세션이 정해 준 trailer>`
Disk is tight (≈ 1.7 GB free): delete S2a's RP copy once yours exists (ask the lead), delete render intermediates.

All stages, always: never hand-edit generated outputs (change the generator, regenerate); the real-game traps — no negative literals in `scoreboard players add/remove`, no glyph-font inheritance, lowercase resource ids, nothing below the floor, no teleport into blocks, held props pointing the right way, one display card per projectile, `summon` does not take the execute rotation; originality (PLAN §1.5): names stay neutral (`scarlet` / `hr`), never name a part, texture, model, function or file after the original game's costume or level pieces; the EULA consent is not recorded, so the local test server is never started.

**⑨ 보고 (report)**: commit, clip / key-file counts, the RP hash, per-sequence function counts, footage-fidelity notes per
beat, render paths, test counts, "loadcheck pending the user's EULA consent", requests (`HR/requests/s2b.md`), what S3's
generator must do with `seq.SERVICES` (start args, the `#sq_sig` beats, `seq/intro/skip`).

---------------------------------------------------------------------------------------------------------------------

## S3 — the module core, AI, phase-1 patterns, the shield, the event logic

**① 너는 (you are)** writing the boss module of the special boss 홍련 (Scarlet; module `scarlet`, registry n 21, function
root `boss/scarlet`, arena `hr_field`) for the existing special / chapter-boss framework (`F:mboss/`, chapter mode) of a
Minecraft Java 26.3 roguelike datapack (namespace `rlk`, Korean UI; repository `/home/user/rlk`, datapack root
`roguelike/`): the generator, the 17 hooks, the phase machine, the AI, A1-A10, the shield and the event logic. Worktree
`S:hr/wt_s3` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/hr/wt_s3`, branch
`wip/hr-s3`, base = **the head of `wip/hr-s1`** that S1 reported (it carries FN-a/b/c/e/f; `git -C /home/user/rlk rev-parse
wip/hr-s1`; if the worktree is missing: `git -C /home/user/rlk worktree add
/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/hr/wt_s3 -b wip/hr-s3 wip/hr-s1`; never touch
`/home/user/rlk` otherwise). Abbreviations: `S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`,
`HR` = `S:hr`, `R:` = `<worktree>/roguelike`, `F:` = `R:data/rlk/function`, `T:` = `R:tools`. S4 continues from your branch.

**② 먼저 읽을 것 (read first)**: `R:README.md` chapter 0 and the sections 중간보스 (공용 라이브러리: hz / pj / grp / pl_dot /
true_pct / mv / push / cine / floors / incoming / bars; 예고 규칙), 챕터 보스 (틀 기능), 특수 보스, 타키 (all: the special-boss
module precedent), 아를레키노 (core / AI / HUD); `HR/PLAN.md` §0, §1.2-§1.4, §3.0 and §3.8 (division, pause / reload), §4
(all), §5 (all), §6.6 (the look request), §6.7 (decor props), §7.0-§7.3 (the chain, the roll, `ev/**`, the reward hook),
§9.1-§9.5, §11; `HR/understand/framework.md` and `patterns.md`; `HR/contract.md` (all); `T:mboss_scarlet/api.py` (all) and
`__init__.py`; `T:mboss_lib.py` (hooks, helpers, `bars` from S1); the reference modules `T:build_mboss_tachy.py` +
`T:mboss_tachy/{api,core,ai,s3lib,p_melee}.py` and `T:build_mboss_arlecchino.py` + `T:mboss_arlecchino/{core,ai,p1,s3lib}.py`
(how a module generator writes hooks, the rig stub, stand-in sequences, other stages' Writers); `F:combat/apply`
(on_hit context, `#skillDmg tmp`), `F:boss/raiden/hazard/fatal` (the instant-death model for `ult/fatal`), `F:items/give`,
`F:root/give` (the inventory capacity check); the sheets of PLAN §10 (P1).

**③ 목표 (goals)** — your files: new `T:build_mboss_scarlet.py`, `T:mboss_scarlet/{core,ai,shield,p1,s3lib,reward}.py`;
outputs = the prefixes `api.OWN['S3']` under `F:boss/scarlet/` (the 17 hooks + `test/help`, `init`, `reward`, `core/ ai/
shield/ ult/ hud/ ev/ test/ rig_stub/`, `p/<key>/` for `api.P1`); `HR/tests/test_scarlet.py`, `pat_p1.py`, `test_reward.py`,
`HR/tests/lib/**` (S1 created it; yours from your start, `api.HANDOVER`: extend `hrsim.py`, keep the vendored sims
unchanged); `HR/s3/readme_scarlet.md` (the README section 「홍련 (`boss/scarlet/`)」 draft; your scratch is `HR/s3/`).
1. `build_mboss_scarlet.py` (top generator; imports `mboss_scarlet.{core,ai,shield,p1,s3lib,reward,p_ghost,seq}`) with one
   `api.Writer` per owner (`OWN['S3']`, and S4's / S2b's outputs from `p_ghost.PATTERNS` / `seq.SERVICES` through
   `api.Writer('S4', OWN['S4'])` / `api.Writer('S2b', OWN['S2b'])`); stale-file cleanup only inside owned prefixes;
   deterministic (twice → identical). Only patterns / services that exist are wired (empty lists → skip / stand-in).
2. Hooks, `init` / `uninstall` (objective `hr`, `api.CORE_FP`, the event scores `api.EV_FP` never touched by `cleanup`),
   the phase machine of PLAN §4.6 (`api.PH`): intro → P1 (floor `api.FLOOR_P1`) → CS1 (`rlk_mb_inv`, `cine`, P1 hazards
   cancelled, `api.bars(0)`, floor → `api.FLOOR_ULT`) → SQ1 (`api.bars(1)` + `shield/arm` at its tick 0) → A8 → judge
   (`#gres`) → deflect: `seq/repel {at:60}` → down (`api.DOWN_T`, normal damage, the under bar = ticks left, gold) →
   kipup → P2; fail: `ult/fail60` → `g_reform` → P2 at T + 214 (`api.FAIL60_P2_T`) → … 5 % floor → `lead_stand {g:"a13"}`
   or `lead_down` (`api.DOWN_FLOOR_WAIT` 40 t after the hit from the down window) → A13 → deflect: `seq/repel {at:5}` →
   the kill at kick → `death_start` (+ `ev/roll`) → `seq/ending` → `seq/event` (same `death_tick` when `#sqdone`) →
   `death_finish` at H + 122; fail: `ult/fatal` (Ronova revive → `api.REVIVE` → `lead_stand {g:"a13"}` → A13 again).
   Invulnerable windows of PLAN §4.6 (+ `rlk_mb_inv` while the body carries `rlk_hr_ghost`). Read `#sq_sig hr` right
   after each `seq/<name>/tick`: `hp1-3` → `api.COUNTER_PM[at][i-1]` ‰ of `mhpM` via `mboss/true_hit` (`'kill'` →
   `mboss/true_pct {pct:100}`), `refill` → `shield/arm`; reset it to 0.
3. `shield.py` (PLAN §5, `api.SHIELD_CALLS` / `api.shield()`): `shield/arm`, `shield/cut {s}` (store the lock point; pip
   check at s and s + 1 per `api.PIP_DASH`, feet within `api.PIP_R` 6.2 b, one pip per cut, never below 0, kit
   `pip_break` + sound), `shield/judge` (→ `#gres hr` 1 / 2; deflect staging: `clash_gold` + `light_column`, the sounds,
   `g_deflect`), `ult/fail60` (`pl_dot` `api.FAIL60_PM` ‰, `#mbDotLethal 0` + `push_ring(2.5, 3)`), `ult/fatal`
   (`F:boss/raiden/hazard/fatal` model: skipped while `rnDie ≥ 1`, `player/hurt_do` with all HP, through i-frames and shields;
   in a test → `mboss/test/defeat`), `shield/off`; the under bar (`#buSub` / `#buSubMax 5` / `#buSubCol` `api.BU_SHIELD`).
4. `ai.py` (PLAN §4.7): `api.BANDS`, `MID_MAX`, `WEIGHTS`, `COOLDOWN`, `TRIGGER_ONLY`, `FAR_RULE`, `REAR_RULE`,
   `COUNTER_TRIGGER` (A1 / A2 + `flinch`), `A6_TRIGGER` (from `#skillDmg tmp 1` in `on_hit`), `NO_REPEAT`, recoveries
   `api.RECOVER` with walk / strafe / P2 glide facing the player (`WALK_SPEED`, `GLIDE_SPEED`), seeded randomness.
5. `p1.py`: A1, A2, A3, A4 (+ A5), A6 (line 12 at its tick 12), A9, A10 as `api.Pattern`s per PLAN §4.3 and `api.HITS`
   (ticks from `api.ev`, shapes, tiers `api.DMG`, kb, `TRACK`, `A3_GLIDE`, `LEAP_H`, `DASH_LEN`, `A9_BEYOND`; quiet tells,
   no decal, Electro 1U, end points via `mv/ok` inside `api.MOVE_R`, the fallback `FALLBACK_R`).
6. HUD and the rest: the `bars` hook (nothing while `#hud hr 0`; the shield / down under bar), the intro skip input
   (`rlk:in_sneak` held `api.SKIP_HOLD` t inside `api.SKIP_WINDOW`; `K.hud('skip', s=0..4)` brightening, `s=5` clears;
   then `seq/intro/skip`), the look request (`#hrLook` → `api.look_job(look)` at the first tick with `#mbArBuild 0`),
   decor props at `spawn` from `api.deco()` through `api.K.prop` (tag `rlk_hr_deco`), music (`api.music`), pause / resume /
   reload / cleanup per PLAN §3.8 / §5.6, the kit wiring (contract §3.3), test ids `api.TEST_IDS` + `test/help`
   (`api.TEST_HELP_NAMES`) + `test/lock` (`api.LOCK_IDS`).
7. Stand-ins (removed by I1 when the real files exist): `rig_stub/**` while `T:scarlet_rig_manifest.json` is missing
   (every `api.rig` call name; `play/<clip>` / `start/<clip>` set `#rigc hr` to the clip id) — never when it exists; minimal
   stand-in sequences while `seq.SERVICES` is empty (wait the clip length, title / music at their events, `seq/intro/skip`,
   `#sqdone`). Never reference a function another stage has not produced (`api.K`, `api.rig`, `api.arena_look`,
   `api.look_job`, `api.bars`, `api.ev_apply` / `ev_title` handle it).
8. `reward.py` (PLAN §7.3; `SERVICES` non-empty from now on): `ev/{roll,apply,item,buff,title,record,reset}` and the FN-b
   hook `reward` (not a macro, @s = the player, positions itself `at @e[tag=rlk_body,limit=1]`): the roll at
   `death_start` (`rlk:hr ev.force` → no duplicate (`it_sword_hwamu ≥ 1` → buff, `hrMoon ≥ 1` → item) → `random value
   1..1000 ≤ api.EVENT['item_pm']`), `#hrEv` / `#hrEvDone` / `#hrEvDrop`, the grant (item: `items/enh_add` to
   `api.EVENT['item_enh']`, capacity check as `F:root/give:4-5`, `items/give {id:"sword_hwamu"}` or `#hrEvDrop 1`; buff:
   `scoreboard players set @s hrMoon 1`), the titles and chat texts exactly `api.EV_TEXT`, tests 90-92.
Contract names you use: all of `api.py` except the kit / rig internals.

**④ 건드리지 말 것 (do not touch)**: `T:mboss_scarlet/{api,__init__}.py`, the stub manifest, `seq.py` (S2b), `p_ghost.py`
(S4), the registry (it stays `enabled:false`; test with a **local uncommitted** `enabled:true` + core regeneration in a
variant tree), core / `mboss_lib` / `check_mboss_pack` (S1's, already on your base), kit, rig, arena, `tools/dev/**`, the SR
hand files (`F:items/**`, `F:player/**`), the player avatar files. Requests: `HR/requests/s3.md`.

**⑤ 시험 (tests)** (harness `HR/tests/lib` = the vendored `R:tools/dev/sim/az/tests_cm/lib` sims + `hrsim.py`; run from
outside the datapack): `test_scarlet.py` (PLAN §9.3: hooks; the phase order incl. both fail branches; floors 60 % / 5 %;
invulnerable windows; the CS2 / CS3 HP steps; the down window (both exits); pips (a timed dash at a counting cut −1
whatever its direction, disc dodges ignored, one per cut, never below 0); the judge; fail-60 (500 ‰ + the push, never kills
at 1 HP); `ult/fatal` (through i-frames and shields, skipped while `rnDie`, a revive → A13 again); the banner never on
during A8 with `ULT60_LETHAL` false nor during A13 with `ULT5_LETHAL` false, incl. restarts after pause / revive; the intro
skip (sneak held 20 t at any tick 20-540 → black, line 11 at the jump, the same end state as the full intro; released early
→ no skip); counter / skill / far / rear triggers, weights and cooldowns (seeded); bars off in CS1 and back in SQ1; the
look request through pause / reload inside a running job; pause / reload in every phase and sequence (§3.8); cleanup
leaves no `rlk_hr_*`; tick cost); `pat_p1.py` (every hit tick = its clip event; tells ≥ 12 / 20, gaps ≥ 10, lock lead 7;
shapes / tiers / kb; quiet, no decal; end points inside `MOVE_R`, never in blocks; cancel at every tick leaves nothing);
`test_reward.py` (PLAN §7.6: flow, roll 10 000 seeded 50 ± 1.5 %, inventory room / full at `invCap` 9 and 18, reload at
every tick E0-E120 and in CS4 → the outcome exactly once, words verbatim).

**⑥ 그림 (renders)** (≤ 640 px, `HR/renders/`): per P1 pattern a top-down hit-shape diagram over time
(`s3_<key>.png`).

**⑦ 게이트 (gates)**: loadcheck — **pending the user's EULA consent** (do not start the server; say so);
`python3 tools/build_mboss_scarlet.py` twice → identical; `bash HR/tools/regen_d0.sh <wt>/roguelike` → only your files
change; `python3 tools/check_mboss_pack.py` → 0; `python3 tools/mboss_scarlet/api.py --check` green; average commands per
fight tick ≤ Apep's ≈ 830 (target ≤ 600); `bash HR/tools/checkers.sh <wt>/roguelike` → no new finding; your suites
green; the standing rules: no negative literals in `scoreboard players add/remove` (use `operation -=`), no glyph-font
inheritance, lowercase ids, nothing below the floor, no teleport into blocks (`mv/ok`), one display card per projectile,
`summon` ignores the execute rotation, no floor decal, quiet tells ≥ 12 / 20 t, no tip text (only names, her lines, the
skip prompt, the lethal banner, §7 names / numbers / notices); never hand-edit generated outputs.

**⑧ 커밋 (commit)** on `wip/hr-s3` in your worktree only; never push. The message ends with exactly these two lines and
names no model anywhere else:
`<세션이 정해 준 trailer>`
Disk is tight (≈ 1.7 GB free): variant trees under your test folder only, deleted after use.

All stages, always: never hand-edit generated outputs (change the generator, regenerate); the real-game traps — no negative literals in `scoreboard players add/remove`, no glyph-font inheritance, lowercase resource ids, nothing below the floor, no teleport into blocks, held props pointing the right way, one display card per projectile, `summon` does not take the execute rotation; originality (PLAN §1.5): names stay neutral (`scarlet` / `hr`), never name a part, texture, model, function or file after the original game's costume or level pieces; the EULA consent is not recorded, so the local test server is never started.

**⑨ 보고 (report)**: your head commit (S4 branches from it), function counts per subtree, the per-tick command cost of a
fight tick (vs Apep), test counts, render paths, "loadcheck pending the user's EULA consent", requests
(`HR/requests/s3.md`), and what S4 / S2b must know (the `shield/*` semantics as built, the `#sq_sig` reading order, how a
gauntlet ends and hands back `#gres`).

---------------------------------------------------------------------------------------------------------------------

## S4 — the ghost patterns: R1-R3 and the gauntlets A8 / A13

**① 너는 (you are)** writing the phase-2 ghost patterns and the two gauntlets of the special boss 홍련 (Scarlet; module
`scarlet`, function root `boss/scarlet`) in a Minecraft Java 26.3 roguelike datapack (namespace `rlk`, Korean UI;
repository `/home/user/rlk`, datapack root `roguelike/`), on top of S3's module. Worktree `S:hr/wt_s4` =
`/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/hr/wt_s4`, branch `wip/hr-s4`, base = **the
head of `wip/hr-s3`** that S3 reported (`git -C /home/user/rlk rev-parse wip/hr-s3`; if the worktree is missing:
`git -C /home/user/rlk worktree add /tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/hr/wt_s4
-b wip/hr-s4 wip/hr-s3`; never touch `/home/user/rlk` otherwise). Abbreviations: `S:` =
`/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`, `HR` = `S:hr`, `R:` = `<worktree>/roguelike`,
`F:` = `R:data/rlk/function`, `T:` = `R:tools`.

**② 먼저 읽을 것 (read first)**: `R:README.md` chapter 0 and the sections 중간보스 → 공용 라이브러리 (hz / pj / grp / mv /
`mv/ok` / push / pl_dot), 타키 (the aerial patterns of S4's precedent); `HR/PLAN.md` §1.3-§1.4, §3.5-§3.6, §4.1-§4.2,
**§4.4-§4.5 (the move set table, the A8 / A13 scripts, the disc)**, **§5 (all)**, §6.5-§6.6 (the darkness), §9.2 (Shield),
§9.3 (`pat_ghost.py`), §11 (FE-2, FE-12, FI-22); `HR/understand/patterns.md` §5, §10 and `critic.md` (C30-C58);
`HR/contract.md` (all; §3.5-§3.6); `T:mboss_scarlet/api.py` §2 (`HITS`, `CUT_R`, `LOCK_LEAD`, `TELL_*`, `MOVE_R`,
`FALLBACK_R`, `DISC`), §3 (`A8_SCRIPT`, `A13_SCRIPT`, `R1`, `R2`, `R2_TWO_PCT`, `R3`, `SCRIPTS`, `CUT_IDS`,
`DISC_RELEASE`, `BOLTS`, `JUDGE_T`, `REPEL_T`, `DARK_*`, `REAPPEAR`, `FAIL5_T`, `ULT*_LETHAL`), §7 (`CLIPS`, `ev`, `play`,
`rig`), §8 (`K`), §9 (`Pattern`, `Writer`, `OWN['S4']`, `cut`, `CUT_CALLS`, `CUT_ARGS`, `disc`, `shield`,
`SHIELD_CALLS`); S3's `T:build_mboss_scarlet.py`, `T:mboss_scarlet/{core,shield,p1,s3lib}.py` and its report; the sheets of
PLAN §10 (SQ1 + A8, A13, discs).

**③ 목표 (goals)** — your files: `T:mboss_scarlet/p_ghost.py`; outputs `F:boss/scarlet/p/{r1,r2,r3,a8,a13}/**` and
`F:boss/scarlet/g/**` (= `api.OWN['S4']`, written by S3's generator — run `python3 tools/build_mboss_scarlet.py`);
`HR/tests/pat_ghost.py`; `HR/s4/readme_ghost.md`.
1. `PATTERNS` = `api.Pattern` for `r1`, `r2`, `r3`, `a8`, `a13` (test ids 11-13, 21-29), each following its
   `api.SCRIPTS` rows exactly (clip starts, cuts, disc releases), every effect / sound at its clip event (PLAN §4.5 move
   table: `ghost_burst`, `ghost_trail`, `qi_*`, `glint`, the sounds `g_*`), the form switches (`rig/look/form/ghost` at T0
   for the lilac tell, `form/normal` at the dive's reappearance) and the body tag `rlk_hr_ghost` while in ghost form (the
   core keeps `rlk_mb_inv` on a body with that tag), `g_reform` / `solid` per the R1 / R3 rows.
2. The ghost helpers `g/**`: the cut builder `g/cut/make {s,t,dmg,kb,n}` / `g/cut/aim {s}` / `g/cut/lock {s}` exactly as
   `api.cut()` emits them (a quiet Electro `mboss/hz/disc` of `api.CUT_R` at the player's feet via `hz_opts(quiet=1, el=3,
   kb=…, act=2)`, tagged `rlk_hr_cut`, re-aimed every tick with `mboss_lib.hz_aim()` until the lock, fixed from the lock;
   `g/cut/lock` calls `shield/cut {s}` when n = 1); `g/disc/throw {kb}` exactly as `api.disc()` (one `pj/launch` per
   `api.DISC`, blade shape, aimed at the player's position at release, wall stop, one kit card `fx/prop/disc` summoned then
   rotated); reappear points per `api.REAPPEAR` with `mv/ok` inside `api.MOVE_R` 22.5 and the guaranteed fallback on the
   player → C line ≤ `api.FALLBACK_R`; never in blocks; the decoration bolts `deco_bolt` at `api.BOLTS` (no hit).
3. The gauntlet frame: T0 = the pattern's start (SQ1 / the lead-ins already made it dark and, if lethal, showed the
   banner); the judge at `api.JUDGE_T` calls `shield/judge` (S3's: on a deflect it plays the PLAN §5.4 staging incl.
   `g_deflect` itself); then darkness lifts (`api.arena_look('crimson')`), banner off, and on a deflect `#done` at
   `api.REPEL_T` (the core starts `seq/repel`); fail → A8: `ult/fail60` + `g_reform`
   (P2 at T + 214); A13: the instant-death staging of `api.FAIL5_T` + `ult/fatal`. `cancel` removes cuts, discs, the ghost
   tag, the banner, requests `crimson`; idempotent (pause / revive restart via the core's `lead_stand`).
4. Counting cuts: the nine per gauntlet (`api.CUT_IDS`); R1 / R3 cuts never count (`count=0`); discs and the dive never
   count. Tiers / kb from the script rows (`api.HITS` derives the same).
Contract names you use: `api.SCRIPTS` and the rows above, `cut`, `disc`, `shield`, `HITS`, `DMG`, `CUT_R`, `LOCK_LEAD`,
`TELL_MIN`, `MOVE_R`, `FALLBACK_R`, `DISC`, `REAPPEAR`, `BOLTS`, `JUDGE_T`, `REPEL_T`, `FAIL5_T`, `CUT_IDS`, `K`, `play`,
`rig`, `ev`, `arena_look`, `Pattern`, `Writer`, `OWN`, `TAGS`.

**④ 건드리지 말 것 (do not touch)**: every other file in `T:mboss_scarlet/` (S3's core / shield / p1 / reward, S2b's
`seq.py`, the lead's `api.py`), the generator `T:build_mboss_scarlet.py` (S3's: run it, do not edit it), registry, core,
kit, rig, arena, the SR hand files, the player avatar files (`T:build_player_rig.mjs`, `T:player_motion/**`, `F:char/**`,
`F:player/**`). Requests: `HR/requests/s4.md`.

**⑤ 시험 (tests)**: `HR/tests/pat_ghost.py` (S3's harness `HR/tests/lib`, read only; your own helpers in `HR/s4/`): every
hit tick = its clip event and the §4.5 tables; tells ≥
12 / 20, gaps ≥ 10, lock lead 7; shapes / tiers / kb; quiet, no decal; every counting cut made ≥ 12 t before its strike,
following the player until the lock, act 2, dodgeable; the pip window in the sim with four dash agents — stand-then-dash,
and move-then-dash outward / sideways / inward at 0.22 and 0.28 b/t — each scoring with ≥ 90 % of correctly timed dashes;
discs (speed, aim at release, wall stop, one card); reappear points (bearings, distances, `mv/ok` within `MOVE_R` 22.5
with the player at r 22 facing outward, the guaranteed fallback, never in blocks); the darkness ticks; a 2-charge dasher
reaches every counting window; cancel at every tick leaves nothing.

**⑥ 그림 (renders)** (≤ 640 px, `HR/renders/`): per pattern a top-down hit-shape diagram over time (`s4_<key>.png`) and one
gauntlet timeline chart per gauntlet `s4_timeline_a8.png` / `s4_timeline_a13.png` (cut ticks, lock ticks, dash windows,
pips).

**⑦ 게이트 (gates)**: loadcheck — **pending the user's EULA consent** (do not start the server; say so);
`python3 tools/build_mboss_scarlet.py` twice → identical; `bash HR/tools/regen_d0.sh <wt>/roguelike` → only your outputs
change; `python3 tools/check_mboss_pack.py` → 0; `python3 tools/mboss_scarlet/api.py --check` green; S3's suites still
green; `bash HR/tools/checkers.sh <wt>/roguelike` → no new finding; your suite green; the standing rules: no negative
literals in `scoreboard players add/remove`, nothing below the floor, no teleport into blocks (`mv/ok`), one display card
per projectile facing its flight, `summon` ignores the execute rotation (rotate after), no floor decal, tells ≥ 12 / 20 t,
cuts kb 0 except the scripts' last hits; never hand-edit generated outputs.

**⑧ 커밋 (commit)** on `wip/hr-s4` in your worktree only; never push. The message ends with exactly these two lines and
names no model anywhere else:
`<세션이 정해 준 trailer>`
Disk is tight (≈ 1.7 GB free): variant trees under your test folder only, deleted after use.

All stages, always: never hand-edit generated outputs (change the generator, regenerate); the real-game traps — no negative literals in `scoreboard players add/remove`, no glyph-font inheritance, lowercase resource ids, nothing below the floor, no teleport into blocks, held props pointing the right way, one display card per projectile, `summon` does not take the execute rotation; originality (PLAN §1.5): names stay neutral (`scarlet` / `hr`), never name a part, texture, model, function or file after the original game's costume or level pieces; the EULA consent is not recorded, so the local test server is never started.

**⑨ 보고 (report)**: commit, function counts, the gauntlet timelines as built, pip-agent results, test counts, render paths,
"loadcheck pending the user's EULA consent", requests (`HR/requests/s4.md`).

---------------------------------------------------------------------------------------------------------------------

## SR — the reward item 「[ MYTHIC ] 화무십일홍」 and the buff 「월하대작」 (hand-maintained files)

**① 너는 (you are)** adding the two outcomes of the special boss 홍련's random event to a Minecraft Java 26.3 roguelike
datapack (namespace `rlk`, Korean UI; repository `/home/user/rlk`, datapack root `roguelike/`): the mythic item
「[ MYTHIC ] 화무십일홍」 (`sword_hwamu`) and the run buff 「월하대작」 (`hrMoon`), both in hand-maintained source files (no
generator). Worktree `S:hr/wt_sr` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/hr/wt_sr`,
branch `wip/hr-sr`, base `wip/hr-d0` = **5d2c3ac** (if missing: `git -C /home/user/rlk worktree add
/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/hr/wt_sr -b wip/hr-sr 5d2c3ac`; never touch
`/home/user/rlk` otherwise). Abbreviations: `S:` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`,
`HR` = `S:hr`, `R:` = `<worktree>/roguelike`, `F:` = `R:data/rlk/function`, `T:` = `R:tools`. S3 (another branch) rolls and
grants them (`items/give {id:"sword_hwamu"}`, `scoreboard players set @s hrMoon 1`); you build what is granted.

**② 먼저 읽을 것 (read first)**: `R:README.md` chapter 0 (0-5, 0-6) and **6 (아이템: the def format, `tk` placeholders,
등급 규칙, item damage recipe ≈ README:859, `#sub itv`, tune tables ≈ :876-:882)**, 12 / 12-1 (각인), the sections 시점
(`vBig`, the F5 crosshair title ≈ :1979-:1986), 조절 지점; `R:items.md` (conventions, the mythic list); `HR/PLAN.md` **§7.4
(all: identity, numbers per star with the exact rounding, the def text verbatim, cues, the file table §7.4.6, balance)**,
**§7.5 (the buff: B1, §7.5.2 the file table, §7.5.3 the forever variant)**, §7.3.3-§7.3.4 (texts, how S3 grants), §7.6
(`test_hwamu.py`, `test_moon.py`), §7.7, §11 (FE-5, FE-9, FE-14, FI-16); `HR/plan/reward.md` (the original of §7) and
`HR/wiki/w2.txt` (l.405 / l.411 / l.522 / l.633: quote only verbatim); `HR/contract.md` (§1 SR row, §2, §3.7, §4, §5);
`T:mboss_scarlet/api.py` §9b (`ITEM_ID`, `ITEM_NAME`, `ITEM_SCORE`, `ITEM_MODEL`, `ITEM_VANILLA`, `BUFF_OBJ`,
`BUFF_NAME`, `BUFF_FP`, `BUFF_VALUES`, `ITEM_SND`, `EVENT`, `EV_TEXT`) and §8 (`VIG`, `FONT`); the precedent items
`F:items/mythic/*/def` (e.g. `ember_oath`), `F:items/proc/salon_pay`, the counter of 불사자의 갈기, `F:items/tune/{b10,
register,apply_loop,stat_one,stats_scale}`, `F:snd/f134` (the sound-wrapper pattern), `F:room/obj/do_hp` (the node-buff
precedent), `F:player/{take_damage,dash_iframe,reset_one,update_item,update_item_macro}`, `F:items/hook/*`.

**③ 목표 (goals)** — your files (PLAN §7.4.6 / §7.5.2): lines in `F:items/register` (def call after ≈ :113, `impl` list),
`F:items/build_rarbuckets` (`box_exclude` += `"sword_hwamu"`), `F:items/tune/b10` (constants + `t.sword_hwamu` + ids),
`F:items/hook/{on_hit,stat_buffs,tick_player,on_cast_burst}` (one line each), optional `F:items/enh_add` (the ★★★ line, w2
l.522 verbatim); new `F:items/mythic/sword_hwamu/def` (§7.4.4 verbatim: the def with both lore lines w2 l.633 / l.411,
model `rlk:mboss/scarlet/item_sword` = `api.ITEM_MODEL`, engravings `["berserk","keen"]`), new `F:items/proc/hw_{hit,stack,
cost,stat,tick,ctr_q,ctr,slash_q,slash,slash_fx,ready,clear}`; `F:player/take_damage` (after ≈ :37) and
`F:player/dash_iframe` (after ≈ :2) one line each; `F:player/reset_one` (`hrMoon 0`, run scope), `F:player/update_item` +
`F:player/update_item_macro` (the `$(moon)` lore line = `api.EV_TEXT['status']`), new `F:player/hr_moon/apply`;
`F:codex/labels` (`lab.sword_hwamu`); new `F:snd/f422`-`f429` (keys `#k352`-`#k359`, free at D0); `F:load` (objective
`hrMoon`, the 조절 지점 constants `#hrMoonAtk 20` / `#hrMoonCrit 10` / `#hrMoonSpd 10` tmp = `api.BUFF_VALUES['run']`) and
`F:uninstall` (remove `hrMoon`); `R:items.md` (the 8th mythic entry, §7.4.4 text, and the 등급 규칙 exception line);
`HR/tests/test_hwamu.py`, `HR/tests/test_moon.py`; README fragments `HR/sr/readme_items.md` (§6 item list + the 등급 규칙
exception 「예외(사용자 요청 11-04): 화무십일홍 …」 verbatim from PLAN §7.4.1, the boss section's item / buff rows).
1. The item exactly per PLAN §7.4.1-§7.4.5: numbers per star (`(base × fac + 500) / 1000`), 육참골단 (every 4th basic hit
   +1 stack ≤ 5, refresh, −4 % of current HP above 50 %, never below 1, `operation -=` only), 검신합일 (on a landed hit
   or a dash's i-frames eating it; nearest `rlk_mob` ≤ 12 b; 2 s cooldown; queued, dealt next tick; crit dmg at HP ≤ 60 %),
   홍련일섬 (from `on_cast_burst`, 40 s ICD, 4-t delay, every `rlk_mob` ≤ 20 b once, crit rate if HP ≤ 50 % at the cast,
   the optional edge vignette = a title of glyph `api.VIG` U+EC16 in font `rlk:mboss_hr` with an empty unstyled root and
   `font` on the component, skipped while `vBig ≥ 1`); item damage by the README recipe with **`#sub itv 1`**, `#elem 3`,
   `#elU 1000`; never offered by boxes / shop / level-up / 나무뿌리 (`box_exclude`); codex label; sounds through the
   `f422`-`f429` wrappers (vanilla ids of §7.4.5); state and sidebar cleared when sold / dropped.
2. The buff per §7.5.2: `hrMoon` per player, `stat_buffs` adds `ampAtk` / `critChance` / `moveSpeed` from the three
   constants, `reset_one` clears it (run scope; the forever switch keeps it, §7.5.3), `uninstall` removes it, the stat-item
   lore line through `update_item_macro`'s `$(moon)` (no item modifier).
3. Hook lines from generators live in some of these files (`F:load` / `F:uninstall` carry `# rift (build_rift.py)` and ch2 /
   ch3 mob-generator lines; `combat/*` too): add your lines beside them, never edit theirs.
Contract names you use: `api.ITEM_ID`, `ITEM_NAME`, `ITEM_SCORE`, `ITEM_MODEL`, `ITEM_VANILLA`, `BUFF_OBJ`, `BUFF_NAME`,
`BUFF_FP`, `BUFF_VALUES`, `ITEM_SND`, `VIG`, `FONT`, `EV_TEXT`, `EVENT['buff_scope']`.

**④ 건드리지 말 것 (do not touch)**: any generator or generated output (`tools/**` except reading, `F:mboss/**`,
`F:boss/**`, `F:room/rift/**`, the ch2 / ch3 generated `cm/` files), `T:mboss_scarlet/**`, the registry, kit, rig, arena,
other items' behaviour (only the lines PLAN §7.4.6 / §7.5.2 name), the player avatar files (`T:build_player_rig.mjs`,
`T:player_motion/**`, `F:char/**`) and every `F:player/**` file not named above. Requests: `HR/requests/sr.md`.

**⑤ 시험 (tests)** (harness of `R:tools/dev/sim/ar/tests`: the vendored `R:tools/dev/sim/az/tests_cm/lib` sims in
`HR/tests/lib` — S3's, read only; your own helpers in `HR/sr/` — azsim runs `combat/apply`, `player/take_damage` etc. from
the datapack; run from outside the datapack): `test_hwamu.py` (def /
register / `impl` / `box_exclude` / codex label / engravings / `items.md` mirror; never offered (`pick_cand` / shop /
나무뿌리 buckets); the tune table vs §7.4.3 for stars 0-3 (exact rounding); stacks 4 hits → 1, max 5, refresh, all drop at
0; HP cost 4 % of current above 50 %, none at ≤ 50 %, never below 1, no negative literals; counter on a landed hit and on
`dash_iframe`, 2 s cooldown, nearest ≤ 12 b, no target = no cooldown, queued; crit dmg only at ≤ 60 %; slash only from
`on_cast_burst`, ICD, 4-t delay, every `rlk_mob` ≤ 20 b once, crit rate only if HP ≤ 50 % at the cast; `#sub itv 1` on all
item damage; state and sidebar cleared when sold / dropped; sounds in `sound_ids.txt`; the `vig` title skipped while
`vBig ≥ 1`; both lore lines equal w2 l.633 / l.411); `test_moon.py` (`stat_buffs` adds exactly +20 `ampAtk` / +10 crit /
+10 move when `hrMoon 1`; final ATK = old × 1.20 (±1); `reset_one` clears (run) / keeps (forever switch); `uninstall`
removes; the stat-item lore line present iff on, its numbers = the constants).

**⑥ 그림 (renders)**: the item tooltip and the stat item, rendered as text (`HR/renders/sr_tooltip.txt`,
`sr_stat_item.txt`).

**⑦ 게이트 (gates)**: loadcheck — **pending the user's EULA consent** (do not start the server; say so);
`bash HR/tools/regen_d0.sh <wt>/roguelike` and the mob generators `python3 tools/build_ch2_mobs.py` + `python3
tools/build_ch3_mobs.py` → nothing changes (your hand files keep every generator hook line; `git status` = only your
files); `python3 tools/check_mboss_pack.py` → 0; `R:tools/dev/sim/az/tests_cm/run_all.sh` from a copy → no failure beyond
README 0-9's known list; `bash HR/tools/checkers.sh <wt>/roguelike` → no new finding (your hand files are checked by
`check_refs`); your suites green; per tick ≤ ≈ 12 commands while the item is held; the standing rules: no negative literals
in `scoreboard players add/remove`, text components never inherit a glyph font, lowercase ids, vanilla sounds only, no tip
text (names, the two verbatim lore lines, numbers, notices).

**⑧ 커밋 (commit)** on `wip/hr-sr` in your worktree only; never push. The message ends with exactly these two lines and
names no model anywhere else:
`<세션이 정해 준 trailer>`
Disk is tight (≈ 1.7 GB free): variant trees under your test folder only, deleted after use.

All stages, always: never hand-edit generated outputs (change the generator, regenerate); the real-game traps — no negative literals in `scoreboard players add/remove`, no glyph-font inheritance, lowercase resource ids, nothing below the floor, no teleport into blocks, held props pointing the right way, one display card per projectile, `summon` does not take the execute rotation; originality (PLAN §1.5): names stay neutral (`scarlet` / `hr`), never name a part, texture, model, function or file after the original game's costume or level pieces; the EULA consent is not recorded, so the local test server is never started.

**⑨ 보고 (report)**: commit, new / edited file counts, the tune table as built (stars 0-3), per-tick cost while held, test
counts, the rendered tooltip / stat item, "loadcheck pending the user's EULA consent", requests (`HR/requests/sr.md`), and
anything S3 must know (the exact give / buff calls, the inventory capacity check you rely on).
